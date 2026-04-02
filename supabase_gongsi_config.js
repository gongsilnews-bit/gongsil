
// [공실 프로젝트] 회원 로그인 및 물건 등록 전용 Supabase 설정
const GONGSI_CONFIG = {
    URL: 'https://kjrjrjnsiynrcelzepju.supabase.co',
    KEY: 'sb_publishable_pwzXQ_2LgDo-mhjBIKcXmw_KS8es5Cj'
};

function _createGongsiClient() {
    if (window.supabase && !window.gongsiClient) {
        window.gongsiClient = window.supabase.createClient(GONGSI_CONFIG.URL, GONGSI_CONFIG.KEY);
        console.log("Gongsi Supabase Client Initialized");
        // supabase_auth.js가 이미 로드됐지만 클라이언트가 없어서 초기화 못 했을 경우 재시도
        if (typeof window._gongsiAuthBootstrap === 'function') {
            window._gongsiAuthBootstrap();
        }
    }
}

// SDK가 이미 있으면 바로 생성, 없으면 로드 완료 후 생성
if (window.supabase) {
    _createGongsiClient();
} else {
    // CDN script가 아직 로드 중일 수 있음 → DOMContentLoaded 후 재시도
    document.addEventListener('DOMContentLoaded', _createGongsiClient);
    // 혹은 짧은 폴링으로 체크
    let _retry = 0;
    const _poll = setInterval(() => {
        _retry++;
        if (window.supabase) {
            clearInterval(_poll);
            _createGongsiClient();
        } else if (_retry > 20) {
            clearInterval(_poll);
            console.error("Supabase SDK 로드 실패 (CDN 연결 오류)");
        }
    }, 200);
}
