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
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hero-bg {
            background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .page-section { display: none; }
        .page-section.active { display: block; }
        .nav-link.active-nav { color: #1d4ed8; border-bottom: 2px solid #1d4ed8; }
        .tab-btn.active { background-color: #1d4ed8; color: white; }
    </style>
    <script>
        function showPage(pageId) {
            let pages = document.getElementsByClassName('page-section');
            for(let p of pages) { p.classList.remove('active'); }
            document.getElementById(pageId).classList.add('active');
            
            let links = document.getElementsByClassName('nav-link');
            for(let l of links) { l.classList.remove('active-nav'); }
            document.getElementById('nav-' + pageId).classList.add('active-nav');
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
<body class="bg-gray-50 font-sans text-gray-800 flex flex-col min-h-screen">

    <!-- Navbar -->
    <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="text-blue-800 text-4xl">
                    <i class="fa-solid fa-hands-holding-child"></i>
                </div>
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-blue-900">Private Social Security Pension</h1>
                    <p class="text-xs md:text-sm font-semibold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            
            <div class="hidden lg:flex space-x-6 mt-4 lg:mt-0 font-bold">
                <button id="nav-home" onclick="showPage('home')" class="nav-link active-nav pb-1 transition hover:text-blue-800"><i class="fa-solid fa-house mr-1"></i> Home</button>
                <button id="nav-about" onclick="showPage('about')" class="nav-link pb-1 transition hover:text-blue-800 text-gray-600"><i class="fa-solid fa-circle-info mr-1"></i> About Us</button>
                <button id="nav-schemes" onclick="showPage('schemes')" class="nav-link pb-1 transition hover:text-blue-800 text-gray-600"><i class="fa-solid fa-list mr-1"></i> Schemes</button>
                <button id="nav-conditions" onclick="showPage('conditions')" class="nav-link pb-1 transition hover:text-blue-800 text-gray-600"><i class="fa-solid fa-scale-balanced mr-1"></i> Conditions</button>
                <button id="nav-contact" onclick="showPage('contact')" class="nav-link pb-1 transition hover:text-blue-800 text-gray-600"><i class="fa-solid fa-phone mr-1"></i> Contact Us</button>
            </div>
        </div>
    </header>

    <main class="flex-grow">
        <!-- HOME PAGE -->
        <section id="home" class="page-section active">
            <div class="hero-bg py-16 px-4 border-b border-gray-200">
                <div class="container mx-auto">
                    <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-xl border-l-8 border-blue-700">
                        <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">
                            Support for Senior Citizens, Widows, Disabled and the Needy
                        </h2>
                        <p class="text-lg text-gray-700 font-semibold mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                        <button onclick="showPage('schemes')" class="bg-blue-700 text-white px-8 py-3 rounded font-bold shadow-md hover:bg-blue-800 transition">Apply Now</button>
                    </div>
                </div>
            </div>

            <!-- Original 6 Cards -->
            <div class="container mx-auto px-4 py-12 relative -mt-10 z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="bg-blue-700 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-blue-800 cursor-pointer">
                        <i class="fa-solid fa-user-shield text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Admin Login</h3>
                        <p class="text-sm text-blue-100 mb-4">Official login for Management</p>
                    </div>
                    <div onclick="showPage('schemes')" class="bg-green-600 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-green-700 cursor-pointer">
                        <i class="fa-solid fa-pen-to-square text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Pension Apply</h3>
                        <p class="text-sm text-green-100 mb-4">Apply for New Pension Scheme</p>
                    </div>
                    <div class="bg-orange-500 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-orange-600 cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Application Status</h3>
                        <p class="text-sm text-orange-100 mb-4">Check Application Approval Status</p>
                    </div>
                    <div class="bg-purple-600 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-purple-700 cursor-pointer">
                        <i class="fa-solid fa-users text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Beneficiary Login</h3>
                        <p class="text-sm text-purple-100 mb-4">Login for Pension Beneficiaries</p>
                    </div>
                    <div onclick="showPage('conditions')" class="bg-red-600 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-red-700 cursor-pointer">
                        <i class="fa-solid fa-scale-balanced text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Terms & Conditions</h3>
                        <p class="text-sm text-red-100 mb-4">Read our strict policies and rules</p>
                    </div>
                    <div onclick="showPage('contact')" class="bg-teal-600 text-white rounded-xl p-8 text-center shadow-lg card-hover border border-teal-700 cursor-pointer">
                        <i class="fa-solid fa-headset text-5xl mb-4"></i>
                        <h3 class="font-bold text-xl mb-2">Help & Contact</h3>
                        <p class="text-sm text-teal-100 mb-4">Get Support and Contact Details</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- ABOUT US PAGE -->
        <section id="about" class="page-section container mx-auto px-4 py-12">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-users mr-2"></i>About Us / हमारे बारे में / ଆମ ବିଷୟରେ</h2>
                <div class="w-24 h-1 bg-blue-700 mx-auto mt-4"></div>
            </div>
            <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
                <div class="flex border-b border-gray-200 bg-gray-100">
                    <button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-lg transition">ଓଡ଼ିଆ</button>
                    <button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-lg transition border-l border-gray-200">हिंदी</button>
                    <button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-lg transition border-l border-gray-200">English</button>
                </div>
                <div class="p-8 text-center md:text-left text-lg">
                    <div id="about-or" class="block">
                        <p class="text-gray-700 leading-relaxed font-medium">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ।</p>
                    </div>
                    <div id="about-hi" class="hidden">
                        <p class="text-gray-700 leading-relaxed font-medium">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों (बुजुर्गों, विधवाओं और दिव्यांगों) को आर्थिक सहायता और सम्मान प्रदान करना है। पेंशन केवल पैसा नहीं, बल्कि सम्मान है।</p>
                    </div>
                    <div id="about-en" class="hidden">
                        <p class="text-gray-700 leading-relaxed font-medium">The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy (senior citizens, widows, and disabled). Pension is not just money; it is respect.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- SCHEMES PAGE -->
        <section id="schemes" class="page-section container mx-auto px-4 py-12">
            <div class="text-center mb-10">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-list-check mr-2"></i>Schemes, Age Limits & Pension Amount</h2>
                <div class="w-24 h-1 bg-blue-700 mx-auto mt-4"></div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-600">
                    <h3 class="text-xl font-bold text-blue-900 mb-2">Old Age Pension</h3>
                    <p class="text-gray-600 mb-3 font-semibold">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p>
                    <div class="bg-gray-100 p-3 rounded mb-3">
                        <p class="text-sm"><b>Age:</b> 55 to 100 Years</p>
                        <p class="text-sm mt-1 text-green-700"><b>Amount:</b> ₹3000 / Year (Monthly Credit)</p>
                    </div>
                    <button class="w-full bg-blue-100 text-blue-800 font-bold py-2 rounded">Apply Now</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-purple-600">
                    <h3 class="text-xl font-bold text-purple-900 mb-2">Widow Pension</h3>
                    <p class="text-gray-600 mb-3 font-semibold">ବିଧବା ପେନସନ୍</p>
                    <div class="bg-gray-100 p-3 rounded mb-3">
                        <p class="text-sm"><b>Age:</b> 30 to 55 Years</p>
                        <p class="text-sm mt-1 text-green-700"><b>Amount:</b> Applicable Rate</p>
                    </div>
                    <button class="w-full bg-purple-100 text-purple-800 font-bold py-2 rounded">Apply Now</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-600">
                    <h3 class="text-xl font-bold text-green-900 mb-2">Disability Pension</h3>
                    <p class="text-gray-600 mb-3 font-semibold">ଭିନ୍ନକ୍ଷମ / ଦିବ୍ୟାଙ୍ଗ ପେନସନ୍</p>
                    <div class="bg-gray-100 p-3 rounded mb-3">
                        <p class="text-sm"><b>Age:</b> 10 to 100 Years</p>
                        <p class="text-sm mt-1 text-green-700"><b>Amount:</b> ₹3500 / Year (Monthly Credit)</p>
                    </div>
                    <button class="w-full bg-green-100 text-green-800 font-bold py-2 rounded">Apply Now</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-pink-600">
                    <h3 class="text-xl font-bold text-pink-900 mb-2">Unmarried Woman</h3>
                    <p class="text-gray-600 mb-3 font-semibold">ଅବିବାହିତା ମହିଳା</p>
                    <div class="bg-gray-100 p-3 rounded mb-3"><p class="text-sm"><b>Age:</b> 30 to 55 Years</p></div>
                    <button class="w-full bg-pink-100 text-pink-800 font-bold py-2 rounded">Apply Now</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-red-600">
                    <h3 class="text-xl font-bold text-red-900 mb-2">Divorcee Women</h3>
                    <p class="text-gray-600 mb-3 font-semibold">ଛାଡପତ୍ର ପାଇଥିବା ମହିଳା</p>
                    <div class="bg-gray-100 p-3 rounded mb-3"><p class="text-sm"><b>Age:</b> 35 to 55 Years</p></div>
                    <button class="w-full bg-red-100 text-red-800 font-bold py-2 rounded">Apply Now</button>
                </div>
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-orange-600">
                    <h3 class="text-xl font-bold text-orange-900 mb-2">Transgender</h3>
                    <p class="text-gray-600 mb-3 font-semibold">କିନ୍ନର ପେନସନ୍</p>
                    <div class="bg-gray-100 p-3 rounded mb-3"><p class="text-sm"><b>Age:</b> 35 to 55 Years</p></div>
                    <button class="w-full bg-orange-100 text-orange-800 font-bold py-2 rounded">Apply Now</button>
                </div>
            </div>
        </section>

        <!-- CONDITIONS PAGE -->
        <section id="conditions" class="page-section container mx-auto px-4 py-12 max-w-4xl">
            <div class="flex items-center justify-center mb-8 border-b-2 border-red-200 pb-4">
                <i class="fa-solid fa-triangle-exclamation text-red-600 text-4xl mr-3"></i>
                <h2 class="text-3xl font-bold text-red-900">Strict Terms & Conditions (ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ)</h2>
            </div>
            <div class="bg-white border-2 border-red-200 rounded-xl p-8 shadow-lg relative overflow-hidden space-y-6 text-gray-800">
                <div class="absolute top-0 left-0 w-2 h-full bg-red-600"></div>
                <div>
                    <h4 class="font-bold text-red-900 text-xl">1. No Refund Policy (ଟଙ୍କା ଫେରସ୍ତ ହେବ ନାହିଁ)</h4>
                    <p class="text-base mt-2">ଆବେଦନ ଫି (Application Charge) କୌଣସି ପରିସ୍ଥିତିରେ ଫେରସ୍ତ ଦିଆଯିବ ନାହିଁ। ଭେରିଫିକେସନ୍ ସମୟରେ ତ୍ରୁଟି ବାହାରିଲେ ବା ଆବେଦନ Reject ହେଲେ ମଧ୍ୟ ଟଙ୍କା ଫେରସ୍ତ ମିଳିବ ନାହିଁ। ସବୁ ଜାତି ଓ ବର୍ଗ (All Castes) ପାଇଁ ଏହା ପ୍ରଯୁଜ୍ୟ।</p>
                </div>
                <div>
                    <h4 class="font-bold text-red-900 text-xl">2. First Payment Timeline (ପ୍ରଥମ ପେନସନ୍ ସମୟ)</h4>
                    <p class="text-base mt-2">ଆବେଦନ ଶେଷ ତାରିଖର ଠିକ୍ <b>୩ ମାସ ପରେ</b> ପ୍ରଥମ ପେନସନ୍ ଟଙ୍କା ଆକାଉଣ୍ଟକୁ କ୍ରେଡିଟ୍ ହେବ।</p>
                </div>
                <div>
                    <h4 class="font-bold text-red-900 text-xl">3. Mandatory 3-Month Renewal (ରିନ୍ୟୁ ବାଧ୍ୟତାମୂଳକ)</h4>
                    <p class="text-base mt-2">ପ୍ରତି ୩ ମାସରେ ଥରେ ନିଜର ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ ଅଟେ, ନଚେତ୍ ପେନସନ୍ ବନ୍ଦ ହୋଇଯିବ।</p>
                </div>
                <div>
                    <h4 class="font-bold text-red-900 text-xl">4. Absolute Admin Rights (ଆଡମିନ୍ ଙ୍କ ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର)</h4>
                    <p class="text-base mt-2">ବିନା କାରଣ ଦର୍ଶାଇ କାହାର ବି ପେନସନ୍ ବନ୍ଦ କରିବାର ଅଧିକାର ଆଡମିନ୍ ପାଖରେ ଅଛି। ଏଥିପାଇଁ କୌଣସି ଆଇନଗତ କାର୍ଯ୍ୟାନୁଷ୍ଠାନ କରାଯାଇପାରିବ ନାହିଁ।</p>
                </div>
            </div>
        </section>

        <!-- CONTACT PAGE -->
        <section id="contact" class="page-section container mx-auto px-4 py-16 max-w-3xl text-center">
            <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-8 md:p-12">
                <i class="fa-solid fa-headset text-6xl text-blue-700 mb-6"></i>
                <h2 class="text-3xl font-bold text-blue-900 mb-4">Get in Touch (ଯୋଗାଯୋଗ କରନ୍ତୁ)</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                    <div class="bg-gray-50 p-6 rounded-lg border">
                        <i class="fa-solid fa-phone text-3xl text-blue-600 mb-2"></i>
                        <p class="text-2xl font-extrabold text-blue-800">8910223342</p>
                    </div>
                    <div class="bg-gray-50 p-6 rounded-lg border">
                        <i class="fa-solid fa-envelope text-3xl text-blue-600 mb-2"></i>
                        <p class="text-lg font-bold text-blue-800">admin@kulusutar.in</p>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="bg-blue-900 text-center py-6 mt-auto border-t-4 border-blue-700 text-blue-200">
        <p>&copy; 2026 Private Social Security Pension Scheme | All Rights Reserved.</p>
    </footer>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design
