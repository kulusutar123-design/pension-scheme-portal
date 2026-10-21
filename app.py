from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. HOME PAGE DESIGN (ମୁଖ୍ୟ ପୃଷ୍ଠା - Purna Design Sahit)
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

    <!-- Top Header / Navbar -->
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

    <!-- Hero Section -->
    <section id="home" class="hero-bg py-16 px-4 border-b">
        <div class="container mx-auto">
            <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-xl border-l-8 border-blue-600 backdrop-blur-sm">
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">
                    Support for Senior Citizens, Widows, Disabled & the Needy
                </h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition duration-300 flex items-center w-max">
                    View Schemes <i class="fa-solid fa-arrow-down ml-2"></i>
                </a>
            </div>
        </div>
    </section>

    <!-- 6 Action Cards Section -->
    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Admin Login</h3>
                <p class="text-sm mb-4 text-blue-100">Official login for Administration</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Pension Apply</h3>
                <p class="text-sm mb-4 text-green-100">Apply for New Pension</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Check Status</h3>
                <p class="text-sm mb-4 text-orange-100">Check Your Application Status</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Beneficiary</h3>
                <p class="text-sm mb-4 text-purple-100">Login for Beneficiaries</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Schemes</h3>
                <p class="text-sm mb-4 text-teal-100">View Info & Guidelines</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Help Desk</h3>
                <p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

        </div>
    </section>

    <!-- NEW SECTION: ABOUT US -->
    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Odia -->
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm">
                    <h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3>
                    <p class="text-gray-700 leading-relaxed text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ।"</p>
                </div>
                <!-- English -->
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm">
                    <h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">English</h3>
                    <p class="text-gray-700 leading-relaxed text-sm">"The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy. Pension is not just money; it is respect."</p>
                </div>
                <!-- Hindi -->
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm">
                    <h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Hindi (हिन्दी)</h3>
                    <p class="text-gray-700 leading-relaxed text-sm">"प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों को आर्थिक सहायता और सम्मान प्रदान करना है। पेंशन केवल पैसा नहीं, बल्कि सम्मान है।"</p>
                </div>
            </div>
        </div>
    </section>

    <!-- NEW SECTION: SCHEMES & RULES -->
    <section id="schemes" class="bg-gray-100 py-12 border-t border-b border-gray-200">
        <div class="container mx-auto px-4">
            <div class="text-center mb-10">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-list-check mr-2"></i> ଯୋଜନା ଏବଂ ସର୍ତ୍ତାବଳୀ (Schemes & Conditions)</h2>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Schemes List -->
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-hand-holding-dollar mr-2"></i> Pension Schemes</h3>
                    <ul class="space-y-4">
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-green-500 shadow-sm">
                            <span class="font-semibold text-gray-800">ବୃଦ୍ଧାବସ୍ଥା (Old Age)</span>
                            <span class="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">୫୫ ରୁ ୧୦୦ ବର୍ଷ</span>
                        </li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-blue-500 shadow-sm">
                            <span class="font-semibold text-gray-800">ବିଧବା (Widow)</span>
                            <span class="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span>
                        </li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-orange-500 shadow-sm">
                            <span class="font-semibold text-gray-800">ଭିନ୍ନକ୍ଷମ (Disability)</span>
                            <span class="text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded">୧୦ ରୁ ୧୦୦ ବର୍ଷ</span>
                        </li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-purple-500 shadow-sm">
                            <span class="font-semibold text-gray-800">ଅବିବାହିତା (Unmarried)</span>
                            <span class="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">୩୦ ରୁ ୫୫ ବର୍ଷ</span>
                        </li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-pink-500 shadow-sm">
                            <span class="font-semibold text-gray-800">ଛାଡପତ୍ର ପାଇଥିବା (Divorcee)</span>
                            <span class="text-sm bg-pink-100 text-pink-800 px-2 py-1 rounded">୩୫ ରୁ ୫୫ ବର୍ଷ</span>
                        </li>
                        <li class="flex justify-between items-center bg-gray-50 p-3 rounded border-l-4 border-teal-500 shadow-sm">
                            <span class="font-semibold text-gray-800">କିନ୍ନର (Transgender)</span>
                            <span class="text-sm bg-teal-100 text-teal-800 px-2 py-1 rounded">୩୫ ରୁ ୫୫ ବର୍ଷ</span>
                        </li>
                        <li class="text-xs text-gray-500 italic mt-2">* ଅନ୍ୟାନ୍ୟ ଯୋଜନା: କୁଷ୍ଠରୋଗ ଆରୋଗ୍ୟ, ଏଡସ୍/ଏଚଆଇଭି ଆକ୍ରାନ୍ତ (ବିଧବା/ଭିନ୍ନକ୍ଷମ)</li>
                    </ul>
                </div>

                <!-- Strict Rules -->
                <div class="lg:col-span-1 bg-red-50 rounded-xl p-6 shadow border border-red-200">
                    <h3 class="font-bold text-xl text-red-800 mb-4 border-b-2 border-red-500 pb-2"><i class="fa-solid fa-triangle-exclamation mr-2"></i> କଡ଼ା ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ</h3>
                    <div class="space-y-4 text-sm text-gray-800">
                        <div class="flex items-start">
                            <i class="fa-solid fa-ban text-red-600 mt-1 mr-2 text-lg"></i>
                            <p><strong>Private Initiative:</strong> ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଟ୍ରଷ୍ଟ/ବେସରକାରୀ ସାହାଯ୍ୟ। ଏହା ସରକାରୀ ଯୋଜନା ନୁହେଁ।</p>
                        </div>
                        <div class="flex items-start">
                            <i class="fa-solid fa-gavel text-red-600 mt-1 mr-2 text-lg"></i>
                            <p><strong>Admin Rights:</strong> ବିନା କାରଣ ଦର୍ଶାଇ, କାହାର ବି ପେନସନ୍ ଆବେଦନ ନାକଚ ବା ବନ୍ଦ କରିବାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର Admin ଙ୍କ ପାଖରେ ରହିବ।</p>
                        </div>
                        <div class="flex items-start">
                            <i class="fa-solid fa-rotate text-red-600 mt-1 mr-2 text-lg"></i>
                            <p><strong>Mandatory Renewal:</strong> ପ୍ରତି ୩ ମାସରେ ଥରେ ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ। ନଚେତ୍ ଆପେ ଆପେ ବନ୍ଦ ହୋଇଯିବ।</p>
                        </div>
                        <div class="flex items-start">
                            <i class="fa-solid fa-wallet text-red-600 mt-1 mr-2 text-lg"></i>
                            <p><strong>Zero Income:</strong> ଆବେଦନକାରୀଙ୍କର କୌଣସି ଆୟ ନଥିବା ଦରକାର। ଭୁଲ୍ ତଥ୍ୟ ଦେଲେ ପେନସନ୍ ତୁରନ୍ତ ବାତିଲ୍ ହେବ।</p>
                        </div>
                    </div>
                </div>

                <!-- Documents -->
                <div class="lg:col-span-1 bg-white rounded-xl p-6 shadow border border-gray-200">
                    <h3 class="font-bold text-xl text-blue-800 mb-4 border-b-2 border-blue-500 pb-2"><i class="fa-solid fa-folder-open mr-2"></i> ଦରକାରୀ କାଗଜପତ୍ର (Documents)</h3>
                    <ul class="space-y-3 text-sm text-gray-700">
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆଧାର କାର୍ଡ (Aadhaar Card)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବୟସ ପ୍ରମାଣପତ୍ର (Age Proof)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ଆୟ ପ୍ରମାଣପତ୍ର (Income Certificate)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ବ୍ୟାଙ୍କ୍ ପାସବୁକ୍ (Bank Passbook)</li>
                        <li class="flex items-center"><i class="fa-solid fa-check text-green-500 mr-2"></i> ପାସପୋର୍ଟ ସାଇଜ୍ ଫଟୋ (Passport Size Photo)</li>
                        <li class="flex items-start mt-2 bg-yellow-50 p-2 rounded text-xs border border-yellow-200">
                            <i class="fa-solid fa-circle-info text-yellow-600 mt-1 mr-2"></i>
                            ଯୋଜନା ଅନୁସାରେ ସ୍ୱତନ୍ତ୍ର ପ୍ରମାଣପତ୍ର (ଉଦାହରଣ: ଭିନ୍ନକ୍ଷମ ପ୍ରମାଣପତ୍ର, ସ୍ୱାମୀଙ୍କ ମୃତ୍ୟୁ ପ୍ରମାଣପତ୍ର ଇତ୍ୟାଦି)।
                        </li>
                    </ul>
                </div>

            </div>
        </div>
    </section>

    <!-- NEW SECTION: CONTACT US -->
    <section id="contact" class="container mx-auto px-4 py-12">
        <div class="bg-blue-900 text-white rounded-xl p-8 shadow-xl text-center max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold mb-4"><i class="fa-solid fa-envelope-open-text mr-2"></i> ଯୋଗାଯୋଗ (Contact Us)</h2>
            <p class="mb-6 text-blue-200">For any inquiries, application support, or grievances, please reach out to us at our official email address.</p>
            <div class="inline-block bg-white text-blue-900 px-6 py-4 rounded-lg font-bold text-xl shadow-inner">
                <i class="fa-solid fa-envelope mr-2"></i> admin@kulusutar.in
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-8 border-t-4 border-blue-600">
        <div class="container mx-auto px-4 flex justify-between items-center text-sm">
            <p class="text-gray-300">&copy; 2026 Private Social Security Pension Scheme</p>
        </div>
    </footer>

