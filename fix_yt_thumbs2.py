import glob

files = glob.glob('*.html')

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    # We will find the exact block from `let extractUrl` to `<div class="an-img" ...>NO IMAGE</div>`;`
    start_str = "let extractUrl = (news.article_media && news.article_media.url) ? news.article_media.url : news.image_url;"
    end_str = ">NO IMAGE</div>`;"
    
    if start_str in content and end_str in content:
        start_idx = content.find(start_str)
        end_idx = content.find(end_str, start_idx) + len(end_str)
        
        if start_idx != -1 and end_idx > start_idx + len(start_str):
            old_block = content[start_idx:end_idx]
            
            # Make sure this is the right block
            if "const imgHtml =" in old_block:
                replacement = """let extractUrl = (news.article_media && news.article_media.url) ? news.article_media.url : news.image_url;
            let isVideo = false;
            
            if (extractUrl && extractUrl.includes('youtube.com/embed/')) {
                isVideo = true;
                const parts = extractUrl.split('youtube.com/embed/');
                if (parts.length > 1) {
                    const vId = parts[1].split('?')[0].split('"')[0];
                    extractUrl = `https://img.youtube.com/vi/${vId}/mqdefault.jpg`;
                }
            }

            if(!extractUrl && news.content) {
                const ytIframeMatch = news.content.match(/<iframe[^>]+src=["']([^"']*youtube\\.com\\/embed\\/[^"']+)["']/i);
                if (ytIframeMatch) {
                    isVideo = true;
                    const parts = ytIframeMatch[1].split('youtube.com/embed/');
                    if (parts.length > 1) {
                        const vId = parts[1].split('?')[0].split('"')[0];
                        extractUrl = `https://img.youtube.com/vi/${vId}/mqdefault.jpg`;
                    }
                } else {
                    const imgMatch = news.content.match(/<img[^>]+src=["']([^"']+)["']/i);
                    if(imgMatch) extractUrl = imgMatch[1];
                }
            }
            
            const playOverlay = isVideo ? `<div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); width:44px; height:44px; background:rgba(0,0,0,0.4); border-radius:50%; border: 2.5px solid white; display:flex; align-items:center; justify-content:center; z-index:5;"><svg viewBox="0 0 24 24" width="24" height="24" fill="white" style="margin-left:4px;"><path d="M8 5v14l11-7z"/></svg></div>` : ``;

            let imgHtml = extractUrl ? `<img src="${extractUrl}" style="width:100%; height:100%; object-fit:cover; border-radius:6px;" onerror="this.src='https://via.placeholder.com/160x100?text=News'">` : `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#ccc;font-size:12px;background:#f4f6fa;border-radius:6px;">NO IMAGE</div>`;
            imgHtml = `<div class="an-img" style="position:relative; flex-shrink:0;">${imgHtml}${playOverlay}</div>`;"""
                
                new_content = content[:start_idx] + replacement + content[end_idx:]
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Updated {f}")
