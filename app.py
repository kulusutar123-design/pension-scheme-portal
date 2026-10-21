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
            background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
        }
        .tab-btn.active {
            background-color: #1d4ed8; /* blue-700 */
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
<body class="bg-gray-50 font-sans text-gray-800">

    <!-- Header / Navbar -->
    <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex flex-wrap justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="text-blue-800 text-4xl">
                    <i class="fa-solid fa-hands-holding-child"></i>
                </div>
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-blue-900">Private Social Security Pension Scheme</h1>
                    <p class="text-xs md:text-sm font-semibold text-gray-600">A Private Initiative for the Needy</p>
                </div>
            </div>
            <div class="hidden lg:flex space-x-6 mt-4 lg:mt-0">
                <a href="#home" class="text-blue-800 font-bold"><i class="fa-solid fa-house mr-1"></i> Home</a>
                <a href="#about" class="text-gray-700 hover:text-blue-800 font-semibold"><i class="fa-solid fa-circle-info mr-1"></i> About Us</a>
                <a href="#schemes" class="text-gray-700 hover:text-blue-800 font-semibold"><i class="fa-solid fa-list mr-1"></i> Schemes</a>
                <a href="#conditions" class="text-gray-700 hover:text-blue-800 font-semibold"><i class="fa-solid fa-scale-balanced mr-1"></i> Conditions</a>
                <a href="#contact" class="text-gray-700 hover:text-blue-800 font-semibold"><i class="fa-solid fa-phone mr-1"></i> Contact Us</a>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section id="home" class="hero-bg py-16 px-4 border-b border-gray-200">
        <div class="container mx-auto">
            <div class="max-w-3xl bg-white p-8 rounded-xl shadow-xl border-l-8 border-blue-700">
                <h2 class="text-3xl md:text-5xl font-extrabold text-blue-900 mb-6 leading-tight">
                    Support for Senior Citizens, Widows, Disabled and the Needy
                </h2>
                <p class="text-lg text-gray-700 font-semibold mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <div class="flex space-x-4">
                    <button class="bg-blue-700 text-white px-8 py-3 rounded font-bold shadow-md hover:bg-blue-800 transition">Apply Now</button>
                    <button class="bg-green-600 text-white px-8 py-3 rounded font-bold shadow-md hover:bg-green-700 transition"><i class="fa-solid fa-user-shield mr-2"></i>Admin Login</button>
                </div>
            </div>
        </div>
    </section>

    <!-- About Us (Multilingual Tabs) -->
    <section id="about" class="container mx-auto px-4 py-12">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-users mr-2"></i>About Us / हमारे बारे में / ଆମ ବିଷୟରେ</h2>
            <div class="w-24 h-1 bg-blue-700 mx-auto mt-4"></div>
        </div>
        
        <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
            <!-- Language Buttons -->
            <div class="flex border-b border-gray-200 bg-gray-100">
                <button id="btn-or" onclick="showTab('or')" class="tab-btn active flex-1 py-4 font-bold text-lg transition">ଓଡ଼ିଆ</button>
                <button id="btn-hi" onclick="showTab('hi')" class="tab-btn flex-1 py-4 font-bold text-lg transition border-l border-gray-200">हिंदी</button>
                <button id="btn-en" onclick="showTab('en')" class="tab-btn flex-1 py-4 font-bold text-lg transition border-l border-gray-200">English</button>
            </div>
            
            <!-- Content -->
            <div class="p-8 text-center md:text-left text-lg">
                <!-- Odia -->
                <div id="about-or" class="block">
                    <p class="text-gray-700 leading-relaxed font-medium">ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ (ବୃଦ୍ଧ, ବିଧବା ଏବଂ ଭିନ୍ନକ୍ଷମ) ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ। ଆମେ ସମାଜର ଅବହେଳିତ ବର୍ଗଙ୍କ ସହ ଛିଡା ହେବାକୁ ପ୍ରତିଶ୍ରୁତିବଦ୍ଧ।</p>
                </div>
                <!-- Hindi -->
                <div id="about-hi" class="hidden">
                    <p class="text-gray-700 leading-relaxed font-medium">प्राइवेट सोशल सिक्योरिटी पेंशन स्कीम एक 100% निजी और गैर-सरकारी पहल है। हमारा उद्देश्य जरूरतमंदों (बुजुर्गों, विधवाओं और दिव्यांगों) को आर्थिक सहायता और सम्मान प्रदान करना है। पेंशन केवल पैसा नहीं, बल्कि सम्मान है। हम समाज के वंचित वर्गों के साथ खड़े होने के लिए प्रतिबद्ध हैं।</p>
                </div>
                <!-- English -->
                <div id="about-en" class="hidden">
                    <p class="text-gray-700 leading-relaxed font-medium">The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy (senior citizens, widows, and disabled). Pension is not just money; it is respect. We are committed to standing with the underprivileged sections of society.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Schemes & Age Limits -->
    <section id="schemes" class="bg-gray-100 py-12 border-t border-b border-gray-200">
        <div class="container mx-auto px-4">
            <div class="text-center mb-10">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-list-check mr-2"></i>Available Schemes & Age Limits</h2>
                <p class="text-gray-600 mt-2">Check your eligibility based on the age criteria below</p>
                <div class="w-24 h-1 bg-blue-700 mx-auto mt-4"></div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                
                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-blue-800 mb-2">Old Age Pension</h3>
                    <p class="text-gray-600 mb-4">ବୃଦ୍ଧାବସ୍ଥା ପେନସନ୍</p>
                    <div class="bg-blue-50 text-blue-800 font-bold px-4 py-2 rounded inline-block">Age: 55 to 100 Years</div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-purple-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-purple-800 mb-2">Widow Pension</h3>
                    <p class="text-gray-600 mb-4">ବିଧବା ପେନସନ୍</p>
                    <div class="bg-purple-50 text-purple-800 font-bold px-4 py-2 rounded inline-block">Age: 30 to 55 Years</div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-green-800 mb-2">Disability Pension</h3>
                    <p class="text-gray-600 mb-4">ଭିନ୍ନକ୍ଷମ ପେନସନ୍</p>
                    <div class="bg-green-50 text-green-800 font-bold px-4 py-2 rounded inline-block">Age: 10 to 100 Years</div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-pink-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-pink-800 mb-2">Unmarried Woman</h3>
                    <p class="text-gray-600 mb-4">ଅବିବାହିତା ମହିଳା</p>
                    <div class="bg-pink-50 text-pink-800 font-bold px-4 py-2 rounded inline-block">Age: 30 to 55 Years</div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-red-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-red-800 mb-2">Divorcee Women</h3>
                    <p class="text-gray-600 mb-4">ଛାଡପତ୍ର ପାଇଥିବା ମହିଳା</p>
                    <div class="bg-red-50 text-red-800 font-bold px-4 py-2 rounded inline-block">Age: 35 to 55 Years</div>
                </div>

                <div class="bg-white p-6 rounded-lg shadow-md border-t-4 border-orange-500 hover:shadow-lg transition">
                    <h3 class="text-xl font-bold text-orange-800 mb-2">Transgender</h3>
                    <p class="text-gray-600 mb-4">କିନ୍ନର ପେନସନ୍</p>
                    <div class="bg-orange-50 text-orange-800 font-bold px-4 py-2 rounded inline-block">Age: 35 to 55 Years</div>
                </div>

            </div>
        </div>
    </section>

    <!-- Strict Terms & Conditions -->
    <section id="conditions" class="container mx-auto px-4 py-12">
        <div class="max-w-5xl mx-auto bg-red-50 border-2 border-red-200 rounded-xl p-8 shadow-md relative overflow-hidden">
            <div class="absolute top-0 left-0 w-2 h-full bg-red-600"></div>
            
            <div class="flex items-center mb-6">
                <i class="fa-solid fa-triangle-exclamation text-4xl text-red-600 mr-4"></i>
                <h2 class="text-2xl md:text-3xl font-bold text-red-900">Strict Terms & Conditions (ନିୟମ ଓ ସର୍ତ୍ତାବଳୀ)</h2>
            </div>
            
            <div class="space-y-4 text-gray-800">
                <div class="bg-white p-4 rounded border border-red-100 shadow-sm flex items-start">
                    <i class="fa-solid fa-ban text-red-500 mt-1 mr-3 text-lg"></i>
                    <div>
                        <h4 class="font-bold text-red-800">Private & Non-Governmental (ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ପ୍ରୟାସ)</h4>
                        <p class="text-sm mt-1">This is a 100% private trust initiative. This is NOT a government scheme. (ଏହା ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ସାହାଯ୍ୟ ଅଟେ, ଏହା କୌଣସି ସରକାରୀ ଯୋଜନା ନୁହେଁ।)</p>
                    </div>
                </div>

                <div class="bg-white p-4 rounded border border-red-100 shadow-sm flex items-start">
                    <i class="fa-solid fa-gavel text-red-500 mt-1 mr-3 text-lg"></i>
                    <div>
                        <h4 class="font-bold text-red-800">Absolute Admin Rights (ମ୍ୟାନେଜମେଣ୍ଟର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର)</h4>
                        <p class="text-sm mt-1">The Management/Admin reserves the absolute right to reject any application or stop an ongoing pension at any time without providing any reason. <b>No legal action or claim can be made against the Admin.</b> Help is strictly subject to the availability of funds. (ବିନା କାରଣରେ ପେନସନ୍ ବନ୍ଦ କରିବାର ଅଧିକାର Admin ଙ୍କ ପାଖରେ ଅଛି। ଏଥିପାଇଁ Admin ଙ୍କ ଉପରେ କୌଣସି ଆଇନଗତ କାର୍ଯ୍ୟାନୁଷ୍ଠାନ କରାଯାଇପାରିବ ନାହିଁ।)</p>
                    </div>
                </div>

                <div class="bg-white p-4 rounded border border-red-100 shadow-sm flex items-start">
                    <i class="fa-solid fa-arrows-rotate text-red-500 mt-1 mr-3 text-lg"></i>
                    <div>
                        <h4 class="font-bold text-red-800">Mandatory 3-Month Renewal (୩ ମାସରେ ରିନ୍ୟୁ ବାଧ୍ୟତାମୂଳକ)</h4>
                        <p class="text-sm mt-1">Every beneficiary MUST renew their pension every 3 months. Failure to do so will result in automatic termination of the pension. (ପ୍ରତି ୩ ମାସରେ ଥରେ ପେନସନ୍ ରିନ୍ୟୁ (Renew) କରିବା ବାଧ୍ୟତାମୂଳକ ଅଟେ। ନଚେତ୍ ପେନସନ୍ ବନ୍ଦ ହୋଇଯିବ।)</p>
                    </div>
                </div>

                <div class="bg-white p-4 rounded border border-red-100 shadow-sm flex items-start">
                    <i class="fa-solid fa-money-bill-wave text-red-500 mt-1 mr-3 text-lg"></i>
                    <div>
                        <h4 class="font-bold text-red-800">Zero Income Rule (ଶୂନ୍ୟ ଆୟ ନିୟମ)</h4>
                        <p class="text-sm mt-1">The applicant must have strictly ZERO alternative income. Any false information will lead to immediate cancellation. (ଆବେଦନକାରୀଙ୍କର ଅନ୍ୟ କୌଣସି ଆୟ ନଥିବା ଦରକାର।)</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer / Contact Us -->
    <footer id="contact" class="bg-blue-900 text-white pt-12 pb-6 border-t-8 border-blue-700">
        <div class="container mx-auto px-4 max-w-6xl">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 text-center md:text-left">
                
                <div>
                    <h3 class="text-xl font-bold mb-4 border-b border-blue-700 pb-2 inline-block">Private Pension Scheme</h3>
                    <p class="text-blue-200 text-sm leading-relaxed">Dedicated to providing a secure tomorrow and a life of dignity to the vulnerable sections of our society.</p>
                </div>
                
                <div>
                    <h3 class="text-xl font-bold mb-4 border-b border-blue-700 pb-2 inline-block">Quick Links</h3>
                    <ul class="space-y-2 text-sm text-blue-200">
                        <li><a href="#schemes" class="hover:text-white transition"><i class="fa-solid fa-chevron-right text-xs mr-2"></i>Apply for Pension</a></li>
                        <li><a href="#conditions" class="hover:text-white transition"><i class="fa-solid fa-chevron-right text-xs mr-2"></i>Terms & Conditions</a></li>
                        <li><a href="#" class="hover:text-white transition"><i class="fa-solid fa-chevron-right text-xs mr-2"></i>Admin Login</a></li>
                    </ul>
                </div>
                
                <div>
                    <h3 class="text-xl font-bold mb-4 border-b border-blue-700 pb-2 inline-block">Contact Us (ଯୋଗାଯୋଗ)</h3>
                    <ul class="space-y-3 text-sm text-blue-200">
                        <li class="flex items-center justify-center md:justify-start">
                            <div class="bg-blue-800 p-2 rounded-full mr-3"><i class="fa-solid fa-phone"></i></div>
                            <span class="font-bold text-white text-lg">8910223342</span>
                        </li>
                        <li class="flex items-center justify-center md:justify-start">
                            <div class="bg-blue-800 p-2 rounded-full mr-3"><i class="fa-solid fa-envelope"></i></div>
                            <span class="text-white">admin@kulusutar.in</span>
                        </li>
                    </ul>
                </div>

            </div>
            
            <div class="text-center text-blue-400 text-sm border-t border-blue-800 pt-6 mt-6">
                <p>&copy; 2026 Private Social Security Pension Scheme | All Rights Reserved.</p>
                <p class="mt-1 text-xs">This is a private initiative. Not affiliated with any government department.</p>
            </div>
        </div>
    </footer>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design
