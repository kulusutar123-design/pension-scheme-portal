from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. PUBLIC WEBSITE DESIGN (ସମ୍ପୂର୍ଣ୍ଣ ପୁରୁଣା ଡାଟା)
# ==========================================
public_html_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Social Security Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg { background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'); background-size: cover; background-position: center; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); transition: all 0.3s ease; }
        .tab-btn.active { background-color: #1d4ed8; color: white; }
        .page-section { display: none; animation: fadeIn 0.5s; }
        .page-section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .nav-link.active-link { color: #1d4ed8; border-bottom: 3px solid #1d4ed8; padding-bottom: 4px; }
    </style>
    <script>
        function switchPage(pageId) {
            var pages = document.getElementsByClassName('page-section');
            for(var i = 0; i < pages.length; i++) pages[i].classList.remove('active');
            document.getElementById(pageId).classList.add('active');
            
            var links = document.getElementsByClassName('nav-link');
            for(var i = 0; i < links.length; i++) links[i].classList.remove('active-link');
            if(document.getElementById('link-' + pageId)) document.getElementById('link-' + pageId).classList.add('active-link');
        }
        function showTab(lang) {
            document.getElementById('about-en').classList.add('hidden');
            document.getElementById('about-hi').classList.add('hidden');
            document.getElementById('about-or').classList.add('hidden');
            document.getElementById('btn-en').classList.remove('active');
            document.getElementById('btn-hi').classList.remove('active');
            document.getElementById('btn-or').classList.remove('active');
            document.getElementById('about-' + lang).classList.remove('hidden');
            document.getElementById('btn-' + lang).classList.add('active');
        }
        function checkStatusSimulate() {
            alert("System Message: Application is under 2-Day Auto Verification. Checking Aadhaar and Penny Drop Name Matching. If rejected, your Aadhaar will be locked for 3 months.");
        }
    </script>
</head>
<body class="bg-gray-50 font-sans text-gray-800 min-h-screen flex flex-col">

    <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-3 cursor-pointer" onclick="switchPage('page-home')">
                <div class="text-blue-800 text-4xl"><i class="fa-solid fa-hands-holding-child"></i></div>
                <div>
                    <h1 class="text-xl md:text-2xl font-extrabold text-blue-900 tracking-tight">Private Social Security Pension Scheme</h1>
                    <p class="text-sm font-bold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            <div class="hidden md:flex space-x-6 mt-4 md:mt-0 text-lg">
                <button id="link-page-home" onclick="switchPage('page-home')" class="nav-link active-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-house mr-1"></i> Home</button>
                <button id="link-page-about" onclick="switchPage('page-about')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-circle-info mr-1"></i> About Us</button>
                <button id="link-page-schemes" onclick="switchPage('page-schemes')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-list-check mr-1"></i> Schemes</button>
                <button id="link-page-conditions" onclick="switchPage('page-conditions')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-scale-balanced mr-1"></i> Conditions</button>
                <button id="link-page-contact" onclick="switchPage('page-contact')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-phone mr-1"></i> Contact Us</button>
            </div>
        </div>
    </header>

    <main class="flex-grow">
        <div id="page-home" class="page-section active">
            <section class="hero-bg py-16 px-4 border-b">
                <div class="container mx-auto">
                    <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-2xl border-l-8 border-blue-700">
                        <h2 class="text-3xl md:text-4xl font-black text-blue-900 mb-4 leading-tight">Support for Senior Citizens, Widows, Disabled and the Needy</h2>
                        <p class="text-lg text-gray-800 font-semibold mb-6">Pension is not just money, it is respect. Dual Aadhaar & Penny Drop Verification Active.</p>
                        <button onclick="switchPage('page-schemes')" class="bg-blue-700 text-white px-8 py-3 rounded-md font-bold shadow-lg hover:bg-blue-800 transition text-lg">Apply / Learn More</button>
                    </div>
                </div>
            </section>
            <section class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    <div onclick="window.location.href='/admin'" class="bg-gradient-to-br from-blue-600 to-blue-800 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-user-shield text-5xl mb-4 text-blue-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Admin Login</h3>
                        <p class="text-sm mb-4 text-blue-100 font-medium">Official login for Administration Management</p>
                        <button class="bg-white text-blue-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="switchPage('page-schemes')" class="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-file-signature text-5xl mb-4 text-green-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Apply Pension</h3>
                        <p class="text-sm mb-4 text-green-100 font-medium">Apply for New Private Pension Scheme</p>
                        <button class="bg-white text-green-800 font-bold py-2 px-6 rounded-full text-sm">Apply Now <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="checkStatusSimulate()" class="bg-gradient-to-br from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart text-5xl mb-4 text-orange-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Check Status</h3>
                        <p class="text-sm mb-4 text-orange-100 font-medium">Track your Application & 2-Day Verify Status</p>
                        <button class="bg-white text-orange-800 font-bold py-2 px-6 rounded-full text-sm">Check <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>
            </section>
        </div>

        <div id="page-about" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-blue-900"><i class="fa-solid fa-circle-info text-blue-600"></i> About Us / ଆମ ବିଷୟରେ</h2><div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4"></div></div>
                <div class="bg-gray-50 rounded-xl shadow-lg overflow-hidden border-2 border-gray-200">
                    <div class="flex border-b-2 border-gray-200 bg-white"><button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-xl">ଓଡ଼ିଆ</button><button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">हिंदी</button><button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">English</button></div>
                    <div class="p-8 md:p-12 text-lg">
                        <div id="about-or" class="block"><p class="font-semibold">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ। ଆମେ ସମାଜର ଅବହେଳିତ ବର୍ଗଙ୍କ ସହ ଛିଡା ହେବାକୁ ପ୍ରତିଶ୍ରୁତିବଦ୍ଧ।</p></div>
                        <div id="about-hi" class="hidden"><p class="font-semibold">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी पहल है।</p></div>
                        <div id="about-en" class="hidden"><p class="font-semibold">This is a 100% private initiative. Pension is respect.</p></div>
                    </div>
                </div>
            </div>
        </div>

        <div id="page-schemes" class="page-section py-12 bg-gray-50">
            <div class="container mx-auto px-4 max-w-7xl">
                <div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-blue-900"><i class="fa-solid fa-list-check text-blue-600"></i> Schemes & Limits</h2><div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4"></div></div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-blue-600"><h3 class="text-2xl font-black text-blue-900">Old Age Pension</h3><p class="text-gray-500 mb-2 border-b pb-2">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p><p class="bg-blue-100 p-2 rounded font-bold mb-2">Age: 55 to 100 Years</p><p class="bg-green-100 p-2 rounded font-bold text-green-800">Amount: ₹3000 / Year</p></div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-green-600"><h3 class="text-2xl font-black text-green-900">Disability Pension</h3><p class="text-gray-500 mb-2 border-b pb-2">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p><p class="bg-green-100 p-2 rounded font-bold mb-2">Age: 10 to 100 Years</p><p class="bg-green-100 p-2 rounded font-bold text-green-800">Amount: ₹3500 / Year</p></div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-purple-600"><h3 class="text-2xl font-black text-purple-900">Widow Pension</h3><p class="bg-purple-100 p-2 rounded font-bold">Age: 30 to 55 Years</p></div>
                </div>
            </div>
        </div>

        <div id="page-conditions" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-red-700">Strict Terms & Conditions</h2><div class="w-32 h-1.5 bg-red-600 mx-auto mt-4"></div></div>
                <div class="bg-red-50 border-2 border-red-300 rounded-xl p-8 shadow-xl">
                    <div class="space-y-6">
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">2-Day Verification & Name Matching</h4><p class="mt-2 text-gray-700 font-bold">All applications undergo a 2-day API check. We use Penny Drop 1 Rupee test to match bank name with Aadhaar name exactly. Mismatch = Automatic Reject.</p></div>
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">3-Month Ban & Re-Apply Fee</h4><p class="mt-2 text-gray-700">If rejected due to fake documents, your Aadhaar is locked for 3 months. You must pay the application fee again to re-apply.</p></div>
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">Non-Refundable Fee</h4><p class="mt-2 text-gray-700">Application fees are absolutely NON-REFUNDABLE under any circumstance.</p></div>
                    </div>
                </div>
            </div>
        </div>

        <div id="page-contact" class="page-section py-12 bg-blue-50">
            <div class="container mx-auto text-center"><h2 class="text-3xl font-extrabold text-blue-900 mb-6">Contact Us</h2>
                <div class="bg-white p-10 rounded-xl max-w-2xl mx-auto shadow-xl"><p class="text-2xl font-black"><i class="fa-solid fa-phone text-blue-700"></i> 8910223342</p><p class="text-2xl font-black mt-4"><i class="fa-solid fa-envelope text-blue-700"></i> admin@kulusutar.in</p></div>
            </div>
        </div>

    </main>
    <footer class="bg-blue-900 text-white py-6 text-center mt-auto"><p>&copy; 2026 Private Social Security Pension Scheme</p></footer>
</body>
</html>
"""

# ==========================================
# 2. SUPER ADMIN PANEL WITH PAYMENT API & FORGOT PASSWORD
# ==========================================
admin_html_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Super Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .admin-page { display: none; }
        .admin-page.active { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 100; align-items: center; justify-content: center; }
        .modal.active { display: flex; }
    </style>
</head>
<body class="bg-gray-100 font-sans">

    <!-- LOGIN SCREEN -->
    <div id="login-screen" class="min-h-screen flex items-center justify-center bg-gray-900 absolute inset-0 z-50">
        <div class="bg-white p-10 rounded-xl shadow-2xl w-96 text-center">
            <i class="fa-solid fa-user-shield text-6xl text-blue-700 mb-4"></i>
            <h2 class="text-2xl font-bold mb-6 text-gray-800">Admin Login</h2>
            <input type="text" id="username" placeholder="Username" class="w-full p-3 mb-4 border rounded outline-none font-bold">
            <input type="password" id="password" placeholder="Password" class="w-full p-3 mb-4 border rounded outline-none font-bold">
            <div class="text-right mb-6">
                <button onclick="showForgotPassword()" class="text-blue-600 text-sm font-bold hover:underline">Forgot Password?</button>
            </div>
            <button onclick="login()" class="w-full bg-blue-700 text-white font-bold py-3 rounded hover:bg-blue-800 shadow">LOGIN</button>
            <p id="login-error" class="text-red-500 mt-3 hidden text-sm font-bold">Incorrect Details!</p>
        </div>
    </div>

    <!-- FORGOT PASSWORD SCREEN -->
    <div id="forgot-pwd-screen" class="hidden min-h-screen flex items-center justify-center bg-gray-900 absolute inset-0 z-50">
        <div class="bg-white p-10 rounded-xl shadow-2xl w-96 text-center">
            <i class="fa-solid fa-lock-open text-6xl text-orange-500 mb-4"></i>
            <h2 class="text-2xl font-bold mb-2 text-gray-800">Reset Password</h2>
            <p class="text-xs text-gray-500 mb-6 font-bold">Enter registered Email (admin@kulusutar.in)</p>
            
            <div id="fp-step-1">
                <input type="email" id="fp-email" placeholder="Registered Email ID" class="w-full p-3 mb-4 border rounded outline-none font-bold">
                <button onclick="sendOTP()" class="w-full bg-orange-500 text-white font-bold py-3 rounded hover:bg-orange-600 shadow mb-4">Send OTP</button>
            </div>

            <div id="fp-step-2" class="hidden">
                <input type="text" id="fp-otp" placeholder="Enter OTP" class="w-full p-3 mb-4 border rounded outline-none font-bold text-center tracking-widest text-lg">
                <button onclick="verifyOTP()" class="w-full bg-green-600 text-white font-bold py-3 rounded hover:bg-green-700 shadow mb-4">Verify OTP</button>
            </div>

            <div id="fp-step-3" class="hidden">
                <input type="password" id="fp-new-pwd" placeholder="New Password" class="w-full p-3 mb-4 border rounded outline-none font-bold">
                <input type="password" id="fp-conf-pwd" placeholder="Confirm Password" class="w-full p-3 mb-4 border rounded outline-none font-bold">
                <button onclick="resetPassword()" class="w-full bg-blue-700 text-white font-bold py-3 rounded hover:bg-blue-800 shadow mb-4">Save New Password</button>
            </div>

            <button onclick="backToLogin()" class="text-gray-500 text-sm font-bold hover:underline mt-2"><i class="fa-solid fa-arrow-left"></i> Back to Login</button>
        </div>
    </div>

    <!-- MAIN ADMIN PANEL -->
    <div id="admin-dashboard" class="hidden min-h-screen flex">
        <!-- SIDEBAR -->
        <div class="w-64 bg-gray-900 text-white flex flex-col shadow-2xl">
            <div class="p-6 border-b border-gray-800 text-center">
                <i class="fa-solid fa-user-tie text-4xl text-blue-400 mb-2"></i>
                <h2 class="font-bold text-lg">Super Admin</h2>
            </div>
            <nav class="flex-1 p-4 space-y-2 text-sm font-bold">
                <button onclick="switchAdmin('dash')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-chart-pie w-6"></i> Dashboard</button>
                <button onclick="switchAdmin('verify')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-check-double w-6"></i> Verify (System Passed)</button>
                <button onclick="switchAdmin('rejected')" class="w-full text-left p-3 rounded text-red-400 hover:bg-gray-800"><i class="fa-solid fa-folder-closed w-6"></i> Rejected Vault</button>
                <button onclick="switchAdmin('vault')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-vault w-6"></i> Active Vault</button>
                <button onclick="switchAdmin('payment')" class="w-full text-left p-3 rounded bg-green-700"><i class="fa-solid fa-building-columns w-6"></i> Payment Management</button>
                <!-- NEW ADMIN PROFILE MENU -->
                <button onclick="switchAdmin('profile')" class="w-full text-left p-3 rounded hover:bg-gray-800 mt-6 border-t border-gray-700 pt-4"><i class="fa-solid fa-user-gear w-6"></i> Admin Profile</button>
            </nav>
            <div class="p-4 border-t border-gray-800">
                <button onclick="window.location.href='/'" class="w-full text-left p-2 text-red-500 font-bold"><i class="fa-solid fa-power-off w-6"></i> Logout</button>
            </div>
        </div>

        <!-- RIGHT CONTENT -->
        <div class="flex-1 flex flex-col h-screen overflow-y-auto">
            <header class="bg-white shadow p-4 flex justify-between border-b-4 border-blue-600">
                <h1 class="text-2xl font-bold text-gray-800" id="page-title">Dashboard</h1>
                <div class="flex items-center text-gray-600 font-bold cursor-pointer" onclick="switchAdmin('profile')">
                    <i class="fa-solid fa-bell text-red-600 mr-4"></i> <i class="fa-solid fa-user-circle text-blue-600 text-xl mr-2"></i> Kulu Sutar
                </div>
            </header>

            <!-- DASHBOARD -->
            <main id="view-dash" class="admin-page active p-6">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded shadow border-l-4 border-blue-500"><p class="text-gray-500 font-bold">Total Forms</p><h3 class="text-3xl font-black">124</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-green-500"><p class="text-gray-500 font-bold">System Passed</p><h3 class="text-3xl font-black text-green-600">89</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-red-500"><p class="text-gray-500 font-bold">Rejected / Locked</p><h3 class="text-3xl font-black text-red-600">35</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-orange-500"><p class="text-gray-500 font-bold">Re-apply Fees</p><h3 class="text-3xl font-black text-gray-800">₹5,000</h3></div>
                </div>
            </main>

            <!-- VERIFICATION (SYSTEM PASSED) -->
            <main id="view-verify" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-blue-900"><i class="fa-solid fa-check-double"></i> 2nd Step Verification (System Passed)</h2>
                <div class="bg-white rounded shadow overflow-hidden">
                    <table class="w-full text-left">
                        <thead class="bg-gray-100 border-b">
                            <tr><th class="p-4">App ID</th><th class="p-4">Name</th><th class="p-4">System Status</th><th class="p-4">Action</th></tr>
                        </thead>
                        <tbody>
                            <tr class="border-b">
                                <td class="p-4 font-bold">#APP-001</td><td class="p-4">Ramesh Pradhan</td>
                                <td class="p-4"><span class="bg-blue-100 text-blue-800 px-2 py-1 text-xs font-bold rounded"><i class="fa-solid fa-robot"></i> 1 Rupee Match Passed</span></td>
                                <td class="p-4"><button onclick="alert('Final Verify Window opened!')" class="bg-blue-600 text-white px-4 py-1 rounded font-bold shadow">Final Verify</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </main>

            <!-- REJECTED VAULT -->
            <main id="view-rejected" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-red-900"><i class="fa-solid fa-folder-closed"></i> Rejected Vault (3-Month Locked)</h2>
                <div class="bg-red-50 p-6 rounded border border-red-200 shadow">
                    <p class="font-bold text-red-800 mb-2">Users banned for mismatch in spelling/fake docs.</p>
                </div>
            </main>
            
            <main id="view-vault" class="admin-page p-6"><h2 class="text-xl font-bold mb-4">Active Vault</h2></main>

            <!-- PAYMENT MANAGEMENT SECTION -->
            <main id="view-payment" class="admin-page p-6">
                <h2 class="text-xl font-black mb-6 text-green-900 border-b-2 border-green-200 pb-2"><i class="fa-solid fa-building-columns"></i> Secure Payment Management</h2>
                <div class="bg-white p-6 rounded-lg shadow border border-gray-200 mb-6">
                    <h3 class="font-bold text-lg text-gray-800 mb-3"><i class="fa-solid fa-key text-blue-500"></i> Gateway API Configuration</h3>
                    <div class="flex flex-col md:flex-row gap-4">
                        <input type="text" placeholder="Enter PayU API Key (e.g., payu_live_xxxx)" class="flex-1 p-3 border rounded bg-gray-50 outline-none font-bold text-sm">
                        <button onclick="alert('API Key Saved & Connected Successfully!')" class="bg-gray-800 text-white px-6 py-2 rounded font-bold shadow hover:bg-gray-900">Save API & Connect</button>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-green-50 p-6 rounded-lg shadow border-2 border-green-400 relative overflow-hidden">
                        <div class="absolute top-0 right-0 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">Highly Secure</div>
                        <h3 class="font-black text-xl text-green-800 mb-2"><i class="fa-solid fa-fingerprint"></i> Aadhaar DBT Payouts</h3>
                        <p class="text-sm font-semibold text-gray-700 mb-6">Send money directly to Aadhaar-linked accounts. No account numbers required.</p>
                        <button onclick="processPayment('DBT')" class="w-full bg-green-600 text-white font-black py-3 rounded shadow-lg hover:bg-green-700 transition"><i class="fa-solid fa-paper-plane mr-2"></i> Process DBT Payments Now</button>
                    </div>
                    <div class="bg-blue-50 p-6 rounded-lg shadow border-2 border-blue-400 relative overflow-hidden">
                        <div class="absolute top-0 right-0 bg-blue-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">Manual Entry</div>
                        <h3 class="font-black text-xl text-blue-800 mb-2"><i class="fa-solid fa-money-check-dollar"></i> Bank A/C Payouts</h3>
                        <p class="text-sm font-semibold text-gray-700 mb-6">Send money to manually verified Bank Accounts (Penny Drop passed).</p>
                        <button onclick="processPayment('Account')" class="w-full bg-blue-600 text-white font-black py-3 rounded shadow-lg hover:bg-blue-700 transition"><i class="fa-solid fa-paper-plane mr-2"></i> Process A/C Payments Now</button>
                    </div>
                </div>
            </main>

            <!-- NEW: ADMIN PROFILE SECTION -->
            <main id="view-profile" class="admin-page p-6">
                <h2 class="text-2xl font-black mb-6 text-blue-900 border-b-2 border-blue-200 pb-2"><i class="fa-solid fa-user-gear"></i> Admin Profile & Settings</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <!-- Profile Details -->
                    <div class="bg-white p-8 rounded-xl shadow border border-gray-200">
                        <h3 class="font-bold text-xl text-gray-800 mb-6 border-b pb-2">Owner Details</h3>
                        <div class="space-y-4">
                            <div>
                                <label class="text-xs font-bold text-gray-500">Full Name</label>
                                <p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border">Kulu Sutar</p>
                            </div>
                            <div>
                                <label class="text-xs font-bold text-gray-500">Registered Mobile No.</label>
                                <p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border"><i class="fa-solid fa-phone text-blue-500 mr-2"></i> 8910223342</p>
                            </div>
                            <div>
                                <label class="text-xs font-bold text-gray-500">Registered Email ID</label>
                                <p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border"><i class="fa-solid fa-envelope text-blue-500 mr-2"></i> admin@kulusutar.in</p>
                            </div>
                        </div>
                    </div>

                    <!-- Change Password Inside Profile -->
                    <div class="bg-white p-8 rounded-xl shadow border border-gray-200">
                        <h3 class="font-bold text-xl text-gray-800 mb-6 border-b pb-2"><i class="fa-solid fa-lock text-gray-600 mr-2"></i> Change Password</h3>
                        <div class="space-y-4">
                            <input type="password" placeholder="Current Password" class="w-full p-3 border rounded outline-none font-bold bg-gray-50 focus:border-blue-500">
                            <input type="password" placeholder="New Password" class="w-full p-3 border rounded outline-none font-bold bg-gray-50 focus:border-blue-500">
                            <input type="password" placeholder="Confirm New Password" class="w-full p-3 border rounded outline-none font-bold bg-gray-50 focus:border-blue-500">
                            <button onclick="updateProfilePassword()" class="w-full bg-blue-700 text-white font-bold py-3 rounded shadow hover:bg-blue-800 mt-2">Update Password</button>
                        </div>
                    </div>
                </div>
            </main>

        </div>
    </div>

    <script>
        // Normal Login Logic
        function login() {
            if(document.getElementById('username').value === 'admin' && document.getElementById('password').value === '12345') {
                document.getElementById('login-screen').classList.add('hidden'); 
                document.getElementById('admin-dashboard').classList.remove('hidden');
            } else { 
                document.getElementById('login-error').classList.remove('hidden'); 
            }
        }

        // Dashboard Switcher
        function switchAdmin(pageId) {
            var pages = document.getElementsByClassName('admin-page');
            for(var i=0; i<pages.length; i++) pages[i].classList.remove('active');
            document.getElementById('view-' + pageId).classList.add('active');
            
            var titles = {
                'dash':'Dashboard',
                'verify':'Final Verification (System Passed)',
                'rejected':'Rejected Vault',
                'vault':'Active Vault',
                'payment':'Payment Management (PayU API)',
                'profile':'Admin Profile & Settings'
            };
            document.getElementById('page-title').innerText = titles[pageId];
        }
        
        function processPayment(type) {
            var confirmAction = confirm("Are you sure you want to process all pending " + type + " payments?");
            if (confirmAction) {
                alert("Processing... Connecting to PayU Gateway.");
                setTimeout(function() { alert("SUCCESS: All " + type + " transfers completed successfully!"); }, 1500);
            }
        }

        // ==========================================
        // FORGOT PASSWORD LOGIC
        // ==========================================
        function showForgotPassword() {
            document.getElementById('login-screen').classList.add('hidden');
            document.getElementById('forgot-pwd-screen').classList.remove('hidden');
        }

        function backToLogin() {
            document.getElementById('forgot-pwd-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            // Reset steps
            document.getElementById('fp-step-1').classList.remove('hidden');
            document.getElementById('fp-step-2').classList.add('hidden');
            document.getElementById('fp-step-3').classList.add('hidden');
        }

        function sendOTP() {
            var email = document.getElementById('fp-email').value;
            if(email === 'admin@kulusutar.in') {
                alert("Email Matched! \\nA Demo OTP has been sent to " + email + ". \\n\\n[ DEMO OTP: 123456 ]");
                document.getElementById('fp-step-1').classList.add('hidden');
                document.getElementById('fp-step-2').classList.remove('hidden');
            } else {
                alert("Error: Email is not registered in the system.");
            }
        }

        function verifyOTP() {
            var otp = document.getElementById('fp-otp').value;
            if(otp === '123456') {
                alert("OTP Verified Successfully!");
                document.getElementById('fp-step-2').classList.add('hidden');
                document.getElementById('fp-step-3').classList.remove('hidden');
            } else {
                alert("Invalid OTP! Please try again.");
            }
        }

        function resetPassword() {
            var p1 = document.getElementById('fp-new-pwd').value;
            var p2 = document.getElementById('fp-conf-pwd').value;
            if(p1 === p2 && p1 !== "") {
                alert("Password changed successfully! You can now login with your new password.");
                backToLogin();
            } else {
                alert("Passwords do not match!");
            }
        }

        // Profile Password Update
        function updateProfilePassword() {
            alert("Password already changed / updated successfully in the system!");
        }
    </script>
</body>
</html>
"""

# ==========================================
# 3. ROUTING
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return public_html_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    return admin_html_design
