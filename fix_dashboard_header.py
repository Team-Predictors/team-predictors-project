import re

# Read projects.html to get the gold standard header
with open('client/projects.html', 'r', encoding='utf-8') as f:
    projects_html = f.read()

header_match = re.search(r'(<header.*?</header>)', projects_html, re.DOTALL)
if not header_match:
    print("Could not find header in projects.html")
    exit(1)
new_header = header_match.group(1)

# Read dashboard.html
with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    dash_html = f.read()

# Replace header
dash_html = re.sub(r'<header.*?</header>', new_header, dash_html, flags=re.DOTALL)

# Write back
with open('client/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_html)
    
print("Dashboard header updated successfully!")
