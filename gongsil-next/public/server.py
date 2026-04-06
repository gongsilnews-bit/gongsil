#!/usr/bin/env python3
"""
공실뉴스 지도 - 로컬 개발 서버
- 포트 8000에서 파일 서빙
- .html 확장자 없이도 접근 가능 (예: /gongsil -> gongsil.html)
- 잘못된 301 리다이렉트 방지
"""

import http.server
import os
import sys

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 경로 파싱
        path = self.path.split('?')[0]  # 쿼리스트링 제거
        
        # 실제 파일 경로 확인
        local_path = path.lstrip('/')
        
        # 1) 경로가 비어있으면 index.html 서빙
        if local_path == '' or local_path == '/':
            self.path = '/index.html'
            return super().do_GET()
        
        # 2) 파일이 그대로 존재하면 그냥 서빙
        if os.path.isfile(local_path):
            return super().do_GET()
        
        # 3) 슬래시로 끝나는 경우 (예: /gongsil/) → gongsil.html 로 처리
        if local_path.endswith('/'):
            base = local_path.rstrip('/')
            if os.path.isfile(base + '.html'):
                self.path = '/' + base + '.html'
                return super().do_GET()
        
        # 4) 확장자 없는 경우 (예: /gongsil) → gongsil.html 로 처리
        if not os.path.splitext(local_path)[1]:
            if os.path.isfile(local_path + '.html'):
                self.path = '/' + local_path + '.html'
                return super().do_GET()
        
        # 5) 기타 - 기본 처리
        return super().do_GET()

    def log_message(self, format, *args):
        # 로그 출력 포맷 정리
        print(f"[{self.address_string()}] {format % args}")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with http.server.HTTPServer(('', PORT), CustomHandler) as httpd:
        print("=" * 55)
        print("  공실뉴스 지도 로컬 서버 시작!")
        print("=" * 55)
        print(f"  브라우저에서 접속: http://localhost:{PORT}")
        print(f"  공실열람:          http://localhost:{PORT}/gongsil.html")
        print(f"  어드민:            http://localhost:{PORT}/admin")
        print()
        print("  서버를 종료하려면 Ctrl+C 를 누르세요.")
        print("=" * 55)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
            sys.exit(0)
