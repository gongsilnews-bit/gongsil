
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

    // 로그인 클릭 핸들러
    window.handleLoginClick = async function(e) {
        if (e) e.preventDefault();
        try {
            let redirectPath = window.location.pathname;
            if (redirectPath !== '/' && !redirectPath.endsWith('.html') && !redirectPath.endsWith('/')) {
                redirectPath += '.html';
            }
            const redirectUrl = window.location.origin + redirectPath + window.location.search;
            const { error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: { redirectTo: redirectUrl }
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
