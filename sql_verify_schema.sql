-- ===================================================
-- 부동산 회원 검증 시스템 스키마 업데이트
-- Supabase 대시보드 > SQL Editor에서 실행하세요
-- ===================================================

-- 1. members 테이블에 검증 관련 컬럼 추가
ALTER TABLE public.members
  ADD COLUMN IF NOT EXISTS verification_status TEXT DEFAULT 'pending',
  ADD COLUMN IF NOT EXISTS verification_checked_at TIMESTAMP WITH TIME ZONE,
  ADD COLUMN IF NOT EXISTS biz_verified BOOLEAN DEFAULT false,    -- 국세청 API 결과
  ADD COLUMN IF NOT EXISTS reg_verified BOOLEAN DEFAULT false,    -- 국토부 API 결과
  ADD COLUMN IF NOT EXISTS admin_note TEXT,                       -- 관리자 메모
  ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP WITH TIME ZONE,
  ADD COLUMN IF NOT EXISTS approved_by TEXT;                      -- 승인한 관리자 이메일

-- verification_status 값:
--   pending          : 가입 직후 기본값
--   auto_verified    : 두 API 모두 통과 → 자동 승인
--   manual_required  : API 불일치 → 관리자 검토 필요
--   approved         : 관리자 최종 승인
--   rejected         : 관리자 거절

-- 2. 기존 부동산 회원은 manual_required로 설정 (재검토 필요)
UPDATE public.members
SET verification_status = 'manual_required'
WHERE role = 'realtor' AND verification_status = 'pending';

-- 3. 관리자만 verification_status 변경 가능하도록 RLS 정책
-- (기존 정책이 있다면 먼저 확인 후 추가)

-- 검증 이력 테이블 (로그)
CREATE TABLE IF NOT EXISTS public.verification_logs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  member_id UUID REFERENCES public.members(id) ON DELETE CASCADE,
  checked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  biz_reg_no TEXT,
  broker_reg_no TEXT,
  biz_api_result JSONB,     -- 국세청 API 응답 원문
  reg_api_result JSONB,     -- 국토부 API 응답 원문
  final_status TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. 인덱스 추가 (조회 성능)
CREATE INDEX IF NOT EXISTS idx_members_verification_status 
  ON public.members(verification_status);
CREATE INDEX IF NOT EXISTS idx_members_role 
  ON public.members(role);

-- 전체 공개 읽기 (필요시 RLS 조정)
ALTER TABLE public.verification_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY IF NOT EXISTS "service_role_only" ON public.verification_logs
  FOR ALL USING (auth.role() = 'service_role');
