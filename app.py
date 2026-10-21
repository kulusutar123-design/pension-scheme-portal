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
        .card-hover:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); transition: all 0.3s ease; }
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
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition duration-300 flex items-center w-max">View Schemes <i class="fa-solid fa-arrow-down ml-2"></i></a>
            </div>
        </div>
    </section>

    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3><p class="text-sm mb-4 text-blue-100">Official login for Administration</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <!-- NEW LINK: Pointing to /apply -->
            <a href="/apply" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3><p class="text-sm mb-4 text-green-100">Apply for New Pension</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3><p class="text-sm mb-4 text-orange-100">Check Your Application Status</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
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

    <!-- ABOUT, SCHEMES, CONTACT (KEPT INTACT AS REQUESTED) -->
    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <h2 class="text-3xl font-bold text-blue-900 text-center mb-8"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3><p class="text-gray-700 text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା।"</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3><p class="text-gray-700 text-sm">"The Private Social Security Pension Scheme is a private initiative providing financial support and respect to the needy."</p></div>
                <div class="bg-blue-50 p-6 rounded-lg border shadow-sm"><h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3><p class="text-gray-700 text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक निजी पहल है। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है।"</p></div>
            </div>
        </div>
    </section>

    <section id="schemes" class="bg-gray-100 py-12 border-t border-b border-gray-200">
        <div class="container mx-auto px-4">
            <h2 class="text-3xl font-bold text-blue-900 text-center mb-10"><i class="fa-solid fa-list-check mr-2"></i> ଯୋଜନା ଏବଂ ସର୍ତ୍ତାବଳୀ (Schemes & Conditions)</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2">Pension Schemes</h3>
                    <ul class="space-y-4">
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-green-500"><span class="font-semibold text-gray-800">ବୃଦ୍ଧାବସ୍ଥା (Old Age)</span><span class="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">୫୫ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-blue-500"><span class="font-semibold text-gray-800">ବିଧବା (Widow)</span><span class="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span></li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-orange-500"><span class="font-semibold text-gray-800">ଭିନ୍ନକ୍ଷମ (Disability)</span><span class="text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded">୧୦ ରୁ ୧୦୦ ବର୍ଷ</span></li>
                    </ul>
                </div>
                <div class="lg:col-span-1 bg-red-50 rounded-xl p-6 shadow border border-red-200">
                    <h3 class="font-bold text-xl text-red-800 mb-4 border-b-2 border-red-500 pb-2">କଡ଼ା ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ</h3>
                    <div class="space-y-4 text-sm text-gray-800">
                        <p><strong>Private Initiative:</strong> ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ସାହାଯ୍ୟ। ଏହା ସରକାରୀ ଯୋଜନା ନୁହେଁ।</p>
                        <p><strong>Mandatory Renewal:</strong> ପ୍ରତି ୩ ମାସରେ ଥରେ ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ।</p>
                        <p><strong>Zero Income:</strong> ଆବେଦନକାରୀଙ୍କର କୌଣସି ଆୟ ନଥିବା ଦରକାର।</p>
                    </div>
                </div>
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2">ଦରକାରୀ କାଗଜପତ୍ର</h3>
                    <ul class="space-y-3 text-sm text-gray-700">
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆଧାର କାର୍ଡ (Aadhaar Card)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆୟ ପ୍ରମାଣପତ୍ର (Income Certificate)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବ୍ୟାଙ୍କ୍ ପାସବୁକ୍ (Bank Passbook)</li>
                    </ul>
                </div>
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
# 2. NEW REGISTRATION & PENSION APPLY PAGE
# ==========================================
pension_apply_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pension Application & Registration</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function selectMethod(method) {
            document.getElementById('method-selection').classList.add('hidden');
            document.getElementById('registration-form').classList.remove('hidden');
            
            if(method === 'otp') {
                document.getElementById('otp-section').classList.remove('hidden');
                document.getElementById('manual-section').classList.add('hidden');
                document.getElementById('reg-title').innerText = "Aadhaar OTP Registration";
            } else {
                document.getElementById('otp-section').classList.add('hidden');
                document.getElementById('manual-section').classList.remove('hidden');
                document.getElementById('reg-title').innerText = "Manual Registration (No Linked Mobile)";
            }
        }

        function sendOTP() {
            document.getElementById('otp-verify-box').classList.remove('hidden');
            alert("OTP Sent to Aadhaar linked mobile number!");
        }

        function verifyAndSetPassword() {
            document.getElementById('set-password-box').classList.remove('hidden');
            alert("OTP Verified Successfully!");
        }

        function completeRegistration() {
            document.getElementById('registration-step').classList.add('hidden');
            document.getElementById('application-step').classList.remove('hidden');
            alert("Registration Complete! Your Aadhaar Number is your User ID.");
        }
    </script>
