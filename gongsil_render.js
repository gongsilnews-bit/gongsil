/* gongsil_render.js */
const supabase = window.gongsiClient;
let mapInstance = null; 

document.addEventListener('DOMContentLoaded', async () => {
    // 1. 지도 초기화 대기 (kakao.maps.load는 이미 html에서 처리 중일 수 있으나 명시적으로 한 번 더 관리)
    if (typeof kakao !== 'undefined') {
        kakao.maps.load(() => {
            initMap();
            loadActiveProperties(); 
        });
    }
});

function initMap() {
    const container = document.getElementById('map');
    if (!container) return;
    const options = {
        center: new kakao.maps.LatLng(37.5665, 126.9780), 
        level: 8
    };
    mapInstance = new kakao.maps.Map(container, options);
    window.mapInstance = mapInstance; 
    console.log('gongsil_render: 지도 초기화 완료');
}

let allActiveProperties = [];

async function loadActiveProperties() {
    const listArea = document.getElementById('propertyListArea');
    const countHeader = document.querySelector('#listCountHeader span');
    
    if (listArea) listArea.innerHTML = '<div style="padding:20px; text-align:center; color:#999;">매물을 불러오는 중... 🔄</div>';

    const { data, error } = await supabase
        .from('properties')
        .select('*')
        .eq('status', 'active')
        .order('created_at', { ascending: false });

    if (error) {
        console.error("매물 로드 에러:", error);
        if (listArea) listArea.innerHTML = '<div style="padding:20px; text-align:center; color:red;">데이터를 불러오지 못했습니다.</div>';
        return;
    }

    allActiveProperties = data || [];
    
    if (countHeader) countHeader.textContent = `지역 목록 ${allActiveProperties.length}개`;

    renderPropertyCards(allActiveProperties);
    addMarkersToMap(allActiveProperties);
}

function renderPropertyCards(props) {
    const listArea = document.getElementById('propertyListArea');
    if (!listArea) return;
    listArea.innerHTML = '';

    if (props.length === 0) {
        listArea.innerHTML = '<div style="padding:50px 20px; text-align:center; color:#999;">등록된 공실매물이 없습니다.</div>';
        return;
    }

    props.forEach(p => {
        const card = document.createElement('div');
        card.className = 'property-card';
        card.onclick = () => showPropertyDetail(p);
        
        const priceStr = formatPriceDisplay(p);
        const imgUrl = (p.images && p.images.length > 0) ? p.images[0] : 'https://via.placeholder.com/150/EEEEEE/999999?text=No+Image';

        card.innerHTML = `
            <div class="property-info">
                <span class="recommend-tag">추천</span>
                <h3 class="price-title">${priceStr}</h3>
                <div class="maintenance-fee">관리비 ${p.maintenance_fee || 0}만원</div>
                <div class="property-desc">${p.property_type} · ${p.area || '-'}㎡ · 층 정보없음</div>
                <div class="property-loc">${p.sido || ''} ${p.sigungu || ''} ${p.dong || ''}</div>
                <div class="property-detail">${p.description || p.building_name || ''}</div>
            </div>
            <div class="property-image">
                <img src="${imgUrl}" alt="매물사진">
            </div>
        `;
        listArea.appendChild(card);
    });
}

function formatPriceDisplay(p) {
    const dep = formatPriceValue(p.deposit);
    if (p.trade_type === '매매' || p.trade_type === '전세') return `${p.trade_type} ${dep}`;
    return `${p.trade_type} ${dep}/${p.monthly_rent || 0}`;
}

function formatPriceValue(val) {
    val = Number(val);
    if (!val || val === 0) return '0';
    if (val >= 10000) {
        const uk = Math.floor(val / 10000);
        const man = val % 10000;
        return man > 0 ? `${uk}억 ${man}` : `${uk}억`;
    }
    return val.toLocaleString();
}

window.showPropertyDetail = function(p) {
    const detailView = document.getElementById('propertyDetailView');
    if (!detailView) return;

    const priceStr = formatPriceDisplay(p);
    
    detailView.querySelector('.detail-price-title').textContent = priceStr;
    const metaTop = detailView.querySelector('.detail-meta-top');
    if (metaTop) {
        const regDate = new Date(p.created_at);
        metaTop.innerHTML = `<span>등록번호 ${p.id}</span><span>${regDate.toLocaleDateString()}</span>`;
    }

    detailView.querySelector('.detail-loc-text').textContent = `${p.sido || ''} ${p.sigungu || ''} ${p.dong || ''} · 관리비 ${p.maintenance_fee || 0}만원`;
    detailView.querySelector('.detail-desc-box').textContent = p.description || '상세 설명이 없습니다.';
    detailView.querySelector('.bottom-price').textContent = priceStr;
    
    const features = detailView.querySelectorAll('.feature-item');
    if (features[0]) features[0].innerHTML = `<div class="feature-icon">📐</div>전용 ${p.area || '-'}㎡`;
    if (features[1]) features[1].innerHTML = `<div class="feature-icon">🚪</div>${p.room_count || '-'} (욕실 ${p.bathroom_count || '-'}개)`;
    
    const galleryImg = detailView.querySelector('.detail-gallery img');
    if (galleryImg) {
        galleryImg.src = (p.images && p.images.length > 0) ? p.images[0] : 'https://via.placeholder.com/600x400/DDDDDD/666666?text=No+Image';
    }

    detailView.style.display = 'flex';
};

window.hidePropertyDetail = function() {
    const detailView = document.getElementById('propertyDetailView');
    if (detailView) detailView.style.display = 'none';
};

// 주소 기반 마커 표시 로직 (Kakao Geocoder 사용)
function addMarkersToMap(props) {
    if (!window.mapInstance) return;
    
    const geocoder = new kakao.maps.services.Geocoder();

    props.forEach(p => {
        const fullAddr = `${p.sido || ''} ${p.sigungu || ''} ${p.dong || ''} ${p.detail_address || ''}`;
        
        geocoder.addressSearch(fullAddr, (result, status) => {
            if (status === kakao.maps.services.Status.OK) {
                const coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                const marker = new kakao.maps.Marker({
                    map: window.mapInstance,
                    position: coords
                });

                const infowindow = new kakao.maps.InfoWindow({
                    content: `<div style="padding:5px;font-size:12px;">${formatPriceDisplay(p)}</div>`
                });

                kakao.maps.event.addListener(marker, 'click', () => {
                    showPropertyDetail(p);
                    infowindow.open(window.mapInstance, marker);
                    setTimeout(() => infowindow.close(), 3000);
                });
            }
        });
    });
}
