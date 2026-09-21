import re
with open('client/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
# Remove the <header ...> tag before the nav
content = re.sub(r'<header[^>]*>\s*(<!-- UNIFIED BIG NAVBAR -->)', r'\1', content)
# Remove the closing </header> after the nav
content = re.sub(r'(</nav>)\s*</header>', r'\1', content)
with open('client/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
