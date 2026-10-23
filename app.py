from fastapi import FastAPI
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
            
            // Simulation logic for Demo
            if(appNo === "APP-REJECTED") {
                resBox.className = "mt-6 border p-4 rounded-lg bg-red-50 border-red-200";
                statIcon.className = "fa-solid fa-circle-xmark text-red-600 mr-1";
                statText.className = "text-red-600 font-bold";
                statText.innerText = "Rejected by Admin";
                statRemark.innerHTML = "<strong>Remark:</strong> Aadhaar Name and Income Certificate Name mismatch.";
                statRemark.classList.remove('hidden');
            } else {
                resBox.className = "mt-6 border p-4 rounded-lg bg-orange-50 border-orange-200";
                statIcon.className = "fa-solid fa-hourglass-half text-orange-600 mr-1";
                statText.className = "text-orange-600 font-bold";
                statText.innerText = "Pending System Verification";
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
            "Odisha": "Odia"
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
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    <div class="w-full max-w-xl bg-white p-8 rounded-2xl shadow-xl border-t-4 border-green-600 mt-10">
        <h2 id="dynamic_heading" class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration (ନୂଆ ଆବେଦନକାରୀ)</h2>
        <form action="/user/login" method="GET" class="space-y-4">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-700">State (ରାଜ୍ୟ)</label>
                    <select id="state_select" onchange="updateLanguageOptions()" class="w-full px-4 py-2 border rounded-lg" required>
                        <option value="">Select State</option>
                        <option value="Odisha">Odisha</option>
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
                    <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
            </div>

            <div class="flex gap-4">
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Mobile No</label><input type="text" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Email ID</label>
                    <div class="flex"><input type="email" class="w-full px-4 py-2 border rounded-l-lg" required><button type="button" class="bg-blue-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="generateOTP()">Get OTP</button></div>
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
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Set Password</label><input type="password" class="w-full px-4 py-2 border rounded-lg" required></div>
                <div class="w-1/2"><label class="block text-sm font-semibold text-gray-700">Confirm Password</label><input type="password" class="w-full px-4 py-2 border rounded-lg" required></div>
            </div>
            <button type="submit" id="submitBtn" disabled class="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700 opacity-50 cursor-not-allowed transition" onclick="alert('Registration Successful! Your Application No is: APP-2026101.')">
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
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a></div>
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Beneficiary Login (ଲଗଇନ୍)</h2>
        <form action="/user/dashboard" method="GET" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Application Number</label>
                <input type="text" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Password</label>
                <input type="password" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
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
        };

        function populateDistricts() {
            let state = "Odisha"; 
            let distSelect = document.getElementById("district");
            let blockSelect = document.getElementById("block");
            
            distSelect.innerHTML = "<option value=''>Select</option>";
            blockSelect.innerHTML = "<option value=''>Select</option>";

            if(state && locationData[state]) {
                for(let dist in locationData[state]) {
                    distSelect.innerHTML += `<option value='${dist}'>${dist}</option>`;
                }
            }
        }

        function populateBlocks() {
            let state = "Odisha";
            let dist = document.getElementById("district").value;
            let blockSelect = document.getElementById("block");
            
            blockSelect.innerHTML = "<option value=''>Select</option>";

            if(state && dist && locationData[state][dist]) {
                let blocks = locationData[state][dist];
                for(let i=0; i<blocks.length; i++) {
                    blockSelect.innerHTML += `<option value='${blocks[i]}'>${blocks[i]}</option>`;
                }
            }
        }

        function switchUserTab(tabId) {
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
        }
        
        function calculateAge() {
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age' && age < 55) { alert('System Error: Age must be 55 or above for Old Age Pension.'); }
        }

        function checkSchemeCondition() {
            let scheme = document.getElementById('scheme').value;
            let specialBox = document.getElementById('special_cert_box');
            if(scheme === 'Widow' || scheme === 'Disability' || scheme === 'Divorcee' || scheme === 'Transgender') {
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
                    document.getElementById("bank_name_display").innerText = data.BANK;
                    document.getElementById("branch_name_display").innerText = data.BRANCH;
                } else {
                    alert("Invalid IFSC Code");
                    document.getElementById("bank_name_display").innerText = "--";
                    document.getElementById("branch_name_display").innerText = "--";
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

                    document.getElementById('full_name').value = data.name;
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
            let amount = "100.00";
            let productinfo = "PensionApplication";
            let firstname = document.getElementById('full_name').value || "User";
            let email = "user@example.com"; 
            let phone = "9876543210";
            let surl = window.location.origin + "/status/check";
            let furl = window.location.origin + "/status/check";

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

    <main class="flex-1 overflow-y-auto p-6">
        
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow print:hidden">
            
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
                
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-semibold">Full Name (ପୂରା ନାମ)</label>
                        <input type="text" id="full_name" class="w-full border-b border-gray-300 p-2 outline-none font-bold text-blue-800 bg-transparent" required>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-blue-600">Profile Photo <i class="fa-solid fa-camera"></i></label>
                        <input type="file" class="w-full border-b border-gray-300 p-2 text-sm outline-none bg-transparent" accept="image/*" required>
                    </div>
                    <div><label class="block text-sm font-semibold">Father's/Husband's Name</label><input type="text" id="father_name" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                    <div><label class="block text-sm font-semibold">Mother's Name (ମାଆଙ୍କ ନାମ)</label><input type="text" id="mother_name" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                    <div>
                        <label class="block text-sm font-semibold">Gender (ଲିଙ୍ଗ)</label>
                        <select class="w-full border-b border-gray-300 p-2 outline-none bg-transparent"><option>Male</option><option>Female</option><option>Transgender</option></select>
                    </div>
                    <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border-b border-gray-300 p-2 outline-none bg-transparent" required></div>
                    <div><label class="block text-sm font-semibold">Age (Auto Calculate)</label><input type="text" id="age" readonly class="w-full border-b border-gray-300 p-2 outline-none bg-gray-50"></div>
                </div>
                
                <div class="grid grid-cols-2 gap-6 border-t pt-4">
                    <div>
                        <label class="block text-sm font-semibold mb-2">Scheme Category (ଯୋଜନା ବାଛନ୍ତୁ)</label>
                        <select id="scheme" onchange="checkSchemeCondition()" class="w-full border p-2 rounded bg-purple-50">
                            <option value="Old Age">Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option><option value="Widow">Widow (ବିଧବା)</option><option value="Disability">Disability (ଭିନ୍ନକ୍ଷମ)</option><option value="Unmarried">Unmarried (ଅବିବାହିତା)</option><option value="Divorcee">Divorcee (ଛାଡପତ୍ର ପାଇଥିବା)</option><option value="Transgender">Transgender (କିନ୍ନର)</option>
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
                        <div class="col-span-3 text-right">
                            <button type="button" onclick="verifyIncome()" class="bg-green-600 text-white font-bold px-6 py-2 rounded hover:bg-green-700 shadow"><i class="fa-solid fa-cloud-arrow-down mr-2"></i>Fetch Data</button>
                        </div>
                        
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
                        <div class="text-center">
                            <p class="text-sm text-gray-500">Bank Name: <span id="bank_name_display" class="font-bold text-gray-800 text-base">--</span></p>
                        </div>
                        <div class="text-center">
                            <p class="text-sm text-gray-500">Branch Name: <span id="branch_name_display" class="font-bold text-gray-800 text-base">--</span></p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                        <div>
                            <label class="block text-sm text-gray-600 mb-1">Account Holder Name</label>
                            <input type="text" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent">
                        </div>
                        <div>
                            <label class="block text-sm text-gray-600 mb-1">Account Number <span class="text-red-500">*</span></label>
                            <input type="text" class="w-full border-b border-gray-300 outline-none p-2 bg-transparent" required>
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
                        <i class="fa-solid fa-lock mr-2"></i> Pay Now with PayU
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

        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <div class="print:hidden">
                <h2 class="text-3xl font-bold mb-6 text-green-700 border-b pb-2"><i class="fa-solid fa-circle-check"></i> Application Submitted & Paid</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-green-50 border-l-4 border-green-500 p-5 rounded shadow-sm">
                        <p class="text-gray-500 text-sm font-semibold uppercase">Application Number</p>
                        <p class="text-2xl font-bold text-gray-800">APP-2026101</p>
                        <p class="mt-2 text-sm"><strong>Status:</strong> <span class="bg-orange-200 text-orange-800 py-1 px-2 rounded font-bold text-xs">Pending Admin Verification</span></p>
                    </div>
                    <div class="bg-blue-50 border-l-4 border-blue-500 p-5 rounded shadow-sm">
                        <p class="text-gray-500 text-sm font-semibold uppercase">Payment Reference (PayU)</p>
                        <p class="text-xl font-bold text-gray-800">TXN-9843729910</p>
                        <p class="mt-2 text-sm"><strong>Amount Paid:</strong> <span class="text-green-700 font-bold">₹100.00</span> (Success)</p>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row gap-4 justify-center mt-6">
                    <button type="button" onclick="window.print()" class="bg-gray-800 text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:bg-gray-900 transition flex items-center justify-center">
                        <i class="fa-solid fa-print mr-2 text-xl"></i> Print Payment Receipt
                    </button>
                    <button type="button" onclick="window.print()" class="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg hover:bg-blue-700 transition flex items-center justify-center">
                        <i class="fa-solid fa-file-pdf mr-2 text-xl"></i> View & Print Application PDF
                    </button>
                </div>
            </div>

            <div class="hidden print:block border-2 border-gray-800 p-8 rounded-lg mt-10 relative">
                <div class="absolute top-4 right-4 border border-gray-400 p-1 w-24 h-32 text-center text-xs text-gray-500 flex items-center justify-center">Passport Photo</div>
                <div class="text-center border-b-2 border-gray-800 pb-4 mb-6">
                    <h1 class="text-2xl font-extrabold uppercase">Private Social Security Pension Scheme</h1>
                    <p class="font-bold text-lg">Application & Payment Receipt</p>
                </div>
                <div class="grid grid-cols-2 gap-4 text-sm mb-6">
                    <div><strong>Application No:</strong> APP-2026101</div>
                    <div><strong>Transaction ID:</strong> TXN-9843729910</div>
                    <div><strong>Applicant Name:</strong> Kulu Sutar</div>
                    <div><strong>Payment Status:</strong> SUCCESS (₹100)</div>
                    <div><strong>Scheme Category:</strong> Old Age Pension</div>
                    <div><strong>Date & Time:</strong> 23 Oct 2026</div>
                </div>
                <div class="border-t border-gray-400 pt-4 text-xs text-justify">
                    <strong>Declaration:</strong> I declare that all information provided is true and my annual income is strictly below Rs. 50,000. If my income is found to exceed 50,000 or if any data is false, Admin holds the right to reject my application without prior notice. I agree to all terms and conditions.
                </div>
                <div class="mt-16 flex justify-between">
                    <div class="border-t border-gray-800 pt-1 w-48 text-center font-bold">Applicant Signature</div>
                    <div class="border-t border-gray-800 pt-1 w-48 text-center font-bold">Admin Authority (Seal)</div>
                </div>
            </div>

        </div>
        
        <div id="section-renew" class="content-section hidden bg-white p-6 rounded-xl shadow print:hidden">
            <h2 class="text-2xl font-bold mb-4 text-orange-600">3-Month Renewal</h2>
            <button onclick="alert('Data Fetched! Proceeding to Payment...');" class="bg-orange-600 text-white px-6 py-2 rounded font-bold">Renew Pension</button>
        </div>
    </main>
</body>
</html>
"""

# ==========================================
# 6. FULL ADMIN DASHBOARD (UPDATED STRICT LOGIN & VIEW OPTION)
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

        // STRICT LOGIN AUTHENTICATION
        function handleAdminLogin(event) {
            event.preventDefault();
            let adminId = document.getElementById('admin_id').value;
            let adminPass = document.getElementById('password').value;

            if(adminId === 'admin@kulusutar.in' && adminPass === 'Admin@123') {
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
            if(localStorage.getItem('payout_api_key')) document.getElementById('payout_api_key').value = localStorage.getItem('payout_api_key');
            if(localStorage.getItem('payout_api_secret')) document.getElementById('payout_api_secret').value = localStorage.getItem('payout_api_secret');
        };

        function saveSettings() {
            localStorage.setItem('app_fee', document.getElementById('app_fee').value);
            localStorage.setItem('payu_merchant_key', document.getElementById('payu_merchant_key').value);
            localStorage.setItem('payu_merchant_salt', document.getElementById('payu_merchant_salt').value);
            localStorage.setItem('payout_api_key', document.getElementById('payout_api_key').value);
            localStorage.setItem('payout_api_secret', document.getElementById('payout_api_secret').value);
            alert('Settings Saved Successfully!');
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

        function verifySysDoc() {
            document.getElementById('sys_verification_modal').classList.remove('hidden');
        }
        
        function closeSysModal() {
            document.getElementById('sys_verification_modal').classList.add('hidden');
        }

        function viewFullApplication(appId) {
            document.getElementById('full_app_view_modal').classList.remove('hidden');
        }

        function closeFullAppModal() {
            document.getElementById('full_app_view_modal').classList.add('hidden');
        }

        function rejectAppWithRemark() {
            let reason = prompt("Please enter the reason for rejection (Remark):");
            if (reason != null && reason != "") {
                alert("Application Rejected and Moved to Rejected Box with Remark: " + reason);
                document.getElementById('row_app_9082').classList.add('hidden');
                document.getElementById('sys_verification_modal').classList.add('hidden');
            }
        }

        function deleteRejectedRow(rowId) {
            if(confirm("Are you sure you want to permanently delete this rejected application data?")) {
                document.getElementById(rowId).classList.add('hidden');
            }
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
                <span class="text-sm font-medium">Welcome, <strong>Admin</strong></span>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-6 bg-gray-50 print:hidden">
            
            <!-- DASHBOARD -->
            <div id="section-dashboard" class="content-section">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-blue-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Total Applications</p><h3 class="text-2xl font-bold text-blue-700">1,245</h3></div>
                        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-file-lines"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-green-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Approved Pension (Active)</p><h3 class="text-2xl font-bold text-green-700">850</h3></div>
                        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-check-circle"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-orange-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Pending Verification</p><h3 class="text-2xl font-bold text-orange-700">310</h3></div>
                        <div class="w-12 h-12 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-hourglass-half"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-red-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500 font-semibold">Total Rejected</p><h3 class="text-2xl font-bold text-red-700">85</h3></div>
                        <div class="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-ban"></i></div>
                    </div>
                </div>
            </div>

            <!-- SYSTEM VERIFICATION (LEVEL 1) -->
            <div id="section-sysverify" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-orange-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg text-orange-800"><i class="fa-solid fa-microchip mr-2"></i> System Verification Stage</h2>
                        <div class="space-x-2">
                            <button onclick="alert('Downloading Data to Excel...')" class="bg-green-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Download Excel</button>
                            <button onclick="alert('Downloading Data to PDF...')" class="bg-red-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-red-700"><i class="fa-solid fa-file-pdf mr-1"></i> Download PDF</button>
                        </div>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">App ID</th><th class="py-3 px-4 border-b">Applicant Name</th><th class="py-3 px-4 border-b">Scheme</th><th class="py-3 px-4 border-b text-center">System Action</th></tr>
                            </thead>
                            <tbody class="text-sm">
                                <tr id="row_app_9082" class="hover:bg-gray-50 border-b">
                                    <td class="py-4 px-4 font-medium text-blue-600">#APP-9082</td><td class="py-4 px-4 font-bold">Rama Chandra Das</td><td class="py-4 px-4">Old Age Pension</td>
                                    <td class="py-4 px-4 flex justify-center space-x-2 items-center">
                                        <!-- ADDED VIEW BUTTON -->
                                        <button onclick="viewFullApplication('#APP-9082')" class="bg-purple-600 text-white px-3 py-1 rounded shadow hover:bg-purple-700 text-xs font-bold"><i class="fa-solid fa-eye"></i> View</button>
                                        <button onclick="verifySysDoc()" class="bg-blue-500 text-white px-3 py-1 rounded shadow hover:bg-blue-600 text-xs font-bold"><i class="fa-solid fa-magnifying-glass"></i> Sys Auto Check</button>
                                        <button class="bg-green-600 text-white px-3 py-1 rounded shadow hover:bg-green-700 text-xs font-bold"><i class="fa-solid fa-check"></i> Approve</button>
                                        <button onclick="rejectAppWithRemark()" class="bg-red-500 text-white px-3 py-1 rounded shadow hover:bg-red-600 text-xs font-bold"><i class="fa-solid fa-xmark"></i> Reject</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- VERIFICATION MODAL -->
                <div id="sys_verification_modal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
                    <div class="bg-white w-full max-w-lg rounded-xl shadow-2xl p-6 relative">
                        <button onclick="closeSysModal()" class="absolute top-4 right-4 text-gray-400 hover:text-red-500 text-2xl"><i class="fa-solid fa-xmark"></i></button>
                        <h3 class="text-xl font-bold mb-4 border-b pb-2 text-blue-800">System Match Analysis</h3>
                        <div class="space-y-4 text-sm">
                            <div class="flex justify-between items-center p-2 bg-gray-50 rounded border">
                                <span class="font-semibold text-gray-600">Applicant Form Name:</span><span class="font-bold text-gray-800">Rama Chandra Das</span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-green-50 rounded border border-green-200">
                                <span class="font-semibold text-gray-600">Aadhaar Card Name Match:</span><span class="font-bold text-green-700"><i class="fa-solid fa-circle-check mr-1"></i> Match (99%)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-green-50 rounded border border-green-200">
                                <span class="font-semibold text-gray-600">Income Cert Name Match:</span><span class="font-bold text-green-700"><i class="fa-solid fa-circle-check mr-1"></i> Match (100%)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 bg-green-50 rounded border border-green-200">
                                <span class="font-semibold text-gray-600">Age Proof Document Check:</span><span class="font-bold text-green-700"><i class="fa-solid fa-circle-check mr-1"></i> Verified (>55 Yrs)</span>
                            </div>
                        </div>
                        <div class="mt-6 flex justify-end gap-3">
                            <button onclick="rejectAppWithRemark()" class="bg-red-500 text-white px-4 py-2 rounded font-bold hover:bg-red-600">Reject Data</button>
                            <button onclick="closeSysModal()" class="bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700">All Good (Close)</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- FINAL ADMIN APPROVAL (LEVEL 2) -->
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
                            <tbody class="text-sm">
                                <tr class="hover:bg-gray-50 border-b">
                                    <td class="py-4 px-4 font-medium text-blue-600">#APP-8051</td><td class="py-4 px-4 font-bold">Harihar Nayak</td>
                                    <td class="py-4 px-4"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> System Approved</span></td>
                                    <td class="py-4 px-4 flex justify-center space-x-2 items-center">
                                        <!-- ADDED VIEW BUTTON -->
                                        <button onclick="viewFullApplication('#APP-8051')" class="bg-purple-600 text-white px-4 py-1 rounded shadow hover:bg-purple-700 font-bold"><i class="fa-solid fa-eye"></i> View Details</button>
                                        <button onclick="alert('Application Finally Approved and Added to Beneficiary List!');" class="bg-green-600 text-white px-4 py-1 rounded shadow hover:bg-green-700 font-bold"><i class="fa-solid fa-signature"></i> Final Approve</button>
                                        <button onclick="rejectAppWithRemark()" class="bg-red-500 text-white px-4 py-1 rounded shadow hover:bg-red-600 font-bold"><i class="fa-solid fa-ban"></i> Reject</button>
                                    </td>
                                </tr>
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
                            <tbody class="text-sm">
                                <tr id="rej_row_1" class="hover:bg-red-50 border-b">
                                    <td class="py-4 px-4 font-medium text-red-600">#APP-REJECTED</td><td class="py-4 px-4 font-bold text-gray-800">Demo User</td>
                                    <td class="py-4 px-4 text-gray-600 font-semibold">Admin</td>
                                    <td class="py-4 px-4 text-gray-600 italic">Aadhaar Name and Income Certificate Name mismatch.</td>
                                    <td class="py-4 px-4 text-center">
                                        <button onclick="deleteRejectedRow('rej_row_1')" class="bg-gray-200 text-red-600 px-3 py-1 rounded shadow hover:bg-red-600 hover:text-white transition text-xs font-bold"><i class="fa-solid fa-trash"></i> Delete Data</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- BENEFICIARIES -->
            <div id="section-beneficiaries" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <!-- EXCEL PDF ADDED -->
                    <div class="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg">Active Beneficiaries List</h2>
                        <div class="space-x-2">
                            <button onclick="alert('Downloading User Data to Excel...')" class="bg-green-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Download Excel</button>
                            <button onclick="alert('Downloading User Data to PDF...')" class="bg-red-600 text-white px-3 py-1 rounded text-sm font-semibold hover:bg-red-700"><i class="fa-solid fa-file-pdf mr-1"></i> Download PDF</button>
                        </div>
                    </div>
                    <div class="overflow-x-auto p-4">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr><th class="py-3 px-4 border-b">Ben. ID</th><th class="py-3 px-4 border-b">Name</th><th class="py-3 px-4 border-b">Status</th><th class="py-3 px-4 border-b text-center">Admin Action</th></tr>
                            </thead>
                            <tbody class="text-sm">
                                <tr class="hover:bg-gray-50 border-b">
                                    <td class="py-4 px-4 font-medium text-blue-600">#BEN-101</td><td class="py-4 px-4 font-bold">Harihar Nayak</td>
                                    <td class="py-4 px-4"><span class="bg-green-100 text-green-800 py-1 px-3 rounded-full text-xs font-semibold">Active</span></td>
                                    <td class="py-4 px-4 text-center space-x-2">
                                        <button class="bg-orange-500 text-white px-3 py-1 rounded shadow text-xs"><i class="fa-solid fa-pause"></i> Hold</button>
                                        <button class="bg-red-600 text-white px-3 py-1 rounded shadow text-xs"><i class="fa-solid fa-hand-paper"></i> Stop</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- RENEWALS -->
            <div id="section-renewals" class="content-section hidden">
                 <div class="bg-white border rounded-xl p-6 shadow-sm mb-6">
                    <h2 class="font-bold text-lg mb-4">Renewal Status</h2>
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-100 text-gray-600 text-sm">
                            <tr><th class="py-3 px-4 border-b">Ben. ID</th><th class="py-3 px-4 border-b">Name</th><th class="py-3 px-4 border-b">Status / Alert</th><th class="py-3 px-4 border-b text-center">Action</th></tr>
                        </thead>
                        <tbody class="text-sm">
                            <tr class="bg-red-50 hover:bg-red-100 border-b">
                                <td class="py-4 px-4 font-medium text-red-700">#BEN-089</td><td class="py-4 px-4 font-bold text-red-700">Bimala Das</td>
                                <td class="py-4 px-4"><span class="bg-red-200 text-red-800 py-1 px-3 rounded-full text-xs font-bold animate-pulse"><i class="fa-solid fa-triangle-exclamation"></i> Overdue (3+ Months)</span></td>
                                <td class="py-4 px-4 text-center"><button class="bg-red-600 text-white px-3 py-1 rounded shadow text-xs"><i class="fa-solid fa-hand-paper"></i> Stop Pension</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- PAYMENTS -->
            <div id="section-payments" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="font-bold text-lg">Monthly Payment Records</h2>
                        <div class="space-x-2">
                            <button onclick="alert('Downloading Payments Data to Excel...')" class="bg-green-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-green-700"><i class="fa-solid fa-file-excel mr-1"></i> Excel</button>
                            <button onclick="alert('Downloading Payments Data to PDF...')" class="bg-red-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-red-700"><i class="fa-solid fa-file-pdf mr-1"></i> PDF</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SETTINGS SECTION -->
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
                            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Admin Name</label><input type="text" value="Super Admin" class="w-full px-4 py-2 border rounded-lg"></div>
                            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Mobile No.</label><input type="text" value="9876543210" class="w-full px-4 py-2 border rounded-lg"></div>
                        </div>
                        <div><label class="block text-sm font-semibold text-gray-700 mb-1">Admin Email ID (Login ID)</label><input type="email" value="admin@kulusutar.in" class="w-full px-4 py-2 border rounded-lg"></div>
                        <div class="border-t pt-5 mt-5">
                            <h3 class="font-bold text-gray-800 mb-4"><i class="fa-solid fa-lock text-gray-500"></i> Change Password</h3>
                            <div class="grid grid-cols-2 gap-6">
                                <div><label class="block text-sm text-gray-600 mb-1">New Password</label><input type="password" placeholder="Enter new password" class="w-full px-4 py-2 border rounded-lg"></div>
                                <div><label class="block text-sm text-gray-600 mb-1">Confirm Password</label><input type="password" placeholder="Re-enter password" class="w-full px-4 py-2 border rounded-lg"></div>
                            </div>
                        </div>
                        <div class="mt-8 flex justify-end"><button type="button" class="bg-blue-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-blue-800 shadow">Save Changes</button></div>
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
                    <div><p class="text-gray-500 font-semibold text-xs">Application No</p><p class="font-bold text-base text-blue-700">APP-9082</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Scheme Category</p><p class="font-bold text-base">Old Age Pension</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Applied Date</p><p class="font-bold text-base">23-Oct-2026</p></div>
                    <div><p class="text-gray-500 font-semibold text-xs">Payment Status</p><p class="font-bold text-green-600"><i class="fa-solid fa-check-circle"></i> Paid (₹100)</p></div>
                </div>
                
                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">1. Personal Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                    <div><p class="text-gray-500 text-xs">Full Name</p><p class="font-bold">Rama Chandra Das</p></div>
                    <div><p class="text-gray-500 text-xs">Father's Name</p><p class="font-bold">Harihar Das</p></div>
                    <div><p class="text-gray-500 text-xs">Mother's Name</p><p class="font-bold">Sita Das</p></div>
                    <div><p class="text-gray-500 text-xs">Gender</p><p class="font-bold">Male</p></div>
                    <div><p class="text-gray-500 text-xs">Date of Birth</p><p class="font-bold">15-Aug-1950 (76 Yrs)</p></div>
                    <div><p class="text-gray-500 text-xs">Aadhaar Number</p><p class="font-bold tracking-widest">XXXX-XXXX-9876</p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">2. Address Information</h4>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div><p class="text-gray-500 text-xs">State</p><p class="font-bold">Odisha</p></div>
                    <div><p class="text-gray-500 text-xs">District</p><p class="font-bold">Bhadrak</p></div>
                    <div><p class="text-gray-500 text-xs">Block</p><p class="font-bold">Dhamanagar</p></div>
                    <div><p class="text-gray-500 text-xs">GP / Ward</p><p class="font-bold">Kalyani</p></div>
                    <div class="col-span-4"><p class="text-gray-500 text-xs">Full Address</p><p class="font-bold">At- Kalyani, Po- Dhamanagar, Dist- Bhadrak, Pin- 756117</p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">3. Income Certificate Details</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 bg-blue-50 p-3 rounded">
                    <div><p class="text-gray-500 text-xs">Certificate No</p><p class="font-bold">E-INC/2025/111222</p></div>
                    <div><p class="text-gray-500 text-xs">Issued By</p><p class="font-bold">Tahasildar, Bhubaneswar</p></div>
                    <div><p class="text-gray-500 text-xs">Detected Income</p><p class="font-bold text-red-600">Rs. 35,000/-</p></div>
                </div>

                <h4 class="font-bold text-lg border-b mb-3 text-gray-800">4. Bank & DBT Information</h4>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 bg-green-50 p-3 rounded">
                    <div><p class="text-gray-500 text-xs">Bank Name</p><p class="font-bold">State Bank of India</p></div>
                    <div><p class="text-gray-500 text-xs">Account No</p><p class="font-bold tracking-wider">30987654321</p></div>
                    <div><p class="text-gray-500 text-xs">IFSC Code</p><p class="font-bold">SBIN0001234</p></div>
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

@app.get("/user/register", response_class=HTMLResponse)
async def user_register_page():
    return user_register_design

@app.get("/user/login", response_class=HTMLResponse)
async def user_login_page():
    return user_login_design

@app.get("/user/dashboard", response_class=HTMLResponse)
async def user_dashboard_page():
    return user_dashboard_design

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    return admin_login_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page():
    return admin_design
