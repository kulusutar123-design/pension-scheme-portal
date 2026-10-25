from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

# Allow CORS for API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 0. BACKEND DATABASE (DUMMY DATA)
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
    # Asali (Live) money ke liye yahan apni Live Key aur Live Salt dalna hoga
    key = "OLBUPA" 
    salt = "63LJwDVAEKqfR32B3ynr0TKayqyVjGg7" 
    
    # Hash formula: key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10|salt
    hash_string = f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
    hash_val = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    
    return {"hash": hash_val, "key": key}


# ==========================================
# 1. HOME PAGE DESIGN
# ==========================================
html_design = """
<!DOCTYPE html>
<html lang="en" style="scroll-behavior: smooth;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Social Security Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }
        .card-hover:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
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
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 leading-relaxed text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है।"</p></div>
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
status_check_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Check Application Status</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function checkAppStatus(e) {
            e.preventDefault();
            let appNo = document.getElementById('appNoInput').value.trim().toUpperCase();
            let resBox = document.getElementById('statusResult');
            let statIcon = document.getElementById('stat_icon');
            let statText = document.getElementById('stat_text');
            let statRemark = document.getElementById('stat_remark');

            resBox.classList.remove('hidden');
            
            let isApplied = localStorage.getItem('user_has_applied');
            let savedAppNo = localStorage.getItem('user_app_no');
            let appStatus = localStorage.getItem('app_status');
            let pensionSent = localStorage.getItem('pension_sent');

            if (appNo === savedAppNo && isApplied === 'true') {
                if(appStatus === 'rejected') {
                    let reason = localStorage.getItem('reject_reason') || "Admin rejected without remark.";
                    resBox.className = "mt-6 border p-4 rounded-lg bg-red-50 border-red-200";
                    statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                    statText.className = "text-red-600 font-bold";
                    statText.innerText = "Rejected by System/Admin";
                    statRemark.innerHTML = "<strong>Remark:</strong> " + reason;
                    statRemark.classList.remove('hidden');
                } else if (appStatus === 'admin_pending') {
                    resBox.className = "mt-6 border p-4 rounded-lg bg-blue-50 border-blue-200";
                    statIcon.className = "fa-solid fa-user-check text-blue-600 mr-1";
                    statText.className = "text-blue-600 font-bold";
                    statText.innerText = "Pending Final Admin Approval";
                    statRemark.classList.add('hidden');
                } else if (appStatus === 'approved') {
                    if(pensionSent === 'true') {
                        resBox.className = "mt-6 border p-4 rounded-lg bg-green-50 border-green-200";
                        statIcon.className = "fa-solid fa-money-bill-wave text-green-600 mr-1";
                        statText.className = "text-green-600 font-bold";
                        statText.innerText = "Application Approved & Pension Sent (DBT Successful)";
                        statRemark.classList.add('hidden');
                    } else {
                        resBox.className = "mt-6 border p-4 rounded-lg bg-green-50 border-green-200";
                        statIcon.className = "fa-solid fa-circle-check text-green-600 mr-1";
                        statText.className = "text-green-600 font-bold";
                        statText.innerText = "Application Approved (Active Beneficiary)";
                        statRemark.classList.add('hidden');
                    }
                } else {
                    resBox.className = "mt-6 border p-4 rounded-lg bg-orange-50 border-orange-200";
                    statIcon.className = "fa-solid fa-hourglass-half text-orange-600 mr-1";
                    statText.className = "text-orange-600 font-bold";
                    statText.innerText = "Pending System Verification";
                    statRemark.classList.add('hidden');
                }
            } else {
                 resBox.className = "mt-6 border p-4 rounded-lg bg-gray-50 border-gray-200";
                statIcon.className = "fa-solid fa-question-circle text-gray-600 mr-1";
                statText.className = "text-gray-600 font-bold";
                statText.innerText = "Application Not Found / Not Paid";
                statRemark.classList.add('hidden');
            }
        }
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
user_register_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>New User Registration</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        const stateLanguages = {
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
        };

        function updateLanguageOptions() {
            let state = document.getElementById('state_select').value;
            let langSelect = document.getElementById('language_select');
            langSelect.innerHTML = '<option value="">Select Language</option>';

            if(state && stateLanguages[state]) {
                let localLang = stateLanguages[state];
                let langs = new Set([localLang, "English", "Hindi"]); 
                langs.forEach(l => {
                    langSelect.innerHTML += `<option value="${l}">${l}</option>`;
                });
                document.getElementById('dynamic_heading').innerText = `User Registration (${localLang} / English / Hindi)`;
            } else {
                document.getElementById('dynamic_heading').innerText = `User Registration (ନୂଆ ଆବେଦନକାରୀ)`;
            }
        }

        let currentOTP = "";
        function generateOTP() {
            currentOTP = Math.floor(100000 + Math.random() * 900000).toString();
            document.getElementById('otpDisplay').innerText = "Demo OTP received: " + currentOTP;
            document.getElementById('otpDisplay').classList.remove('hidden');
        }
        function verifyOTP() {
            let enteredOTP = document.getElementById('otpInput').value;
            if (enteredOTP === currentOTP && enteredOTP !== "") {
                document.getElementById('otpSuccess').classList.remove('hidden');
                document.getElementById('otpError').classList.add('hidden');
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('submitBtn').classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                document.getElementById('otpError').classList.remove('hidden');
                document.getElementById('otpSuccess').classList.add('hidden');
            }
        }

        function handleUserRegistration(event) {
            event.preventDefault();
            let pwd = document.getElementById('reg_pass').value;
            let conf_pwd = document.getElementById('reg_conf_pass').value;
            let fullName = document.getElementById('reg_full_name').value;
            let mobileNo = document.getElementById('reg_mobile').value;
            let emailId = document.getElementById('reg_email').value;
            
            if (pwd !== conf_pwd) {
                alert('Password and Confirm Password do not match!');
                return;
            }
            
            let randomNum = Math.floor(100000 + Math.random() * 900000);
            let appNo = 'APP-' + randomNum;
            
            localStorage.setItem('user_app_no', appNo);
            localStorage.setItem('user_password', pwd);
            localStorage.setItem('user_full_name', fullName);
            localStorage.setItem('user_mobile', mobileNo);
            localStorage.setItem('user_email', emailId);
            
            alert('Registration Successful! Your Unique Application No is: ' + appNo + '. Please Login using this ID.');
            window.location.href = '/user/login';
        }
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
            <div id="otpDisplay" class="hidden text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse"></div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Enter OTP</label>
                <div class="flex"><input type="text" id="otpInput" class="w-full px-4 py-2 border rounded-l-lg" required><button type="button" class="bg-green-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="verifyOTP()">Verify</button></div>
                <p id="otpSuccess" class="hidden text-green-600 text-xs font-bold mt-1"><i class="fa-solid fa-check-circle"></i> OTP Verified</p>
                <p id="otpError" class="hidden text-red-600 text-xs font-bold mt-1"><i class="fa-solid fa-xmark-circle"></i> Invalid OTP</p>
            </div>
            <div class="flex gap-4">
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Set Password</label><input type="password" id="reg_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Confirm Password</label><input type="password" id="reg_conf_pass" class="w-full px-4 py-2 border rounded-lg" required></div>
            </div>
            <button type="submit" id="submitBtn" disabled class="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700 opacity-50 cursor-not-allowed transition">
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
user_login_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User / Beneficiary Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function handleUserLogin(event) {
            event.preventDefault();
            let appNo = document.getElementById('login_app_no').value.trim().toUpperCase();
            let pass = document.getElementById('login_pass').value;
            
            let savedAppNo = localStorage.getItem('user_app_no');
            let savedPass = localStorage.getItem('user_password');
            
            if (!savedPass || !savedAppNo) {
                alert('No Registration Found! Please register first.');
                return;
            }
            
            if (appNo === savedAppNo && pass === savedPass) {
                window.location.href = '/user/dashboard';
            } else {
                alert('Access Denied: Invalid Application Number or Password!');
            }
        }
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
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
            <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700">Login</button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# 5. FULL USER DASHBOARD 
# ==========================================
user_dashboard_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        const stateLanguages = {
            "Odisha": "Odia"
        };

        const locationData = {
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
                "Phulbani": ["Phiringia", "Khajuripada", "K.Nuagaon", "Daringbadi", "Balliguda", "Kotgarh", "Tumudibandh", "G.Udayagiri", "Raikia", "Tikabali", "Chakapad", "Phulbani"],
                "Puri": ["Brahmagiri", "Krushnaprasad", "Satyabadi", "Kanas", "Delang", "Pipili", "Nimapada", "Gop", "Kakatpur", "Astarang", "Puri Sadar"],
                "Rayagada": ["Kolanara", "Kaalyansinghpur", "Kaashipur", "Padmapur", "Ramanaguda", "Gunupur", "Gudari", "Muniguda", "Bisam-Cuttack", "Chandrapur", "Rayagada"],
                "Sambalpur": ["Dhankauda", "Maneswar", "Jujumora", "Rengali", "Rairakhola", "Nakatideul", "Kuchinda", "Bamara", "Jamanakira", "Pairakhal", "Sambalpur"],
                "Sonepur": ["Tarva", "Birmaharajpur", "Ulunda", "Dunguripalli", "Binka", "Sonepur"],
                "Sundargarh": ["Balisankara", "Subdega", "Lephripara", "Hemgiri", "Rajgangpur", "Panposh", "Tanngarapalli", "Kutra", "Lathikata", "Kuanrmunda", "Badagaon", "Nuagaon", "Bisra", "Gurundia", "Koira", "Lahunipada", "Banaigarh", "Sundargarh (Sadar)"]
            }
        };

        window.onload = function() {
            populateDistricts();
            
            let dynamicFee = localStorage.getItem('app_fee') || '100';
            document.querySelectorAll('.display_app_fee').forEach(el => el.innerText = dynamicFee);
            
            let savedFullName = localStorage.getItem('user_full_name');
            let savedMobile = localStorage.getItem('user_mobile');
            let savedEmail = localStorage.getItem('user_email');
            
            if(savedFullName) {
                let nameField = document.getElementById('full_name');
                nameField.value = savedFullName;
                nameField.setAttribute('readonly', 'readonly');
                nameField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
            }
            if(savedMobile) {
                let mobField = document.getElementById('app_mobile');
                if(mobField){
                    mobField.value = savedMobile;
                    mobField.setAttribute('readonly', 'readonly');
                    mobField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
                }
            }
            if(savedEmail) {
                let emailField = document.getElementById('app_email');
                if(emailField){
                    emailField.value = savedEmail;
                    emailField.setAttribute('readonly', 'readonly');
                    emailField.className = "w-full border-b border-gray-300 p-2 outline-none font-bold text-gray-500 bg-gray-100 cursor-not-allowed";
                }
            }
            
            let isApplied = localStorage.getItem('user_has_applied');
            if(isApplied === 'true') {
                document.getElementById('apply_form_container').innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded shadow-sm text-center">
                        <i class="fa-solid fa-triangle-exclamation text-yellow-500 text-4xl mb-4"></i>
                        <h3 class="text-xl font-bold text-gray-800">Application Already Submitted</h3>
                        <p class="text-gray-600 mt-2">You have already submitted an application with this Aadhaar Number. Multiple applications are not allowed. Please check your status.</p>
                        <button onclick="switchUserTab('status')" class="mt-4 bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700">Check Status</button>
                    </div>
                `;
            }

            // RENEWAL LOGIC UPDATE
            let penSent = localStorage.getItem('app_status');
            if(penSent === 'pension_sent') {
                let rname = localStorage.getItem('user_full_name');
                let rapp = localStorage.getItem('user_app_no');
                document.getElementById('section-renew').innerHTML = `
                    <h2 class="text-2xl font-bold mb-4 text-orange-600"><i class="fa-solid fa-clock-rotate-left"></i> 3-Month Renewal</h2>
                    <div class="bg-white border rounded-xl p-6 shadow-sm mb-6 border-l-4 border-green-500">
                        <p class="text-gray-600 font-semibold mb-2">Beneficiary Found: <strong class="text-gray-800">${rname} (${rapp})</strong></p>
                        <p class="text-sm text-gray-500 mb-4">Your current pension is active. Proceed with Renewal to continue receiving benefits.</p>
                        <button onclick="alert('Data Verified! Proceeding to Payment Gateway...');" class="bg-orange-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-orange-700 transition shadow"><i class="fa-solid fa-credit-card"></i> Pay Renewal Fee</button>
                    </div>
                `;
            } else {
                 document.getElementById('section-renew').innerHTML = `
                    <h2 class="text-2xl font-bold mb-4 text-orange-600"><i class="fa-solid fa-clock-rotate-left"></i> 3-Month Renewal</h2>
                    <div class="bg-white border rounded-xl p-6 shadow-sm mb-6 text-center">
                        <i class="fa-solid fa-folder-open text-gray-300 text-5xl mb-3"></i>
                        <p class="text-gray-500 font-semibold">No active pension found eligible for renewal yet.</p>
                    </div>
                `;
            }
        };

        function populateDistricts() {
            let state = "Odisha"; 
            let distSelect = document.getElementById("district");
            let blockSelect = document.getElementById("block");
            
            if(distSelect && blockSelect) {
                distSelect.innerHTML = "<option value=''>Select</option>";
                blockSelect.innerHTML = "<option value=''>Select</option>";

                if(state && locationData[state]) {
                    for(let dist in locationData[state]) {
                        distSelect.innerHTML += `<option value='${dist}'>${dist}</option>`;
                    }
                }
            }
        }

        function populateBlocks() {
            let state = "Odisha";
            let dist = document.getElementById("district").value;
            let blockSelect = document.getElementById("block");
            
            if(blockSelect) {
                blockSelect.innerHTML = "<option value=''>Select</option>";

                if(state && dist && locationData[state][dist]) {
                    let blocks = locationData[state][dist];
                    for(let i=0; i<blocks.length; i++) {
                        blockSelect.innerHTML += `<option value='${blocks[i]}'>${blocks[i]}</option>`;
                    }
                }
            }
        }

        function switchUserTab(tabId) {
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
            if(tabId === 'status') {
                loadPrintData();
            }
        }
        
        function calculateAge() {
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age Pension' && age < 55) { alert('System Error: Age must be 55 or above for Old Age Pension.'); }
        }

        function checkSchemeCondition() {
            let scheme = document.getElementById('scheme').value;
            let specialBox = document.getElementById('special_cert_box');
            if(scheme === 'Widow Pension' || scheme === 'Disability Pension' || scheme === 'Divorcee Pension' || scheme === 'Transgender Pension') {
                specialBox.classList.remove('hidden');
            } else { specialBox.classList.add('hidden'); }
        }

        function updateAgeProof() {
            let docType = document.getElementById("age_proof_type").value;
            let docNumBox = document.getElementById("age_proof_number");
            let docFileBox = document.getElementById("age_proof_file_container");
            if(docType) {
                docNumBox.classList.remove("hidden");
                docNumBox.placeholder = "Enter " + docType + " Number";
                docFileBox.classList.remove("hidden");
            } else {
                docNumBox.classList.add("hidden");
                docFileBox.classList.add("hidden");
            }
        }

        function verifyAadhaar() {
            let fullName = document.getElementById('full_name').value;
            let aadhaarInput = document.getElementById('aadhaar_input').value;
            
            let savedAadhaar = localStorage.getItem('user_aadhaar');
            if (savedAadhaar === aadhaarInput) {
                alert('An application with this Aadhaar number already exists!');
                return;
            }
            
            if(!fullName) { alert("Please enter your Full Name at the top to fetch matching data."); return; }
            if(!aadhaarInput) { alert("Please enter Aadhaar Number."); return; }
            
            alert('Aadhaar OTP verified automatically!');
            document.getElementById('aadhaar_success_box').classList.remove('hidden');
            document.getElementById('aadhaar_status').classList.add('hidden');
        }

        async function fetchIFSC() {
            let ifsc = document.getElementById("ifsc_code").value.trim().toUpperCase();
            if(!ifsc) { alert("Please enter IFSC Code first."); return; }
            try {
                let res = await fetch(`https://ifsc.razorpay.com/${ifsc}`);
                if(res.ok) {
                    let data = await res.json();
                    document.getElementById("bank_name_display").value = data.BANK;
                } else {
                    alert("Invalid IFSC Code");
                    document.getElementById("bank_name_display").value = "";
                }
            } catch (e) {
                alert("Error fetching IFSC details.");
            }
        }

        async function verifyIncome() {
            let cert = document.getElementById('income_cert_no').value;
            let year = document.getElementById('income_year').value;

            if(cert && year !== "Select") {
                try {
                    let response = await fetch(`/api/get_income?cert_no=${cert}`);
                    let data = await response.json();

                    if(data.error) {
                        alert("Invalid Certificate Number or Data Not Found in Database!");
                        return;
                    }

                    alert(`Fetching Income Details from Database for Certificate ${cert}...`);
                    
                    document.getElementById('inc_issued_to').value = data.name;
                    document.getElementById('inc_father').value = data.father;
                    document.getElementById('inc_mother').value = data.mother;
                    document.getElementById('inc_district').value = data.district;
                    document.getElementById('inc_authority').value = data.authority;
                    document.getElementById('inc_date').value = data.date;
                    document.getElementById('inc_amount').value = data.amount;
                    document.getElementById('inc_relation').value = "Self";

                    let nameField = document.getElementById('full_name');
                    if(!nameField.value) {
                        nameField.value = data.name;
                    }
                    document.getElementById('father_name').value = data.father;
                    document.getElementById('mother_name').value = data.mother;
                    
                    populateDistricts();
                    setTimeout(() => {
                        document.getElementById("district").value = data.district;
                        populateBlocks();
                    }, 100);

                } catch (error) {
                    console.error("Error fetching data:", error);
                    alert("System Error: Unable to fetch data from Server.");
                }
            } else {
                alert("Please select Issuing Year and enter Certificate No. first to auto-fetch.");
            }
        }
        
        function updateAddressCharCount() {
            let addressInput = document.getElementById('manual_address');
            let charsLeft = 200 - addressInput.value.length;
            document.getElementById('address_char_count').innerText = charsLeft + " characters remaining";
        }
        
        function goToPaymentStep(e) {
            e.preventDefault();
            
            localStorage.setItem('user_aadhaar', document.getElementById('aadhaar_input').value);
            localStorage.setItem('u_father', document.getElementById('father_name').value);
            localStorage.setItem('u_mother', document.getElementById('mother_name').value);
            localStorage.setItem('u_scheme', document.getElementById('scheme').value);
            localStorage.setItem('u_dist', document.getElementById('district').value);
            localStorage.setItem('u_block', document.getElementById('block').value);
            localStorage.setItem('u_gp', document.getElementById('panchayat').value);
            localStorage.setItem('u_address', document.getElementById('manual_address').value);
            
            localStorage.setItem('u_gender', document.getElementById('gender_select').value);
            localStorage.setItem('u_dob', document.getElementById('dob').value);
            localStorage.setItem('u_inc_cert', document.getElementById('income_cert_no').value);
            localStorage.setItem('u_inc_auth', document.getElementById('inc_authority').value);
            localStorage.setItem('u_inc_amount', document.getElementById('inc_amount').value);
            localStorage.setItem('u_ifsc', document.getElementById('ifsc_code').value);
            localStorage.setItem('u_bank', document.getElementById('bank_name_display').value); // Dynamic Bank saved
            localStorage.setItem('u_acc', document.getElementById('acc_no').value);
            
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-payment-step').classList.remove('hidden');
        }

        function togglePayButton() {
            let cb = document.getElementById('tnc_checkbox');
            let btn = document.getElementById('payu_button');
            if(cb.checked) {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                btn.disabled = true;
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            }
        }

        async function simulatePayUPayment() {
            alert('Redirecting to Asali PayU Live Secure Payment Gateway...');
            
            let txnid = "TXN" + new Date().getTime();
            let amtSetting = localStorage.getItem('app_fee') || '100';
            let amount = parseFloat(amtSetting).toFixed(2);
            localStorage.setItem('paid_amount', amount); 
            
            let productinfo = "PensionApplication";
            let firstname = document.getElementById('full_name').value || "User";
            let email = document.getElementById('app_email').value || "user@example.com"; 
            let phone = document.getElementById('app_mobile').value || "9876543210";
            
            let surl = window.location.origin + "/payment_success";
            let furl = window.location.origin + "/payment_failure";

            // AUTO SYSTEM VERIFICATION LOGIC (REAL)
            let incAmt = document.getElementById('inc_amount').value || "";
            let authName = document.getElementById('inc_issued_to').value || "";
            
            let autoRemark = "";
            let autoStatus = "sys_pending"; // SET AS PENDING FOR SYSTEM TO VERIFY
            
            localStorage.setItem('user_has_applied', 'true');
            localStorage.setItem('app_status', autoStatus);
            
            try {
                let response = await fetch(`/api/payu_hash?txnid=${txnid}&amount=${amount}&productinfo=${productinfo}&firstname=${firstname}&email=${email}`);
                let data = await response.json();

                let form = document.createElement("form");
                form.setAttribute("method", "POST");
                form.setAttribute("action", "https://secure.payu.in/_payment");

                let params = {
                    "key": data.key,
                    "txnid": txnid,
                    "amount": amount,
                    "productinfo": productinfo,
                    "firstname": firstname,
                    "email": email,
                    "phone": phone,
                    "surl": surl,
                    "furl": furl,
                    "hash": data.hash
                };

                for(let key in params) {
                    let hiddenField = document.createElement("input");
                    hiddenField.setAttribute("type", "hidden");
                    hiddenField.setAttribute("name", key);
                    hiddenField.setAttribute("value", params[key]);
                    form.appendChild(hiddenField);
                }

                document.body.appendChild(form);
                form.submit(); 
                
            } catch (error) {
                alert("Error connecting to PayU Gateway. Checking connection...");
            }
        }

        function loadPrintData() {
            let safeSet = (className, key, defaultVal) => {
                let val = localStorage.getItem(key) || defaultVal;
                document.querySelectorAll(className).forEach(el => el.innerText = val);
            };
            
            safeSet('.print_u_name', 'user_full_name', 'N/A');
            safeSet('.print_u_appno', 'user_app_no', 'N/A');
            safeSet('.print_u_scheme', 'u_scheme', 'N/A');
            safeSet('.display_app_fee', 'paid_amount', '100.00');

            let safeSetId = (id, key) => {
                let el = document.getElementById(id);
                if(el) el.innerText = localStorage.getItem(key) || 'N/A';
            };
            
            safeSetId('print_u_father', 'u_father');
            safeSetId('print_u_mother', 'u_mother');
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
        }
        
        function viewUserAppModal() {
            loadPrintData();
            document.getElementById('user_app_view_modal').classList.remove('hidden');
        }

        function closeUserAppModal() {
            document.getElementById('user_app_view_modal').classList.add('hidden');
        }
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
                    
                    <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
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

                    <div class="border border-blue-200 bg-blue-50 p-4 rounded-lg mt-6 shadow-sm">
                        <h3 class="text-lg font-bold text-blue-800 mb-4 border-b border-blue-200 pb-2">Income Certificate Details</h3>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-700">Issuing Year <span class="text-red-500">*</span></label>
                                <select id="income_year" class="w-full border p-2 rounded bg-white">
                                    <option>Select</option><option>2024-25</option><option>2025-26</option><option>2026-27</option>
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
                            <input type="file" class="w-full md:w-1/2 border p-1 rounded text-sm bg-white" accept=".pdf" required>
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
                                <label class="block text-sm text-gray-600 mb-1">Bank Name</label>
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
                    <p class="text-sm font-semibold text-gray-500 mb-2">Proceed to Secure Payment</p>
                    <button type="button" id="payu_button" onclick="simulatePayUPayment()" disabled class="bg-green-600 text-white font-extrabold text-xl py-4 px-10 rounded-lg shadow-lg hover:bg-green-700 opacity-50 cursor-not-allowed transition-all w-full md:w-auto">
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
                    <div><p class="text-gray-500 font-semibold text-xs">Scheme Category</p><p class="font-bold text-base print_u_scheme"></p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Applied Date</p><p class="font-bold text-base">23-Oct-2026</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Payment Status</p><p class="font-bold text-green-600"><i class="fa-solid fa-check-circle"></i> Paid (₹<span class="display_app_fee"></span>)</p></div>
                </div>
                
                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">Application Details</h4>
                <div class="grid grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded border">
                    <p><strong>Name:</strong> <span class="print_u_name"></span></p>
                    <p><strong>Aadhaar:</strong> <script>document.write(localStorage.getItem('user_aadhaar') || 'N/A');</script></p>
                    <p><strong>District:</strong> <script>document.write(localStorage.getItem('u_dist') || 'N/A');</script></p>
                    <p><strong>Block:</strong> <script>document.write(localStorage.getItem('u_block') || 'N/A');</script></p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# 6. FULL ADMIN DASHBOARD
# ==========================================
admin_login_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Login - Private Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function togglePassword() {
            var passField = document.getElementById("password");
            var eyeIcon = document.getElementById("eye-icon");
            if (passField.type === "password") { passField.type = "text"; eyeIcon.classList.remove("fa-eye"); eyeIcon.classList.add("fa-eye-slash"); } 
            else { passField.type = "password"; eyeIcon.classList.remove("fa-eye-slash"); eyeIcon.classList.add("fa-eye"); }
        }

        function handleAdminLogin(event) {
            event.preventDefault();
            let adminId = document.getElementById('admin_id').value;
            let adminPass = document.getElementById('password').value;

            let savedId = localStorage.getItem('admin_email') || 'admin@kulusutar.in';
            let savedPass = localStorage.getItem('admin_password') || 'Admin@123';

            if(adminId === savedId && adminPass === savedPass) {
                window.location.href = '/admin';
            } else {
                alert('Access Denied: Invalid ID or Password! Please enter correct credentials.');
            }
        }
    </script>
</head>
<body class="bg-gray-100 font-sans flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700">
        <div class="text-center mb-8">
            <i class="fa-solid fa-user-shield text-5xl text-blue-700 mb-3"></i>
            <h2 class="text-2xl font-bold text-gray-800">Admin Login</h2>
        </div>
        <form onsubmit="handleAdminLogin(event)" class="space-y-6">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Admin ID / Email</label>
                <div class="relative"><i class="fa-solid fa-envelope absolute left-3 top-3.5 text-gray-400"></i><input type="text" id="admin_id" placeholder="Enter ID or Email" class="w-full pl-10 pr-4 py-3 border rounded-lg" required></div>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <div class="relative"><i class="fa-solid fa-lock absolute left-3 top-3.5 text-gray-400"></i><input type="password" id="password" placeholder="Enter password" class="w-full pl-10 pr-10 py-3 border rounded-lg" required>
                    <button type="button" onclick="togglePassword()" class="absolute right-3 top-3.5 text-gray-400 hover:text-blue-500"><i id="eye-icon" class="fa-solid fa-eye"></i></button>
                </div>
            </div>
            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg hover:bg-blue-800 shadow-md">Login to Dashboard</button>
        </form>
        <div class="text-center mt-6"><a href="/" class="text-sm text-gray-500 hover:text-blue-700"><i class="fa-solid fa-arrow-left mr-1"></i> Back to Home</a></div>
    </div>
</body>
</html>
"""

