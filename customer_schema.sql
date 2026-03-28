-- 손님(고객) 관리 테이블 생성
CREATE TABLE IF NOT EXISTS public.customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    realtor_id UUID NOT NULL, -- auth.users(id)에 해당 (중개사 본인만 볼 수 있도록)
    customer_type TEXT DEFAULT '일반문의', -- 매도인, 매수인, 임대인, 임차인, 일반문의
    name TEXT NOT NULL,
    phone_number TEXT,
    status TEXT DEFAULT '신규', -- 신규, 진행중, 계약완료, 보류
    budget TEXT, -- 예산 (예: 보증금 5천 / 월 50)
    target_items TEXT, -- 희망 매물/지역 (예: 마포구, 투룸, 주차가능)
    move_in_date TEXT, -- 이사 희망일 또는 잔금일
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 고객 상담 내역 및 메모 (타임라인) 테이블 생성
CREATE TABLE IF NOT EXISTS public.customer_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES public.customers(id) ON DELETE CASCADE,
    realtor_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 고객 테이블 요약 메모 업데이트를 위한 함수/트리거(선택) 또는 JS에서 직접 처리 가능

-- 보안(RLS) 정책 설정 (자신의 고객만 볼 수 있도록 강제)
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for own customers" ON public.customers FOR SELECT USING (auth.uid() = realtor_id);
CREATE POLICY "Enable insert access for own customers" ON public.customers FOR INSERT WITH CHECK (auth.uid() = realtor_id);
CREATE POLICY "Enable update access for own customers" ON public.customers FOR UPDATE USING (auth.uid() = realtor_id);
CREATE POLICY "Enable delete access for own customers" ON public.customers FOR DELETE USING (auth.uid() = realtor_id);

ALTER TABLE public.customer_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for own logs" ON public.customer_logs FOR SELECT USING (auth.uid() = realtor_id);
CREATE POLICY "Enable insert access for own logs" ON public.customer_logs FOR INSERT WITH CHECK (auth.uid() = realtor_id);
CREATE POLICY "Enable update access for own logs" ON public.customer_logs FOR UPDATE USING (auth.uid() = realtor_id);
CREATE POLICY "Enable delete access for own logs" ON public.customer_logs FOR DELETE USING (auth.uid() = realtor_id);
