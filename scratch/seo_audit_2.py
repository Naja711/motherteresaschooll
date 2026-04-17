import glob
import re
import shutil

shutil.copy('assets/images/school_logo.jpg', 'favicon.ico')

files = glob.glob('*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add apple-touch-icon if missing
    if 'apple-touch-icon' not in content:
        apple_icon = '    <link rel="apple-touch-icon" href="assets/images/school_logo.jpg">'
        content = content.replace('</head>', f'{apple_icon}\n</head>')
        
    imgs = re.findall(r'<img[^>]+>', content, re.IGNORECASE)
    missing_alt = [img for img in imgs if 'alt=' not in img.lower()]
    
    h1s = re.findall(r'<h1[^>]*>.*?</h1>', content, re.IGNORECASE | re.DOTALL)
    
    print(f"--- {f} ---")
    print(f"  H1 Count: {len(h1s)}")
    print(f"  Images missing alt: {len(missing_alt)}")
    if missing_alt:
        print("  " + "\n  ".join(missing_alt))
        
    # write content back (apple-touch-icon)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
