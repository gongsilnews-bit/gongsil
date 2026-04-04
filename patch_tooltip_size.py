import glob

old_css = """        .icon-tooltip-wrap::after {
            content: attr(data-tooltip);
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            margin-top: 6px;
            background-color: rgba(17, 17, 17, 0.85);
            color: #fff;
            font-size: 11px;
            font-weight: 600;
            padding: 4px 6px;
            border-radius: 4px;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s ease;
            pointer-events: none;
            z-index: 10000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }"""

new_css = """        .icon-tooltip-wrap::after {
            content: attr(data-tooltip);
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            margin-top: 8px;
            background-color: #ffffff;
            color: #111111;
            font-size: 14px;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s ease;
            pointer-events: none;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }"""

for file_path in glob.glob('*.html'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()
            
    original_len = len(content)
    
    # We replace strict exact string, ignoring different line endings
    content = content.replace(old_css.replace('\\n', '\\r\\n'), new_css)
    content = content.replace(old_css, new_css)

    if len(content) != original_len:
        print(f"Patched tooltip CSS in {file_path}")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            with open(file_path, 'w', encoding='utf-16') as f:
                f.write(content)
