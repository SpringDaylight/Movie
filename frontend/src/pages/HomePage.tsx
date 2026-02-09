import MainLayout from "../components/layout/MainLayout";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <MainLayout>
      <main className="container">
        <section className="hero">
          <div>
            {/* <p className="eyebrow">Discover</p> */}
            <h1>지금 기분에 맞는 영화를 찾아보세요</h1>
            <p>
              취향 데이터와 상황 맥락을 결합해 만족 가능성까지 한 번에 알려드려요.
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
        </section>

        <section className="section">
          <div className="section-header">
            <h2>나를 위한 추천</h2>
            <button className="primary-btn btn-animate">새로고침</button>
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

            <Link className="card-link" to="/movies/4">
              <article className="card movie-tile">
              <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg"
                  alt="조커 포스터"
                />
                <div className="movie-info">
                  <h3>조커</h3>
                  <p className="probability">만족 확률 78%</p>
                  <p className="muted">인물 심리와 관계 서사를 좋아할 때 추천.</p>
                  <span className="ghost-btn">자세히 보기</span>
                </div>
              </article>
            </Link>
          </div>
        </section>
      </main>
    </MainLayout>
  );
}