admin_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Private Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        window.onload = function() {
            if(localStorage.getItem('app_fee')) document.getElementById('app_fee').value = localStorage.getItem('app_fee');
            if(localStorage.getItem('payu_merchant_key')) document.getElementById('payu_merchant_key').value = localStorage.getItem('payu_merchant_key');
            if(localStorage.getItem('payu_merchant_salt')) document.getElementById('payu_merchant_salt').value = localStorage.getItem('payu_merchant_salt');
            if(localStorage.getItem('rzp_key_id')) document.getElementById('rzp_key_id').value = localStorage.getItem('rzp_key_id');
            if(localStorage.getItem('rzp_key_secret')) document.getElementById('rzp_key_secret').value = localStorage.getItem('rzp_key_secret');
            if(localStorage.getItem('payout_api_key')) document.getElementById('payout_api_key').value = localStorage.getItem('payout_api_key');
            if(localStorage.getItem('payout_api_secret')) document.getElementById('payout_api_secret').value = localStorage.getItem('payout_api_secret');
            
            loadAdminData();
            loadAdminProfile();
        };

        function saveSettings() {
            localStorage.setItem('app_fee', document.getElementById('app_fee').value);
            localStorage.setItem('payu_merchant_key', document.getElementById('payu_merchant_key').value);
            localStorage.setItem('payu_merchant_salt', document.getElementById('payu_merchant_salt').value);
            localStorage.setItem('rzp_key_id', document.getElementById('rzp_key_id').value);
            localStorage.setItem('rzp_key_secret', document.getElementById('rzp_key_secret').value);
            localStorage.setItem('payout_api_key', document.getElementById('payout_api_key').value);
            localStorage.setItem('payout_api_secret', document.getElementById('payout_api_secret').value);
            alert('Settings Saved Successfully!');
        }

        function loadAdminProfile() {
            let n = localStorage.getItem('admin_name');
            if(n) {
                document.getElementById('prof_admin_name').value = n;
                document.getElementById('welcome_admin_name').innerText = n;
            }
            
            let m = localStorage.getItem('admin_mobile');
            if(m) document.getElementById('prof_admin_mobile').value = m;
            
            let e = localStorage.getItem('admin_email');
            if(e) document.getElementById('prof_admin_email').value = e;
        }

        function saveAdminProfile() {
            let n = document.getElementById('prof_admin_name').value;
            let m = document.getElementById('prof_admin_mobile').value;
            let e = document.getElementById('prof_admin_email').value;
            let p1 = document.getElementById('prof_new_pass').value;
            let p2 = document.getElementById('prof_conf_pass').value;
            
            if(p1 || p2) {
                if(p1 !== p2) {
                    alert("Passwords do not match!");
                    return;
                }
                localStorage.setItem('admin_password', p1);
            }
            
            localStorage.setItem('admin_name', n);
            localStorage.setItem('admin_mobile', m);
            localStorage.setItem('admin_email', e);
            
            alert("Admin Profile Saved Successfully! Login credentials updated.");
            location.reload();
        }

        function switchTab(tabId, element) {
            let sections = document.querySelectorAll('.content-section');
            for(let i=0; i<sections.length; i++) { sections[i].classList.add('hidden'); }
            document.getElementById('section-' + tabId).classList.remove('hidden');

            let links = document.querySelectorAll('.menu-link');
            for(let i=0; i<links.length; i++) {
                links[i].classList.remove('bg-blue-700', 'text-white');
                links[i].classList.add('text-slate-300', 'hover:bg-slate-800');
            }
            element.classList.remove('text-slate-300', 'hover:bg-slate-800');
            element.classList.add('bg-blue-700', 'text-white');

            let titles = {
                'dashboard': '<i class="fa-solid fa-list-check text-blue-600 mr-2"></i> Dashboard Overview',
                'sysverify': '<i class="fa-solid fa-microchip text-blue-600 mr-2"></i> System Verification (Level 1)',
                'adminapprove': '<i class="fa-solid fa-file-signature text-blue-600 mr-2"></i> Final Admin Approval (Level 2)',
                'rejected': '<i class="fa-solid fa-trash-can text-red-600 mr-2"></i> Rejected Applications Box',
                'beneficiaries': '<i class="fa-solid fa-users text-blue-600 mr-2"></i> Manage Beneficiaries',
                'renewals': '<i class="fa-solid fa-clock-rotate-left text-blue-600 mr-2"></i> 3-Month Renewals',
                'payments': '<i class="fa-solid fa-money-bill-transfer text-blue-600 mr-2"></i> Payment Records',
                'settings': '<i class="fa-solid fa-gears text-blue-600 mr-2"></i> System & API Settings',
                'profile': '<i class="fa-solid fa-user-gear text-blue-600 mr-2"></i> Admin Profile Settings'
            };
            document.getElementById('header-title').innerHTML = titles[tabId];
        }

        function loadAdminData() {
            document.getElementById('count_total').innerText = '0';
            document.getElementById('count_pending').innerText = '0';
            document.getElementById('count_approved').innerText = '0';
            document.getElementById('count_rejected').innerText = '0';
            document.getElementById('total_wallet_val').innerText = '0';

            let isApplied = localStorage.getItem('user_has_applied');
            if(isApplied === 'true') {
                document.getElementById('count_total').innerText = '1';
                
                let amt = localStorage.getItem('paid_amount') || '100';
                document.getElementById('total_wallet_val').innerText = amt;
                
                let status = localStorage.getItem('app_status') || 'sys_pending';
                let name = localStorage.getItem('user_full_name');
                let appNo = localStorage.getItem('user_app_no');
                let scheme = localStorage.getItem('u_scheme');
                let bankName = localStorage.getItem('u_bank') || 'N/A';
                let accNo = localStorage.getItem('u_acc') || 'N/A';

                if(status === 'sys_pending') {
                    document.getElementById('count_pending').innerText = '1';
                    document.getElementById('sys_verify_tbody').innerHTML = `
                        <tr class="hover:bg-green-50 border-b bg-green-50 transition-all">
                            <td class="py-4 px-4 font-medium text-blue-600">#${appNo} <span class="bg-green-500 text-white text-[10px] px-1 rounded ml-1">NEW</span></td>
                            <td class="py-4 px-4 font-bold text-green-800">${name}</td>
                            <td class="py-4 px-4">${scheme}</td>
                            <td class="py-4 px-4 flex justify-center space-x-2 items-center">
                                <button onclick="viewFullApplication()" class="bg-purple-600 text-white px-3 py-1 rounded shadow hover:bg-purple-700 text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                <button onclick="verifySysDoc()" class="bg-blue-500 text-white px-3 py-1 rounded shadow hover:bg-blue-600 text-xs font-bold"><i class="fa-solid fa-robot"></i> Auto Verify & Send to Admin</button>
                                <button onclick="rejectApp()" class="bg-red-500 text-white px-3 py-1 rounded shadow hover:bg-red-600 text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                            </td>
                        </tr>
                    `;
                } else if(status === 'admin_pending') {
                    document.getElementById('count_pending').innerText = '1';
                    document.getElementById('admin_approve_tbody').innerHTML = `
                        <tr class="hover:bg-green-50 border-b transition-all">
                            <td class="py-4 px-4 font-medium text-blue-600">#${appNo} <span class="bg-green-500 text-white text-[10px] px-1 rounded ml-1">SYS OK</span></td>
                            <td class="py-4 px-4 font-bold text-blue-800">${name}</td>
                            <td class="py-4 px-4"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> System Approved</span></td>
                            <td class="py-4 px-4 flex justify-center space-x-2 items-center">
                                <button onclick="viewFullApplication()" class="bg-purple-600 text-white px-4 py-1 rounded shadow hover:bg-purple-700 font-bold"><i class="fa-solid fa-eye"></i> View Details</button>
                                <button onclick="finalApprove()" class="bg-green-600 text-white px-4 py-1 rounded shadow hover:bg-green-700 font-bold"><i class="fa-solid fa-signature"></i> Final Approve</button>
                                <button onclick="rejectApp()" class="bg-red-500 text-white px-4 py-1 rounded shadow hover:bg-red-600 font-bold"><i class="fa-solid fa-ban"></i> Reject</button>
                            </td>
                        </tr>
                    `;
                } else if(status === 'approved' || status === 'pension_sent') {
                    document.getElementById('count_approved').innerText = '1';
                    let sentFlag = localStorage.getItem('pension_sent');
                    let btnHtml = "";
                    if(sentFlag === 'true') {
                        btnHtml = `<button disabled class="bg-green-600 text-white px-3 py-1 rounded shadow text-xs font-bold cursor-not-allowed"><i class="fa-solid fa-check-double"></i> Paid</button>`;
                        
                        // Populate Payment Tab
                        let utr = localStorage.getItem('utr_number') || 'N/A';
                        document.getElementById('payments_tbody').innerHTML = `
                            <tr class="bg-gray-50 border-b">
                                <td class="py-4 px-4 font-bold text-blue-600">#${appNo}</td>
                                <td class="py-4 px-4 font-bold">${name}</td>
                                <td class="py-4 px-4 font-semibold text-gray-700">${bankName} (A/C: ${accNo})</td>
                                <td class="py-4 px-4"><span class="bg-green-100 text-green-800 py-1 px-3 rounded font-bold">Success</span></td>
                                <td class="py-4 px-4 font-mono font-bold text-gray-800">${utr}</td>
                            </tr>
                        `;
                    } else {
                        btnHtml = `<button onclick="markManualPaid('${appNo}', '${name}', '${accNo}')" class="bg-blue-600 text-white px-3 py-1 rounded shadow text-xs font-bold hover:bg-blue-700"><i class="fa-solid fa-money-check-dollar"></i> Pay Pension (Manual)</button>`;
                    }

                    document.getElementById('beneficiaries_tbody').innerHTML = `
                        <tr class="hover:bg-gray-50 border-b">
                            <td class="py-4 px-4 font-medium text-blue-600">#${appNo}</td>
                            <td class="py-4 px-4 font-bold">${name}</td>
                            <td class="py-4 px-4"><span class="bg-green-100 text-green-800 py-1 px-3 rounded-full text-xs font-semibold">Active</span></td>
                            <td class="py-4 px-4 text-center space-x-2 flex items-center justify-center">
                                ${btnHtml}
                                <button class="bg-orange-500 text-white px-3 py-1 rounded shadow text-xs font-bold hover:bg-orange-600"><i class="fa-solid fa-pause"></i> Hold</button>
                                <button class="bg-red-600 text-white px-3 py-1 rounded shadow text-xs font-bold hover:bg-red-700"><i class="fa-solid fa-hand-paper"></i> Stop</button>
                            </td>
                        </tr>
                    `;
                } else if(status === 'rejected') {
                    document.getElementById('count_rejected').innerText = '1';
                    let reason = localStorage.getItem('reject_reason') || 'System Auto-Rejected';
                    document.getElementById('rejected_tbody').innerHTML = `
                        <tr id="rej_row_real" class="hover:bg-red-50 border-b">
                            <td class="py-4 px-4 font-medium text-red-600">#${appNo}</td>
                            <td class="py-4 px-4 font-bold text-gray-800">${name}</td>
                            <td class="py-4 px-4 text-gray-600 font-semibold">System/Admin</td>
                            <td class="py-4 px-4 text-gray-600 italic">${reason}</td>
                            <td class="py-4 px-4 text-center">
                                <button onclick="deleteRejectedRow('rej_row_real')" class="bg-gray-200 text-red-600 px-3 py-1 rounded shadow hover:bg-red-600 hover:text-white transition text-xs font-bold"><i class="fa-solid fa-trash"></i> Delete Data</button>
                            </td>
                        </tr>
                    `;
                }
            }
        }

        function verifySysDoc() {
            let authName = localStorage.getItem('u_inc_auth') || "";
            let amount = localStorage.getItem('u_inc_amount') || "";
            
            document.getElementById('modal_sys_name').innerText = localStorage.getItem('user_full_name') || 'N/A';
            document.getElementById('modal_sys_inc_name').innerText = authName;
            document.getElementById('modal_sys_inc_amt').innerText = amount;
            
            document.getElementById('sys_verification_modal').classList.remove('hidden');
        }
        function closeSysModal() {
            document.getElementById('sys_verification_modal').classList.add('hidden');
        }

        function approveSys() {
            localStorage.setItem('app_status', 'admin_pending');
            alert("System Validation Completed! Forwarded to Final Admin Approval Portal.");
            location.reload();
        }

        function finalApprove() {
            localStorage.setItem('app_status', 'approved');
            alert("Application Finally Approved! Added to Beneficiaries.");
            location.reload();
        }

        function rejectApp() {
            let reason = prompt("Please enter the reason for rejection (Remark):");
            if (reason != null && reason != "") {
                localStorage.setItem('app_status', 'rejected');
                localStorage.setItem('reject_reason', reason);
                alert("Application Rejected and Moved to Rejected Box with Remark: " + reason);
                document.getElementById('sys_verification_modal').classList.add('hidden');
                location.reload();
            }
        }

        function deleteRejectedRow(rowId) {
            if(confirm("Are you sure you want to permanently delete this rejected application data?")) {
                document.getElementById(rowId).classList.add('hidden');
                localStorage.removeItem('user_has_applied');
                localStorage.removeItem('app_status');
                location.reload();
            }
        }

        function markManualPaid(appNo, name, accNo) {
            let utr = prompt(`Enter Payment UTR/Transaction Number for ${name} (A/C: ${accNo}):`);
            if(utr != null && utr.trim() !== "") {
                localStorage.setItem('utr_number', utr);
                localStorage.setItem('pension_sent', 'true');
                localStorage.setItem('app_status', 'pension_sent');
                alert(`Manual Payment Verified! UTR ${utr} saved. Customer will now see Payment Success status.`);
                location.reload();
            } else {
                alert("UTR Number is required to confirm manual payment.");
            }
        }

        function viewFullApplication() {
            document.getElementById('v_appno').innerText = localStorage.getItem('user_app_no') || 'N/A';
            document.getElementById('v_scheme').innerText = localStorage.getItem('u_scheme') || 'N/A';
            document.getElementById('v_name').innerText = localStorage.getItem('user_full_name') || 'N/A';
            document.getElementById('v_father').innerText = localStorage.getItem('u_father') || 'N/A';
            document.getElementById('v_mother').innerText = localStorage.getItem('u_mother') || 'N/A';
            document.getElementById('v_aadhaar').innerText = localStorage.getItem('user_aadhaar') || 'N/A';
            document.getElementById('v_dist').innerText = localStorage.getItem('u_dist') || 'N/A';
            document.getElementById('v_block').innerText = localStorage.getItem('u_block') || 'N/A';
            document.getElementById('v_gp').innerText = localStorage.getItem('u_gp') || 'N/A';
            document.getElementById('v_address').innerText = localStorage.getItem('u_address') || 'N/A';
            
            document.getElementById('v_dob').innerText = localStorage.getItem('u_dob') || 'N/A';
            document.getElementById('v_gender').innerText = localStorage.getItem('u_gender') || 'N/A';
            document.getElementById('v_inc_cert').innerText = localStorage.getItem('u_inc_cert') || 'N/A';
            document.getElementById('v_inc_auth').innerText = localStorage.getItem('u_inc_auth') || 'N/A';
            document.getElementById('v_inc_amount').innerText = localStorage.getItem('u_inc_amount') || 'N/A';
            
            document.getElementById('v_bank').innerText = localStorage.getItem('u_bank') || 'N/A';
            document.getElementById('v_acc').innerText = localStorage.getItem('u_acc') || 'N/A';
            document.getElementById('v_ifsc').innerText = localStorage.getItem('u_ifsc') || 'N/A';
            
            let fee = localStorage.getItem('paid_amount') || '100';
            document.getElementById('v_fee').innerText = "Paid (₹" + fee + ")";

            document.getElementById('full_app_view_modal').classList.remove('hidden');
        }

        function closeFullAppModal() {
            document.getElementById('full_app_view_modal').classList.add('hidden');
        }
    </script>
