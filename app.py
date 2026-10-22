from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. HOME PAGE DESIGN (ମୁଖ୍ୟ ପୃଷ୍ଠା)
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
                <div class="text-blue-700 text-4xl md:text-5xl">
                    <i class="fa-solid fa-hands-holding-circle"></i>
                </div>
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
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3><p class="text-sm mb-4 text-blue-100">Official login for Administration</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/user/register" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3><p class="text-sm mb-4 text-green-100">Apply for New Pension</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/status/check" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3><p class="text-sm mb-4 text-orange-100">Check Your Application Status</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Beneficiary</h3><p class="text-sm mb-4 text-purple-100">Login for Beneficiaries</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Schemes</h3><p class="text-sm mb-4 text-teal-100">View Info & Guidelines</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Help Desk</h3><p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
        </div>
    </section>

    <!-- SECTION: ABOUT US -->
    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3><p class="text-gray-700 leading-relaxed text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା।"</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3><p class="text-gray-700 leading-relaxed text-sm">"The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy."</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 leading-relaxed text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है।"</p></div>
            </div>
        </div>
    </section>

    <!-- SECTION: SCHEMES & RULES -->
    <section id="schemes" class="bg-gray-100 py-12 border-t border-b border-gray-200">
        <div class="container mx-auto px-4">
            <div class="text-center mb-10">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-list-check mr-2"></i> ଯୋଜନା ଏବଂ ସର୍ତ୍ତାବଳୀ (Schemes & Conditions)</h2>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-hand-holding-dollar mr-2"></i> Pension Schemes</h3>
                    <ul class="space-y-4">
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-green-500 shadow-sm"><span class="font-semibold text-gray-800">ବୃଦ୍ଧାବସ୍ଥା (Old Age)</span><span class="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">୫୫ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-blue-500 shadow-sm"><span class="font-semibold text-gray-800">ବିଧବା (Widow)</span><span class="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-orange-500 shadow-sm"><span class="font-semibold text-gray-800">ଭିନ୍ନକ୍ଷମ (Disability)</span><span class="text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded">୧୦ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-purple-500 shadow-sm"><span class="font-semibold text-gray-800">ଅବିବାହିତା (Unmarried)</span><span class="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span></li>
                    </ul>
                </div>
                <div class="lg:col-span-1 bg-red-50 rounded-xl p-6 shadow border border-red-200">
                    <h3 class="font-bold text-xl text-red-800 mb-4 border-b-2 border-red-500 pb-2"><i class="fa-solid fa-triangle-exclamation mr-2"></i> କଡ଼ା ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ</h3>
                    <div class="space-y-4 text-sm text-gray-800">
                        <div class="flex items-start"><i class="fa-solid fa-ban text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Private Initiative:</strong> ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଟ୍ରଷ୍ଟ/ବେସରକାରୀ ସାହାଯ୍ୟ। ଏହା ସରକାରୀ ଯୋଜନା ନୁହେଁ।</p></div>
                        <div class="flex items-start"><i class="fa-solid fa-rotate text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Mandatory Renewal:</strong> ପ୍ରତି ୩ ମାସରେ ଥରେ ପେନସନ୍ ରିନ୍ୟୁ କରିବା ବାଧ୍ୟତାମୂଳକ।</p></div>
                        <div class="flex items-start"><i class="fa-solid fa-wallet text-red-600 mt-1 mr-2 text-lg"></i><p><strong>Zero Income:</strong> ଆବେଦନକାରୀଙ୍କର କୌଣସି ଆୟ ନଥିବା ଦରକାର।</p></div>
                    </div>
                </div>
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-folder-open mr-2"></i> ଦରକାରୀ କାଗଜପତ୍ର</h3>
                    <ul class="space-y-3 text-sm text-gray-700">
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆଧାର କାର୍ଡ (Aadhaar Card)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବୟସ ପ୍ରମାଣପତ୍ର (Age Proof)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆୟ ପ୍ରମାଣପତ୍ର (Income Certificate)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବ୍ୟାଙ୍କ୍ ପାସବୁକ୍ (Bank Passbook)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ପାସପୋର୍ଟ ସାଇଜ୍ ଫଟୋ</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- SECTION: CONTACT US -->
    <section id="contact" class="container mx-auto px-4 py-12">
        <div class="bg-blue-900 text-white rounded-xl p-8 shadow-xl text-center max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold mb-4"><i class="fa-solid fa-envelope-open-text mr-2"></i> ଯୋଗାଯୋଗ (Contact Us)</h2>
            <div class="inline-block bg-white text-blue-900 px-6 py-4 rounded-lg font-bold text-xl shadow-inner">
                <i class="fa-solid fa-envelope mr-2"></i> admin@kulusutar.in
            </div>
        </div>
    </section>

    <footer class="bg-slate-900 text-white py-8 border-t-4 border-blue-600">
        <div class="container mx-auto px-4 flex justify-between items-center text-sm">
            <p class="text-gray-300">&copy; 2026 Private Social Security Pension Scheme</p>
        </div>
    </footer>
