import glob

files = ["board.html", "news_all.html", "news_etc.html", "news_finance.html", "news_law.html", "news_life.html", "news_politics.html"]

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    start_str = "let extractUrl = (news.article_media && news.article_media.url)"
    
    # We find the exact line containing NO IMAGE
    idx = content.find(start_str)
    if idx == -1: 
        continue
        
    # Find the end of the NO IMAGE line.
    end_idx = content.find("NO IMAGE</div>\\`;", idx)
    end_str_len = len("NO IMAGE</div>\\`;")
    
    # Just in case `news_all.html` doesn't have the backslash because it was replaced by fixing script earlier:
    if end_idx == -1:
        end_idx = content.find("NO IMAGE</div>`;", idx)
        end_str_len = len("NO IMAGE</div>`;")
    
    if end_idx != -1:
        end_idx += end_str_len
        
        replacement = r"""let extractUrl = (news.article_media && news.article_media.url) ? news.article_media.url : news.image_url;
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
                const ytIframeMatch = news.content.match(/<iframe[^>]+src=["']([^"']*youtube\.com\/embed\/[^"']+)["']/i);
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

            let imgHtml = extractUrl ? `\<img src="\${extractUrl}" style="width:100%; height:100%; object-fit:cover; border-radius:6px;" onerror="this.src='https://via.placeholder.com/160x100?text=News'"\>` : `\<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#ccc;font-size:12px;background:#f4f6fa;border-radius:6px;"\>NO IMAGE\</div\>`;
            imgHtml = `\<div class="an-img" style="position:relative; flex-shrink:0;"\>\${imgHtml}\${playOverlay}\</div\>`;"""
        
        # fix backslash escaping (they should be escaped in the JS file as \` and \${var})
        replacement = replacement.replace(r"\<", r"\`").replace(r"\>", r"\`")
        
        new_content = content[:idx] + replacement + content[end_idx:]
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {f}")
