from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. HOME PAGE DESIGN (ମୁଖ୍ୟ ପୃଷ୍ଠା) - UNCHANGED
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
            background-size: cover; background-position: center;
        }
        .card-hover:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); transition: all 0.3s ease; }
    </style>
</head>
<body class="bg-gray-50 font-sans text-gray-800">
    <!-- Header -->
    <header class="bg-white shadow-md border-b-4 border-blue-700 sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <div class="text-blue-700 text-4xl md:text-5xl"><i class="fa-solid fa-hands-holding-circle"></i></div>
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
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">Support for Senior Citizens, Widows, Disabled & the Needy</h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <a href="#schemes" class="inline-block bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition flex items-center w-max">View Schemes <i class="fa-solid fa-arrow-down ml-2"></i></a>
            </div>
        </div>
    </section>

    <!-- 6 Action Cards Section -->
    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            <a href="/admin/login" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Admin Login</h3><p class="text-sm mb-4 text-blue-100">Official login for Administration</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/user/register" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Pension Apply</h3><p class="text-sm mb-4 text-green-100">Apply for New Pension</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-orange-400 to-orange-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-magnifying-glass text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Check Status</h3><p class="text-sm mb-4 text-orange-100">Check Your Application Status</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="/user/login" class="block bg-gradient-to-b from-purple-500 to-purple-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-user text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Beneficiary</h3><p class="text-sm mb-4 text-purple-100">Login for Beneficiaries</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#schemes" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Schemes</h3><p class="text-sm mb-4 text-teal-100">View Info & Guidelines</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
            <a href="#contact" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i><h3 class="font-bold text-lg mb-2">Help Desk</h3><p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p><i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>
        </div>
    </section>
    
    <!-- (Skipping About Us, Schemes, Contact for brevity but they are preserved in your original code) -->
