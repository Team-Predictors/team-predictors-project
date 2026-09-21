import re

# 1. Read projects.html shell
with open('client/projects.html', 'r', encoding='utf-8') as f:
    projects_html = f.read()

# Extract everything BEFORE <main ...>
before_main = re.search(r'(.*?)<main[^>]*>', projects_html, re.DOTALL).group(1)
# Extract the <main> tag itself to keep its classes
main_tag = re.search(r'(<main[^>]*>)', projects_html).group(1)
# Extract everything AFTER </main>
after_main = re.search(r'</main>(.*)', projects_html, re.DOTALL).group(1)

# Adjust active states in before_main (Sidebar)
# Make Dashboard active, Projects inactive
before_main = before_main.replace('sidebar-active flex items-center gap-3 px-3 py-2.5 rounded-r-lg text-sm font-medium text-white transition-colors ml-[-12px] pl-[15px]', 'TEMP_INACTIVE')
before_main = before_main.replace('sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors', 'TEMP_ACTIVE_CANDIDATE')
before_main = re.sub(r'(<a href="dashboard\.html[^"]*" class=")TEMP_ACTIVE_CANDIDATE', r'\1sidebar-active flex items-center gap-3 px-3 py-2.5 rounded-r-lg text-sm font-medium text-white transition-colors ml-[-12px] pl-[15px]', before_main)
before_main = before_main.replace('TEMP_INACTIVE', 'sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors')
before_main = before_main.replace('TEMP_ACTIVE_CANDIDATE', 'sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors')

# 2. Read dashboard.html inner content
with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash_html = f.read()

# Extract everything between <main...> and </main>
main_content_match = re.search(r'<main[^>]*>(.*?)</main>', dash_html, re.DOTALL)
if main_content_match:
    inner_content = main_content_match.group(1)
else:
    # If there is no main tag, maybe it's inside some other container? Let's just fallback to the whole body minus header and sidebar
    print("Could not find <main> in dashboard.html. Exiting.")
    exit(1)

# Extract any <script> tags at the end of dashboard.html (like Chart.js scripts)
scripts_match = re.search(r'</main>.*?((?:<script.*?</script>\s*)+)</body>', dash_html, re.DOTALL)
scripts = scripts_match.group(1) if scripts_match else ''

# 3. Assemble the new dashboard.html
final_html = before_main + main_tag + inner_content + '\n        </main>\n    </div>\n' + scripts + '\n</body>\n</html>'

with open('client/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Dashboard completely rebuilt with Projects shell!")
