import uuid
import random

titles = [
    "[2026 기초] 아파트 매매 권리분석 마스터",
    "초보자를 위한 상가 중개 실무 기초",
    "계약서 특약사항 작성 완벽 가이드",
    "공인중개사 창업 전 필수 체크리스트 10",
    "다가구/다세대 수익률 분석 마스터",
    "토지 중개 실전 투자 가이드",
    "꼬마빌딩 건물로 월천만원 만들기",
    "공실률 제로! 상가 임대 마케팅 전략",
    "네이버 부동산 매물 상위 노출 꿀팁",
    "유튜브로 시작하는 부동산 브랜딩",
    "재건축/재개발 투자 분석 기초",
    "주택 임대차 보호법 권리분석 심화",
    "법원 명도 소송 및 실전 권리분석",
    "부동산 세금(취득세, 양도세) 완벽 정리",
    "공장/창고 중개 실무와 특약",
    "신도심 분양권 투자와 전매 제한",
    "빌딩 매매 협상 스킬과 계약 실무",
    "외국인 대상 부동산 중개 영어 회화",
    "중개사무소 직원 관리와 세무 기장",
    "[2026 개정] 상가 임대차 보호법 완전 정복"
]

prices = [0, 10000, 30000, 50000, 100000, 150000, 200000]
statuses = ['published', 'published', 'published', 'draft', 'published']

sql_statements = []

for title in titles:
    cid = str(uuid.uuid4())
    price = random.choice(prices)
    status = random.choice(statuses)
    days_ago = random.randint(0, 60)
    
    # Insert main course
    sql_statements.append(
        f"INSERT INTO public.study_courses (id, title, description, price, status, created_at) "
        f"VALUES ('{cid}', '{title}', '이 스터디는 전문가가 진행하는 핵심 실무 과정입니다. 현장 경험을 꾹꾹 담았습니다.', "
        f"{price}, '{status}', now() - interval '{days_ago} days');"
    )
    
    # Insert 3 lessons per course
    for i in range(1, 4):
        lid = str(uuid.uuid4())
        lesson_title = f"{i}강. 실전 핵심 요약 및 꿀팁 ({title})"
        
        # Mix mostly YouTube, some Vimeo
        video_url = "https://youtu.be/dQw4w9WgXcQ" if random.random() > 0.3 else "https://vimeo.com/76979871"
        
        sql_statements.append(
            f"INSERT INTO public.study_lessons (id, course_id, section_title, lesson_title, video_url, order_index) "
            f"VALUES ('{lid}', '{cid}', '제1장. 기초 이론', '{i}강. 오리엔테이션 및 요약', '{video_url}', {i});"
        )
        
    # Use real UUID for material
    if random.random() > 0.5:
        mid = str(uuid.uuid4())
        sql_statements.append(
            f"INSERT INTO public.study_materials (id, course_id, material_type, title, file_url) "
            f"VALUES ('{mid}', '{cid}', 'link', '공통 수업 자료 (해설강의 및 판례모음)', 'https://drive.google.com/');"
        )

with open('seed_courses.sql', 'w', encoding='utf-8') as f:
    f.write("-- 공실스터디 데이터 20건 자동 삽입 스크립트\n")
    f.write("\n".join(sql_statements))

print("seed_courses.sql 생성 완료")