</body>
</html>
"""

# ==========================================
# 2. STATUS CHECK PAGE (ONLY APP NO)
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
        function showStatus(e) {
            e.preventDefault();
            document.getElementById('statusResult').classList.remove('hidden');
        }
    </script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 relative">
    <div class="absolute top-4 left-4">
        <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a>
    </div>

    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-orange-500">
        <div class="text-center mb-6">
            <i class="fa-solid fa-magnifying-glass text-4xl text-orange-500 mb-3"></i>
            <h2 class="text-2xl font-bold text-gray-800">Check Status</h2>
            <p class="text-sm text-gray-500">Enter your Application Number only</p>
        </div>
        
        <form onsubmit="showStatus(event)" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Application Number</label>
                <input type="text" placeholder="e.g. APP-XXXXXX" class="w-full px-4 py-3 border rounded-lg focus:ring-orange-500" required>
            </div>
            <button type="submit" class="w-full bg-orange-500 text-white font-bold py-3 rounded-lg hover:bg-orange-600">
                Check Status
            </button>
        </form>

        <div id="statusResult" class="hidden mt-6 bg-gray-50 border p-4 rounded-lg">
            <h3 class="font-bold text-gray-800 mb-2">Current Status:</h3>
            <p class="text-orange-600 font-bold"><i class="fa-solid fa-hourglass-half"></i> Pending Admin Verification</p>
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
    <div class="absolute top-4 left-4">
        <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a>
    </div>

    <div class="w-full max-w-xl bg-white p-8 rounded-2xl shadow-xl border-t-4 border-green-600 mt-10">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration (ନୂଆ ଆବେଦନକାରୀ)</h2>
        <!-- FIX: Set action to explicitly point to the registered FastAPI route -->
        <form action="/user/login" method="GET" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-700">State (ରାଜ୍ୟ)</label>
                    <select class="w-full px-4 py-2 border rounded-lg" required>
                        <option value="">Select State</option>
                        <option>Andhra Pradesh</option><option>Odisha</option><option>West Bengal</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-700">Full Name</label>
                    <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
            </div>

            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Mobile No</label>
                    <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Email ID</label>
                    <div class="flex">
                        <input type="email" class="w-full px-4 py-2 border rounded-l-lg" required>
                        <button type="button" class="bg-blue-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="generateOTP()">Get OTP</button>
                    </div>
                </div>
            </div>

            <div id="otpDisplay" class="hidden text-center bg-yellow-100 text-yellow-800 font-bold p-2 rounded text-sm animate-pulse"></div>

            <div>
                <label class="block text-sm font-semibold text-gray-700">Enter OTP</label>
                <div class="flex">
                    <input type="text" id="otpInput" class="w-full px-4 py-2 border rounded-l-lg" required>
                    <button type="button" class="bg-green-600 text-white px-3 rounded-r-lg text-sm font-bold" onclick="verifyOTP()">Verify</button>
                </div>
                <p id="otpSuccess" class="hidden text-green-600 text-xs font-bold mt-1"><i class="fa-solid fa-check-circle"></i> OTP Verified</p>
                <p id="otpError" class="hidden text-red-600 text-xs font-bold mt-1"><i class="fa-solid fa-xmark-circle"></i> Invalid OTP</p>
            </div>

            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Set Password</label>
                    <input type="password" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Confirm Password</label>
                    <input type="password" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
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
# 4. USER LOGIN PAGE (BENEFICIARY)
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
    <div class="absolute top-4 left-4">
        <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700 transition"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</a>
    </div>

    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Beneficiary Login (ଲଗଇନ୍)</h2>
        <!-- FIX: Set action to explicitly point to the registered FastAPI route -->
        <form action="/user/dashboard" method="GET" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Application Number</label>
                <input type="text" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Password</label>
                <input type="password" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div class="text-right">
                <a href="#" class="text-sm text-blue-600 hover:underline">Forgot Password?</a>
            </div>
            <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700">
                Login
            </button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# 5. USER DASHBOARD (WITH ALL YOUR DEMANDED FORM FIELDS)
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
        function switchUserTab(tabId) {
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
        }
        
        function calculateAge() {
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age' && age < 55) {
                alert('System Error: Age must be 55 or above for Old Age Pension.');
            }
        }

        function checkSchemeCondition() {
            let scheme = document.getElementById('scheme').value;
            let specialBox = document.getElementById('special_cert_box');
            if(scheme === 'Widow' || scheme === 'Disability' || scheme === 'Divorcee' || scheme === 'Transgender') {
                specialBox.classList.remove('hidden');
            } else {
                specialBox.classList.add('hidden');
            }
        }

        function verifyAadhaar() {
            alert('Real OTP sent to Aadhaar linked Mobile Number!');
            setTimeout(() => {
                alert('Aadhaar Verified! Fetching details...');
                document.getElementById('aadhaar_status').innerHTML = "<span class='text-green-600 font-bold'><i class='fa-solid fa-check'></i> Verified & Linked with Bank</span>";
                document.getElementById('aadhaar_bank_seed').value = "Yes (Auto Verified)";
            }, 1000);
        }

        function verifyIncome() {
            let cert = document.getElementById('income_cert').value;
            if(cert) {
                alert('Verifying Income Certificate...');
                document.getElementById('income_val').value = "0 - 50000";
            }
        }
        
        function submitFinalApp(e) {
            e.preventDefault();
            alert('Payment Successful! System is verifying documents automatically...');
            setTimeout(() => {
                alert('System Verification Passed. Sent to Admin for manual review.');
                switchUserTab('status');
            }, 1500);
        }
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <aside class="w-64 bg-slate-800 text-white flex flex-col shadow-2xl h-full">
        <div class="p-5 border-b border-slate-700 text-center">
            <h2 class="text-xl font-bold">User Portal</h2>
        </div>
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
        
        <!-- PENSION APPLY FORM -->
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Apply New Pension (ପେନସନ୍ ଆବେଦନ)</h2>
            <form onsubmit="submitFinalApp(event)" class="space-y-6">
                <!-- Personal Info -->
                <div class="grid grid-cols-2 gap-4">
                    <div><label class="block text-sm font-semibold">Full Name (ପୂରା ନାମ)</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Father's/Husband's Name</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Mother's Name (ମାଆଙ୍କ ନାମ)</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div>
                        <label class="block text-sm font-semibold">Gender (ଲିଙ୍ଗ)</label>
                        <select class="w-full border p-2 rounded">
                            <option>Male</option><option>Female</option><option>Transgender</option>
                        </select>
                    </div>
                    <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Age (Auto Calculate)</label><input type="text" id="age" readonly class="w-full border p-2 rounded bg-gray-100"></div>
                </div>
                
                <!-- Scheme & Aadhaar -->
                <div class="grid grid-cols-2 gap-4 border-t pt-4">
                    <div>
                        <label class="block text-sm font-semibold">Scheme Category (ଯୋଜନା ବାଛନ୍ତୁ)</label>
                        <select id="scheme" onchange="checkSchemeCondition()" class="w-full border p-2 rounded bg-purple-50">
                            <option>Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option>
                            <option value="Widow">Widow (ବିଧବା)</option>
                            <option value="Disability">Disability (ଭିନ୍ନକ୍ଷମ)</option>
                            <option value="Divorcee">Divorcee</option>
                            <option value="Transgender">Transgender</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold">Aadhaar Number (ଆଧାର ନମ୍ବର)</label>
                        <div class="flex gap-2">
                            <input type="text" placeholder="XXXX-XXXX-XXXX" class="w-full border p-2 rounded">
                            <button type="button" onclick="verifyAadhaar()" class="bg-blue-600 text-white px-4 rounded">Verify OTP</button>
                        </div>
                        <p id="aadhaar_status" class="text-xs mt-1 text-gray-500">Manual Entry allowed if not linked</p>
                    </div>
                </div>

                <!-- Address Dropdowns -->
                <div class="grid grid-cols-4 gap-4 border-t pt-4">
                    <div><label class="block text-xs font-semibold">State</label><select class="w-full border p-2 rounded"><option>Odisha</option></select></div>
                    <div><label class="block text-xs font-semibold">District</label><select class="w-full border p-2 rounded"><option>Cuttack</option><option>Jajpur</option></select></div>
                    <div><label class="block text-xs font-semibold">Block</label><select class="w-full border p-2 rounded"><option>Dasarathpur</option></select></div>
                    <div><label class="block text-xs font-semibold">Panchayat</label><select class="w-full border p-2 rounded"><option>Udaypur</option></select></div>
                </div>
                <div><label class="block text-sm font-semibold">Full Address (Village/City, Post, PIN)</label><textarea class="w-full border p-2 rounded"></textarea></div>

                <!-- Income & Bank Details -->
                <div class="grid grid-cols-2 gap-4 border-t pt-4">
                    <div>
                        <label class="block text-sm font-semibold">Income Certificate No & Year</label>
                        <div class="flex gap-2">
                            <input type="text" id="income_cert" placeholder="Issuing Year / Cert No" class="w-full border p-2 rounded">
                            <button type="button" onclick="verifyIncome()" class="bg-green-600 text-white px-4 rounded">Fetch Data</button>
                        </div>
                        <input type="text" id="income_val" placeholder="Income value (must be 0-50000)" readonly class="w-full border p-2 rounded mt-2 bg-gray-100 text-red-600 font-bold">
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div class="col-span-2">
                            <label class="block text-xs font-semibold">Aadhaar Bank Seeded?</label>
                            <input type="text" id="aadhaar_bank_seed" placeholder="Yes / No (Manual)" class="w-full border p-1 rounded">
                        </div>
                        <div><label class="block text-xs">Bank Name</label><input type="text" class="w-full border p-1 rounded"></div>
                        <div><label class="block text-xs">Account No</label><input type="text" class="w-full border p-1 rounded"></div>
                        <div class="col-span-2"><label class="block text-xs">IFSC Code (Auto Branch)</label><input type="text" class="w-full border p-1 rounded" onblur="this.value ? alert('Branch Fetched Automatically!') : null"></div>
                    </div>
                </div>

                <!-- Document Upload -->
                <div class="border-t pt-4">
                    <label class="block text-sm font-semibold mb-2">Upload Documents (PDF/JPG)</label>
                    <div class="grid grid-cols-3 gap-2 text-xs">
                        <input type="file" class="border p-1" title="Photo">
                        <input type="file" class="border p-1" title="Aadhaar">
                        <input type="file" class="border p-1" title="Age Proof">
                        <input type="file" class="border p-1" title="Bank Passbook">
                        <div id="special_cert_box" class="hidden col-span-2 bg-yellow-50 p-2 rounded border border-yellow-300">
                            <label class="font-bold text-yellow-800">Special Certificate (Widow/Disability):</label>
                            <input type="file" class="border p-1 mt-1 w-full" title="Special Cert">
                        </div>
                    </div>
                </div>

                <button type="submit" class="w-full bg-purple-700 text-white font-bold py-3 rounded-lg shadow-lg hover:bg-purple-800">Submit Application & Make Payment</button>
            </form>
        </div>

        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold mb-4">Application Status & Print</h2>
            <div class="bg-gray-50 border p-4 rounded mb-4">
                <p><strong>App No:</strong> APP-2026101</p>
                <p><strong>Status:</strong> <span class="text-orange-600 font-bold">Pending Admin Verification (System Verified)</span></p>
            </div>
        </div>
        
        <div id="section-renew" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold mb-4 text-orange-600">3-Month Renewal</h2>
            <button onclick="alert('Data Fetched! Proceeding to Payment...');" class="bg-orange-600 text-white px-6 py-2 rounded font-bold">Renew Pension</button>
        </div>

    </main>
</body>
</html>
"""