</body>
</html>
"""


# ==========================================
# 2. ADMIN LOGIN PAGE DESIGN
# ==========================================
admin_login_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Private Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function togglePassword() {
            var passField = document.getElementById("password");
            var eyeIcon = document.getElementById("eye-icon");
            if (passField.type === "password") {
                passField.type = "text";
                eyeIcon.classList.remove("fa-eye");
                eyeIcon.classList.add("fa-eye-slash");
            } else {
                passField.type = "password";
                eyeIcon.classList.remove("fa-eye-slash");
                eyeIcon.classList.add("fa-eye");
            }
        }
    </script>
</head>
<body class="bg-gray-100 font-sans flex items-center justify-center min-h-screen">
    
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-blue-700">
        <div class="text-center mb-8">
            <i class="fa-solid fa-user-shield text-5xl text-blue-700 mb-3"></i>
            <h2 class="text-2xl font-bold text-gray-800">Admin Login</h2>
            <p class="text-sm text-gray-500 mt-1">Private Social Security Pension Scheme</p>
        </div>

        <form action="/admin" method="GET" class="space-y-6">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Admin ID / Email</label>
                <div class="relative">
                    <i class="fa-solid fa-envelope absolute left-3 top-3.5 text-gray-400"></i>
                    <input type="text" placeholder="Enter ID or Email" class="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-blue-500" required>
                </div>
            </div>

            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <div class="relative">
                    <i class="fa-solid fa-lock absolute left-3 top-3.5 text-gray-400"></i>
                    <input type="password" id="password" placeholder="Enter password" class="w-full pl-10 pr-10 py-3 border rounded-lg focus:ring-blue-500" required>
                    <button type="button" onclick="togglePassword()" class="absolute right-3 top-3.5 text-gray-400 hover:text-blue-500">
                        <i id="eye-icon" class="fa-solid fa-eye"></i>
                    </button>
                </div>
            </div>

            <div class="flex items-center justify-between text-sm">
                <label class="flex items-center text-gray-600">
                    <input type="checkbox" class="mr-2 rounded text-blue-600"> Remember me
                </label>
                <a href="#" class="font-semibold text-blue-600 hover:text-blue-800">Forgot Password?</a>
            </div>

            <button type="submit" class="w-full bg-blue-700 text-white font-bold py-3 rounded-lg hover:bg-blue-800 shadow-md">
                <i class="fa-solid fa-right-to-bracket mr-2"></i> Login to Dashboard
            </button>
        </form>

        <div class="text-center mt-6">
            <a href="/" class="text-sm text-gray-500 hover:text-blue-700"><i class="fa-solid fa-arrow-left mr-1"></i> Back to Home</a>
        </div>
    </div>
</body>
</html>
"""