</head>
<body class="bg-gray-100 font-sans text-gray-800">

    <header class="bg-blue-900 text-white shadow-md py-4">
        <div class="container mx-auto px-4 flex justify-between items-center">
            <h1 class="text-xl font-bold"><i class="fa-solid fa-pen-to-square mr-2"></i> New Pension Application</h1>
            <a href="/" class="text-blue-200 hover:text-white"><i class="fa-solid fa-house"></i> Back to Home</a>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8 max-w-4xl">
        
        <!-- STEP 1: REGISTRATION -->
        <div id="registration-step" class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-green-600">
            
            <div id="method-selection" class="text-center">
                <h2 class="text-2xl font-bold text-gray-800 mb-6">Choose Registration Method</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <button onclick="selectMethod('otp')" class="p-6 border-2 border-green-500 rounded-lg hover:bg-green-50 transition">
                        <i class="fa-solid fa-mobile-screen-button text-4xl text-green-600 mb-3"></i>
                        <h3 class="font-bold text-lg">Aadhaar Linked with Mobile</h3>
                        <p class="text-sm text-gray-500 mt-2">Instant OTP verification and quick setup.</p>
                    </button>
                    <button onclick="selectMethod('manual')" class="p-6 border-2 border-blue-500 rounded-lg hover:bg-blue-50 transition">
                        <i class="fa-solid fa-file-pen text-4xl text-blue-600 mb-3"></i>
                        <h3 class="font-bold text-lg">Manual Registration</h3>
                        <p class="text-sm text-gray-500 mt-2">If mobile is not linked to Aadhaar.</p>
                    </button>
                </div>
            </div>

            <div id="registration-form" class="hidden">
                <h2 id="reg-title" class="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Registration</h2>
                
                <div class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-semibold mb-1">Full Name</label>
                            <input type="text" class="w-full border p-2 rounded focus:border-green-500" placeholder="As per Aadhaar">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold mb-1">Aadhaar Number (User ID)</label>
                            <input type="text" class="w-full border p-2 rounded focus:border-green-500" placeholder="12-digit number">
                        </div>
                    </div>

                    <!-- OTP Specific Section -->
                    <div id="otp-section" class="bg-green-50 p-4 rounded-lg border border-green-200 mt-4">
                        <label class="block text-sm font-semibold mb-1">Aadhaar Linked Mobile Number</label>
                        <div class="flex space-x-2">
                            <input type="text" class="flex-1 border p-2 rounded" placeholder="10-digit number">
                            <button onclick="sendOTP()" class="bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700">Send OTP</button>
                        </div>
                        
                        <div id="otp-verify-box" class="hidden mt-4">
                            <label class="block text-sm font-semibold mb-1">Enter OTP</label>
                            <div class="flex space-x-2">
                                <input type="text" class="flex-1 border p-2 rounded" placeholder="6-digit OTP">
                                <button onclick="verifyAndSetPassword()" class="bg-blue-600 text-white px-4 py-2 rounded font-bold">Verify OTP</button>
                            </div>
                        </div>

                        <div id="set-password-box" class="hidden mt-4 pt-4 border-t border-green-300">
                            <label class="block text-sm font-semibold mb-1">Set Password for Login</label>
                            <input type="password" class="w-full border p-2 rounded mb-3" placeholder="Create a strong password">
                            <button onclick="completeRegistration()" class="w-full bg-green-700 text-white py-3 rounded font-bold text-lg">Complete Registration & Open Form</button>
                        </div>
                    </div>

                    <!-- Manual Specific Section -->
                    <div id="manual-section" class="bg-blue-50 p-4 rounded-lg border border-blue-200 mt-4 hidden">
                        <p class="text-sm text-blue-800 mb-4"><i class="fa-solid fa-circle-info"></i> Admin will verify your details manually.</p>
                        <label class="block text-sm font-semibold mb-1">Mobile Number (Any active number)</label>
                        <input type="text" class="w-full border p-2 rounded mb-4" placeholder="10-digit number">
                        <label class="block text-sm font-semibold mb-1">Set Password for Login</label>
                        <input type="password" class="w-full border p-2 rounded mb-4" placeholder="Create a strong password">
                        <button onclick="completeRegistration()" class="w-full bg-blue-700 text-white py-3 rounded font-bold text-lg">Proceed to Application Form</button>
                    </div>

                </div>
            </div>
        </div>

        <!-- STEP 2: MAIN APPLICATION FORM -->
        <div id="application-step" class="hidden bg-white rounded-xl shadow-lg p-8 border-t-4 border-blue-600">
            <h2 class="text-2xl font-bold text-blue-900 mb-6 border-b pb-2"><i class="fa-solid fa-file-lines mr-2"></i> Pension Application Form</h2>
            
            <form class="space-y-6">
                <!-- Personal Info -->
                <div class="bg-gray-50 p-4 rounded border">
                    <h3 class="font-bold text-lg mb-3">1. Personal Information</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <input type="text" class="border p-2 rounded" placeholder="Father's/Husband's Name">
                        <input type="date" class="border p-2 rounded" title="Date of Birth">
                        <select class="border p-2 rounded"><option>Select Gender</option><option>Male</option><option>Female</option><option>Transgender</option></select>
                        <select class="border p-2 rounded font-bold text-blue-700"><option>Select Pension Scheme</option><option>Old Age Pension</option><option>Widow Pension</option><option>Disability Pension</option></select>
                    </div>
                </div>

                <!-- Bank Info -->
                <div class="bg-gray-50 p-4 rounded border">
                    <h3 class="font-bold text-lg mb-3">2. Address & Bank Details</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <textarea class="border p-2 rounded col-span-1 md:col-span-2" placeholder="Full Address with PIN Code"></textarea>
                        <input type="text" class="border p-2 rounded" placeholder="Bank Name">
                        <input type="text" class="border p-2 rounded" placeholder="Account Number">
                        <input type="text" class="border p-2 rounded" placeholder="IFSC Code">
                        <input type="text" class="border p-2 rounded bg-red-50" value="Annual Income: 0 (Zero)" readonly>
                    </div>
                </div>

                <!-- Document Uploads -->
                <div class="bg-gray-50 p-4 rounded border">
                    <h3 class="font-bold text-lg mb-3">3. Document Uploads</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div><label class="font-semibold">Passport Photo</label><input type="file" class="w-full mt-1"></div>
                        <div><label class="font-semibold">Aadhaar Card</label><input type="file" class="w-full mt-1"></div>
                        <div><label class="font-semibold">Age Proof</label><input type="file" class="w-full mt-1"></div>
                        <div><label class="font-semibold">Income Certificate</label><input type="file" class="w-full mt-1"></div>
                        <div><label class="font-semibold">Bank Passbook</label><input type="file" class="w-full mt-1"></div>
                    </div>
                </div>

                <!-- Declaration -->
                <div class="bg-yellow-50 p-4 rounded border border-yellow-300">
                    <label class="flex items-start cursor-pointer">
                        <input type="checkbox" class="mt-1 mr-3 w-5 h-5 text-blue-600">
                        <span class="text-sm font-semibold text-gray-800">
                            ମୁଁ ଘୋଷଣା କରୁଛି ଯେ ମୋର ଅନ୍ୟ କୌଣସି ଆୟ ନାହିଁ। ଏହା ଏକ ଘରୋଇ ସହାୟତା, ଯଦି ମୋର ତଥ୍ୟ ଭୁଲ୍ ପ୍ରମାଣିତ ହୁଏ ଅଥବା ୩ ମାସରେ ଥରେ ରିନ୍ୟୁ ନହୁଏ, ତେବେ Admin ମୋର ପେନସନ୍ ବାତିଲ୍ କରିପାରିବେ।
                        </span>
                    </label>
                </div>

                <button type="button" class="w-full bg-blue-700 text-white font-bold py-4 rounded-lg text-xl shadow-lg hover:bg-blue-800 transition">Submit Final Application</button>
            </form>
        </div>
    </main>

