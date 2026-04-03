import sys

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Split before <main class="container...
split_idx = html.find('<main class="container')
header_html = html[:split_idx]

content = header_html + """
    <style>
        .news-layout {
            display: flex;
            gap: 40px;
            margin-top: 30px;
            margin-bottom: 60px;
        }
        /* Left: List */
        .news-list-area {
            flex: 1;
        }
        .list-header {
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 20px;
            color: var(--brand-navy);
            border-bottom: 2px solid #222;
            padding-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .an-card {
            display: flex;
            gap: 20px;
            border-bottom: 1px solid #eee;
            padding: 24px 10px;
            align-items: center;
            cursor: pointer;
            transition: background 0.2s;
            border-radius: 8px;
        }
        .an-card:hover {
            background: #f9f9f9;
        }
        .an-img {
            width: 160px;
            height: 100px;
            border-radius: 6px;
            object-fit: cover;
            background: #f4f6fa;
            flex-shrink: 0;
        }
        .an-body {
            flex: 1;
        }
        .an-title {
            font-size: 18px;
            font-weight: 700;
            color: #111;
            margin-bottom: 8px;
            line-height: 1.4;
            cursor: pointer;
        }
        .an-title:hover {
            color: var(--brand-blue);
            text-decoration: underline;
        }
        .an-desc {
            font-size: 14px;
            color: #555;
            line-height: 1.5;
            margin-bottom: 12px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .an-meta {
            font-size: 13px;
            color: #999;
        }
        
        /* Pagination */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
            gap: 10px;
        }
        .page-btn {
            border: 1px solid #ddd;
            background: #fff;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            color: #555;
            cursor: pointer;
        }
        .page-btn:hover { background: #f9f9f9; }
        .page-info { font-size: 14px; color: #333; font-weight: bold; margin: 0 10px;}
        
        /* Right: Sidebar */
        .news-sidebar {
            width: 320px;
            flex-shrink: 0;
        }
        .sb-banner {
            width: 100%;
            height: 200px;
            background: #e2e2e2;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: bold;
            color: #888;
            margin-bottom: 40px;
        }
        .sb-widget {
            margin-bottom: 40px;
        }
        .sb-title {
            font-size: 16px;
            font-weight: 800;
            color: #111;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #111;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .sb-title-more {
            font-size: 12px;
            color: #888;
            font-weight: 400;
            cursor: pointer;
        }
        
        /* Popular List */
        .pop-list { list-style: none; margin: 0; padding: 0; }
        .pop-item { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; cursor:pointer;}
        .pop-item:hover .pop-title { text-decoration: underline; color: var(--brand-blue); }
        .pop-ranking { font-size: 18px; font-weight: 900; color: #111; width: 14px; font-style: italic;}
        .pop-title { font-size: 14px; color: #333; line-height: 1.4; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        
        /* Prop List */
        .prop-item { display: flex; gap: 15px; margin-bottom: 20px; cursor: pointer; padding-bottom: 15px; border-bottom: 1px solid #f2f2f2;}
        .prop-item:hover .prop-title { text-decoration: underline; color: var(--brand-blue); }
        .prop-info { flex: 1; }
        .prop-title { font-size: 13px; font-weight: bold; color: #111; margin-bottom: 4px; line-height: 1.3;}
        .prop-price { font-size: 14px; font-weight: 900; color: #1a73e8; margin-bottom: 4px;}
        .prop-meta { font-size: 11px; color: #777; line-height: 1.4;}
        .prop-img-wrapper { width: 80px; height: 80px; flex-shrink: 0; border-radius: 6px; overflow: hidden; background: #eee;}
        .prop-img { width: 100%; height: 100%; object-fit: cover; }
        .prop-badge { font-size: 10px; color:#e74c3c; border:1px solid #e74c3c; border-radius:3px; padding:1px 4px; display:inline-block; margin-top:4px;}

    </style>
    
    <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
        .skeleton-card {
            pointer-events: none; border:none; background: transparent;
        }
        .skeleton-img {
            background: #e2e8f0; animation: pulse 1.5s infinite ease-in-out;
        }
        .skeleton-line {
            background: #e2e8f0; animation: pulse 1.5s infinite ease-in-out; border-radius:4px; margin-bottom: 8px;
        }
    </style>

    <main class="container px-20 relative">
        <div class="news-layout">
            <!-- 좌측 뉴스 리스트 (전체뉴스) -->
            <div class="news-list-area">
                <div class="list-header">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    전체뉴스
                </div>
                
                <div id="allNewsContainer">
                    <!-- Skeleton Loading UI -->
                </div>
                
                <div class="pagination">
                    <button class="page-btn" id="btnPrevPage" onclick="changePage(-1)">&lt; 이전</button>
                    <span class="page-info"><span id="currentPageDisplay">1</span> / <span id="totalPagesDisplay">-</span></span>
                    <button class="page-btn" id="btnNextPage" onclick="changePage(1)">다음 &gt;</button>
                </div>
            </div>
            
            <!-- 우측 사이드바 -->
            <div class="news-sidebar">
                <!-- 배너 영역 -->
                <div class="sb-banner">
                    배너 1
                </div>
                
                <!-- 많이 본 뉴스 5개 -->
                <div class="sb-widget">
                    <div class="sb-title">많이 본 뉴스</div>
                    <ul class="pop-list" id="popularNewsSidebarContainer">
                        <!-- 동적 렌더링 -->
                    </ul>
                </div>
                
                <!-- 추천공실 매물리스트 -->
                <div class="sb-widget">
                    <div class="sb-title">
                        추천 공실
                        <span class="sb-title-more" onclick="window.location.href='gongsil/index.html'">더보기 &gt;</span>
                    </div>
                    <div id="recommendPropSidebarContainer">
                        <!-- 동적 렌더링 -->
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Supabase 등 공통 스크립트 로드 -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="supabase_gongsi_config.js"></script>
    <script src="supabase_auth.js"></script>
    
    <script>
    const ITEMS_PER_PAGE = 10;
    let currentPage = 1;
    let totalItems = 0;
    let allNewsDataCache = []; // 캐시 보관용
    
    document.addEventListener('DOMContentLoaded', async () => {
        // 메인 GNB의 '전체뉴스' 링크 활성화 스타일 (선택사항)
        const menuLinks = document.querySelectorAll('.gnb-new a');
        menuLinks.forEach(a => {
            if(a.innerText === '전체뉴스') {
                a.style.color = '#1e56a0';
                a.style.fontWeight = '800';
            }
        });
        
        await loadAllNewsData();
        await loadPopularSidebarNews();
        await loadRecommendSidebarProps();
    });
    
    // 1. 전체뉴스 리스트 로드 (페이지네이션)
    async function loadAllNewsData() {
        const sb = window.gongsiClient || window.supabaseClient;
        if(!sb) return;
        
        // Count query
        const { count, error: countErr } = await sb.from('articles').select('*', { count: 'exact', head: true }).eq('status', 'published');
        if(!countErr) totalItems = count || 0;
        
        const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE) || 1;
        document.getElementById('totalPagesDisplay').innerText = totalPages;
        
        fetchPageData();
    }
    
    async function fetchPageData() {
        const sb = window.gongsiClient || window.supabaseClient;
        if(!sb) return;
        
        const startIdx = (currentPage - 1) * ITEMS_PER_PAGE;
        const endIdx = startIdx + ITEMS_PER_PAGE - 1;
        
        const container = document.getElementById('allNewsContainer');
        const skeletonHtml = Array(5).fill(`
            <div class="an-card skeleton-card">
                <div class="an-img skeleton-img"></div>
                <div class="an-body">
                    <div class="skeleton-line" style="width:80%; height:20px;"></div>
                    <div class="skeleton-line" style="width:100%; height:14px; margin-top:8px;"></div>
                    <div class="skeleton-line" style="width:60%; height:14px;"></div>
                    <div class="skeleton-line" style="width:30%; height:13px; margin-top:10px;"></div>
                </div>
            </div>
        `).join('');
        container.innerHTML = skeletonHtml;
        
        const { data, error } = await sb.from('articles')
            .select('*')
            .eq('status', 'published')
            .order('created_at', { ascending: false })
            .range(startIdx, endIdx);
            
        if(error || !data) {
            container.innerHTML = '<div style="padding: 20px; text-align:center;">데이터를 불러올 수 없습니다.</div>';
            return;
        }
        
        container.innerHTML = '';
        data.forEach(news => {
            const dateStr = new Date(news.created_at).toLocaleString('ko-KR', { year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit'});
            
            const card = document.createElement('div');
            card.className = 'an-card';
            const detailUrl = `news_read.html?article_id=${news.id}`; 
            card.onclick = () => window.location.href = detailUrl;
            
            const imgHtml = news.image_url ? `<img src="${news.image_url}" class="an-img" onerror="this.src='https://via.placeholder.com/160x100?text=News'">` : `<div class="an-img" style="display:flex;align-items:center;justify-content:center;color:#ccc;font-size:12px;">NO IMAGE</div>`;
            
            const categoryBadge = news.section1 ? `[${news.section1}${news.section2 ? ' > '+news.section2 : ''}]` : '';
            
            card.innerHTML = `
                ${imgHtml}
                <div class="an-body">
                    <div class="an-title">${news.title}</div>
                    <div class="an-desc">${news.subtitle || news.content?.replace(/<[^>]+>/g, '').substring(0, 150) || ''}</div>
                    <div class="an-meta"><span style="color:#1e56a0; font-weight:bold; margin-right:8px;">${categoryBadge}</span> ${dateStr} · ${news.reporter_name || '공실뉴스'}</div>
                </div>
            `;
            container.appendChild(card);
        });
        
        document.getElementById('currentPageDisplay').innerText = currentPage;
        
        // 버튼 활성화 처리
        const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE) || 1;
        document.getElementById('btnPrevPage').disabled = (currentPage <= 1);
        document.getElementById('btnNextPage').disabled = (currentPage >= totalPages);
    }
    
    // Text Banner Ticker Animation & Dropdown
    document.addEventListener("DOMContentLoaded", function() {
        const container = document.getElementById('txt-banner-container');
        const bannerList = document.getElementById('txt-banner-list');
        const dropdown = document.querySelector('.txt-dropdown');
        if (!bannerList || !container || !dropdown) return;
        
        const items = bannerList.querySelectorAll('li');
        if (items.length <= 1) return;
        
        let idx = 0;
        const itemHeight = 24; 
        
        const firstClone = items[0].cloneNode(true);
        bannerList.appendChild(firstClone);
        const totalItems = items.length + 1;
        
        let tickerInterval;
        function startTicker() {
            tickerInterval = setInterval(() => {
                idx++;
                bannerList.style.transition = 'transform 0.5s ease-in-out';
                bannerList.style.transform = `translateY(-${idx * itemHeight}px)`;
                if (idx === totalItems - 1) {
                    setTimeout(() => {
                        bannerList.style.transition = 'none';
                        bannerList.style.transform = `translateY(0)`;
                        idx = 0;
                    }, 500);
                }
            }, 3000);
        }
        startTicker();
        
        container.addEventListener('mouseenter', () => {
            clearInterval(tickerInterval);
            dropdown.style.display = 'block';
        });
        container.addEventListener('mouseleave', () => {
            startTicker();
            dropdown.style.display = 'none';
        });
    });

    // Sticky Header scroll detection
    document.addEventListener("scroll", () => {
        const header = document.querySelector('.header');
        if (header) {
            if (window.scrollY > 40) {
                header.classList.add('is-sticky');
            } else {
                header.classList.remove('is-sticky');
            }
        }
    });
    
    function changePage(delta) {
        const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE) || 1;
        let newPage = currentPage + delta;
        if(newPage < 1) newPage = 1;
        if(newPage > totalPages) newPage = totalPages;
        
        if(newPage !== currentPage) {
            currentPage = newPage;
            fetchPageData();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    // 2. 우측 사이드바: 많이 본 뉴스 (Top 5)
    async function loadPopularSidebarNews() {
        const sb = window.gongsiClient || window.supabaseClient;
        if(!sb) return;
        
        const { data, error } = await sb.from('articles')
            .select('id, title, view_count')
            .eq('status', 'published')
            .order('view_count', { ascending: false })
            .limit(5);
            
        const c = document.getElementById('popularNewsSidebarContainer');
        if(error || !data) return;
        
        c.innerHTML = data.map((item, i) => `
            <li class="pop-item" onclick="window.location.href='news_read.html?article_id=${item.id}'">
                <span class="pop-ranking">${i+1}</span>
                <span class="pop-title">${item.title}</span>
            </li>
        `).join('');
    }
    
    // 3. 우측 사이드바: 추천공실 매물리스트
    //    매물 클릭 시 공실열람으로 이동
    async function loadRecommendSidebarProps() {
        const container = document.getElementById('recommendPropSidebarContainer');
        const sb = window.gongsiClient || window.supabaseClient;
        if(!sb) return;

        const { data, error } = await sb.from('properties')
            .select('*')
            .eq('status', 'active')
            .order('created_at', { ascending: false })
            .limit(4);

        if(error || !data || data.length === 0) {
            container.innerHTML = '<div style="padding:20px; text-align:center; color:#999; font-size:13px;">추천 공실이 없습니다.</div>';
            return;
        }

        function formatPriceValue(val) {
            val = Number(val);
            if (!val || val === 0) return '0';
            if (val >= 10000) {
                const uk = Math.floor(val / 10000);
                const man = val % 10000;
                return man > 0 ? `${uk}억 ${man}` : `${uk}억`;
            }
            return val.toLocaleString();
        }

        container.innerHTML = data.map(p => {
            let propTitle = p.building_name || p.property_type || '공실매물';
            if (p.main_category === '아파트·오피스텔') {
                let aptName = p.building_name || p.property_type || '';
                let dongStr = '';
                if (p.dong_number) dongStr = String(p.dong_number).includes('동') ? p.dong_number : `${p.dong_number}동`;
                let roomStr = '';
                if (p.room_number) roomStr = String(p.room_number).includes('호') ? p.room_number : `${p.room_number}호`;
                let tempStr = `${aptName} ${dongStr} ${roomStr}`.trim();
                if (tempStr) propTitle = tempStr;
            }

            const badgeText = (function(pf) {
                if (!pf) return '공실매물';
                if (pf.includes('100') || pf.includes('양타')) return '수수료100%';
                if (pf.includes('50') || pf.includes('단타')) return '수수료50%';
                if (pf.includes('25')) return '수수료25%';
                if (pf.includes('공동')) return '공동중개';
                return '공동중개';
            })(p.brokerage_fee);

            const dep = formatPriceValue(p.deposit);
            let priceStr = '';
            if (p.trade_type === '매매' || p.trade_type === '전세') priceStr = `${p.trade_type} ${dep}`;
            else priceStr = `${p.trade_type} ${dep}/${p.monthly_rent || 0}`;

            const supAreaM2 = p.supply_area ? parseFloat(p.supply_area) : 0;
            const excAreaM2 = p.dedicated_area ? parseFloat(p.dedicated_area) : (p.area ? parseFloat(p.area) : 0);
            const fmtM2P = (m2) => m2 ? `${m2}㎡(${(m2 / 3.3058).toFixed(1)}평)` : '';
            let areaDisplay = '';
            if (supAreaM2 && excAreaM2) areaDisplay = `${fmtM2P(supAreaM2)} / ${fmtM2P(excAreaM2)}`;
            else if (supAreaM2) areaDisplay = fmtM2P(supAreaM2);
            else if (excAreaM2) areaDisplay = fmtM2P(excAreaM2);

            let locStr = '';
            if(p.address) {
                 const words = p.address.split(' ');
                 if(words.length > 2) locStr = words[2];
                 else locStr = words[0];
            } else {
                 locStr = p.location || '';
            }

            let metaArr = [];
            if(locStr) metaArr.push(locStr);
            if(areaDisplay) metaArr.push('면적 ' + areaDisplay);
            
            let extraArr = [];
            if(p.room_count) extraArr.push(`룸 ${p.room_count}개`);
            if(p.bathroom_count) extraArr.push(`욕실 ${p.bathroom_count}개`);
            
            let metaHtml = metaArr.join(' · ');
            if (extraArr.length > 0) metaHtml += '<br>' + extraArr.join(', ');

            let imgUrl = (p.images && p.images.length > 0) ? p.images[0] : 'https://via.placeholder.com/80?text=NoImg';

            return `
            <div class="prop-item" onclick="window.location.href='gongsil/index.html'">
                <div class="prop-info" style="min-width:0; overflow:hidden;">
                    <div class="prop-title" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width:180px;">${propTitle}</div>
                    <div class="prop-price">${priceStr}</div>
                    <div class="prop-meta">${metaHtml}</div>
                    <span class="prop-badge">${badgeText}</span>
                </div>
                <div class="prop-img-wrapper" style="flex-shrink:0;">
                    <img src="${imgUrl}" class="prop-img" onerror="this.src='https://via.placeholder.com/80?text=NoImg'">
                </div>
            </div>
            `;
        }).join('');
    }
    
    </script>
</body>
</html>
"""

with open("news_all.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Created news_all.html successfully.")
