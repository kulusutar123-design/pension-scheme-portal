from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
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
                background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.7)), url('https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
                background-size: cover; background-position: center;
            }
            .page-sec { display: none; }
            .page-sec.active { display: block; }
            .nav-btn.active-tab { color: #1d4ed8; border-bottom: 3px solid #1d4ed8; }
        </style>
        <script>
            function switchTab(tabId) {
                let sections = document.getElementsByClassName('page-sec');
                for (let s of sections) { s.classList.remove('active'); }
                document.getElementById(tabId).classList.add('active');

                let btns = document.getElementsByClassName('nav-btn');
                for (let b of btns) { b.classList.remove('active-tab'); }
                document.getElementById('nav-' + tabId).classList.add('active-tab');
            }
        </script>
    </head>
    <body class="bg-gray-50 font-sans text-gray-800 flex flex-col min-h-screen">

        <header class="bg-white shadow-md border-b-4 border-blue-800 sticky top-0 z-50">
            <div class="container mx-auto px-4 py-3 flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <i class="fa-solid fa-hands-holding-child text-blue-800 text-3xl"></i>
                    <div>
                        <h1 class="text-lg md:text-xl font-bold text-blue-900">Private Social Security Pension</h1>
                        <p class="text-xs text-gray-600 font-semibold">A Private Initiative for the Needy</p>
                    </div>
                </div>
                <div class="hidden md:flex space-x-6 font-bold text-gray-700">
                    <button id="nav-home" onclick="switchTab('home')" class="nav-btn active-tab pb-1">Home</button>
                    <button id="nav-about" onclick="switchTab('about')" class="nav-btn pb-1">About Us</button>
                    <button id="nav-schemes" onclick="switchTab('schemes')" class="nav-btn pb-1">Schemes</button>
                    <button id="nav-conditions" onclick="switchTab('conditions')" class="nav-btn pb-1">Conditions</button>
                    <button id="nav-contact" onclick="switchTab('contact')" class="nav-btn pb-1">Contact Us</button>
                </div>
            </div>
        </header>

        <main class="flex-grow">
            <!-- HOME -->
            <section id="home" class="page-sec active">
                <div class="hero-bg py-16 px-4 border-b">
                    <div class="container mx-auto max-w-2xl bg-white p-8 rounded-xl shadow-lg border-l-8 border-blue-700">
                        <h2 class="text-3xl font-extrabold text-blue-900 mb-4">Support for Senior Citizens, Widows, Disabled and the Needy</h2>
                        <p class="text-gray-700 mb-6 font-medium">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                        <button onclick="switchTab('schemes')" class="bg-blue-700 text-white px-6 py-3 rounded font-bold shadow hover:bg-blue-800">Apply Now</button>
                    </div>
                </div>
            </section>

            <!-- ABOUT -->
            <section id="about" class="page-sec container mx-auto px-4 py-12 max-w-3xl">
                <h2 class="text-2xl font-bold text-blue-900 mb-4 border-b pb-2"><i class="fa-solid fa-circle-info mr-2"></i>About Us / ଆମ ବିଷୟରେ</h2>
                <div class="bg-white p-6 rounded shadow border">
                    <p class="text-gray-700 leading-relaxed font-medium">
                        <b>English:</b> The Private Social Security Pension Scheme is a 100% private and non-governmental initiative. Our goal is to provide financial support and respect to the needy.<br><br>
                        <b>ଓଡ଼ିଆ:</b> ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା।
                    </p>
                </div>
            </section>

            <!-- SCHEMES -->
            <section id="schemes" class="page-sec container mx-auto px-4 py-12 max-w-4xl">
                <h2 class="text-2xl font-bold text-blue-900 mb-6 border-b pb-2"><i class="fa-solid fa-list mr-2"></i>Schemes & Age Limits</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-white p-5 rounded shadow border-l-4 border-blue-600">
                        <h3 class="font-bold text-lg text-blue-900">Old Age Pension (ବୃଦ୍ଧାବସ୍ଥା)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 55 to 100 Years | Amount: ₹3000 / Year (Credited Monthly)</p>
                    </div>
                    <div class="bg-white p-5 rounded shadow border-l-4 border-green-600">
                        <h3 class="font-bold text-lg text-green-900">Disability Pension (ଭିନ୍ନକ୍ଷମ)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 10 to 100 Years | Amount: ₹3500 / Year (Credited Monthly)</p>
                    </div>
                    <div class="bg-white p-5 rounded shadow border-l-4 border-purple-600">
                        <h3 class="font-bold text-lg text-purple-900">Widow Pension (ବିଧବା)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 30 to 55 Years</p>
                    </div>
                    <div class="bg-white p-5 rounded shadow border-l-4 border-pink-600">
                        <h3 class="font-bold text-lg text-pink-900">Unmarried Woman (ଅବିବାହିତା)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 30 to 55 Years</p>
                    </div>
                    <div class="bg-white p-5 rounded shadow border-l-4 border-red-600">
                        <h3 class="font-bold text-lg text-red-900">Divorcee Women (ଛାଡପତ୍ର)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 35 to 55 Years</p>
                    </div>
                    <div class="bg-white p-5 rounded shadow border-l-4 border-orange-600">
                        <h3 class="font-bold text-lg text-orange-900">Transgender (କିନ୍ନର)</h3>
                        <p class="text-sm text-gray-600 mt-1">Age: 35 to 55 Years</p>
                    </div>
                </div>
            </section>

            <!-- CONDITIONS -->
            <section id="conditions" class="page-sec container mx-auto px-4 py-12 max-w-3xl">
                <h2 class="text-2xl font-bold text-red-900 mb-6 border-b pb-2"><i class="fa-solid fa-scale-balanced mr-2"></i>Strict Terms & Conditions</h2>
                <div class="bg-red-50 p-6 rounded border border-red-200 text-gray-800 space-y-3 text-sm font-medium">
                    <p><b>1. No Refund Policy:</b> Application charges are strictly non-refundable for all castes. If rejected, money will not be returned.</p>
                    <p><b>2. Payment Timeline:</b> First pension installment will be credited strictly after 3 months from the application end date.</p>
                    <p><b>3. Mandatory Renewal:</b> Beneficiaries must renew their pension every 3 months.</p>
                    <p><b>4. Admin Rights:</b> The Admin reserves absolute rights to cancel/stop pension anytime. No legal action can be taken against Admin.</p>
                </div>
            </section>

            <!-- CONTACT -->
            <section id="contact" class="page-sec container mx-auto px-4 py-12 max-w-xl text-center">
                <h2 class="text-2xl font-bold text-blue-900 mb-6 border-b pb-2"><i class="fa-solid fa-phone mr-2"></i>Contact Us</h2>
                <div class="bg-white p-6 rounded shadow border">
                    <p class="text-xl font-extrabold text-blue-800 mb-2"><i class="fa-solid fa-phone mr-2"></i> 8910223342</p>
                    <p class="text-lg font-bold text-gray-700"><i class="fa-solid fa-envelope mr-2"></i> admin@kulusutar.in</p>
                </div>
            </section>
        </main>

        <footer class="bg-blue-900 text-white text-center py-4 mt-auto text-xs">
            <p>&copy; 2026 Private Social Security Pension Scheme | All Rights Reserved.</p>
        </body>
        </html>
    """
