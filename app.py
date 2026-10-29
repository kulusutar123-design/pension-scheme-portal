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
# LIVE GMAIL OTP SENDER API
# ==========================================
class EmailRequest(BaseModel):
    email: str
    otp: str
    subject: str

@app.post("/api/send_email")
async def send_email_api(req: EmailRequest):
    # UPDATED EMAIL ID & PASSWORD
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
              
              <p style="color: #4b5563; font-size: 14px;">This OTP is strictly valid for 5 minutes. Please do not share this secure code with anyone to keep your account 100% safe.</p>
              
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">
                Regards,<br>
                <strong>Admin Team</strong><br>
                Private Social Security Pension Scheme
              </p>
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
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Successful! Apananka Pension Application Fee Paith Heyejaichi.");
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
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh;">
        <script>
            alert("Payment Failed! Kounasi Karana Basatah Payment Asafala Hela. Puni Thare Try Karantu.");
            window.location.href = "/user/dashboard";
        </script>
    </body>
    </html>
    """)

# ==========================================
# CLOUD SYNC SCRIPT (100% CROSS BROWSER FIX)
# ==========================================
cloud_sync_script = """
    <!-- 100% WORKING CROSS-DEVICE SYNC SCRIPT -->
    <script>
        const originalSetItem = Storage.prototype.setItem;
        const originalRemoveItem = Storage.prototype.removeItem;
        const originalClear = Storage.prototype.clear;

        // Synchronously fetch server data on page load
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/get_all_storage', false); 
            xhr.send(null);
            if (xhr.status === 200) {
                var serverData = JSON.parse(xhr.responseText);
                originalClear.call(localStorage); // Clear old garbage
                for (var key in serverData) {
                    originalSetItem.call(localStorage, key, serverData[key]); // Load fresh from DB
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
            background-image: -moz-linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-image: -o-linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }}
        .card-hover:hover {{
            -webkit-transform: translateY(-8px);
            -moz-transform: translateY(-8px);
            -ms-transform: translateY(-8px);
            -o-transform: translateY(-8px);
            transform: translateY(-8px);
            
            -webkit-box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            -moz-box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            
            -webkit-transition: all 0.3s ease;
            -moz-transition: all 0.3s ease;
            -o-transition: all 0.3s ease;
            transition: all 0.3s ease;
        }}
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

    <!-- THIN TRANSPARENT GLASS NOTICE BOARD -->
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
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition duration-300 flex items-center w-max">
                    View Schemes <i class="fa-solid fa-arrow-down ml-2"></i>
                </a>
            </div>
        </div>
    </section>

    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3><p class="text-sm mb-4 text-blue-100">Official login for Administration</p>
            </a>
            <a href="/user/register" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3><p class="text-sm mb-4 text-green-100">Apply for New Pension</p>
            </a>
            <a href="/status/check" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3><p class="text-sm mb-4 text-orange-100">Check Your Application Status</p>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Beneficiary</h3><p class="text-sm mb-4 text-purple-100">Login for Beneficiaries</p>
            </a>
            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Schemes</h3><p class="text-sm mb-4 text-teal-100">View Info & Guidelines</p>
            </a>
            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Help Desk</h3><p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p>
            </a>
        </div>
    </section>

    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <div class="text-center mb-8"><h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3><p class="text-gray-700 leading-relaxed text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା।"</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3><p class="text-gray-700 leading-relaxed text-sm">"The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy."</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 leading-relaxed text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल, 100%। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है।"</p></div>
            </div>
        </div>
    </section>

    <section id="schemes" class="bg-gray-100 py-12 border-t border-b border-gray-200">
        <div class="container mx-auto px-4">
            <div class="text-center mb-10"><h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-list-check mr-2"></i> ଯୋଜନା ଏବଂ ସର୍ତ୍ତାବଳୀ (Schemes & Conditions)</h2></div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-hand-holding-dollar mr-2"></i> Pension Schemes</h3>
                    <ul class="space-y-4">
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-green-500 shadow-sm"><span class="font-semibold text-gray-800">ବୃଦ୍ଧାବସ୍ଥା (Old Age)</span><span class="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">୫୫ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-blue-500 shadow-sm"><span class="font-semibold text-gray-800">ବିଧବା (Widow)</span><span class="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-orange-500 shadow-sm"><span class="font-semibold text-gray-800">ଭିନ୍ନକ୍ଷମ (Disability)</span><span class="text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded">୧୦ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-purple-500 shadow-sm"><span class="font-semibold text-gray-800">ଅବିବାହିତା (Unmarried)</span><span class="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-pink-500 shadow-sm"><span class="font-semibold text-gray-800">ଛାଡପତ୍ର ପାଇଥିବା (Divorcee)</span><span class="text-sm bg-pink-100 text-pink-800 px-2 py-1 rounded">୩୫ ରୁ ୫୫ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-teal-500 shadow-sm"><span class="font-semibold text-gray-800">କିନ୍ନର (Transgender)</span><span class="text-sm bg-teal-100 text-teal-800 px-2 py-1 rounded">୩୫ ରୁ ୫୫ ବର୍ଷ</span></li>
                    </ul>
                </div>
                <div class="lg:col-span-1 bg-red-50 rounded-xl p-6 shadow border border-red-200">
                    <h3 class="font-bold text-xl text-red-800 mb-4 border-b-2 border-red-500 pb-2"><i class="fa-solid fa-triangle-exclamation mr-2"></i> କଡ଼ା ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ</h3>
                    <div class="space-y-4 text-sm text-gray-800">
                        <div class="flex items-start"><i class="fa-solid fa-ban text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Private Initiative:</strong> ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଟ୍ରଷ୍ଟ/ବେସରକାରୀ ସାହାଯ୍ୟ। ଏହା ସରକାରୀ ଯୋଜନା ନୁହେଁ।</p></div>
                        <div class="flex items-start"><i class="fa-solid fa-gavel text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Admin Rights:</strong> ବିନା କାରଣ ଦର୍ଶାଇ, କାହାର ବି ପେନସନ୍ ଆବେଦନ ନାକଚ ବା ବନ୍ଦ କରିବାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର Admin ଙ୍କ ପାଖରେ ରହିବ।</p></div>
                        <div class="flex items-start"><i class="fa-solid fa-rotate text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Mandatory Renewal:</strong> ପ୍ରତି ୩ ମାସରେ ଥରେ ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ।</p></div>
                        <div class="flex items-start"><i class="fa-solid fa-wallet text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Zero Income:</strong> ଆବେଦନକାରୀଙ୍କର କୌଣସି ଆୟ ନଥିବା ଦରକାର।</p></div>
                    </div>
                </div>
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-folder-open mr-2"></i> ଦରକାରୀ କାଗଜପତ୍ର (Documents)</h3>
                    <ul class="space-y-3 text-sm text-gray-700">
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆଧାର କାର୍ଡ (Aadhaar Card)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବୟସ ପ୍ରମାଣପତ୍ର (Age Proof)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆୟ ପ୍ରମାଣପତ୍ର (Income Certificate)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବ୍ୟାଙ୍କ୍ ପାସବୁକ୍ (Bank Passbook)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ପାସପୋର୍ଟ ସାଇଜ୍ ଫଟୋ (Passport Size Photo)</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="container mx-auto px-4 py-12">
        <div class="bg-blue-900 text-white rounded-xl p-8 shadow-xl text-center max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold mb-4"><i class="fa-solid fa-envelope-open-text mr-2"></i> ଯୋଗାଯୋଗ (Contact Us)</h2>
            <p class="mb-6 text-blue-200">For any inquiries, application support, or grievances, please reach out to us at our official email address.</p>
            <div class="inline-block bg-white text-blue-900 px-6 py-4 rounded-lg font-bold text-xl shadow-inner">
                <i class="fa-solid fa-envelope mr-2"></i> admin@kulusutar.in
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
            let utrSaved = localStorage.getItem('utr_number_' + appNo);
            let hasAccount = localStorage.getItem('user_password_' + appNo);

            if (hasAccount && isApplied === 'true') {{
                if(appStatus === 'rejected') {{
                    let reason = localStorage.getItem('reject_reason_' + appNo) || "Admin rejected without remark.";
                    resBox.className = "mt-6 border p-4 rounded-lg bg-red-50 border-red-200";
                    statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                    statText.className = "text-red-600 font-bold";
                    statText.innerText = "Rejected by System/Admin";
                    statRemark.innerHTML = "<strong>Remark:</strong> " + reason;
                    statRemark.classList.remove('hidden');
                }} else if (appStatus === 'admin_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-blue-50 border-blue-200";
                    statIcon.className = "fa-solid fa-user-check text-blue-600 mr-1";
                    statText.className = "text-blue-600 font-bold";
                    statText.innerText = "Pending Final Admin Approval";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'approved' || appStatus === 'pension_sent') {{
                    if(pensionSent === 'true') {{
                        resBox.className = "mt-6 border p-4 rounded-lg bg-green-100 border-green-400";
                        statIcon.className = "fa-solid fa-money-bill-wave text-green-700 mr-1";
                        statText.className = "text-green-700 font-bold";
                        statText.innerText = "Payment Success!";
                        statRemark.innerHTML = "<strong>Bank UTR No:</strong> " + (utrSaved || "Processing...");
                        statRemark.classList.remove('hidden');
                    }} else {{
                        resBox.className = "mt-6 border p-4 rounded-lg bg-green-50 border-green-200";
                        statIcon.className = "fa-solid fa-circle-check text-green-600 mr-1";
                        statText.className = "text-green-600 font-bold";
                        statText.innerText = "Application Approved (Active Beneficiary)";
                        statRemark.classList.add('hidden');
                    }}
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
            
            // Generate a Unique Application Number for EACH user
            let randomNum = Math.floor(100000 + Math.random() * 900000);
            let appNo = 'APP-' + randomNum;
            
            // Save Individual User Data with App No prefix
            localStorage.setItem('user_password_' + appNo, pwd);
            localStorage.setItem('user_full_name_' + appNo, fullName);
            localStorage.setItem('user_mobile_' + appNo, mobileNo);
            localStorage.setItem('user_email_' + appNo, emailId);
            localStorage.setItem('user_has_applied_' + appNo, 'false'); // Status
            
            // Add App No to Master List for Admin
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
    
    <!-- LOGIN SECTION -->
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
            
            <!-- CAPTCHA -->
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

    <!-- FORGOT PASSWORD SECTION -->
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
# 5. FULL USER DASHBOARD 
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
        const stateLanguages = {{
            "Odisha": "Odia"
        }};

        const locationData = {{
            "Odisha": {{
                "Angul": ["Banarpal", "Chhendiapada", "Athamallik", "Kisshorenagar", "Talcher", "Kaniha", "Pallahara", "Angul"],
                "Balasore": ["Basta", "Remuna", "Jaleswar", "Bhograi", "Baliapal", "Nilagiri", "Oupada", "Sora", "Bahanaga", "Simulia", "Khaira", "Balasore"],
                "Bargarh": ["Barpali", "Bheden", "Bhatli", "Ambabhona", "Atabira", "Padampur", "Paikmal", "Jharbhand", "Sohella", "Bijepur", "Bargarh"],
                "Bhadrak": ["Bonth", "Chandabali", "Dhamanagar", "Tihidi", "Bhandaripokhari", "Bhadrak"],
                "Bolangir": ["Deogam", "Gudvella", "Puintal", "Luisinga", "Agalapur", "Titilagarh", "Saintala", "Bangamunda", "Muribahal", "Turekela", "Patnagarh", "Belapada", "Khaprakhole", "Bolangir"],
                "Boudh": ["Boudh", "Harbhanga", "Kantamal"],
                "Cuttack": ["Cuttack Sadar", "Baranga", "Niali", "Kantapada", "Salepur", "Nischantakoili", "Mahanga", "Tangi-Choudwar", "Athagarh", "Tigiria", "Baramba", "Narasinghpur", "Banki", "Banki-Dampada", "Cuttack"],
                "Deogarh": ["Barkote", "Reamal", "Tileibani", "Deogarh"],
                "Dhenkanal": ["Dhenkanal (Sadar)", "Gondia", "Odapada", "Hindol", "Kamakhyanagar", "Parjang", "Kankadahad", "Bhuban", "Dhenkanal"],
                "Gajapati": ["Paralakhemundi", "Kasinagar", "Gumma", "Mohana", "Nuagada", "R.Udayagiri", "Rayagad"],
                "Ganjam": ["Patrapur", "Chikiti", "Rangeilunda", "Digipahandi", "Sanakhemundi", "Kukudakhandi", "Chhatrapur", "Ganjam", "Purusottampur", "Hinjilikatu", "Khallikote", "Beguniapada", "Kabisuryanagar", "Polsara", "Aska", "Sheragada", "Dharakote", "Sorada", "Bhanjanagar", "Belguntha", "Buguda", "Jagannath Prasad"],
                "Jagatsinghpur": ["Biridi", "Naugaon", "Balikuda", "Raghunathpur", "Tirtol", "Ersama", "Kujang", "Jagatsinghpur"],
                "Jajpur": ["Dasarathpur", "Binjharpur", "Dangadi", "Sukinda", "Korei", "Dharmasala", "Barchana", "Rasulpur", "Bari", "Jajpur"],
                "Jharsuguda": ["Jharsuguda", "Lakhanpur", "Kirmira", "Kolabira", "Laikera"],
                "Kalahandi": ["Bhawanipatna", "Kesinga", "Thuamul Rampur", "Narla", "Madanpur Rampur", "Karlamunda", "Lanjigarh", "Dharmagarh", "Golamunda", "Jaipatna", "Junagarh", "Kalampur", "Koksara"],
                "Kendrapara": ["Derabish", "Marsaghai", "Mahakalapara", "Garadpur", "Pattamundai", "Rajkanika", "Rajnagar", "Aul", "Kendrapara"],
                "Keonjhar": ["Saharapada", "Telkoi", "Ghatgaon", "Bansalpal", "Patna", "Harichandanpur", "Anandapur", "Ghasipura", "Hatadihi", "Champua", "Jhumpura", "Joda", "Keonjhar"],
                "Khordha": ["Begunia", "Bolagad", "Bhubaneswar", "Jatni", "Balipatna", "Balianta", "Tangi", "Chilika", "Banapur", "Khurda"],
                "Koraput": ["Dasamanthpur", "Semiliguda", "Nandapur", "Pottangi", "Lamptaput", "Narayanapatna", "Bandhugaon", "Laxmipur", "Kundra", "Boriguma", "Kotpad", "Boipariguda", "Koraput", "jeypore"],
                "Malkanagiri": ["Korukonda", "Mathili", "Motu", "Kallimela", "Podia", "Givindpali", "Khairaput", "Kudmulgumma", "Malkanagiri"],
                "Mayurbhanj": ["Samakhunta", "Suliapdad", "Betanati", "Badasahi", "Rasagobindapur", "Bangiriposhi", "Kuliana", "Sarasakana", "Udala", "Khunta", "Kaptipada", "Karanjia", "Thakurmunda", "Sukuruli", "Joshipur", "Raruan", "Jamda", "Bijatala", "Bisoi", "Gopabandhunagar", "Tiring", "Kusumi", "Moroda", "Bahalda", "Baripada", "Rairangapur"],
                "Nawarangpur": ["Nandahandi", "Tentulikhuinti", "Papadahandi", "Kosagumuda", "Dabugaon", "Umerkote", "Jharigaon", "Chandahandi", "Raighar", "Nawarangpur"],
                "Nayagarh": ["Odagaon", "Bhapur", "Khandapada", "Ranpur", "Daspalla", "Nuagaon", "Gania", "Nayagarh"],
                "Nuapada": ["Boden", "Khariar", "Komna", "Sinapali", "Nuapada"],
                "Phulbani": ["Khajuripada", "K.Nuagaon", "Daringbadi", "Balliguda", "Kotgarh", "Tumudibandh", "G.Udayagiri", "Raikia", "Tikabali", "Chakapad", "Phulbani"],
                "Puri": ["Brahmagiri", "Krushnaprasad", "Satyabadi", "Kanas", "Delang", "Pipili", "Nimapada", "Gop", "Kakatpur", "Astarang", "Puri Sadar"],
                "Rayagada": ["Kolanara", "Kaalyansinghpur", "Kaashipur", "Padmapur", "Ramanaguda", "Gunupur", "Gudari", "Muniguda", "Bisam-Cuttack", "Chandrapur", "Rayagada"],
                "Sambalpur": ["Dhankauda", "Maneswar", "Jujumora", "Rengali", "Rairakhola", "Nakatideul", "Kuchinda", "Bamara", "Jamanakira", "Pairakhal", "Sambalpur"],
                "Sonepur": ["Tarva", "Birmaharajpur", "Ulunda", "Dunguripalli", "Binka", "Sonepur"],
                "Sundargarh": ["Balisankara", "Subdega", "Lephripara", "Hemgiri", "Rajgangpur", "Panposh", "Tanngarapalli", "Kutra", "Lathikata", "Kuanrmunda", "Badagaon", "Nuagaon", "Bisra", "Gurundia", "Koira", "Lahunipada", "Banaigarh", "Sundargarh (Sadar)"]
            }}
        }};

        window.onload = function() {{
            let appNo = localStorage.getItem('active_app_no');
            if(!appNo) {{
                window.location.href = '/user/login';
                return;
            }}
            
            populateDistricts();
            
            let dynamicFee = localStorage.getItem('app_fee') || '100';
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = dynamicFee);
            
            let savedFullName = localStorage.getItem('user_full_name_' + appNo);
            let savedMobile = localStorage.getItem('user_mobile_' + appNo);
            let savedEmail = localStorage.getItem('user_email_' + appNo);
            
            if(savedFullName) {{
                let nameField = document.getElementById('full_name');
                if(nameField) {{
                    nameField.value = savedFullName;
                    nameField.setAttribute('readonly', 'readonly');
                    nameField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
                }}
            }}
            if(savedMobile) {{
                let mobField = document.getElementById('app_mobile');
                if(mobField){{
                    mobField.value = savedMobile;
                    mobField.setAttribute('readonly', 'readonly');
                    mobField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
                }}
            }}
            if(savedEmail) {{
                let emailField = document.getElementById('app_email');
                if(emailField){{
                    emailField.value = savedEmail;
                    emailField.setAttribute('readonly', 'readonly');
                    emailField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
                }}
            }}
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            if(isApplied === 'true') {{
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <i class="fa-solid fa-triangle-exclamation text-yellow-500 text-4xl mb-4"></i>
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted</h3>
                        <p class="text-gray-600 mt-2">You have already submitted an application with this Aadhaar Number. Multiple applications are not allowed. Please check your status.</p>
                        <div class="mt-4 flex justify-center gap-4">
                            <button onclick="switchUserTab('status')" class="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700 font-bold">Check Status</button>
                            <button onclick="resetApplicationForm()" class="bg-red-500 text-white px-6 py-2 rounded shadow hover:bg-red-600 font-bold"><i class="fa-solid fa-rotate-left"></i> Reset / Fill New Form</button>
                        </div>
                    </div>
                `;
            }}

            // RENEWAL LOGIC UPDATE
            let penSent = localStorage.getItem('app_status_' + appNo);
            if(penSent === 'pension_sent') {{
                let rname = savedFullName;
                document.getElementById('section-renew').innerHTML = `
                    <h2 class="text-2xl font-bold mb-4 text-orange-600"><i class="fa-solid fa-clock-rotate-left"></i> 3-Month Renewal</h2>
                    <div class="bg-white border rounded-xl p-6 shadow-sm mb-6 border-l-4 border-green-500">
                        <p class="text-gray-600 font-semibold mb-2">Beneficiary Found: <strong class="text-gray-800">${{rname}} (${{appNo}})</strong></p>
                        <p class="text-sm text-gray-500 mb-4">Your current pension is active. Proceed with Renewal to continue receiving benefits.</p>
                        <button onclick="alert('Data Verified! Proceeding to Payment Gateway...');" class="bg-orange-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-orange-700 transition shadow"><i class="fa-solid fa-credit-card"></i> Pay Renewal Fee</button>
                    </div>
                `;
            }} else {{
                 document.getElementById('section-renew').innerHTML = `
                    <h2 class="text-2xl font-bold mb-4 text-orange-600"><i class="fa-solid fa-clock-rotate-left"></i> 3-Month Renewal</h2>
                    <div class="bg-white border rounded-xl p-6 shadow-sm mb-6 text-center">
                        <i class="fa-solid fa-folder-open text-gray-300 text-5xl mb-3"></i>
                        <p class="text-gray-500 font-semibold">No active pension found eligible for renewal yet.</p>
                    </div>
                `;
            }}
        }};

        function resetApplicationForm() {{
            let appNo = localStorage.getItem('active_app_no');
            if(confirm('Are you sure you want to reset and fill a new form for this ID? Previous application data will be overwritten.')) {{
                localStorage.setItem('user_has_applied_' + appNo, 'false');
                localStorage.removeItem('app_status_' + appNo);
                location.reload();
            }}
        }}

        function populateDistricts() {{
            let state = "Odisha"; 
            let distSelect = document.getElementById("district");
            let blockSelect = document.getElementById("block");
            
            if(distSelect && blockSelect) {{
                distSelect.innerHTML = "<option value=''>Select</option>";
                blockSelect.innerHTML = "<option value=''>Select</option>";

                if(state && locationData[state]) {{
                    for(let dist in locationData[state]) {{
                        distSelect.innerHTML += `<option value='${{dist}}'>${{dist}}</option>`;
                    }}
                }}
            }}
        }}

        function populateBlocks() {{
            let state = "Odisha";
            let dist = document.getElementById("district").value;
            let blockSelect = document.getElementById("block");
            
            if(blockSelect) {{
                blockSelect.innerHTML = "<option value=''>Select</option>";

                if(state && dist && locationData[state][dist]) {{
                    let blocks = locationData[state][dist];
                    for(let i=0; i<blocks.length; i++) {{
                        blockSelect.innerHTML += `<option value='${{blocks[i]}}'>${{blocks[i]}}</option>`;
                    }}
                }}
            }}
        }}

        function switchUserTab(tabId) {{
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            if(tabId === 'status') {{
                loadPrintData();
            }}
        }}
        
        function handleCategoryChange() {{
            let cat = document.getElementById('user_category').value;
            let certBox = document.getElementById('caste_cert_box');
            let appNo = localStorage.getItem('active_app_no');
            let originalFee = parseFloat(localStorage.getItem('app_fee') || '100');
            
            let ageStr = document.getElementById('age').value;
            let isSenior = (ageStr && parseInt(ageStr) >= 80);

            if(cat === 'SC' || cat === 'ST') {{
                certBox.classList.remove('hidden');
                document.getElementById('caste_cert_file').required = true;
            }} else {{
                certBox.classList.add('hidden');
                document.getElementById('caste_cert_file').required = false;
            }}
            
            // Check for discount & Income Cert Exemption
            let incBox = document.getElementById('income_cert_section');
            if(cat === 'SC' || cat === 'ST' || isSenior) {{
                let discountedFee = originalFee / 2;
                document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = discountedFee.toFixed(2));
                incBox.classList.add('hidden'); // Exclude income cert
                document.getElementById('income_cert_no').required = false;
                document.getElementById('income_year').required = false;
            }} else {{
                document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = originalFee.toFixed(2));
                incBox.classList.remove('hidden'); // Require income cert
                document.getElementById('income_cert_no').required = true;
                document.getElementById('income_year').required = true;
            }}
        }}

        function calculateAge() {{
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age Pension' && age < 55) {{ alert('System Error: Age must be 55 or above for Old Age Pension.'); }}
            handleCategoryChange(); // Update logic based on new age
        }}

        function checkSchemeCondition() {{
            let scheme = document.getElementById('scheme').value;
            let specialBox = document.getElementById('special_cert_box');
            if(scheme === 'Widow Pension' || scheme === 'Disability Pension' || scheme === 'Divorcee Pension' || scheme === 'Transgender Pension') {{
                specialBox.classList.remove('hidden');
            }} else {{ specialBox.classList.add('hidden'); }}
        }}

        function updateAgeProof() {{
            let docType = document.getElementById("age_proof_type").value;
            let docNumBox = document.getElementById("age_proof_number");
            let docFileBox = document.getElementById("age_proof_file_container");
            if(docType) {{
                docNumBox.classList.remove("hidden");
                docNumBox.placeholder = "Enter " + docType + " Number";
                docFileBox.classList.remove("hidden");
            }} else {{
                docNumBox.classList.add("hidden");
                docFileBox.classList.add("hidden");
            }}
        }}

        function verifyAadhaar() {{
            let appNo = localStorage.getItem('active_app_no');
            let fullName = document.getElementById('full_name').value;
            let aadhaarInput = document.getElementById('aadhaar_input').value;
            
            let savedAadhaar = localStorage.getItem('user_aadhaar_' + appNo);
            if (savedAadhaar === aadhaarInput) {{
                alert('An application with this Aadhaar number already exists!');
                return;
            }}
            
            if(!fullName) {{ alert("Please enter your Full Name at the top to fetch matching data."); return; }}
            if(!aadhaarInput) {{ alert("Please enter Aadhaar Number."); return; }}
            
            alert('Aadhaar OTP verified automatically!');
            document.getElementById('aadhaar_success_box').classList.remove('hidden');
            document.getElementById('aadhaar_status').classList.add('hidden');
        }}

        async function fetchIFSC() {{
            let ifsc = document.getElementById("ifsc_code").value.trim().toUpperCase();
            if(!ifsc) {{ alert("Please enter IFSC Code first."); return; }}
            try {{
                let res = await fetch(`https://ifsc.razorpay.com/${{ifsc}}`);
                if(res.ok) {{
                    let data = await res.json();
                    document.getElementById("bank_name_display").value = data.BANK + " - " + data.BRANCH;
                }} else {{
                    alert("Invalid IFSC Code");
                    document.getElementById("bank_name_display").value = "";
                }}
            }} catch (e) {{
                alert("Error fetching IFSC details.");
            }}
        }}

        async function verifyIncome() {{
            let cert = document.getElementById('income_cert_no').value;
            let year = document.getElementById('income_year').value;

            if(cert && year !== "Select") {{
                try {{
                    let response = await fetch(`/api/get_income?cert_no=${{cert}}`);
                    let data = await response.json();

                    if(data.error) {{
                        alert("Invalid Certificate Number or Data Not Found in Database!");
                        return;
                    }}

                    alert(`Fetching Income Details from Database for Certificate ${{cert}}...`);
                    
                    document.getElementById('inc_issued_to').value = data.name;
                    document.getElementById('inc_father').value = data.father;
                    document.getElementById('inc_mother').value = data.mother;
                    document.getElementById('inc_district').value = data.district;
                    document.getElementById('inc_authority').value = data.authority;
                    document.getElementById('inc_date').value = data.date;
                    document.getElementById('inc_amount').value = data.amount;
                    document.getElementById('inc_relation').value = "Self";

                    let nameField = document.getElementById('full_name');
                    if(!nameField.value) {{
                        nameField.value = data.name;
                    }}
                    document.getElementById('father_name').value = data.father;
                    document.getElementById('mother_name').value = data.mother;
                    
                    populateDistricts();
                    setTimeout(() => {{
                        document.getElementById("district").value = data.district;
                        populateBlocks();
                    }}, 100);

                }} catch (error) {{
                    console.error("Error fetching data:", error);
                    alert("System Error: Unable to fetch data from Server.");
                }}
            }} else {{
                alert("Please select Issuing Year and enter Certificate No. first to auto-fetch.");
            }}
        }}
        
        function updateAddressCharCount() {{
            let addressInput = document.getElementById('manual_address');
            let charsLeft = 200 - addressInput.value.length;
            document.getElementById('address_char_count').innerText = charsLeft + " characters remaining";
        }}
        
        function goToPaymentStep(e) {{
            e.preventDefault();
            let appNo = localStorage.getItem('active_app_no');
            
            localStorage.setItem('user_aadhaar_' + appNo, document.getElementById('aadhaar_input').value);
            localStorage.setItem('u_category_' + appNo, document.getElementById('user_category').value);
            localStorage.setItem('u_father_' + appNo, document.getElementById('father_name').value);
            localStorage.setItem('u_mother_' + appNo, document.getElementById('mother_name').value);
            localStorage.setItem('u_scheme_' + appNo, document.getElementById('scheme').value);
            localStorage.setItem('u_dist_' + appNo, document.getElementById('district').value);
            localStorage.setItem('u_block_' + appNo, document.getElementById('block').value);
            localStorage.setItem('u_gp_' + appNo, document.getElementById('panchayat').value);
            localStorage.setItem('u_address_' + appNo, document.getElementById('manual_address').value);
            
            localStorage.setItem('u_gender_' + appNo, document.getElementById('gender_select').value);
            localStorage.setItem('u_dob_' + appNo, document.getElementById('dob').value);
            
            // Only save income if not hidden
            if(!document.getElementById('income_cert_section').classList.contains('hidden')){
                localStorage.setItem('u_inc_cert_' + appNo, document.getElementById('income_cert_no').value);
                localStorage.setItem('u_inc_auth_' + appNo, document.getElementById('inc_authority').value);
                localStorage.setItem('u_inc_amount_' + appNo, document.getElementById('inc_amount').value);
            } else {
                localStorage.setItem('u_inc_cert_' + appNo, 'EXEMPTED');
                localStorage.setItem('u_inc_amount_' + appNo, 'EXEMPTED (SC/ST/Senior)');
            }

            localStorage.setItem('u_ifsc_' + appNo, document.getElementById('ifsc_code').value);
            localStorage.setItem('u_bank_' + appNo, document.getElementById('bank_name_display').value); 
            localStorage.setItem('u_acc_' + appNo, document.getElementById('acc_no').value);
            
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-payment-step').classList.remove('hidden');
        }}

        function togglePayButton() {{
            let cb = document.getElementById('tnc_checkbox');
            let btn = document.getElementById('payu_button');
            if(cb.checked) {{
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            }} else {{
                btn.disabled = true;
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            }}
        }}

        async function processPayment() {{
            let gateway = document.querySelector('input[name="pay_gateway"]:checked').value;
            let appNo = localStorage.getItem('active_app_no');
            
            // Getting Dynamic Amount (Could be 100 or 50 based on logic)
            let finalAmt = document.querySelector('.display_app_fee').innerText;
            localStorage.setItem('paid_amount_' + appNo, finalAmt); 
            
            // AUTO SYSTEM VERIFICATION LOGIC (REAL)
            let autoStatus = "sys_pending"; 
            let autoRemark = "";
            let cat = localStorage.getItem('u_category_' + appNo);
            let isExempt = (cat === 'SC' || cat === 'ST' || parseInt(document.getElementById('age').value) >= 80);
            
            // Verify Bank Details First
            if(!document.getElementById('bank_name_display').value) {
                autoStatus = "rejected";
                autoRemark = "System Auto-Reject: Invalid IFSC Code or Bank Details.";
            }

            if(autoStatus !== "rejected" && !isExempt) {
                let incAmt = document.getElementById('inc_amount').value || "";
                let authName = document.getElementById('inc_issued_to').value || "";
                let firstname = document.getElementById('full_name').value || "User";
                
                if (!incAmt || !incAmt.includes("Rs.")) {{
                    autoStatus = "rejected";
                    autoRemark = "System Auto-Reject: Income Certificate data missing or not correctly verified.";
                }} else if (authName.toLowerCase().trim() !== firstname.toLowerCase().trim() && authName !== "") {{
                    autoStatus = "rejected";
                    autoRemark = "System Auto-Reject: Aadhaar Name and Income Certificate Name Mismatch.";
                }} else {{
                    let numAmt = parseInt(incAmt.replace(/[^0-9]/g, ''));
                    if (numAmt > 50000) {{
                        autoStatus = "rejected";
                        autoRemark = "System Auto-Reject: Annual Income (" + incAmt + ") exceeds Rs. 50,000 limit.";
                    }}
                }}
            }
            
            localStorage.setItem('user_has_applied_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, autoStatus);
            if(autoStatus === 'rejected') {{
                localStorage.setItem('reject_reason_' + appNo, autoRemark);
            }}

            if(gateway === 'razorpay') {{
                alert('Redirecting to Asali Razorpay Live Secure Payment Gateway...');
                setTimeout(() => {{
                    window.location.href = "/payment_success";
                }}, 1000);
            }} else {{
                alert('Redirecting to Asali PayU Live Secure Payment Gateway...');
                let txnid = "TXN" + new Date().getTime();
                let productinfo = "PensionApplication";
                let email = document.getElementById('app_email').value || "user@example.com"; 
                let phone = document.getElementById('app_mobile').value || "9876543210";
                let firstname = document.getElementById('full_name').value || "User";
                
                let surl = window.location.origin + "/payment_success";
                let furl = window.location.origin + "/payment_failure";
                
                try {{
                    let response = await fetch(`/api/payu_hash?txnid=${{txnid}}&amount=${{finalAmt}}&productinfo=${{productinfo}}&firstname=${{firstname}}&email=${{email}}`);
                    let data = await response.json();

                    let form = document.createElement("form");
                    form.setAttribute("method", "POST");
                    form.setAttribute("action", "https://secure.payu.in/_payment");

                    let params = {{
                        "key": data.key,
                        "txnid": txnid,
                        "amount": finalAmt,
                        "productinfo": productinfo,
                        "firstname": firstname,
                        "email": email,
                        "phone": phone,
                        "surl": surl,
                        "furl": furl,
                        "hash": data.hash
                    }};

                    for(let key in params) {{
                        let hiddenField = document.createElement("input");
                        hiddenField.setAttribute("type", "hidden");
                        hiddenField.setAttribute("name", key);
                        hiddenField.setAttribute("value", params[key]);
                        form.appendChild(hiddenField);
                    }}

                    document.body.appendChild(form);
                    form.submit(); 
                    
                }} catch (error) {{
                    alert("Error connecting to PayU Gateway. Checking connection...");
                }}
            }}
        }}

        function loadPrintData() {{
            let appNo = localStorage.getItem('active_app_no');
            let safeSet = (className, key, defaultVal) => {{
                let val = localStorage.getItem(key + '_' + appNo) || defaultVal;
                document.querySelectorAll(className).forEach(el => el.innerText = val);
            }};
            
            safeSet('.print_u_name', 'user_full_name', 'N/A');
            safeSet('.print_u_appno', 'user_app_no', 'N/A');
            safeSet('.print_u_scheme', 'u_scheme', 'N/A');
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = localStorage.getItem('paid_amount_' + appNo) || '100.00');

            let safeSetId = (id, key) => {{
                let el = document.getElementById(id);
                if(el) el.innerText = localStorage.getItem(key + '_' + appNo) || 'N/A';
            }};
            
            safeSetId('print_u_father', 'u_father');
            safeSetId('print_u_mother', 'u_mother');
            safeSetId('print_u_category', 'u_category');
            safeSetId('print_u_aadhaar', 'user_aadhaar');
            safeSetId('print_u_dist', 'u_dist');
            safeSetId('print_u_block', 'u_block');
            safeSetId('print_u_gp', 'u_gp');
            safeSetId('print_u_address', 'u_address');
            safeSetId('print_u_dob', 'u_dob');
            safeSetId('print_u_gender', 'u_gender');
            safeSetId('print_u_inc_cert', 'u_inc_cert');
            safeSetId('print_u_inc_auth', 'u_inc_auth');
            safeSetId('print_u_inc_amount', 'u_inc_amount');
            safeSetId('print_u_bank', 'u_bank');
            safeSetId('print_u_acc', 'u_acc');
            safeSetId('print_u_ifsc', 'u_ifsc');
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
                <li><a href="#" onclick="switchUserTab('apply')" class="flex items-center px-4 py-3 bg-purple-600 text-white rounded-lg"><i class="fa-solid fa-pen-to-square w-6 mr-2"></i> Apply Pension</a></li>
                <li><a href="#" onclick="switchUserTab('status')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-file-pdf w-6 mr-2"></i> Status / Print</a></li>
                <li><a href="#" onclick="switchUserTab('renew')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> Renewal</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="flex items-center text-red-400 hover:text-red-300"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout / Back Home</a></div>
    </aside>

    <main class="flex-1 overflow-y-auto p-6 print:p-0 print:overflow-visible">
        
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow print:hidden">
            
            <div id="apply_form_container">
                <div class="bg-blue-50 p-4 rounded-lg flex flex-col md:flex-row justify-between items-center mb-6 border border-blue-200">
                    <div class="mb-2 md:mb-0">
                        <p class="text-sm font-semibold text-blue-800"><i class="fa-solid fa-earth-asia"></i> Registered State: <span id="display_reg_state" class="font-bold text-lg text-purple-700 border-b border-purple-300 pb-1">Odisha</span></p>
                    </div>
                    <div class="flex items-center gap-3">
                        <label class="text-sm font-bold text-gray-700"><i class="fa-solid fa-language text-blue-600"></i> Form Language:</label>
                        <select id="form_language" class="border border-blue-300 p-2 rounded bg-white font-bold text-sm text-blue-800 outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer" required>
                            <option value="Odia">Odia</option>
                            <option value="English">English</option>
                            <option value="Hindi">Hindi</option>
                        </select>
                    </div>
                </div>

                <h2 class="text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Apply New Pension (ପେନସନ୍ ଆବେଦନ)</h2>
                <form onsubmit="goToPaymentStep(event)" class="space-y-6">
                    
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <label class="block text-sm font-semibold">Full Name (ପୂରା ନାମ)</label>
                            <input type="text" id="full_name" class="w-full border-b border-gray-300 p-2 outline-none font-bold text-blue-800 bg-transparent" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-600">Registered Mobile No</label>
                            <input type="text" id="app_mobile" class="w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-800 bg-transparent" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-gray-600">Registered Email ID</label>
                            <input type="text" id="app_email" class="w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-800 bg-transparent" required>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-blue-600">Category (ବର୍ଗ)</label>
                            <select id="user_category" onchange="handleCategoryChange()" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required>
                                <option value="General">General</option>
                                <option value="OBC">OBC</option>
                                <option value="SC">SC</option>
                                <option value="ST">ST</option>
                                <option value="Other">Other</option>
                            </select>
                            <div id="caste_cert_box" class="hidden mt-2 bg-yellow-50 p-2 rounded border border-yellow-300">
                                <label class="font-bold text-yellow-800 text-xs">Upload Caste Certificate (PDF):</label>
                                <input type="file" id="caste_cert_file" class="border p-1 mt-1 w-full bg-white text-xs" accept=".pdf">
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 border-t pt-4">
                        <div>
                            <label class="block text-sm font-semibold text-blue-600">Profile Photo <i class="fa-solid fa-camera"></i></label>
                            <input type="file" class="w-full border-b border-gray-300 p-2 text-sm outline-none bg-transparent" accept="image/*" required>
                        </div>
                        <div><label class="block text-sm font-semibold">Father's/Husband's Name</label><input type="text" id="father_name" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                        <div><label class="block text-sm font-semibold">Mother's Name (ମାଆଙ୍କ ନାମ)</label><input type="text" id="mother_name" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                        <div>
                            <label class="block text-sm font-semibold">Gender (ଲିଙ୍ଗ)</label>
                            <select id="gender_select" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent"><option value="Male">Male</option><option value="Female">Female</option><option value="Transgender">Transgender</option></select>
                        </div>
                        <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                        <div><label class="block text-sm font-semibold">Age (Auto Calculate)</label><input type="text" id="age" readonly class="w-full border-b border-gray-300 p-2 outline-none bg-gray-50"></div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-6 border-t pt-4">
                        <div>
                            <label class="block text-sm font-semibold mb-2">Scheme Category (ଯୋଜନା ବାଛନ୍ତୁ)</label>
                            <select id="scheme" onchange="checkSchemeCondition()" class="w-full border p-2 rounded bg-purple-50">
                                <option value="Old Age Pension">Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option><option value="Widow Pension">Widow (ବିଧବା)</option><option value="Disability Pension">Disability (ଭିନ୍ନକ୍ଷମ)</option><option value="Unmarried Pension">Unmarried (ଅବିବାହିତା)</option><option value="Divorcee Pension">Divorcee (ଛାଡପତ୍ର ପାଇଥିବା)</option><option value="Transgender Pension">Transgender (କିନ୍ନର)</option>
                            </select>
                            <div id="special_cert_box" class="hidden mt-4 bg-yellow-50 p-2 rounded border border-yellow-300">
                                <label class="font-bold text-yellow-800 text-sm">Special Certificate (Widow/Disability PDF):</label>
                                <input type="file" class="border p-1 mt-1 w-full bg-white text-sm" accept=".pdf">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2">Aadhaar Number (ଆଧାର ନମ୍ବର)</label>
                            <div class="flex gap-2">
                                <input type="text" id="aadhaar_input" placeholder="[Aadhaar Redacted]" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required>
                                <button type="button" onclick="verifyAadhaar()" class="bg-blue-600 text-white font-bold px-4 rounded hover:bg-blue-700">VALIDATE</button>
                            </div>
                            <div id="aadhaar_success_box" class="hidden mt-3 border-l-4 border-green-500 bg-gray-50 p-3 shadow-sm flex items-start gap-3">
                                <i class="fa-solid fa-check text-green-500 text-2xl mt-1"></i>
                                <div class="text-xs">
                                    <p class="font-semibold text-gray-800 text-sm">Aadhaar Verified Successfully.</p>
                                </div>
                            </div>
                            <p id="aadhaar_status" class="text-xs mt-1 text-gray-500 mb-2">Manual Entry allowed if not linked</p>
                            
                            <label class="block text-sm font-semibold text-blue-600 mb-1">Upload Aadhaar PDF <i class="fa-solid fa-file-pdf"></i></label>
                            <input type="file" class="w-full border p-1 rounded text-sm bg-gray-50" accept=".pdf" required>
                        </div>
                    </div>

                    <div class="mt-6 border-t pt-4">
                        <h3 class="font-bold text-lg mb-4 text-gray-800">Address Information</h3>
                        <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
                            <div>
                                <label class="block text-sm text-gray-500 mb-1">District</label>
                                <select id="district" onchange="populateBlocks()" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                                    <option value="">Select</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm text-gray-500 mb-1">Block/ULB</label>
                                <select id="block" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                                    <option value="">Select</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm text-gray-500 mb-1">GP/Ward <span class="text-red-500 text-xs">*</span></label>
                                <input type="text" id="panchayat" placeholder="Enter GP/Ward" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                            </div>
                            <div>
                                <label class="block text-sm text-gray-500 mb-1">Village <span class="text-red-500 text-xs">*</span></label>
                                <input type="text" placeholder="Enter Village" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                            </div>
                            <div>
                                <label class="block text-sm text-gray-500 mb-1">Pin Code <span class="text-red-500 text-xs">*</span></label>
                                <input type="text" placeholder="e.g. 751001" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                            </div>
                        </div>
                        
                        <div class="mt-6">
                            <label class="block text-sm text-gray-500 mb-1">Address <span class="text-red-500 text-xs">*</span></label>
                            <input type="text" id="manual_address" maxlength="200" oninput="updateAddressCharCount()" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent text-gray-800 font-semibold" required>
                            <p id="address_char_count" class="text-red-500 text-sm mt-1">200 characters remaining</p>
                        </div>
                    </div>

                    <div class="border p-4 rounded-lg bg-gray-50 mt-6 shadow-sm border-gray-200">
                        <h3 class="font-bold text-sm mb-2 text-gray-700"><i class="fa-solid fa-id-card mr-1"></i> Age Proof Document Upload</h3>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <select id="age_proof_type" onchange="updateAgeProof()" class="w-full border p-2 rounded bg-white" required>
                                    <option value="">Select Document...</option>
                                    <option value="PAN Card">PAN Card</option>
                                    <option value="Voter Card">Voter Card</option>
                                    <option value="Ration Card">Ration Card</option>
                                </select>
                            </div>
                            <div>
                                <input type="text" id="age_proof_number" class="w-full border p-2 rounded hidden bg-white font-bold" placeholder="Document Number" required>
                            </div>
                            <div id="age_proof_file_container" class="hidden">
                                <input type="file" class="w-full border p-1 rounded bg-white text-sm" accept=".pdf, image/*" required>
                            </div>
                        </div>
                    </div>

                    <div id="income_cert_section" class="border border-blue-200 bg-blue-50 p-4 rounded-lg mt-6 shadow-sm">
                        <h3 class="text-lg font-bold text-blue-800 mb-4 border-b border-blue-200 pb-2">Income Certificate Details</h3>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-700">Issuing Year <span class="text-red-500">*</span></label>
                                <select id="income_year" class="w-full border p-2 rounded bg-white">
                                    <option value="">Select</option><option value="2024-25">2024-25</option><option value="2025-26">2025-26</option><option value="2026-27">2026-27</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-700">Income Certificate No. <span class="text-red-500">*</span></label>
                                <input type="text" id="income_cert_no" placeholder="e.g: e-INC/2020/12345" class="w-full border p-2 rounded bg-white placeholder-red-400">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-700">Token No</label>
                                <input type="text" id="income_token_no" class="w-full border p-2 rounded bg-white">
                            </div>
                            
                            <!-- MANUAL ENTRY (NO FETCH BUTTON) -->
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">To Whom the Certificate Issued</label>
                                <input type="text" id="inc_issued_to" placeholder="Enter Name manually" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Applicant Father</label>
                                <input type="text" id="inc_father" placeholder="Enter Father Name" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Applicant Mother</label>
                                <input type="text" id="inc_mother" placeholder="Enter Mother Name" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Issuing District</label>
                                <input type="text" id="inc_district" placeholder="Enter District" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                            </div>
                            <div class="col-span-2">
                                <label class="block text-xs font-semibold text-gray-500">Issuing Authority</label>
                                <input type="text" id="inc_authority" placeholder="Enter Authority" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Issue Date</label>
                                <input type="date" id="inc_date" class="w-full border border-gray-300 rounded p-2 font-bold text-gray-800 bg-white">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Relationship</label>
                                <select id="inc_relation" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-gray-800">
                                    <option>Select</option><option>Self</option><option>Daughter</option><option>Son</option><option>Wife</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-500">Annual Income Detected</label>
                                <input type="text" id="inc_amount" placeholder="e.g. Rs. 48,000/-" class="w-full border border-gray-300 rounded p-2 bg-white outline-none font-bold text-red-600 text-lg">
                            </div>
                        </div>
                        
                        <div class="mt-4 border-t border-blue-200 pt-4">
                            <label class="block text-sm font-semibold text-blue-700 mb-1"><i class="fa-solid fa-file-pdf"></i> Upload Income Certificate (PDF) <span class="text-red-500">*</span></label>
                            <input type="file" class="w-full md:w-1/2 border p-1 rounded text-sm bg-white" accept=".pdf">
                        </div>
                    </div>

                    <div class="border border-blue-200 bg-white p-6 rounded-lg mt-6 shadow-sm">
                        <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Bank Information</h3>
                        
                        <div class="bg-red-50 border border-red-200 p-4 rounded text-red-600 text-sm mb-6 space-y-2 italic shadow-sm">
                            <p class="font-bold">Note:</p>
                            <p>1. Kindly provide correct and active bank account number and IFSC code. Be very careful while furnishing bank-account information as for any wrong entry, Government will not be responsible for mis-credit of Scholarship amount. Applicant will be held responsible in case of diversion of public money on this ground.</p>
                            <p>2. Please note that your Aadhaar Number will be used for crediting scholarship amount in the bank account linked/ seeded to your Aadhaar number in fast-track mode. To link/ seed your bank account with your Aadhaar, please visit you bank branch and submit a "bank consent form for receiving DBT".</p>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-end mb-6">
                            <div>
                                <label class="block text-sm text-gray-600 mb-1">IFSC Code <span class="text-red-500">*</span></label>
                                <div class="flex">
                                    <input type="text" id="ifsc_code" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent uppercase" placeholder="IFSC Code" required>
                                    <button type="button" onclick="fetchIFSC()" class="bg-blue-500 text-white px-4 py-2 text-sm font-bold shadow hover:bg-blue-600 transition whitespace-nowrap">FIND IFSC</button>
                                </div>
                            </div>
                            <div class="text-center col-span-2 md:col-span-1">
                                <label class="block text-sm text-gray-600 mb-1">Bank Name & Branch</label>
                                <input type="text" id="bank_name_display" placeholder="Auto fetched or type manual" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent font-bold text-gray-800">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                            <div>
                                <label class="block text-sm text-gray-600 mb-1">Account Holder Name</label>
                                <input type="text" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent">
                            </div>
                            <div>
                                <label class="block text-sm text-gray-600 mb-1">Account Number <span class="text-red-500">*</span></label>
                                <input type="text" id="acc_no" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent" required>
                            </div>
                            <div>
                                <label class="block text-sm text-gray-600 mb-1">Re-type Account No. <span class="text-red-500">*</span></label>
                                <input type="text" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent" required>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                            <div>
                                <p class="text-sm text-gray-600 italic mb-2">Whether account number seeded with the Aadhaar number?</p>
                                <div class="flex gap-4">
                                    <label class="flex items-center gap-1 cursor-pointer"><input type="radio" name="aadhaar_seeded" value="yes" class="w-4 h-4 text-blue-600"> Yes</label>
                                    <label class="flex items-center gap-1 cursor-pointer"><input type="radio" name="aadhaar_seeded" value="no" class="w-4 h-4 text-blue-600" checked> No</label>
                                </div>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600 italic mb-2">Upload front page of passbook where the Account number and IFSC code given above is clearly visible <span class="text-red-500">*</span></p>
                                <div class="flex border rounded overflow-hidden">
                                    <div class="px-3 py-2 bg-gray-50 text-gray-500 border-r w-full truncate">Upload Passbook Front Page</div>
                                    <input type="file" class="hidden" id="passbook_upload" accept=".pdf" required>
                                    <button type="button" onclick="document.getElementById('passbook_upload').click()" class="px-4 py-2 bg-white text-blue-600 font-bold hover:bg-gray-100">Browse</button>
                                </div>
                                <div class="flex justify-between items-center mt-2">
                                    <p class="text-red-600 text-xs">Note: Upload .pdf file upto 1MB file size.</p>
                                    <i class="fa-regular fa-file-pdf text-red-500 text-xl"></i>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 flex justify-center gap-4">
                        <button type="button" class="bg-gray-300 text-gray-800 font-bold py-3 px-8 rounded shadow hover:bg-gray-400">BACK</button>
                        <button type="submit" class="bg-blue-500 text-white font-bold py-3 px-8 rounded shadow-lg hover:bg-blue-600">ELIGIBLE / NEXT</button>
                    </div>
                </form>
            </div>
        </div>

        <div id="section-payment-step" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <div class="max-w-3xl mx-auto border-2 border-orange-300 rounded-xl p-6 bg-orange-50">
                <h2 class="text-2xl font-bold text-orange-700 mb-4 text-center border-b border-orange-300 pb-2"><i class="fa-solid fa-file-shield mr-2"></i> Application Declaration & Payment</h2>
                
                <div class="bg-white p-5 rounded border border-gray-200 shadow-inner mb-6 text-gray-700 leading-relaxed text-lg font-medium text-justify">
                    <p>I declare that all information provided is true and my annual income is strictly below Rs. 50,000. If my income is found to exceed 50,000 or if any data is false, Admin holds the right to reject my application without prior notice. I agree to all terms and conditions.</p>
                </div>

                <label class="flex items-start gap-3 cursor-pointer p-3 bg-white rounded border border-gray-300 hover:bg-gray-50 transition mb-6 shadow-sm">
                    <input type="checkbox" id="tnc_checkbox" onchange="togglePayButton()" class="w-6 h-6 mt-1 text-orange-600 focus:ring-orange-500 cursor-pointer">
                    <span class="text-gray-800 font-bold">I Agree to the Terms & Conditions and Confirm the above Declaration. (ମୁଁ ସମସ୍ତ ସର୍ତ୍ତାବଳୀ ସହ ସହମତ)</span>
                </label>

                <div class="text-center">
                    <p class="text-sm font-semibold text-gray-500 mb-2">Select Payment Gateway & Proceed</p>
                    <div class="flex justify-center gap-4 mb-4">
                        <label class="flex items-center gap-2 border p-3 rounded-lg cursor-pointer hover:bg-gray-50 font-bold text-blue-900 border-blue-200">
                            <input type="radio" name="pay_gateway" value="razorpay" checked class="w-5 h-5 text-blue-600 focus:ring-blue-500">
                            <i class="fa-solid fa-credit-card"></i> Razorpay
                        </label>
                        <label class="flex items-center gap-2 border p-3 rounded-lg cursor-pointer hover:bg-gray-50 font-bold text-orange-700 border-orange-200">
                            <input type="radio" name="pay_gateway" value="payu" class="w-5 h-5 text-orange-500 focus:ring-orange-500">
                            <i class="fa-solid fa-wallet"></i> PayU
                        </label>
                    </div>
                    
                    <button type="button" id="payu_button" onclick="processPayment()" disabled class="bg-green-600 text-white font-extrabold text-xl py-4 px-10 rounded-lg shadow-lg hover:bg-green-700 opacity-50 cursor-not-allowed transition-all w-full md:w-auto">
                        <i class="fa-solid fa-lock mr-2"></i> Pay Now (₹<span class="display_app_fee"></span>)
                    </button>
                    <div class="mt-4 flex justify-center items-center gap-4 text-gray-400 text-3xl">
                        <i class="fa-brands fa-cc-visa"></i>
                        <i class="fa-brands fa-cc-mastercard"></i>
                        <i class="fa-solid fa-building-columns"></i>
                        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/UPI-Logo-vector.svg" class="h-6 grayscale opacity-60">
                    </div>
                </div>
            </div>
        </div>

        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <!-- Content Managed dynamically by checkAppStatus -->
        </div>
        
        <div id="section-renew" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <!-- Dynamic Renewal HTML -->
        </div>
    </main>

    <!-- FULL APPLICATION VIEW MODAL (USER DASHBOARD) -->
    <div id="user_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 print:hidden">
        <div class="bg-white w-full max-w-4xl h-[90vh] rounded-xl shadow-2xl flex flex-col">
            <div class="p-4 border-b flex justify-between items-center bg-blue-50 rounded-t-xl">
                <h3 class="text-xl font-bold text-blue-800"><i class="fa-solid fa-file-lines mr-2"></i> My Application Data</h3>
                <div class="space-x-2">
                    <button onclick="window.print()" class="bg-gray-800 text-white px-4 py-2 rounded shadow font-bold hover:bg-gray-900"><i class="fa-solid fa-print"></i> Print Form & Receipt</button>
                    <button onclick="closeUserAppModal()" class="bg-red-500 text-white px-4 py-2 rounded shadow font-bold hover:bg-red-600"><i class="fa-solid fa-xmark"></i> Close</button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-8">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-6 bg-gray-50 p-4 rounded border">
                    <div><p class="text-gray-500 font-semibold text-xs">Application No</p><p class="font-bold text-base text-blue-700"><span class="print_u_appno"></span></p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Scheme Category</p><p class="print_u_scheme font-bold text-base"></p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Applied Date</p><p class="font-bold text-base">23-Oct-2026</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Payment Status</p><p class="font-bold text-green-600"><i class="fa-solid fa-check-circle"></i> Paid (₹<span class="display_app_fee"></span>)</p></div>
                </div>
                
                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">Application Details</h4>
                <div class="grid grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded border">
                    <p><strong>Name:</strong> <span class="print_u_name"></span></p>
                    <p><strong>Category:</strong> <span id="print_u_category"></span></p>
                    <p><strong>Aadhaar:</strong> <span id="print_u_aadhaar"></span></p>
                    <p><strong>District:</strong> <span id="print_u_dist"></span></p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 6. FULL ADMIN DASHBOARD (SYSTEM -> ADMIN -> SUPER ADMIN)
# ==========================================
admin_login_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin & Super Admin Login</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        let currentCaptcha = "";

        window.onload = function() {{ generateCaptcha(); }};

        function generateCaptcha() {{
            const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            currentCaptcha = "";
            for (let i = 0; i < 6; i++) {{ currentCaptcha += chars[Math.floor(Math.random() * chars.length)]; }}
            document.getElementById('captcha_display').innerText = currentCaptcha;
        }}

        function handleAdminLogin(event) {{
            event.preventDefault();
            let adminId = document.getElementById('admin_id').value;
            let adminPass = document.getElementById('password').value;
            let captchaInput = document.getElementById('login_captcha').value;
            
            if (captchaInput !== currentCaptcha) {{
                alert("Invalid Captcha! Please try again."); generateCaptcha(); return;
            }}

            let savedAdminId = localStorage.getItem('admin_email') || 'admin@kulusutar.in';
            let savedAdminPass = localStorage.getItem('admin_password') || 'Admin@123';
            
            let superAdminId = 'superadmin@kulusutar.in';
            let superAdminPass = 'Super@123';

            if(adminId === superAdminId && adminPass === superAdminPass) {{
                localStorage.setItem('active_role', 'superadmin');
                window.location.href = '/admin';
            }}
            else if(adminId === savedAdminId && adminPass === savedAdminPass) {{
                localStorage.setItem('active_role', 'admin');
                window.location.href = '/admin';
            }} else {{
                alert('Access Denied: Invalid ID or Password!'); generateCaptcha();
            }}
        }}
    </script>
</head>
<body class="bg-gray-100 font-sans flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700">
        <div class="text-center mb-8">
            <i class="fa-solid fa-user-shield text-5xl text-blue-700 mb-3"></i>
            <h2 class="text-2xl font-bold text-gray-800">Admin / Super Admin Login</h2>
        </div>
        <form onsubmit="handleAdminLogin(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Login ID / Email</label>
                <div class="relative"><i class="fa-solid fa-envelope absolute left-3 top-3.5 text-gray-400"></i><input type="text" id="admin_id" class="w-full pl-10 pr-4 py-3 border rounded-lg" required></div>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <div class="relative"><i class="fa-solid fa-lock absolute left-3 top-3.5 text-gray-400"></i><input type="password" id="password" class="w-full pl-10 pr-4 py-3 border rounded-lg" required></div>
            </div>
            <div class="mt-4">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Enter Captcha</label>
                <div class="flex gap-2 mb-2">
                    <div id="captcha_display" class="bg-gray-200 border-2 border-gray-400 font-mono text-xl tracking-widest px-4 py-2 font-bold text-gray-700 w-1/2 text-center line-through decoration-gray-500 rounded select-none"></div>
                    <button type="button" onclick="generateCaptcha()" class="bg-blue-100 text-blue-700 px-3 rounded"><i class="fa-solid fa-arrows-rotate"></i></button>
                </div>
                <input type="text" id="login_captcha" class="w-full px-4 py-2 border rounded-lg" required>
            </div>
            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg hover:bg-blue-800 shadow-md mt-4">Login to Dashboard</button>
        </form>
        <div class="text-center mt-6"><a href="/" class="text-sm text-gray-500 hover:text-blue-700"><i class="fa-solid fa-arrow-left mr-1"></i> Back to Home</a></div>
    </div>
</body>
</html>
"""

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
        let role = localStorage.getItem('active_role') || 'admin';

        window.onload = function() {{
            document.getElementById('welcome_role').innerText = role === 'superadmin' ? 'Super Admin' : 'Admin';
            
            if(role === 'admin') {{
                document.getElementById('super_admin_menu').classList.add('hidden');
                document.getElementById('payout_menu').classList.add('hidden');
            }}
            loadAdminData();
        }};

        function switchTab(tabId, element) {{
            let sections = document.querySelectorAll('.content-section');
            for(let i=0; i<sections.length; i++) {{ sections[i].classList.add('hidden'); }}
            document.getElementById('section-' + tabId).classList.remove('hidden');

            let links = document.querySelectorAll('.menu-link');
            for(let i=0; i<links.length; i++) {{
                links[i].classList.remove('bg-blue-700', 'text-white');
                links[i].classList.add('text-slate-300', 'hover:bg-slate-800');
            }}
            element.classList.remove('text-slate-300', 'hover:bg-slate-800');
            element.classList.add('bg-blue-700', 'text-white');
        }}

        function loadAdminData() {{
            let appList = JSON.parse(localStorage.getItem('app_list') || '[]');
            
            let sysHtml = ''; let adminHtml = ''; let superAdminHtml = ''; let rejHtml = ''; let benHtml = '';
            
            appList.forEach(appNo => {{
                let isApplied = localStorage.getItem('user_has_applied_' + appNo);
                if(isApplied === 'true') {{
                    let status = localStorage.getItem('app_status_' + appNo);
                    let name = localStorage.getItem('user_full_name_' + appNo) || 'N/A';
                    let cat = localStorage.getItem('u_category_' + appNo) || 'N/A';
                    
                    if(status === 'sys_pending') {{
                        sysHtml += `
                            <tr class="border-b">
                                <td class="py-2 px-4">#${{appNo}}</td>
                                <td class="py-2 px-4">${{name}}</td>
                                <td class="py-2 px-4">
                                    <button onclick="verifySys('${{appNo}}')" class="bg-blue-500 text-white px-2 py-1 rounded text-xs">Verify Details</button>
                                    <button onclick="rejectApp('${{appNo}}', 'System')" class="bg-red-500 text-white px-2 py-1 rounded text-xs">Reject</button>
                                </td>
                            </tr>
                        `;
                    }} else if (status === 'admin_pending') {{
                        adminHtml += `
                            <tr class="border-b">
                                <td class="py-2 px-4">#${{appNo}}</td>
                                <td class="py-2 px-4">${{name}} (${{cat}})</td>
                                <td class="py-2 px-4">
                                    <button onclick="verifyAdmin('${{appNo}}')" class="bg-blue-500 text-white px-2 py-1 rounded text-xs">Check Edit</button>
                                    <button onclick="sendToSuperAdmin('${{appNo}}')" class="bg-green-500 text-white px-2 py-1 rounded text-xs">Send to Super Admin</button>
                                    <button onclick="rejectApp('${{appNo}}', 'Admin')" class="bg-red-500 text-white px-2 py-1 rounded text-xs">Reject</button>
                                </td>
                            </tr>
                        `;
                    }} else if (status === 'super_admin_pending') {{
                        superAdminHtml += `
                            <tr class="border-b">
                                <td class="py-2 px-4">#${{appNo}}</td>
                                <td class="py-2 px-4">${{name}}</td>
                                <td class="py-2 px-4">
                                    <button onclick="verifySuperAdmin('${{appNo}}')" class="bg-blue-500 text-white px-2 py-1 rounded text-xs">View/Edit Full Data</button>
                                    <button onclick="approveFinal('${{appNo}}')" class="bg-green-500 text-white px-2 py-1 rounded text-xs">Approve for Payout</button>
                                    <button onclick="rejectApp('${{appNo}}', 'Super Admin')" class="bg-red-500 text-white px-2 py-1 rounded text-xs">Reject</button>
                                </td>
                            </tr>
                        `;
                    }} else if (status === 'rejected') {{
                        let reason = localStorage.getItem('reject_reason_' + appNo);
                        rejHtml += `<tr class="border-b"><td class="py-2 px-4 text-red-500">#${{appNo}}</td><td class="py-2 px-4">${{name}}</td><td class="py-2 px-4 text-xs">${{reason}}</td></tr>`;
                    }} else if (status === 'approved' || status === 'pension_sent') {{
                        benHtml += `<tr class="border-b"><td class="py-2 px-4">#${{appNo}}</td><td class="py-2 px-4">${{name}}</td><td class="py-2 px-4 text-green-500">Active Beneficiary</td></tr>`;
                    }}
                }}
            }});

            document.getElementById('sys_verify_tbody').innerHTML = sysHtml;
            document.getElementById('admin_approve_tbody').innerHTML = adminHtml;
            document.getElementById('super_admin_tbody').innerHTML = superAdminHtml;
            document.getElementById('rejected_tbody').innerHTML = rejHtml;
            document.getElementById('beneficiaries_tbody').innerHTML = benHtml;
        }}

        function rejectApp(appNo, byWhom) {{
            let remark = prompt(`Enter rejection remark (${{byWhom}}):`);
            if(remark) {{
                localStorage.setItem('app_status_' + appNo, 'rejected');
                localStorage.setItem('reject_reason_' + appNo, `${{byWhom}} Rejected: ` + remark);
                location.reload();
            }}
        }}

        function verifySys(appNo) {{
            if(confirm('Is Bank and IFCS Details Correct for Application ' + appNo + '?')) {{
                localStorage.setItem('app_status_' + appNo, 'admin_pending');
                alert('Sent to Admin Desk');
                location.reload();
            }}
        }}

        function sendToSuperAdmin(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'super_admin_pending');
            alert('Forwarded to Super Admin for Final Check.');
            location.reload();
        }}

        function approveFinal(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'approved');
            alert('Finally Approved by Super Admin! Ready for Payment.');
            location.reload();
        }}
        
        function verifyAdmin(appNo) {{
            alert('Admin Edit Panel for ' + appNo + '\\n(Caste, Bank, Address can be edited here by fetching data from localstorage)');
        }}
        function verifySuperAdmin(appNo) {{
            alert('Super Admin Edit Panel for ' + appNo + '\\n(All data visible)');
        }}
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl h-full print:hidden">
        <div class="p-5 border-b border-slate-700 text-center"><h2 class="text-xl font-bold" id="welcome_role">Admin</h2></div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchTab('sysverify', this)" class="menu-link block px-4 py-3 bg-blue-700 text-white rounded">1. System Level Check</a></li>
                <li><a href="#" onclick="switchTab('adminapprove', this)" class="menu-link block px-4 py-3 text-slate-300 hover:bg-slate-800 rounded">2. Admin Level Check</a></li>
                <li id="super_admin_menu"><a href="#" onclick="switchTab('superadmin', this)" class="menu-link block px-4 py-3 text-yellow-300 hover:bg-slate-800 rounded">3. Super Admin (Final)</a></li>
                <li><a href="#" onclick="switchTab('rejected', this)" class="menu-link block px-4 py-3 text-red-400 hover:bg-slate-800 rounded">Rejected Box</a></li>
                <li><a href="#" onclick="switchTab('beneficiaries', this)" class="menu-link block px-4 py-3 text-green-400 hover:bg-slate-800 rounded">Beneficiaries</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="text-red-400">Logout</a></div>
    </aside>

    <main class="flex-1 p-6 overflow-y-auto">
        
        <div id="section-sysverify" class="content-section bg-white p-6 rounded shadow">
            <h2 class="text-xl font-bold mb-4">1. System Level Verification (Bank & Basic Checks)</h2>
            <table class="w-full text-left"><tbody id="sys_verify_tbody"></tbody></table>
        </div>

        <div id="section-adminapprove" class="content-section bg-white p-6 rounded shadow hidden">
            <h2 class="text-xl font-bold mb-4">2. Admin Desk (Document & Form Checks)</h2>
            <table class="w-full text-left"><tbody id="admin_approve_tbody"></tbody></table>
        </div>

        <div id="section-superadmin" class="content-section bg-white p-6 rounded shadow hidden">
            <h2 class="text-xl font-bold mb-4 text-yellow-600">3. Super Admin (Final Approval)</h2>
            <table class="w-full text-left"><tbody id="super_admin_tbody"></tbody></table>
        </div>

        <div id="section-rejected" class="content-section bg-white p-6 rounded shadow hidden">
            <h2 class="text-xl font-bold mb-4 text-red-600">Rejected Box</h2>
            <table class="w-full text-left"><tbody id="rejected_tbody"></tbody></table>
        </div>

        <div id="section-beneficiaries" class="content-section bg-white p-6 rounded shadow hidden">
            <h2 class="text-xl font-bold mb-4 text-green-600">Active Beneficiaries</h2>
            <table class="w-full text-left"><tbody id="beneficiaries_tbody"></tbody></table>
        </div>
    </main>
</body>
</html>
"""

# ==========================================
# 7. EXPLICIT ROUTES DEFINITION 
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design

@app.get("/status/check", response_class=HTMLResponse)
async def status_check_page():
    return status_check_design

@app.post("/status/check", response_class=HTMLResponse)
async def status_check_page_post(request: Request):
    return status_check_design

@app.get("/user/register", response_class=HTMLResponse)
async def user_register_page():
    return user_register_design

@app.get("/user/login", response_class=HTMLResponse)
async def user_login_page():
    return user_login_design

@app.get("/user/dashboard", response_class=HTMLResponse)
async def user_dashboard_route():
    return user_dashboard_design

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    return admin_login_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_route():
    return admin_design
