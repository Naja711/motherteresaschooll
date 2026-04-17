import glob
import os

files = glob.glob('*.html')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    old_icon = '<link rel="icon" type="image/jpg" href="assets/images/school_logo.jpg?v=2">'
    new_icons = '<link rel="icon" type="image/x-icon" href="/favicon.ico">\n    <link rel="shortcut icon" href="/favicon.ico">'
    
    if old_icon in content:
        content = content.replace(old_icon, new_icons)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
