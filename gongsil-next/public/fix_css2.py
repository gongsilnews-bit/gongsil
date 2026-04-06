import re

with open(r'c:\Users\user\Desktop\test\news_write.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix search-box CSS
text = text.replace(
    '.search-box input {\n            width: 100%; padding: 10px 30px 10px 10px; background: #f9fafb;\n            border: 1px solid #e5e7eb; border-radius: 4px; font-size: 13px; outline:none;\n        }',
    '.search-box input {\n            width: 100%; padding: 10px 30px 10px 10px; background: #f9fafb;\n            border: 1px solid #e5e7eb; border-radius: 4px; font-size: 13px; outline:none; box-sizing: border-box;\n        }'
)

# Fix dash-drop-box CSS
text = text.replace(
    '.dash-drop-box {\n            border: 1px dashed #d1d5db; background: #fdfdfd; padding: 20px;\n            text-align: center; color: #9ca3af; font-size: 12px; border-radius: 4px;\n            min-height: 80px; display: flex; flex-direction: column; justify-content: center;\n        }',
    '.dash-drop-box {\n            border: 1px dashed #d1d5db; background: #fdfdfd; padding: 20px;\n            text-align: center; color: #9ca3af; font-size: 12px; border-radius: 4px;\n            min-height: 80px; display: flex; flex-direction: column; justify-content: center; box-sizing: border-box;\n        }'
)

# Fix libYoutubeInput div
text = text.replace(
    '<div style="display:flex; border:1px solid #6b7280; border-radius:4px; overflow:hidden;">',
    '<div style="display:flex; border:1px solid #6b7280; border-radius:4px; overflow:hidden; box-sizing: border-box; width: 100%;">'
)
text = text.replace(
    'placeholder="YouTube영상링크입력" style="flex:1; padding:10px; border:none; outline:none; font-size:13px; color:#6b7280; background:#fff;"',
    'placeholder="YouTube영상링크입력" style="flex:1; padding:10px; border:none; outline:none; font-size:13px; color:#6b7280; background:#fff; box-sizing: border-box; min-width: 0;"'
)

# Also check for box-sizing universally on col-library padding:
text = text.replace(
    '        .col-library {\n            width: 320px;\n            position: sticky;',
    '        .col-library {\n            width: 320px;\n            position: sticky;\n            box-sizing: border-box;'
)

with open(r'c:\Users\user\Desktop\test\news_write.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS")
