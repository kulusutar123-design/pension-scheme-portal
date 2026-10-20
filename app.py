from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. PUBLIC WEBSITE DESIGN (ALL 6 BOXES RESTORED)
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
            alert("System Message: Application is under 2-Day Auto Verification. If rejected, your Aadhaar will be locked for 3 months.");
        }
        function toggleBankFields() {
            var dbtStatus = document.getElementById('dbt-select').value;
            var manualBankDiv = document.getElementById('manual-bank-details');
            if(dbtStatus === 'no') {
                manualBankDiv.classList.remove('hidden');
            } else {
                manualBankDiv.classList.add('hidden');
            }
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
                <button id="link-page-apply" onclick="switchPage('page-apply')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-file-signature mr-1"></i> Apply</button>
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
                        <h2 class="text-3xl md:text-4xl font-black text-blue-900 mb-4 leading-tight">Support for Senior Citizens, Widows, Disabled and the Needy</h2>
                        <p class="text-lg text-gray-800 font-semibold mb-6">Pension is not just money, it is respect. Dual Aadhaar & Penny Drop Verification Active.</p>
                        <button onclick="switchPage('page-apply')" class="bg-blue-700 text-white px-8 py-3 rounded-md font-bold shadow-lg hover:bg-blue-800 transition text-lg">Apply Now</button>
                    </div>
                </div>
            </section>
            
            <section class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <!-- ALL 6 BOXES RESTORED HERE -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    <!-- Admin Login -->
                    <div onclick="window.location.href='/admin'" class="bg-gradient-to-br from-blue-600 to-blue-800 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-user-shield text-5xl mb-4 text-blue-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Admin Login</h3>
                        <p class="text-sm mb-4 text-blue-100 font-medium">Official login for Administration</p>
                        <button class="bg-white text-blue-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <!-- Apply Form Link -->
                    <div onclick="switchPage('page-apply')" class="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-file-signature text-5xl mb-4 text-green-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Apply Pension</h3>
                        <p class="text-sm mb-4 text-green-100 font-medium">Fill the Secure Pension Form</p>
                        <button class="bg-white text-green-800 font-bold py-2 px-6 rounded-full text-sm">Apply <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <!-- Status Check -->
                    <div onclick="checkStatusSimulate()" class="bg-gradient-to-br from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart text-5xl mb-4 text-orange-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Check Status</h3>
                        <p class="text-sm mb-4 text-orange-100 font-medium">Track your Application Status</p>
                        <button class="bg-white text-orange-800 font-bold py-2 px-6 rounded-full text-sm">Check <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <!-- Beneficiary Login (Restored) -->
                    <div class="bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-users text-5xl mb-4 text-purple-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Beneficiary Login</h3>
                        <p class="text-sm mb-4 text-purple-100 font-medium">Dashboard for Approved Beneficiaries</p>
                        <button class="bg-white text-purple-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <!-- Scheme Details (Restored) -->
                    <div onclick="switchPage('page-schemes')" class="bg-gradient-to-br from-teal-500 to-teal-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-hand-holding-dollar text-5xl mb-4 text-teal-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Scheme Details</h3>
                        <p class="text-sm mb-4 text-teal-100 font-medium">View Payment Structure & Limits</p>
                        <button class="bg-white text-teal-800 font-bold py-2 px-6 rounded-full text-sm">View <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <!-- Strict Rules (Restored) -->
                    <div onclick="switchPage('page-conditions')" class="bg-gradient-to-br from-red-500 to-red-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-triangle-exclamation text-5xl mb-4 text-red-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Strict Rules</h3>
                        <p class="text-sm mb-4 text-red-100 font-medium">Read Terms & Conditions Before Applying</p>
                        <button class="bg-white text-red-800 font-bold py-2 px-6 rounded-full text-sm">Read <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>
            </section>
        </div>

        <!-- FULL APPLICATION FORM PAGE -->
        <div id="page-apply" class="page-section py-12 bg-gray-100">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="bg-white rounded-xl shadow-2xl overflow-hidden border-t-8 border-blue-700">
                    <div class="bg-blue-50 p-6 border-b border-blue-200">
                        <h2 class="text-2xl font-black text-blue-900"><i class="fa-solid fa-file-invoice text-blue-600 mr-2"></i> Social Security Pension Scheme Form</h2>
                        <p class="text-sm text-gray-600 font-bold mt-1">Please fill out the form carefully. System verification will reject any mismatches.</p>
                    </div>
                    <form class="p-8 space-y-6">
                        <!-- Section 1: Basic & Identity -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-b pb-6">
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Pension Type <span class="text-red-500">*</span></label>
                                <select class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                                    <option>-- Select Pension Type --</option>
                                    <option>Old Age Pension</option>
                                    <option>Widow Pension</option>
                                    <option>Disability Pension</option>
                                </select>
                            </div>
                            <div class="flex flex-col">
                                <label class="block text-sm font-bold text-gray-700 mb-1">Aadhaar No <span class="text-red-500">*</span></label>
                                <div class="flex space-x-2">
                                    <input type="text" placeholder="Enter Aadhaar Number" class="flex-1 p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                                    <button type="button" class="bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700">Verify</button>
                                </div>
                            </div>
                            <!-- OTP Verification Feature -->
                            <div class="flex flex-col">
                                <label class="block text-sm font-bold text-gray-700 mb-1">Mobile Number (Aadhaar Linked Preferred) <span class="text-red-500">*</span></label>
                                <div class="flex space-x-2">
                                    <input type="text" placeholder="Enter Mobile No." class="flex-1 p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                                    <button type="button" class="bg-blue-600 text-white px-4 py-2 rounded font-bold hover:bg-blue-700">Send OTP</button>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Enter OTP <span class="text-red-500">*</span></label>
                                <input type="text" placeholder="OTP" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                            </div>
                        </div>

                        <!-- Section 2: Personal Details -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-b pb-6">
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Name As Per Aadhaar <span class="text-red-500">*</span></label>
                                <input type="text" placeholder="Exact spelling as Aadhaar" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Father's/Spouse Name <span class="text-red-500">*</span></label>
                                <input type="text" placeholder="Full Name" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                            </div>
                            <div class="flex gap-4">
                                <div class="flex-1">
                                    <label class="block text-sm font-bold text-gray-700 mb-1">Age <span class="text-red-500">*</span></label>
                                    <input type="number" placeholder="Years" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50">
                                </div>
                                <div class="flex-1">
                                    <label class="block text-sm font-bold text-gray-700 mb-1">Age Proof (PDF) <span class="text-red-500">*</span></label>
                                    <input type="file" class="w-full p-2 border rounded outline-none bg-gray-50 text-sm">
                                </div>
                            </div>
                            <div class="flex gap-4 items-center">
                                <div class="w-24 h-24 bg-gray-200 border-2 border-dashed border-gray-400 rounded flex items-center justify-center text-gray-500 text-3xl"><i class="fa-solid fa-user"></i></div>
                                <div class="flex-1">
                                    <label class="block text-sm font-bold text-gray-700 mb-1">Upload Photo (JPG) <span class="text-red-500">*</span></label>
                                    <input type="file" accept="image/*" class="w-full p-2 border rounded bg-gray-50 text-sm">
                                </div>
                            </div>
                        </div>

                        <!-- Section 3: Income & Government API Matching -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-b pb-6 bg-yellow-50 p-4 rounded border border-yellow-200">
                            <div>
                                <label class="block text-sm font-bold text-gray-800 mb-1">Income Certificate Number / Barcode <span class="text-red-500">*</span></label>
                                <input type="text" placeholder="E.g., INC-2026-XXXX" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-white">
                                <p class="text-xs text-red-600 mt-1 font-bold"><i class="fa-solid fa-triangle-exclamation"></i> System will auto-verify this with Govt API.</p>
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-gray-800 mb-1">Upload Income Certificate (PDF) <span class="text-red-500">*</span></label>
                                <input type="file" accept=".pdf" class="w-full p-2 border rounded outline-none bg-white text-sm">
                            </div>
                        </div>

                        <!-- Section 4: Bank Details -->
                        <div class="border-b pb-6 bg-blue-50 p-4 rounded border border-blue-200">
                            <h3 class="font-bold text-blue-900 mb-4 border-b border-blue-200 pb-2"><i class="fa-solid fa-building-columns"></i> Bank Account Information</h3>
                            <div class="mb-4">
                                <label class="block text-sm font-bold text-gray-800 mb-1">Is your Bank Account linked with Aadhaar (DBT Active)? <span class="text-red-500">*</span></label>
                                <select id="dbt-select" onchange="toggleBankFields()" class="w-full md:w-1/2 p-3 border rounded outline-none focus:border-blue-500 bg-white font-bold">
                                    <option value="yes">Yes, Aadhaar is Linked (Secure DBT Transfer)</option>
                                    <option value="no">No / I don't know (Enter Manual Details)</option>
                                </select>
                            </div>
                            <div id="manual-bank-details" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 hidden bg-white p-4 rounded border shadow-sm">
                                <div><label class="block text-sm font-bold text-gray-700 mb-1">Account Holder Name <span class="text-red-500">*</span></label><input type="text" placeholder="As per Bank Passbook" class="w-full p-3 border rounded bg-gray-50"></div>
                                <div><label class="block text-sm font-bold text-gray-700 mb-1">Account Number <span class="text-red-500">*</span></label><input type="text" placeholder="Enter Bank A/C No." class="w-full p-3 border rounded bg-gray-50"></div>
                                <div><label class="block text-sm font-bold text-gray-700 mb-1">Bank Name & Branch <span class="text-red-500">*</span></label><input type="text" placeholder="E.g., SBI, Link Road" class="w-full p-3 border rounded bg-gray-50"></div>
                                <div><label class="block text-sm font-bold text-gray-700 mb-1">Upload Passbook Front Page <span class="text-red-500">*</span></label><input type="file" accept="image/*,.pdf" class="w-full p-2 border rounded bg-gray-50 text-sm"></div>
                            </div>
                        </div>

                        <!-- Section 5: Payment & Submit -->
                        <div class="bg-gray-100 p-6 rounded text-center border-2 border-gray-300">
                            <h3 class="text-xl font-black text-gray-800 mb-2">Application Fee: ₹100.00</h3>
                            <p class="text-sm text-red-600 font-bold mb-4">Fee is 100% NON-REFUNDABLE. If documents are fake, your Aadhaar will be locked for 3 months.</p>
                            <div class="flex justify-center space-x-4">
                                <button type="button" class="bg-green-600 text-white px-8 py-3 rounded-lg font-black text-lg shadow-lg hover:bg-green-700"><i class="fa-solid fa-credit-card mr-2"></i> Pay Fee & Submit</button>
                                <button type="reset" class="bg-gray-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-gray-600">Reset Form</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- ABOUT US -->
        <div id="page-about" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-blue-900"><i class="fa-solid fa-circle-info text-blue-600"></i> About Us / ଆମ ବିଷୟରେ</h2><div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4"></div></div>
                <div class="bg-gray-50 rounded-xl shadow-lg overflow-hidden border-2 border-gray-200">
                    <div class="flex border-b-2 border-gray-200 bg-white"><button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-xl">ଓଡ଼ିଆ</button><button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">हिंदी</button><button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-xl border-l-2">English</button></div>
                    <div class="p-8 md:p-12 text-lg">
                        <div id="about-or" class="block"><p class="font-semibold">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ।</p></div>
                        <div id="about-hi" class="hidden"><p class="font-semibold">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी पहल है।</p></div>
                        <div id="about-en" class="hidden"><p class="font-semibold">This is a 100% private initiative. Pension is respect.</p></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SCHEMES -->
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

        <!-- CONDITIONS -->
        <div id="page-conditions" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10"><h2 class="text-3xl font-extrabold text-red-700">Strict Terms & Conditions</h2><div class="w-32 h-1.5 bg-red-600 mx-auto mt-4"></div></div>
                <div class="bg-red-50 border-2 border-red-300 rounded-xl p-8 shadow-xl">
                    <div class="space-y-6">
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">2-Day Verification & Name Matching</h4><p class="mt-2 text-gray-700 font-bold">All applications undergo a 2-day API check. We use Penny Drop test to match bank name with Aadhaar name exactly. Mismatch = Reject.</p></div>
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">3-Month Ban & Re-Apply Fee</h4><p class="mt-2 text-gray-700">If rejected due to fake documents, your Aadhaar is locked for 3 months. You must pay the fee again to re-apply.</p></div>
                        <div class="bg-white p-5 rounded-lg border border-red-200"><h4 class="font-black text-red-900 text-xl">Non-Refundable Fee</h4><p class="mt-2 text-gray-700">Application fees are absolutely NON-REFUNDABLE under any circumstance.</p></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONTACT -->
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
# 2. SUPER ADMIN PANEL WITH WALLET FUND & FORGOT PWD
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
        <div class="absolute top-4 left-4">
            <!-- BACK TO HOME BUTTON -->
            <button onclick="window.location.href='/'" class="bg-white/20 text-white px-4 py-2 rounded-full font-bold hover:bg-white/30 backdrop-blur"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</button>
        </div>
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
        <div class="w-64 bg-gray-900 text-white flex flex-col shadow-2xl h-screen sticky top-0 overflow-y-auto">
            <div class="p-6 border-b border-gray-800 text-center">
                <i class="fa-solid fa-user-tie text-4xl text-blue-400 mb-2"></i>
                <h2 class="font-bold text-lg">Super Admin</h2>
            </div>
            <nav class="flex-1 p-4 space-y-2 text-sm font-bold">
                <button onclick="switchAdmin('dash')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-chart-pie w-6"></i> Dashboard</button>
                <button onclick="switchAdmin('verify')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-check-double w-6"></i> Verify (System Passed)</button>
                <button onclick="switchAdmin('rejected')" class="w-full text-left p-3 rounded text-red-400 hover:bg-gray-800"><i class="fa-solid fa-folder-closed w-6"></i> Rejected Vault</button>
                <button onclick="switchAdmin('vault')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-vault w-6"></i> Active Vault</button>
                <button onclick="switchAdmin('payment')" class="w-full text-left p-3 rounded bg-green-700 hover:bg-green-600"><i class="fa-solid fa-building-columns w-6"></i> Payment & Wallet Fund</button>
                <button onclick="switchAdmin('profile')" class="w-full text-left p-3 rounded hover:bg-gray-800 mt-6 border-t border-gray-700 pt-4"><i class="fa-solid fa-user-gear w-6"></i> Admin Profile</button>
            </nav>
            <div class="p-4 border-t border-gray-800 bg-gray-900 space-y-2">
                <button onclick="window.location.href='/'" class="w-full bg-gray-800 text-white p-2 rounded hover:bg-gray-700 font-bold"><i class="fa-solid fa-house w-6"></i> Back to Home</button>
                <button onclick="window.location.reload()" class="w-full text-left p-2 text-red-500 font-bold hover:bg-gray-800 rounded"><i class="fa-solid fa-power-off w-6"></i> Logout</button>
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
                    <div class="bg-white p-6 rounded shadow border-l-4 border-orange-500 bg-orange-50"><p class="text-orange-800 font-bold">Wallet Fund Balance</p><h3 class="text-3xl font-black text-orange-600">₹31,000</h3></div>
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
                                <td class="p-4"><span class="bg-blue-100 text-blue-800 px-2 py-1 text-xs font-bold rounded"><i class="fa-solid fa-robot"></i> All Docs Matched</span></td>
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
                    <p class="font-bold text-red-800 mb-2">Users banned for mismatch in spelling/fake docs. Fee forfeited.</p>
                </div>
            </main>
            
            <main id="view-vault" class="admin-page p-6"><h2 class="text-xl font-bold mb-4">Active Vault</h2></main>

            <!-- PAYMENT MANAGEMENT & WALLET FUND -->
            <main id="view-payment" class="admin-page p-6">
                <h2 class="text-2xl font-black mb-6 text-green-900 border-b-2 border-green-200 pb-2"><i class="fa-solid fa-wallet"></i> Admin Wallet & Fund Management</h2>
                
                <div class="bg-gradient-to-r from-gray-900 to-gray-800 p-8 rounded-xl shadow-2xl mb-8 flex flex-col md:flex-row justify-between items-center border-l-8 border-green-500">
                    <div class="text-white mb-4 md:mb-0">
                        <p class="text-gray-400 font-bold uppercase tracking-wider text-sm mb-1"><i class="fa-solid fa-building-columns mr-2"></i> System Nodal Account</p>
                        <h3 class="text-5xl font-black">₹ 31,000<span class="text-xl text-gray-400 font-bold">.00</span></h3>
                        <p class="text-green-400 font-semibold text-sm mt-2"><i class="fa-solid fa-arrow-trend-up"></i> Funds collected from Application Fees</p>
                    </div>
                    <div class="flex space-x-4">
                        <button onclick="alert('Funds transferring to your personal Bank Account...\\nSuccess!')" class="bg-white text-gray-900 px-6 py-3 rounded font-black shadow hover:bg-gray-100"><i class="fa-solid fa-building-columns mr-2"></i> Withdraw to Bank</button>
                    </div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow border border-gray-200 mb-6">
                    <h3 class="font-bold text-lg text-gray-800 mb-3"><i class="fa-solid fa-key text-blue-500"></i> PayU Gateway API Configuration</h3>
                    <div class="flex flex-col md:flex-row gap-4">
                        <input type="password" value="payu_live_xxxx_yyyy" class="flex-1 p-3 border rounded bg-gray-50 outline-none font-bold text-sm">
                        <button onclick="alert('API Key Saved & Connected Successfully!')" class="bg-gray-800 text-white px-6 py-2 rounded font-bold shadow hover:bg-gray-900">Connected</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-green-50 p-6 rounded-lg shadow border-2 border-green-400 relative overflow-hidden">
                        <div class="absolute top-0 right-0 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">Highly Secure</div>
                        <h3 class="font-black text-xl text-green-800 mb-2"><i class="fa-solid fa-fingerprint"></i> Aadhaar DBT Payouts</h3>
                        <p class="text-sm font-semibold text-gray-700 mb-6">Deduct from Wallet and send directly to Aadhaar-linked accounts.</p>
                        <button onclick="processPayment('DBT')" class="w-full bg-green-600 text-white font-black py-3 rounded shadow-lg hover:bg-green-700 transition"><i class="fa-solid fa-paper-plane mr-2"></i> Pay Pensions from Wallet</button>
                    </div>
                    <div class="bg-blue-50 p-6 rounded-lg shadow border-2 border-blue-400 relative overflow-hidden">
                        <div class="absolute top-0 right-0 bg-blue-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">Manual Entry</div>
                        <h3 class="font-black text-xl text-blue-800 mb-2"><i class="fa-solid fa-money-check-dollar"></i> Bank A/C Payouts</h3>
                        <p class="text-sm font-semibold text-gray-700 mb-6">Deduct from Wallet and send to manually verified Bank Accounts.</p>
                        <button onclick="processPayment('Account')" class="w-full bg-blue-600 text-white font-black py-3 rounded shadow-lg hover:bg-blue-700 transition"><i class="fa-solid fa-paper-plane mr-2"></i> Pay Pensions from Wallet</button>
                    </div>
                </div>
            </main>

            <!-- ADMIN PROFILE SECTION -->
            <main id="view-profile" class="admin-page p-6">
                <h2 class="text-2xl font-black mb-6 text-blue-900 border-b-2 border-blue-200 pb-2"><i class="fa-solid fa-user-gear"></i> Admin Profile & Settings</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="bg-white p-8 rounded-xl shadow border border-gray-200">
                        <h3 class="font-bold text-xl text-gray-800 mb-6 border-b pb-2">Owner Details</h3>
                        <div class="space-y-4">
                            <div><label class="text-xs font-bold text-gray-500">Full Name</label><p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border">Kulu Sutar</p></div>
                            <div><label class="text-xs font-bold text-gray-500">Registered Mobile No.</label><p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border"><i class="fa-solid fa-phone text-blue-500 mr-2"></i> 8910223342</p></div>
                            <div><label class="text-xs font-bold text-gray-500">Registered Email ID</label><p class="text-lg font-black text-gray-900 bg-gray-50 p-2 rounded border"><i class="fa-solid fa-envelope text-blue-500 mr-2"></i> admin@kulusutar.in</p></div>
                        </div>
                    </div>
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
        function login() {
            if(document.getElementById('username').value === 'admin' && document.getElementById('password').value === '12345') {
                document.getElementById('login-screen').classList.add('hidden'); 
                document.getElementById('admin-dashboard').classList.remove('hidden');
            } else { 
                document.getElementById('login-error').classList.remove('hidden'); 
            }
        }

        function switchAdmin(pageId) {
            var pages = document.getElementsByClassName('admin-page');
            for(var i=0; i<pages.length; i++) pages[i].classList.remove('active');
            document.getElementById('view-' + pageId).classList.add('active');
            
            var titles = {
                'dash':'Dashboard',
                'verify':'Final Verification (System Passed)',
                'rejected':'Rejected Vault',
                'vault':'Active Vault',
                'payment':'Wallet Fund & Payout Management',
                'profile':'Admin Profile & Settings'
            };
            document.getElementById('page-title').innerText = titles[pageId];
        }
        
        function processPayment(type) {
            var confirmAction = confirm("Deduct funds from Wallet and process all pending " + type + " payments?");
            if (confirmAction) {
                alert("Processing... Connecting to PayU Gateway.");
                setTimeout(function() { alert("SUCCESS: All " + type + " transfers completed successfully! Wallet balance updated."); }, 1500);
            }
        }

        // FORGOT PASSWORD LOGIC
        function showForgotPassword() {
            document.getElementById('login-screen').classList.add('hidden');
            document.getElementById('forgot-pwd-screen').classList.remove('hidden');
        }
        function backToLogin() {
            document.getElementById('forgot-pwd-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
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
            } else { alert("Invalid OTP! Please try again."); }
        }
        function resetPassword() {
            var p1 = document.getElementById('fp-new-pwd').value;
            var p2 = document.getElementById('fp-conf-pwd').value;
            if(p1 === p2 && p1 !== "") {
                alert("Password changed successfully! You can now login with your new password.");
                backToLogin();
            } else { alert("Passwords do not match!"); }
        }
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