# ==========================================
# 3. ADMIN DASHBOARD DESIGN (With JS Tabs for Sidebar)
# ==========================================
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
        // Sidebar click kelyavar tab change karnyachi script
        function switchTab(tabId, element) {
            // Hide all content sections
            let sections = document.querySelectorAll('.content-section');
            for(let i=0; i<sections.length; i++) {
                sections[i].classList.add('hidden');
            }
            // Show the selected section
            document.getElementById('section-' + tabId).classList.remove('hidden');

            // Reset all menu links to default color
            let links = document.querySelectorAll('.menu-link');
            for(let i=0; i<links.length; i++) {
                links[i].classList.remove('bg-blue-700', 'text-white');
                links[i].classList.add('text-slate-300', 'hover:bg-slate-800');
            }
            // Highlight the clicked menu link
            element.classList.remove('text-slate-300', 'hover:bg-slate-800');
            element.classList.add('bg-blue-700', 'text-white');

            // Update Header Title dynamically
            let titles = {
                'dashboard': '<i class="fa-solid fa-list-check text-blue-600 mr-2"></i> Dashboard Overview',
                'newapps': '<i class="fa-solid fa-file-signature text-blue-600 mr-2"></i> New Applications',
                'beneficiaries': '<i class="fa-solid fa-users text-blue-600 mr-2"></i> Manage Beneficiaries',
                'renewals': '<i class="fa-solid fa-clock-rotate-left text-blue-600 mr-2"></i> 3-Month Renewals',
                'payments': '<i class="fa-solid fa-money-bill-transfer text-blue-600 mr-2"></i> Payment Records'
            };
            document.getElementById('header-title').innerHTML = titles[tabId];
        }
    </script>
