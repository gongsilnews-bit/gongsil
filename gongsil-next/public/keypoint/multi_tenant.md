# 멀티테넌트 부동산 사이트 기획

> 작성일: 2026-04-03  
> 목적: 하나의 DB로 여러 부동산 홈페이지 운영 방안

---

## 📌 핵심 전략

> **DB 1개 + 코드 1개 + config.js만 부동산마다 다르게**

---

## 📌 DB 구조 (Supabase 1개로 통합)

### properties 테이블에 `agency_id` 컬럼 추가 (필수)

```sql
ALTER TABLE properties ADD COLUMN agency_id varchar;
```

### 표준 필드 (모든 부동산 동일하게 맞춤)

| 필드명 | 설명 |
|--------|------|
| `agency_id` | 부동산 구분자 (예: agency_001) |
| `main_category` | 대분류 (아파트/오피스텔/상가 등) |
| `property_type` | 소분류 |
| `trade_type` | 거래구분 (매매/전세/월세) |
| `deposit` | 보증금 |
| `monthly_rent` | 월세 |
| `maintenance_fee` | 관리비 |
| `supply_area` | 공급면적 |
| `dedicated_area` | 전용면적 |
| `sido` | 시/도 |
| `sigungu` | 시/군/구 |
| `dong` | 법정동 |
| `detail_address` | 상세주소 |
| `lat` | 위도 (geocoding 자동 저장) |
| `lng` | 경도 (geocoding 자동 저장) |
| `status` | 매물 상태 (active/pending) |
| `images` | 사진 배열 |

> ⚠️ 필드를 중간에 바꾸면 모든 사이트 코드 수정 필요 → **초기에 표준 확정 필수**

---

## 📌 부동산 정보 테이블 (agencies)

```sql
CREATE TABLE agencies (
    id          varchar PRIMARY KEY,   -- agency_001
    name        varchar,               -- 강남공인중개사
    phone       varchar,
    address     varchar,
    logo_url    varchar,
    theme_color varchar,               -- 사이트 테마 색상
    domain      varchar                -- gangnam.com
);
```

---

## 📌 코드 구조

```
📁 GitHub 저장소 (1개)
├── gongsil/
│   └── index.html       ← 공통 템플릿 (1개로 전체 관리)
├── style.css            ← 공통 스타일
├── agencies/
│   ├── gangnam/
│   │   └── config.js   ← 강남공인 설정만
│   ├── mapo/
│   │   └── config.js   ← 마포부동산 설정만
│   └── daejeon/
│       └── config.js   ← 대전한빛 설정만
└── keypoint/            ← 이 문서들
```

### config.js 예시 (부동산마다 이것만 다름)

```javascript
const AGENCY_CONFIG = {
    agency_id:     'agency_001',
    name:          '강남공인중개사',
    phone:         '02-1234-5678',
    theme_color:   '#e53935',
    logo:          'gangnam_logo.png',
    kakao_api_key: 'xxxxxx강남전용키xxxxxx'  // ← 부동산마다 다른 키
};
```

---

## 📌 카카오 API 키 전략

### 핵심 개념
카카오 API 키는 **앱(App) 단위**로 일일 쿼터가 부여됨.

```
API 키 1개 → 일 쿼터 N만건/일
API 키 10개 → 일 쿼터 N만건 × 10 = 10배
```

### 권장 방식: 부동산마다 API 키 따로 발급

| 방식 | 쿼터 | 관리 | 추천 |
|------|------|------|------|
| API 키 1개 공유 | N만건/일 | 쉬움 | 소규모 |
| **부동산마다 따로** | **N만건 × 부동산 수** | config.js만 | **✅ 권장** |

### 발급 절차 (부동산별)
1. [카카오 개발자 콘솔](https://developers.kakao.com) → 새 앱 생성
2. 앱 이름: `강남공인중개사` 등 부동산명
3. Web 플랫폼 추가 → 도메인 등록 (gangnam.com 또는 github 경로)
4. 발급된 키를 `config.js`의 `kakao_api_key`에 입력

### 도메인 포워딩 시 주의사항
- **단순 리디렉션** (gangnam.com → github URL로 이동): github 도메인 등록으로 OK
- **도메인 마스킹/커스텀 도메인** (URL이 gangnam.com 유지): gangnam.com을 허용 도메인에 등록 필요

### 우리 시스템에서 실제 쿼터 소비량
좌표를 DB에 저장해두었기 때문에 Geocoding 사용은 거의 0.  
**지도 SDK 표시 = 사용자 방문 수**가 주요 소비량.  
부동산마다 방문자가 다르므로 **각자 키를 쓰는 것이 안전**.

---

## 📌 각 부동산 매물 조회 방식

```javascript
// 각 사이트에서 자기 부동산 매물만 조회
const { data } = await supabase
    .from('properties')
    .select('*')
    .eq('agency_id', AGENCY_CONFIG.agency_id)
    .eq('status', 'active');
```

```javascript
// 공실뉴스 메인에서는 전체 조회
const { data } = await supabase
    .from('properties')
    .select('*')
    .eq('status', 'active');
```

---

## 📌 배포 URL 구조

```
gongsilnews-bit.github.io/          ← 공실뉴스 통합 메인
gongsilnews-bit.github.io/gangnam/  ← 강남공인중개사
gongsilnews-bit.github.io/mapo/     ← 마포부동산
gongsilnews-bit.github.io/daejeon/ ← 대전한빛공인
```

---

## 📌 비용 예상

| 항목 | 개별 DB | **공통 DB (추천)** |
|------|---------|-----------------|
| Supabase | 부동산 수 × $25/월 | **$25/월 고정** |
| 코드 유지보수 | 각각 따로 | **한 번에 전체** |
| 통합 검색 | 불가 | **가능** |
| 신규 부동산 추가 | 신규 DB 세팅 필요 | **config.js 1개만 추가** |

---

## 📌 신규 부동산 추가 절차

1. `agencies` 테이블에 부동산 정보 INSERT
2. `config.js` 파일 생성 (agency_id, 이름, 색상)
3. GitHub에 폴더 추가 및 배포
4. 완료 → 새 부동산 사이트 즉시 오픈

**→ 신규 사이트 추가에 걸리는 시간: 30분 이내**
