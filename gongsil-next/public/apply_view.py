import sys
import re

with open('article_view.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '// ── HTML 조립 ──'
end_marker = '    // 댓글 글자수 카운터'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Markers not found')
    sys.exit(1)

new_html = '''// ── HTML 조립 ──
    document.getElementById('pageBody').innerHTML =
    '<div style="display:flex; gap:30px; max-width:1100px; margin:0 auto; align-items:flex-start;">'+
      
      // ── 좌측 실제 기사 뷰 영역 ──
      '<div style="flex:1; min-width:0; background:#fff; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,0.06); overflow:hidden;">'+
        
        // 상단 디바이스 버튼 영역 (흰 배경 위쪽)
        '<div style="display:flex; justify-content:center; padding:15px; border-bottom:1px solid #f0f0f0; background:#fafafa;">' +
          '<div class="device-btns" style="background:#fff; border:1px solid #ddd; display:flex; gap:4px; padding:6px 8px; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">' +
              '<button class="device-btn active" id="devPC" data-dev="pc" onclick="setDevice(this.dataset.dev)" title="PC" style="padding:4px 16px; background:#0bc2c2; color:#fff;">🖥️</button>' +
              '<button class="device-btn" id="devTB" data-dev="tablet" onclick="setDevice(this.dataset.dev)" title="태블릿" style="padding:4px 16px;">📱</button>' +
              '<button class="device-btn" id="devMB" data-dev="mobile" onclick="setDevice(this.dataset.dev)" title="모바일" style="padding:4px 16px;">📲</button>' +
          '</div>' +
        '</div>' +

        // 실제 기사 컨텐츠 영역 (흰색)
        '<div class="preview-frame" id="previewFrame" style="transition:all 0.3s; margin:0 auto; padding:40px;">'+
          '<div style="margin-bottom:0;">'+
            '<div style="font-size: 14px; color: #666; margin-bottom: 8px; font-weight: 600;">'+crumb+'</div>'+
            '<h1 style="font-size: 32px; font-weight: 800; color: #111; line-height: 1.3; margin-bottom: 16px; letter-spacing:-1px; word-break:keep-all;">'+escHtml(a.title||'(제목 없음)')+'</h1>'+
            '<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; padding-bottom: 16px; margin-bottom: 30px;">'+
               '<div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: #666;">'+
                    '<span style="color:#111; font-weight:bold;">'+(a.reporter_name||'공실뉴스')+'</span>'+
                    '<span style="display:inline-block; width:1px; height:12px; background:#ddd; margin:0 4px;"></span>'+
                    '<span>입력 '+pubDate+'</span>'+
                    '<span style="display:inline-block; width:1px; height:12px; background:#ddd; margin:0 4px;"></span>'+
                    '<span>조회수 '+(a.view_count||0)+'</span>'+
               '</div>'+
               '<div style="display: flex; gap: 8px; align-items: center;">'+
                    '<button class="btn-toolbar" style="padding:4px 12px; border-radius:4px; font-size:13px; background:#fff; border:1px solid #ddd; color:#555; cursor:pointer;" onclick="shareArticle()">🔗 주소복사</button>'+
                    '<button class="btn-toolbar" style="padding:4px 12px; border-radius:4px; font-size:13px; background:#fff; border:1px solid #ddd; color:#555; cursor:pointer;" data-msg="미리보기 화면입니다" onclick="alert(this.dataset.msg)">💻 미리보기</button>'+
               '</div>'+
            '</div>'+
          '</div>'+
          
          '<div class="article-body" style="font-size:17px; line-height:1.75; color:#222; padding:0; border:none;">'+
            subtitleHtml +
            bodyHtml +
          '</div>'+
        '</div>'+
      '</div>'+
      
      // ── 우측 사이드바 영역 ──
      '<div class="article-sidebar" style="width:280px; flex-shrink:0;">'+
        '<div class="sidebar-card" style="margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); padding:20px; background:#fff; border-radius:10px;">'+
          '<div class="sidebar-card-title" style="margin-bottom:12px; font-size:14px; font-weight:bold;">⚙️ 기사 관리</div>'+
          '<div class="admin-actions">'+
            approveBtnHtml +
            '<div style="display:flex; gap:6px; margin-top:8px;">'+
              '<button class="btn-full btn-edit" onclick="goEdit()" style="flex:1; background:#eff6ff; color:#3b82f6; border:1px solid #bfdbfe; padding:8px 0; border-radius:4px; cursor:pointer;">기사 수정</button>'+
              '<button class="btn-full btn-delete" onclick="deleteArticle()" style="flex:1; background:#fef2f2; color:#ef4444; border:1px solid #fecaca; padding:8px 0; border-radius:4px; cursor:pointer;">기사 삭제</button>'+
            '</div>'+
            '<button class="btn-full" onclick="goBack()" style="margin-top:8px; width:100%; background:#fff; border:1px solid #ddd; color:#555; padding:8px 0; border-radius:4px; cursor:pointer;">← 목록으로 돌아가기</button>'+
          '</div>'+
        '</div>'+
        
        '<div class="sidebar-card" style="margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); padding:20px; background:#fff; border-radius:10px;">'+
          '<div class="sidebar-card-title" style="margin-bottom:12px; font-size:14px; font-weight:bold;">📋 기사 서비스 로그</div>'+
          '<div class="sidebar-memo">'+
            '<textarea id="logMemoInput" placeholder="이곳에 서비스 메모를 남겨두세요..." style="width:100%; box-sizing:border-box; height:110px; padding:10px; border:1px solid #ddd; border-radius:6px; resize:none; margin-bottom:8px; font-family:inherit;"></textarea>'+
            '<div class="sidebar-memo-footer" style="text-align:right;">'+
              '<button onclick="addServiceLog()" style="padding:6px 16px; background:#444; color:#fff; border:none; border-radius:4px; cursor:pointer; font-weight:600;">등록</button>'+
            '</div>'+
          '</div>'+
          '<ul class="sidebar-log-list" id="serviceLogList" style="list-style:none; padding:0; margin-top:12px; font-size:13px; color:#555; border-top:1px solid #f0f0f0; padding-top:12px;">'+
            '<li class="log-empty" style="color:#aaa; text-align:center; padding:10px;">등록된 로그가 없습니다.</li>'+
          '</ul>'+
        '</div>'+
        
        '<div class="sidebar-card" style="margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06); padding:20px; background:#fff; border-radius:10px;">'+
          '<div class="sidebar-card-title" style="margin-bottom:12px; font-size:14px; font-weight:bold;">🕐 기사 최근 로그</div>'+
          '<ul class="sidebar-log-list" id="recentLogList" style="list-style:none; padding:0; margin:0; font-size:13px; color:#555;">\'+buildRecentLog(a)+\'</ul>'+
        '</div>'+
      '</div>'+
    '</div>;\n\n'''

new_content = content[:start_idx] + new_html + content[end_idx:]

with open('article_view.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Success')
