import glob

old_svg = """<svg onclick="document.getElementById('topSearchWrap').classList.toggle('active'); document.getElementById('topSearchInput').focus();" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>"""
new_svg = """<svg onclick="document.getElementById('topSearchWrap').classList.toggle('active'); document.getElementById('topSearchInput').focus();" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" title="검색"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>"""

for file_path in glob.glob("*.html"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-16") as f:
            content = f.read()

    original_len = len(content)
    content = content.replace(old_svg, new_svg)

    if len(content) != original_len:
        print(f"Patched {file_path}")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except:
            with open(file_path, "w", encoding="utf-16") as f:
                f.write(content)
