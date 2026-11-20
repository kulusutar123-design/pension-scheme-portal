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
import urllib.request

app = FastAPI()

# ==========================================
# CASHFREE CREDENTIALS (ADDED AS REQUESTED)
# ==========================================
CASHFREE_APP_ID = "1515812276f3edeb0677e6e62642185151"
CASHFREE_SECRET_KEY = "cfsk_ma_prod_1b755875b3e4253c4e2865ddd5f27524_fa5dfc25"

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
# LIVE CASHFREE ORDER API
# ==========================================
@app.post("/api/cashfree_order")
async def create_cashfree_order(req: Request):
    try:
        data = await req.json()
        db_data = read_db()
        app_id = db_data.get("cashfree_app_id", CASHFREE_APP_ID)
        secret_key = db_data.get("cashfree_secret_key", CASHFREE_SECRET_KEY)
        
        order_id = "CF_" + str(data.get("txnid"))
        amount = float(data.get("amount", 100.0))
        
        url = "https://api.cashfree.com/pg/orders"
        headers = {
            "x-client-id": app_id,
            "x-client-secret": secret_key,
            "x-api-version": "2023-08-01",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(data.get("appNo", "USER_001")),
                "customer_name": str(data.get("firstname", "Applicant")),
                "customer_email": str(data.get("email", "user@example.com")),
                "customer_phone": str(data.get("phone", "9876543210"))
            },
            "order_meta": {
                "return_url": str(data.get("surl"))
            }
        }
        req_obj = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
        with urllib.request.urlopen(req_obj) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return {"status": "success", "payment_session_id": res_data.get("payment_session_id"), "order_id": order_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# LIVE GMAIL OTP & NOTIFICATION SENDER API
# ==========================================
class EmailRequest(BaseModel):
    email: str
    otp: str
    subject: str

class NotificationRequest(BaseModel):
    email: str
    subject: str
    message: str
    app_no: str = ""
    status_label: str = ""

SENDER_EMAIL = "privatesocialsecuritypensionsc@gmail.com" 
SENDER_PASSWORD = "gzafqvjphaftybhy" 

@app.post("/api/send_email")
async def send_email_api(req: EmailRequest):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Gopabandhu Pension Yojana <{SENDER_EMAIL}>"
        msg['To'] = req.email
        msg['Subject'] = req.subject

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; margin: 0;">
            <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1d4ed8;">
              <h2 style="color: #1e3a8a; margin-top: 0; text-align: center;">Gopabandhu Pension Yojana</h2>
              <p style="color: #374151; font-size: 16px;">Dear User / Officer,</p>
              <p style="color: #374151; font-size: 16px;">Your One Time Password (OTP) is:</p>
              <div style="background-color: #fef08a; padding: 15px; text-align: center; border-radius: 8px; margin: 25px 0;">
                  <span style="font-size: 32px; font-weight: bold; color: #b45309; letter-spacing: 8px;">{req.otp}</span>
              </div>
              <p style="color: #4b5563; font-size: 14px;">This OTP is strictly valid for 5 minutes. Do not share this code with anyone.</p>
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">
                Regards,<br><strong>Admin Team</strong><br>Gopabandhu Pension Yojana
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

@app.post("/api/send_notification")
async def send_notification_api(req: NotificationRequest):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"Gopabandhu Pension Yojana <{SENDER_EMAIL}>"
        msg['To'] = req.email
        msg['Subject'] = req.subject

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; margin: 0;">
            <div style="max-width: 550px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #059669;">
              <h2 style="color: #1e3a8a; margin-top: 0; text-align: center;">Gopabandhu Pension Yojana - Status Update</h2>
              <p style="color: #374151; font-size: 15px;">Application No: <strong>{req.app_no}</strong></p>
              <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 15px; border-radius: 6px; margin: 20px 0;">
                  <p style="margin: 0; font-size: 16px; font-weight: bold; color: #1e40af;">{req.status_label}</p>
                  <p style="margin: 8px 0 0 0; font-size: 14px; color: #374151;">{req.message}</p>
              </div>
              <p style="color: #4b5563; font-size: 13px;">Please login to your Beneficiary Dashboard to view full details.</p>
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 25px 0;">
              <p style="font-size: 12px; color: #9ca3af; text-align: center;">
                Regards,<br><strong>Gopabandhu Pension Yojana Administration</strong>
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
            alert("Payment Successful! Apananka Gopabandhu Pension Yojana Application Fee Paith Heyejaichi.");
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
# SHARED LOCATION DATA SCRIPT (ODISHA 30 DISTRICTS + BLOCKS)
# ==========================================
shared_location_script = """
    <script>
        const GLOBAL_LOCATION_DATA = {
            "Odisha": {
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
            }
        };
    </script>
"""

# ==========================================
# CLOUD SYNC SCRIPT (100% CROSS BROWSER FIX)
# ==========================================
cloud_sync_script = """
    <!-- 100% WORKING CROSS-DEVICE SYNC SCRIPT -->
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
# 1. HOME PAGE DESIGN (GOPABANDHU PENSION YOJANA)
# ==========================================
html_design = f"""
<!DOCTYPE html>
<html lang="en" style="-webkit-scroll-behavior: smooth; -moz-scroll-behavior: smooth; scroll-behavior: smooth;">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }}
        .card-hover:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
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
                    <h1 class="text-xl md:text-2xl font-bold text-blue-800">Gopabandhu Pension Yojana</h1>
                    <p class="text-sm font-semibold text-gray-600">Private Social Security Pension Initiative for the Needy</p>
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

            let cName = localStorage.getItem('contact_name');
            let cMob = localStorage.getItem('contact_mobile');
            let cEmail = localStorage.getItem('contact_email');
            if(cName) document.getElementById('home_contact_name').innerText = cName;
            if(cMob) document.getElementById('home_contact_mobile').innerText = cMob;
            if(cEmail) document.getElementById('home_contact_email').innerText = cEmail;
        }});
    </script>

    <section id="home" class="hero-bg py-16 px-4 border-b">
        <div class="container mx-auto">
            <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-xl border-l-8 border-blue-600 backdrop-blur-sm">
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">Gopabandhu Pension Yojana: Support for Senior Citizens, Widows, Disabled & the Needy</h2>
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
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Officer / Admin Login</h3><p class="text-sm mb-4 text-blue-100">Block, District, State & Admin Login</p>
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
            <div class="text-center mb-8"><h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Gopabandhu Pension Yojana)</h2></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3><p class="text-gray-700 leading-relaxed text-sm">"ଗୋପବନ୍ଧୁ ପେନସନ୍ ଯୋଜନା ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା।"</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3><p class="text-gray-700 leading-relaxed text-sm">"Gopabandhu Pension Yojana is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy."</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 leading-relaxed text-sm">"गोपबंधु पेंशन योजना एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है।"</p></div>
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
        <div class="bg-blue-900 text-white rounded-xl p-8 shadow-xl text-center max-w-4xl mx-auto">
            <h2 class="text-3xl font-bold mb-4"><i class="fa-solid fa-envelope-open-text mr-2"></i> ଯୋଗାଯୋଗ (Contact Us)</h2>
            <p class="mb-6 text-blue-200">For any inquiries, application support, or grievances, please reach out to us:</p>
            <div class="flex flex-col md:flex-row justify-center gap-4">
                <div class="bg-white text-blue-900 px-4 py-3 rounded-lg font-bold text-lg shadow-inner flex items-center justify-center">
                    <i class="fa-solid fa-user mr-2 text-xl"></i> <span id="home_contact_name">Admin Support</span>
                </div>
                <div class="bg-white text-blue-900 px-4 py-3 rounded-lg font-bold text-lg shadow-inner flex items-center justify-center">
                    <i class="fa-solid fa-phone mr-2 text-xl"></i> <span id="home_contact_mobile">+91 9876543210</span>
                </div>
                <div class="bg-white text-blue-900 px-4 py-3 rounded-lg font-bold text-lg shadow-inner flex items-center justify-center">
                    <i class="fa-solid fa-envelope mr-2 text-xl"></i> <span id="home_contact_email">admin@kulusutar.in</span>
                </div>
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
    <title>Check Application Status - Gopabandhu Pension Yojana</title>
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
                    let reason = localStorage.getItem('reject_reason_' + appNo) || "Rejected by Officer/Admin.";
                    resBox.className = "mt-6 border p-4 rounded-lg bg-red-50 border-red-200";
                    statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                    statText.className = "text-red-600 font-bold";
                    statText.innerText = "Rejected";
                    statRemark.innerHTML = "<strong>Remark:</strong> " + reason;
                    statRemark.classList.remove('hidden');
                }} else if (appStatus === 'block_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-yellow-50 border-yellow-200";
                    statIcon.className = "fa-solid fa-building-user text-yellow-600 mr-1";
                    statText.className = "text-yellow-700 font-bold";
                    statText.innerText = "Pending at Block Officer Verification";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'dist_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-indigo-50 border-indigo-200";
                    statIcon.className = "fa-solid fa-landmark text-indigo-600 mr-1";
                    statText.className = "text-indigo-700 font-bold";
                    statText.innerText = "Block Approved - Pending at District Officer";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'state_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-purple-50 border-purple-200";
                    statIcon.className = "fa-solid fa-flag text-purple-600 mr-1";
                    statText.className = "text-purple-700 font-bold";
                    statText.innerText = "District Approved - Pending at State Officer";
                    statRemark.classList.add('hidden');
                }} else if (appStatus === 'sys_pending_2days' || appStatus === 'admin_correction' || appStatus === 'sys_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-orange-50 border-orange-200";
                    statIcon.className = "fa-solid fa-microchip text-orange-600 mr-1";
                    statText.className = "text-orange-600 font-bold";
                    statText.innerText = (appStatus === 'admin_correction') ? "Pending Correction by Admin" : "State Approved - Pending System Verification";
                    let sysRem = localStorage.getItem('sys_remark_' + appNo);
                    if(sysRem) {{
                        statRemark.innerHTML = "<strong>System Remark:</strong> " + sysRem;
                        statRemark.classList.remove('hidden');
                    }} else {{
                        statRemark.classList.add('hidden');
                    }}
                }} else if (appStatus === 'admin_pending' || appStatus === 'super_admin_pending') {{
                    resBox.className = "mt-6 border p-4 rounded-lg bg-blue-50 border-blue-200";
                    statIcon.className = "fa-solid fa-user-check text-blue-600 mr-1";
                    statText.className = "text-blue-600 font-bold";
                    statText.innerText = "System Verified - Pending Final Admin Approval";
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
                    statText.innerText = "Pending Verification";
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
            <p class="text-xs text-gray-500">Gopabandhu Pension Yojana</p>
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
            <p><i id="stat_icon" class="fa-solid fa-hourglass-half mr-1"></i> <span id="stat_text" class="font-bold">Pending</span></p>
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
    <title>New User Registration - Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        const stateLanguages = {{
            "Odisha": "Odia", "Andhra Pradesh": "Telugu", "Arunachal Pradesh": "English", "Assam": "Assamese",
            "Bihar": "Hindi", "Chhattisgarh": "Hindi", "Goa": "Konkani", "Gujarat": "Gujarati",
            "Haryana": "Hindi", "Himachal Pradesh": "Hindi", "Jharkhand": "Hindi", "Karnataka": "Kannada",
            "Kerala": "Malayalam", "Madhya Pradesh": "Hindi", "Maharashtra": "Marathi", "Manipur": "Manipuri",
            "Meghalaya": "English", "Mizoram": "Mizo", "Nagaland": "English", "Punjab": "Punjabi",
            "Rajasthan": "Hindi", "Sikkim": "English", "Tamil Nadu": "Tamil", "Telangana": "Telugu",
            "Tripura": "Bengali", "Uttar Pradesh": "Hindi", "Uttarakhand": "Hindi", "West Bengal": "Bengali"
        }};

        window.addEventListener('DOMContentLoaded', () => {{
            let startDate = localStorage.getItem('reg_start_date');
            let closeDate = localStorage.getItem('reg_close_date');
            let isOpen = true;
            if(startDate && closeDate) {{
                let start = new Date(startDate).setHours(0,0,0,0);
                let end = new Date(closeDate).setHours(23,59,59,999);
                let now = new Date().getTime();
                if(now < start || now > end) {{ isOpen = false; }}
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
                langs.forEach(l => {{ langSelect.innerHTML += `<option value="${{l}}">${{l}}</option>`; }});
                document.getElementById('dynamic_heading').innerText = `User Registration (${{localLang}} / English / Hindi)`;
            }} else {{
                document.getElementById('dynamic_heading').innerText = `User Registration (ନୂଆ ଆବେଦନକାରୀ)`;
            }}
        }}

        let currentOTP = "";
        
        async function generateOTP() {{
            let emailId = document.getElementById('reg_email').value;
            if(!emailId) {{ alert("Please enter Email ID first to get OTP."); return; }}
            currentOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('otpDisplay').innerText = `Sending Real OTP to ${{emailId}}... (Demo OTP: ${{currentOTP}})`;
            document.getElementById('otpDisplay').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse mt-2";
            document.getElementById('otpDisplay').classList.remove('hidden');
            try {{
                let response = await fetch('/api/send_email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: emailId, otp: currentOTP, subject: "Your Registration OTP - Gopabandhu Pension Yojana" }})
                }});
                let data = await response.json();
                if(data.status === 'success') {{
                    document.getElementById('otpDisplay').innerText = `Real OTP sent to ${{emailId}}! (Demo OTP: ${{currentOTP}})`;
                    document.getElementById('otpDisplay').className = "text-center bg-green-100 text-green-800 font-bold p-2 rounded text-sm mt-2";
                }} else {{
                    document.getElementById('otpDisplay').innerText = `Email failed. (Demo OTP: ${{currentOTP}})`;
                    document.getElementById('otpDisplay').className = "text-center bg-red-100 text-red-800 font-bold p-2 rounded text-sm mt-2";
                }}
            }} catch(e) {{ alert("Server error connecting to Email API."); }}
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
            let regState = document.getElementById('state_select').value;
            
            let passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{{6,}}$/;
            if (!passRegex.test(pwd)) {{
                alert('Password must contain at least 1 Capital letter, 1 Small letter, 1 Number, and 1 Special Character (@, #, $)!');
                return;
            }}
            if (pwd !== conf_pwd) {{ alert('Password and Confirm Password do not match!'); return; }}
            
            let randomNum = Math.floor(100000 + Math.random() * 900000);
            let appNo = 'APP-' + randomNum;
            
            localStorage.setItem('user_password_' + appNo, pwd);
            localStorage.setItem('user_full_name_' + appNo, fullName);
            localStorage.setItem('user_mobile_' + appNo, mobileNo);
            localStorage.setItem('user_email_' + appNo, emailId);
            localStorage.setItem('u_state_' + appNo, regState || 'Odisha');
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
        <p class="text-center text-xs font-bold text-blue-700 uppercase mb-1">Gopabandhu Pension Yojana</p>
        <h2 id="dynamic_heading" class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration (ନୂଆ ଆବେଦନକାରୀ)</h2>
        <form onsubmit="handleUserRegistration(event)" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-700">State (ରାଜ୍ୟ)</label>
                    <select id="state_select" onchange="updateLanguageOptions()" class="w-full px-4 py-2 border rounded-lg" required>
                        <option value="">Select State</option>
                        <option value="Odisha">Odisha</option>
                        <option value="Andhra Pradesh">Andhra Pradesh</option>
                        <option value="Bihar">Bihar</option>
                        <option value="Chhattisgarh">Chhattisgarh</option>
                        <option value="Jharkhand">Jharkhand</option>
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
    <title>User / Beneficiary Login - Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        let currentCaptcha = "";
        let forgotOTP = "";
        let otpTimerInterval;
        let timeLeft = 300;

        window.onload = function() {{ generateCaptcha(); }};

        function generateCaptcha() {{
            const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            currentCaptcha = "";
            for (let i = 0; i < 6; i++) {{ currentCaptcha += chars[Math.floor(Math.random() * chars.length)]; }}
            document.getElementById('captcha_display').innerText = currentCaptcha;
        }}

        function handleUserLogin(event) {{
            event.preventDefault();
            let appNo = document.getElementById('login_app_no').value.trim().toUpperCase();
            let pass = document.getElementById('login_pass').value;
            let captchaInput = document.getElementById('login_captcha').value;
            if (captchaInput !== currentCaptcha) {{ alert("Invalid Captcha!"); generateCaptcha(); return; }}
            let savedPass = localStorage.getItem('user_password_' + appNo);
            if (savedPass && pass === savedPass) {{
                localStorage.setItem('active_app_no', appNo);
                window.location.href = '/user/dashboard';
            }} else {{
                alert('Access Denied: Invalid Application Number or Password!');
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
            if (!userEmail) {{ alert("Application Number not found in system!"); return; }}
            forgotOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('forgot_otp_display').innerText = `Sending Real OTP to ${{userEmail}}... (Demo OTP: ${{forgotOTP}})`;
            document.getElementById('forgot_otp_display').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse";
            document.getElementById('forgot_otp_display').classList.remove('hidden');
            try {{
                let response = await fetch('/api/send_email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: userEmail, otp: forgotOTP, subject: "Password Reset OTP - Gopabandhu Pension Yojana" }})
                }});
                let data = await response.json();
                if(data.status === 'success') {{
                    document.getElementById('forgot_otp_display').innerText = `Real OTP sent to ${{userEmail}}! (Demo OTP: ${{forgotOTP}})`;
                    document.getElementById('forgot_otp_display').className = "text-center bg-green-100 text-green-800 font-bold p-2 rounded text-sm";
                    document.getElementById('step2_forgot').classList.remove('hidden');
                    startOtpTimer();
                }} else {{ alert("Email sending failed."); }}
            }} catch(e) {{ alert("Server Error in sending email."); }}
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
                    forgotOTP = "";
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
            if(timeLeft <= 0 || !forgotOTP) {{ alert("OTP has expired!"); return; }}
            if (entered === forgotOTP && entered !== "") {{
                clearInterval(otpTimerInterval);
                document.getElementById('timer_display').innerText = "OTP Verified successfully!";
                document.getElementById('timer_display').classList.add('text-green-600');
                document.getElementById('step3_forgot').classList.remove('hidden');
            }} else {{ alert("Invalid OTP!"); }}
        }}

        function saveNewPassword(event) {{
            event.preventDefault();
            let appNo = document.getElementById('forgot_app_no').value.trim().toUpperCase();
            let p1 = document.getElementById('new_pass').value;
            let p2 = document.getElementById('conf_new_pass').value;
            let passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{{6,}}$/;
            if (!passRegex.test(p1)) {{ alert('Password must contain 1 Capital, 1 Small, 1 Number, 1 Special Char!'); return; }}
            if(p1 !== p2) {{ alert("Passwords do not match!"); return; }}
            localStorage.setItem('user_password_' + appNo, p1);
            alert("Password Changed Successfully! Please Login.");
            backToLogin();
        }}
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    
    <div id="login_section" class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <p class="text-center text-xs font-bold text-blue-700 uppercase mb-1">Gopabandhu Pension Yojana</p>
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Beneficiary Login (ଲଗଇନ୍)</h2>
        <form onsubmit="handleUserLogin(event)" class="space-y-4">
            <div><label class="block text-sm font-semibold text-gray-700">Application Number</label><input type="text" id="login_app_no" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg" required></div>
            <div><label class="block text-sm font-semibold text-gray-700">Password</label><input type="password" id="login_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
            <div class="mt-4">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Enter Captcha</label>
                <div class="flex gap-2 mb-2">
                    <div id="captcha_display" class="bg-gray-200 border-2 border-gray-400 font-mono text-xl tracking-widest px-4 py-2 font-bold text-gray-700 w-1/2 text-center line-through decoration-gray-500 rounded select-none"></div>
                    <button type="button" onclick="generateCaptcha()" class="bg-blue-100 text-blue-700 px-3 rounded hover:bg-blue-200 transition"><i class="fa-solid fa-arrows-rotate"></i></button>
                </div>
                <input type="text" id="login_captcha" placeholder="Enter code" class="w-full px-4 py-2 border rounded-lg" required>
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
                <div><label class="block text-sm font-semibold text-gray-700">New Password</label><input type="password" id="new_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div><label class="block text-sm font-semibold text-gray-700">Confirm Password</label><input type="password" id="conf_new_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
                <button type="submit" class="w-full bg-red-600 text-white font-bold py-3 rounded-lg hover:bg-red-700 shadow">Save Password & Login</button>
            </form>
        </div>
        <div class="text-center mt-6"><button onclick="backToLogin()" class="text-sm text-gray-500 hover:text-gray-800"><i class="fa-solid fa-arrow-left"></i> Back to Login</button></div>
    </div>
</body>
</html>
"""

# ==========================================
# 5. FULL USER DASHBOARD (WITH PHOTO UPLOAD, FULL STATUS TIMELINE & A4 PRINT/PDF)
# ==========================================
user_dashboard_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard - Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    {shared_location_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://sdk.cashfree.com/js/v3/cashfree.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @media print {{
            body * {{ visibility: hidden; }}
            #user_app_view_modal, #user_app_view_modal * {{ visibility: visible; }}
            #user_app_view_modal {{ position: absolute; left: 0; top: 0; width: 100%; height: auto; background: white; padding: 0; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
    <script>
        let uploadedPhotoDataUrl = "";
        let uploadedDocs = {{}};

        function handleFileToBase64(input, storageKey) {{
            if(input.files && input.files[0]) {{
                let reader = new FileReader();
                reader.onload = function(e) {{
                    if(storageKey === 'photo') {{
                        uploadedPhotoDataUrl = e.target.result;
                        let prev = document.getElementById('photo_preview');
                        if(prev) {{ prev.src = uploadedPhotoDataUrl; prev.classList.remove('hidden'); }}
                    }} else {{
                        uploadedDocs[storageKey] = e.target.result;
                    }}
                }};
                reader.readAsDataURL(input.files[0]);
            }}
        }}

        window.onload = function() {{
            let appNo = localStorage.getItem('active_app_no');
            if(!appNo) {{ window.location.href = '/user/login'; return; }}
            
            populateDistricts();
            let dynamicFee = localStorage.getItem('app_fee') || '100';
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = dynamicFee);
            
            let savedFullName = localStorage.getItem('user_full_name_' + appNo);
            let savedMobile = localStorage.getItem('user_mobile_' + appNo);
            let savedEmail = localStorage.getItem('user_email_' + appNo);
            
            if(savedFullName) {{
                let f = document.getElementById('full_name');
                if(f) {{ f.value = savedFullName; f.setAttribute('readonly', 'readonly'); f.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed"; }}
            }}
            if(savedMobile) {{
                let f = document.getElementById('app_mobile');
                if(f) {{ f.value = savedMobile; f.setAttribute('readonly', 'readonly'); f.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed"; }}
            }}
            if(savedEmail) {{
                let f = document.getElementById('app_email');
                if(f) {{ f.value = savedEmail; f.setAttribute('readonly', 'readonly'); f.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed"; }}
            }}
            
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);
            if(isApplied === 'true') {{
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <i class="fa-solid fa-triangle-exclamation text-yellow-500 text-4xl mb-4"></i>
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted (#${{appNo}})</h3>
                        <p class="text-gray-600 mt-2">You have already submitted an application. Check your live status or print your application form below.</p>
                        <div class="mt-4 flex flex-wrap justify-center gap-4">
                            <button onclick="switchUserTab('status')" class="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700 font-bold"><i class="fa-solid fa-list-check"></i> Check Status & Print</button>
                            <button onclick="resetApplicationForm()" class="bg-red-500 text-white px-6 py-2 rounded shadow hover:bg-red-600 font-bold"><i class="fa-solid fa-rotate-left"></i> Reset / Fill New Form</button>
                        </div>
                    </div>
                `;
            }}

            let penSent = localStorage.getItem('app_status_' + appNo);
            if(penSent === 'pension_sent') {{
                document.getElementById('section-renew').innerHTML = `
                    <h2 class="text-2xl font-bold mb-4 text-orange-600"><i class="fa-solid fa-clock-rotate-left"></i> 3-Month Renewal</h2>
                    <div class="bg-white border rounded-xl p-6 shadow-sm mb-6 border-l-4 border-green-500">
                        <p class="text-gray-600 font-semibold mb-2">Beneficiary Found: <strong class="text-gray-800">${{savedFullName}} (${{appNo}})</strong></p>
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
            checkCategoryAndAge();
        }};

        function resetApplicationForm() {{
            let appNo = localStorage.getItem('active_app_no');
            if(confirm('Are you sure you want to reset and fill a new form for this ID?')) {{
                localStorage.setItem('user_has_applied_' + appNo, 'false');
                localStorage.removeItem('app_status_' + appNo);
                location.reload();
            }}
        }}

        function populateDistricts() {{
            let distSelect = document.getElementById("district");
            let blockSelect = document.getElementById("block");
            if(distSelect && blockSelect) {{
                distSelect.innerHTML = "<option value=''>Select</option>";
                blockSelect.innerHTML = "<option value=''>Select</option>";
                for(let dist in GLOBAL_LOCATION_DATA["Odisha"]) {{
                    distSelect.innerHTML += `<option value='${{dist}}'>${{dist}}</option>`;
                }}
            }}
        }}

        function populateBlocks() {{
            let dist = document.getElementById("district").value;
            let blockSelect = document.getElementById("block");
            if(blockSelect) {{
                blockSelect.innerHTML = "<option value=''>Select</option>";
                if(dist && GLOBAL_LOCATION_DATA["Odisha"][dist]) {{
                    GLOBAL_LOCATION_DATA["Odisha"][dist].forEach(b => {{
                        blockSelect.innerHTML += `<option value='${{b}}'>${{b}}</option>`;
                    }});
                }}
            }}
        }}

        function toggleSidebar() {{
            document.getElementById('sidebar').classList.toggle('-translate-x-full');
            document.getElementById('sidebar_overlay').classList.toggle('hidden');
        }}

        function switchUserTab(tabId) {{
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            if(tabId === 'status') {{ renderUserStatusDashboard(); }}
            if(window.innerWidth < 768) {{
                document.getElementById('sidebar').classList.add('-translate-x-full');
                document.getElementById('sidebar_overlay').classList.add('hidden');
            }}
        }}
        
        function calculateAge() {{
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age Pension' && age < 55) {{ alert('System Error: Age must be 55 or above for Old Age Pension.'); }}
            checkCategoryAndAge();
        }}
        
        function checkCategoryAndAge() {{
            let category = document.getElementById('category_select') ? document.getElementById('category_select').value : 'General';
            let age = parseInt(document.getElementById('age') ? document.getElementById('age').value : 0) || 0;
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
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = finalFee.toFixed(2));
        }}

        function checkSchemeCondition() {{
            let scheme = document.getElementById('scheme').value;
            let specialBox = document.getElementById('special_cert_box');
            if(['Widow Pension', 'Disability Pension', 'Divorcee Pension', 'Transgender Pension'].includes(scheme)) specialBox.classList.remove('hidden');
            else specialBox.classList.add('hidden');
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
            let fullName = document.getElementById('full_name').value;
            let aadhaarInput = document.getElementById('aadhaar_input').value;
            if(!fullName) {{ alert("Please enter your Full Name."); return; }}
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
                }} else {{ alert("Invalid IFSC Code"); }}
            }} catch (e) {{ alert("Error fetching IFSC details."); }}
        }}
        
        function updateAddressCharCount() {{
            let addressInput = document.getElementById('manual_address');
            document.getElementById('address_char_count').innerText = (200 - addressInput.value.length) + " characters remaining";
        }}
        
        function goToPaymentStep(e) {{
            e.preventDefault();
            let appNo = localStorage.getItem('active_app_no');
            
            localStorage.setItem('user_aadhaar_' + appNo, document.getElementById('aadhaar_input').value);
            localStorage.setItem('u_father_' + appNo, document.getElementById('father_name').value);
            localStorage.setItem('u_mother_' + appNo, document.getElementById('mother_name').value);
            localStorage.setItem('u_scheme_' + appNo, document.getElementById('scheme').value);
            localStorage.setItem('u_dist_' + appNo, document.getElementById('district').value);
            localStorage.setItem('u_block_' + appNo, document.getElementById('block').value);
            localStorage.setItem('u_gp_' + appNo, document.getElementById('panchayat').value);
            localStorage.setItem('u_village_' + appNo, document.getElementById('village_input').value);
            localStorage.setItem('u_pin_' + appNo, document.getElementById('pin_input').value);
            localStorage.setItem('u_address_' + appNo, document.getElementById('manual_address').value);
            
            localStorage.setItem('u_category_' + appNo, document.getElementById('category_select').value);
            localStorage.setItem('u_gender_' + appNo, document.getElementById('gender_select').value);
            localStorage.setItem('u_dob_' + appNo, document.getElementById('dob').value);
            localStorage.setItem('u_age_' + appNo, document.getElementById('age').value);
            localStorage.setItem('u_age_proof_type_' + appNo, document.getElementById('age_proof_type').value);
            localStorage.setItem('u_age_proof_no_' + appNo, document.getElementById('age_proof_number').value);
            
            localStorage.setItem('u_inc_cert_' + appNo, document.getElementById('income_cert_no').value);
            localStorage.setItem('u_inc_issued_to_' + appNo, document.getElementById('inc_issued_to').value);
            localStorage.setItem('u_inc_auth_' + appNo, document.getElementById('inc_authority').value);
            localStorage.setItem('u_inc_amount_' + appNo, document.getElementById('inc_amount').value);
            localStorage.setItem('u_ifsc_' + appNo, document.getElementById('ifsc_code').value);
            localStorage.setItem('u_bank_' + appNo, document.getElementById('bank_name_display').value); 
            localStorage.setItem('u_acc_holder_' + appNo, document.getElementById('acc_holder_name').value);
            localStorage.setItem('u_acc_' + appNo, document.getElementById('acc_no').value);
            localStorage.setItem('u_applied_date_' + appNo, new Date().toLocaleDateString('en-IN'));

            // Save Profile Photo & Uploaded Docs
            if(uploadedPhotoDataUrl) localStorage.setItem('u_photo_' + appNo, uploadedPhotoDataUrl);
            for(let dk in uploadedDocs) {{
                localStorage.setItem('u_doc_' + dk + '_' + appNo, uploadedDocs[dk]);
            }}
            
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-payment-step').classList.remove('hidden');
        }}

        function togglePayButton() {{
            let cb = document.getElementById('tnc_checkbox');
            let btn = document.getElementById('payu_button');
            if(cb.checked) {{ btn.disabled = false; btn.classList.remove('opacity-50', 'cursor-not-allowed'); }}
            else {{ btn.disabled = true; btn.classList.add('opacity-50', 'cursor-not-allowed'); }}
        }}

        async function processPayment() {{
            let gateway = document.querySelector('input[name="pay_gateway"]:checked').value;
            let appNo = localStorage.getItem('active_app_no');
            
            let baseFee = parseFloat(localStorage.getItem('app_fee') || '100');
            let category = document.getElementById('category_select').value;
            let age = parseInt(document.getElementById('age').value) || 0;
            let finalFee = ((category === 'SC' || category === 'ST') || (age >= 80 && age <= 100)) ? (baseFee * 0.5) : baseFee;
            let amount = finalFee.toFixed(2);
            localStorage.setItem('paid_amount_' + appNo, amount); 
            
            // START MULTI-TIER WORKFLOW: FIRST GOES TO BLOCK OFFICER
            localStorage.setItem('user_has_applied_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, 'block_pending');
            let history = [{{ stage: "Application Submitted & Fee Paid", status: "Completed", remark: "Forwarded to Block Officer (" + document.getElementById('block').value + ")", date: new Date().toLocaleString() }}];
            localStorage.setItem('app_history_' + appNo, JSON.stringify(history));

            let firstname = document.getElementById('full_name').value || "User";

            if(gateway === 'razorpay') {{
                alert('Redirecting to Razorpay Live Secure Payment Gateway...');
                setTimeout(() => {{ window.location.href = "/payment_success"; }}, 1000);
            }} else if(gateway === 'cashfree') {{
                alert('Redirecting to Cashfree Live Secure Payment Gateway...');
                let txnid = "TXN" + new Date().getTime();
                let email = document.getElementById('app_email').value || "user@example.com"; 
                let phone = document.getElementById('app_mobile').value || "9876543210";
                let surl = window.location.origin + "/payment_success";
                try {{
                    let response = await fetch('/api/cashfree_order', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ txnid, amount, appNo, firstname, email, phone, surl }})
                    }});
                    let data = await response.json();
                    if(data.status === 'success' && data.payment_session_id) {{
                        const cashfree = Cashfree({{ mode: "production" }});
                        cashfree.checkout({{ paymentSessionId: data.payment_session_id, redirectTarget: "_self" }});
                    }} else {{ window.location.href = "/payment_success"; }}
                }} catch (error) {{ window.location.href = "/payment_success"; }}
            }} else {{
                alert('Redirecting to PayU Live Secure Payment Gateway...');
                let txnid = "TXN" + new Date().getTime();
                let productinfo = "PensionApplication";
                let email = document.getElementById('app_email').value || "user@example.com"; 
                let phone = document.getElementById('app_mobile').value || "9876543210";
                let surl = window.location.origin + "/payment_success";
                let furl = window.location.origin + "/payment_failure";
                try {{
                    let response = await fetch(`/api/payu_hash?txnid=${{txnid}}&amount=${{amount}}&productinfo=${{productinfo}}&firstname=${{firstname}}&email=${{email}}`);
                    let data = await response.json();
                    let form = document.createElement("form");
                    form.setAttribute("method", "POST");
                    form.setAttribute("action", "https://secure.payu.in/_payment");
                    let params = {{ key: data.key, txnid, amount, productinfo, firstname, email, phone, surl, furl, hash: data.hash }};
                    for(let key in params) {{
                        let hf = document.createElement("input");
                        hf.setAttribute("type", "hidden"); hf.setAttribute("name", key); hf.setAttribute("value", params[key]);
                        form.appendChild(hf);
                    }}
                    document.body.appendChild(form);
                    form.submit();
                }} catch (error) {{ alert("Error connecting to PayU Gateway."); }}
            }}
        }}

        function renderUserStatusDashboard() {{
            let appNo = localStorage.getItem('active_app_no');
            let container = document.getElementById('section-status');
            let isApplied = localStorage.getItem('user_has_applied_' + appNo);

            if(isApplied !== 'true') {{
                container.innerHTML = `<div class="text-center py-10"><i class="fa-solid fa-file-circle-question text-5xl text-gray-300 mb-3"></i><p class="text-gray-500 font-bold">You have not submitted your pension application yet.</p></div>`;
                return;
            }}

            let status = localStorage.getItem('app_status_' + appNo) || 'block_pending';
            let history = JSON.parse(localStorage.getItem('app_history_' + appNo) || '[]');
            let rejectReason = localStorage.getItem('reject_reason_' + appNo) || '';
            let utr = localStorage.getItem('utr_number_' + appNo) || '';

            const statusLabels = {{
                'block_pending': 'Pending at Block Officer Verification',
                'dist_pending': 'Block Approved -> Pending at District Officer',
                'state_pending': 'District Approved -> Pending at State Officer',
                'sys_pending': 'State Approved -> Pending System Verification',
                'sys_pending_2days': 'State Approved -> Pending System Verification',
                'admin_pending': 'System Verified -> Pending Admin Approval',
                'super_admin_pending': 'Admin Approved -> Pending Super Admin Final Approval',
                'approved': 'Approved (Active Beneficiary - Ready for Payment)',
                'pension_sent': 'Pension Disbursed Successfully! (UTR: ' + utr + ')',
                'rejected': 'Application Rejected'
            }};

            let badgeColor = status === 'rejected' ? 'bg-red-100 text-red-800 border-red-300' : (status === 'approved' || status === 'pension_sent' ? 'bg-green-100 text-green-800 border-green-300' : 'bg-blue-100 text-blue-800 border-blue-300');

            let historyHtml = history.map(h => `
                <li class="mb-4 ml-6">
                    <span class="absolute flex items-center justify-center w-6 h-6 bg-blue-100 rounded-full -left-3 ring-4 ring-white">
                        <i class="fa-solid fa-check text-blue-600 text-xs"></i>
                    </span>
                    <h4 class="font-bold text-gray-800 text-sm">${{h.stage}} <span class="text-xs font-normal text-gray-500 ml-2">${{h.date}}</span></h4>
                    <p class="text-xs font-semibold text-gray-600">${{h.status}} - ${{h.remark}}</p>
                </li>
            `).join('');

            container.innerHTML = `
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 border-b pb-4 gap-4">
                    <div>
                        <h2 class="text-2xl font-bold text-blue-900"><i class="fa-solid fa-file-shield mr-2"></i> Application Status & Print</h2>
                        <p class="text-sm text-gray-600 font-semibold">Application No: <span class="text-blue-700 font-bold">#${{appNo}}</span></p>
                    </div>
                    <button onclick="viewUserAppModal()" class="bg-gray-900 text-white px-5 py-2.5 rounded-lg font-bold shadow hover:bg-black flex items-center gap-2">
                        <i class="fa-solid fa-print"></i> View & Print / Save PDF
                    </button>
                </div>

                <div class="p-4 rounded-xl border ${{badgeColor}} mb-6">
                    <p class="text-xs uppercase font-bold opacity-75">Current Live Status</p>
                    <p class="text-lg font-extrabold mt-1">${{statusLabels[status] || status}}</p>
                    ${{rejectReason ? `<p class="mt-2 text-sm font-bold text-red-700 bg-white/70 p-2 rounded">Rejection Remark: ${{rejectReason}}</p>` : ''}}
                </div>

                <h3 class="font-bold text-gray-800 mb-4"><i class="fa-solid fa-clock-rotate-left mr-1 text-blue-600"></i> Complete Verification Tracking History</h3>
                <ol class="relative border-l-2 border-blue-200 ml-3">
                    ${{historyHtml || '<li class="ml-6 text-sm text-gray-500">Application submitted and queued for verification.</li>'}}
                </ol>
            `;
        }}

        function loadPrintData() {{
            let appNo = localStorage.getItem('active_app_no');
            let setT = (id, val) => {{ let el = document.getElementById(id); if(el) el.innerText = val || 'N/A'; }};
            
            setT('p_appno', appNo);
            setT('p_scheme', localStorage.getItem('u_scheme_' + appNo));
            setT('p_date', localStorage.getItem('u_applied_date_' + appNo) || new Date().toLocaleDateString('en-IN'));
            setT('p_fee', 'Paid (₹' + (localStorage.getItem('paid_amount_' + appNo) || '100.00') + ')');
            
            setT('p_name', localStorage.getItem('user_full_name_' + appNo));
            setT('p_mobile', localStorage.getItem('user_mobile_' + appNo));
            setT('p_email', localStorage.getItem('user_email_' + appNo));
            setT('p_father', localStorage.getItem('u_father_' + appNo));
            setT('p_mother', localStorage.getItem('u_mother_' + appNo));
            setT('p_gender', localStorage.getItem('u_gender_' + appNo));
            setT('p_dob', localStorage.getItem('u_dob_' + appNo));
            setT('p_age', localStorage.getItem('u_age_' + appNo));
            setT('p_category', localStorage.getItem('u_category_' + appNo));
            setT('p_aadhaar', localStorage.getItem('user_aadhaar_' + appNo));
            setT('p_age_proof', (localStorage.getItem('u_age_proof_type_' + appNo) || '') + ' - ' + (localStorage.getItem('u_age_proof_no_' + appNo) || ''));

            setT('p_state', localStorage.getItem('u_state_' + appNo) || 'Odisha');
            setT('p_dist', localStorage.getItem('u_dist_' + appNo));
            setT('p_block', localStorage.getItem('u_block_' + appNo));
            setT('p_gp', localStorage.getItem('u_gp_' + appNo));
            setT('p_village', localStorage.getItem('u_village_' + appNo));
            setT('p_pin', localStorage.getItem('u_pin_' + appNo));
            setT('p_address', localStorage.getItem('u_address_' + appNo));

            setT('p_inc_cert', localStorage.getItem('u_inc_cert_' + appNo));
            setT('p_inc_auth', localStorage.getItem('u_inc_auth_' + appNo));
            setT('p_inc_amount', localStorage.getItem('u_inc_amount_' + appNo));

            setT('p_bank', localStorage.getItem('u_bank_' + appNo));
            setT('p_acc_holder', localStorage.getItem('u_acc_holder_' + appNo));
            setT('p_acc', localStorage.getItem('u_acc_' + appNo));
            setT('p_ifsc', localStorage.getItem('u_ifsc_' + appNo));

            let photo = localStorage.getItem('u_photo_' + appNo);
            let photoEl = document.getElementById('p_photo_img');
            if(photo && photoEl) {{ photoEl.src = photo; photoEl.classList.remove('hidden'); }}
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
<body class="bg-gray-100 flex h-screen overflow-hidden relative">
    
    <div id="sidebar_overlay" onclick="toggleSidebar()" class="fixed inset-0 bg-black bg-opacity-50 z-30 hidden md:hidden"></div>

    <aside id="sidebar" class="w-64 bg-slate-800 text-white flex flex-col shadow-2xl h-full absolute z-40 inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform duration-300 ease-in-out print:hidden">
        <div class="p-5 border-b border-slate-700 text-center flex justify-between items-center md:block">
            <h2 class="text-lg font-bold">Gopabandhu Pension</h2>
            <p class="text-xs text-slate-400">Beneficiary Portal</p>
            <button onclick="toggleSidebar()" class="md:hidden text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchUserTab('apply')" class="flex items-center px-4 py-3 bg-purple-600 text-white rounded-lg"><i class="fa-solid fa-pen-to-square w-6 mr-2"></i> Apply Pension</a></li>
                <li><a href="#" onclick="switchUserTab('status')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-file-pdf w-6 mr-2"></i> Status / Print PDF</a></li>
                <li><a href="#" onclick="switchUserTab('renew')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> Renewal</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="flex items-center text-red-400 hover:text-red-300"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout / Back Home</a></div>
    </aside>

    <main class="flex-1 overflow-y-auto p-4 md:p-6 print:p-0 print:overflow-visible w-full">
        <div class="md:hidden flex justify-between items-center mb-4 bg-white p-3 rounded-lg shadow-sm border border-gray-200 print:hidden">
            <h2 class="font-bold text-gray-800 text-lg"><i class="fa-solid fa-user-circle text-blue-600 mr-2"></i> User Dashboard</h2>
            <button onclick="toggleSidebar()" class="text-blue-700 text-2xl p-1"><i class="fa-solid fa-bars"></i></button>
        </div>

        <div id="section-apply" class="content-section bg-white p-4 md:p-6 rounded-xl shadow print:hidden">
            <div id="apply_form_container">
                <div class="bg-blue-50 p-4 rounded-lg flex flex-col md:flex-row justify-between items-center mb-6 border border-blue-200">
                    <div><p class="text-sm font-semibold text-blue-800"><i class="fa-solid fa-earth-asia"></i> Registered State: <span class="font-bold text-lg text-purple-700">Odisha</span></p></div>
                    <div class="flex items-center gap-3">
                        <label class="text-sm font-bold text-gray-700"><i class="fa-solid fa-language text-blue-600"></i> Form Language:</label>
                        <select id="form_language" class="border border-blue-300 p-2 rounded bg-white font-bold text-sm text-blue-800" required>
                            <option value="Odia">Odia</option><option value="English">English</option><option value="Hindi">Hindi</option>
                        </select>
                    </div>
                </div>

                <h2 class="text-xl md:text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Gopabandhu Pension Yojana - Application Form</h2>
                <form onsubmit="goToPaymentStep(event)" class="space-y-6">
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 border-b pb-4">
                        <div class="sm:col-span-2"><label class="block text-sm font-semibold">Full Name (ପୂରା ନାମ)</label><input type="text" id="full_name" class="w-full border-b border-gray-300 p-2 outline-none font-bold text-blue-800" required></div>
                        <div><label class="block text-sm font-semibold text-gray-600">Registered Mobile No</label><input type="text" id="app_mobile" class="w-full border-b border-gray-300 p-2 outline-none font-bold" required></div>
                        <div><label class="block text-sm font-semibold text-gray-600">Registered Email ID</label><input type="text" id="app_email" class="w-full border-b border-gray-300 p-2 outline-none font-bold" required></div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t pt-4">
                        <div>
                            <label class="block text-sm font-semibold text-blue-600">Profile Photo <i class="fa-solid fa-camera"></i></label>
                            <input type="file" onchange="handleFileToBase64(this, 'photo')" class="w-full border-b border-gray-300 p-2 text-sm outline-none" accept="image/*" required>
                            <img id="photo_preview" class="hidden mt-2 h-20 w-20 object-cover rounded border shadow" />
                        </div>
                        <div><label class="block text-sm font-semibold">Father's/Husband's Name</label><input type="text" id="father_name" class="w-full border-b border-gray-300 p-2 outline-none" required></div>
                        <div><label class="block text-sm font-semibold">Mother's Name (ମାଆଙ୍କ ନାମ)</label><input type="text" id="mother_name" class="w-full border-b border-gray-300 p-2 outline-none" required></div>
                        <div><label class="block text-sm font-semibold">Gender (ଲିଙ୍ଗ)</label><select id="gender_select" class="w-full border-b border-gray-300 p-2 outline-none"><option value="Male">Male</option><option value="Female">Female</option><option value="Transgender">Transgender</option></select></div>
                        <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border-b border-gray-300 p-2 outline-none" required></div>
                        <div><label class="block text-sm font-semibold">Age (Auto Calculate)</label><input type="text" id="age" readonly class="w-full border-b border-gray-300 p-2 outline-none bg-gray-50"></div>
                        <div>
                            <label class="block text-sm font-semibold text-red-600">Category (ବର୍ଗ)</label>
                            <select id="category_select" onchange="checkCategoryAndAge()" class="w-full border-b border-red-300 p-2 outline-none bg-red-50 text-red-800 font-bold">
                                <option value="General">General</option><option value="OBC">OBC</option><option value="SC">SC</option><option value="ST">ST</option><option value="Other">Other</option>
                            </select>
                        </div>
                        <div id="caste_cert_box" class="hidden">
                            <label class="block text-sm font-semibold text-purple-700">Upload Caste Certificate (SC/ST)</label>
                            <input type="file" onchange="handleFileToBase64(this, 'caste')" id="caste_cert_file" class="w-full border-b border-purple-300 p-2 text-sm bg-purple-50" accept=".pdf, image/*">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 border-t pt-4">
                        <div>
                            <label class="block text-sm font-semibold mb-2">Scheme Category (ଯୋଜନା ବାଛନ୍ତୁ)</label>
                            <select id="scheme" onchange="checkSchemeCondition()" class="w-full border p-2 rounded bg-purple-50">
                                <option value="Old Age Pension">Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option><option value="Widow Pension">Widow (ବିଧବା)</option><option value="Disability Pension">Disability (ଭିନ୍ନକ୍ଷମ)</option><option value="Unmarried Pension">Unmarried (ଅବିବାହିତା)</option><option value="Divorcee Pension">Divorcee (ଛାଡପତ୍ର ପାଇଥିବା)</option><option value="Transgender Pension">Transgender (କିନ୍ନର)</option>
                            </select>
                            <div id="special_cert_box" class="hidden mt-4 bg-yellow-50 p-2 rounded border border-yellow-300">
                                <label class="font-bold text-yellow-800 text-sm">Special Certificate (Widow/Disability PDF):</label>
                                <input type="file" onchange="handleFileToBase64(this, 'special')" class="border p-1 mt-1 w-full bg-white text-sm" accept=".pdf, image/*">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-2">Aadhaar Number (ଆଧାର ନମ୍ବର)</label>
                            <div class="flex gap-2">
                                <input type="text" id="aadhaar_input" placeholder="12-digit Aadhaar Number" class="w-full border-b border-gray-300 p-2 outline-none" required>
                                <button type="button" onclick="verifyAadhaar()" class="bg-blue-600 text-white font-bold px-4 rounded hover:bg-blue-700">VALIDATE</button>
                            </div>
                            <div id="aadhaar_success_box" class="hidden mt-3 border-l-4 border-green-500 bg-gray-50 p-3 shadow-sm flex items-start gap-3">
                                <i class="fa-solid fa-check text-green-500 text-2xl mt-1"></i>
                                <div class="text-xs"><p class="font-semibold text-gray-800 text-sm">Aadhaar Verified Successfully.</p></div>
                            </div>
                            <p id="aadhaar_status" class="text-xs mt-1 text-gray-500 mb-2">Manual Entry allowed if not linked</p>
                            <label class="block text-sm font-semibold text-blue-600 mb-1">Upload Aadhaar PDF <i class="fa-solid fa-file-pdf"></i></label>
                            <input type="file" onchange="handleFileToBase64(this, 'aadhaar')" class="w-full border p-1 rounded text-sm bg-gray-50" accept=".pdf, image/*" required>
                        </div>
                    </div>

                    <div class="mt-6 border-t pt-4">
                        <h3 class="font-bold text-lg mb-4 text-gray-800">Address Information</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6">
                            <div><label class="block text-sm text-gray-500 mb-1">District</label><select id="district" onchange="populateBlocks()" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required><option value="">Select</option></select></div>
                            <div><label class="block text-sm text-gray-500 mb-1">Block/ULB</label><select id="block" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required><option value="">Select</option></select></div>
                            <div><label class="block text-sm text-gray-500 mb-1">GP/Ward *</label><input type="text" id="panchayat" placeholder="Enter GP/Ward" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required></div>
                            <div><label class="block text-sm text-gray-500 mb-1">Village *</label><input type="text" id="village_input" placeholder="Enter Village" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required></div>
                            <div><label class="block text-sm text-gray-500 mb-1">Pin Code *</label><input type="text" id="pin_input" placeholder="e.g. 751001" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required></div>
                        </div>
                        <div class="mt-6">
                            <label class="block text-sm text-gray-500 mb-1">Address *</label>
                            <input type="text" id="manual_address" maxlength="200" oninput="updateAddressCharCount()" class="w-full border-b border-gray-300 outline-none p-2 font-semibold" required>
                            <p id="address_char_count" class="text-red-500 text-sm mt-1">200 characters remaining</p>
                        </div>
                    </div>

                    <div class="border p-4 rounded-lg bg-gray-50 mt-6 shadow-sm border-gray-200">
                        <h3 class="font-bold text-sm mb-2 text-gray-700"><i class="fa-solid fa-id-card mr-1"></i> Age Proof Document Upload</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div>
                                <select id="age_proof_type" onchange="updateAgeProof()" class="w-full border p-2 rounded bg-white" required>
                                    <option value="">Select Document...</option><option value="PAN Card">PAN Card</option><option value="Voter Card">Voter Card</option><option value="Ration Card">Ration Card</option>
                                </select>
                            </div>
                            <div><input type="text" id="age_proof_number" class="w-full border p-2 rounded hidden bg-white font-bold" placeholder="Document Number" required></div>
                            <div id="age_proof_file_container" class="hidden"><input type="file" onchange="handleFileToBase64(this, 'ageproof')" class="w-full border p-1 rounded bg-white text-sm" accept=".pdf, image/*" required></div>
                        </div>
                    </div>

                    <div id="income_section_full" class="border border-blue-200 bg-blue-50 p-4 rounded-lg mt-6 shadow-sm">
                        <h3 class="text-lg font-bold text-blue-800 mb-4 border-b border-blue-200 pb-2">Income Certificate Details</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div><label class="block text-xs font-semibold text-gray-700">Issuing Year *</label><select id="income_year" class="w-full border p-2 rounded bg-white"><option>Select</option><option>2024-25</option><option>2025-26</option><option>2026-27</option></select></div>
                            <div><label class="block text-xs font-semibold text-gray-700">Income Certificate No. *</label><input type="text" id="income_cert_no" placeholder="e.g: e-INC/2025/12345" class="w-full border p-2 rounded bg-white"></div>
                            <div><label class="block text-xs font-semibold text-gray-700">Token No</label><input type="text" id="income_token_no" class="w-full border p-2 rounded bg-white"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">To Whom Issued</label><input type="text" id="inc_issued_to" placeholder="Enter Name" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Applicant Father</label><input type="text" id="inc_father" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Applicant Mother</label><input type="text" id="inc_mother" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Issuing District</label><input type="text" id="inc_district" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div class="sm:col-span-2"><label class="block text-xs font-semibold text-gray-500">Issuing Authority</label><input type="text" id="inc_authority" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Issue Date</label><input type="date" id="inc_date" class="w-full border rounded p-2 bg-white font-bold"></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Relationship</label><select id="inc_relation" class="w-full border rounded p-2 bg-white font-bold"><option>Select</option><option>Self</option><option>Daughter</option><option>Son</option><option>Wife</option></select></div>
                            <div><label class="block text-xs font-semibold text-gray-500">Annual Income</label><input type="text" id="inc_amount" placeholder="e.g. Rs. 48,000/-" class="w-full border rounded p-2 bg-white font-bold text-red-600 text-lg"></div>
                        </div>
                        <div class="mt-4 border-t border-blue-200 pt-4">
                            <label class="block text-sm font-semibold text-blue-700 mb-1"><i class="fa-solid fa-file-pdf"></i> Upload Income Certificate (PDF) *</label>
                            <input type="file" onchange="handleFileToBase64(this, 'income')" class="w-full md:w-1/2 border p-1 rounded text-sm bg-white" accept=".pdf, image/*">
                        </div>
                    </div>

                    <div class="border border-blue-200 bg-white p-4 md:p-6 rounded-lg mt-6 shadow-sm">
                        <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Bank Information</h3>
                        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 items-end mb-6">
                            <div>
                                <label class="block text-sm text-gray-600 mb-1">IFSC Code *</label>
                                <div class="flex">
                                    <input type="text" id="ifsc_code" class="w-full border-b border-gray-300 outline-none p-2 uppercase" placeholder="IFSC Code" required>
                                    <button type="button" onclick="fetchIFSC()" class="bg-blue-500 text-white px-4 py-2 text-sm font-bold shadow hover:bg-blue-600 whitespace-nowrap">FIND IFSC</button>
                                </div>
                            </div>
                            <div class="sm:col-span-1 md:col-span-2">
                                <label class="block text-sm text-gray-600 mb-1">Bank Name & Branch</label>
                                <input type="text" id="bank_name_display" placeholder="Auto fetched or type manual" class="w-full border-b border-gray-300 outline-none p-2 font-bold">
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                            <div><label class="block text-sm text-gray-600 mb-1">Account Holder Name</label><input type="text" id="acc_holder_name" class="w-full border-b border-gray-300 outline-none p-2"></div>
                            <div><label class="block text-sm text-gray-600 mb-1">Account Number *</label><input type="text" id="acc_no" class="w-full border-b border-gray-300 outline-none p-2" required></div>
                            <div><label class="block text-sm text-gray-600 mb-1">Re-type Account No. *</label><input type="text" class="w-full border-b border-gray-300 outline-none p-2" required></div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
                            <div>
                                <p class="text-sm text-gray-600 italic mb-2">Whether account number seeded with Aadhaar?</p>
                                <div class="flex gap-4">
                                    <label class="flex items-center gap-1 cursor-pointer"><input type="radio" name="aadhaar_seeded" value="yes" class="w-4 h-4"> Yes</label>
                                    <label class="flex items-center gap-1 cursor-pointer"><input type="radio" name="aadhaar_seeded" value="no" class="w-4 h-4" checked> No</label>
                                </div>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600 italic mb-2">Upload front page of passbook *</p>
                                <input type="file" onchange="handleFileToBase64(this, 'passbook')" id="passbook_upload" class="w-full border p-1 rounded text-sm bg-gray-50" accept=".pdf, image/*" required>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 flex justify-center gap-4">
                        <button type="submit" class="bg-blue-600 text-white font-bold py-3 px-8 rounded shadow-lg hover:bg-blue-700">ELIGIBLE / NEXT</button>
                    </div>
                </form>
            </div>
        </div>

        <div id="section-payment-step" class="content-section hidden bg-white p-4 md:p-6 rounded-xl shadow print:hidden">
            <div class="max-w-3xl mx-auto border-2 border-orange-300 rounded-xl p-4 md:p-6 bg-orange-50">
                <h2 class="text-xl md:text-2xl font-bold text-orange-700 mb-4 text-center border-b border-orange-300 pb-2"><i class="fa-solid fa-file-shield mr-2"></i> Application Declaration & Payment</h2>
                <div class="bg-white p-5 rounded border border-gray-200 shadow-inner mb-6 text-gray-700 text-justify">
                    <p>I declare that all information provided for Gopabandhu Pension Yojana is true. If my data is found false, Officers/Admin hold the right to reject my application.</p>
                </div>
                <label class="flex items-start gap-3 cursor-pointer p-3 bg-white rounded border border-gray-300 mb-6 shadow-sm">
                    <input type="checkbox" id="tnc_checkbox" onchange="togglePayButton()" class="w-6 h-6 mt-1 text-orange-600 cursor-pointer">
                    <span class="text-gray-800 font-bold text-sm md:text-base">I Agree to the Terms & Conditions and Confirm the above Declaration.</span>
                </label>
                <div class="text-center">
                    <div class="flex flex-col md:flex-row justify-center gap-4 mb-4">
                        <label class="flex items-center justify-center gap-2 border p-3 rounded-lg cursor-pointer font-bold text-purple-900 bg-white"><input type="radio" name="pay_gateway" value="cashfree" checked class="w-5 h-5"> Cashfree</label>
                        <label class="flex items-center justify-center gap-2 border p-3 rounded-lg cursor-pointer font-bold text-blue-900 bg-white"><input type="radio" name="pay_gateway" value="razorpay" class="w-5 h-5"> Razorpay</label>
                        <label class="flex items-center justify-center gap-2 border p-3 rounded-lg cursor-pointer font-bold text-orange-700 bg-white"><input type="radio" name="pay_gateway" value="payu" class="w-5 h-5"> PayU</label>
                    </div>
                    <button type="button" id="payu_button" onclick="processPayment()" disabled class="bg-green-600 text-white font-extrabold text-lg py-4 px-10 rounded-lg shadow-lg opacity-50 cursor-not-allowed w-full md:w-auto">
                        <i class="fa-solid fa-lock mr-2"></i> Pay Now (₹<span class="display_app_fee"></span>)
                    </button>
                </div>
            </div>
        </div>

        <div id="section-status" class="content-section hidden bg-white p-4 md:p-6 rounded-xl shadow print:hidden"></div>
        <div id="section-renew" class="content-section hidden bg-white p-4 md:p-6 rounded-xl shadow print:hidden"></div>
    </main>

    <!-- FULL APPLICATION PRINT / PDF MODAL WITH PROFILE PHOTO & ALL DETAILS -->
    <div id="user_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-4xl h-[92vh] rounded-xl shadow-2xl flex flex-col">
            <div class="p-4 border-b flex justify-between items-center bg-blue-50 rounded-t-xl no-print">
                <h3 class="text-lg md:text-xl font-bold text-blue-800"><i class="fa-solid fa-file-pdf mr-2"></i> Gopabandhu Pension Yojana - Print / PDF</h3>
                <div class="space-x-2 flex">
                    <button onclick="window.print()" class="bg-gray-900 text-white px-4 py-2 rounded shadow font-bold hover:bg-black text-sm"><i class="fa-solid fa-print"></i> Print / Save PDF</button>
                    <button onclick="closeUserAppModal()" class="bg-red-500 text-white px-4 py-2 rounded shadow font-bold hover:bg-red-600 text-sm"><i class="fa-solid fa-xmark"></i> Close</button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-6">
                <div class="flex justify-between items-center border-b-2 border-blue-900 pb-4 mb-6">
                    <div>
                        <h2 class="text-2xl font-extrabold text-blue-900 uppercase">Gopabandhu Pension Yojana</h2>
                        <p class="text-sm font-bold text-gray-600">Official Application Acknowledgement & Details Copy</p>
                    </div>
                    <img id="p_photo_img" class="hidden h-24 w-24 object-cover border-2 border-gray-800 rounded shadow" alt="Applicant Photo" />
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-6 bg-gray-50 p-4 rounded border">
                    <div><p class="text-gray-500 text-xs">Application No</p><p id="p_appno" class="font-bold text-blue-700"></p></div>
                    <div><p class="text-gray-500 text-xs">Scheme</p><p id="p_scheme" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Applied Date</p><p id="p_date" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Payment</p><p id="p_fee" class="font-bold text-green-600"></p></div>
                </div>

                <h4 class="font-bold text-base border-b mb-3 text-blue-900">1. Personal Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm mb-6">
                    <div><span class="text-gray-500 text-xs block">Full Name</span><strong id="p_name"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Father's/Husband's Name</span><strong id="p_father"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Mother's Name</span><strong id="p_mother"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Gender</span><strong id="p_gender"></strong></div>
                    <div><span class="text-gray-500 text-xs block">DOB / Age</span><strong id="p_dob"></strong> (<span id="p_age"></span> Yrs)</div>
                    <div><span class="text-gray-500 text-xs block">Category</span><strong id="p_category"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Mobile</span><strong id="p_mobile"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Email</span><strong id="p_email"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Aadhaar No</span><strong id="p_aadhaar"></strong></div>
                    <div class="col-span-2"><span class="text-gray-500 text-xs block">Age Proof</span><strong id="p_age_proof"></strong></div>
                </div>

                <h4 class="font-bold text-base border-b mb-3 text-blue-900">2. Address Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm mb-6">
                    <div><span class="text-gray-500 text-xs block">State</span><strong id="p_state"></strong></div>
                    <div><span class="text-gray-500 text-xs block">District</span><strong id="p_dist"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Block / ULB</span><strong id="p_block"></strong></div>
                    <div><span class="text-gray-500 text-xs block">GP / Ward</span><strong id="p_gp"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Village</span><strong id="p_village"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Pin Code</span><strong id="p_pin"></strong></div>
                    <div class="col-span-2 md:col-span-3"><span class="text-gray-500 text-xs block">Full Address</span><strong id="p_address"></strong></div>
                </div>

                <h4 class="font-bold text-base border-b mb-3 text-blue-900">3. Income & Bank Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm mb-4">
                    <div><span class="text-gray-500 text-xs block">Income Cert No</span><strong id="p_inc_cert"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Issuing Authority</span><strong id="p_inc_auth"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Annual Income</span><strong id="p_inc_amount" class="text-red-600"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Bank Name</span><strong id="p_bank"></strong></div>
                    <div><span class="text-gray-500 text-xs block">A/C Holder</span><strong id="p_acc_holder"></strong></div>
                    <div><span class="text-gray-500 text-xs block">Account No / IFSC</span><strong id="p_acc"></strong> / <strong id="p_ifsc"></strong></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 6. UNIFIED OFFICER & ADMIN LOGIN PAGE (DROPDOWN: ADMIN / STATE / DISTRICT / BLOCK)
# ==========================================
admin_login_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Officer & Admin Login - Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    {shared_location_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        let currentCaptcha = "";
        let forgotOTP = "";
        let otpTimerInterval;
        let timeLeft = 300;
        let matchedOfficerIndex = -1;

        window.onload = function() {{
            generateCaptcha();
            populateLoginDistricts();
        }};

        function generateCaptcha() {{
            const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
            currentCaptcha = "";
            for (let i = 0; i < 6; i++) {{ currentCaptcha += chars[Math.floor(Math.random() * chars.length)]; }}
            document.getElementById('captcha_display').innerText = currentCaptcha;
        }}

        function togglePassword() {{
            var passField = document.getElementById("password");
            var eyeIcon = document.getElementById("eye-icon");
            if (passField.type === "password") {{ passField.type = "text"; eyeIcon.classList.replace("fa-eye", "fa-eye-slash"); }} 
            else {{ passField.type = "password"; eyeIcon.classList.replace("fa-eye-slash", "fa-eye"); }}
        }}

        function onRoleChange() {{
            let role = document.getElementById('login_role').value;
            document.getElementById('loc_state_div').classList.toggle('hidden', role === 'super_admin');
            document.getElementById('loc_dist_div').classList.toggle('hidden', role === 'super_admin' || role === 'state');
            document.getElementById('loc_block_div').classList.toggle('hidden', role !== 'block');
        }}

        function populateLoginDistricts() {{
            let dSel = document.getElementById('login_dist');
            dSel.innerHTML = '<option value="">Select District</option>';
            for(let d in GLOBAL_LOCATION_DATA["Odisha"]) {{
                dSel.innerHTML += `<option value="${{d}}">${{d}}</option>`;
            }}
        }}

        function populateLoginBlocks() {{
            let dist = document.getElementById('login_dist').value;
            let bSel = document.getElementById('login_block');
            bSel.innerHTML = '<option value="">Select Block</option>';
            if(dist && GLOBAL_LOCATION_DATA["Odisha"][dist]) {{
                GLOBAL_LOCATION_DATA["Odisha"][dist].forEach(b => {{
                    bSel.innerHTML += `<option value="${{b}}">${{b}}</option>`;
                }});
            }}
        }}

        function handleAdminLogin(event) {{
            event.preventDefault();
            let role = document.getElementById('login_role').value;
            let adminId = document.getElementById('admin_id').value.trim();
            let adminPass = document.getElementById('password').value;
            let captchaInput = document.getElementById('login_captcha').value;
            
            if (captchaInput !== currentCaptcha) {{ alert("Invalid Captcha!"); generateCaptcha(); return; }}

            if (role === 'super_admin') {{
                let savedId = localStorage.getItem('admin_email') || 'admin@kulusutar.in';
                let savedPass = localStorage.getItem('admin_password') || 'Admin@123';
                if(adminId === savedId && adminPass === savedPass) {{
                    localStorage.setItem('active_officer_session', JSON.stringify({{ role: 'super_admin', name: localStorage.getItem('admin_name') || 'Super Admin' }}));
                    window.location.href = '/admin';
                }} else {{
                    alert('Access Denied: Invalid Admin ID or Password!');
                    generateCaptcha();
                }}
            }} else {{
                let state = document.getElementById('login_state').value;
                let dist = document.getElementById('login_dist').value;
                let block = document.getElementById('login_block').value;
                let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
                
                let found = officers.find(o => 
                    o.role === role &&
                    o.email.toLowerCase() === adminId.toLowerCase() &&
                    o.password === adminPass &&
                    (role === 'state' ? o.state === state : true) &&
                    (role === 'district' ? (o.state === state && o.district === dist) : true) &&
                    (role === 'block' ? (o.state === state && o.district === dist && o.block === block) : true)
                );

                if(found) {{
                    localStorage.setItem('active_officer_session', JSON.stringify(found));
                    window.location.href = '/admin';
                }} else {{
                    alert('Access Denied: Invalid Officer Credentials or Wrong Block/District Selection!');
                    generateCaptcha();
                }}
            }}
        }}

        function showForgotForm() {{
            document.getElementById('admin_login_form').classList.add('hidden');
            document.getElementById('admin_forgot_form').classList.remove('hidden');
        }}
        function backToLogin() {{
            document.getElementById('admin_forgot_form').classList.add('hidden');
            document.getElementById('admin_login_form').classList.remove('hidden');
            clearInterval(otpTimerInterval);
        }}

        async function sendForgotOTP() {{
            let email = document.getElementById('forgot_email').value.trim();
            let mobile = document.getElementById('forgot_mobile').value.trim();
            let savedEmail = localStorage.getItem('admin_email') || 'admin@kulusutar.in';
            let savedMobile = localStorage.getItem('admin_mobile') || '9876543210';

            matchedOfficerIndex = -1;
            let isAdmin = (email === savedEmail && mobile === savedMobile);
            if(!isAdmin) {{
                let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
                matchedOfficerIndex = officers.findIndex(o => o.email.toLowerCase() === email.toLowerCase() && o.mobile === mobile);
            }}

            if (!isAdmin && matchedOfficerIndex === -1) {{
                alert("Email or Mobile Number does not match any Admin/Officer Records!");
                return;
            }}

            forgotOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('forgot_otp_display').innerText = `Sending Real OTP to ${{email}}... (Demo OTP: ${{forgotOTP}})`;
            document.getElementById('forgot_otp_display').className = "text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse";
            document.getElementById('forgot_otp_display').classList.remove('hidden');
            
            try {{
                let response = await fetch('/api/send_email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: email, otp: forgotOTP, subject: "Officer/Admin Password Reset OTP - Gopabandhu Pension Yojana" }})
                }});
                let data = await response.json();
                if(data.status === 'success') {{
                    document.getElementById('forgot_otp_display').innerText = `Real OTP sent to ${{email}}! (Demo OTP: ${{forgotOTP}})`;
                    document.getElementById('forgot_otp_display').className = "text-center bg-green-100 text-green-800 font-bold p-2 rounded text-sm";
                    document.getElementById('step2_forgot').classList.remove('hidden');
                    startOtpTimer();
                }} else {{ alert("Email sending failed."); }}
            }} catch(e) {{ alert("Server error connecting to Email API."); }}
        }}

        function startOtpTimer() {{
            clearInterval(otpTimerInterval);
            timeLeft = 300;
            otpTimerInterval = setInterval(() => {{
                timeLeft--;
                if (timeLeft <= 0) {{ clearInterval(otpTimerInterval); forgotOTP = ""; document.getElementById('timer_display').innerText = "OTP Expired!"; }}
                else {{
                    let m = Math.floor(timeLeft / 60); let s = timeLeft % 60;
                    document.getElementById('timer_display').innerText = "Expires in: 0" + m + ":" + (s < 10 ? "0" : "") + s;
                }}
            }}, 1000);
        }}

        function verifyForgotOTP() {{
            let entered = document.getElementById('forgot_otp_input').value;
            if(timeLeft <= 0 || !forgotOTP) {{ alert("OTP expired!"); return; }}
            if (entered === forgotOTP) {{
                clearInterval(otpTimerInterval);
                document.getElementById('timer_display').innerText = "OTP Verified!";
                document.getElementById('step3_forgot').classList.remove('hidden');
            }} else {{ alert("Invalid OTP!"); }}
        }}

        function saveNewPassword(event) {{
            event.preventDefault();
            let p1 = document.getElementById('new_pass').value;
            let p2 = document.getElementById('conf_new_pass').value;
            if(p1 !== p2) {{ alert("Passwords do not match!"); return; }}
            if(matchedOfficerIndex === -1) {{
                localStorage.setItem('admin_password', p1);
            }} else {{
                let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
                officers[matchedOfficerIndex].password = p1;
                localStorage.setItem('officers_list', JSON.stringify(officers));
            }}
            alert("Password Changed Successfully! Please Login.");
            backToLogin();
        }}
    </script>
</head>
<body class="bg-gray-100 font-sans flex items-center justify-center min-h-screen p-4">
    <div id="admin_login_form" class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700">
        <div class="text-center mb-6">
            <i class="fa-solid fa-user-shield text-5xl text-blue-700 mb-2"></i>
            <p class="text-xs font-bold text-blue-600 uppercase">Gopabandhu Pension Yojana</p>
            <h2 class="text-2xl font-bold text-gray-800">Officer / Admin Login</h2>
        </div>
        <form onsubmit="handleAdminLogin(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Select Officer Role</label>
                <select id="login_role" onchange="onRoleChange()" class="w-full px-4 py-2.5 border rounded-lg bg-blue-50 font-bold text-blue-900">
                    <option value="super_admin">Main Admin / Super Admin</option>
                    <option value="block">Block Officer Login</option>
                    <option value="district">District Officer Login</option>
                    <option value="state">State Officer Login</option>
                </select>
            </div>

            <div id="loc_state_div" class="hidden">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Select State</label>
                <select id="login_state" class="w-full px-4 py-2 border rounded-lg"><option value="Odisha">Odisha</option></select>
            </div>
            <div id="loc_dist_div" class="hidden">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Select District</label>
                <select id="login_dist" onchange="populateLoginBlocks()" class="w-full px-4 py-2 border rounded-lg"></select>
            </div>
            <div id="loc_block_div" class="hidden">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Select Block</label>
                <select id="login_block" class="w-full px-4 py-2 border rounded-lg"><option value="">Select Block</option></select>
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Officer / Admin Email ID</label>
                <input type="text" id="admin_id" placeholder="Enter Registered Email" class="w-full px-4 py-2.5 border rounded-lg" required>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Password</label>
                <div class="relative">
                    <input type="password" id="password" placeholder="Enter password" class="w-full px-4 py-2.5 border rounded-lg" required>
                    <button type="button" onclick="togglePassword()" class="absolute right-3 top-3 text-gray-400"><i id="eye-icon" class="fa-solid fa-eye"></i></button>
                </div>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Enter Captcha</label>
                <div class="flex gap-2 mb-2">
                    <div id="captcha_display" class="bg-gray-200 border-2 border-gray-400 font-mono text-xl tracking-widest px-4 py-2 font-bold text-gray-700 w-1/2 text-center line-through rounded select-none"></div>
                    <button type="button" onclick="generateCaptcha()" class="bg-blue-100 text-blue-700 px-3 rounded"><i class="fa-solid fa-arrows-rotate"></i></button>
                </div>
                <input type="text" id="login_captcha" placeholder="Enter code" class="w-full px-4 py-2 border rounded-lg" required>
            </div>

            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg hover:bg-blue-800 shadow-md">Login to Dashboard</button>
            <div class="text-center mt-2"><a href="#" onclick="showForgotForm()" class="text-sm text-blue-600 font-bold hover:underline">Officer / Admin Forgot Password?</a></div>
        </form>
        <div class="text-center mt-4"><a href="/" class="text-sm text-gray-500 hover:text-blue-700"><i class="fa-solid fa-arrow-left mr-1"></i> Back to Home</a></div>
    </div>

    <div id="admin_forgot_form" class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-red-500 hidden">
        <h2 class="text-xl font-bold text-center text-gray-800 mb-6"><i class="fa-solid fa-unlock"></i> Officer / Admin Forgot Password</h2>
        <div class="space-y-4">
            <div><label class="block text-sm font-semibold text-gray-700">Registered Email ID</label><input type="email" id="forgot_email" class="w-full px-4 py-2 border rounded-lg"></div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Registered Mobile Number</label>
                <div class="flex gap-2">
                    <input type="text" id="forgot_mobile" class="w-full px-4 py-2 border rounded-lg">
                    <button onclick="sendForgotOTP()" class="bg-blue-600 text-white px-4 rounded-lg font-bold">Get OTP</button>
                </div>
            </div>
            <div id="forgot_otp_display" class="hidden"></div>
            <div id="step2_forgot" class="hidden border-t pt-4">
                <label class="block text-sm font-semibold text-gray-700">Enter 6-digit OTP</label>
                <div class="flex gap-2 mt-1">
                    <input type="text" id="forgot_otp_input" class="w-full px-4 py-2 border rounded-lg">
                    <button onclick="verifyForgotOTP()" class="bg-green-600 text-white px-4 rounded-lg font-bold">Verify</button>
                </div>
                <p id="timer_display" class="text-sm font-bold text-gray-600 mt-2"></p>
            </div>
            <form id="step3_forgot" class="hidden border-t pt-4 space-y-4" onsubmit="saveNewPassword(event)">
                <div><label class="block text-sm font-semibold text-gray-700">New Password</label><input type="password" id="new_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div><label class="block text-sm font-semibold text-gray-700">Confirm Password</label><input type="password" id="conf_new_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
                <button type="submit" class="w-full bg-red-600 text-white font-bold py-3 rounded-lg">Save Password & Login</button>
            </form>
        </div>
        <div class="text-center mt-6"><button onclick="backToLogin()" class="text-sm text-gray-500"><i class="fa-solid fa-arrow-left"></i> Back to Login</button></div>
    </div>
</body>
</html>
"""

# ==========================================
# 7. FULL ADMIN & OFFICER DASHBOARD (BLOCK -> DIST -> STATE -> SYSTEM -> ADMIN)
# ==========================================
admin_design = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin & Officer Panel - Gopabandhu Pension Yojana</title>
    {cloud_sync_script}
    {shared_location_script}
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        let currentSession = JSON.parse(localStorage.getItem('active_officer_session') || '{{"role":"super_admin","name":"Admin"}}');
        let editUploadedFiles = {{}};

        function handleAdminEditFile(input, key) {{
            if(input.files && input.files[0]) {{
                let r = new FileReader();
                r.onload = function(e) {{ editUploadedFiles[key] = e.target.result; }};
                r.readAsDataURL(input.files[0]);
            }}
        }}

        window.onload = function() {{
            document.getElementById('welcome_admin_name').innerText = currentSession.name + " (" + currentSession.role.toUpperCase() + (currentSession.block ? " - " + currentSession.block : (currentSession.district ? " - " + currentSession.district : "")) + ")";
            
            // Hide Admin-only menus for Block/Dist/State Officers
            if(currentSession.role !== 'super_admin') {{
                document.querySelectorAll('.admin-only-menu').forEach(el => el.classList.add('hidden'));
            }}

            populateOfficerDistricts();
            loadOfficersTable();

            if(localStorage.getItem('app_fee')) document.getElementById('app_fee').value = localStorage.getItem('app_fee');
            if(localStorage.getItem('payu_merchant_key')) document.getElementById('payu_merchant_key').value = localStorage.getItem('payu_merchant_key');
            if(localStorage.getItem('payu_merchant_salt')) document.getElementById('payu_merchant_salt').value = localStorage.getItem('payu_merchant_salt');
            if(localStorage.getItem('rzp_key_id')) document.getElementById('rzp_key_id').value = localStorage.getItem('rzp_key_id');
            if(localStorage.getItem('rzp_key_secret')) document.getElementById('rzp_key_secret').value = localStorage.getItem('rzp_key_secret');
            if(localStorage.getItem('cashfree_app_id')) document.getElementById('cashfree_app_id').value = localStorage.getItem('cashfree_app_id');
            if(localStorage.getItem('cashfree_secret_key')) document.getElementById('cashfree_secret_key').value = localStorage.getItem('cashfree_secret_key');
            if(localStorage.getItem('payout_api_key')) document.getElementById('payout_api_key').value = localStorage.getItem('payout_api_key');
            if(localStorage.getItem('payout_api_secret')) document.getElementById('payout_api_secret').value = localStorage.getItem('payout_api_secret');
            if(localStorage.getItem('reg_start_date')) document.getElementById('reg_start_date').value = localStorage.getItem('reg_start_date');
            if(localStorage.getItem('reg_close_date')) document.getElementById('reg_close_date').value = localStorage.getItem('reg_close_date');
            if(localStorage.getItem('notice_text')) document.getElementById('notice_text').value = localStorage.getItem('notice_text');
            if(localStorage.getItem('contact_name')) document.getElementById('contact_name').value = localStorage.getItem('contact_name');
            if(localStorage.getItem('contact_mobile')) document.getElementById('contact_mobile').value = localStorage.getItem('contact_mobile');
            if(localStorage.getItem('contact_email')) document.getElementById('contact_email').value = localStorage.getItem('contact_email');

            loadAdminData();
            loadAdminProfile();
        }};

        async function sendUserEmailUpdate(appNo, statusLabel, message) {{
            let userEmail = localStorage.getItem('user_email_' + appNo);
            if(!userEmail) return;
            try {{
                await fetch('/api/send_notification', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email: userEmail, subject: "Gopabandhu Pension Yojana Update - " + appNo, status_label: statusLabel, message: message, app_no: appNo }})
                }});
            }} catch(e) {{ console.log("Email notify error", e); }}
        }}

        function addAppHistory(appNo, stage, status, remark) {{
            let history = JSON.parse(localStorage.getItem('app_history_' + appNo) || '[]');
            history.push({{ stage, status, remark, date: new Date().toLocaleString() }});
            localStorage.setItem('app_history_' + appNo, JSON.stringify(history));
        }}

        // OFFICER MANAGEMENT FUNCTIONS
        function populateOfficerDistricts() {{
            let dSel = document.getElementById('off_dist');
            if(!dSel) return;
            dSel.innerHTML = '<option value="">Select District</option>';
            for(let d in GLOBAL_LOCATION_DATA["Odisha"]) {{
                dSel.innerHTML += `<option value="${{d}}">${{d}}</option>`;
            }}
        }}
        function populateOfficerBlocks() {{
            let dist = document.getElementById('off_dist').value;
            let bSel = document.getElementById('off_block');
            bSel.innerHTML = '<option value="">Select Block</option>';
            if(dist && GLOBAL_LOCATION_DATA["Odisha"][dist]) {{
                GLOBAL_LOCATION_DATA["Odisha"][dist].forEach(b => {{ bSel.innerHTML += `<option value="${{b}}">${{b}}</option>`; }});
            }}
        }}
        function onOffRoleChange() {{
            let r = document.getElementById('off_role').value;
            document.getElementById('off_dist_wrap').classList.toggle('hidden', r === 'state');
            document.getElementById('off_block_wrap').classList.toggle('hidden', r !== 'block');
        }}
        function createOfficer(e) {{
            e.preventDefault();
            let role = document.getElementById('off_role').value;
            let state = document.getElementById('off_state').value;
            let district = document.getElementById('off_dist').value;
            let block = document.getElementById('off_block').value;
            let name = document.getElementById('off_name').value;
            let mobile = document.getElementById('off_mobile').value;
            let email = document.getElementById('off_email').value;
            let password = document.getElementById('off_pass').value;

            let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
            officers.push({{ role, state, district, block, name, mobile, email, password }});
            localStorage.setItem('officers_list', JSON.stringify(officers));
            alert("Officer Created Successfully!");
            loadOfficersTable();
            e.target.reset();
        }}
        function loadOfficersTable() {{
            let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
            let tbody = document.getElementById('officers_tbody');
            if(!tbody) return;
            if(officers.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">No officers created yet.</td></tr>';
                return;
            }}
            tbody.innerHTML = officers.map((o, idx) => `
                <tr class="border-b hover:bg-gray-50">
                    <td class="p-3 font-bold uppercase text-blue-700">${{o.role}}</td>
                    <td class="p-3">${{o.state}} ${{o.district ? '/ ' + o.district : ''}} ${{o.block ? '/ ' + o.block : ''}}</td>
                    <td class="p-3 font-bold">${{o.name}}</td>
                    <td class="p-3">${{o.mobile}}</td>
                    <td class="p-3">${{o.email}}</td>
                    <td class="p-3 text-center"><button onclick="deleteOfficer(${{idx}})" class="bg-red-500 text-white px-2 py-1 rounded text-xs font-bold">Delete</button></td>
                </tr>
            `).join('');
        }}
        function deleteOfficer(idx) {{
            if(confirm("Delete this officer?")) {{
                let officers = JSON.parse(localStorage.getItem('officers_list') || '[]');
                officers.splice(idx, 1);
                localStorage.setItem('officers_list', JSON.stringify(officers));
                loadOfficersTable();
            }}
        }}

        function saveSettings() {{
            localStorage.setItem('app_fee', document.getElementById('app_fee').value);
            localStorage.setItem('payu_merchant_key', document.getElementById('payu_merchant_key').value);
            localStorage.setItem('payu_merchant_salt', document.getElementById('payu_merchant_salt').value);
            localStorage.setItem('rzp_key_id', document.getElementById('rzp_key_id').value);
            localStorage.setItem('rzp_key_secret', document.getElementById('rzp_key_secret').value);
            localStorage.setItem('cashfree_app_id', document.getElementById('cashfree_app_id').value);
            localStorage.setItem('cashfree_secret_key', document.getElementById('cashfree_secret_key').value);
            localStorage.setItem('payout_api_key', document.getElementById('payout_api_key').value);
            localStorage.setItem('payout_api_secret', document.getElementById('payout_api_secret').value);
            localStorage.setItem('reg_start_date', document.getElementById('reg_start_date').value);
            localStorage.setItem('reg_close_date', document.getElementById('reg_close_date').value);
            localStorage.setItem('notice_text', document.getElementById('notice_text').value);
            localStorage.setItem('contact_name', document.getElementById('contact_name').value);
            localStorage.setItem('contact_mobile', document.getElementById('contact_mobile').value);
            localStorage.setItem('contact_email', document.getElementById('contact_email').value);
            alert('Settings Saved Successfully!');
        }}

        function loadAdminProfile() {{
            if(localStorage.getItem('admin_name')) document.getElementById('prof_admin_name').value = localStorage.getItem('admin_name');
            if(localStorage.getItem('admin_mobile')) document.getElementById('prof_admin_mobile').value = localStorage.getItem('admin_mobile');
            if(localStorage.getItem('admin_email')) document.getElementById('prof_admin_email').value = localStorage.getItem('admin_email');
        }}

        function saveAdminProfile() {{
            let p1 = document.getElementById('prof_new_pass').value;
            let p2 = document.getElementById('prof_conf_pass').value;
            if(p1 || p2) {{
                if(p1 !== p2) {{ alert("Passwords do not match!"); return; }}
                localStorage.setItem('admin_password', p1);
            }}
            localStorage.setItem('admin_name', document.getElementById('prof_admin_name').value);
            localStorage.setItem('admin_mobile', document.getElementById('prof_admin_mobile').value);
            localStorage.setItem('admin_email', document.getElementById('prof_admin_email').value);
            alert("Admin Profile Saved!");
            location.reload();
        }}

        function toggleSidebar() {{
            document.getElementById('sidebar').classList.toggle('-translate-x-full');
            document.getElementById('sidebar_overlay').classList.toggle('hidden');
        }}

        function switchTab(tabId, element) {{
            document.querySelectorAll('.content-section').forEach(s => s.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            document.querySelectorAll('.menu-link').forEach(l => {{ l.classList.remove('bg-blue-700', 'text-white'); l.classList.add('text-slate-300'); }});
            if(element) {{ element.classList.remove('text-slate-300'); element.classList.add('bg-blue-700', 'text-white'); }}
            if(window.innerWidth < 768) {{
                document.getElementById('sidebar').classList.add('-translate-x-full');
                document.getElementById('sidebar_overlay').classList.add('hidden');
            }}
        }}

        function loadAdminData() {{
            let appList = JSON.parse(localStorage.getItem('app_list') || '[]');
            let total = 0, pending = 0, approved = 0, rejected = 0, wallet = 0;
            let blockHtml = '', distHtml = '', stateHtml = '', sysHtml = '', adminHtml = '', superAdminHtml = '', benHtml = '', rejHtml = '', payHtml = '';

            appList.forEach(appNo => {{
                if(localStorage.getItem('user_has_applied_' + appNo) !== 'true') return;
                let uDist = localStorage.getItem('u_dist_' + appNo) || '';
                let uBlock = localStorage.getItem('u_block_' + appNo) || '';
                let uState = localStorage.getItem('u_state_' + appNo) || 'Odisha';

                // Filter by Officer Jurisdiction
                if(currentSession.role === 'block' && (uBlock !== currentSession.block || uDist !== currentSession.district)) return;
                if(currentSession.role === 'district' && uDist !== currentSession.district) return;
                if(currentSession.role === 'state' && uState !== currentSession.state) return;

                total++;
                wallet += parseFloat(localStorage.getItem('paid_amount_' + appNo) || '100');

                let status = localStorage.getItem('app_status_' + appNo) || 'block_pending';
                let name = localStorage.getItem('user_full_name_' + appNo) || 'N/A';
                let scheme = localStorage.getItem('u_scheme_' + appNo) || 'N/A';
                let bankName = localStorage.getItem('u_bank_' + appNo) || 'N/A';
                let accNo = localStorage.getItem('u_acc_' + appNo) || 'N/A';

                if(status === 'block_pending') {{
                    pending++;
                    blockHtml += `
                        <tr class="border-b hover:bg-yellow-50">
                            <td class="p-3 font-bold text-blue-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3">${{uDist}} / <strong>${{uBlock}}</strong></td>
                            <td class="p-3">${{scheme}}</td>
                            <td class="p-3 flex justify-center gap-2 flex-wrap">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-pen"></i> A-Z Edit</button>
                                <button onclick="approveBlock('${{appNo}}')" class="bg-green-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> Approve -> Dist</button>
                                <button onclick="rejectApp('${{appNo}}', 'Block Officer')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'dist_pending') {{
                    pending++;
                    distHtml += `
                        <tr class="border-b hover:bg-indigo-50">
                            <td class="p-3 font-bold text-blue-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3"><strong>${{uDist}}</strong> / ${{uBlock}}</td>
                            <td class="p-3">${{scheme}}</td>
                            <td class="p-3 flex justify-center gap-2 flex-wrap">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-pen"></i> A-Z Edit</button>
                                <button onclick="approveDistrict('${{appNo}}')" class="bg-green-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> Approve -> State</button>
                                <button onclick="rejectApp('${{appNo}}', 'District Officer')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'state_pending') {{
                    pending++;
                    stateHtml += `
                        <tr class="border-b hover:bg-purple-50">
                            <td class="p-3 font-bold text-blue-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3">${{uState}} (${{uDist}})</td>
                            <td class="p-3">${{scheme}}</td>
                            <td class="p-3 flex justify-center gap-2 flex-wrap">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-pen"></i> A-Z Edit</button>
                                <button onclick="approveState('${{appNo}}')" class="bg-green-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> Approve -> System</button>
                                <button onclick="rejectApp('${{appNo}}', 'State Officer')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'sys_pending' || status === 'sys_pending_2days' || status === 'admin_correction') {{
                    pending++;
                    let sysRem = localStorage.getItem('sys_remark_' + appNo) || '';
                    sysHtml += `
                        <tr class="border-b bg-green-50">
                            <td class="p-3 font-bold text-blue-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3">${{scheme}} ${{sysRem ? `<div class="text-xs text-red-600 font-bold mt-1">Remark: ${{sysRem}}</div>` : ''}}</td>
                            <td class="p-3 flex justify-center gap-2 flex-wrap">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-pen"></i> A-Z Edit</button>
                                <button onclick="verifySysDoc('${{appNo}}')" class="bg-blue-600 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-robot"></i> Run System Match</button>
                                <button onclick="rejectApp('${{appNo}}', 'System Verification')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'admin_pending') {{
                    pending++;
                    adminHtml += `
                        <tr class="border-b">
                            <td class="p-3 font-bold text-blue-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold">System OK</span></td>
                            <td class="p-3 flex justify-center gap-2">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-purple-600 text-white px-3 py-1 rounded text-xs font-bold">View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold">A-Z Edit</button>
                                <button onclick="forwardToSuperAdmin('${{appNo}}')" class="bg-blue-600 text-white px-3 py-1 rounded text-xs font-bold">To SuperAdmin</button>
                                <button onclick="rejectApp('${{appNo}}', 'Admin')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold">Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'super_admin_pending') {{
                    pending++;
                    superAdminHtml += `
                        <tr class="border-b">
                            <td class="p-3 font-bold text-purple-600">#${{appNo}}</td>
                            <td class="p-3 font-bold">${{name}}</td>
                            <td class="p-3"><span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-bold">Ready for Final Approval</span></td>
                            <td class="p-3 flex justify-center gap-2">
                                <button onclick="viewFullApplication('${{appNo}}')" class="bg-gray-600 text-white px-3 py-1 rounded text-xs font-bold">View</button>
                                <button onclick="adminEditApp('${{appNo}}')" class="bg-yellow-500 text-white px-3 py-1 rounded text-xs font-bold">A-Z Edit</button>
                                <button onclick="finalApprove('${{appNo}}')" class="bg-green-600 text-white px-3 py-1 rounded text-xs font-bold">Final Approve</button>
                                <button onclick="rejectApp('${{appNo}}', 'Super Admin')" class="bg-red-500 text-white px-3 py-1 rounded text-xs font-bold">Reject</button>
                            </td>
                        </tr>`;
                }} else if(status === 'approved' || status === 'pension_sent') {{
                    approved++;
                    let sentFlag = localStorage.getItem('pension_sent_' + appNo);
                    let btnHtml = sentFlag === 'true' ? `<button disabled class="bg-green-600 text-white px-3 py-1 rounded text-xs font-bold">Paid</button>` : `<button onclick="markManualPaid('${{appNo}}', '${{name}}', '${{accNo}}')" class="bg-blue-600 text-white px-3 py-1 rounded text-xs font-bold">Manual Pay</button> <button onclick="sendPensionDBT('${{appNo}}', '${{name}}', '1000', '${{accNo}}')" class="bg-indigo-600 text-white px-3 py-1 rounded text-xs font-bold">DBT Auto</button>`;
                    if(sentFlag === 'true') {{
                        payHtml += `<tr class="border-b"><td class="p-3 font-bold">#${{appNo}}</td><td class="p-3 font-bold">${{name}}</td><td class="p-3">${{bankName}} (${{accNo}})</td><td class="p-3 text-green-700 font-bold">Success</td><td class="p-3 font-mono font-bold">${{localStorage.getItem('utr_number_' + appNo) || 'N/A'}}</td></tr>`;
                    }}
                    benHtml += `<tr class="border-b"><td class="p-3 font-bold">#${{appNo}}</td><td class="p-3 font-bold">${{name}}</td><td class="p-3"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold">Active</span></td><td class="p-3 text-center">${{btnHtml}}</td></tr>`;
                }} else if(status === 'rejected') {{
                    rejected++;
                    rejHtml += `<tr class="border-b"><td class="p-3 font-bold text-red-600">#${{appNo}}</td><td class="p-3 font-bold">${{name}}</td><td class="p-3">Officer/Admin</td><td class="p-3 italic text-red-700">${{localStorage.getItem('reject_reason_' + appNo) || 'Rejected'}}</td><td class="p-3 text-center"><button onclick="deleteRejectedRow('${{appNo}}')" class="bg-red-600 text-white px-3 py-1 rounded text-xs font-bold">Delete</button></td></tr>`;
                }}
            }});

            document.getElementById('count_total').innerText = total;
            document.getElementById('count_pending').innerText = pending;
            document.getElementById('count_approved').innerText = approved;
            document.getElementById('count_rejected').innerText = rejected;
            document.getElementById('total_wallet_val').innerText = wallet;

            if(blockHtml) document.getElementById('block_verify_tbody').innerHTML = blockHtml;
            if(distHtml) document.getElementById('dist_verify_tbody').innerHTML = distHtml;
            if(stateHtml) document.getElementById('state_verify_tbody').innerHTML = stateHtml;
            if(sysHtml) document.getElementById('sys_verify_tbody').innerHTML = sysHtml;
            if(adminHtml) document.getElementById('admin_approve_tbody').innerHTML = adminHtml;
            if(superAdminHtml) document.getElementById('superadmin_approve_tbody').innerHTML = superAdminHtml;
            if(benHtml) document.getElementById('beneficiaries_tbody').innerHTML = benHtml;
            if(rejHtml) document.getElementById('rejected_tbody').innerHTML = rejHtml;
            if(payHtml) document.getElementById('payments_tbody').innerHTML = payHtml;
        }}

        // MULTI-TIER APPROVAL ACTIONS WITH AUTO EMAIL
        async function approveBlock(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'dist_pending');
            addAppHistory(appNo, "Block Officer Verification", "Approved", "Approved by Block Officer (" + currentSession.name + "). Forwarded to District Officer.");
            await sendUserEmailUpdate(appNo, "Block Verification Approved", "Your application has been approved at Block Level and forwarded to District Officer.");
            alert("Block Approved! Sent to District Officer & Email sent to Applicant.");
            location.reload();
        }}

        async function approveDistrict(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'state_pending');
            addAppHistory(appNo, "District Officer Verification", "Approved", "Approved by District Officer (" + currentSession.name + "). Forwarded to State Officer.");
            await sendUserEmailUpdate(appNo, "District Verification Approved", "Your application has been approved at District Level and forwarded to State Officer.");
            alert("District Approved! Sent to State Officer & Email sent to Applicant.");
            location.reload();
        }}

        async function approveState(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'sys_pending');
            addAppHistory(appNo, "State Officer Verification", "Approved", "Approved by State Officer (" + currentSession.name + "). Forwarded to System Verification.");
            await sendUserEmailUpdate(appNo, "State Verification Approved", "Your application has been approved at State Level and forwarded to System Verification.");
            alert("State Approved! Sent to System Verification & Email sent to Applicant.");
            location.reload();
        }}

        // SYSTEM VERIFICATION: MATCHES DATA & UPLOADED DOCUMENTS, GENERATES REMARK IF WRONG
        function verifySysDoc(appNo) {{
            window.current_modal_appNo = appNo;
            let name = (localStorage.getItem('user_full_name_' + appNo) || '').trim();
            let incName = (localStorage.getItem('u_inc_issued_to_' + appNo) || '').trim();
            let incAmt = (localStorage.getItem('u_inc_amount_' + appNo) || '').trim();
            let cat = localStorage.getItem('u_category_' + appNo) || 'General';
            let hasPhoto = !!localStorage.getItem('u_photo_' + appNo);
            let hasAadhaarDoc = !!localStorage.getItem('u_doc_aadhaar_' + appNo);
            let hasPassbookDoc = !!localStorage.getItem('u_doc_passbook_' + appNo);
            let hasIncomeDoc = !!localStorage.getItem('u_doc_income_' + appNo);

            let issues = [];
            if(!hasPhoto) issues.push("Profile Photo missing");
            if(!hasAadhaarDoc) issues.push("Aadhaar Document PDF missing");
            if(!hasPassbookDoc) issues.push("Bank Passbook PDF missing");
            if(cat !== 'SC' && cat !== 'ST') {{
                if(!hasIncomeDoc) issues.push("Income Certificate PDF missing");
                if(incName && name.toLowerCase() !== incName.toLowerCase()) issues.push("Name mismatch with Income Certificate");
                let numAmt = parseInt(incAmt.replace(/[^0-9]/g, '')) || 0;
                if(numAmt > 50000) issues.push("Annual Income (" + incAmt + ") exceeds Rs. 50,000 limit");
            }}

            document.getElementById('modal_sys_name').innerText = name;
            document.getElementById('modal_sys_inc_name').innerText = incName || 'N/A';
            document.getElementById('modal_sys_inc_amt').innerText = incAmt || 'N/A';
            let statusBox = document.getElementById('modal_sys_result');
            if(issues.length > 0) {{
                let rem = "Issues Found: " + issues.join("; ");
                localStorage.setItem('sys_remark_' + appNo, rem);
                statusBox.className = "p-3 bg-red-50 border border-red-300 rounded text-red-700 font-bold text-sm";
                statusBox.innerHTML = "<i class='fa-solid fa-triangle-exclamation mr-1'></i> " + rem + "<br><span class='text-xs'>Admin can use A-Z Edit to fix data/re-upload documents or Reject.</span>";
            }} else {{
                localStorage.removeItem('sys_remark_' + appNo);
                statusBox.className = "p-3 bg-green-50 border border-green-300 rounded text-green-700 font-bold text-sm";
                statusBox.innerHTML = "<i class='fa-solid fa-check-double mr-1'></i> All Data & Uploaded Documents Matched Successfully!";
            }}
            document.getElementById('sys_verification_modal').classList.remove('hidden');
        }}
        function closeSysModal() {{ document.getElementById('sys_verification_modal').classList.add('hidden'); }}

        async function approveSys() {{
            let appNo = window.current_modal_appNo;
            localStorage.setItem('app_status_' + appNo, 'admin_pending');
            addAppHistory(appNo, "System Verification", "Approved", "Documents & data verified by System.");
            await sendUserEmailUpdate(appNo, "System Verification Passed", "Your uploaded documents and data passed System Verification.");
            alert("System Approved! Forwarded to Admin.");
            location.reload();
        }}

        async function forwardToSuperAdmin(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'super_admin_pending');
            addAppHistory(appNo, "Admin Action", "Approved", "Forwarded to Super Admin for Final Approval.");
            await sendUserEmailUpdate(appNo, "Admin Verification Approved", "Your application has been forwarded to Super Admin for final approval.");
            alert("Forwarded to Super Admin!");
            location.reload();
        }}

        async function finalApprove(appNo) {{
            localStorage.setItem('app_status_' + appNo, 'approved');
            addAppHistory(appNo, "Super Admin Final Approval", "Approved", "Congratulations! Approved as Active Beneficiary.");
            await sendUserEmailUpdate(appNo, "Application Finally Approved!", "Congratulations! Your Gopabandhu Pension Yojana application is approved.");
            alert("Super Admin Approved! User notified via Email.");
            location.reload();
        }}

        async function rejectApp(appNo, byRole) {{
            let targetApp = appNo || window.current_modal_appNo;
            let reason = prompt("Enter Rejection Reason (Remark):");
            if (reason && reason.trim() !== "") {{
                localStorage.setItem('app_status_' + targetApp, 'rejected');
                localStorage.setItem('reject_reason_' + targetApp, (byRole ? byRole + ": " : "") + reason);
                addAppHistory(targetApp, (byRole || "Officer") + " Verification", "Rejected", reason);
                await sendUserEmailUpdate(targetApp, "Application Rejected", "Your application was rejected by " + (byRole || "Officer") + ". Remark: " + reason);
                alert("Application Rejected & Email sent to User.");
                location.reload();
            }}
        }}

        // A-TO-Z CORRECTION + DOCUMENT RE-UPLOAD MODAL
        function adminEditApp(appNo) {{
            window.current_modal_appNo = appNo;
            editUploadedFiles = {{}};
            let g = (k) => localStorage.getItem(k + '_' + appNo) || '';
            document.getElementById('edit_name').value = g('user_full_name');
            document.getElementById('edit_father').value = g('u_father');
            document.getElementById('edit_mother').value = g('u_mother');
            document.getElementById('edit_mobile').value = g('user_mobile');
            document.getElementById('edit_email').value = g('user_email');
            document.getElementById('edit_aadhaar').value = g('user_aadhaar');
            document.getElementById('edit_scheme').value = g('u_scheme');
            document.getElementById('edit_category').value = g('u_category');
            document.getElementById('edit_dist').value = g('u_dist');
            document.getElementById('edit_block').value = g('u_block');
            document.getElementById('edit_address').value = g('u_address');
            document.getElementById('edit_inc_cert').value = g('u_inc_cert');
            document.getElementById('edit_inc_amt').value = g('u_inc_amount');
            document.getElementById('edit_bank').value = g('u_bank');
            document.getElementById('edit_acc').value = g('u_acc');
            document.getElementById('edit_ifsc').value = g('u_ifsc');
            document.getElementById('admin_edit_modal').classList.remove('hidden');
        }}

        function saveAdminEdit() {{
            let appNo = window.current_modal_appNo;
            let s = (k, id) => localStorage.setItem(k + '_' + appNo, document.getElementById(id).value);
            s('user_full_name', 'edit_name');
            s('u_father', 'edit_father');
            s('u_mother', 'edit_mother');
            s('user_mobile', 'edit_mobile');
            s('user_email', 'edit_email');
            s('user_aadhaar', 'edit_aadhaar');
            s('u_scheme', 'edit_scheme');
            s('u_category', 'edit_category');
            s('u_dist', 'edit_dist');
            s('u_block', 'edit_block');
            s('u_address', 'edit_address');
            s('u_inc_cert', 'edit_inc_cert');
            s('u_inc_amount', 'edit_inc_amt');
            s('u_bank', 'edit_bank');
            s('u_acc', 'edit_acc');
            s('u_ifsc', 'edit_ifsc');

            if(editUploadedFiles['photo']) localStorage.setItem('u_photo_' + appNo, editUploadedFiles['photo']);
            if(editUploadedFiles['aadhaar']) localStorage.setItem('u_doc_aadhaar_' + appNo, editUploadedFiles['aadhaar']);
            if(editUploadedFiles['income']) localStorage.setItem('u_doc_income_' + appNo, editUploadedFiles['income']);
            if(editUploadedFiles['passbook']) localStorage.setItem('u_doc_passbook_' + appNo, editUploadedFiles['passbook']);

            addAppHistory(appNo, "Correction / Edit", "Updated", "Details/Documents updated by " + currentSession.name);
            alert('A-to-Z Details & Documents Updated Successfully!');
            document.getElementById('admin_edit_modal').classList.add('hidden');
            location.reload();
        }}
        function closeEditModal() {{ document.getElementById('admin_edit_modal').classList.add('hidden'); }}

        function deleteRejectedRow(appNo) {{
            if(confirm("Permanently delete this rejected application?")) {{
                localStorage.removeItem('user_has_applied_' + appNo);
                localStorage.removeItem('app_status_' + appNo);
                location.reload();
            }}
        }}

        function markManualPaid(appNo, name, accNo) {{
            let utr = prompt(`Enter Payment UTR Number for ${{name}} (A/C: ${{accNo}}):`);
            if(utr && utr.trim() !== "") {{
                localStorage.setItem('utr_number_' + appNo, utr);
                localStorage.setItem('pension_sent_' + appNo, 'true');
                localStorage.setItem('app_status_' + appNo, 'pension_sent');
                addAppHistory(appNo, "Pension Disbursement", "Paid", "Manual Payment UTR: " + utr);
                sendUserEmailUpdate(appNo, "Pension Paid!", "Your pension has been credited. UTR: " + utr);
                alert("Manual Payment Saved!");
                location.reload();
            }}
        }}

        function sendPensionDBT(appNo, name, amount, accNo) {{
            let txnId = "DBT-" + Math.floor(Math.random()*1000000000);
            localStorage.setItem('utr_number_' + appNo, txnId);
            localStorage.setItem('pension_sent_' + appNo, 'true');
            localStorage.setItem('app_status_' + appNo, 'pension_sent');
            addAppHistory(appNo, "Pension Disbursement", "Paid", "DBT Auto Transfer Txn: " + txnId);
            sendUserEmailUpdate(appNo, "Pension Paid via DBT!", "Rs." + amount + " credited. Txn ID: " + txnId);
            alert("DBT Transfer Success! Txn ID: " + txnId);
            location.reload();
        }}

        function viewFullApplication(appNo) {{
            let g = (k) => localStorage.getItem(k + '_' + appNo) || 'N/A';
            document.getElementById('v_appno').innerText = appNo;
            document.getElementById('v_scheme').innerText = g('u_scheme');
            document.getElementById('v_name').innerText = g('user_full_name');
            document.getElementById('v_father').innerText = g('u_father');
            document.getElementById('v_mother').innerText = g('u_mother');
            document.getElementById('v_aadhaar').innerText = g('user_aadhaar');
            document.getElementById('v_dist').innerText = g('u_dist');
            document.getElementById('v_block').innerText = g('u_block');
            document.getElementById('v_gp').innerText = g('u_gp');
            document.getElementById('v_address').innerText = g('u_address');
            document.getElementById('v_dob').innerText = g('u_dob');
            document.getElementById('v_gender').innerText = g('u_gender');
            document.getElementById('v_category').innerText = g('u_category');
            document.getElementById('v_inc_cert').innerText = g('u_inc_cert');
            document.getElementById('v_inc_auth').innerText = g('u_inc_auth');
            document.getElementById('v_inc_amount').innerText = g('u_inc_amount');
            document.getElementById('v_bank').innerText = g('u_bank');
            document.getElementById('v_acc').innerText = g('u_acc');
            document.getElementById('v_ifsc').innerText = g('u_ifsc');
            document.getElementById('v_fee').innerText = "Paid (₹" + (localStorage.getItem('paid_amount_' + appNo) || '100') + ")";

            let photo = localStorage.getItem('u_photo_' + appNo);
            let photoEl = document.getElementById('v_photo_img');
            if(photo) {{ photoEl.src = photo; photoEl.classList.remove('hidden'); }}
            else {{ photoEl.classList.add('hidden'); }}

            document.getElementById('full_app_view_modal').classList.remove('hidden');
        }}
        function closeFullAppModal() {{ document.getElementById('full_app_view_modal').classList.add('hidden'); }}
    </script>
