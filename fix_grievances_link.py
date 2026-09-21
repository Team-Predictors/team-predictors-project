import re

for filepath in ['client/dashboard.html', 'client/project1.html', 'client/grievances.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find the Projects link block and append Grievances link
    pattern = r'(<a href="project1\.html.*?<i class="fa-solid fa-folder-open"></i> Projects\s*</a>)'
    replacement = r'\g<1>\n                <a href="grievances.html?v=6" class="nav-item text-gray-700 px-4 py-2.5 rounded-md font-bold text-sm flex items-center gap-2 transition-colors">\n                    <i class="fa-solid fa-user-group"></i> Grievances\n                </a>'
    
    # Only replace if Grievances link doesn't already exist
    if 'Grievances\n                </a>' not in content:
        content = re.sub(pattern, replacement, content)
        
        # In grievances.html, we need to make the Grievances link active
        if 'grievances.html' in filepath:
            content = content.replace(
                '<a href="grievances.html?v=6" class="nav-item text-gray-700',
                '<a href="grievances.html?v=6" class="nav-active nav-item'
            )
            content = content.replace(
                '<a href="dashboard.html?v=5" class="nav-active',
                '<a href="dashboard.html?v=5" class="nav-item text-gray-700'
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Grievances link to {filepath}")
