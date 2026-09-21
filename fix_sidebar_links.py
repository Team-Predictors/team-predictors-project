import re

files = ['client/projects.html', 'client/dashboard.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace href="dashboard.html" with href="dashboard.html?v=42"
    content = re.sub(r'href="dashboard\.html[^"]*"', 'href="dashboard.html?v=42"', content)
    # Replace href="projects.html" with href="projects.html?v=42"
    content = re.sub(r'href="projects\.html[^"]*"', 'href="projects.html?v=42"', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
print("Sidebar links updated with cache busters!")
