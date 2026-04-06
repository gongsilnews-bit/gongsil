import { supabase } from '../lib/supabase';
import Header from '../components/Header';

export default async function Home() {
  // SSR: Fetch top 3 hot news from supabase server-side
  let hotNews = [];
  try {
    const { data } = await supabase
      .from('articles')
      .select('id, title, thumbnail_url, created_at')
      .order('created_at', { ascending: false })
      .limit(3);
    if (data) hotNews = data;
  } catch (err) {
    console.error('Failed to fetch hot news:', err);
  }

  return (
    <>
      <Header />
      <main className="container px-20 relative" style={{ position: 'relative' }}>
        <div className="hero-section" style={{ padding: '0 25px 0 0', border: '0.5px solid #dcdcdc', borderTop: 'none', marginBottom: '0', background: '#fff' }}>
          
          {/* Left: Map Area placeholder for now, we will add a real Map component */}
          <div className="hero-left" style={{ display: 'flex', marginTop: '0', flex: '2.8', position: 'relative', minHeight: '480px', padding: '0' }}>
            <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: '#eaeaea', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <h2 style={{color: '#888'}}>카카오 지도 SSR 로딩 대기중...</h2>
            </div>
          </div>
          
          {/* Right: AD & HOT NEWS SSR */}
          <div className="hero-right" style={{ marginTop: '0' }}>
            <div className="banner-box" style={{ marginTop: '0', marginBottom: '30px', width: '100%', height: '180px', background: '#f0f0f0', border: '1px solid #ccc', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', fontWeight: '800', color: '#555', textAlign: 'center' }}>배너 1</div>
            
            <div className="hn-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', borderBottom: '2px solid #1a4282', paddingBottom: '10px'}}>
              <h2 style={{fontSize: '18px', fontWeight: '800', color: '#1a4282'}}>HOT 공실뉴스</h2>
              <a href="/news.html" style={{fontSize: '12px', color: '#666', fontWeight: '600'}}>더보기 &gt;</a>
            </div>
            <div className="hn-list" style={{ marginBottom: '0', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {hotNews.map((news) => (
                <div className="hn-item" key={news.id} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', cursor: 'pointer' }}>
                  <div className="hn-img" style={{ width: '90px', height: '65px', background: `url('${news.thumbnail_url || 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&q=80'}') center/cover`, borderRadius: '6px', flexShrink: 0 }}></div>
                  <div className="hn-txt">
                    <h4 style={{ fontSize: '14px', fontWeight: '700', lineHeight: '1.4', marginBottom: '6px', color: '#111', wordBreak: 'keep-all' }}>{news.title}</h4>
                    <span style={{ fontSize: '12px', color: '#999' }}>{new Date(news.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