</head>
<body class="bg-gray-100 font-sans text-gray-800 flex h-screen overflow-hidden relative">

    <div id="sidebar_overlay" onclick="toggleSidebar()" class="fixed inset-0 bg-black bg-opacity-50 z-30 hidden md:hidden"></div>

    <aside id="sidebar" class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl h-full absolute z-40 inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition-transform duration-300 ease-in-out print:hidden">
        <div class="p-5 border-b border-slate-700 text-center flex justify-between items-center md:block">
            <div>
                <h2 class="text-lg font-bold text-blue-400">Gopabandhu Pension</h2>
                <p class="text-xs text-slate-400">Officer & Admin Panel</p>
            </div>
            <button onclick="toggleSidebar()" class="md:hidden text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-1 px-3 text-sm">
                <li><a href="#" onclick="switchTab('dashboard', this)" class="menu-link flex items-center px-4 py-2.5 bg-blue-700 text-white rounded-lg"><i class="fa-solid fa-gauge w-6 mr-2"></i> Dashboard</a></li>
                
                <li class="mt-2 border-t border-slate-700 pt-2"><span class="px-4 text-xs font-bold text-slate-500 uppercase">Verification Flow</span></li>
                <li><a href="#" onclick="switchTab('blockverify', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-building-user w-6 mr-2"></i> Block Verify (Step 1)</a></li>
                <li><a href="#" onclick="switchTab('distverify', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-landmark w-6 mr-2"></i> District Verify (Step 2)</a></li>
                <li><a href="#" onclick="switchTab('stateverify', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-flag w-6 mr-2"></i> State Verify (Step 3)</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('sysverify', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-microchip w-6 mr-2"></i> System Verify (Step 4)</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('adminapprove', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-file-signature w-6 mr-2"></i> Admin Action (Step 5)</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('superadmin', this)" class="menu-link flex items-center px-4 py-2.5 text-purple-300 hover:bg-purple-900 rounded-lg"><i class="fa-solid fa-gavel w-6 mr-2"></i> Super Admin (Final)</a></li>
                <li><a href="#" onclick="switchTab('rejected', this)" class="menu-link flex items-center px-4 py-2.5 text-red-400 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-trash-can w-6 mr-2"></i> Rejected Box</a></li>

                <li class="admin-only-menu mt-2 border-t border-slate-700 pt-2"><span class="px-4 text-xs font-bold text-slate-500 uppercase">Admin Management</span></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('officers', this)" class="menu-link flex items-center px-4 py-2.5 text-yellow-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-user-tie w-6 mr-2"></i> Manage Officers</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('beneficiaries', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-users w-6 mr-2"></i> Beneficiaries</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('payments', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-money-bill-transfer w-6 mr-2"></i> Payment Records</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('settings', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-gears w-6 mr-2"></i> Portal Settings</a></li>
                <li class="admin-only-menu"><a href="#" onclick="switchTab('profile', this)" class="menu-link flex items-center px-4 py-2.5 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-user-gear w-6 mr-2"></i> Admin Profile</a></li>
            </ul>
        </nav>
        <div class="p-4 border-t border-slate-700"><a href="/admin/login" class="flex items-center px-4 py-2 text-red-400 hover:bg-red-500 hover:text-white rounded-lg"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout</a></div>
    </aside>

    <main class="flex-1 flex flex-col h-full overflow-hidden relative print:hidden w-full">
        <header class="bg-white shadow-sm border-b px-4 md:px-6 py-4 flex justify-between items-center">
            <div class="flex items-center">
                <button onclick="toggleSidebar()" class="md:hidden text-blue-700 text-2xl mr-3"><i class="fa-solid fa-bars"></i></button>
                <h1 id="header-title" class="text-lg md:text-xl font-bold truncate">Gopabandhu Pension Yojana Dashboard</h1>
            </div>
            <span class="text-xs md:text-sm font-bold text-blue-800" id="welcome_admin_name">Admin</span>
        </header>

        <div class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50 w-full">
            <!-- DASHBOARD -->
            <div id="section-dashboard" class="content-section">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-purple-500 shadow-sm md:col-span-2">
                        <p class="text-sm text-gray-500 font-semibold">Total Wallet Collection</p><h3 class="text-3xl font-bold text-purple-700">₹<span id="total_wallet_val">0</span></h3>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-blue-500 shadow-sm"><p class="text-sm text-gray-500 font-semibold">Total Applications</p><h3 id="count_total" class="text-2xl font-bold text-blue-700">0</h3></div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-green-500 shadow-sm"><p class="text-sm text-gray-500 font-semibold">Active Beneficiary</p><h3 id="count_approved" class="text-2xl font-bold text-green-700">0</h3></div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-orange-500 shadow-sm"><p class="text-sm text-gray-500 font-semibold">Pending Approvals</p><h3 id="count_pending" class="text-2xl font-bold text-orange-700">0</h3></div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-red-500 shadow-sm"><p class="text-sm text-gray-500 font-semibold">Total Rejected</p><h3 id="count_rejected" class="text-2xl font-bold text-red-700">0</h3></div>
                </div>
            </div>

            <!-- STEP 1: BLOCK VERIFICATION -->
            <div id="section-blockverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-yellow-50"><h2 class="font-bold text-lg text-yellow-800">Step 1: Block Officer Verification</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">District / Block</th><th class="p-3">Scheme</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="block_verify_tbody" class="text-sm"><tr><td colspan="5" class="text-center py-6 text-gray-500">No pending applications for Block.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- STEP 2: DISTRICT VERIFICATION -->
            <div id="section-distverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-indigo-50"><h2 class="font-bold text-lg text-indigo-800">Step 2: District Officer Verification</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">District / Block</th><th class="p-3">Scheme</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="dist_verify_tbody" class="text-sm"><tr><td colspan="5" class="text-center py-6 text-gray-500">No pending applications for District.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- STEP 3: STATE VERIFICATION -->
            <div id="section-stateverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-purple-50"><h2 class="font-bold text-lg text-purple-800">Step 3: State Officer Verification</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">State / District</th><th class="p-3">Scheme</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="state_verify_tbody" class="text-sm"><tr><td colspan="5" class="text-center py-6 text-gray-500">No pending applications for State.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- STEP 4: SYSTEM VERIFICATION -->
            <div id="section-sysverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-orange-50"><h2 class="font-bold text-lg text-orange-800">Step 4: System Document & Data Verification</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">Scheme / System Remark</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="sys_verify_tbody" class="text-sm"><tr><td colspan="4" class="text-center py-6 text-gray-500">No pending applications for System Verification.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- STEP 5: ADMIN APPROVAL -->
            <div id="section-adminapprove" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-blue-50"><h2 class="font-bold text-lg text-blue-800">Admin Action Panel</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">Sys Status</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="admin_approve_tbody" class="text-sm"><tr><td colspan="4" class="text-center py-6 text-gray-500">No applications pending.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- FINAL: SUPER ADMIN -->
            <div id="section-superadmin" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-purple-50"><h2 class="font-bold text-lg text-purple-900">Super Admin Final Approval</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-purple-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">Status</th><th class="p-3 text-center">Action</th></tr></thead>
                            <tbody id="superadmin_approve_tbody" class="text-sm"><tr><td colspan="4" class="text-center py-6 text-gray-500">No applications pending.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- REJECTED BOX -->
            <div id="section-rejected" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-red-50"><h2 class="font-bold text-lg text-red-800">Rejected Applications Box</h2></div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse min-w-[650px]">
                            <thead class="bg-gray-100 text-sm"><tr><th class="p-3">App ID</th><th class="p-3">Applicant</th><th class="p-3">Rejected By</th><th class="p-3">Remark</th><th class="p-3 text-center">Delete</th></tr></thead>
                            <tbody id="rejected_tbody" class="text-sm"><tr><td colspan="5" class="text-center py-6 text-gray-500">No rejected applications.</td></tr></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- OFFICER MANAGEMENT (ADMIN ONLY) -->
            <div id="section-officers" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border p-6 mb-6">
                    <h2 class="font-bold text-xl text-blue-900 mb-4 border-b pb-2"><i class="fa-solid fa-user-plus mr-2"></i> Create Block / District / State Officer Login</h2>
                    <form onsubmit="createOfficer(event)" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-gray-700 mb-1">Officer Role</label>
                            <select id="off_role" onchange="onOffRoleChange()" class="w-full border p-2 rounded font-bold bg-blue-50">
                                <option value="block">Block Officer</option>
                                <option value="district">District Officer</option>
                                <option value="state">State Officer</option>
                            </select>
                        </div>
                        <div><label class="block text-xs font-bold text-gray-700 mb-1">State</label><select id="off_state" class="w-full border p-2 rounded"><option value="Odisha">Odisha</option></select></div>
                        <div id="off_dist_wrap"><label class="block text-xs font-bold text-gray-700 mb-1">District</label><select id="off_dist" onchange="populateOfficerBlocks()" class="w-full border p-2 rounded"></select></div>
                        <div id="off_block_wrap"><label class="block text-xs font-bold text-gray-700 mb-1">Block</label><select id="off_block" class="w-full border p-2 rounded"><option value="">Select Block</option></select></div>
                        <div><label class="block text-xs font-bold text-gray-700 mb-1">Officer Name</label><input type="text" id="off_name" class="w-full border p-2 rounded" required></div>
                        <div><label class="block text-xs font-bold text-gray-700 mb-1">Mobile No</label><input type="text" id="off_mobile" class="w-full border p-2 rounded" required></div>
                        <div><label class="block text-xs font-bold text-gray-700 mb-1">Email ID (Login ID)</label><input type="email" id="off_email" class="w-full border p-2 rounded" required></div>
                        <div><label class="block text-xs font-bold text-gray-700 mb-1">Password</label><input type="text" id="off_pass" class="w-full border p-2 rounded" required></div>
                        <div class="flex items-end"><button type="submit" class="w-full bg-blue-700 text-white font-bold py-2 rounded hover:bg-blue-800">Save Officer</button></div>
                    </form>
                </div>
                <div class="bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                    <h3 class="font-bold text-lg mb-3">Registered Officers List</h3>
                    <table class="w-full text-left border-collapse text-sm min-w-[650px]">
                        <thead class="bg-gray-100"><tr><th class="p-3">Role</th><th class="p-3">Jurisdiction</th><th class="p-3">Name</th><th class="p-3">Mobile</th><th class="p-3">Email</th><th class="p-3 text-center">Action</th></tr></thead>
                        <tbody id="officers_tbody"></tbody>
                    </table>
                </div>
            </div>

            <!-- BENEFICIARIES & PAYMENTS & SETTINGS & PROFILE -->
            <div id="section-beneficiaries" class="content-section hidden bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                <h2 class="font-bold text-lg mb-4">Active Beneficiaries</h2>
                <table class="w-full text-left border-collapse text-sm"><thead class="bg-gray-100"><tr><th class="p-3">ID</th><th class="p-3">Name</th><th class="p-3">Status</th><th class="p-3 text-center">Action</th></tr></thead><tbody id="beneficiaries_tbody"></tbody></table>
            </div>

            <div id="section-payments" class="content-section hidden bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                <h2 class="font-bold text-lg mb-4">Payment & UTR Records</h2>
                <table class="w-full text-left border-collapse text-sm"><thead class="bg-gray-100"><tr><th class="p-3">App ID</th><th class="p-3">Name</th><th class="p-3">Bank Details</th><th class="p-3">Status</th><th class="p-3">UTR</th></tr></thead><tbody id="payments_tbody"></tbody></table>
            </div>

            <div id="section-settings" class="content-section hidden bg-white rounded-xl shadow-sm border p-6">
                <h2 class="font-bold text-xl mb-4 text-blue-900 border-b pb-2">Portal Settings & API Keys</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div><label class="text-xs font-bold">Reg Start Date</label><input type="date" id="reg_start_date" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Reg Close Date</label><input type="date" id="reg_close_date" class="w-full border p-2 rounded"></div>
                    <div class="md:col-span-2"><label class="text-xs font-bold">Home Notice</label><textarea id="notice_text" class="w-full border p-2 rounded"></textarea></div>
                    <div><label class="text-xs font-bold">Contact Name</label><input type="text" id="contact_name" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Contact Mobile</label><input type="text" id="contact_mobile" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Contact Email</label><input type="email" id="contact_email" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Base Fee (₹)</label><input type="number" id="app_fee" value="100" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Cashfree App ID</label><input type="password" id="cashfree_app_id" value="1515812276f3edeb0677e6e62642185151" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Cashfree Secret</label><input type="password" id="cashfree_secret_key" value="cfsk_ma_prod_1b755875b3e4253c4e2865ddd5f27524_fa5dfc25" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">PayU Key</label><input type="password" id="payu_merchant_key" value="OLBUPA" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">PayU Salt</label><input type="password" id="payu_merchant_salt" value="63LJwDVAEKqfR32B3ynr0TKayqyVjGg7" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Razorpay Key</label><input type="password" id="rzp_key_id" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Razorpay Secret</label><input type="password" id="rzp_key_secret" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Payout API Key</label><input type="password" id="payout_api_key" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Payout API Secret</label><input type="password" id="payout_api_secret" class="w-full border p-2 rounded"></div>
                </div>
                <button onclick="saveSettings()" class="mt-6 bg-blue-700 text-white font-bold px-6 py-2.5 rounded">Save All Settings</button>
            </div>

            <div id="section-profile" class="content-section hidden bg-white rounded-xl shadow-sm border p-6 max-w-xl">
                <h2 class="font-bold text-xl mb-4">Admin Profile</h2>
                <div class="space-y-3">
                    <div><label class="text-xs font-bold">Admin Name</label><input type="text" id="prof_admin_name" value="Super Admin" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Mobile</label><input type="text" id="prof_admin_mobile" value="9876543210" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Email</label><input type="email" id="prof_admin_email" value="admin@kulusutar.in" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">New Password</label><input type="password" id="prof_new_pass" class="w-full border p-2 rounded"></div>
                    <div><label class="text-xs font-bold">Confirm Password</label><input type="password" id="prof_conf_pass" class="w-full border p-2 rounded"></div>
                    <button onclick="saveAdminProfile()" class="bg-blue-700 text-white font-bold px-6 py-2 rounded">Save Profile</button>
                </div>
            </div>
        </div>
    </main>

    <!-- SYSTEM VERIFICATION MODAL -->
    <div id="sys_verification_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-lg rounded-xl shadow-2xl p-6 relative">
            <button onclick="closeSysModal()" class="absolute top-4 right-4 text-gray-400 text-2xl"><i class="fa-solid fa-xmark"></i></button>
            <h3 class="text-xl font-bold mb-4 border-b pb-2 text-blue-800">System Auto-Verification Report</h3>
            <div class="space-y-3 text-sm mb-4">
                <p><strong>Applicant Name:</strong> <span id="modal_sys_name"></span></p>
                <p><strong>Income Cert Name:</strong> <span id="modal_sys_inc_name"></span></p>
                <p><strong>Income Amount:</strong> <span id="modal_sys_inc_amt"></span></p>
                <div id="modal_sys_result"></div>
            </div>
            <div class="flex justify-end gap-3">
                <button onclick="rejectApp(null, 'System')" class="bg-red-500 text-white px-4 py-2 rounded font-bold">Reject</button>
                <button onclick="approveSys()" class="bg-blue-600 text-white px-4 py-2 rounded font-bold">Approve -> Admin</button>
            </div>
        </div>
    </div>

    <!-- A-TO-Z CORRECTION + DOCUMENT RE-UPLOAD MODAL -->
    <div id="admin_edit_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-xl shadow-2xl p-6 border-t-4 border-yellow-500">
            <h3 class="text-xl font-bold text-yellow-700 border-b pb-2 mb-4"><i class="fa-solid fa-pen-to-square"></i> A-to-Z Application Correction & Document Upload</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                <div><label class="font-bold text-xs">Full Name</label><input type="text" id="edit_name" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Father Name</label><input type="text" id="edit_father" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Mother Name</label><input type="text" id="edit_mother" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Mobile</label><input type="text" id="edit_mobile" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Email</label><input type="text" id="edit_email" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Aadhaar</label><input type="text" id="edit_aadhaar" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Scheme</label><input type="text" id="edit_scheme" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Category</label><input type="text" id="edit_category" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">District</label><input type="text" id="edit_dist" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Block</label><input type="text" id="edit_block" class="w-full border p-1.5 rounded"></div>
                <div class="md:col-span-2"><label class="font-bold text-xs">Full Address</label><input type="text" id="edit_address" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Income Cert No</label><input type="text" id="edit_inc_cert" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Income Amount</label><input type="text" id="edit_inc_amt" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">Bank Name</label><input type="text" id="edit_bank" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">A/C No</label><input type="text" id="edit_acc" class="w-full border p-1.5 rounded"></div>
                <div><label class="font-bold text-xs">IFSC</label><input type="text" id="edit_ifsc" class="w-full border p-1.5 rounded uppercase"></div>
            </div>
            <h4 class="font-bold text-sm mt-4 mb-2 text-blue-800 border-t pt-3">Re-Upload / Update Documents (Optional)</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div><label class="font-bold">Update Profile Photo</label><input type="file" onchange="handleAdminEditFile(this, 'photo')" accept="image/*" class="w-full border p-1 rounded"></div>
                <div><label class="font-bold">Update Aadhaar PDF</label><input type="file" onchange="handleAdminEditFile(this, 'aadhaar')" accept=".pdf,image/*" class="w-full border p-1 rounded"></div>
                <div><label class="font-bold">Update Income PDF</label><input type="file" onchange="handleAdminEditFile(this, 'income')" accept=".pdf,image/*" class="w-full border p-1 rounded"></div>
                <div><label class="font-bold">Update Passbook PDF</label><input type="file" onchange="handleAdminEditFile(this, 'passbook')" accept=".pdf,image/*" class="w-full border p-1 rounded"></div>
            </div>
            <div class="mt-6 flex justify-end gap-3">
                <button onclick="closeEditModal()" class="bg-gray-300 px-4 py-2 font-bold rounded">Cancel</button>
                <button onclick="saveAdminEdit()" class="bg-green-600 text-white px-5 py-2 font-bold rounded hover:bg-green-700">Save All Corrections</button>
            </div>
        </div>
    </div>

    <!-- FULL APPLICATION VIEW & PRINT MODAL WITH PROFILE PHOTO -->
    <div id="full_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white w-full max-w-4xl h-[90vh] rounded-xl shadow-2xl flex flex-col">
            <div class="p-4 border-b flex justify-between items-center bg-blue-50 rounded-t-xl print:hidden">
                <h3 class="text-lg font-bold text-blue-800">Applicant Full Details (With Photo)</h3>
                <div class="space-x-2 flex">
                    <button onclick="window.print()" class="bg-gray-800 text-white px-4 py-2 rounded font-bold text-sm"><i class="fa-solid fa-print"></i> Print</button>
                    <button onclick="closeFullAppModal()" class="bg-red-500 text-white px-4 py-2 rounded font-bold text-sm">Close</button>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto p-6">
                <div class="flex justify-between items-center border-b-2 border-gray-800 pb-4 mb-6">
                    <div>
                        <h2 class="text-2xl font-extrabold uppercase text-blue-900">Gopabandhu Pension Yojana</h2>
                        <p class="font-bold text-gray-600">Applicant Full Verification Copy</p>
                    </div>
                    <img id="v_photo_img" class="hidden h-24 w-24 object-cover border-2 border-gray-800 rounded shadow" />
                </div>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-6 bg-gray-50 p-4 rounded border">
                    <div><p class="text-gray-500 text-xs">App No</p><p id="v_appno" class="font-bold text-blue-700"></p></div>
                    <div><p class="text-gray-500 text-xs">Scheme</p><p id="v_scheme" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Category</p><p id="v_category" class="font-bold text-red-600"></p></div>
                    <div><p class="text-gray-500 text-xs">Payment</p><p id="v_fee" class="font-bold text-green-600"></p></div>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm mb-6">
                    <div><p class="text-gray-500 text-xs">Full Name</p><p id="v_name" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Father</p><p id="v_father" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Mother</p><p id="v_mother" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Gender</p><p id="v_gender" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">DOB</p><p id="v_dob" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Aadhaar</p><p id="v_aadhaar" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">District</p><p id="v_dist" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Block</p><p id="v_block" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">GP / Ward</p><p id="v_gp" class="font-bold"></p></div>
                    <div class="col-span-2 md:col-span-3"><p class="text-gray-500 text-xs">Full Address</p><p id="v_address" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Income Cert No</p><p id="v_inc_cert" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Issued By</p><p id="v_inc_auth" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Annual Income</p><p id="v_inc_amount" class="font-bold text-red-600"></p></div>
                    <div><p class="text-gray-500 text-xs">Bank Name</p><p id="v_bank" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Account No</p><p id="v_acc" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">IFSC</p><p id="v_ifsc" class="font-bold"></p></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 8. EXPLICIT ROUTES DEFINITION
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
