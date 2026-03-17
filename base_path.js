/**
 * base_path.js
 * 로컬(localhost)과 GitHub Pages 양쪽에서 경로가 올바르게 동작하도록
 * BASE_PATH를 자동으로 감지합니다.
 *
 * 로컬:         BASE_PATH = ""
 * GitHub Pages: BASE_PATH = "/gongsil-news-map"
 */

(function() {
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        // 로컬 개발 환경
        window.BASE_PATH = '';
    } else {
        // GitHub Pages 환경
        // pathname의 첫 번째 세그먼트를 레포명으로 사용
        // 예: /gongsil-news-map/index.html -> /gongsil-news-map
        const pathParts = window.location.pathname.split('/').filter(Boolean);
        window.BASE_PATH = pathParts.length > 0 ? '/' + pathParts[0] : '';
    }

    console.log('[BASE_PATH 감지]', window.BASE_PATH || '(로컬 루트)');
})();
