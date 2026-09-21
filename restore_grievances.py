import re
import glob

# 1. Recreate grievances.html with empty content
with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Split dashboard shell
dash_top = dash.split('<!-- MAIN CONTENT -->')[0]

# Add Grievances link back to dashboard
# It was inside:
#                 <a href="project1.html?v=5" class="nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors">
#                     <i class="fa-solid fa-folder-open"></i> Projects
#                 </a>
#             </div>
dash_top = dash_top.replace('                </a>\n            </div>', '                </a>\n                <a href="grievances.html?v=6" class="TEMP_GRIEV">\n                    <i class="fa-solid fa-user-group"></i> Grievances\n                </a>\n            </div>')

dash_top = dash_top.replace('nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', 'TEMP_DASH')
dash_top = dash_top.replace('TEMP_GRIEV', 'nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
dash_top = dash_top.replace('TEMP_DASH', 'nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
dash_top = dash_top.replace('<title>INFRA GATI - Dashboard</title>', '<title>INFRA GATI - Grievances</title>')

dash_bottom = dash.split('</main>')[1]

inner_main = '''
    <main class="flex-1 p-6 lg:p-8 max-w-[1600px] w-full mx-auto flex items-center justify-center">
        <div class="text-center text-gray-500">
            <i class="fa-solid fa-person-digging text-6xl mb-4 text-gray-300"></i>
            <h2 class="text-2xl font-bold text-gray-700">Grievances Module</h2>
            <p class="mt-2">This module is currently under construction. Content will be added soon.</p>
        </div>
    </main>
'''

final_griev = dash_top + '\n<!-- MAIN CONTENT -->\n' + inner_main + '\n' + dash_bottom

with open('client/grievances.html', 'w', encoding='utf-8') as f:
    f.write(final_griev)

# 2. Add Grievances link back to dashboard.html and project1.html
for filepath in ['client/dashboard.html', 'client/project1.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('                </a>\n            </div>', '                </a>\n                <a href="grievances.html?v=6" class="nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors">\n                    <i class="fa-solid fa-user-group"></i> Grievances\n                </a>\n            </div>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Restored grievances.html and nav links!")
