files = ['client/dashboard.html', 'client/projects.html', 'client/grievances.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('href="#" class="nav-active', 'href="grievances.html?v=5" class="nav-active')
    content = content.replace('href="#" class="nav-item', 'href="grievances.html?v=5" class="nav-item')
    content = content.replace('dashboard.html?v=4', 'dashboard.html?v=5')
    content = content.replace('projects.html?v=4', 'projects.html?v=5')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print("Top Nav links fixed across all 3 admin pages!")
