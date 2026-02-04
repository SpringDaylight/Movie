import MainLayout from "../components/layout/MainLayout";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <MainLayout>
      <main className="container">
        <section className="hero">
          <div>
            <p className="eyebrow">Discover</p>
            <h1>지금 기분에 맞는 영화를 찾아보세요</h1>
            <p>
              취향 데이터와 상황 맥락을 결합해 만족 가능성까지 한 번에
              알려드려요.
            </p>
            <div className="hero-actions">
              <input
                className="search-input"
                type="text"
                placeholder="장르, 분위기, 제목으로 검색"
              />
              <button className="primary-btn">맞춤 추천 받기</button>
            </div>
          </div>
          <div className="card">
            <h3>오늘의 집중 키워드</h3>
            <p className="muted">감정 흐름 · 관계성 · 여운</p>
            <div className="tag-list" style={{ marginTop: 12 }}>
              <span className="tag">잔잔한 성장</span>
              <span className="tag">따뜻한 로맨스</span>
              <span className="tag">몰입감 있는 SF</span>
            </div>
            <button className="secondary-btn" style={{ marginTop: 16 }}>
              컨디션 설정하기
            </button>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>오늘의 제안</h2>
            <p>당신의 최근 취향을 반영한 추천 리스트</p>
          </div>
          <div className="movie-grid">
            <Link className="card-link" to="/movies/1">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg"
                  alt="이터널 선샤인 포스터"
                />
                <div className="movie-info">
                  <h3>이터널 선샤인</h3>
                  <p className="probability">만족 확률 81%</p>
                  <p className="muted">
                    관계 중심 서사와 여운 있는 결말을 선호하셨어요.
                  </p>
                  <span className="ghost-btn">자세히 보기</span>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/movies/2">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
                  alt="라라랜드 포스터"
                />
                <div className="movie-info">
                  <h3>라라랜드</h3>
                  <p className="probability">만족 확률 74%</p>
                  <p className="muted">음악과 성장 서사를 좋아하셨어요.</p>
                  <span className="ghost-btn">자세히 보기</span>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/movies/3">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/bgIt92V3IDysoAIcEfOo2ZK9PEv.jpg"
                  alt="인셉션 포스터"
                />
                <div className="movie-info">
                  <h3>인셉션</h3>
                  <p className="probability">만족 확률 69%</p>
                  <p className="muted">
                    퍼즐형 전개와 강한 몰입감을 선호하셨어요.
                  </p>
                  <span className="ghost-btn">자세히 보기</span>
                </div>
              </article>
            </Link>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>지금 감정에 맞는 무드</h2>
            <p>오늘은 어떤 결을 보고 싶나요?</p>
          </div>
          <div className="tag-list">
            <span className="tag">위로가 되는</span>
            <span className="tag">속도감 있는</span>
            <span className="tag">세계관 몰입</span>
            <span className="tag">감정 정리</span>
            <span className="tag">연인과 함께</span>
            <span className="tag">혼자 보기 좋은</span>
          </div>
        </section>
      </main>
    </MainLayout>
  );
}