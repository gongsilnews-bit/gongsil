-- 1. 관리자 메모 컬럼 추가
ALTER TABLE public.members
  ADD COLUMN IF NOT EXISTS admin_note text;

-- 2. 사업자등록증 / 중개등록증 이미지 URL 컬럼 추가 (혹시 없는 경우 대비)
ALTER TABLE public.members
  ADD COLUMN IF NOT EXISTS license_image text,
  ADD COLUMN IF NOT EXISTS license_image_brokerage text;

-- 3. 스키마 캐시 새로고침
NOTIFY pgrst, 'reload schema';
