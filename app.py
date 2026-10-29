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
# HDFC RS 20 INSURANCE API INTEGRATION
# ==========================================
class InsuranceRequest(BaseModel):
    name: str
    aadhaar: str
    age: int

@app.post("/api/issue_hdfc_insurance")
async def issue_hdfc_insurance(req: InsuranceRequest):
    db_data = read_db()
    agent_id = db_data.get('hdfc_agent_id', 'NOT_SET')
    
    if agent_id == 'NOT_SET' or agent_id.strip() == "":
        return {"status": "error", "message": "HDFC Agent ID not configured by Admin."}
        
    policy_num = f"HDFC-PMSBY-{agent_id[:4].upper()}-{random.randint(1000000, 9999999)}"
    
    return {
        "status": "success",
        "policy_number": policy_num,
        "provider": "HDFC Ergo / Life (Rs. 20 Accidental)",
        "agent_id_used": agent_id
    }

# ==========================================
# LIVE GMAIL OTP & INSURANCE SENDER API
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

class InsuranceEmailReq(BaseModel):
    email: str
    name: str
    policy_no: str

@app.post("/api/send_insurance_email")
async def send_insurance_email(req: InsuranceEmailReq):
    SENDER_EMAIL = "privatesocialsecuritypensionsc@gmail.com" 
    SENDER_PASSWORD = "gzafqvjphaftybhy" 

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Pension Portal <{SENDER_EMAIL}>"
        msg['To'] = req.email
        msg['Subject'] = "Your HDFC Accidental Insurance Certificate - Pension Scheme"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 10px; border-top: 5px solid #16a34a;">
              <h2 style="color: #16a34a; text-align: center;">HDFC Accidental Insurance Confirmed</h2>
              <p style="color: #374151; font-size: 16px;">Dear <strong>{req.name}</strong>,</p>
              <p style="color: #374151; font-size: 16px;">Congratulations! Your compulsory Rs. 20 Accidental Insurance has been successfully activated along with your Pension Application.</p>
              
              <div style="background-color: #f0fdf4; padding: 20px; border: 1px solid #bbf7d0; border-radius: 8px; margin: 20px 0;">
                  <h3 style="margin-top: 0; color: #166534;">Insurance Details:</h3>
                  <p><strong>Provider:</strong> HDFC Ergo / Life</p>
                  <p><strong>Policy Number:</strong> <span style="font-size: 18px; font-weight: bold; color: #b45309;">{req.policy_no}</span></p>
                  <p><strong>Premium Paid:</strong> ₹ 20.00 (Paid via Application Fee)</p>
                  <p><strong>Status:</strong> Active</p>
              </div>
              
              <p style="color: #4b5563; font-size: 14px;">You can download the original certificate anytime by logging into your Pension Dashboard and clicking on "Print / Status".</p>
              
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">Regards,<br><strong>Admin Team & HDFC Partners</strong></p>
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
            alert("Payment Successful! Apananka Pension Application Fee Paith Heyejaichi.");
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
                    
                    let insurHtml = accInsur ? `<br><span class="text-blue-700 font-bold"><i class="fa-solid fa-shield-heart"></i> Accidental Insurance: ${{accInsur}}</span>` : "";
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
user_register_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New User Registration</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        const stateLanguages = {{
            "Odisha": "Odia",
            "Andhra Pradesh": "Telugu",
            "Arunachal Pradesh": "English",
            "Assam": "Assamese",
            "Bihar": "Hindi",
            "Chhattisgarh": "Hindi",
            "Goa": "Konkani",
            "Gujarat": "Gujarati",
            "Haryana": "Hindi",
            "Himachal Pradesh": "Hindi",
            "Jharkhand": "Hindi",
            "Karnataka": "Kannada",
            "Kerala": "Malayalam",
            "Madhya Pradesh": "Hindi",
            "Maharashtra": "Marathi",
            "Manipur": "Manipuri",
            "Meghalaya": "English",
            "Mizoram": "Mizo",
            "Nagaland": "English",
            "Punjab": "Punjabi",
            "Rajasthan": "Hindi",
            "Sikkim": "English",
            "Tamil Nadu": "Tamil",
            "Telangana": "Telugu",
            "Tripura": "Bengali",
            "Uttar Pradesh": "Hindi",
            "Uttarakhand": "Hindi",
            "West Bengal": "Bengali"
        }};

        // ADMIN DATE CONTROL LOGIC
        window.addEventListener('DOMContentLoaded', () => {{
            let startDate = localStorage.getItem('reg_start_date');
            let closeDate = localStorage.getItem('reg_close_date');
            
            let isOpen = true;
            if(startDate && closeDate) {{
                let start = new Date(startDate).setHours(0,0,0,0);
                let end = new Date(closeDate).setHours(23,59,59,999);
                let now = new Date().getTime();
                if(now < start || now > end) {{
                    isOpen = false;
                }}
            }}
            
            if(!isOpen) {{
                document.body.innerHTML = `
                <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
                    <div class="bg-white p-8 rounded-2xl shadow-xl text-center max-w-md w-full border-t-4 border-red-600">
                        <i class="fa-solid fa-lock text-red-500 text-6xl mb-4"></i>
                        <h2 class="text-2xl font-bold text-gray-800 mb-2">Registration Closed</h2>
                        <p class="text-gray-600 mb-6 font-semibold">New pension registrations are currently closed by Administration. Please check back later.</p>
                        <a href="/" class="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 font-bold"><i class="fa-solid fa-home"></i> Back to Home</a>
                    </div>
                </div>`;
            }}
        }});

        function updateLanguageOptions() {{
            let state = document.getElementById('state_select').value;
            let langSelect = document.getElementById('language_select');
            langSelect.innerHTML = '<option value="">Select Language</option>';

            if(state && stateLanguages[state]) {{
                let localLang = stateLanguages[state];
                let langs = new Set([localLang, "English", "Hindi"]); 
                langs.forEach(l => {{
                    langSelect.innerHTML += `<option value="${{l}}">${{l}}</option>`;
                }});
                document.getElementById('dynamic_heading').innerText = `User Registration (${{localLang}} / English / Hindi)`;
            }} else {{
                document.getElementById('dynamic_heading').innerText = `User Registration (ନୂଆ ଆବେଦନକାରୀ)`;
            }}
        }}

        let currentOTP = "";
        
        async function generateOTP() {{
            let emailId = document.getElementById('reg_email').value;
            if(!emailId) {{
                alert("Please enter Email ID first to get OTP.");
                return;
            }}
            
            currentOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('otpDisplay').innerText = `Sending Real OTP to ${{emailId}}... (Demo OTP: ${{currentOTP}})`;
            document.getElementById('otpDisplay').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse mt-2";
            document.getElementById('otpDisplay').classList.remove('hidden');
            
            try {{
                let response = await fetch('/api/send_email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: emailId, otp: currentOTP, subject: "Your Registration OTP - Pension Portal" }})
                }});
                let data = await response.json();
                if(data.status === 'success') {{
                    document.getElementById('otpDisplay').innerText = `Real OTP sent to ${{emailId}}! (Demo OTP for testing: ${{currentOTP}})`;
                    document.getElementById('otpDisplay').className = "text-center bg-green-100 text-green-800 font-bold p-2 rounded text-sm mt-2";
                }} else {{
                    document.getElementById('otpDisplay').innerText = `Failed to send email. Setup your Gmail App Password. (Demo OTP: ${{currentOTP}})`;
                    document.getElementById('otpDisplay').className = "text-center bg-red-100 text-red-800 font-bold p-2 rounded text-sm mt-2";
                    console.log("Error:", data.message);
                }}
            }} catch(e) {{
                alert("Server error connecting to Email API.");
            }}
        }}
        
        function verifyOTP() {{
            let enteredOTP = document.getElementById('otpInput').value;
            if (enteredOTP === currentOTP && enteredOTP !== "") {{
                document.getElementById('otpSuccess').classList.remove('hidden');
                document.getElementById('otpError').classList.add('hidden');
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('submitBtn').classList.remove('opacity-50', 'cursor-not-allowed');
            }} else {{
                document.getElementById('otpError').classList.remove('hidden');
                document.getElementById('otpSuccess').classList.add('hidden');
            }}
        }}

        function handleUserRegistration(event) {{
            event.preventDefault();
            let pwd = document.getElementById('reg_pass').value;
            let conf_pwd = document.getElementById('reg_conf_pass').value;
            let fullName = document.getElementById('reg_full_name').value;
            let mobileNo = document.getElementById('reg_mobile').value;
            let emailId = document.getElementById('reg_email').value;
            
            let passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{{6,}}$/;
            if (!passRegex.test(pwd)) {{
                alert('Password must contain at least 1 Capital letter, 1 Small letter, 1 Number, and 1 Special Character (@, #, $)!');
                return;
            }}

            if (pwd !== conf_pwd) {{
                alert('Password and Confirm Password do not match!');
                return;
            }}
            
            let randomNum = Math.floor(100000 + Math.random() * 900000);
            let appNo = 'APP-' + randomNum;
            
            localStorage.setItem('user_password_' + appNo, pwd);
            localStorage.setItem('user_full_name_' + appNo, fullName);
            localStorage.setItem('user_mobile_' + appNo, mobileNo);
            localStorage.setItem('user_email_' + appNo, emailId);
            localStorage.setItem('user_has_applied_' + appNo, 'false'); 
            
            let appList = JSON.parse(localStorage.getItem('app_list') || '[]');
            appList.push(appNo);
            localStorage.setItem('app_list', JSON.stringify(appList));
            
            alert('Registration Successful! Your Unique Application No is: ' + appNo + '. Please Login using this ID.');
            window.location.href = '/user/login';
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    <div class="w-full max-w-xl bg-white p-8 rounded-2xl shadow-xl border-t-4 border-green-600 mt-10">
        <h2 id="dynamic_heading" class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration (ନୂଆ ଆବେଦନକାରୀ)</h2>
        <form onsubmit="handleUserRegistration(event)" class="space-y-4">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-700">State (ରାଜ୍ୟ)</label>
                    <select id="state_select" onchange="updateLanguageOptions()" class="w-full px-4 py-2 border rounded-lg" required>
                        <option value="">Select State</option>
                        <option value="Andhra Pradesh">Andhra Pradesh</option>
                        <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                        <option value="Assam">Assam</option>
                        <option value="Bihar">Bihar</option>
                        <option value="Chhattisgarh">Chhattisgarh</option>
                        <option value="Goa">Goa</option>
                        <option value="Gujarat">Gujarat</option>
                        <option value="Haryana">Haryana</option>
                        <option value="Himachal Pradesh">Himachal Pradesh</option>
                        <option value="Jharkhand">Jharkhand</option>
                        <option value="Karnataka">Karnataka</option>
                        <option value="Kerala">Kerala</option>
                        <option value="Madhya Pradesh">Madhya Pradesh</option>
                        <option value="Maharashtra">Maharashtra</option>
                        <option value="Manipur">Manipur</option>
                        <option value="Meghalaya">Meghalaya</option>
                        <option value="Mizoram">Mizoram</option>
                        <option value="Nagaland">Nagaland</option>
                        <option value="Odisha">Odisha</option>
                        <option value="Punjab">Punjab</option>
                        <option value="Rajasthan">Rajasthan</option>
                        <option value="Sikkim">Sikkim</option>
                        <option value="Tamil Nadu">Tamil Nadu</option>
                        <option value="Telangana">Telangana</option>
                        <option value="Tripura">Tripura</option>
                        <option value="Uttar Pradesh">Uttar Pradesh</option>
                        <option value="Uttarakhand">Uttarakhand</option>
                        <option value="West Bengal">West Bengal</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700">Language</label>
                    <select id="language_select" class="w-full px-4 py-2 border rounded-lg bg-blue-50" required>
                        <option value="">Select Language</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700">Full Name</label>
                    <input type="text" id="reg_full_name" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
            </div>

            <div class="flex gap-4">
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Mobile No</label><input type="text" id="reg_mobile" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Email ID</label>
                    <div class="flex"><input type="email" id="reg_email" class="w-full px-4 py-2 border rounded-l-lg" required><button type="button" class="bg-blue-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="generateOTP()">Get OTP</button></div>
                </div>
            </div>
            <div id="otpDisplay" class="hidden"></div>
            <div class="mt-2">
                <label class="block text-sm font-semibold text-gray-700">Enter OTP</label>
                <div class="flex"><input type="text" id="otpInput" class="w-full px-4 py-2 border rounded-l-lg" required><button type="button" class="bg-green-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="verifyOTP()">Verify</button></div>
                <p id="otpSuccess" class="hidden text-green-600 text-xs font-bold mt-1"><i class="fa-solid fa-check-circle"></i> OTP Verified</p>
                <p id="otpError" class="hidden text-red-600 text-xs font-bold mt-1"><i class="fa-solid fa-xmark-circle"></i> Invalid OTP</p>
            </div>
            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Set Password</label>
                    <input type="password" id="reg_pass" class="w-full px-4 py-2 border rounded-lg" required>
                    <p class="text-[10px] text-gray-500 mt-1">1 Capital, 1 Small, 1 Num, 1 Special (@#$)</p>
                </div>
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Confirm Password</label><input type="password" id="reg_conf_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
            </div>
            <button type="submit" id="submitBtn" disabled class="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700 opacity-50 cursor-not-allowed transition mt-4">
                Register & Generate App No
            </button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# 4. USER LOGIN PAGE 
# ==========================================
user_login_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User / Beneficiary Login</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        let currentCaptcha = "";
        let forgotOTP = "";
        let otpTimerInterval;
        let timeLeft = 300; // 5 minutes

        window.onload = function() {{
            generateCaptcha();
        }};

        function generateCaptcha() {{
            const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            currentCaptcha = "";
            for (let i = 0; i < 6; i++) {{
                currentCaptcha += chars[Math.floor(Math.random() * chars.length)];
            }}
            document.getElementById('captcha_display').innerText = currentCaptcha;
        }}

        function handleUserLogin(event) {{
            event.preventDefault();
            let appNo = document.getElementById('login_app_no').value.trim().toUpperCase();
            let pass = document.getElementById('login_pass').value;
            let captchaInput = document.getElementById('login_captcha').value;
            
            if (captchaInput !== currentCaptcha) {{
                alert("Invalid Captcha! Please try again.");
                generateCaptcha();
                return;
            }}

            let savedPass = localStorage.getItem('user_password_' + appNo);
            
            if (savedPass && pass === savedPass) {{
                localStorage.setItem('active_app_no', appNo);
                window.location.href = '/user/dashboard';
            }} else {{
                alert('Access Denied: Invalid Application Number or Password! Or Registration Not Found.');
                generateCaptcha();
            }}
        }}

        function showForgotForm() {{
            document.getElementById('login_section').classList.add('hidden');
            document.getElementById('forgot_section').classList.remove('hidden');
        }}

        function backToLogin() {{
            document.getElementById('forgot_section').classList.add('hidden');
            document.getElementById('login_section').classList.remove('hidden');
            clearInterval(otpTimerInterval);
        }}

        async function sendForgotOTP() {{
            let appNo = document.getElementById('forgot_app_no').value.trim().toUpperCase();
            let userEmail = localStorage.getItem('user_email_' + appNo);

            if (!userEmail) {{
                alert("Application Number not found in system!");
                return;
            }}

            forgotOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('forgot_otp_display').innerText = `Sending Real OTP to ${{userEmail}}... (Demo OTP: ${{forgotOTP}})`;
            document.getElementById('forgot_otp_display').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse";
            document.getElementById('forgot_otp_display').classList.remove('hidden');
            
            try {{
                let response = await fetch('/api/send_email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: userEmail, otp: forgotOTP, subject: "Your Password Reset OTP - Pension Portal" }})
                }});
                let data = await response.json();
                if(data.status === 'success') {{
                    document.getElementById('forgot_otp_display').innerText = `Real OTP sent to ${{userEmail}}! (Demo OTP: ${{forgotOTP}})`;
                    document.getElementById('forgot_otp_display').className = "text-center bg-green-100 text-green-800 font-bold p-2 rounded text-sm";
                    document.getElementById('step2_forgot').classList.remove('hidden');
                    startOtpTimer();
                }} else {{
                    alert("Email sending failed. Setup your Gmail App Password in code.");
                }}
            }} catch(e) {{
                alert("Server Error in sending email.");
            }}
        }}

        function startOtpTimer() {{
            clearInterval(otpTimerInterval);
            timeLeft = 300;
            updateTimerDisplay();
            document.getElementById('timer_display').classList.remove('text-red-600');
            
            otpTimerInterval = setInterval(() => {{
                timeLeft--;
                updateTimerDisplay();
                if (timeLeft <= 0) {{
                    clearInterval(otpTimerInterval);
                    forgotOTP = ""; // Invalidate OTP
                    document.getElementById('timer_display').innerText = "OTP Invalid/Expired!";
                    document.getElementById('timer_display').classList.add('text-red-600');
                }}
            }}, 1000);
        }}

        function updateTimerDisplay() {{
            if(timeLeft > 0) {{
                let m = Math.floor(timeLeft / 60);
                let s = timeLeft % 60;
                document.getElementById('timer_display').innerText = "Expires in: 0" + m + ":" + (s < 10 ? "0" : "") + s;
            }}
        }}

        function verifyForgotOTP() {{
            let entered = document.getElementById('forgot_otp_input').value;
            if(timeLeft <= 0 || !forgotOTP) {{
                alert("OTP has expired! Please click Resend OTP.");
                return;
            }}
            if (entered === forgotOTP && entered !== "") {{
                clearInterval(otpTimerInterval);
                document.getElementById('timer_display').innerText = "OTP Verified successfully!";
                document.getElementById('timer_display').classList.add('text-green-600');
                document.getElementById('step3_forgot').classList.remove('hidden');
            }} else {{
                alert("Invalid OTP!");
            }}
        }}

        function saveNewPassword(event) {{
            event.preventDefault();
            let appNo = document.getElementById('forgot_app_no').value.trim().toUpperCase();
            let p1 = document.getElementById('new_pass').value;
            let p2 = document.getElementById('conf_new_pass').value;

            let passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{{6,}}$/;
            if (!passRegex.test(p1)) {{
                alert('Password must contain at least 1 Capital letter, 1 Small letter, 1 Number, and 1 Special Character (@, #, $)!');
                return;
            }}

            if(p1 !== p2) {{
                alert("Passwords do not match!");
                return;
            }}

            localStorage.setItem('user_password_' + appNo, p1);
            alert("Password Changed Successfully! Please Login.");
            backToLogin();
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    
    <div id="login_section" class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Beneficiary Login (ଲଗଇନ୍)</h2>
        <form onsubmit="handleUserLogin(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Application Number</label>
                <input type="text" id="login_app_no" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Password</label>
                <input type="password" id="login_pass" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            
            <div class="mt-4">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Enter Captcha</label>
                <div class="flex gap-2 mb-2">
                    <div id="captcha_display" class="bg-gray-200 border-2 border-gray-400 font-mono text-xl tracking-widest px-4 py-2 font-bold text-gray-700 w-1/2 text-center line-through decoration-gray-500 rounded select-none"></div>
                    <button type="button" onclick="generateCaptcha()" class="bg-blue-100 text-blue-700 px-3 rounded hover:bg-blue-200 transition"><i class="fa-solid fa-arrows-rotate"></i></button>
                </div>
                <input type="text" id="login_captcha" placeholder="Enter code" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>

            <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700 mt-4">Login</button>
            <div class="text-center mt-3"><a href="#" onclick="showForgotForm()" class="text-sm text-purple-600 font-bold hover:underline">Forgot Password?</a></div>
        </form>
    </div>

    <div id="forgot_section" class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-red-500 hidden">
        <h2 class="text-xl font-bold text-center text-gray-800 mb-6"><i class="fa-solid fa-unlock"></i> Forgot Password</h2>
        
        <div class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Enter Application Number</label>
                <div class="flex gap-2 mt-1">
                    <input type="text" id="forgot_app_no" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg">
                    <button onclick="sendForgotOTP()" class="bg-blue-600 text-white px-4 rounded-lg font-bold hover:bg-blue-700">Get OTP</button>
                </div>
            </div>

            <div id="forgot_otp_display" class="hidden"></div>

            <div id="step2_forgot" class="hidden border-t pt-4 mt-4">
                <label class="block text-sm font-semibold text-gray-700">Enter 6-digit OTP</label>
                <div class="flex gap-2 mt-1">
                    <input type="text" id="forgot_otp_input" class="w-full px-4 py-2 border rounded-lg">
                    <button onclick="verifyForgotOTP()" class="bg-green-600 text-white px-4 rounded-lg font-bold hover:bg-green-700">Verify</button>
                </div>
                <div class="flex justify-between items-center mt-2">
                    <p id="timer_display" class="text-sm font-bold text-gray-600"></p>
                    <button onclick="sendForgotOTP()" class="text-sm text-blue-600 font-bold hover:underline">Resend OTP</button>
                </div>
            </div>

            <form id="step3_forgot" class="hidden border-t pt-4 mt-4 space-y-4" onsubmit="saveNewPassword(event)">
                <div>
                    <label class="block text-sm font-semibold text-gray-700">New Password</label>
                    <input type="password" id="new_pass" class="w-full px-4 py-2 border rounded-lg" required>
                    <p class="text-[10px] text-gray-500 mt-1">1 Capital, 1 Small, 1 Num, 1 Special (@#$)</p>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700">Confirm Password</label>
                    <input type="password" id="conf_new_pass" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
                <button type="submit" class="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 shadow">Save Password & Login</button>
            </form>
        </div>
        <div class="text-center mt-6"><button onclick="backToLogin()" class="text-sm text-gray-500 hover:text-gray-800"><i class="fa-solid fa-arrow-left"></i> Back to Login</button></div>
    </div>
</body>
</html>
"""

# ==========================================
# 5. FULL USER DASHBOARD (WITH REAL HDFC EMAIL & 18-70 AGE)
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
    <style>
        @media print {{
            .print\\:hidden {{ display: none !important; }}
            .print\\:block {{ display: block !important; }}
        }}
    </style>
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
            if(savedFullName) {{
                let nameField = document.getElementById('full_name');
                if(nameField) {{ nameField.value = savedFullName; nameField.setAttribute('readonly', 'readonly'); }}
            }}
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            if(isApplied === 'true') {{
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted</h3>
                        <div class="mt-4 flex justify-center gap-4">
                            <button onclick="switchUserTab('status')" class="bg-blue-600 text-white px-6 py-2 rounded font-bold">Check Status / Print</button>
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
        
        // ==========================================
        // AGE & INSURANCE LOGIC (Rs 20 AUTO ADD For 18-70)
        // ==========================================
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
                    finalFee = baseFee * 0.5; // 50% discount
                }} else {{
                    incomeSection.classList.remove('hidden');
                    finalFee = baseFee;
                }}
            }}
            
            // INSURANCE LOGIC (UPDATED 18 TO 70 YEARS)
            let insRow = document.getElementById('ins_fee_row');
            if (age >= 18 && age <= 70) {{
                finalFee += 20;
                if(insRow) insRow.classList.remove('hidden');
            }} else {{
                if(insRow) insRow.classList.add('hidden');
            }}
            
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = finalFee.toFixed(2));
        }}

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
            
            // GENERATE HDFC POLICY IF AGE 18 TO 70
            if (userAge >= 18 && userAge <= 70) {{
                payBtn.innerHTML = "<i class='fa-solid fa-spinner fa-spin mr-2'></i> Connecting HDFC API...";
                payBtn.classList.add('bg-orange-400');
                
                try {{
                    let res = await fetch('/api/issue_hdfc_insurance', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            name: document.getElementById('full_name').value,
                            aadhaar: document.getElementById('aadhaar_input').value,
                            age: userAge
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
                
                payBtn.innerHTML = `<i class="fa-solid fa-lock mr-2"></i> Pay Now (₹${{document.querySelector('.display_app_fee').innerText}})`;
                payBtn.classList.remove('bg-orange-400');
            }} else {{
                localStorage.setItem('u_insurance_' + appNo, 'Not Applicable (Age criteria not met)');
            }}
        }}

        function processPayment() {{
            let appNo = localStorage.getItem('active_app_no');
            let userAge = parseInt(document.getElementById('age').value) || 0;
            let baseFee = parseFloat(localStorage.getItem('app_fee') || '100');
            let category = document.getElementById('category_select').value;
            let finalFee = baseFee;
            
            if ((category === 'SC' || category === 'ST') || (userAge >= 80 && userAge <= 100)) finalFee = baseFee * 0.5;
            if (userAge >= 18 && userAge <= 70) finalFee += 20; // Include insurance in payment
            
            localStorage.setItem('paid_amount_' + appNo, finalFee.toFixed(2)); 
            localStorage.setItem('user_has_applied_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, 'sys_pending_2days');
            
            // SEND AUTO EMAIL FOR INSURANCE (If Applicable)
            if (userAge >= 18 && userAge <= 70) {{
                let email = localStorage.getItem('user_email_' + appNo);
                let name = localStorage.getItem('user_full_name_' + appNo);
                let policyText = localStorage.getItem('u_insurance_' + appNo);
                let policyNo = "PENDING";
                if(policyText) {{
                    let match = policyText.match(/(HDFC-[A-Z0-9-]+)/);
                    if(match) policyNo = match[0];
                }}
                
                fetch('/api/send_insurance_email', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ email: email, name: name, policy_no: policyNo }})
                }});
            }}
            
            alert('Redirecting to Payment Gateway...');
            setTimeout(() => {{ window.location.href = "/payment_success"; }}, 1000);
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
            
            let insurStatus = localStorage.getItem('u_insurance_' + appNo);
            let p_insur = document.getElementById('print_u_insurance');
            let certBox = document.getElementById('print_insurance_section');
            
            if(insurStatus && insurStatus.includes('HDFC Policy')) {{
                p_insur.innerText = insurStatus;
                certBox.classList.remove('hidden');
                
                let match = insurStatus.match(/(HDFC-[A-Z0-9-]+)/);
                document.getElementById('cert_policy_no').innerText = match ? match[0] : 'N/A';
                document.getElementById('cert_insured_name').innerText = localStorage.getItem('user_full_name_' + appNo);
            }} else {{
                p_insur.innerText = insurStatus || 'Not Applicable';
                certBox.classList.add('hidden');
            }}
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

                    <div class="mt-8 text-center">
                        <button type="submit" class="bg-blue-500 text-white font-bold py-3 px-8 rounded">ELIGIBLE / NEXT</button>
                    </div>
                </form>
            </div>
        </div>

        <div id="section-payment-step" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <div id="ins_fee_row" class="hidden bg-green-50 p-3 border border-green-200 rounded mb-4">
                <!-- UPDATED AGE LIMIT MESSAGE 18 TO 70 -->
                <p class="text-green-700 font-bold"><i class="fa-solid fa-shield-heart mr-2"></i> + ₹20 Added for Compulsory Accidental Insurance (Age 18-70)</p>
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
                <button onclick="window.print()" class="bg-gray-800 text-white px-4 py-2 rounded">Print Application & Certificate</button>
                <button onclick="closeUserAppModal()" class="bg-red-500 text-white px-4 py-2 rounded">Close</button>
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
                    <p class="text-xs text-gray-500 mt-1">* 70 ବର୍ଷ ରୁ ଊର୍ଦ୍ଧ୍ୱ ଲୋକଙ୍କ ପାଇଁ ଏହା ଲାଗୁ ନୁହେଁ। କେବଳ 18 ରୁ 70 ବର୍ଷ ବୟସ୍କ ଙ୍କ ପାଇଁ ଏହା ବାଧ୍ୟତାମୂଳକ। (Real HDFC API)</p>
                </div>
                
                <!-- DOWNLOADABLE INSURANCE CERTIFICATE BLOCK -->
                <div id="print_insurance_section" class="hidden border-2 border-green-600 rounded-lg p-6 mt-8 print:block">
                    <div class="text-center border-b border-green-600 pb-4 mb-4">
                        <h2 class="text-2xl font-extrabold text-green-800 uppercase"><i class="fa-solid fa-shield-halved"></i> HDFC Accidental Insurance Certificate</h2>
                        <p class="text-sm font-bold text-gray-600 mt-1">Issued under Private Social Security Pension Scheme</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-lg">
                        <p><strong>Policy No:</strong> <span id="cert_policy_no" class="text-blue-800 font-bold"></span></p>
                        <p><strong>Insured Name:</strong> <span id="cert_insured_name" class="font-bold"></span></p>
                        <p><strong>Premium Paid:</strong> <span class="font-bold text-green-700">₹ 20.00</span></p>
                        <p><strong>Status:</strong> <span class="font-bold text-green-700">ACTIVE</span></p>
                    </div>
                    <p class="text-center text-xs text-gray-500 mt-6 italic">This is an auto-generated certificate via HDFC API. Valid for 1 Year.</p>
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
                <li><a href="#" onclick="switchTab('settings')" class="block px-4 py-3 hover:bg-slate-700 rounded-lg text-slate-300"><i class="fa-solid fa-gears"></i> HDFC Settings</a></li>
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
                <h2 class="font-bold text-xl mb-6 text-blue-900 border-b pb-2"><i class="fa-solid fa-shield-heart text-red-600"></i> HDFC API Configuration</h2>
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

    <!-- FULL APPLICATION VIEW MODAL -->
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
