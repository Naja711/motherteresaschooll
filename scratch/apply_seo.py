import os
import re
import glob

domain = "https://motherteresaschoolnazirpur.com"
base_keywords = "Mother Teresa School Nazirpur, best school in Nazirpur, private English medium school West Bengal, CBSE school Nadia, top school in Nazirpur, holistic education, co-educational institute, Christian minority school"

schema = """
    <!-- JSON-LD Schema Markup -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "School",
      "name": "Mother Teresa School",
      "url": "https://motherteresaschoolnazirpur.com",
      "logo": "https://motherteresaschoolnazirpur.com/assets/images/school_logo.jpg",
      "description": "Mother Teresa School in Nazirpur, West Bengal is a top Private English Medium, Co-Educational Institute administered by the Roman Catholic Diocese of Krishnagar.",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Village: Mahishakola, P.O.: Nazirpur, P.S.: Karimpur",
        "addressLocality": "Nazirpur",
        "addressRegion": "West Bengal",
        "postalCode": "741165",
        "addressCountry": "IN"
      },
      "telephone": "+918167586775",
      "email": "mtsnazirpur4@gmail.com"
    }
    </script>
"""

files = glob.glob('*.html')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Update keywords meta tag
    keywords_match = re.search(r'<meta name="keywords"\s*content="([^"]*)">', content, re.IGNORECASE | re.DOTALL)
    if keywords_match:
        old_kw = keywords_match.group(1).replace('\n', ' ').strip()
        new_kw = f"{base_keywords}, {old_kw}"
        
        # Remove duplicates while keeping order
        kws = [k.strip() for k in new_kw.split(',')]
        seen = set()
        unique_kws = [k for k in kws if not (k.lower() in seen or seen.add(k.lower()))]
        final_kw = ", ".join(unique_kws)
        
        content = re.sub(
            r'<meta name="keywords"\s*content="[^"]*">',
            f'<meta name="keywords" content="{final_kw}">',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

    # 2. Add canonical URL
    if '<link rel="canonical"' not in content:
        url = f"{domain}/{f}" if f != 'index.html' else f"{domain}/"
        canonical = f'    <link rel="canonical" href="{url}">'
        content = content.replace('</head>', f'{canonical}\n</head>')

    # 3. Add robots directives
    if '<meta name="robots"' not in content:
        robots = '    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
        content = content.replace('</head>', f'{robots}\n</head>')

    # 4. OpenGraph tags
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    desc_match = re.search(r'<meta name="description"\s*content="([^"]*)">', content, re.IGNORECASE | re.DOTALL)
    
    if title_match and desc_match:
        page_title = title_match.group(1).strip()
        page_desc = desc_match.group(1).replace('\n', ' ').strip()
        url = f"{domain}/{f}" if f != 'index.html' else f"{domain}/"
        
        if 'property="og:' not in content:
            og_tags = f"""    <!-- OpenGraph Tags -->
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{domain}/assets/images/school_logo.jpg">
    <meta property="og:site_name" content="Mother Teresa School, Nazirpur">"""
            content = content.replace('</head>', f'{og_tags}\n</head>')

    # 5. Add Schema to index.html
    if f == 'index.html' and 'application/ld+json' not in content:
        content = content.replace('</head>', f'{schema}</head>')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Enhanced SEO tags for {f}")
