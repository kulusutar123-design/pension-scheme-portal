from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. HOME PAGE DESIGN (ମୁଖ୍ୟ ପୃଷ୍ଠା)
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
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 transition duration-300 flex items-center w-max">
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

    <!-- ABOUT US SECTION -->
    <section id="about" class="container mx-auto px-4 py-10">
        <div class="bg-white rounded-xl p-8 shadow-md border-t-4 border-blue-700">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-blue-900"><i class="fa-solid fa-circle-info mr-2"></i> ଆମ ବିଷୟରେ (About Us)</h2>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Odia -->
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-100 shadow-sm">
                    <h3 class="font-bold text-blue-800 text-lg mb-3 border-b pb-2">Odia (ଓଡ଼ିଆ)</h3>
                    <p class="text-gray-700 leading-relaxed text-sm">"ପ୍ରାଇଭେଟ୍ ସୋସିଆଲ୍ ସିକ୍ୟୁରିଟି ପେନସନ୍ ସ୍କିମ୍ ହେଉଛି ଏକ ସମ୍ପୂର୍ଣ୍ଣ ଘରୋଇ ଏବଂ ବେସରକାରୀ ପ୍ରୟାସ। ଆମର ଉଦ୍ଦେଶ୍ୟ ଗରିବ ଏବଂ ଅସହାୟ ଲୋକଙ୍କୁ ଆର୍ଥିକ ସହାୟତା ଏବଂ ସମ୍ମାନ ପ୍ରଦାନ କରିବା। ପେନସନ୍ କେବଳ ଟଙ୍କା ନୁହେଁ, ଏହା ହେଉଛି ସମ୍ମାନ।"</p>
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
# 3. ADMIN DASHBOARD DESIGN
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
                <li><a href="#" class="flex items-center px-4 py-3 bg-blue-700 text-white rounded-lg"><i class="fa-solid fa-gauge w-6 mr-2"></i> Dashboard</a></li>
                <li><a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-file-signature w-6 mr-2"></i> New Apps <span class="ml-auto bg-red-500 px-2 rounded-full text-xs">3</span></a></li>
                <li><a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-users w-6 mr-2"></i> Beneficiaries</a></li>
                <li><a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> Renewals</a></li>
                <li><a href="#" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-800 rounded-lg"><i class="fa-solid fa-money-bill-transfer w-6 mr-2"></i> Payments</a></li>
            </ul>
        </nav>
        
        <div class="p-4 border-t border-slate-700">
            <a href="/" class="flex items-center px-4 py-2 text-red-400 hover:bg-red-500 hover:text-white rounded-lg"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout</a>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col h-full overflow-hidden relative">
        <header class="bg-white shadow-sm border-b px-6 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold"><i class="fa-solid fa-list-check text-blue-600 mr-2"></i> Verification</h1>
            <div class="flex items-center space-x-4">
                <span class="text-sm font-medium">Welcome, <strong>Super Admin</strong></span>
            </div>
        </header>

        <div class="flex-1 overflow-y-auto p-6 bg-gray-50">
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
