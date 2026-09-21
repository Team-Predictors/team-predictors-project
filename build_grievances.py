import re

with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

dash_top = dash.split('<!-- MAIN CONTENT -->')[0]
dash_top = dash_top.replace('nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', 'TEMP_DASH')
dash_top = dash_top.replace('nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', 'TEMP_GRIEV')

# We used href="#" for Grievances. Let's change all nav links to correct ones.
dash_top = dash_top.replace('href="#" class="TEMP_GRIEV', 'href="grievances.html?v=4" class="nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
dash_top = dash_top.replace('TEMP_DASH', 'nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
dash_top = dash_top.replace('TEMP_GRIEV', 'nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
dash_top = dash_top.replace('<title>INFRA GATI - Dashboard</title>', '<title>INFRA GATI - Grievances</title>')

# Update dashboard and projects to point to grievances.html
# We will do this later.

dash_bottom = dash.split('</main>')[1]

inner_main = '''
    <main class="flex-1 p-6 lg:p-8 max-w-[1600px] w-full mx-auto flex items-center justify-center">
        <div class="text-center text-gray-500">
            <i class="fa-solid fa-person-digging text-6xl mb-4 text-gray-300"></i>
            <h2 class="text-2xl font-bold text-gray-700">Grievances Module</h2>
            <p class="mt-2">This module is under construction.</p>
        </div>
    </main>
'''

final_griev = dash_top + '\n<!-- MAIN CONTENT -->\n' + inner_main + '\n' + dash_bottom

with open('client/grievances.html', 'w', encoding='utf-8') as f:
    f.write(final_griev)
print("grievances.html created.")