</head>
<body class="bg-gray-100 font-sans text-gray-800 flex h-screen overflow-hidden">

    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl h-full">
        <div class="p-5 border-b border-slate-700 text-center">
            <i class="fa-solid fa-user-shield text-4xl text-blue-500 mb-2"></i>
            <h2 class="text-xl font-bold">Admin Panel</h2>
        </div>
        
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <!-- Javascript function switchTab() add kela aahe -->
                <li><a href="#" onclick="switchTab('dashboard', this)" class="menu-link flex items-center px-4 py-3 bg-blue-700 text-white rounded-lg transition"><i class="fa-solid fa-gauge w-6 mr-2"></i> Dashboard</a></li>
                <li><a href="#" onclick="switchTab('newapps', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-file-signature w-6 mr-2"></i> New Apps <span class="ml-auto bg-red-500 text-white px-2 rounded-full text-xs">3</span></a></li>
                <li><a href="#" onclick="switchTab('beneficiaries', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-users w-6 mr-2"></i> Beneficiaries</a></li>
                <li><a href="#" onclick="switchTab('renewals', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> Renewals</a></li>
                <li><a href="#" onclick="switchTab('payments', this)" class="menu-link flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg transition"><i class="fa-solid fa-money-bill-transfer w-6 mr-2"></i> Payments</a></li>
            </ul>
        </nav>
        
        <div class="p-4 border-t border-slate-700">
            <a href="/" class="flex items-center px-4 py-2 text-red-400 hover:bg-red-500 hover:text-white rounded-lg transition"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout</a>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
        <header class="bg-white shadow-sm border-b px-6 py-4 flex justify-between items-center">
            <h1 id="header-title" class="text-2xl font-bold"><i class="fa-solid fa-list-check text-blue-600 mr-2"></i> Dashboard Overview</h1>
            <div class="flex items-center space-x-4">
                <span class="text-sm font-medium">Welcome, <strong>Super Admin</strong></span>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-6 bg-gray-50">
            
            <!-- SECTION 1: DASHBOARD (Default Open) -->
            <div id="section-dashboard" class="content-section">
                <!-- Stats Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-blue-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500">Total Applications</p><h3 class="text-2xl font-bold">1,245</h3></div>
                        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-file-lines"></i></div>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-l-4 border-green-500 shadow-sm flex justify-between items-center">
                        <div><p class="text-sm text-gray-500">Active Pensioners</p><h3 class="text-2xl font-bold">850</h3></div>
                        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl"><i class="fa-solid fa-check-circle"></i></div>
                    </div>
                </div>

                <!-- Table -->
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
                        <h2 class="font-bold text-lg">Pending Applications</h2>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr>
                                    <th class="py-3 px-6">ID</th>
                                    <th class="py-3 px-6">Name</th>
                                    <th class="py-3 px-6">Scheme</th>
                                    <th class="py-3 px-6 text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm divide-y">
                                <tr class="hover:bg-gray-50">
                                    <td class="py-4 px-6 font-medium text-blue-600">#APP-9082</td>
                                    <td class="py-4 px-6 font-bold">Rama Chandra Das</td>
                                    <td class="py-4 px-6"><span class="bg-green-100 text-green-800 py-1 px-3 rounded-full text-xs font-semibold">Old Age Pension</span></td>
                                    <td class="py-4 px-6 text-center space-x-2">
                                        <button class="bg-green-100 text-green-700 px-3 py-1 rounded"><i class="fa-solid fa-check"></i> Approve</button>
                                        <button class="bg-red-100 text-red-700 px-3 py-1 rounded"><i class="fa-solid fa-xmark"></i> Reject</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- SECTION 2: NEW APPS -->
            <div id="section-newapps" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-gray-50">
                        <h2 class="font-bold text-lg">Review New Applications</h2>
                    </div>
                    <div class="p-8 text-center text-gray-500">
                        <i class="fa-solid fa-folder-open text-4xl mb-3 text-blue-300"></i>
                        <p>No new applications found today.</p>
                    </div>
                </div>
            </div>

            <!-- SECTION 3: BENEFICIARIES -->
            <div id="section-beneficiaries" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div class="px-6 py-4 border-b bg-gray-50">
                        <h2 class="font-bold text-lg">Active Beneficiaries List</h2>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead class="bg-gray-100 text-gray-600 text-sm">
                                <tr>
                                    <th class="py-3 px-6">ID</th>
                                    <th class="py-3 px-6">Name</th>
                                    <th class="py-3 px-6">Status</th>
                                    <th class="py-3 px-6 text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody class="text-sm divide-y">
                                <tr class="hover:bg-gray-50">
                                    <td class="py-4 px-6 font-medium text-blue-600">#BEN-101</td>
                                    <td class="py-4 px-6 font-bold">Harihar Nayak</td>
                                    <td class="py-4 px-6"><span class="bg-green-100 text-green-800 py-1 px-3 rounded-full text-xs font-semibold">Active</span></td>
                                    <td class="py-4 px-6 text-center">
                                        <button class="bg-red-600 text-white px-3 py-1 rounded shadow hover:bg-red-700 transition"><i class="fa-solid fa-hand-paper"></i> Stop Pension</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- SECTION 4: RENEWALS -->
            <div id="section-renewals" class="content-section hidden">
                 <div class="bg-red-50 border border-red-200 rounded-xl p-6 shadow-sm">
                    <h2 class="font-bold text-lg text-red-800 mb-2"><i class="fa-solid fa-triangle-exclamation"></i> Overdue Renewals</h2>
                    <p class="text-sm text-red-600">The following beneficiaries have not renewed their pension in 3 months.</p>
                </div>
            </div>

            <!-- SECTION 5: PAYMENTS -->
            <div id="section-payments" class="content-section hidden">
                <div class="bg-white rounded-xl shadow-sm border p-8 text-center text-gray-500">
                    <i class="fa-solid fa-money-check-dollar text-4xl mb-3 text-green-300"></i>
                    <p>Payment records will be displayed here.</p>
                </div>
            </div>

        </div>
    </main>
</body>
</html>
"""


# ==========================================
# 4. ALL ROUTES (ରାଉଟ୍ ସେଟଅପ୍)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    return admin_login_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    return admin_design