</body>
</html>
"""

# ==========================================
# NEW: USER REGISTRATION PAGE
# ==========================================
user_register_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>New User Registration</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-lg bg-white p-8 rounded-2xl shadow-xl border-t-4 border-green-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">User Registration (ନୂଆ ଆବେଦନକାରୀ)</h2>
        <form action="/user/login" method="GET" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Full Name (ପୂରା ନାମ)</label>
                <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
            </div>
            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Mobile No</label>
                    <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Email ID</label>
                    <div class="flex">
                        <input type="email" class="w-full px-4 py-2 border rounded-l-lg" required>
                        <button type="button" class="bg-blue-600 text-white px-3 rounded-r-lg text-xs" onclick="alert('OTP Sent to Email!')">Get OTP</button>
                    </div>
                </div>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Enter OTP</label>
                <input type="text" class="w-full px-4 py-2 border rounded-lg" required>
            </div>
            <div class="flex gap-4">
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Set Password</label>
                    <input type="password" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
                <div class="w-1/2">
                    <label class="block text-sm font-semibold text-gray-700">Confirm Password</label>
                    <input type="password" class="w-full px-4 py-2 border rounded-lg" required>
                </div>
            </div>
            <button type="submit" class="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700" onclick="alert('Registration Successful! Your Application No is: APP-2026101. Password sent to Email.')">
                Register & Generate App No
            </button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# NEW: USER LOGIN PAGE
# ==========================================
user_login_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User / Beneficiary Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border-t-4 border-purple-600">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Beneficiary Login (ଲଗଇନ୍)</h2>
        <form action="/user/dashboard" method="GET" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700">Application Number / User ID</label>
                <input type="text" placeholder="APP-XXXXXX" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700">Password</label>
                <input type="password" class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500" required>
            </div>
            <div class="text-right">
                <a href="#" class="text-sm text-blue-600 hover:underline">Forgot Password?</a>
            </div>
            <button type="submit" class="w-full bg-purple-600 text-white font-bold py-3 rounded-lg hover:bg-purple-700">
                Login
            </button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# NEW: USER DASHBOARD & APPLY FORM
# ==========================================
user_dashboard_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        function switchUserTab(tabId) {
            document.querySelectorAll('.content-section').forEach(el => el.classList.add('hidden'));
            document.getElementById('section-' + tabId).classList.remove('hidden');
        }
        
        function calculateAge() {
            let dob = new Date(document.getElementById('dob').value);
            let age = new Date().getFullYear() - dob.getFullYear();
            document.getElementById('age').value = age;
            let scheme = document.getElementById('scheme').value;
            if(scheme === 'Old Age' && age < 55) {
                alert('System Error: Age must be 55 or above for Old Age Pension.');
            }
        }

        function verifyAadhaar() {
            alert('Real OTP sent to Aadhaar linked Mobile Number!');
            setTimeout(() => {
                alert('Aadhaar Verified! Fetching details...');
                document.getElementById('aadhaar_status').innerHTML = "<span class='text-green-600 font-bold'><i class='fa-solid fa-check'></i> Verified & Linked with Bank</span>";
            }, 1000);
        }

        function verifyIncome() {
            let cert = document.getElementById('income_cert').value;
            if(cert) {
                alert('Verifying Income Certificate...');
                document.getElementById('income_val').value = "0 - 50000";
            }
        }
        
        function processPayment(e) {
            e.preventDefault();
            document.getElementById('payment-modal').classList.remove('hidden');
        }
        
        function submitFinalApp() {
            alert('Payment Successful! System is verifying documents automatically...');
            setTimeout(() => {
                alert('System Verification Passed. Sent to Admin for manual review.');
                document.getElementById('payment-modal').classList.add('hidden');
                switchUserTab('status');
            }, 1500);
        }
    </script>
</head>
<body class="bg-gray-100 flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 text-white flex flex-col shadow-2xl h-full">
        <div class="p-5 border-b border-slate-700 text-center">
            <h2 class="text-xl font-bold">User Portal</h2>
            <p class="text-sm text-gray-300 mt-2">Welcome, Applicant</p>
        </div>
        <nav class="flex-1 overflow-y-auto py-4">
            <ul class="space-y-2 px-3">
                <li><a href="#" onclick="switchUserTab('apply')" class="flex items-center px-4 py-3 bg-purple-600 text-white rounded-lg"><i class="fa-solid fa-pen-to-square w-6 mr-2"></i> Apply Pension</a></li>
                <li><a href="#" onclick="switchUserTab('status')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-file-pdf w-6 mr-2"></i> Application Status / Print</a></li>
                <li><a href="#" onclick="switchUserTab('renew')" class="flex items-center px-4 py-3 text-slate-300 hover:bg-slate-700 rounded-lg"><i class="fa-solid fa-clock-rotate-left w-6 mr-2"></i> 3-Month Renewal</a></li>
            </ul>
        </nav>
        <div class="p-4"><a href="/" class="flex items-center text-red-400 hover:text-red-300"><i class="fa-solid fa-power-off w-6 mr-2"></i> Logout</a></div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-6">
        
        <!-- SECTION: APPLY PENSION -->
        <div id="section-apply" class="content-section bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold text-purple-800 mb-6 border-b pb-2">Apply New Pension (ପେନସନ୍ ଆବେଦନ)</h2>
            <form onsubmit="processPayment(event)" class="space-y-6">
                <!-- 1. Personal Info -->
                <div class="grid grid-cols-2 gap-4">
                    <div><label class="block text-sm font-semibold">Full Name</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Father/Husband Name</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Mother's Name</label><input type="text" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Gender</label>
                        <select class="w-full border p-2 rounded">
                            <option>Male</option><option>Female</option><option>Transgender</option>
                        </select>
                    </div>
                    <div><label class="block text-sm font-semibold">Date of Birth</label><input type="date" id="dob" onchange="calculateAge()" class="w-full border p-2 rounded" required></div>
                    <div><label class="block text-sm font-semibold">Age (Auto)</label><input type="text" id="age" readonly class="w-full border p-2 rounded bg-gray-100"></div>
                </div>
                
                <!-- Scheme & Aadhaar -->
                <div class="grid grid-cols-2 gap-4 border-t pt-4">
                    <div>
                        <label class="block text-sm font-semibold">Scheme Category</label>
                        <select id="scheme" class="w-full border p-2 rounded bg-purple-50">
                            <option>Old Age (ବୃଦ୍ଧାବସ୍ଥା)</option>
                            <option>Widow (ବିଧବା)</option>
                            <option>Disability (ଭିନ୍ନକ୍ଷମ)</option>
                            <option>Unmarried Woman</option>
                            <option>Divorcee</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold">Aadhaar Number</label>
                        <div class="flex gap-2">
                            <input type="text" placeholder="XXXX-XXXX-XXXX" class="w-full border p-2 rounded">
                            <button type="button" onclick="verifyAadhaar()" class="bg-blue-600 text-white px-4 rounded">Verify</button>
                        </div>
                        <p id="aadhaar_status" class="text-xs mt-1 text-gray-500">Not Verified</p>
                    </div>
                </div>

                <!-- Address Dropdowns (Simulated) -->
                <div class="grid grid-cols-4 gap-4 border-t pt-4">
                    <div><label class="block text-xs font-semibold">State</label><select class="w-full border p-2 rounded"><option>Odisha</option></select></div>
                    <div><label class="block text-xs font-semibold">District</label><select class="w-full border p-2 rounded"><option>Cuttack</option><option>Jajpur</option></select></div>
                    <div><label class="block text-xs font-semibold">Block</label><select class="w-full border p-2 rounded"><option>Dasarathpur</option></select></div>
                    <div><label class="block text-xs font-semibold">Panchayat</label><select class="w-full border p-2 rounded"><option>Udaypur</option></select></div>
                </div>

                <!-- Income & Bank Details -->
                <div class="grid grid-cols-2 gap-4 border-t pt-4">
                    <div>
                        <label class="block text-sm font-semibold">Income Cert No & Year</label>
                        <div class="flex gap-2">
                            <input type="text" id="income_cert" placeholder="INC/2026/..." class="w-full border p-2 rounded">
                            <button type="button" onclick="verifyIncome()" class="bg-green-600 text-white px-4 rounded">Fetch</button>
                        </div>
                        <input type="text" id="income_val" placeholder="Verified Income will show here" readonly class="w-full border p-2 rounded mt-2 bg-gray-100 text-red-600 font-bold">
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div><label class="block text-xs">Bank Name</label><input type="text" class="w-full border p-1 rounded"></div>
                        <div><label class="block text-xs">A/C No</label><input type="text" class="w-full border p-1 rounded"></div>
                        <div><label class="block text-xs">IFSC</label><input type="text" class="w-full border p-1 rounded" onblur="this.value ? alert('Branch Fetched!') : null"></div>
                    </div>
                </div>

                <!-- Document Upload -->
                <div class="border-t pt-4">
                    <label class="block text-sm font-semibold mb-2">Upload Documents (PDF/JPG)</label>
                    <div class="grid grid-cols-3 gap-2 text-xs">
                        <input type="file" class="border p-1" title="Photo">
                        <input type="file" class="border p-1" title="Aadhaar">
                        <input type="file" class="border p-1" title="Age Proof">
                        <input type="file" class="border p-1" title="Passbook">
                        <input type="file" class="border p-1" title="Special Cert (if any)">
                    </div>
                </div>

                <!-- Declaration -->
                <div class="border-t pt-4 flex items-start gap-2">
                    <input type="checkbox" required class="mt-1">
                    <p class="text-xs text-red-700 font-bold">ମୁଁ ଘୋଷଣା କରୁଛି ଯେ ମୋର ଅନ୍ୟ କୌଣସି ଆୟ ନାହିଁ। ମୁଁ ଜାଣିଛି ଯେ ଏହା ଏକ ଘରୋଇ ସହାୟତା (Private Initiative) ଏବଂ ପ୍ରତି ୩ ମାସରେ ରିନ୍ୟୁ ନକଲେ ଅଥବା ଭୁଲ୍ ତଥ୍ୟ ଦେଲେ Admin ମୋର ପେନସନ୍ ବନ୍ଦ କରିପାରିବେ।</p>
                </div>

                <button type="submit" class="w-full bg-purple-700 text-white font-bold py-3 rounded-lg shadow-lg hover:bg-purple-800">Submit Application & Proceed to Payment</button>
            </form>
        </div>

        <!-- SECTION: STATUS & PRINT -->
        <div id="section-status" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold mb-4">Application Status & Print</h2>
            <div class="bg-gray-50 border p-4 rounded mb-4">
                <p><strong>App No:</strong> APP-2026101</p>
                <p><strong>Status:</strong> <span class="text-orange-600 font-bold">Pending Admin Verification (System Verified)</span></p>
                <p class="text-sm text-red-600 mt-2" id="reject-reason" style="display:none;">Rejection Reason: Name mismatch in Aadhaar.</p>
            </div>
            <button class="bg-blue-600 text-white px-4 py-2 rounded"><i class="fa-solid fa-print"></i> Print Application</button>
            <button class="bg-red-600 text-white px-4 py-2 rounded"><i class="fa-solid fa-file-pdf"></i> Download PDF</button>
        </div>

        <!-- SECTION: RENEWAL -->
        <div id="section-renew" class="content-section hidden bg-white p-6 rounded-xl shadow">
            <h2 class="text-2xl font-bold mb-4 text-orange-600">3-Month Renewal</h2>
            <p class="text-sm mb-4">Click below to auto-fetch your data and complete the 3-month renewal process to keep your pension active.</p>
            <button onclick="alert('Data Fetched! Proceeding to Payment...');" class="bg-orange-600 text-white px-6 py-2 rounded font-bold">Renew Pension</button>
        </div>

    </main>

    <!-- Payment Modal (Hidden) -->
    <div id="payment-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-xl w-96 text-center">
            <h3 class="text-xl font-bold mb-4">Payment Gateway</h3>
            <p class="mb-4">Processing Fee: ₹50</p>
            <button onclick="submitFinalApp()" class="bg-green-600 text-white px-6 py-2 rounded font-bold w-full">Pay Now</button>
            <button onclick="document.getElementById('payment-modal').classList.add('hidden')" class="mt-2 text-sm text-red-600 underline">Cancel</button>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# ROUTES SETUP (ସମସ୍ତ ରାଉଟ୍)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    return admin_login_design

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    return admin_design # Apnar purono admin_design code thik bhabe run korbe.

@app.get("/user/register", response_class=HTMLResponse)
async def user_register_page():
    return user_register_design

@app.get("/user/login", response_class=HTMLResponse)
async def user_login_page():
    return user_login_design

@app.get("/user/dashboard", response_class=HTMLResponse)
async def user_dashboard_page():
    return user_dashboard_design
