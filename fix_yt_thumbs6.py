import glob

content = open('script.js', encoding='utf-8').read()

# Replace the Top 1 article thumbnail play button
content = content.replace(
    'width:60px; height:60px; background:rgba(0,0,0,0.6); border-radius:50%; display:flex; align-items:center; justify-content:center; padding-left:4px; z-index:5;',
    'width:64px; height:64px; background:rgba(0,0,0,0.4); border-radius:50%; border: 3px solid white; display:flex; align-items:center; justify-content:center; z-index:5;'
)
content = content.replace(
    '<svg viewBox="0 0 24 24" width="30" height="30" fill="white">',
    '<svg viewBox="0 0 24 24" width="30" height="30" fill="white" style="margin-left:5px;">'
)

# And one in the side items if the SVG doesn't have margin-left:
content = content.replace(
    '<svg viewBox="0 0 24 24" width="14" height="14" fill="white">',
    '<svg viewBox="0 0 24 24" width="16" height="16" fill="white" style="margin-left:2px;">'
)

# And in portal list
content = content.replace(
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="white">',
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="white" style="margin-left:3px;">'
)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
