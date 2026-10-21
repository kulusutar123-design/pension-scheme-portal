from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Ehi variable bhitare amara sampurna website ra design (HTML/CSS) achi
html_design = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Social Security Pension Scheme</title>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome for Icons -->
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
            
            <!-- Desktop Menu -->
            <div class="hidden md:flex space-x-6 items-center">
                <a href="#" class="text-blue-700 font-bold flex items-center border-b-2 border-blue-700 pb-1"><i class="fa-solid fa-house mr-1"></i> Home</a>
                <a href="#" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-circle-info mr-1"></i> About Us</a>
                <a href="#" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-file-lines mr-1"></i> Schemes</a>
                <a href="#" class="text-gray-700 hover:text-blue-700 font-semibold flex items-center transition duration-300"><i class="fa-solid fa-phone mr-1"></i> Contact</a>
            </div>

            <!-- Mobile Menu Icon -->
            <div class="md:hidden flex items-center">
                <button class="text-gray-700 text-2xl focus:outline-none">
                    <i class="fa-solid fa-bars"></i>
                </button>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-bg py-16 px-4 border-b">
        <div class="container mx-auto">
            <div class="max-w-2xl bg-white/95 p-8 rounded-xl shadow-xl border-l-8 border-blue-600 backdrop-blur-sm">
                <h2 class="text-3xl md:text-4xl font-extrabold text-blue-900 mb-4 leading-tight">
                    Support for Senior Citizens, Widows, Disabled & the Needy
                </h2>
                <p class="text-lg text-gray-700 font-medium mb-6">Providing financial independence and respect through our private pension initiative. Pension is not just money, it is respect.</p>
                <button class="bg-blue-700 text-white px-8 py-3 rounded-lg font-bold shadow-md hover:bg-blue-800 hover:shadow-lg transition duration-300 flex items-center">
                    Learn More <i class="fa-solid fa-arrow-right ml-2"></i>
                </button>
            </div>
        </div>
    </section>

    <!-- 6 Action Cards Section -->
    <section class="container mx-auto px-4 py-12 relative -mt-10 md:-mt-16 z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-6">
            
            <a href="#" class="block bg-gradient-to-b from-blue-500 to-blue-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-building text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Admin Login</h3>
                <p class="text-sm mb-4 text-blue-100">Official login for Administration</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-green-500 to-green-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-pen-to-square text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Pension Apply</h3>
                <p class="text-sm mb-4 text-green-100">Apply for New Pension Scheme</p>
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
                <p class="text-sm mb-4 text-purple-100">Login for Pension Beneficiaries</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-teal-400 to-teal-600 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-book-open text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Schemes</h3>
                <p class="text-sm mb-4 text-teal-100">View Scheme Info & Guidelines</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

            <a href="#" class="block bg-gradient-to-b from-pink-500 to-pink-700 text-white rounded-xl p-6 text-center shadow-lg card-hover border-2 border-white">
                <i class="fa-solid fa-headset text-4xl mb-4"></i>
                <h3 class="font-bold text-lg mb-2">Help Desk</h3>
                <p class="text-sm mb-4 text-pink-100">Get Help and Contact Us</p>
                <i class="fa-solid fa-circle-chevron-right text-2xl"></i>
            </a>

        </div>
    </section>

    <!-- Bottom Information Section -->
    <section class="container mx-auto px-4 py-8 mb-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            
            <!-- About -->
            <div class="bg-blue-50 rounded-xl p-6 border border-blue-100 shadow-sm hover:shadow-md transition">
                <div class="flex items-center mb-4">
                    <i class="fa-solid fa-users text-blue-700 text-2xl mr-3"></i>
                    <h3 class="font-bold text-xl text-blue-900">About the Scheme</h3>
                </div>
                <p class="text-gray-700 text-sm mb-5 leading-relaxed text-justify">
                    The Private Social Security Pension Scheme aims to provide financial assistance to senior citizens, widows, disabled persons and other vulnerable sections of society for a better and secure life. Our goal is to ensure dignity for everyone.
                </p>
                <button class="text-blue-700 font-bold text-sm hover:text-blue-900 flex items-center">Read Full Story <i class="fa-solid fa-arrow-right-long ml-2"></i></button>
            </div>

            <!-- Quick Links -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition">
                <div class="flex items-center mb-4 border-b pb-3">
                    <i class="fa-solid fa-link text-blue-700 text-2xl mr-3"></i>
                    <h3 class="font-bold text-xl text-blue-900">Quick Links</h3>
                </div>
                <ul class="space-y-3 mt-4">
                    <li><a href="#" class="text-gray-700 hover:text-blue-700 flex justify-between items-center text-sm font-medium transition group"><span class="flex items-center"><i class="fa-solid fa-chevron-right text-blue-500 text-xs mr-3 group-hover:translate-x-1 transition"></i> Scheme Guidelines</span></a></li>
                    <li><a href="#" class="text-gray-700 hover:text-blue-700 flex justify-between items-center text-sm font-medium transition group"><span class="flex items-center"><i class="fa-solid fa-chevron-right text-blue-500 text-xs mr-3 group-hover:translate-x-1 transition"></i> Eligibility Criteria</span></a></li>
                    <li><a href="#" class="text-gray-700 hover:text-blue-700 flex justify-between items-center text-sm font-medium transition group"><span class="flex items-center"><i class="fa-solid fa-chevron-right text-blue-500 text-xs mr-3 group-hover:translate-x-1 transition"></i> Required Documents</span></a></li>
                    <li><a href="#" class="text-gray-700 hover:text-blue-700 flex justify-between items-center text-sm font-medium transition group"><span class="flex items-center"><i class="fa-solid fa-chevron-right text-blue-500 text-xs mr-3 group-hover:translate-x-1 transition"></i> Frequently Asked Questions</span></a></li>
                </ul>
            </div>

            <!-- Updates -->
            <div class="bg-blue-50 rounded-xl p-6 border border-blue-100 shadow-sm hover:shadow-md transition">
                <div class="flex items-center mb-4 border-b border-blue-200 pb-3">
                    <i class="fa-solid fa-bell text-blue-700 text-2xl mr-3"></i>
                    <h3 class="font-bold text-xl text-blue-900">Latest Updates</h3>
                </div>
                <div class="space-y-4 mt-4">
                    <div class="flex items-start bg-white p-3 rounded shadow-sm">
                        <div class="bg-blue-700 text-white text-center rounded p-1 min-w-[45px] mr-3 shadow">
                            <div class="text-sm font-bold">21</div>
                            <div class="text-[10px] uppercase">Oct</div>
                        </div>
                        <p class="text-sm text-gray-700 font-medium">New Pension Application Process Now Online for 2026-27.</p>
                    </div>
                    <div class="flex items-start bg-white p-3 rounded shadow-sm">
                        <div class="bg-blue-700 text-white text-center rounded p-1 min-w-[45px] mr-3 shadow">
                            <div class="text-sm font-bold">15</div>
                            <div class="text-[10px] uppercase">Oct</div>
                        </div>
                        <p class="text-sm text-gray-700 font-medium">Updated eligibility guidelines uploaded for Widow Pension.</p>
                    </div>
                </div>
            </div>

        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white py-8 border-t-4 border-blue-600">
        <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center text-sm">
            <p class="text-gray-300">&copy; 2026 Private Social Security Pension Scheme | All Rights Reserved.</p>
            <div class="flex space-x-4 mt-4 md:mt-0">
                <a href="#" class="text-blue-400 hover:text-white transition"><i class="fa-brands fa-facebook text-xl"></i></a>
                <a href="#" class="text-blue-400 hover:text-white transition"><i class="fa-brands fa-twitter text-xl"></i></a>
                <a href="#" class="text-blue-400 hover:text-white transition"><i class="fa-brands fa-youtube text-xl"></i></a>
            </div>
        </div>
    </footer>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_design
