import re

with open('client/projects.html', 'r', encoding='utf-8') as f:
    projects_html = f.read()

# Extract aside
aside_match = re.search(r'(<aside.*?</aside>)', projects_html, re.DOTALL)
new_aside = aside_match.group(1)

new_aside = new_aside.replace('sidebar-active flex items-center gap-3 px-3 py-2.5 rounded-r-lg text-sm font-medium text-white transition-colors ml-[-12px] pl-[15px]', 'TEMP_INACTIVE')
new_aside = new_aside.replace('sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors', 'TEMP_ACTIVE_CANDIDATE')

dashboard_regex = r'(<a href="dashboard\.html" class=")TEMP_ACTIVE_CANDIDATE'
new_aside = re.sub(dashboard_regex, r'\1sidebar-active flex items-center gap-3 px-3 py-2.5 rounded-r-lg text-sm font-medium text-white transition-colors ml-[-12px] pl-[15px]', new_aside)

new_aside = new_aside.replace('TEMP_INACTIVE', 'sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors')
new_aside = new_aside.replace('TEMP_ACTIVE_CANDIDATE', 'sidebar-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-green-50 transition-colors')

# Extract header
header_match = re.search(r'(<header.*?</header>)', projects_html, re.DOTALL)
new_header = header_match.group(1)

body_match = re.search(r'<body class="(.*?)">', projects_html)
body_class = body_match.group(1)

style_match = re.search(r'<style>.*?</style>', projects_html, re.DOTALL)
new_styles = style_match.group(0)

# Dashboard
with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash_html = f.read()

dash_html = re.sub(r'<body[^>]*>', f'<body class="{body_class}">', dash_html)
dash_html = re.sub(r'<style>.*?</style>', new_styles, dash_html, flags=re.DOTALL)
dash_html = re.sub(r'<aside.*?</aside>', new_aside, dash_html, flags=re.DOTALL)

# In dashboard.html, the top header is currently:
# <header class="h-20 bg-white shadow-sm border-b border-gray-100 flex items-center justify-between px-8">
dash_html = re.sub(r'<header.*?</header>', new_header, dash_html, flags=re.DOTALL)

# Main container wrapping header and main content
dash_html = re.sub(r'<div class="flex-1.*?">', '<div class="flex-1 flex flex-col h-full overflow-hidden bg-[#f4f7f6]">', dash_html, count=1)

with open('client/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_html)
    
print("Dashboard updated successfully!")
