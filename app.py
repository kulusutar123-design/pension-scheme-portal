from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. PUBLIC WEBSITE (FULL FORM & PAYMENT)
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
            alert("System Message: Application is under 2-Day Auto Verification. If rejected, your [Aadhaar Redacted] will be locked for 3 months.");
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
        function generateQRCode() {
            var upiId = document.getElementById('applicant-upi').value;
            if(upiId) {
                document.getElementById('qr-container').classList.remove('hidden');
                alert("QR Code generated successfully for UPI ID: " + upiId);
            } else {
                alert("Please enter a valid UPI ID first.");
            }
        }
        function submitAndPayFee() {
            var confirmPay = confirm("Proceed to Pay ₹100.00 Application Fee via UPI / QR Code?\\nFunds will be credited directly to Admin Wallet Fund.");
            if(confirmPay) {
                alert("Payment Successful! ₹100 added to Admin Wallet Fund.");
                switchPage('page-home');
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
                        <p class="text-lg text-gray-800 font-semibold mb-6">Pension is not just money, it is respect. Dual [Aadhaar Redacted] & Penny Drop Verification Active.</p>
                        <button onclick="switchPage('page-apply')" class="bg-blue-700 text-white px-8 py-3 rounded-md font-bold shadow-lg hover:bg-blue-800 transition text-lg">Apply Now</button>
                    </div>
                </div>
            </section>
            
            <section class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    <div onclick="window.location.href='/admin'" class="bg-gradient-to-br from-blue-600 to-blue-800 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-user-shield text-5xl mb-4 text-blue-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Admin Login</h3>
                        <p class="text-sm mb-4 text-blue-100 font-medium">Official login for Administration</p>
                        <button class="bg-white text-blue-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="switchPage('page-apply')" class="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-file-signature text-5xl mb-4 text-green-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Apply Pension</h3>
                        <p class="text-sm mb-4 text-green-100 font-medium">Fill the Secure Pension Form</p>
                        <button class="bg-white text-green-800 font-bold py-2 px-6 rounded-full text-sm">Apply <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="checkStatusSimulate()" class="bg-gradient-to-br from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart text-5xl mb-4 text-orange-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Check Status</h3>
                        <p class="text-sm mb-4 text-orange-100 font-medium">Track your Application Status</p>
                        <button class="bg-white text-orange-800 font-bold py-2 px-6 rounded-full text-sm">Check <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div class="bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-users text-5xl mb-4 text-purple-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Beneficiary Login</h3>
                        <p class="text-sm mb-4 text-purple-100 font-medium">Dashboard for Approved Beneficiaries</p>
                        <button class="bg-white text-purple-800 font-bold py-2 px-6 rounded-full text-sm">Login <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="switchPage('page-schemes')" class="bg-gradient-to-br from-teal-500 to-teal-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-hand-holding-dollar text-5xl mb-4 text-teal-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Scheme Details</h3>
                        <p class="text-sm mb-4 text-teal-100 font-medium">View Payment Structure & Limits</p>
                        <button class="bg-white text-teal-800 font-bold py-2 px-6 rounded-full text-sm">View <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                    <div onclick="switchPage('page-conditions')" class="bg-gradient-to-br from-red-500 to-red-700 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-triangle-exclamation text-5xl mb-4 text-red-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Strict Rules</h3>
                        <p class="text-sm mb-4 text-red-100 font-medium">Read Terms & Conditions Before Applying</p>
                        <button class="bg-white text-red-800 font-bold py-2 px-6 rounded-full text-sm">Read <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>
            </section>
        </div>

        <!-- FULL APPLICATION FORM PAGE WITH DYNAMIC QR CODE -->
        <div id="page-apply" class="page-section py-12 bg-gray-100">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="bg-white rounded-xl shadow-2xl overflow-hidden border-t-8 border-blue-700">
                    <div class="bg-blue-50 p-6 border-b border-blue-200">
                        <h2 class="text-2xl font-black text-blue-900"><i class="fa-solid fa-file-invoice text-blue-600 mr-2"></i> Social Security Pension Scheme Form</h2>
                        <p class="text-sm text-gray-600 font-bold mt-1">Please fill out the form carefully. System verification will reject any mismatches.</p>
                    </div>
                    <form class="p-8 space-y-6" onsubmit="event.preventDefault(); submitAndPayFee();">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-b pb-6">
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Pension Type <span class="text-red-500">*</span></label>
                                <select class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50 font-bold">
                                    <option>-- Select Pension Type --</option>
                                    <option>Old Age Pension</option>
                                    <option>Widow Pension</option>
                                    <option>Disability Pension</option>
                                    <option>Transgender Pension</option>
                                </select>
                            </div>
                            <div class="flex flex-col">
                                <label class="block text-sm font-bold text-gray-700 mb-1">[Aadhaar Redacted] No <span class="text-red-500">*</span></label>
                                <div class="flex space-x-2">
                                    <input type="text" placeholder="Enter [Aadhaar Redacted] Number" class="flex-1 p-3 border rounded outline-none focus:border-blue-500 bg-gray-50 font-bold">
                                    <button type="button" onclick="alert('Verified successfully!')" class="bg-green-600 text-white px-4 py-2 rounded font-bold hover:bg-green-700 shadow">Verify</button>
                                </div>
                            </div>
                            <div class="flex flex-col">
                                <label class="block text-sm font-bold text-gray-700 mb-1">Mobile Number <span class="text-red-500">*</span></label>
                                <div class="flex space-x-2">
                                    <input type="text" placeholder="Enter Mobile No." class="flex-1 p-3 border rounded outline-none focus:border-blue-500 bg-gray-50 font-bold">
                                    <button type="button" onclick="alert('OTP Sent!')" class="bg-blue-600 text-white px-4 py-2 rounded font-bold hover:bg-blue-700 shadow">Send OTP</button>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-gray-700 mb-1">Enter OTP <span class="text-red-500">*</span></label>
                                <input type="text" placeholder="Enter OTP" class="w-full p-3 border rounded outline-none focus:border-blue-500 bg-gray-50 font-bold">
                            </div>
                        </div>

                        <!-- Payment Option Section with Auto UPI QR Code -->
                        <div class="bg-purple-50 p-6 rounded-lg border-2 border-purple-300">
                            <h3 class="font-black text-lg text-purple-900 mb-3"><i class="fa-solid fa-qrcode mr-2"></i> Application Fee Payment (₹100.00)</h3>
                            <p class="text-sm font-semibold text-gray-700 mb-4">Enter your UPI ID to automatically generate a secure payment QR code.</p>
                            
                            <div class="flex flex-col md:flex-row gap-4 items-center">
                                <input type="text" id="applicant-upi" placeholder="Enter your UPI ID (e.g. user@paytm)" class="flex-1 p-3 border rounded bg-white font-bold outline-none">
                                <button type="button" onclick="generateQRCode()" class="bg-purple-700 text-white px-6 py-3 rounded font-bold hover:bg-purple-800 shadow">Generate QR Code</button>
                            </div>

                            <!-- QR Code Container -->
                            <div id="qr-container" class="hidden mt-6 text-center bg-white p-6 rounded-lg border shadow-inner">
                                <div class="inline-block p-4 bg-gray-100 border-2 border-dashed border-purple-400 rounded-lg">
                                    <i class="fa-solid fa-qrcode text-8xl text-purple-900"></i>
                                    <p class="text-xs font-bold text-gray-600 mt-2">Scan & Pay ₹100 via any UPI App</p>
                                </div>
                                <p class="text-xs text-green-700 font-bold mt-3"><i class="fa-solid fa-check-circle"></i> Funds will be credited directly to Admin Wallet Fund account.</p>
                            </div>
                        </div>

                        <div class="bg-gray-100 p-6 rounded text-center border-2 border-gray-300">
                            <div class="flex justify-center space-x-4">
                                <button type="submit" class="bg-green-600 text-white px-8 py-3 rounded-lg font-black text-lg shadow-lg hover:bg-green-700"><i class="fa-solid fa-credit-card mr-2"></i> Confirm Payment & Submit</button>
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
                <div class="text-center mb-10">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900"><i class="fa-solid fa-list-check mr-2 text-blue-600"></i> Available Schemes & Limits</h2>
                    <p class="text-gray-700 font-bold mt-3 text-lg">Scheme Details & Yearly Pension Amount</p>
                    <div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4 rounded"></div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-blue-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-blue-900 mb-1">Old Age Pension</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-blue-200 text-blue-900 font-bold px-3 py-1 rounded">55 to 100 Years</span></div>
                            <div class="flex justify-between items-center bg-green-50 p-2 rounded border border-green-200"><span class="font-bold text-green-800">Total Amount:</span><span class="font-black text-green-700 text-lg">₹3000 / Year</span></div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-green-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-green-900 mb-1">Disability Pension</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-green-200 text-green-900 font-bold px-3 py-1 rounded">10 to 100 Years</span></div>
                            <div class="flex justify-between items-center bg-green-50 p-2 rounded border border-green-200"><span class="font-bold text-green-800">Total Amount:</span><span class="font-black text-green-700 text-lg">₹3500 / Year</span></div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-purple-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-purple-900 mb-1">Widow Pension</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ବିଧବା ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-purple-200 text-purple-900 font-bold px-3 py-1 rounded">30 to 55 Years</span></div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-pink-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-pink-900 mb-1">Unmarried Woman</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଅବିବାହିତା ମହିଳା</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-pink-200 text-pink-900 font-bold px-3 py-1 rounded">30 to 55 Years</span></div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-red-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-red-900 mb-1">Divorcee Women</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଛାଡପତ୍ର ପାଇଥିବା ମହିଳା</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-red-200 text-red-900 font-bold px-3 py-1 rounded">35 to 55 Years</span></div>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-orange-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-orange-900 mb-1">Transgender</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">କିନ୍ନର ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded"><span class="font-bold text-gray-700">Age Limit:</span><span class="bg-orange-200 text-orange-900 font-bold px-3 py-1 rounded">35 to 55 Years</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONDITIONS -->
        <div id="page-conditions" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-red-700"><i class="fa-solid fa-triangle-exclamation mr-2 text-red-600"></i> Strict Terms & Conditions</h2>
                    <p class="text-red-900 font-bold mt-2 text-xl">ଦୟାକରି ଆବେଦନ କରିବା ପୂର୍ବରୁ ଏହି ନିୟମଗୁଡିକ ଭଲଭାବେ ପଢନ୍ତୁ</p>
                    <div class="w-32 h-1.5 bg-red-600 mx-auto mt-4 rounded"></div>
                </div>
                <div class="bg-red-50 border-2 border-red-300 rounded-xl p-6 md:p-10 shadow-xl relative overflow-hidden">
                    <div class="space-y-6 text-gray-800 text-lg">
                        <div class="bg-white p-5 rounded-lg border border-red-200 shadow-sm flex flex-col md:flex-row items-start">
                            <div class="bg-red-100 p-3 rounded-full mr-4 mb-3 md:mb-0"><i class="fa-solid fa-money-bill-transfer text-red-600 text-2xl"></i></div>
                            <div>
                                <h4 class="font-black text-red-900 text-xl">Non-Refundable Application Fee</h4>
                                <p class="font-semibold mt-2 text-gray-700">Application fee is mandatory. If application is <b class="text-red-600">rejected</b>, the fee will <b class="text-red-600 underline">NOT BE REFUNDED</b>.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONTACT -->
        <div id="page-contact" class="page-section py-12 bg-blue-50">
            <div class="container mx-auto px-4 max-w-4xl text-center">
                <i class="fa-solid fa-headset text-6xl text-blue-700 mb-6"></i>
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-6">Contact & Support</h2>
                <div class="bg-white p-10 rounded-xl shadow-xl border-t-8 border-blue-700">
                    <p class="text-xl font-bold text-gray-700 mb-8">For any queries regarding the Private Social Security Pension Scheme, please reach out to us:</p>
                    <div class="flex flex-col md:flex-row justify-center items-center space-y-6 md:space-y-0 md:space-x-12">
                        <div class="flex items-center text-2xl font-black text-blue-900"><div class="bg-blue-100 p-4 rounded-full mr-4"><i class="fa-solid fa-phone text-blue-700"></i></div>8910223342</div>
                        <div class="flex items-center text-2xl font-black text-blue-900"><div class="bg-blue-100 p-4 rounded-full mr-4"><i class="fa-solid fa-envelope text-blue-700"></i></div>admin@kulusutar.in</div>
                    </div>
                </div>
            </div>
        </div>

    </main>
    <footer class="bg-blue-900 text-white py-6 border-t-4 border-blue-700 mt-auto text-center">
        <p class="font-bold">&copy; 2026 Private Social Security Pension Scheme</p>
    </footer>
</body>
</html>
"""

# ==========================================
# 2. SUPER ADMIN PANEL WITH BANK ACCOUNT & UPI SETTINGS TABLE
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
    </style>
</head>
<body class="bg-gray-100 font-sans">

    <!-- LOGIN SCREEN -->
    <div id="login-screen" class="min-h-screen flex items-center justify-center bg-gray-900 absolute inset-0 z-50">
        <div class="absolute top-4 left-4">
            <button onclick="window.location.href='/'" class="bg-white/20 text-white px-4 py-2 rounded-full font-bold hover:bg-white/35 backdrop-blur"><i class="fa-solid fa-arrow-left mr-2"></i> Back to Home</button>
        </div>
        <div class="bg-white p-10 rounded-xl shadow-2xl w-96 text-center">
            <i class="fa-solid fa-user-shield text-6xl text-blue-700 mb-4"></i>
            <h2 class="text-2xl font-bold mb-6 text-gray-800">Admin Login</h2>
            <input type="text" id="username" placeholder="Username" class="w-full p-3 mb-4 border rounded outline-none font-bold">
            <input type="password" id="password" placeholder="Password" class="w-full p-3 mb-4 border rounded outline-none font-bold">
            <button onclick="login()" class="w-full bg-blue-700 text-white font-bold py-3 rounded hover:bg-blue-800 shadow">LOGIN</button>
            <p id="login-error" class="text-red-500 mt-3 hidden text-sm font-bold">Incorrect Details!</p>
        </div>
    </div>

    <!-- MAIN ADMIN PANEL -->
    <div id="admin-dashboard" class="hidden min-h-screen flex">
        <div class="w-64 bg-gray-900 text-white flex flex-col shadow-2xl h-screen sticky top-0 overflow-y-auto">
            <div class="p-6 border-b border-gray-800 text-center">
                <i class="fa-solid fa-user-tie text-4xl text-blue-400 mb-2"></i>
                <h2 class="font-bold text-lg">Super Admin</h2>
            </div>
            <nav class="flex-1 p-4 space-y-2 text-sm font-bold">
                <button onclick="switchAdmin('dash')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-chart-pie w-6"></i> Dashboard</button>
                <button onclick="switchAdmin('verify')" class="w-full text-left p-3 rounded hover:bg-gray-800"><i class="fa-solid fa-check-double w-6"></i> Verify (System Passed)</button>
                <button onclick="switchAdmin('rejected')" class="w-full text-left p-3 rounded text-red-400 hover:bg-gray-800"><i class="fa-solid fa-folder-closed w-6"></i> Rejected Vault</button>
                <button onclick="switchAdmin('payment')" class="w-full text-left p-3 rounded bg-green-700 hover:bg-green-600"><i class="fa-solid fa-building-columns w-6"></i> Payment & Wallet Fund</button>
                <button onclick="switchAdmin('profile')" class="w-full text-left p-3 rounded hover:bg-gray-800 mt-6 border-t border-gray-700 pt-4"><i class="fa-solid fa-user-gear w-6"></i> Admin Profile</button>
            </nav>
            <div class="p-4 border-t border-gray-800 bg-gray-900 space-y-2">
                <button onclick="window.location.href='/'" class="w-full bg-gray-800 text-white p-2 rounded hover:bg-gray-700 font-bold"><i class="fa-solid fa-house w-6"></i> Back to Home</button>
                <button onclick="window.location.reload()" class="w-full text-left p-2 text-red-500 font-bold hover:bg-gray-800 rounded"><i class="fa-solid fa-power-off w-6"></i> Logout</button>
            </div>
        </div>

        <div class="flex-1 flex flex-col h-screen overflow-y-auto">
            <header class="bg-white shadow p-4 flex justify-between border-b-4 border-blue-600">
                <h1 class="text-2xl font-bold text-gray-800" id="page-title">Dashboard</h1>
                <div class="flex items-center text-gray-600 font-bold">Kulu Sutar</div>
            </header>

            <main id="view-dash" class="admin-page active p-6">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded shadow border-l-4 border-blue-500"><p class="text-gray-500 font-bold">Total Forms</p><h3 class="text-3xl font-black">124</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-green-500"><p class="text-gray-500 font-bold">System Passed</p><h3 class="text-3xl font-black text-green-600">89</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-red-500"><p class="text-gray-500 font-bold">Rejected / Locked</p><h3 class="text-3xl font-black text-red-600">35</h3></div>
                    <div class="bg-white p-6 rounded shadow border-l-4 border-orange-500 bg-orange-50"><p class="text-orange-800 font-bold">Wallet Fund Balance</p><h3 class="text-3xl font-black text-orange-600">₹31,000</h3></div>
                </div>
            </main>

            <main id="view-verify" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-blue-900">Verification List</h2>
            </main>

            <main id="view-rejected" class="admin-page p-6">
                <h2 class="text-xl font-bold mb-4 text-red-900">Rejected Vault</h2>
            </main>

            <!-- PAYMENT MANAGEMENT & BANK / UPI SETTINGS TABLE -->
            <main id="view-payment" class="admin-page p-6">
                <h2 class="text-2xl font-black mb-6 text-green-900 border-b-2 border-green-200 pb-2"><i class="fa-solid fa-wallet"></i> Admin Wallet & Bank Account Settings</h2>
                
                <div class="bg-gradient-to-r from-gray-900 to-gray-800 p-8 rounded-xl shadow-2xl mb-8 flex flex-col md:flex-row justify-between items-center border-l-8 border-green-500">
                    <div class="text-white mb-4 md:mb-0">
                        <p class="text-gray-400 font-bold uppercase tracking-wider text-sm mb-1">System Nodal Account</p>
                        <h3 class="text-5xl font-black">₹ 31,000<span class="text-xl text-gray-400 font-bold">.00</span></h3>
                        <p class="text-green-400 font-semibold text-sm mt-2">Funds collected from Application Fees (₹100/form)</p>
                    </div>
                    <div class="flex space-x-4">
                        <button onclick="alert('Funds transferred to your main Bank Account successfully!')" class="bg-white text-gray-900 px-6 py-3 rounded font-black shadow hover:bg-gray-100"><i class="fa-solid fa-building-columns mr-2"></i> Withdraw Wallet to Bank</button>
                    </div>
                </div>

                <!-- ADMIN RECEIVING ACCOUNT SETTINGS TABLE -->
                <div class="bg-white p-6 rounded-lg shadow border border-gray-200 mb-6">
                    <h3 class="font-bold text-lg text-gray-800 mb-4"><i class="fa-solid fa-table text-blue-600 mr-2"></i> Admin Receiving Bank Account & UPI Setup (For Application Fees)</h3>
                    
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-gray-100 border-b text-sm">
                                    <th class="p-3 border">Account Holder Name</th>
                                    <th class="p-3 border">Bank Account Number</th>
                                    <th class="p-3 border">IFSC Code</th>
                                    <th class="p-3 border">UPI ID (For QR Generation)</th>
                                    <th class="p-3 border text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="p-3 border"><input type="text" id="admin-name" value="Kulu Sutar" class="w-full p-2 border rounded font-bold bg-gray-50"></td>
                                    <td class="p-3 border"><input type="text" id="admin-acc" value="12345678901" class="w-full p-2 border rounded font-bold bg-gray-50"></td>
                                    <td class="p-3 border"><input type="text" id="admin-ifsc" value="SBIN0001234" class="w-full p-2 border rounded font-bold bg-gray-50"></td>
                                    <td class="p-3 border"><input type="text" id="admin-upi" value="kulusutar@sbi" class="w-full p-2 border rounded font-bold bg-gray-50"></td>
                                    <td class="p-3 border text-center">
                                        <button onclick="alert('Admin Bank & UPI settings updated successfully! QR codes will now send funds to this account.')" class="bg-green-600 text-white px-4 py-2 rounded font-bold text-sm shadow hover:bg-green-700">Save</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <p class="text-xs text-gray-500 mt-2 font-bold"><i class="fa-solid fa-info-circle"></i> When applicants scan the QR code and pay the fee, the amount will accumulate in your Wallet Fund above, and you can withdraw it anytime.</p>
                </div>
            </main>

            <main id="view-profile" class="admin-page p-6">
                <h2 class="text-2xl font-black mb-6 text-blue-900 border-b-2 border-blue-200 pb-2">Admin Profile</h2>
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
            var titles = {'dash':'Dashboard','verify':'Final Verification','rejected':'Rejected Vault','payment':'Wallet Fund & Bank Settings','profile':'Admin Profile'};
            document.getElementById('page-title').innerText = titles[pageId];
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
