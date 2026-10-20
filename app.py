from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Social Security Pension Scheme</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg {
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .tab-btn.active {
            background-color: #1d4ed8; 
            color: white;
        }
        /* Hide sections by default, JavaScript will toggle this */
        .page-section {
            display: none;
            animation: fadeIn 0.5s;
        }
        .page-section.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        /* Menu Active state */
        .nav-link.active-link {
            color: #1d4ed8; /* blue-700 */
            border-bottom: 3px solid #1d4ed8;
            padding-bottom: 4px;
        }
    </style>
    
    <script>
        // Function to switch between main pages (Home, About, Schemes, Conditions, Contact)
        function switchPage(pageId) {
            // Hide all pages
            var pages = document.getElementsByClassName('page-section');
            for(var i = 0; i < pages.length; i++) {
                pages[i].classList.remove('active');
            }
            // Show the selected page
            document.getElementById(pageId).classList.add('active');
            
            // Update menu link styles
            var links = document.getElementsByClassName('nav-link');
            for(var i = 0; i < links.length; i++) {
                links[i].classList.remove('active-link');
            }
            document.getElementById('link-' + pageId).classList.add('active-link');
        }

        // Function for Language Tabs in About Us
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

    <!-- Top Header / Navbar -->
    <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-3 cursor-pointer" onclick="switchPage('page-home')">
                <div class="text-blue-800 text-4xl">
                    <i class="fa-solid fa-hands-holding-child"></i>
                </div>
                <div>
                    <h1 class="text-xl md:text-2xl font-extrabold text-blue-900 tracking-tight">Private Social Security Pension Scheme</h1>
                    <p class="text-sm font-bold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            
            <!-- Menu Links -->
            <div class="hidden md:flex space-x-6 mt-4 md:mt-0 text-lg">
                <button id="link-page-home" onclick="switchPage('page-home')" class="nav-link active-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-house mr-1"></i> Home</button>
                <button id="link-page-about" onclick="switchPage('page-about')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-circle-info mr-1"></i> About Us</button>
                <button id="link-page-schemes" onclick="switchPage('page-schemes')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-list-check mr-1"></i> Schemes</button>
                <button id="link-page-conditions" onclick="switchPage('page-conditions')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-scale-balanced mr-1"></i> Conditions</button>
                <button id="link-page-contact" onclick="switchPage('page-contact')" class="nav-link text-gray-700 hover:text-blue-800 font-bold transition flex items-center"><i class="fa-solid fa-phone mr-1"></i> Contact Us</button>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-grow">
    
        <!-- ================= HOME PAGE ================= -->
        <div id="page-home" class="page-section active">
            <!-- Hero Section -->
            <section class="hero-bg py-16 px-4 border-b">
                <div class="container mx-auto">
                    <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-2xl border-l-8 border-blue-700">
                        <h2 class="text-3xl md:text-4xl font-black text-blue-900 mb-4 leading-tight">
                            Support for Senior Citizens, Widows, Disabled and the Needy
                        </h2>
                        <p class="text-lg text-gray-800 font-semibold mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                        <button onclick="switchPage('page-schemes')" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-md font-bold shadow-lg hover:bg-blue-800 transition text-lg">Apply / Learn More</button>
                    </div>
                </div>
            </section>

            <!-- 6 Action Cards Section -->
            <section class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    
                    <div class="bg-gradient-to-br from-blue-600 to-blue-800 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
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

                    <div class="bg-gradient-to-br from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-xl card-hover border-2 border-white cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart text-5xl mb-4 text-orange-100"></i>
                        <h3 class="font-bold text-2xl mb-2">Check Status</h3>
                        <p class="text-sm mb-4 text-orange-100 font-medium">Track your Pension Application Status</p>
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

        <!-- ================= ABOUT US PAGE ================= -->
        <div id="page-about" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900"><i class="fa-solid fa-circle-info mr-2 text-blue-600"></i> About Us / हमारे बारे में / ଆମ ବିଷୟରେ</h2>
                    <div class="w-32 h-1.5 bg-blue-700 mx-auto mt-4 rounded"></div>
                </div>
                
                <div class="bg-gray-50 rounded-xl shadow-lg overflow-hidden border-2 border-gray-200">
                    <div class="flex flex-col md:flex-row border-b-2 border-gray-200 bg-white">
                        <button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-xl transition border-b-4 border-transparent">ଓଡ଼ିଆ</button>
                        <button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-xl transition border-l md:border-l-2 border-gray-200 border-b-4 border-transparent">हिंदी</button>
                        <button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-xl transition border-l md:border-l-2 border-gray-200 border-b-4 border-transparent">English</button>
                    </div>
                    
                    <div class="p-8 md:p-12 text-center md:text-left text-lg md:text-xl">
                        <div id="about-or" class="block">
                            <p class="text-gray-800 leading-relaxed font-semibold">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ। ଆମେ ସମାଜର ଅବହେଳିତ ବର୍ଗଙ୍କ ସହ ଛିଡା ହେବାକୁ ପ୍ରତିଶ୍ରୁତିବଦ୍ଧ।</p>
                        </div>
                        <div id="about-hi" class="hidden">
                            <p class="text-gray-800 leading-relaxed font-semibold">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों (बुजुर्गों, विधवाओं और दिव्यांगों) को आर्थिक सहायता और सम्मान प्रदान करना है। पेंशन केवल पैसा नहीं, बल्कि सम्मान है। हम समाज के वंचित वर्गों के साथ खड़े होने के लिए प्रतिबद्ध हैं।</p>
                        </div>
                        <div id="about-en" class="hidden">
                            <p class="text-gray-800 leading-relaxed font-semibold">The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy (senior citizens, widows, and disabled). Pension is not just money; it is respect. We are committed to standing with the underprivileged sections of society.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= SCHEMES PAGE ================= -->
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
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-blue-200 text-blue-900 font-bold px-3 py-1 rounded">55 to 100 Years</span>
                            </div>
                            <div class="flex justify-between items-center bg-green-50 p-2 rounded border border-green-200">
                                <span class="font-bold text-green-800">Total Amount:</span>
                                <span class="font-black text-green-700 text-lg">₹3000 / Year</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-green-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-green-900 mb-1">Disability Pension</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-green-200 text-green-900 font-bold px-3 py-1 rounded">10 to 100 Years</span>
                            </div>
                            <div class="flex justify-between items-center bg-green-50 p-2 rounded border border-green-200">
                                <span class="font-bold text-green-800">Total Amount:</span>
                                <span class="font-black text-green-700 text-lg">₹3500 / Year</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-purple-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-purple-900 mb-1">Widow Pension</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ବିଧବା ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-purple-200 text-purple-900 font-bold px-3 py-1 rounded">30 to 55 Years</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-pink-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-pink-900 mb-1">Unmarried Woman</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଅବିବାହିତା ମହିଳା</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-pink-200 text-pink-900 font-bold px-3 py-1 rounded">30 to 55 Years</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-red-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-red-900 mb-1">Divorcee Women</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">ଛାଡପତ୍ର ପାଇଥିବା ମହିଳା</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-red-200 text-red-900 font-bold px-3 py-1 rounded">35 to 55 Years</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-lg border-t-8 border-orange-600 hover:shadow-2xl transition">
                        <h3 class="text-2xl font-black text-orange-900 mb-1">Transgender</h3>
                        <p class="text-md font-bold text-gray-500 mb-4 border-b pb-2">କିନ୍ନର ପେନସନ୍</p>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center bg-gray-100 p-2 rounded">
                                <span class="font-bold text-gray-700">Age Limit:</span>
                                <span class="bg-orange-200 text-orange-900 font-bold px-3 py-1 rounded">35 to 55 Years</span>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- ================= CONDITIONS PAGE (STRICT RULES) ================= -->
        <div id="page-conditions" class="page-section py-12 bg-white">
            <div class="container mx-auto px-4 max-w-5xl">
                <div class="text-center mb-10">
                    <h2 class="text-3xl md:text-4xl font-extrabold text-red-700"><i class="fa-solid fa-triangle-exclamation mr-2 text-red-600"></i> Strict Terms & Conditions</h2>
                    <p class="text-red-900 font-bold mt-2 text-xl">ଦୟାକରି ଆବେଦନ କରିବା ପୂର୍ବରୁ ଏହି ନିୟମଗୁଡିକ ଭଲଭାବେ ପଢନ୍ତୁ</p>
                    <div class="w-32 h-1.5 bg-red-600 mx-auto mt-4 rounded"></div>
                </div>
                
                <div class="bg-red-50 border-2 border-red-300 rounded-xl p-6 md:p-10 shadow-xl relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-3 h-full bg-red-600"></div>
                    
                    <div class="space-y-6 text-gray-800 text-lg">
                        
                        <!-- RULE 1: Non-Refundable Fee -->
                        <div class="bg-white p-5 rounded-lg border border-red-200 shadow-sm flex flex-col md:flex-row items-start">
                            <div class="bg-red-100 p-3 rounded-full mr-4 mb-3 md:mb-0">
                                <i class="fa-solid fa-money-bill-transfer text-red-600 text-2xl"></i>
                            </div>
                            <div>
                                <h4 class="font-black text-red-900 text-xl">Non-Refundable Application Fee (ଆବେଦନ ଫିସ୍ ଫେରସ୍ତ ଅଯୋଗ୍ୟ)</h4>
                                <p class="font-semibold mt-2 text-gray-700">Application fee is mandatory for all castes/categories. If your application is <b class="text-red-600">rejected</b> during document verification, the fee will <b class="text-red-600 underline">NOT BE REFUNDED</b> under any circumstances. No legal claims will be entertained.</p>
                                <p class="font-bold text-red-800 mt-2 bg-red-50 p-2 border-l-4 border-red-500 text-base">ସବୁ ବର୍ଗ/ଜାତି ପାଇଁ ଆବେଦନ ଫିସ୍ ବାଧ୍ୟତାମୂଳକ। ଡକ୍ୟୁମେଣ୍ଟ ଯାଞ୍ଚ ସମୟରେ ଫର୍ମ ରିଜେକ୍ଟ ହେଲେ, କୌଣସି ପରିସ୍ଥିତିରେ ବି ଫିସ୍ ଫେରସ୍ତ ଦିଆଯିବ ନାହିଁ। ଏହାକୁ ନେଇ କୌଣସି ଆଇନଗତ ଦାବି ଗ୍ରହଣଯୋଗ୍ୟ ହେବନାହିଁ।</p>
                            </div>
                        </div>

                        <!-- RULE 2: Monthly Payment & 3 Month Rule -->
                        <div class="bg-white p-5 rounded-lg border border-red-200 shadow-sm flex flex-col md:flex-row items-start">
                            <div class="bg-red-100 p-3 rounded-full mr-4 mb-3 md:mb-0">
                                <i class="fa-solid fa-calendar-check text-red-600 text-2xl"></i>
                            </div>
                            <div>
                                <h4 class="font-black text-red-900 text-xl">Payment Credit & 3-Month Wait Rule (ପେମେଣ୍ଟ୍ ନିୟମ)</h4>
                                <p class="font-semibold mt-2 text-gray-700">The total yearly amount (e.g. ₹3000 or ₹3500) will be credited in <b>monthly installments</b> to the bank account. The very first installment will be credited strictly <b>3 months after the application closing date</b>.</p>
                                <p class="font-bold text-red-800 mt-2 bg-red-50 p-2 border-l-4 border-red-500 text-base">ବାର୍ଷିକ ଟଙ୍କା ଏକାଥରକେ ନମିଳି ମାସିକ କିସ୍ତି ହିସାବରେ ପଠାଯିବ। ଆବେଦନ ତାରିଖ ସରିବାର ଠିକ୍ ୩ ମାସ ପରେ ଯାଇ ପ୍ରଥମ କିସ୍ତି ବ୍ୟାଙ୍କ ଆକାଉଣ୍ଟରେ କ୍ରେଡିଟ୍ ହେବ।</p>
                            </div>
                        </div>

                        <!-- RULE 3: Absolute Admin Rights -->
                        <div class="bg-white p-5 rounded-lg border border-red-200 shadow-sm flex flex-col md:flex-row items-start">
                            <div class="bg-red-100 p-3 rounded-full mr-4 mb-3 md:mb-0">
                                <i class="fa-solid fa-gavel text-red-600 text-2xl"></i>
                            </div>
                            <div>
                                <h4 class="font-black text-red-900 text-xl">Absolute Admin Rights (ମ୍ୟାନେଜମେଣ୍ଟର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର)</h4>
                                <p class="font-semibold mt-2 text-gray-700">This is a strictly private initiative. The Admin reserves the absolute right to reject any application or stop an ongoing pension at any time without any reason. <b>Admin is legally protected from any claims.</b></p>
                                <p class="font-bold text-red-800 mt-2 bg-red-50 p-2 border-l-4 border-red-500 text-base">ଏହା ଏକ ଘରୋଇ ପ୍ରୟାସ। ବିନା କାରଣରେ ପେନସନ୍ ବନ୍ଦ କରିବାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର Admin ଙ୍କ ପାଖରେ ସଂରକ୍ଷିତ। ଏଥିପାଇଁ Admin ଙ୍କ ଉପରେ କୌଣସି ଆଇନଗତ କାର୍ଯ୍ୟାନୁଷ୍ଠାନ କରାଯାଇପାରିବ ନାହିଁ।</p>
                            </div>
                        </div>

                        <!-- RULE 4: Mandatory Renewal -->
                        <div class="bg-white p-5 rounded-lg border border-red-200 shadow-sm flex flex-col md:flex-row items-start">
                            <div class="bg-red-100 p-3 rounded-full mr-4 mb-3 md:mb-0">
                                <i class="fa-solid fa-arrows-rotate text-red-600 text-2xl"></i>
                            </div>
                            <div>
                                <h4 class="font-black text-red-900 text-xl">Mandatory 3-Month Renewal (ରିନ୍ୟୁ ବାଧ୍ୟତାମୂଳକ)</h4>
                                <p class="font-semibold mt-2 text-gray-700">Every beneficiary MUST renew their pension application every 3 months, failing which the pension will be permanently stopped.</p>
                                <p class="font-bold text-red-800 mt-2 bg-red-50 p-2 border-l-4 border-red-500 text-base">ପ୍ରତି ୩ ମାସରେ ଥରେ ନିଜ ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ ଅଟେ। ନଚେତ୍ ପେନସନ୍ ବନ୍ଦ ହୋଇଯିବ।</p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <!-- ================= CONTACT US PAGE ================= -->
        <div id="page-contact" class="page-section py-12 bg-blue-50">
            <div class="container mx-auto px-4 max-w-4xl text-center">
                <i class="fa-solid fa-headset text-6xl text-blue-700 mb-6"></i>
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-6">Contact & Support</h2>
                <div class="bg-white p-10 rounded-xl shadow-xl border-t-8 border-blue-700">
                    <p class="text-xl font-bold text-gray-700 mb-8">For any queries regarding the Private Social Security Pension Scheme, please reach out to us:</p>
                    <div class="flex flex-col md:flex-row justify-center items-center space-y-6 md:space-y-0 md:space-x-12">
                        <div class="flex items-center text-2xl font-black text-blue-900">
                            <div class="bg-blue-100 p-4 rounded-full mr-4">
                                <i class="fa-solid fa-phone text-blue-700"></i>
                            </div>
                            8910223342
                        </div>
                        <div class="flex items-center text-2xl font-black text-blue-900">
                            <div class="bg-blue-100 p-4 rounded-full mr-4">
                                <i class="fa-solid fa-envelope text-blue-700"></i>
                            </div>
                            admin@kulusutar.in
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Global Footer (Always visible) -->
    <footer class="bg-blue-900 text-white py-6 border-t-4 border-blue-700 mt-auto">
        <div class="container mx-auto px-4 text-center">
            <p class="font-bold">&copy; 2026 Private Social Security Pension Scheme</p>
            <p class="text-sm text-blue-300 mt-1">This is a 100% private initiative. Not affiliated with any government department.</p>
        </div>
    </footer>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design
