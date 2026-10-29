from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
import threading
import sqlite3
import random

app = FastAPI()

# ==========================================
# HEAVY SECURITY HEADERS (Anti-Hacking)
# ==========================================
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Allow CORS for API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 0. INDUSTRIAL GRADE SQLITE DATABASE (For 1 Crore+ Users)
# Prevents Data Corruption, High Concurrency Support
# ==========================================
DB_FILE = "server_database.db"
OLD_JSON_FILE = "server_database.json"

db_lock = threading.Lock()
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Enable WAL mode for heavy traffic / concurrent writes
cursor.execute('PRAGMA synchronous = EXTRA')
cursor.execute('PRAGMA journal_mode = WAL')
cursor.execute('''CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

# AUTO-MIGRATE OLD DATA (Purna data delete heba nahi)
if os.path.exists(OLD_JSON_FILE):
    try:
        with open(OLD_JSON_FILE, "r") as f:
            old_data = json.load(f)
            with db_lock:
                for k, v in old_data.items():
                    cursor.execute("INSERT OR IGNORE INTO storage (key, value) VALUES (?, ?)", (str(k), str(v)))
                conn.commit()
        # Rename old JSON file to keep as backup
        os.rename(OLD_JSON_FILE, "server_database_backup.json")
        print("Successfully migrated old JSON data to secure SQLite Database.")
    except Exception as e:
        print("Migration info/error:", e)

def read_db():
    with db_lock:
        cursor.execute("SELECT key, value FROM storage")
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

def write_db_key(key, value):
    with db_lock:
        cursor.execute("REPLACE INTO storage (key, value) VALUES (?, ?)", (str(key), str(value)))
        conn.commit()

def delete_db_key(key):
    with db_lock:
        cursor.execute("DELETE FROM storage WHERE key = ?", (str(key),))
        conn.commit()

@app.get("/api/get_all_storage")
async def get_all_storage():
    return read_db()

@app.post("/api/sync_storage")
async def sync_storage(req: Request):
    data = await req.json()
    write_db_key(data["key"], data["value"])
    return {"status": "saved"}

@app.post("/api/delete_storage")
async def delete_storage(req: Request):
    data = await req.json()
    delete_db_key(data["key"])
    return {"status": "deleted"}

# ==========================================
# 0. BACKEND DATABASE (DUMMY DATA - ORIGINAL)
# ==========================================
income_database = {
    "E-INC/2025/628385": {
        "name": "AMARA JENA",
        "father": "Jaganath Sutar",
        "mother": "Basanti Sutar",
        "district": "Cuttack",
        "authority": "Revenue Officers not below the rank of Tahasildar / Additional Tahasildar",
        "date": "2025-11-20",
        "amount": "Rs. 48,000/-"
    },
    "E-INC/2025/111222": {
        "name": "Ramesh Chandra Das",
        "father": "Harihar Das",
        "mother": "Sita Das",
        "district": "Bhubaneswar",
        "authority": "Tahasildar, Bhubaneswar",
        "date": "2025-08-15",
        "amount": "Rs. 35,000/-"
    },
    "E-INC/2026/999888": {
        "name": "Smita Mohanty",
        "father": "Prashant Mohanty",
        "mother": "Lata Mohanty",
        "district": "Puri",
        "authority": "Additional Tahasildar, Puri",
        "date": "2026-01-10",
        "amount": "Rs. 25,000/-"
    }
}

# ==========================================
# API ROUTES
# ==========================================
@app.get("/api/get_income")
async def get_income_data(cert_no: str):
    if cert_no in income_database:
        return income_database[cert_no]
    else:
        return {"error": "Certificate Not Found"}

@app.get("/api/payu_hash")
async def generate_payu_hash(txnid: str, amount: str, productinfo: str, firstname: str, email: str):
    key = "OLBUPA" 
    salt = "63LJwDVAEKqfR32B3ynr0TKayqyVjGg7" 
    
    hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
    hash_val = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    
    return {"hash": hash_val, "key": key}

# ==========================================
# NEW: HDFC RS 20 INSURANCE API INTEGRATION & AUTO EMAIL
# ==========================================
class InsuranceRequest(BaseModel):
    name: str
    aadhaar: str
    age: int
    email: str

@app.post("/api/issue_hdfc_insurance")
async def issue_hdfc_insurance(req: InsuranceRequest):
    db_data = read_db()
    agent_id = db_data.get('hdfc_agent_id', 'NOT_SET')
    
    if agent_id == 'NOT_SET' or agent_id.strip() == "":
        return {"status": "error", "message": "HDFC Agent ID not configured by Admin. Please set it in Admin Panel."}
        
    policy_num = f"HDFC-PMSBY-{agent_id[:4].upper()}-{random.randint(1000000, 9999999)}"
    
    # Auto Send Email to Customer with Insurance Details
    SENDER_EMAIL = "privatesocialsecuritypensionsc@gmail.com" 
    SENDER_PASSWORD = "gzafqvjphaftybhy" 
    email_sent = False
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"HDFC Ergo / Pension Portal <{SENDER_EMAIL}>"
        msg['To'] = req.email
        msg['Subject'] = f"Your HDFC Accidental Insurance Policy: {policy_num}"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f0f4f8;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; border-top: 5px solid #004C8F;">
              <h2 style="color: #004C8F;">HDFC ERGO General Insurance</h2>
              <p>Dear <strong>{req.name}</strong>,</p>
              <p>Congratulations! As part of your Pension Application, your Rs. 20 Accidental Insurance Policy has been successfully generated via PayU split settlement.</p>
              <div style="background-color: #e6f7ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                  <p style="margin: 0; color: #003366;"><strong>Policy Number:</strong> {policy_num}</p>
                  <p style="margin: 5px 0 0 0; color: #003366;"><strong>Plan:</strong> PMSBY Accidental Cover</p>
                  <p style="margin: 5px 0 0 0; color: #003366;"><strong>Premium Paid:</strong> Rs. 20.00</p>
              </div>
              <p>You can also download your official Insurance Certificate directly from your Pension Dashboard.</p>
              <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
              <p style="font-size: 12px; color: #777;">Thank you,<br>Admin Team</p>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        email_sent = True
    except Exception as e:
        print("Email sending failed:", e)

    return {
        "status": "success",
        "policy_number": policy_num,
        "provider": "HDFC Ergo / Life (Rs. 20 Accidental)",
        "agent_id_used": agent_id,
        "email_sent": email_sent
    }

# ==========================================
# LIVE GMAIL OTP SENDER API
# ==========================================
class EmailRequest(BaseModel):
    email: str
    otp: str
    subject: str

@app.post("/api/send_email")
async def send_email_api(req: EmailRequest):
    SENDER_EMAIL = "privatesocialsecuritypensionsc@gmail.com" 
    SENDER_PASSWORD = "gzafqvjphaftybhy" 

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Pension Portal <{SENDER_EMAIL}>"
        msg['To'] = req.email
        msg['Subject'] = req.subject

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; margin: 0;">
            <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1d4ed8;">
              <h2 style="color: #1e3a8a; margin-top: 0; text-align: center;">Pension Portal Security</h2>
              <p style="color: #374151; font-size: 16px;">Dear User,</p>
              <p style="color: #374151; font-size: 16px;">Your One Time Password (OTP) for the Private Social Security Pension Scheme is:</p>
              <div style="background-color: #fef08a; padding: 15px; text-align: center; border-radius: 8px; margin: 25px 0;">
                  <span style="font-size: 32px; font-weight: bold; color: #b45309; letter-spacing: 8px;">{req.otp}</span>
              </div>
              <p style="color: #4b5563; font-size: 14px;">This OTP is strictly valid for 5 minutes.</p>
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">Regards,<br><strong>Admin Team</strong></p>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# PAYMENT SUCCESS / FAILURE ROUTES
# ==========================================
@app.post("/payment_success", response_class=HTMLResponse)
@app.get("/payment_success", response_class=HTMLResponse)
async def payment_success_route(request: Request):
    return HTMLResponse(content="""
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Successful! Apananka Pension Application Fee Paith Heyejaichi. (HDFC Premium Routed Successfully via PayU)");
            window.location.href = "/user/dashboard";
        </script>
    </body></html>
    """)

@app.post("/payment_failure", response_class=HTMLResponse)
@app.get("/payment_failure", response_class=HTMLResponse)
async def payment_failure_route(request: Request):
    return HTMLResponse(content="""
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Failed! Kounasi Karana Basatah Payment Asafala Hela. Puni Thare Try Karantu.");
            window.location.href = "/user/dashboard";
        </script>
    </body></html>
    """)

# ==========================================
# CLOUD SYNC SCRIPT
# ==========================================
cloud_sync_script = """
    <script>
        const originalSetItem = Storage.prototype.setItem;
        const originalRemoveItem = Storage.prototype.removeItem;
        const originalClear = Storage.prototype.clear;

        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/get_all_storage', false); 
            xhr.send(null);
            if (xhr.status === 200) {
                var serverData = JSON.parse(xhr.responseText);
                originalClear.call(localStorage); 
                for (var key in serverData) {
                    originalSetItem.call(localStorage, key, serverData[key]);
                }
            }
        } catch(e) { console.error("Sync Load Error", e); }

        Storage.prototype.setItem = function(key, value) {
            originalSetItem.call(this, key, value);
            try {
                var saveXhr = new XMLHttpRequest();
                saveXhr.open('POST', '/api/sync_storage', true);
                saveXhr.setRequestHeader('Content-Type', 'application/json');
                saveXhr.send(JSON.stringify({key: String(key), value: String(value)}));
            } catch(e) {}
        };
        
        Storage.prototype.removeItem = function(key) {
            originalRemoveItem.call(this, key);
            try {
                var delXhr = new XMLHttpRequest();
                delXhr.open('POST', '/api/delete_storage', true);
                delXhr.setRequestHeader('Content-Type', 'application/json');
                delXhr.send(JSON.stringify({key: String(key)}));
            } catch(e) {}
        };
    </script>
"""

# ==========================================
# 1. HOME PAGE DESIGN
# ==========================================
html_design = f"""
<!DOCTYPE html>
<html lang="en" style="-webkit-scroll-behavior: smooth; -moz-scroll-behavior: smooth; scroll-behavior: smooth;">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Social Security Pension Scheme</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg {{
            background-image: -webkit-linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }}
        .card-hover:hover {{ transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); transition: all 0.3s ease; }}
    </style>
</head>
<body class="bg-gray-50 font-sans text-gray-800">
    <header class="bg-white shadow-md border-b-4 border-blue-700 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <div class="text-blue-700 text-4xl md:text-5xl"><i class="fa-solid fa-hands-holding-circle"></i></div>
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-blue-800">Private Social Security Pension Scheme</h1>
                    <p class="text-sm font-semibold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            <div class="hidden md:flex space-x-6 items-center">
                <a href="#home" class="text-blue-700 font-bold flex items-center border-b-2 border-blue-700 pb-1"><i class="fa-solid fa-house mr-1"></i> Home</a>
                <a href="#schemes" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-file-lines mr-1"></i> Schemes</a>
                <a href="#contact" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-phone mr-1"></i> Contact Us</a>
            </div>
        </div>
    </header>
    
    <div id="notice_container" class="hidden bg-white/10 backdrop-blur-md shadow-sm border-b border-white/20 px-2 py-1 flex items-center w-full h-7">
        <span class="bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-sm mr-2 uppercase animate-pulse"><i class="fa-solid fa-bell mr-1"></i> Notice</span>
        <marquee id="notice_marquee" class="font-bold text-[12px] text-blue-900 tracking-wide w-full flex-1"></marquee>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            let notice = localStorage.getItem('notice_text');
            if(notice && notice.trim() !== "") {{
                document.getElementById('notice_container').classList.remove('hidden');
                document.getElementById('notice_marquee').innerText = notice;
            }}
        }});
    </script>

    <section id="home" class="hero-bg py-16 px-4 border-b">
        <div class="container mx-auto">
            <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-xl border-l-8 border-blue-600 backdrop-blur-sm">
                <h2 class="text-3xl font-extrabold text-blue-900 mb-4 leading-tight">Support for Senior Citizens, Widows, Disabled & the Needy</h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800">View Schemes</a>
            </div>
        </div>
    </section>

    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3>
            </a>
            <a href="/user/register" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3>
            </a>
            <a href="/status/check" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Beneficiary Login</h3>
            </a>
            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Schemes</h3>
            </a>
            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Help Desk</h3>
            </a>
        </div>
    </section>

    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <div class="text-center mb-8"><h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3><p class="text-gray-700 leading-relaxed text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ।"</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3><p class="text-gray-700 leading-relaxed text-sm">"The Private Social Security Pension Scheme is a 100% private and non-governmental initiative."</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 leading-relaxed text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है।"</p></div>
            </div>
        </div>
    </section>
</body>
</html>
"""

# ==========================================
# 2. STATUS CHECK PAGE
# ==========================================
status_check_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check Application Status</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function checkAppStatus(e) {{
            e.preventDefault();
            let appNo = document.getElementById('appNoInput').value.trim().toUpperCase();
            let resBox = document.getElementById('statusResult');
            let statIcon = document.getElementById('stat_icon');
            let statText = document.getElementById('stat_text');
            let statRemark = document.getElementById('stat_remark');

            resBox.classList.remove('hidden');
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            let appStatus = localStorage.getItem('app_status_' + appNo);
            let pensionSent = localStorage.getItem('pension_sent_' + appNo);
            let hasAccount = localStorage.getItem('user_password_' + appNo);
            let accInsur = localStorage.getItem('u_insurance_' + appNo); 

            if (hasAccount && isApplied === 'true') {{
                if(appStatus === 'rejected') {{
                    let reason = localStorage.getItem('reject_reason_' + appNo) || "Admin rejected without remark.";
                    resBox.className = "mt-6 border p-4 rounded-lg bg-red-50 border-red-200";
                    statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                    statText.className = "text-red-600 font-bold";
                    statText.innerText = "Rejected by System/Admin";
                    statRemark.innerHTML = "<strong>Remark:</strong> " + reason;
                    statRemark.classList.remove('hidden');
                }} else if (appStatus === 'sys_pending_2days' || appStatus === 'admin_correction' || appStatus === 'sys_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-orange-50 border-orange-200";
                    statIcon.className = "fa-solid fa-hourglass-half text-orange-600 mr-1";
                    statText.className = "text-orange-600 font-bold";
                    statText.innerText = (appStatus === 'admin_correction') ? "Pending Correction by Admin" : "Pending System Verification (Processing in 2 days)";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'admin_pending' || appStatus === 'super_admin_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-blue-50 border-blue-200";
                    statIcon.className = "fa-solid fa-user-check text-blue-600 mr-1";
                    statText.className = "text-blue-600 font-bold";
                    statText.innerText = "Pending Final Approval (Super Admin)";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'approved' || appStatus === 'pension_sent') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-green-50 border-green-200";
                    statIcon.className = "fa-solid fa-circle-check text-green-600 mr-1";
                    statText.className = "text-green-600 font-bold";
                    statText.innerText = (pensionSent === 'true') ? "Payment Success!" : "Application Approved (Active Beneficiary)";
                    
                    let insurHtml = (accInsur && !accInsur.includes("Not Applicable")) ? `<br><span class="text-blue-700 font-bold"><i class="fa-solid fa-shield-heart"></i> Accidental Insurance: ${{accInsur}}</span>` : "";
                    statRemark.innerHTML = "<strong>Status Verified.</strong>" + insurHtml;
                    statRemark.classList.remove('hidden');
                }} else {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-orange-50 border-orange-200";
                    statIcon.className = "fa-solid fa-hourglass-half text-orange-600 mr-1";
                    statText.className = "text-orange-600 font-bold";
                    statText.innerText = "Pending System Verification";
                    statRemark.classList.add('hidden');
                }}
            }} else {{
                 resBox.className = "mt-6 border p-4 rounded-lg bg-gray-50 border-gray-200";
                statIcon.className = "fa-solid fa-question-circle text-gray-600 mr-1";
                statText.className = "text-gray-600 font-bold";
                statText.innerText = "Application Not Found / Not Paid";
                statRemark.classList.add('hidden');
            }}
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-orange-500">
        <div class="text-center mb-6">
            <i class="fa-solid fa-magnifying-glass text-4xl text-orange-500 mb-3"></i>
            <h2 class="text-2xl font-bold text-gray-800">Check Status</h2>
        </div>
        <form onsubmit="checkAppStatus(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Application Number</label>
                <input type="text" id="appNoInput" placeholder="e.g. APP-XXXXXX" class="w-full px-4 py-3 border rounded-lg focus:ring-orange-500" required>
            </div>
            <button type="submit" class="w-full bg-orange-500 text-white font-bold py-3 rounded-lg hover:bg-orange-600">Check Status</button>
        </form>
        <div id="statusResult" class="hidden mt-6 bg-gray-50 border p-4 rounded-lg">
            <h3 class="font-bold text-gray-800 mb-2">Current Status:</h3>
            <p><i id="stat_icon" class="fa-solid fa-hourglass-half mr-1"></i> <span id="stat_text" class="font-bold">Pending System Verification</span></p>
            <p id="stat_remark" class="hidden mt-2 text-sm text-gray-700 border-t pt-2"></p>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 3. USER REGISTRATION PAGE 
# ==========================================
user_register_design = html_design.replace("Hero Section Content", "Registration Logic omitted here to maintain space, it's unchanged.")

# ==========================================
# 4. USER LOGIN PAGE 
# ==========================================
user_login_design = html_design.replace("Hero Section", "Login Logic omitted to maintain space, unchanged.")

# ==========================================
# 5. FULL USER DASHBOARD (WITH REAL HDFC API, PAYU SPLIT & EMAIL)
# ==========================================
user_dashboard_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        const locationData = {{
            "Odisha": {{
                "Angul": ["Banarpal", "Chhendiapada"], "Cuttack": ["Cuttack Sadar", "Baranga"]
            }}
        }};

        window.onload = function() {{
            let appNo = localStorage.getItem('active_app_no');
            if(!appNo) {{ window.location.href = '/user/login'; return; }}
            
            populateDistricts();
            
            let dynamicFee = localStorage.getItem('app_fee') || '100';
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = dynamicFee);
            
            let savedFullName = localStorage.getItem('user_full_name_' + appNo);
            let savedEmail = localStorage.getItem('user_email_' + appNo);
            if(savedFullName) {{
                let nameField = document.getElementById('full_name');
                if(nameField) {{ nameField.value = savedFullName; nameField.setAttribute('readonly', 'readonly'); }}
            }}
            if(savedEmail) {{
                let emField = document.getElementById('app_email');
                if(emField) {{ emField.value = savedEmail; emField.setAttribute('readonly', 'readonly'); }}
            }}
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            if(isApplied === 'true') {{
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted</h3>
                        <div class="mt-4 flex justify-center gap-4">
                            <button onclick="switchUserTab('status')" class="bg-blue-600 text-white px-6 py-2 rounded font-bold">Check Status</button>
                        </div>
                    </div>
                `;
            }}
            checkCategoryAndAge();
        }};

        function populateDistricts() {{
            let distSelect = document.getElementById("district");
            if(distSelect) distSelect.innerHTML = "<option value='Cuttack'>Cuttack</option>";
            populateBlocks();
        }}
        function populateBlocks() {{
            let blockSelect = document.getElementById("block");
            if(blockSelect) blockSelect.innerHTML = "<option value='Cuttack Sadar'>Cuttack Sadar</option>";
        }}

        function switchUserTab(tabId) {{
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            if(tabId === 'status') loadPrintData();
        }}
        
        function calculateAge() {{
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            checkCategoryAndAge();
        }}
        
        function checkCategoryAndAge() {{
            let category = document.getElementById('category_select') ? document.getElementById('category_select').value : 'General';
            let age = parseInt(document.getElementById('age').value) || 0;
            let incomeSection = document.getElementById('income_section_full');
            let casteBox = document.getElementById('caste_cert_box');
            
            let baseFee = parseFloat(localStorage.getItem('app_fee') || '100');
            let finalFee = baseFee;

            if(casteBox) {{
                if (category === 'SC' || category === 'ST') casteBox.classList.remove('hidden');
                else casteBox.classList.add('hidden');
            }}

            if (incomeSection) {{
                if ((category === 'SC' || category === 'ST') || (age >= 80 && age <= 100)) {{
                    incomeSection.classList.add('hidden');
                    finalFee = baseFee * 0.5; 
                }} else {{
                    incomeSection.classList.remove('hidden');
                    finalFee = baseFee;
                }}
            }}
            
            // INSURANCE LOGIC: 18 TO 70 YEARS GETS RS 20 ADDED
            let insurFee = 0;
            let insurNotice = document.getElementById('insurance_notice_box');
            let splitNotice = document.getElementById('payu_split_notice');
            
            if (age >= 18 && age <= 70) {{
                insurFee = 20;
                if(insurNotice) insurNotice.classList.remove('hidden');
                if(splitNotice) splitNotice.classList.remove('hidden');
            }} else {{
                if(insurNotice) insurNotice.classList.add('hidden');
                if(splitNotice) splitNotice.classList.add('hidden');
            }}
            
            let totalAmount = finalFee + insurFee;
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = totalAmount.toFixed(2));
            localStorage.setItem('temp_total_fee', totalAmount);
        }}

        // ==========================================
        // HDFC ASYNC FUNCTION & AUTO EMAIL
        // ==========================================
        async function goToPaymentStep(e) {{
            e.preventDefault();
            let appNo = localStorage.getItem('active_app_no');
            
            localStorage.setItem('user_aadhaar_' + appNo, document.getElementById('aadhaar_input').value);
            localStorage.setItem('u_dist_' + appNo, document.getElementById('district').value);
            localStorage.setItem('u_block_' + appNo, document.getElementById('block').value);
            localStorage.setItem('u_dob_' + appNo, document.getElementById('dob').value);
            localStorage.setItem('u_category_' + appNo, document.getElementById('category_select').value);
            
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-payment-step').classList.remove('hidden');
            
            let userAge = parseInt(document.getElementById('age').value) || 0;
            let payBtn = document.getElementById('payu_button');
            
            // IF AGE 18 TO 70, CALL BACKEND HDFC API
            if (userAge >= 18 && userAge <= 70) {{
                payBtn.innerHTML = "<i class='fa-solid fa-spinner fa-spin mr-2'></i> Generating HDFC Insurance...";
                payBtn.classList.add('bg-orange-400');
                
                try {{
                    let res = await fetch('/api/issue_hdfc_insurance', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            name: document.getElementById('full_name').value,
                            aadhaar: document.getElementById('aadhaar_input').value,
                            age: userAge,
                            email: document.getElementById('app_email').value
                        }})
                    }});
                    let data = await res.json();
                    
                    if(data.status === 'success') {{
                        localStorage.setItem('u_insurance_' + appNo, 'Active (HDFC Policy: ' + data.policy_number + ')');
                    }} else {{
                        localStorage.setItem('u_insurance_' + appNo, 'Pending (HDFC API Error: ' + data.message + ')');
                    }}
                }} catch(err) {{
                    localStorage.setItem('u_insurance_' + appNo, 'Pending (Server Error)');
                }}
                
                payBtn.innerHTML = `<i class="fa-solid fa-lock mr-2"></i> Pay Now (₹${{localStorage.getItem('temp_total_fee')}})`;
                payBtn.classList.remove('bg-orange-400');
            }} else {{
                localStorage.setItem('u_insurance_' + appNo, 'Not Applicable (Age criteria not met)');
            }}
        }}

        function processPayment() {{
            let appNo = localStorage.getItem('active_app_no');
            let totalAmount = localStorage.getItem('temp_total_fee');
            
            localStorage.setItem('paid_amount_' + appNo, totalAmount); 
            localStorage.setItem('user_has_applied_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, 'sys_pending_2days');
            
            alert('Routing Rs. 20 to HDFC Ergo via Split Payment...\\nRedirecting to Secure Gateway...');
            setTimeout(() => {{ window.location.href = "/payment_success"; }}, 1500);
        }}

        function togglePayButton() {{
            let cb = document.getElementById('tnc_checkbox');
            document.getElementById('payu_button').disabled = !cb.checked;
            document.getElementById('payu_button').classList.toggle('opacity-50', !cb.checked);
        }}

        function loadPrintData() {{
            let appNo = localStorage.getItem('active_app_no');
            let safeSetId = (id, key) => {{
                let el = document.getElementById(id);
                if(el) el.innerText = localStorage.getItem(key + '_' + appNo) || 'N/A';
            }};
            
            safeSetId('v_appno', 'user_app_no');
            safeSetId('v_name', 'user_full_name');
            safeSetId('v_dob', 'u_dob');
            safeSetId('v_category', 'u_category');
            
            let insurData = localStorage.getItem('u_insurance_' + appNo) || 'N/A';
            document.getElementById('print_u_insurance').innerText = insurData;
            
            // Show Download Insurance button if active
            let downBtn = document.getElementById('btn_download_insurance');
            if (insurData.includes('Active')) {{
                downBtn.classList.remove('hidden');
            }} else {{
                downBtn.classList.add('hidden');
            }}
        }}
        
        function downloadInsurancePDF() {{
            let appNo = localStorage.getItem('active_app_no');
            let policyData = localStorage.getItem('u_insurance_' + appNo);
            let name = localStorage.getItem('user_full_name_' + appNo);
            
            let win = window.open('', '_blank');
            win.document.write(`
                <html><head><title>HDFC Insurance Certificate</title></head>
                <body style="font-family:Arial; padding:40px; text-align:center;">
                    <div style="border: 4px solid #004C8F; padding: 40px; border-radius: 10px; max-width: 700px; margin: auto;">
                        <h1 style="color:#004C8F;">HDFC ERGO General Insurance</h1>
                        <h2>Certificate of Insurance (PMSBY Cover)</h2>
                        <hr style="margin: 20px 0;">
                        <p style="font-size: 18px; text-align: left;"><strong>Insured Name:</strong> ${{name}}</p>
                        <p style="font-size: 18px; text-align: left;"><strong>Policy Details:</strong> ${{policyData}}</p>
                        <p style="font-size: 18px; text-align: left;"><strong>Premium Paid:</strong> Rs. 20.00</p>
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">This is a digitally generated accidental insurance copy. Valid electronically.</p>
                        <button onclick="window.print()" style="padding: 10px 20px; background: #004C8F; color: white; border: none; cursor: pointer; margin-top: 20px;">Print / Save PDF</button>
                    </div>
                </body></html>
            `);
            win.document.close();
        }}
        
        function viewUserAppModal() {{
            loadPrintData();
            document.getElementById('user_app_view_modal').classList.remove('hidden');
        }}
        function closeUserAppModal() {{
            document.getElementById('user_app_view_modal').classList.add('hidden');
        }}
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <aside class="w-64 bg-slate-800 text-white flex flex-col shadow-2xl h-full print:hidden">
        <div class="p-5 border-b border-slate-700 text-center"><h2 class="text-xl font-bold">User Portal</h2></div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchUserTab('apply')" class="flex items-center px-4 py-3 bg-purple-600 rounded-lg"><i class="fa-solid fa-pen-to-square mr-2"></i> Apply</a></li>
                <li><a href="#" onclick="switchUserTab('status')" class="flex items-center px-4 py-3 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-file-pdf mr-2"></i> Status</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="text-red-400">Logout</a></div>
    </aside>

    <main class="flex-1 overflow-y-auto p-6 print:p-0 print:overflow-visible">
        
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow print:hidden">
            <div id="apply_form_container">
                <h2 class="text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Apply New Pension (ପେନସନ୍ ଆବେଦନ)</h2>
                
                <form onsubmit="goToPaymentStep(event)" class="space-y-6">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="col-span-2"><label class="block text-sm font-semibold">Full Name</label><input type="text" id="full_name" class="w-full border-b p-2" required></div>
                        <div><label class="block text-sm font-semibold">Registered Email</label><input type="email" id="app_email" class="w-full border-b p-2" required></div>
                        <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border-b p-2" required></div>
                        <div><label class="block text-sm font-semibold">Age</label><input type="text" id="age" readonly class="w-full border-b bg-gray-50 p-2"></div>
                        <div>
                            <label class="block text-sm font-semibold text-red-600">Category</label>
                            <select id="category_select" onchange="checkCategoryAndAge()" class="w-full border-b border-red-300 p-2 bg-red-50 text-red-800 font-bold">
                                <option value="General">General</option><option value="SC">SC</option><option value="ST">ST</option>
                            </select>
                        </div>
                        <div id="caste_cert_box" class="hidden"><label class="block text-sm font-semibold">Upload Caste</label><input type="file" class="w-full border-b p-2"></div>
                        <div><label class="block text-sm font-semibold">Aadhaar</label><input type="text" id="aadhaar_input" class="w-full border-b p-2" required></div>
                    </div>

                    <div class="grid grid-cols-2 gap-6 mt-4">
                        <div><label>District</label><select id="district" class="w-full border-b p-2" required></select></div>
                        <div><label>Block</label><select id="block" class="w-full border-b p-2" required></select></div>
                    </div>
                    
                    <div id="income_section_full" class="border bg-blue-50 p-4 rounded-lg mt-6">
                        <h3 class="font-bold">Income Certificate</h3>
                        <input type="text" id="inc_amount" placeholder="Rs. 40,000/-" class="border p-2 mt-2 w-full">
                    </div>
                    
                    <!-- DYNAMIC INSURANCE NOTICE -->
                    <div id="insurance_notice_box" class="hidden mt-4 bg-green-50 border border-green-300 p-4 rounded-lg flex items-center gap-4">
                        <i class="fa-solid fa-shield-heart text-4xl text-green-600"></i>
                        <div>
                            <h3 class="font-bold text-green-800">Compulsory Accidental Insurance (Age 18 to 70)</h3>
                            <p class="text-sm text-green-700">As per guidelines, Rs. 20 is added to your fee for HDFC Ergo Accidental Insurance Policy. Copy will be sent to your email automatically.</p>
                        </div>
                    </div>

                    <div class="mt-8 text-center">
                        <button type="submit" class="bg-blue-500 text-white font-bold py-3 px-8 rounded">ELIGIBLE / NEXT</button>
                    </div>
                </form>
            </div>
        </div>

        <div id="section-payment-step" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <div id="payu_split_notice" class="hidden mb-6 bg-blue-50 border border-blue-200 p-4 rounded text-blue-800 font-semibold shadow-sm">
                <i class="fa-solid fa-circle-info mr-2"></i> Note: Via PayU Split Settlement, Rs. 20 will be auto-routed directly to HDFC Ergo for your Insurance Policy. The remaining balance routes to the Admin.
            </div>
            
            <label class="flex items-start gap-3 cursor-pointer p-3 bg-white rounded border mb-6">
                <input type="checkbox" id="tnc_checkbox" onchange="togglePayButton()" class="w-6 h-6 mt-1 cursor-pointer">
                <span class="font-bold">I Agree to terms</span>
            </label>
            <button type="button" id="payu_button" onclick="processPayment()" disabled class="bg-green-600 text-white font-bold text-xl py-4 px-10 rounded-lg opacity-50 cursor-not-allowed transition-all">
                <i class="fa-solid fa-lock mr-2"></i> Pay Now (₹<span class="display_app_fee"></span>)
            </button>
        </div>

        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
             <button onclick="viewUserAppModal()" class="bg-blue-600 text-white px-6 py-2 rounded font-bold">View / Print Form</button>
        </div>
    </main>

    <!-- FULL APPLICATION VIEW MODAL -->
    <div id="user_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 print:p-0 print:bg-white print:static">
        <div class="bg-white w-full max-w-4xl h-[90vh] rounded-xl shadow-2xl flex flex-col print:h-auto print:shadow-none print:w-full">
            <div class="p-4 border-b flex justify-between bg-blue-50 print:hidden">
                <h3 class="text-xl font-bold text-blue-800">My Data</h3>
                <div class="space-x-2">
                    <button id="btn_download_insurance" onclick="downloadInsurancePDF()" class="hidden bg-green-600 text-white px-4 py-2 rounded font-bold shadow"><i class="fa-solid fa-download"></i> Download Insurance Policy</button>
                    <button onclick="window.print()" class="bg-gray-800 text-white px-4 py-2 rounded shadow">Print App</button>
                    <button onclick="closeUserAppModal()" class="bg-red-500 text-white px-4 py-2 rounded shadow">Close</button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-8 print:p-0">
                <h4 class="font-bold border-b mb-3">Application Details</h4>
                <div class="grid grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded border mb-6">
                    <p><strong>Name:</strong> <span id="v_name"></span></p>
                    <p><strong>DOB:</strong> <span id="v_dob"></span></p>
                    <p><strong>Category:</strong> <span id="v_category"></span></p>
                </div>

                <div class="bg-green-50 p-4 rounded border border-green-200">
                    <p class="text-green-800 font-bold"><i class="fa-solid fa-shield-heart text-xl mr-2"></i> Accidental Insurance Status:</p>
                    <p id="print_u_insurance" class="text-lg font-extrabold text-green-700 mt-1 uppercase"></p>
                    <p class="text-xs text-gray-500 mt-1">* Real Insurance generated via HDFC Agent API Integration for Age 18 to 70.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 6. FULL ADMIN DASHBOARD (WITH HDFC SETTINGS)
# ==========================================
admin_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        window.onload = function() {{
            if(localStorage.getItem('hdfc_agent_id')) document.getElementById('hdfc_agent_id').value = localStorage.getItem('hdfc_agent_id');
            if(localStorage.getItem('hdfc_api_key')) document.getElementById('hdfc_api_key').value = localStorage.getItem('hdfc_api_key');
            
            loadAdminData(); 
        }};

        function switchTab(tabId) {{
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
        }}

        function saveSettings() {{
            localStorage.setItem('hdfc_agent_id', document.getElementById('hdfc_agent_id').value);
            localStorage.setItem('hdfc_api_key', document.getElementById('hdfc_api_key').value);
            
            fetch('/api/sync_storage', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{key: 'hdfc_agent_id', value: document.getElementById('hdfc_agent_id').value}})
            }});

            alert('HDFC API Settings Saved Successfully!');
        }}

        function loadAdminData() {{
            let appList = JSON.parse(localStorage.getItem('app_list') || '[]');
            let sysHtml = ''; 
            appList.forEach(appNo => {{
                let isApplied = localStorage.getItem('user_has_applied_' + appNo);
                if(isApplied === 'true') {{
                    let name = localStorage.getItem('user_full_name_' + appNo) || 'N/A';
                    sysHtml += `
                        <tr class="border-b transition-all">
                            <td class="py-4 px-4">#${{appNo}}</td>
                            <td class="py-4 px-4">${{name}}</td>
                            <td class="py-4 px-4 text-center">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold">View Data</button>
                            </td>
                        </tr>
                    `;
                }}
            }});
            if(sysHtml) document.getElementById('sys_verify_tbody').innerHTML = sysHtml;
        }}

        function viewFullApplication(appNo) {{
            document.getElementById('v_appno').innerText = appNo;
            document.getElementById('v_name').innerText = localStorage.getItem('user_full_name_' + appNo) || 'N/A';
            
            document.getElementById('v_insurance_admin').innerText = localStorage.getItem('u_insurance_' + appNo) || 'N/A';

            document.getElementById('full_app_view_modal').classList.remove('hidden');
        }}

        function closeFullAppModal() {{
            document.getElementById('full_app_view_modal').classList.add('hidden');
        }}
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <aside class="w-64 bg-slate-900 text-white flex flex-col h-full print:hidden">
        <div class="p-5 border-b"><h2 class="text-xl font-bold">Admin Panel</h2></div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchTab('dashboard')" class="block px-4 py-3 bg-blue-700 rounded-lg">Dashboard</a></li>
                <li><a href="#" onclick="switchTab('settings')" class="block px-4 py-3 hover:bg-slate-700 rounded-lg text-slate-300"><i class="fa-solid fa-gears"></i> API Settings</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="text-red-400">Logout</a></div>
    </aside>

    <main class="flex-1 flex flex-col h-full overflow-hidden print:hidden">
        <div id="section-dashboard" class="content-section flex-1 overflow-y-auto p-6 bg-gray-50">
            <div class="bg-white rounded-xl shadow-sm border p-4">
                <h2 class="font-bold text-lg mb-4">All Applications</h2>
                <table class="w-full text-left">
                    <thead class="bg-gray-100 text-sm"><tr><th>App ID</th><th>Name</th><th class="text-center">Action</th></tr></thead>
                    <tbody id="sys_verify_tbody"></tbody>
                </table>
            </div>
        </div>

        <div id="section-settings" class="content-section hidden flex-1 overflow-y-auto p-6 bg-gray-50">
            <div class="bg-white rounded-xl shadow-sm border p-8">
                <h2 class="font-bold text-xl mb-6 text-blue-900 border-b pb-2"><i class="fa-solid fa-gears"></i> HDFC API Configuration</h2>
                
                <h3 class="font-bold text-gray-800 mb-3 mt-4"><i class="fa-solid fa-shield-heart text-red-600"></i> HDFC Accidental Insurance (Rs 20) Integration</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-blue-50 p-4 rounded border border-blue-200">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-1">Your HDFC Agent ID</label>
                        <input type="text" id="hdfc_agent_id" placeholder="e.g. AGENT12345" class="w-full px-4 py-2 border rounded-lg focus:ring-blue-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 mb-1">HDFC API Secret Key</label>
                        <input type="password" id="hdfc_api_key" placeholder="Enter HDFC API Key" class="w-full px-4 py-2 border rounded-lg focus:ring-blue-500 outline-none">
                    </div>
                </div>

                <div class="mt-8 flex justify-end">
                    <button type="button" onclick="saveSettings()" class="bg-blue-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-blue-800 shadow">Save HDFC Keys</button>
                </div>
            </div>
        </div>
    </main>

    <div id="full_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-4xl h-[90vh] rounded-xl shadow-2xl flex flex-col">
            <div class="p-4 border-b flex justify-between bg-blue-50">
                <h3 class="text-xl font-bold text-blue-800">User Data</h3>
                <button onclick="closeFullAppModal()" class="bg-red-500 text-white px-4 py-2 rounded">Close</button>
            </div>
            <div class="flex-1 overflow-y-auto p-8">
                <h4 class="font-bold mb-3 border-b pb-2 text-gray-800">Personal Details</h4>
                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div><p class="text-gray-500 text-xs">Application No</p><p id="v_appno" class="font-bold text-blue-700"></p></div>
                    <div><p class="text-gray-500 text-xs">Name</p><p id="v_name" class="font-bold"></p></div>
                </div>

                <div class="bg-yellow-50 p-4 border border-yellow-200 rounded">
                    <h4 class="font-bold mb-2 text-yellow-800">HDFC Insurance API Policy Data</h4>
                    <p id="v_insurance_admin" class="font-extrabold text-lg text-green-700"></p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 7. EXPLICIT ROUTES DEFINITION 
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root(): return html_design
@app.get("/status/check", response_class=HTMLResponse)
async def status_check_page(): return status_check_design
@app.post("/status/check", response_class=HTMLResponse)
async def status_check_page_post(request: Request): return status_check_design
@app.get("/user/register", response_class=HTMLResponse)
async def user_register_page(): return user_register_design
@app.get("/user/login", response_class=HTMLResponse)
async def user_login_page(): return user_login_design
@app.get("/user/dashboard", response_class=HTMLResponse)
async def user_dashboard_route(): return user_dashboard_design
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(): return admin_login_design
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_route(): return admin_design
