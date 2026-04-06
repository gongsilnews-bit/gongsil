-- Supabase의 SQL Editor 에 아래 구문을 통째로 복사해서 Run 버튼을 눌러주세요.

-- [1] 회원(members) 테이블에 부동산 가입/검토 시 필요한 모든 컬럼을 한꺼번에 추가합니다.
-- 이미 존재하는 컬럼은 건너뜁니다 (IF NOT EXISTS 작동)

ALTER TABLE public.members
  ADD COLUMN IF NOT EXISTS verification_status text DEFAULT 'pending',
  ADD COLUMN IF NOT EXISTS admin_note text,
  ADD COLUMN IF NOT EXISTS company_name text,
  ADD COLUMN IF NOT EXISTS ceo_name text,
  ADD COLUMN IF NOT EXISTS company_reg_no text,
  ADD COLUMN IF NOT EXISTS biz_reg_no text,
  ADD COLUMN IF NOT EXISTS tel_num text,
  ADD COLUMN IF NOT EXISTS cell_num text,
  ADD COLUMN IF NOT EXISTS zipcode text,
  ADD COLUMN IF NOT EXISTS address text,
  ADD COLUMN IF NOT EXISTS address_detail text,
  ADD COLUMN IF NOT EXISTS company_intro text,
  ADD COLUMN IF NOT EXISTS license_image text,
  ADD COLUMN IF NOT EXISTS license_image_brokerage text;

-- [2] Supabase 스키마 캐시 새로고침 (중요)
NOTIFY pgrst, 'reload schema';
