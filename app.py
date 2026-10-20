from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. PUBLIC WEBSITE DESIGN (ଆପଣଙ୍କର ପୁରୁଣା ଡିଜାଇନ୍)
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
    </script>
</head>
<body class="bg-gray-50 font-sans text-gray-800 min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-3 cursor-pointer" onclick="switchPage('page-home')">
                <div class="text-blue-800 text-4xl"><i class="fa-solid fa-hands-holding-child"></i></div>
                <div>
                    <h1 class="text-xl md:text-2xl font-extrabold text-blue-900 tracking-tight">Private Social Security Pension Scheme</h1>
                    <p class="text-sm font-bold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            <!-- Menu -->
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
        <!-- HOME PAGE -->
        <div id="page-home" class="page-section active">
            <section class="hero-bg py-16 px-4 border-b">
                <div class="container mx-auto">
                    <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-2xl border-l-8 border-blue-700">
                        <h2 class="text-3xl md:text-4xl font-black text-blue-900 mb-4">Support for Senior Citizens, Widows, Disabled & the Needy</h2>
                        <p class="text-lg text-gray-800 font-semibold mb-6">Pension is not just money, it is respect.</p>
                        <button onclick="switchPage('page-schemes')" class="bg-blue-700 text-white px-8 py-3 rounded-md font-bold shadow-lg hover:bg-blue-800 text-lg">Apply / Learn More</button>
                    </div>
                </div>
            </section>
            <section class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    <!-- Admin Login Button (Redirects to Admin Page) -->
                    <div onclick="window.location.href='/admin'" class="bg-gradient-to-br from-blue-600 to-blue-800 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-user-shield text-5xl mb-4 text-blue-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Admin Login</h3>
                        <p class="text-sm mb-4">Official login for Administration</p>
                        <button class="bg-white text-blue-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="switchPage('page-schemes')" class="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-file-signature text-5xl mb-4 text-green-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Apply Pension</h3>
                        <p class="text-sm mb-4">Apply for New Private Pension Scheme</p>
                        <button class="bg-white text-green-800 font-bold py-2 px-6 rounded-full text-sm">Apply Now <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div class="bg-gradient-to-br from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart text-5xl mb-4 text-orange-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Check Status</h3>
                        <p class="text-sm mb-4">Track your Application Status</p>
                        <button class="bg-white text-orange-800 font-bold py-2 px-6 rounded-full text-sm">Check <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>
            </section>
        </div>

        <!-- ABOUT US -->
        <div id="page-about" class="page-section py-12 bg-white"><div class="container mx-auto px-4 max-w-5xl"><div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-blue-900"><i class="fa-solid fa-circle-info text-blue-600"></i> About Us / ଆମ ବିଷୟରେ</h2><div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4"></div></div><div class="bg-gray-50 rounded-xl shadow-lg overflow-hidden border-2 border-gray-200"><div class="flex border-b-2 border-gray-200 bg-white"><button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-xl">ଓଡ଼ିଆ</button><button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">हिंदी</button><button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">English</button></div><div class="p-8 md:p-12 text-lg"><div id="about-or" class="block"><p class="font-semibold">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ।</p></div><div id="about-hi" class="hidden"><p class="font-semibold">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी पहल है।</p></div><div id="about-en" class="hidden"><p class="font-semibold">This is a 100% private initiative. Pension is respect.</p></div></div></div></div></div>

        <!-- SCHEMES -->
        <div id="page-schemes" class="page-section py-12 bg-gray-50"><div class="container mx-auto px-4 max-w-7xl"><div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-blue-900"><i class="fa-solid fa-list-check text-blue-600"></i> Schemes & Limits</h2><div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4"></div></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"><div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-blue-600"><h3 class="text-2xl font-black text-blue-900">Old Age Pension</h3><p class="text-gray-500 mb-2 border-b pb-2">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p><p class="bg-blue-100 p-2 rounded font-bold mb-2">Age: 55 to 100 Years</p><p class="bg-green-100 p-2 rounded font-bold text-green-800">Amount: ₹3000 / Year</p></div><div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-green-600"><h3 class="text-2xl font-black text-green-900">Disability Pension</h3><p class="text-gray-500 mb-2 border-b pb-2">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p><p class="bg-green-100 p-2 rounded font-bold mb-2">Age: 10 to 100 Years</p><p class="bg-green-100 p-2 rounded font-bold text-green-800">Amount: ₹3500 / Year</p></div><div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-purple-600"><h3 class="text-2xl font-black text-purple-900">Widow Pension</h3><p class="text-gray-500 mb-2 border-b pb-2">ବିଧବା ପେନସନ୍ (Age: 30-55)</p></div></div></div></div>

        <!-- CONDITIONS -->
        <div id="page-conditions" class="page-section py-12 bg-white"><div class="container mx-auto px-4 max-w-5xl"><div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-red-700">Strict Terms & Conditions</h2><div class="w-32 h-1.5 bg-red-600 mx-auto mt-4"></div></div><div class="bg-red-50 border-2 border-red-300 rounded-xl p-8 shadow-xl"><div class="space-y-6"><div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">Non-Refundable Fee (ଫିସ୍ ଫେରସ୍ତ ଅଯୋଗ୍ୟ)</h4><p class="mt-2 text-gray-700">If rejected during verification, fee will <b>NOT BE REFUNDED</b>.</p></div><div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">Absolute Admin Rights</h4><p class="mt-2 text-gray-700">Admin reserves the right to reject any application anytime without any reason. Admin is legally protected.</p></div></div></div></div></div>

        <!-- CONTACT -->
        <div id="page-contact" class="page-section py-12 bg-blue-50"><div class="container mx-auto text-center"><h2 class="text-3xl font-extrabold text-blue-900 mb-6">Contact Us</h2><div class="bg-white p-10 rounded-xl max-w-2xl mx-auto shadow-xl"><p class="text-2xl font-black"><i class="fa-solid fa-phone text-blue-700"></i> 8910223342</p><p class="text-2xl font-black mt-4"><i class="fa-solid fa-envelope text-blue-700"></i> admin@kulusutar.in</p></div></div></div>
    </main>
    <footer class="bg-blue-900 text-white py-6 text-center mt-auto"><p>&copy; 2026 Private Social Security Pension Scheme</p></footer>
