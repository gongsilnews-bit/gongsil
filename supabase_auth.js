
// [공실 프로젝트] 인증 스크립트 - gongsiClient가 준비된 후에 실행됨

function _gongsiAuthInit(supabase) {
    // UI 요소
    const loginBtns = document.querySelectorAll('#headerLoginBtn, .headerLoginBtn');
    const logoutBtns = document.querySelectorAll('#headerLogoutBtn, .headerLogoutBtn');
    const userProfiles = document.querySelectorAll('#userProfile, .userProfile');
    const userNameDisplays = document.querySelectorAll('#userNameDisplay, .userNameDisplay');
    const userRoleBadges = document.querySelectorAll('#userRoleBadge, .userRoleBadge');

    // 로그인 상태 변경 처리
    async function handleAuthStateChange(user) {
        if (user) {
            loginBtns.forEach(btn => btn.style.display = 'none');
            userProfiles.forEach(p => { p.style.display = 'flex'; p.style.alignItems = 'center'; });
            userNameDisplays.forEach(d => d.textContent = user.user_metadata?.full_name || user.email.split('@')[0]);
            userRoleBadges.forEach(b => b.textContent = "정보 확인중...");
            await handleUserDocument(user);
        } else {
            loginBtns.forEach(btn => btn.style.display = 'inline-block');
            userProfiles.forEach(p => p.style.display = 'none');
            window.currentUser = null;
            localStorage.removeItem('gongsil_user');
        }
    }

    // 구글 로그인 실제 실행 함수
    window.executeGoogleOAuth = async function(redirectUrl) {
        try {
            const { error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: redirectUrl,
                    queryParams: { prompt: 'select_account' }
                }
            });
            if (error) {
                console.error("로그인 에러:", error);
                alert("구글 로그인 오류: " + error.message);
            }
        } catch(err) {
            console.error("로그인 처리 에러:", err);
            alert("로그인 에러: " + err.message);
        }
    };

    // 공실뉴스 특화 로그인 안내 모달 표시
    function showGongsilLoginModal(redirectUrl) {
        let modal = document.getElementById('gongsilLoginModal');
        if (!modal) {
            // 동적 스타일 추가
            const style = document.createElement('style');
            style.innerHTML = `
                .gongsil-login-modal { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); backdrop-filter:blur(3px); display:flex; justify-content:center; align-items:center; z-index:9999999; }
                .glb-box { background:#fff; border-radius:12px; width:400px; max-width:90%; box-shadow:0 10px 40px rgba(0,0,0,0.2); position:relative; overflow:hidden; animation: glbPopup 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28); }
                @keyframes glbPopup { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }
                .glb-close { position:absolute; top:15px; right:15px; font-size:24px; color:#aaa; background:none; border:none; cursor:pointer; font-weight:300; transition:color 0.2s; padding:5px; }
                .glb-close:hover { color:#111; }
                .glb-tabs { display:flex; justify-content:center; gap:12px; padding: 0 40px; margin-top:40px; margin-bottom: 25px; }
                .glb-tab { flex:1; text-align:center; padding:12px 0; border:1px solid #ddd; border-radius:6px; cursor:pointer; color:#444; background:#fff; font-size:14px; font-weight:bold; transition:all 0.2s; }
                .glb-tab:hover { background:#f4f6fa; border-color:#ccc; color:#1e56a0; }
                .glb-body { background:#f8f9fa; margin:0 25px 25px 25px; border-radius:12px; padding:30px 25px; text-align:center; }
                .glb-circle-logo { width:65px; height:65px; background:#fff; border-radius:50%; margin:0 auto 18px; display:flex; justify-content:center; align-items:center; font-weight:900; color:#1e56a0; font-size:15px; border:1px solid #eee; box-shadow:0 4px 10px rgba(0,0,0,0.03); }
                .glb-title { font-size:18px; font-weight:800; color:#111; margin-bottom:12px; }
                .glb-desc { font-size:13.5px; color:#555; line-height:1.5; margin-bottom:20px; word-break:keep-all; }
                .glb-features { text-align:left; border-top:1px solid #e5e5e5; border-bottom:1px solid #e5e5e5; padding:20px 0; margin-bottom:20px; font-size:13px; color:#444; line-height:1.8; }
                .glb-features li { position:relative; padding-left:14px; margin-bottom:8px; }
                .glb-features li:last-child { margin-bottom:0; }
                .glb-features li::before { content:'·'; position:absolute; left:0; color:#1e56a0; font-weight:900; font-size:16px; line-height:1.2; }
                .glb-action { margin-bottom:10px; font-size:13px; color:#666; }
                .glb-btn-google { display:flex; align-items:center; justify-content:center; width:100%; border:1px solid #ddd; background:#fff; color:#222; font-size:15px; font-weight:bold; padding:14px; border-radius:8px; cursor:pointer; transition:background 0.2s; gap:10px; }
                .glb-btn-google:hover { background:#f1f1f1; }
                .glb-btn-google img { width:20px; height:20px; }
                .glb-footer { text-align:center; padding:15px; font-size:12px; color:#888; border-top:1px solid #f0f0f0; background:#fff; cursor:pointer; }
            `;
            document.head.appendChild(style);

            modal = document.createElement('div');
            modal.id = 'gongsilLoginModal';
            modal.className = 'gongsil-login-modal';
            modal.innerHTML = `
                <div class="glb-box" id="glbBox">
                    <button class="glb-close" onclick="document.getElementById('gongsilLoginModal').style.display='none'">&times;</button>
                    
                    <div class="glb-tabs">
                        <div class="glb-tab" onclick="document.getElementById('glbBtnGoogle').click();"><span style="margin-right:6px;">👤</span>회원가입</div>
                        <div class="glb-tab" onclick="document.getElementById('glbBtnGoogle').click();"><span style="margin-right:6px;">👤</span>로그인</div>
                    </div>

                    <div class="glb-body">
                        <div class="glb-circle-logo">공실뉴스</div>
                        <h3 class="glb-title">공실뉴스 회원이 되어 보세요</h3>
                        <p class="glb-desc">지금 바로 공실뉴스 회원으로 가입하시고, 독점 혜택을 누려보세요</p>
                        
                        <ul class="glb-features">
                            <li>프리미엄 부동산 뉴스와 분석 보고서 접근</li>
                            <li>동네별 실시간 공실 및 매물 동향 최신 정보</li>
                            <li>공실뉴스만의 독자적인 부동산 지수 열람</li>
                            <li>온/오프라인 세미나 우선 참가 기회</li>
                        </ul>
                        
                        <div class="glb-action">이미 회원이시면 <b>로그인</b>을 클릭해 주세요</div>
                        <button class="glb-btn-google" id="glbBtnGoogle">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" alt="Google">
                            Google 계정으로 계속하기
                        </button>
                    </div>
                    
                    <div class="glb-footer" onclick="window.location.href='#'">
                        고객센터
                    </div>
                </div>
            `;
            document.body.appendChild(modal);

            // 배경 클릭 시 닫기
            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.style.display = 'none';
            });
        }
        
        // 실행 버튼에 리다이렉트 URL 주입 이벤트 할당
        const btn = document.getElementById('glbBtnGoogle');
        // 기존 이벤트 리스너가 있다면 제거하기 위해 cloneNode 기법 사용
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
        
        newBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            window.executeGoogleOAuth(redirectUrl);
        });

        modal.style.display = 'flex';
    }

    // 로그인 클릭 핸들러
    window.handleLoginClick = async function(e) {
        if (e) e.preventDefault();
        try {
            let redirectPath = window.location.pathname;
            if (redirectPath !== '/' && !redirectPath.endsWith('.html') && !redirectPath.endsWith('/')) {
                redirectPath += '.html';
            }
            const redirectUrl = window.location.origin + redirectPath + window.location.search;
            
            // 모달 노출 (실제 구글 로그인은 모달 내 버튼에서 처리)
            showGongsilLoginModal(redirectUrl);

        } catch(err) {
            console.error("로그인 모달 표시 에러:", err);
        }
    };

    // 로그인 버튼에 이벤트 연결
    loginBtns.forEach(btn => btn.addEventListener('click', window.handleLoginClick));

    // 로그아웃 버튼에 이벤트 연결
    logoutBtns.forEach(btn => btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const { error } = await supabase.auth.signOut();
        if (!error) window.location.reload();
    }));

    // 초기 세션 확인
    supabase.auth.getSession().then(({ data: { session } }) => {
        handleAuthStateChange(session?.user ?? null);
    });

    // 세션 변경 감지
    supabase.auth.onAuthStateChange(async (event, session) => {
        handleAuthStateChange(session?.user ?? null);
    });

    // DB에서 유저 권한 조회
    async function handleUserDocument(user) {
        try {
            const ADMIN_EMAIL = 'gongsilnews@gmail.com';
            let { data: userData, error } = await supabase
                .from('members')
                .select('*')
                .eq('email', user.email)
                .maybeSingle();
            if (error) throw error;
            if (userData) {
                if (userData.id !== user.id) {
                    await supabase.from('members').update({ id: user.id }).eq('email', user.email);
                }
                if (user.email === ADMIN_EMAIL) userData.role = 'admin';
                updateRoleUI(userData, supabase);
                window.currentUser = { ...user, profile: userData };
                localStorage.setItem('gongsil_user', JSON.stringify(window.currentUser));
            } else {
                console.log("신규 가입자 감지 → 프로필 등록 페이지로 이동");
                window.location.href = (window.BASE_PATH || '') + '/register_profile.html';
            }
        } catch (err) {
            console.error("회원 정보 조회 에러:", err);
            userRoleBadges.forEach(b => { b.textContent = "조회 에러"; b.style.background = "red"; b.style.color = "white"; });
        }
    }

    function updateRoleUI(userData) {
        if (!userRoleBadges || userRoleBadges.length === 0) return;
        const existingGear = document.getElementById('adminGearBtn');
        if (existingGear) existingGear.remove();
        const targetPage = userData.role === 'admin'
            ? (window.BASE_PATH || '') + '/admin/'
            : (window.BASE_PATH || '') + '/user_admin.html';
        let roleName = "일반회원";
        if (userData.role === 'admin') roleName = "최고관리자";
        else if (userData.role === 'realtor') roleName = "부동산회원";
        const membershipName = userData.membership === 'paid' ? " (유료)" : " (무료)";
        const displayText = userData.role === 'admin' ? roleName + " >>" : roleName + membershipName + " >>";
        userRoleBadges.forEach(badge => {
            badge.textContent = displayText;
            if (userData.role === 'admin') { badge.style.background = "#e74c3c"; badge.style.color = "white"; }
            else if (userData.role === 'realtor') { badge.style.background = "#1a73e8"; badge.style.color = "white"; }
            else if (userData.membership === 'paid') { badge.style.background = "#ff9f1c"; badge.style.color = "white"; }
            else { badge.style.background = "#f0f0f0"; badge.style.color = "#555"; }
            badge.style.cssText += "; cursor:pointer; display:inline-flex; align-items:center; padding:5px 12px; border-radius:6px; font-weight:bold; font-size:12px;";
            badge.title = userData.role === 'admin' ? '관리자 페이지' : '마이페이지';
            badge.onclick = () => { window.location.href = targetPage; };
        });
    }

    console.log("Gongsil Auth initialized successfully.");
}

// config.js가 gongsiClient를 만들고 나서 이 함수를 호출
window._gongsiAuthBootstrap = function() {
    if (window.gongsiClient) {
        _gongsiAuthInit(window.gongsiClient);
    }
};

// 이미 gongsiClient가 있으면 바로 실행, 없으면 config.js 폴링 후 콜백으로 실행됨
if (window.gongsiClient) {
    _gongsiAuthInit(window.gongsiClient);
} else {
    // 폴링으로 클라이언트 대기
    let _authRetry = 0;
    const _authPoll = setInterval(() => {
        _authRetry++;
        if (window.gongsiClient) {
            clearInterval(_authPoll);
            _gongsiAuthInit(window.gongsiClient);
        } else if (_authRetry > 30) {
            clearInterval(_authPoll);
            console.error("gongsiClient 초기화 30회 실패 - 로그인 버튼 비활성화 상태");
        }
    }, 200);
}
