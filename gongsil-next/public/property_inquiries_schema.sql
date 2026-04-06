-- ============================================================
-- 공실뉴스 부동산 - 비공개 매물 문의 (property_inquiries) 테이블 스키마
-- ============================================================

DROP TABLE IF EXISTS public.property_inquiries CASCADE;

CREATE TABLE public.property_inquiries (
    id              uuid            DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at      timestamptz     NOT NULL DEFAULT now(),
    
    -- 어떤 매물에 대한 문의인지
    property_id     uuid            NOT NULL REFERENCES public.properties(id) ON DELETE CASCADE,
    
    -- 누가 문의를 남겼는지 (문의자)
    author_id       uuid            NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- 매물을 등록한 중개사(또는 일반유저)의 ID (조회 편의성)
    realtor_id      uuid            NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- 문의 내용
    content         text            NOT NULL,

    -- 중개사의 답변 내용 (비어있으면 '답변 대기중')
    answer          text,
    answered_at     timestamptz
);

-- 인덱스 생성 (조회 성능 향상)
CREATE INDEX idx_property_inquiries_property_id ON public.property_inquiries(property_id);
CREATE INDEX idx_property_inquiries_author_id   ON public.property_inquiries(author_id);
CREATE INDEX idx_property_inquiries_realtor_id  ON public.property_inquiries(realtor_id);

-- ============================================================
-- RLS (Row Level Security) 정책 (비공개 처리의 핵심)
-- ============================================================
ALTER TABLE public.property_inquiries ENABLE ROW LEVEL SECURITY;

-- 1. 조회 (SELECT): 본인이 작성한 문의이거나, 해당 매물(문의)의 대상 중개사인 경우만 가능
CREATE POLICY "inquiries_select_policy"
    ON public.property_inquiries FOR SELECT
    USING (
        auth.uid() = author_id 
        OR auth.uid() = realtor_id
    );

-- 2. 작성 (INSERT): 로그인한 유저 누구나 가능 (단, author_id는 본인이어야 함)
CREATE POLICY "inquiries_insert_policy"
    ON public.property_inquiries FOR INSERT
    WITH CHECK (auth.uid() = author_id);

-- 3. 수정 (UPDATE): 
--    문의자는 내용을 수정할 수 있고,
--    중개사는 'answer'와 'answered_at' 필드만 업데이트하여 답변을 남길 수 있어야 함.
CREATE POLICY "inquiries_update_policy"
    ON public.property_inquiries FOR UPDATE
    USING (
        auth.uid() = author_id 
        OR auth.uid() = realtor_id
    );

-- 4. 삭제 (DELETE): 본인이 작성한 문의만 삭제 가능 (또는 중개사도 삭제 가능하게 하려면 OR 추가)
CREATE POLICY "inquiries_delete_policy"
    ON public.property_inquiries FOR DELETE
    USING (auth.uid() = author_id);
