import os
import re

nav_template = '''    <!-- UNIFIED BIG NAVBAR -->
    <nav class="w-full h-[105px] px-8 lg:px-20 flex items-center justify-between bg-white border-b border-gray-100 z-50 relative shrink-0">
        <!-- Logo -->
        <a href="index.html" class="flex items-center gap-3 cursor-pointer">
            <i class="fa-solid fa-leaf text-[45px] text-green-600"></i>
            <div>
                <h1 class="text-[30px] font-extrabold tracking-tight text-gray-900 leading-none" style="font-family: 'Inter', sans-serif;">INFRA GATI</h1>
                <p class="text-[10px] tracking-[5px] uppercase font-semibold text-gray-500 mt-1.5" style="font-family: 'Inter', sans-serif;">Land Today. A Better Tomorrow.</p>
            </div>
        </a>

        <!-- Links -->
        <div class="hidden lg:flex items-center gap-10 text-[14px] font-bold text-gray-700" style="font-family: 'Inter', sans-serif;">
            <a href="index.html" class="hover:text-green-700 transition">Home</a>
            <a href="about.html" class="hover:text-green-700 transition">About</a>
            <a href="features.html" class="hover:text-green-700 transition">Features</a>
            <a href="how_it_works.html" class="hover:text-green-700 transition">How It Works</a>
            <a href="contact.html" class="hover:text-green-700 transition">Contact</a>
        </div>

        <!-- Button -->
        <div>
            <a href="login_demo.html" class="bg-[#126f43] hover:bg-green-800 text-white px-8 py-3 rounded-md font-bold text-[14px] transition-colors shadow-md" style="font-family: 'Inter', sans-serif;">
                Login
            </a>
        </div>
    </nav>'''

files = ['index.html', 'about.html', 'features.html', 'how_it_works.html', 'contact.html', 'login_demo.html']

for f in files:
    path = os.path.join('client', f)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the existing nav tag and its contents
    new_content = re.sub(r'<!-- UNIFIED BIG NAVBAR -->.*?<\/nav>', nav_template, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print(f"Updated {f}")
