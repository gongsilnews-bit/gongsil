@echo off
chcp 65001 >nul
echo.
echo ========================================================
echo Supabase 로그인을 시작합니다...
echo 브라우저 창이 열리면 [Authorize] (승인) 버튼을 눌러주세요!
echo ========================================================
call npx supabase login

echo.
echo ========================================================
echo 기존 프로젝트와 연결합니다. (비밀번호를 물어보면 엔터를 치거나 데이터베이스 비밀번호를 입력해주세요)
echo ========================================================
call npx supabase link --project-ref kjrjrjnsiynrcelzepju

echo.
echo ========================================================
echo 프로젝트 API 키(Secret)를 서버에 등록합니다...
echo ========================================================
call npx supabase secrets set DATA_GO_KR_KEY="0c70894217e28613a63cea5f413098c837a45e1d3fdba3fa94b9dc273cf12e7d"

echo.
echo ========================================================
echo 부동산 검증 함수(Edge Function)를 서버에 배포합니다...
echo ========================================================
call npx supabase functions deploy verify-realtor

echo.
echo 모든 작업이 완료되었습니다!
pause