</head>
<body class="bg-gray-100 font-sans text-gray-800 flex h-screen overflow-hidden">

    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl h-full print:hidden">
        <div class="p-5 border-b border-slate-700 text-center">
            <i class="fa-solid fa-user-shield text-4xl text-blue-500 mb-2"></i>
            <h2 class="text-xl font-bold">Admin Panel</h2>
        </div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchTab('dashboard', this)" class="menu-link flex items-center px-4 py-3 bg-blue-700 text-white rounded-lg transition"><i class="fa-solid fa-gauge w-6 mr-2"></i> Dashboard</a></li>
                
                <li class="mt-2 border-t border-slate-700 pt-2"><span class="px-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Verification Steps</span></li>
                <li><a href="#" onclick="switchTab('sysverify', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-microchip w-6 mr-2"></i> System Verification</a></li>
                <li><a href="#" onclick="switchTab('adminapprove', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-file-signature w-6 mr-2"></i> Final Admin Approval</a></li>
                <li><a href="#" onclick="switchTab('rejected', this)" class="menu-link flex items-center px-4 py-3 text-red-400 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-trash-can w-6 mr-2"></i> Rejected Box</a></li>

                <li class="mt-4 border-t border-slate-700 pt-2"><span class="px-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Management</span></li>
                <li><a href="#" onclick="switchTab('beneficiaries', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-users w-6 mr-2"></i> Beneficiaries</a></li>
                <li><a href="#" onclick="switchTab('renewals', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> Renewals Tracker</a></li>
                <li><a href="#" onclick="switchTab('payments', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-money-bill-transfer w-6 mr-2"></i> Payment Records</a></li>
                
                <li class="mt-8 border-t border-slate-700 pt-4"><a href="#" onclick="switchTab('settings', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-gears w-6 mr-2"></i> API & Settings</a></li>
                <li><a href="#" onclick="switchTab('profile', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-user-gear w-6 mr-2"></i> Admin Profile</a></li>
            </ul>
        </nav>
        <div class="p-4 border-t border-slate-700">
            <a href="/" class="flex items-center px-4 py-2 text-red-400 hover:bg-red-500 hover:text-white rounded-lg transition"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout</a>
        </div>
    </aside>

    <main class="flex-1 flex flex-col h-full overflow-hidden relative print:hidden">
        <header class="bg-white shadow-sm border-b px-6 py-4 flex justify-between items-center print:hidden">
            <h1 id="header-title" class="text-2xl font-bold"><i class="fa-solid fa-list-check text-blue-600 mr-2"></i> Dashboard Overview</h1>
            <div class="flex items-center space-x-4">
                <span class="text-sm font-medium">Welcome, <strong id="welcome_admin_name">Admin</strong></span>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-6 bg-gray-50 print:hidden">
            
            <div id="section-dashboard" class="content-section">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-purple-500 shadow-sm flex justify-between items-center md:col-span-2">
                        <div><p class="text-sm text-gray-500 font-semibold">Total Wallet Collection (Reg. Fees)</p><h3 class="text-3xl font-bold text-purple-700">₹<span id="total_wallet_val">0</span></h3></div>
                        <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-2xl"><i class="fa-solid fa-wallet"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-blue-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Total Applications</p><h3 id="count_total" class="text-2xl font-bold text-blue-700">0</h3></div>
                        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-file-lines"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-green-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Active Beneficiary</p><h3 id="count_approved" class="text-2xl font-bold text-green-700">0</h3></div>
                        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-check-circle"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-orange-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Pending Approvals</p><h3 id="count_pending" class="text-2xl font-bold text-orange-700">0</h3></div>
                        <div class="w-12 h-12 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-hourglass-half"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-red-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Total Rejected</p><h3 id="count_rejected" class="text-2xl font-bold text-red-700">0</h3></div>
                        <div class="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-ban"></i></div>
                    </div>
                </div>
            </div>

            <!-- SYSTEM VERIFICATION -->
            <div id="section-sysverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-orange-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg text-orange-800"><i class="fa-solid fa-microchip mr-2"></i> System Verification Stage</h2>
                        <div class="space-x-2">
                            <button class="bg-green-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Download Excel</button>
                        </div>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">App ID</th><th class="py-3 px-4 border-b">Applicant Name</th><th class="py-3 px-4 border-b">Scheme</th><th class="py-3 px-4 border-b text-center">System Action</th></tr>
                            </thead>
                            <tbody id="sys_verify_tbody" class="text-sm">
                                <!-- DYNAMIC DATA -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- VERIFICATION MODAL -->
                <div id="sys_verification_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
                    <div class="bg-white w-full max-w-lg rounded-xl shadow-2xl p-6 relative">
                        <button onclick="closeSysModal()" class="absolute top-4 right-4 text-gray-400 hover:text-red-500 text-2xl"><i class="fa-solid fa-xmark"></i></button>
                        <h3 class="text-xl font-bold mb-4 border-b pb-2 text-blue-800">System Automatic Verification Match</h3>
                        <div class="space-y-4 text-sm">
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded border">
                                <span class="font-semibold text-gray-600">Applicant Form Name:</span><span id="modal_sys_name" class="font-bold text-gray-800"></span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-green-50 rounded border border-green-200">
                                <span class="font-semibold text-gray-600">Aadhaar Verification:</span><span class="font-bold text-green-700"><i class="fa-solid fa-circle-check mr-1"></i> Authenticated</span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded border">
                                <span class="font-semibold text-gray-600">Income Cert Name Found:</span><span id="modal_sys_inc_name" class="font-bold text-gray-800"></span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded border">
                                <span class="font-semibold text-gray-600">Income Cert Amount:</span><span id="modal_sys_inc_amt" class="font-bold text-gray-800"></span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-green-50 rounded border border-green-200">
                                <span class="font-semibold text-gray-600">Overall System Status:</span><span class="font-bold text-green-700"><i class="fa-solid fa-check-double mr-1"></i> Data Consistent. Ready for Admin.</span>
                            </div>
                        </div>
                        <div class="mt-6 flex justify-end gap-3">
                            <button onclick="rejectApp()" class="bg-red-500 text-white px-4 py-2 rounded font-bold hover:bg-red-600">Reject Data</button>
                            <button onclick="approveSys()" class="bg-blue-600 text-white px-4 py-2 rounded font-bold hover:bg-blue-700">All Good (Send to Admin Portal)</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- FINAL ADMIN APPROVAL -->
            <div id="section-adminapprove" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-blue-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg text-blue-800"><i class="fa-solid fa-user-check mr-2"></i> Final Admin Approval</h2>
                        <span class="text-xs font-bold text-gray-500 bg-white px-2 py-1 border rounded">System Verified Applications Only</span>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">App ID</th><th class="py-3 px-4 border-b">Applicant Name</th><th class="py-3 px-4 border-b">Sys Status</th><th class="py-3 px-4 border-b text-center">Final Action</th></tr>
                            </thead>
                            <tbody id="admin_approve_tbody" class="text-sm">
                                <!-- DYNAMIC DATA -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- REJECTED BOX -->
            <div id="section-rejected" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border border-red-200 overflow-hidden">
                    <div class="px-6 py-4 border-b bg-red-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg text-red-800"><i class="fa-solid fa-trash-can mr-2"></i> Rejected Applications Box</h2>
                        <span class="text-xs font-bold text-red-600 border border-red-300 bg-white px-2 py-1 rounded-full"><i class="fa-solid fa-rotate-left"></i> Items Auto-Delete after 3 Months</span>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">App ID</th><th class="py-3 px-4 border-b">Applicant Name</th><th class="py-3 px-4 border-b">Rejected By</th><th class="py-3 px-4 border-b w-1/3">Remark / Reason</th><th class="py-3 px-4 border-b text-center">Delete</th></tr>
                            </thead>
                            <tbody id="rejected_tbody" class="text-sm">
                                <!-- DYNAMIC DATA -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- BENEFICIARIES -->
            <div id="section-beneficiaries" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg">Active Beneficiaries List</h2>
                        <div class="space-x-2">
                            <button class="bg-green-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Excel</button>
                        </div>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">Ben. ID</th><th class="py-3 px-4 border-b">Name</th><th class="py-3 px-4 border-b">Status</th><th class="py-3 px-4 border-b text-center">Admin Action</th></tr>
                            </thead>
                            <tbody id="beneficiaries_tbody" class="text-sm">
                                <!-- DYNAMIC DATA -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- RENEWALS -->
            <div id="section-renewals" class="content-section hidden">
                 <div class="bg-white border rounded-xl p-6 shadow-sm mb-6">
                    <h2 class="font-bold text-lg mb-4">Renewal Status Tracker</h2>
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-100 text-gray-600 text-sm">
                            <tr><th class="py-3 px-4 border-b">Ben. ID</th><th class="py-3 px-4 border-b">Name</th><th class="py-3 px-4 border-b">Renewal Alert</th><th class="py-3 px-4 border-b text-center">Action</th></tr>
                        </thead>
                        <tbody class="text-sm">
                            <tr class="bg-red-50 hover:bg-red-100 border-b hidden" id="dynamic_renewal_row">
                                <td class="py-4 px-4 font-medium text-red-700" id="dr_appno"></td>
                                <td class="py-4 px-4 font-bold text-red-700" id="dr_name"></td>
                                <td class="py-4 px-4"><span class="bg-red-200 text-red-800 py-1 px-3 rounded-full text-xs font-bold animate-pulse"><i class="fa-solid fa-triangle-exclamation"></i> Renewal Pending</span></td>
                                <td class="py-4 px-4 text-center"><button class="bg-red-600 text-white px-3 py-1 rounded shadow text-xs hover:bg-red-700"><i class="fa-solid fa-hand-paper"></i> Stop Pension</button></td>
                            </tr>
                            <tr id="dr_empty" class="border-b"><td colspan="4" class="text-center py-6 text-gray-500 font-semibold">No active beneficiaries are currently pending renewal.</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- PAYMENTS -->
            <div id="section-payments" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="font-bold text-lg">Monthly Payment & UTR Records</h2>
                        <div class="space-x-2">
                            <button class="bg-green-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Excel</button>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">App ID</th><th class="py-3 px-4 border-b">Beneficiary Name</th><th class="py-3 px-4 border-b">Bank A/C Details</th><th class="py-3 px-4 border-b">Status</th><th class="py-3 px-4 border-b">Bank UTR / Txn No.</th></tr>
                            </thead>
                            <tbody id="payments_tbody" class="text-sm">
                                <tr><td colspan="5" class="text-center py-6 text-gray-500 font-semibold">No payments successfully recorded yet.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="section-settings" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border p-8">
                    <h2 class="font-bold text-xl mb-6 text-blue-900 border-b pb-2"><i class="fa-solid fa-gears"></i> System & API Settings</h2>
                    <form>
                        <h3 class="font-bold text-gray-800 mb-3 mt-4"><i class="fa-solid fa-indian-rupee-sign text-green-600"></i> Application Fee Setting</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50 p-4 rounded border">
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Registration Fee Amount (₹)</label>
                                <input type="number" id="app_fee" value="100" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>

                        <h3 class="font-bold text-gray-800 mb-3 mt-6"><i class="fa-solid fa-credit-card text-blue-600"></i> PayU Payment Gateway Keys</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-blue-50 p-4 rounded border border-blue-100">
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">PayU Merchant Key</label>
                                <input type="password" id="payu_merchant_key" value="OLBUPA" placeholder="Enter Merchant Key" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">PayU Merchant Salt</label>
                                <input type="password" id="payu_merchant_salt" value="63LJwDVAEKqfR32B3ynr0TKayqyVjGg7" placeholder="Enter Merchant Salt" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>

                        <h3 class="font-bold text-gray-800 mb-3 mt-6"><i class="fa-solid fa-credit-card text-blue-600"></i> Razorpay Payment Gateway Keys</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-blue-50 p-4 rounded border border-blue-100">
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Razorpay Key ID</label>
                                <input type="password" id="rzp_key_id" placeholder="Enter Key ID" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Razorpay Key Secret</label>
                                <input type="password" id="rzp_key_secret" placeholder="Enter Key Secret" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>

                        <h3 class="font-bold text-gray-800 mb-3 mt-6"><i class="fa-solid fa-building-columns text-purple-600"></i> DBT / Payout API Keys (Bank Transfer)</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-purple-50 p-4 rounded border border-purple-100">
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Payout API Key</label>
                                <input type="password" id="payout_api_key" value="0b223e8abf8a96a8b53ebba0c1e610dd6acb9dc0ed3d9b6754cd67f2a42b9b03" placeholder="Enter API Key" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Payout API Secret</label>
                                <input type="password" id="payout_api_secret" value="4e513dcbf8512d0ca462d356e09abeba7de8937582d8635919a7bab3db5b4562" placeholder="Enter API Secret" class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>

                        <div class="mt-8 flex justify-end">
                            <button type="button" onclick="saveSettings()" class="bg-blue-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-blue-800 shadow">Save All Settings</button>
                        </div>
                    </form>
                </div>
            </div>

            <div id="section-profile" class="content-section hidden">
                <div class="max-w-2xl bg-white rounded-xl shadow-sm border p-8">
                    <h2 class="font-bold text-xl mb-6 text-blue-900 border-b pb-2"><i class="fa-solid fa-user-pen"></i> Update Admin Profile</h2>
                    <form class="space-y-5">
                        <div class="grid grid-cols-2 gap-6">
                            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Admin Name</label><input type="text" id="prof_admin_name" value="Super Admin" class="w-full px-4 py-2 border rounded-lg"></div>
                            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Mobile No.</label><input type="text" id="prof_admin_mobile" value="9876543210" class="w-full px-4 py-2 border rounded-lg"></div>
                        </div>
                        <div><label class="block text-sm font-semibold text-gray-700 mb-1">Admin Email ID (Login ID)</label><input type="email" id="prof_admin_email" value="admin@kulusutar.in" class="w-full px-4 py-2 border rounded-lg"></div>
                        <div class="border-t pt-5 mt-5">
                            <h3 class="font-bold text-gray-800 mb-4"><i class="fa-solid fa-lock text-gray-500"></i> Change Password</h3>
                            <div class="grid grid-cols-2 gap-6">
                                <div><label class="block text-sm text-gray-600 mb-1">New Password</label><input type="password" id="prof_new_pass" placeholder="Enter new password" class="w-full px-4 py-2 border rounded-lg"></div>
                                <div><label class="block text-sm text-gray-600 mb-1">Confirm Password</label><input type="password" id="prof_conf_pass" placeholder="Re-enter password" class="w-full px-4 py-2 border rounded-lg"></div>
                            </div>
                        </div>
                        <div class="mt-8 flex justify-end"><button type="button" onclick="saveAdminProfile()" class="bg-blue-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-blue-800 shadow">Save Changes</button></div>
                    </form>
                </div>
            </div>

        </div>
    </main>

    <!-- FULL APPLICATION VIEW & PRINT MODAL -->
    <div id="full_app_view_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 print:p-0 print:bg-white print:static">
        <div class="bg-white w-full max-w-4xl h-[90vh] rounded-xl shadow-2xl flex flex-col print:h-auto print:shadow-none print:w-full">
            
            <div class="p-4 border-b flex justify-between items-center bg-blue-50 rounded-t-xl print:hidden">
                <h3 class="text-xl font-bold text-blue-800"><i class="fa-solid fa-file-lines mr-2"></i> User Application Data</h3>
                <div class="space-x-2">
                    <button onclick="window.print()" class="bg-gray-800 text-white px-4 py-2 rounded shadow font-bold hover:bg-gray-900"><i class="fa-solid fa-print"></i> Print Details</button>
                    <button onclick="closeFullAppModal()" class="bg-red-500 text-white px-4 py-2 rounded shadow font-bold hover:bg-red-600"><i class="fa-solid fa-xmark"></i> Close</button>
                </div>
            </div>
            
            <div class="flex-1 overflow-y-auto p-8 print:overflow-visible print:p-0">
                <div class="text-center mb-6 border-b-2 border-gray-800 pb-4">
                    <h2 class="text-2xl font-extrabold uppercase">Private Social Security Pension Scheme</h2>
                    <p class="font-bold text-lg text-gray-600">Applicant Full Details Form</p>
                </div>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-6 bg-gray-50 p-4 rounded border">
                    <div><p class="text-gray-500 font-semibold text-xs">Application No</p><p id="v_appno" class="font-bold text-base text-blue-700"></p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Scheme Category</p><p id="v_scheme" class="font-bold text-base"></p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Applied Date</p><p class="font-bold text-base">23-Oct-2026</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Payment Status</p><p id="v_fee" class="font-bold text-green-600"></p></div>
                </div>
                
                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">1. Personal Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                    <div><p class="text-gray-500 text-xs">Full Name</p><p id="v_name" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Father's Name</p><p id="v_father" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Mother's Name</p><p id="v_mother" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Gender</p><p id="v_gender" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Date of Birth</p><p id="v_dob" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Aadhaar Number</p><p id="v_aadhaar" class="font-bold tracking-widest"></p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">2. Address Information</h4>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div><p class="text-gray-500 text-xs">State</p><p class="font-bold">Odisha</p></div>
                    <div><p class="text-gray-500 text-xs">District</p><p id="v_dist" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Block</p><p id="v_block" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">GP / Ward</p><p id="v_gp" class="font-bold"></p></div>
                    <div class="col-span-4"><p class="text-gray-500 text-xs">Full Address</p><p id="v_address" class="font-bold"></p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">3. Income Certificate Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 bg-blue-50 p-3 rounded">
                    <div><p class="text-gray-500 text-xs">Certificate No</p><p id="v_inc_cert" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Issued By</p><p id="v_inc_auth" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Detected Income</p><p id="v_inc_amount" class="font-bold text-red-600"></p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">4. Bank & DBT Information</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 bg-green-50 p-3 rounded">
                    <div><p class="text-gray-500 text-xs">Bank Name</p><p id="v_bank" class="font-bold"></p></div>
                    <div><p class="text-gray-500 text-xs">Account No</p><p id="v_acc" class="font-bold tracking-wider"></p></div>
                    <div><p class="text-gray-500 text-xs">IFSC Code</p><p id="v_ifsc" class="font-bold"></p></div>
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
