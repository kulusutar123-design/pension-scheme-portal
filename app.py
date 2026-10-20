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
        /* Smooth scrolling for menu clicks */
        html { scroll-behavior: smooth; }
        
        .hero-bg {
            background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.6)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
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
    </style>
    <script>
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
<body id="home" class="bg-gray-100 font-sans text-gray-800">

    <!-- Top Header / Navbar (Menu) -->
    <header class="bg-white shadow-md border-b-4 border-blue-700 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-4">
                <div class="text-blue-700 text-5xl">
                    <i class="fa-solid fa-hands-holding-circle"></i>
                </div>
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-blue-800">Private Social Security Pension Scheme</h1>
                    <p class="text-sm font-semibold text-gray-600">A Private Initiative for the Needy</p>
                    <p class="text-xs italic text-gray-500 mt-1">Secure Tomorrow | Dignity for Life</p>
                </div>
            </div>
            
            <!-- Menu Links (Clicking these will scroll to sections) -->
            <div class="hidden md:flex space-x-6 mt-4 md:mt-0">
                <a href="#home" class="text-blue-700 font-bold flex items-center"><i class="fa-solid fa-house mr-1"></i> Home</a>
                <a href="#about" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-circle-info mr-1"></i> About Us</a>
                <a href="#schemes" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-file-lines mr-1"></i> Schemes</a>
                <a href="#conditions" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-scale-balanced mr-1"></i> Conditions</a>
                <a href="#contact" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center"><i class="fa-solid fa-phone mr-1"></i> Contact Us</a>
            </div>
        </div>
    </header>

    <!-- ORIGINAL Hero Section -->
    <section class="hero-bg py-16 px-4 border-b">
        <div class="container mx-auto">
            <div class="max-w-2xl bg-white/90 p-8 rounded-xl shadow-lg border-l-8 border-blue-600">
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">
                    Support for Senior Citizens, Widows, Disabled and the Needy
                </h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-6 py-3 rounded-md font-bold shadow-md hover:bg-blue-800 transition">Learn More</a>
            </div>
        </div>
    </section>

    <!-- ORIGINAL 6 Action Cards Section -->
    <section class="container mx-auto px-4 py-12 relative -mt-16 z-10">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
            
            <div class="bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Admin Login</h3>
                <p class="text-sm mb-4 text-blue-100">Official login for Administration</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </div>

            <div class="bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white cursor-pointer">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Pension Apply</h3>
                <p class="text-sm mb-4 text-green-100">Apply for New Pension Scheme</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </div>

            <div class="bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Application Status</h3>
                <p class="text-sm mb-4 text-orange-100">Check Your Application Status</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </div>

            <div class="bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Beneficiary Login</h3>
                <p class="text-sm mb-4 text-purple-100">Login for Pension Beneficiaries</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </div>

            <a href="#schemes" class="bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white block">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Scheme Details</h3>
                <p class="text-sm mb-4 text-teal-100">View Scheme Information & Guidelines</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#contact" class="bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white block">
                <i class="fa-solid fa-headset text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Help & Contact</h3>
                <p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

        </div>
    </section>

    <!-- ABOUT US Section -->
    <section id="about" class="container mx-auto px-4 py-12">
        <div class="flex items-center mb-8 border-b-2 border-blue-200 pb-2">
            <i class="fa-solid fa-users text-blue-700 text-3xl mr-3"></i>
            <h2 class="text-2xl font-bold text-blue-900">About Us / हमारे बारे में / ଆମ ବିଷୟରେ</h2>
        </div>
        
        <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
            <div class="flex border-b border-gray-200 bg-gray-100">
                <button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-3 font-bold text-lg transition">ଓଡ଼ିଆ</button>
                <button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-3 font-bold text-lg transition border-l border-gray-200">हिंदी</button>
                <button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-3 font-bold text-lg transition border-l border-gray-200">English</button>
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

    <!-- SCHEMES Section -->
    <section id="schemes" class="container mx-auto px-4 py-12">
        <div class="flex items-center mb-8 border-b-2 border-blue-200 pb-2">
            <i class="fa-solid fa-list-check text-blue-700 text-3xl mr-3"></i>
            <h2 class="text-2xl font-bold text-blue-900">Available Schemes & Age Limits</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-blue-500">
                <h3 class="text-xl font-bold text-blue-800 mb-1">Old Age Pension</h3>
                <p class="text-sm text-gray-500 mb-3">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p>
                <span class="bg-blue-100 text-blue-800 text-sm font-bold px-3 py-1 rounded">Age: 55 to 100 Years</span>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-purple-500">
                <h3 class="text-xl font-bold text-purple-800 mb-1">Widow Pension</h3>
                <p class="text-sm text-gray-500 mb-3">ବିଧବା ପେନସନ୍</p>
                <span class="bg-purple-100 text-purple-800 text-sm font-bold px-3 py-1 rounded">Age: 30 to 55 Years</span>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-green-500">
                <h3 class="text-xl font-bold text-green-800 mb-1">Disability Pension</h3>
                <p class="text-sm text-gray-500 mb-3">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p>
                <span class="bg-green-100 text-green-800 text-sm font-bold px-3 py-1 rounded">Age: 10 to 100 Years</span>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-pink-500">
                <h3 class="text-xl font-bold text-pink-800 mb-1">Unmarried Woman</h3>
                <p class="text-sm text-gray-500 mb-3">ଅବିବାହିତା ମହିଳା</p>
                <span class="bg-pink-100 text-pink-800 text-sm font-bold px-3 py-1 rounded">Age: 30 to 55 Years</span>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-red-500">
                <h3 class="text-xl font-bold text-red-800 mb-1">Divorcee Women</h3>
                <p class="text-sm text-gray-500 mb-3">ଛାଡପତ୍ର ପାଇଥିବା ମହିଳା</p>
                <span class="bg-red-100 text-red-800 text-sm font-bold px-3 py-1 rounded">Age: 35 to 55 Years</span>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 border-l-4 border-l-orange-500">
                <h3 class="text-xl font-bold text-orange-800 mb-1">Transgender</h3>
                <p class="text-sm text-gray-500 mb-3">କିନ୍ନର ପେନସନ୍</p>
                <span class="bg-orange-100 text-orange-800 text-sm font-bold px-3 py-1 rounded">Age: 35 to 55 Years</span>
            </div>
        </div>
    </section>

    <!-- CONDITIONS Section -->
    <section id="conditions" class="container mx-auto px-4 py-12 mb-12">
        <div class="flex items-center mb-8 border-b-2 border-red-200 pb-2">
            <i class="fa-solid fa-triangle-exclamation text-red-600 text-3xl mr-3"></i>
            <h2 class="text-2xl font-bold text-red-900">Strict Terms & Conditions (ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ)</h2>
        </div>
        
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 shadow-sm">
            <ul class="space-y-4 text-gray-800">
                <li class="flex items-start">
                    <i class="fa-solid fa-ban text-red-500 mt-1 mr-3"></i>
                    <div>
                        <b class="text-red-800">Private & Non-Governmental:</b> This is a 100% private trust initiative. NOT a government scheme. (ଏହା କୌଣସି ସରକାରୀ ଯୋଜନା ନୁହେଁ।)
                    </div>
                </li>
                <li class="flex items-start">
                    <i class="fa-solid fa-gavel text-red-500 mt-1 mr-3"></i>
                    <div>
                        <b class="text-red-800">Admin Rights:</b> The Admin reserves the absolute right to reject/stop any pension anytime without providing reasons. No legal action can be taken against the Admin. (ବିନା କାରଣରେ ପେନସନ୍ ବନ୍ଦ କରିବାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର Admin ଙ୍କ ପାଖରେ ଅଛି।)
                    </div>
                </li>
                <li class="flex items-start">
                    <i class="fa-solid fa-arrows-rotate text-red-500 mt-1 mr-3"></i>
                    <div>
                        <b class="text-red-800">Mandatory 3-Month Renewal:</b> Beneficiaries MUST renew every 3 months. (ପ୍ରତି ୩ ମାସରେ ଥରେ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ ଅଟେ।)
                    </div>
                </li>
                <li class="flex items-start">
                    <i class="fa-solid fa-money-bill-wave text-red-500 mt-1 mr-3"></i>
                    <div>
                        <b class="text-red-800">Zero Income:</b> Applicant must have strictly ZERO alternative income. (ଆବେଦନକାରୀଙ୍କର ଅନ୍ୟ କୌଣସି ଆୟ ନଥିବା ଦରକାର।)
                    </div>
                </li>
            </ul>
        </div>
    </section>

    <!-- Footer / CONTACT US Section -->
    <footer id="contact" class="bg-blue-900 text-white py-10">
        <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
            <div class="mb-6 md:mb-0 text-center md:text-left">
                <h3 class="text-xl font-bold mb-2">Contact Us</h3>
                <p class="text-blue-200"><i class="fa-solid fa-phone mr-2"></i> 8910223342</p>
                <p class="text-blue-200"><i class="fa-solid fa-envelope mr-2"></i> admin@kulusutar.in</p>
            </div>
            <div class="text-center md:text-right text-sm text-blue-300">
                <p>&copy; 2026 Private Social Security Pension Scheme</p>
                <p>All Rights Reserved. | Empathetic & Private Initiative</p>
            </div>
        </div>
    </footer>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design