</body>
</html>
"""

# ==========================================
# 3. ADMIN LOGIN & DASHBOARD (KEPT INTACT)
# ==========================================
admin_login_design = """<!DOCTYPE html><html lang="en"><head><title>Admin Login</title><script src="https://cdn.tailwindcss.com"></script><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></head><body class="bg-gray-100 flex items-center justify-center min-h-screen"><div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700"><div class="text-center mb-8"><i class="fa-solid fa-user-shield text-5xl text-blue-700 mb-3"></i><h2 class="text-2xl font-bold">Admin Login</h2></div><form action="/admin" method="GET" class="space-y-6"><input type="text" placeholder="Admin ID / Email" class="w-full p-3 border rounded-lg" required><input type="password" placeholder="Password" class="w-full p-3 border rounded-lg" required><button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg">Login to Dashboard</button></form><div class="text-center mt-6"><a href="/" class="text-sm text-gray-500 hover:text-blue-700">Back to Home</a></div></div></body></html>"""

admin_design = """<!DOCTYPE html><html lang="en"><head><title>Admin Dashboard</title><script src="https://cdn.tailwindcss.com"></script><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></head><body class="bg-gray-100 flex h-screen overflow-hidden"><aside class="w-64 bg-slate-900 text-white flex flex-col"><div class="p-5 border-b border-slate-700 text-center"><i class="fa-solid fa-user-shield text-4xl text-blue-500 mb-2"></i><h2 class="text-xl font-bold">Admin Panel</h2></div><nav class="flex-1 py-4"><ul class="space-y-2 px-3"><li><a href="#" class="block px-4 py-3 bg-blue-700 rounded-lg">Dashboard</a></li></ul></nav><div class="p-4"><a href="/" class="block px-4 py-2 text-red-400">Logout</a></div></aside><main class="flex-1 flex flex-col"><header class="bg-white shadow-sm border-b px-6 py-4"><h1 class="text-2xl font-bold">Verification</h1></header><div class="flex-1 overflow-y-auto p-6 bg-gray-50"><div class="bg-white rounded-xl shadow-sm border overflow-hidden p-6"><h2 class="font-bold text-lg mb-4">Pending Applications</h2><p class="text-gray-500">Applicant data will appear here.</p></div></div></main></body></html>"""

# ==========================================
# 4. ALL ROUTES (ରାଉଟ୍ ସେଟଅପ୍)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design

@app.get("/apply", response_class=HTMLResponse)
async def apply_page():
    return pension_apply_design

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    return admin_login_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    return admin_design