</body>
</html>
"""


# ==========================================
# 2. SUPER ADMIN PANEL DESIGN (ନୂଆ ଆଡମିନ୍ ପ୍ୟାନେଲ୍)
# ==========================================
admin_html_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Pension Scheme</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .admin-page { display: none; }
        .admin-page.active { display: block; animation: fadeIn 0.4s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        /* Modal Style */
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
            <input type="text" id="username" placeholder="Username" class="w-full p-3 mb-4 border rounded focus:border-blue-500 outline-none">
            <input type="password" id="password" placeholder="Password" class="w-full p-3 mb-6 border rounded focus:border-blue-500 outline-none">
            <button onclick="login()" class="w-full bg-blue-700 text-white font-bold py-3 rounded hover:bg-blue-800 transition">LOGIN</button>
            <p id="login-error" class="text-red-500 mt-3 hidden text-sm font-bold">Incorrect Details!</p>
            <p class="text-xs text-gray-400 mt-6"><i class="fa-solid fa-lock"></i> Secured by Private Trust</p>
        </div>
    </div>

    <!-- MAIN ADMIN PANEL (Hidden until login) -->
    <div id="admin-dashboard" class="hidden min-h-screen flex">
        
        <!-- SIDEBAR -->
        <div class="w-64 bg-gray-900 text-white flex flex-col shadow-2xl">
            <div class="p-6 border-b border-gray-800 text-center">
                <i class="fa-solid fa-hands-holding-child text-4xl text-blue-400 mb-2"></i>
                <h2 class="font-bold text-lg">Admin Panel</h2>
                <p class="text-xs text-green-400"><i class="fa-solid fa-circle text-[8px]"></i> Online</p>
            </div>
            <nav class="flex-1 p-4 space-y-2">
                <button onclick="switchAdmin('dash')" class="w-full text-left p-3 rounded hover:bg-gray-800 font-semibold"><i class="fa-solid fa-chart-pie w-6"></i> Dashboard</button>
                <button onclick="switchAdmin('verify')" class="w-full text-left p-3 rounded bg-blue-700 font-semibold"><i class="fa-solid fa-file-signature w-6"></i> Document Verify</button>
                <button onclick="switchAdmin('vault')" class="w-full text-left p-3 rounded hover:bg-gray-800 font-semibold"><i class="fa-solid fa-vault w-6"></i> Document Vault</button>
                <button onclick="switchAdmin('payout')" class="w-full text-left p-3 rounded hover:bg-gray-800 font-semibold"><i class="fa-solid fa-money-bill-transfer w-6"></i> PayU Payouts</button>
            </nav>
            <div class="p-4 border-t border-gray-800">
                <button onclick="window.location.href='/'" class="w-full text-left p-2 text-red-400 hover:text-red-300 font-bold"><i class="fa-solid fa-power-off w-6"></i> Logout / Exit</button>
            </div>
        </div>

        <!-- RIGHT CONTENT AREA -->
        <div class="flex-1 flex flex-col h-screen overflow-y-auto">
            <!-- Topbar -->
            <header class="bg-white shadow p-4 flex justify-between items-center border-b-4 border-blue-600">
                <h1 class="text-2xl font-bold text-gray-800" id="page-title">Document Verification</h1>
                <div class="flex items-center text-gray-600 font-bold">
                    <i class="fa-solid fa-user-circle text-2xl mr-2 text-blue-600"></i> Admin (Kulu Sutar)
                </div>
            </header>

            <!-- DASHBOARD SECTION -->
            <main id="view-dash" class="admin-page p-6">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
                        <p class="text-gray-500 font-bold text-sm">Total Applications</p>
                        <h3 class="text-3xl font-black text-gray-800">124</h3>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
                        <p class="text-gray-500 font-bold text-sm">Approved (Eligible)</p>
                        <h3 class="text-3xl font-black text-green-600">89</h3>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow border-l-4 border-red-500">
                        <p class="text-gray-500 font-bold text-sm">Rejected (Failed)</p>
                        <h3 class="text-3xl font-black text-red-600">35</h3>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow border-l-4 border-orange-500">
                        <p class="text-gray-500 font-bold text-sm">Fees Collected</p>
                        <h3 class="text-3xl font-black text-gray-800">₹31,000</h3>
                    </div>
                </div>
            </main>

            <!-- DOCUMENT VERIFICATION SECTION (ଆପଣଙ୍କର ଆଇଡିଆ) -->
            <main id="view-verify" class="admin-page active p-6">
                <h2 class="text-xl font-bold mb-4 text-blue-900"><i class="fa-solid fa-clock-rotate-left"></i> Pending Verifications</h2>
                <div class="bg-white rounded-lg shadow overflow-hidden">
                    <table class="w-full text-left">
                        <thead class="bg-gray-100 border-b">
                            <tr>
                                <th class="p-4 font-bold text-gray-600">App ID</th>
                                <th class="p-4 font-bold text-gray-600">Applicant Name</th>
                                <th class="p-4 font-bold text-gray-600">Scheme</th>
                                <th class="p-4 font-bold text-gray-600">Fee Status</th>
                                <th class="p-4 font-bold text-gray-600">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="border-b hover:bg-gray-50">
                                <td class="p-4 font-bold">#APP-001</td>
                                <td class="p-4">Ramesh Pradhan</td>
                                <td class="p-4">Old Age Pension</td>
                                <td class="p-4"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold">Paid</span></td>
                                <td class="p-4">
                                    <button onclick="openModal('Ramesh Pradhan')" class="bg-blue-600 text-white px-4 py-1 rounded font-bold hover:bg-blue-700">View & Verify</button>
                                </td>
                            </tr>
                            <tr class="border-b hover:bg-gray-50">
                                <td class="p-4 font-bold">#APP-002</td>
                                <td class="p-4">Sita Mahapatra</td>
                                <td class="p-4">Widow Pension</td>
                                <td class="p-4"><span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-bold">Paid</span></td>
                                <td class="p-4">
                                    <button onclick="openModal('Sita Mahapatra')" class="bg-blue-600 text-white px-4 py-1 rounded font-bold hover:bg-blue-700">View & Verify</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </main>

            <!-- DOCUMENT VAULT SECTION (Complain Handling) -->
            <main id="view-vault" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-blue-900"><i class="fa-solid fa-vault"></i> Secure Document Vault</h2>
                <div class="bg-white p-6 rounded-lg shadow mb-6 border-t-4 border-blue-600">
                    <p class="text-gray-600 mb-4 font-bold">Search rejected/approved users to show them their wrong documents if they complain.</p>
                    <div class="flex">
                        <input type="text" placeholder="Enter Aadhaar Number or Phone..." class="flex-1 p-3 border rounded-l outline-none focus:border-blue-500 font-bold">
                        <button class="bg-blue-800 text-white px-6 py-3 rounded-r font-bold"><i class="fa-solid fa-search"></i> Search Vault</button>
                    </div>
                </div>
            </main>

            <!-- PAYU PAYOUTS SECTION -->
            <main id="view-payout" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-green-900"><i class="fa-solid fa-money-bill-transfer"></i> PayU API Payouts</h2>
                <div class="bg-green-50 p-6 rounded-lg border border-green-200 shadow flex items-center justify-between">
                    <div>
                        <h3 class="font-bold text-lg text-green-800">Transfer Monthly Installments</h3>
                        <p class="text-gray-600 text-sm font-semibold">Clicking "Pay Now" will automatically send money to approved bank accounts via PayU.</p>
                    </div>
                    <button class="bg-green-600 text-white px-8 py-3 rounded-lg font-black shadow-lg hover:bg-green-700 text-lg"><i class="fa-solid fa-paper-plane mr-2"></i> Pay Now (API)</button>
                </div>
            </main>

        </div>
    </div>

    <!-- VERIFICATION MODAL -->
    <div id="verify-modal" class="modal">
        <div class="bg-white rounded-xl shadow-2xl w-11/12 md:w-3/4 lg:w-2/3 max-h-[90vh] flex flex-col">
            <div class="p-4 border-b flex justify-between items-center bg-gray-50 rounded-t-xl">
                <h2 class="text-xl font-black text-blue-900">Applicant Verification: <span id="modal-name" class="text-blue-600"></span></h2>
                <button onclick="closeModal()" class="text-red-500 font-bold text-2xl hover:text-red-700">&times;</button>
            </div>
            
            <div class="p-6 flex-1 overflow-y-auto flex flex-col md:flex-row gap-6">
                <!-- Details Side -->
                <div class="md:w-1/3 space-y-4">
                    <div class="bg-gray-100 p-4 rounded border">
                        <p class="text-xs text-gray-500 font-bold">Aadhaar Number</p>
                        <p class="font-black text-lg">XXXX-XXXX-1234</p>
                    </div>
                    <div class="bg-gray-100 p-4 rounded border">
                        <p class="text-xs text-gray-500 font-bold">Income Status</p>
                        <p class="font-black text-lg text-green-600">Zero Income (Declared)</p>
                    </div>
                </div>
                <!-- Document Side -->
                <div class="md:w-2/3 border-2 border-dashed border-gray-300 rounded p-4 flex items-center justify-center bg-gray-50">
                    <div class="text-center text-gray-400">
                        <i class="fa-solid fa-file-pdf text-6xl mb-2"></i>
                        <p class="font-bold">Uploaded Documents Display Here</p>
                        <p class="text-sm">(Aadhaar, Age Proof, Photo)</p>
                    </div>
                </div>
            </div>
            
            <div class="p-4 border-t bg-gray-100 rounded-b-xl flex justify-end space-x-4">
                <!-- Reject Button triggers Reason -->
                <button onclick="rejectApp()" class="bg-red-600 text-white px-6 py-2 rounded font-bold hover:bg-red-700 shadow"><i class="fa-solid fa-xmark mr-1"></i> Reject Form</button>
                <button onclick="approveApp()" class="bg-green-600 text-white px-6 py-2 rounded font-bold hover:bg-green-700 shadow"><i class="fa-solid fa-check mr-1"></i> Approve Pension</button>
            </div>
        </div>
    </div>

    <!-- JS Logic -->
    <script>
        // Simple Login
        function login() {
            var user = document.getElementById('username').value;
            var pass = document.getElementById('password').value;
            // Test ID Password (admin / 12345)
            if(user === 'admin' && pass === '12345') {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('admin-dashboard').classList.remove('hidden');
            } else {
                document.getElementById('login-error').classList.remove('hidden');
            }
        }

        // Switch Sidebar Pages
        function switchAdmin(pageId) {
            var pages = document.getElementsByClassName('admin-page');
            for(var i=0; i<pages.length; i++) pages[i].classList.remove('active');
            document.getElementById('view-' + pageId).classList.add('active');
            
            var titles = {
                'dash': 'Admin Dashboard Overview',
                'verify': 'Document Verification',
                'vault': 'Secure Document Vault',
                'payout': 'PayU API Payouts'
            };
            document.getElementById('page-title').innerText = titles[pageId];
        }

        // Modal Logic
        function openModal(name) {
            document.getElementById('modal-name').innerText = name;
            document.getElementById('verify-modal').classList.add('active');
        }
        function closeModal() {
            document.getElementById('verify-modal').classList.remove('active');
        }

        // Action Logic (ଆପଣଙ୍କର ଆଇଡିଆ)
        function approveApp() {
            alert("Application Approved Successfully! Moved to Payouts list.");
            closeModal();
        }
        function rejectApp() {
            // Ask for Reason!
            var reason = prompt("Enter Rejection Reason (e.g., Wrong Aadhaar, Invalid Income):");
            if(reason) {
                alert("Application REJECTED. Reason saved: " + reason + "\\nThis will show to the user on their status page.");
                closeModal();
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# 3. ROUTING (URL CONTROLS)
# ==========================================

# ୱେବସାଇଟ୍ ର ମୁଖ୍ୟ ପୃଷ୍ଠା
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return public_html_design

# ଆଡମିନ୍ ଲଗଇନ୍ ପୃଷ୍ଠା (kulusutar.in/admin)
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    return admin_html_design
