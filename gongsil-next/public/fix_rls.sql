-- ==========================================
-- article_media 테이블의 RLS 정책 전체 허용 설정
-- Supabase SQL Editor 에서 붙여넣고 실행하세요
-- ==========================================

-- 정책 강제 삭제 (기존 충돌 방지)
DROP POLICY IF EXISTS "Enable all actions for everyone on article_media" ON public.article_media;
DROP POLICY IF EXISTS "Enable insert for all" ON public.article_media;
DROP POLICY IF EXISTS "Enable update for all" ON public.article_media;
DROP POLICY IF EXISTS "Enable select for all" ON public.article_media;
DROP POLICY IF EXISTS "Enable delete for all" ON public.article_media;

-- 테이블 RLS 활성화
ALTER TABLE public.article_media ENABLE ROW LEVEL SECURITY;

-- 모든 사용자(해커 포함)에게 읽기/쓰기/수정/삭제 권한 부여 (개발용 임시 허용)
CREATE POLICY "Enable all actions for everyone on article_media"
ON public.article_media
FOR ALL
USING (true)
WITH CHECK (true);

-- 부가적으로 articles 테이블 보안 정책도 함께 확인 및 전면 허용
ALTER TABLE public.articles ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all actions for everyone on articles" ON public.articles;

CREATE POLICY "Enable all actions for everyone on articles"
ON public.articles
FOR ALL
USING (true)
WITH CHECK (true);

-- 혹시 tags, comments 테이블도 막힐 수 있으니 함께 열어줍니다.
ALTER TABLE IF EXISTS public.tags ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all actions for everyone on tags" ON public.tags;
CREATE POLICY "Enable all actions for everyone on tags" ON public.tags FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE IF EXISTS public.comments ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all actions for everyone on comments" ON public.comments;
CREATE POLICY "Enable all actions for everyone on comments" ON public.comments FOR ALL USING (true) WITH CHECK (true);
