import glob

html_code = """
                <div class="icon-tooltip-wrap" data-tooltip="회원가입">
                    <svg style="cursor: pointer;" onclick="window.handleLoginClick && window.handleLoginClick(event, 'signup')" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" title="회원가입"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                </div>
                <div class="icon-tooltip-wrap" data-tooltip="로그인">
                    <svg style="cursor: pointer;" onclick="window.handleLoginClick && window.handleLoginClick(event, 'login')" id="headerLoginOnlyBtn" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" title="로그인"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
                </div>
"""

css_code = """
    <style>
        .icon-tooltip-wrap {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .icon-tooltip-wrap::after {
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
        }
        .icon-tooltip-wrap:hover::after {
            opacity: 1;
            visibility: visible;
        }
    </style>
"""

old_login_block = """<svg style=\"cursor: pointer;\" onclick=\"window.handleLoginClick && window.handleLoginClick(event, 'signup')\" viewBox=\"0 0 24 24\" fill=\"none\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" title=\"회원가입\"><path d=\"M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2\"></path><circle cx=\"12\" cy=\"7\" r=\"4\"></circle></svg>
                <svg style=\"cursor: pointer;\" onclick=\"window.handleLoginClick && window.handleLoginClick(event, 'login')\" id=\"headerLoginOnlyBtn\" viewBox=\"0 0 24 24\" fill=\"none\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" title=\"로그인\"><path d=\"M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4\"></path><polyline points=\"10 17 15 12 10 7\"></polyline><line x1=\"15\" y1=\"12\" x2=\"3\" y2=\"12\"></line></svg>"""

search_old = """<svg onclick="document.getElementById('topSearchWrap').classList.toggle('active'); document.getElementById('topSearchInput').focus();" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" title="검색"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>"""
search_new = """<div class="icon-tooltip-wrap" data-tooltip="검색">
                <svg onclick="document.getElementById('topSearchWrap').classList.toggle('active'); document.getElementById('topSearchInput').focus();" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" title="검색"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>"""

for file_path in glob.glob('*.html'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()
    
    modified = False
    
    if old_login_block in content:
        content = content.replace(old_login_block, html_code.strip())
        modified = True
        
    if search_old in content:
        content = content.replace(search_old, search_new)
        modified = True

    if modified:
        if '</head>' in content and css_code.strip() not in content:
            content = content.replace('</head>', css_code.strip() + '\n</head>')
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            with open(file_path, 'w', encoding='utf-16') as f:
                f.write(content)
        print(f'Patched tooltip wrappers in {file_path}')