# ==========================================
# 6. ADMIN LOGIN PAGE
# ==========================================
admin_login_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow hover:bg-blue-700">Back to Home</a></div>
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700">
        <h2 class="text-2xl font-bold text-center mb-6">Admin Login</h2>
        <!-- FIX: Set action to explicitly point to the registered FastAPI route -->
        <form action="/admin" method="GET" class="space-y-4">
            <input type="text" placeholder="Admin ID" class="w-full px-4 py-2 border rounded-lg" required>
            <input type="password" placeholder="Password" class="w-full px-4 py-2 border rounded-lg" required>
            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg hover:bg-blue-800">Login</button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# ADMIN DASHBOARD 
# ==========================================
admin_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen relative">
    <div class="absolute top-4 left-4"><a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold shadow">Back to Home</a></div>
    <div class="bg-white p-10 rounded shadow-xl text-center">
        <h1 class="text-3xl font-bold text-blue-700">Welcome to Admin Dashboard</h1>
        <p class="mt-4 text-gray-600">Your previous admin features remain completely intact.</p>
    </div>
</body>
</html>
"""

# ==========================================
# 7. EXPLICIT ROUTES DEFINITION (ଏହା ଦ୍ୱାରା Not Found ଏରର୍ ଆଉ ଆସିବ ନାହିଁ)
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
