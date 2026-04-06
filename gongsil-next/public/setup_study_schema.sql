-- 공실스터디 데이터베이스 최신 스키마 (초안)

-- 1. 스터디(강의) 기본 정보 테이블
CREATE TABLE IF NOT EXISTS public.study_courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instructor_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL, -- 등록자/강사
    title VARCHAR(255) NOT NULL,      -- 강의명
    description TEXT,                 -- 상세 설명
    thumbnail_urls JSONB,             -- [배열] 대표사진 등 여러 장의 이미지 (최대 5장)
    price INTEGER DEFAULT 0,          -- 수강료 (포인트)
    status VARCHAR(50) DEFAULT 'draft', -- 상태 (draft: 임시저장, pending: 승인대기, published: 판매중)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);
ALTER TABLE public.study_courses ENABLE ROW LEVEL SECURITY;

-- 2. 스터디 커리큘럼(목차) 테이블
CREATE TABLE IF NOT EXISTS public.study_lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES public.study_courses(id) ON DELETE CASCADE,
    section_title VARCHAR(255) NOT NULL, -- 단원명 (예: 1. 오리엔테이션)
    lesson_title VARCHAR(255) NOT NULL,  -- 세부 강의명
    video_url TEXT,                      -- VOD 링크 (비메오 등)
    description TEXT,                    -- 챕터별 핵심 학습 내용 (선택란)
    order_index INTEGER NOT NULL DEFAULT 0, -- 목차 노출 순서
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);
ALTER TABLE public.study_lessons ENABLE ROW LEVEL SECURITY;

-- 3. 통합 수업 자료 첨부 테이블 (파일 & 링크 동시지원)
CREATE TABLE IF NOT EXISTS public.study_materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES public.study_courses(id) ON DELETE CASCADE,
    material_type VARCHAR(20) DEFAULT 'file', -- 'file'(PC첨부) 또는 'link'(구글드라이브) 구별
    title VARCHAR(255) NOT NULL,              -- 자료명
    file_url TEXT NOT NULL,                   -- 파일 스토리지 경로 또는 구글드라이브 URL 링크
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);
ALTER TABLE public.study_materials ENABLE ROW LEVEL SECURITY;

-- 4. 관리자 전용 서비스 로그 (메모) 테이블
CREATE TABLE IF NOT EXISTS public.study_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES public.study_courses(id) ON DELETE CASCADE,
    author_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    message TEXT NOT NULL,                    -- 메모 내용 또는 변경 로그 내용
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);
ALTER TABLE public.study_logs ENABLE ROW LEVEL SECURITY;

-- 5. 수강생 및 구매 내역 테이블
CREATE TABLE IF NOT EXISTS public.study_enrollments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES public.study_courses(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'active', -- 상태 (active: 수강중)
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE, -- 만료일 (기간제 수강 시)
    UNIQUE(course_id, student_id)        -- 한 유저가 같은 강의 중복 구매 방지
);
ALTER TABLE public.study_enrollments ENABLE ROW LEVEL SECURITY;

-- RLS Development Defaults
DROP POLICY IF EXISTS "Enable read access for all" ON public.study_courses;
CREATE POLICY "Enable read access for all" ON public.study_courses FOR SELECT USING (true);
DROP POLICY IF EXISTS "Enable insert for all" ON public.study_courses;
CREATE POLICY "Enable insert for all" ON public.study_courses FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Enable update for all" ON public.study_courses;
CREATE POLICY "Enable update for all" ON public.study_courses FOR UPDATE USING (true);
DROP POLICY IF EXISTS "Enable delete for all" ON public.study_courses;
CREATE POLICY "Enable delete for all" ON public.study_courses FOR DELETE USING (true);

DROP POLICY IF EXISTS "Enable read access for all" ON public.study_lessons;
CREATE POLICY "Enable read access for all" ON public.study_lessons FOR SELECT USING (true);
DROP POLICY IF EXISTS "Enable insert access for all" ON public.study_lessons;
CREATE POLICY "Enable insert access for all" ON public.study_lessons FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Enable delete access for all" ON public.study_lessons;
CREATE POLICY "Enable delete access for all" ON public.study_lessons FOR DELETE USING (true);

DROP POLICY IF EXISTS "Enable read access for all" ON public.study_materials;
CREATE POLICY "Enable read access for all" ON public.study_materials FOR SELECT USING (true);
DROP POLICY IF EXISTS "Enable insert access for all" ON public.study_materials;
CREATE POLICY "Enable insert access for all" ON public.study_materials FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Enable delete access for all" ON public.study_materials;
CREATE POLICY "Enable delete access for all" ON public.study_materials FOR DELETE USING (true);

DROP POLICY IF EXISTS "Enable read access for all" ON public.study_logs;
CREATE POLICY "Enable read access for all" ON public.study_logs FOR SELECT USING (true);
DROP POLICY IF EXISTS "Enable insert access for all" ON public.study_logs;
CREATE POLICY "Enable insert access for all" ON public.study_logs FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Enable read access for all" ON public.study_enrollments;
CREATE POLICY "Enable read access for all" ON public.study_enrollments FOR SELECT USING (true);
DROP POLICY IF EXISTS "Enable insert access for all" ON public.study_enrollments;
CREATE POLICY "Enable insert access for all" ON public.study_enrollments FOR INSERT WITH CHECK (true);
