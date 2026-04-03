import re
with open(r'c:\Users\user\Desktop\test\news_write.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_pattern = r"sb\.rpc\('increment_photo_used', \{ pid: photoId \}\)\.catch\(\(\) => \{[\s\S]*?\}\);"
new_code = '''// Supabase v2 rpc returns {data, error}, not a promise that rejects
            sb.rpc('increment_photo_used', { pid: photoId }).then(res => {
                if (res && res.error) {
                    sb.from('user_photos').select('used_count').eq('id', photoId).single().then(({ data }) => {
                        if (data) sb.from('user_photos').update({ used_count: (data.used_count || 0) + 1 }).eq('id', photoId);
                    });
                }
            });'''
            
content = re.sub(old_pattern, new_code, content)
content = content.replace("async function usePhotoInArticle(url, photoId) { console.log('usePhotoInArticle called', url, photoId);", "async function usePhotoInArticle(url, photoId) {")
content = content.replace("window.insertNodeAtCursor = function(htmlString) { console.log('insertNodeAtCursor called!');", "window.insertNodeAtCursor = function(htmlString) {")

with open(r'c:\Users\user\Desktop\test\news_write.html', 'w', encoding='utf-8') as f:
    f.write(content)
