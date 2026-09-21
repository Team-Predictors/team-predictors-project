import glob
import re

for filepath in glob.glob('client/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replacement of href
    new_content = content.replace('href="projects.html', 'href="project1.html')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            print(f"Updated links in {filepath}")
