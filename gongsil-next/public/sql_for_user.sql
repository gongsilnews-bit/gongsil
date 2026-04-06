-- 전국데이터지수 누적 기록을 위한 히스토리 테이블
CREATE TABLE public.indices_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    record_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    index_type VARCHAR(50) NOT NULL, -- 매매, 전세, 코스피 등
    index_value NUMERIC NOT NULL,
    change_rate VARCHAR(20),
    status_icon VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 누구나 읽고 쓸 수 있도록 RLS 권한 부여
ALTER TABLE public.indices_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all API actions for history" ON public.indices_history FOR ALL USING (true) WITH CHECK (true);
