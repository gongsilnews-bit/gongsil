import re

with open(r'c:\Users\user\Desktop\test\news_write.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. AI 런처 추출 빛 제거 (main에서)
ai_block_regex = r'(<!-- AI 기사작성 런처 -->\s*<div class="form-row" style="background: linear-gradient[^>]+>\s*<div class="form-label"[^>]+>.*?</div>\s*</div>)'
match_ai = re.search(ai_block_regex, html, re.DOTALL)
if not match_ai:
    print("Could not find AI Launcher in main.")
    exit(1)

ai_block_raw = match_ai.group(1)
html = html.replace(ai_block_raw, '') # Remove from main

# 2. sidebar 에서 필요없는 내용 지우기
# 템플릿, 특수문자, 구분선 (lines 664-675)
left_tools_delete_regex = r'<div class="tool-icon" style="font-weight:900(.*?)<span>구분선</span>\s*</div>'
html = re.sub(left_tools_delete_regex, '', html, flags=re.DOTALL)

# 본문크기 (tools-bottom) 영역 제거
tools_bottom_regex = r'<div class="tools-bottom">.*?</div>\s*</div>'
html = re.sub(tools_bottom_regex, '', html, flags=re.DOTALL)

# 3. 새로운 위치 (tools-grid 끝나는 부분) 뒤에 AI 런처 삽입
# sidebar에 맞게 AI 런처 디자인 새로 작성
new_ai_launcher = '''
            <!-- AI 기사작성 런처 (사이드바 이동) -->
            <div style="background: linear-gradient(135deg, #fffbeb, #ffedd5); border: 1px solid #fdba74; border-radius: 8px; padding: 16px; margin-top: 20px; display: flex; flex-direction: column; gap: 12px;">
                <div style="color: #ea580c; font-weight: 800; font-size: 15px; display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 20px;">🪄</span> AI 마법사
                </div>
                <div id="aiLauncherDesc" style="font-size: 12px; color: #431407; font-weight: 600; line-height: 1.4;">
                    매물 정보만 한 번 입력하면 기사, 블로그, 쇼츠 대본까지 5가지 콘텐츠를 AI가 한 번에 완성해 줍니다!
                </div>
                <button type="button" id="aiLauncherBtn" class="btn" onclick="openAiwizardDynamic()" style="background: #f97316; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 700; font-size: 13px; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.4); display: flex; align-items: center; justify-content: center; width: 100%; gap: 6px;">
                    ✨ 실행하기
                </button>
            </div>
'''

html = html.replace('</div>\n        </aside>', '</div>\n' + new_ai_launcher + '        </aside>')

with open(r'c:\Users\user\Desktop\test\news_write.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS")
