import re

with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

with open('client/project1.html', 'r', encoding='utf-8') as f:
    orig_proj = f.read()
    
inner_main_match = re.search(r'(<main.*?</main>)', orig_proj, re.DOTALL)
if inner_main_match:
    inner_main = inner_main_match.group(1)
    
    dash_top = dash.split('<!-- MAIN CONTENT -->')[0]
    dash_top = dash_top.replace('nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', 'TEMP_DASH')
    dash_top = dash_top.replace('nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', 'TEMP_PROJ')
    
    # We used href="projects.html?v=4" in dashboard, so let's match that to make it active
    dash_top = re.sub(r'(<a href="projects\.html\?v=4" class=")TEMP_PROJ', r'\1nav-active nav-item px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors', dash_top)
    dash_top = dash_top.replace('TEMP_DASH', 'nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
    dash_top = dash_top.replace('TEMP_PROJ', 'nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors')
    
    dash_top = dash_top.replace('<title>INFRA GATI - Dashboard</title>', '<title>INFRA GATI - Projects</title>')
    
    step_styles = re.search(r'/\* Stepper styles \*/.*?</style>', orig_proj, re.DOTALL)
    if step_styles:
        dash_top = dash_top.replace('</style>', '\n        ' + step_styles.group(0))

    dash_bottom = dash.split('</main>')[1]
    
    final_proj = dash_top + '\n<!-- MAIN CONTENT -->\n' + inner_main + '\n' + dash_bottom
    
    # Actually, rename project1 to projects.html
    with open('client/projects.html', 'w', encoding='utf-8') as f:
        f.write(final_proj)
    print("projects.html successfully built with Top Nav shell from project1!")
else:
    print("Could not find <main> in project1.html")
