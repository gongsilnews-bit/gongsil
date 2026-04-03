import re

with open(r'c:\Users\user\Desktop\test\news_write.html', 'r', encoding='utf-8') as f:
    text = f.read()

ai_section = '''            <!-- AI 기사작성 런처 (사이드바 이동) -->
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
# Find all occurrences
parts = text.split(ai_section)
# If it was inserted twice, parts will have 3 elements
if len(parts) == 3:
    # Remove the second insertion (which is between parts[1] and parts[2])
    text = parts[0] + ai_section + parts[1] + parts[2]
    
with open(r'c:\Users\user\Desktop\test\news_write.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS", len(parts))
