import os
import re
import glob

files = glob.glob('*.html')

# We want the favicon to be consistently linked in a way that always works
favicon_tags = """
    <link rel="icon" type="image/x-icon" href="favicon.ico?v=3">
    <link rel="shortcut icon" href="favicon.ico?v=3">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/school_logo.jpg?v=3">
"""

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove any existing icon or shortcut icon links to avoid duplicates/conflicts
    content = re.sub(r'    <link rel="(?:shortcut )?icon"[^>]*>\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'    <link rel="apple-touch-icon"[^>]*>\s*', '', content, flags=re.IGNORECASE)
    
    # Insert new tags before </head>
    content = content.replace('</head>', f'{favicon_tags}</head>')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated favicon links in {f}")
