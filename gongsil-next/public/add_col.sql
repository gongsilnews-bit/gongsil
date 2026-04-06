-- articles 테이블에 위도/경도, 관련기사 컬럼 추가
ALTER TABLE public.articles ADD COLUMN IF NOT EXISTS lat NUMERIC;
ALTER TABLE public.articles ADD COLUMN IF NOT EXISTS lng NUMERIC;
ALTER TABLE public.articles ADD COLUMN IF NOT EXISTS related_articles JSONB DEFAULT '[]'::jsonb;
