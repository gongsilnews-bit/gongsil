import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// ── 환경변수 (Supabase Dashboard > Functions > Secrets 에서 설정) ──
const DATA_GO_KR_KEY = Deno.env.get("DATA_GO_KR_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";

// ── 국세청 사업자등록번호 상태조회 API ──
async function checkBizRegistration(bizRegNo: string): Promise<{valid: boolean; result: unknown}> {
  const cleanNo = bizRegNo.replace(/-/g, "");
  const url = `https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey=${DATA_GO_KR_KEY}`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ b_no: [cleanNo] }),
    });
    const data = await res.json();
    const item = data?.data?.[0];
    // b_stt_cd: "01" = 계속사업자(유효), "02" = 휴업, "03" = 폐업
    const valid = item?.b_stt_cd === "01";
    return { valid, result: item };
  } catch (e) {
    console.error("국세청 API 오류:", e);
    return { valid: false, result: { error: String(e) } };
  }
}

// ── 국토교통부 중개업소 조회 API ──
async function checkBrokerRegistration(brokerRegNo: string, companyName: string): Promise<{valid: boolean; result: unknown}> {
  if (!brokerRegNo) return { valid: false, result: { error: "번호 미입력" } };
  const url = `https://api.odcloud.kr/api/15056101/v1/uddi:3fc05f3a-3e0a-4d00-8791-f0a84e9c3bb9_201910231656?serviceKey=${DATA_GO_KR_KEY}&page=1&perPage=1&returnType=json&cond%5B중개업등록번호%3A%3AEQ%5D=${encodeURIComponent(brokerRegNo)}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    const items = data?.data ?? [];
    const found = items.length > 0;
    // 상호명도 일치하는지 추가 검증
    const nameMatch = found
      ? items[0]["상호"]?.includes(companyName) || companyName?.includes(items[0]["상호"])
      : false;
    return { valid: found, result: { items, nameMatch } };
  } catch (e) {
    console.error("국토부 API 오류:", e);
    return { valid: false, result: { error: String(e) } };
  }
}

serve(async (req) => {
  // CORS 허용
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
      },
    });
  }

  try {
    const { memberId, bizRegNo, brokerRegNo, companyName } = await req.json();

    if (!memberId) {
      return new Response(JSON.stringify({ error: "memberId 필수" }), { status: 400 });
    }

    const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    // ── 두 API 동시에 호출 ──
    const [bizResult, brokerResult] = await Promise.all([
      bizRegNo ? checkBizRegistration(bizRegNo) : Promise.resolve({ valid: false, result: { error: "미입력" } }),
      brokerRegNo ? checkBrokerRegistration(brokerRegNo, companyName) : Promise.resolve({ valid: false, result: { error: "미입력" } }),
    ]);

    // ── 최종 상태 결정 ──
    const bothValid = bizResult.valid && brokerResult.valid;
    const finalStatus = bothValid ? "auto_verified" : "manual_required";

    // ── DB 업데이트 ──
    const { error: updateErr } = await supabase
      .from("members")
      .update({
        verification_status: finalStatus,
        biz_verified: bizResult.valid,
        reg_verified: brokerResult.valid,
        verification_checked_at: new Date().toISOString(),
      })
      .eq("id", memberId);

    // ── 검증 로그 저장 ──
    await supabase.from("verification_logs").insert({
      member_id: memberId,
      biz_reg_no: bizRegNo,
      broker_reg_no: brokerRegNo,
      biz_api_result: bizResult.result,
      reg_api_result: brokerResult.result,
      final_status: finalStatus,
    });

    if (updateErr) throw updateErr;

    return new Response(
      JSON.stringify({
        status: finalStatus,
        biz_verified: bizResult.valid,
        reg_verified: brokerResult.valid,
        message: bothValid
          ? "✅ 자동 검증 완료! 공실 매물 등록이 가능합니다."
          : "⏳ 일부 항목 확인 필요 — 관리자가 1~3 영업일 내 검토 후 안내드립니다.",
      }),
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: String(err) }), {
      status: 500,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    });
  }
});
