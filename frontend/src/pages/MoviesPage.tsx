import MainLayout from "../components/layout/MainLayout";
import { Link } from "react-router-dom";

export default function MoviesPage() {
  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>영화 목록</h1>
          <p>장르와 분위기에 따라 원하는 기준으로 골라보세요.</p>
        </section>

        <section className="section card">
          <div className="section-header">
            <h2>필터</h2>
            <p>선택한 분류만 보기</p>
          </div>
          <div className="filter-group">
            <div>
              <p className="filter-title">분류</p>
              <div className="tag-list">
                <button className="filter-chip active">최신개봉작</button>
                <button className="filter-chip">박스오피스 순위</button>
                <button className="filter-chip">평점 높은 순</button>
                <button className="filter-chip">큐레이션 추천</button>
              </div>
            </div>
            <div>
              <p className="filter-title">장르</p>
              <div className="tag-list">
                <button className="filter-chip active">드라마</button>
                <button className="filter-chip">로맨스</button>
                <button className="filter-chip">SF</button>
                <button className="filter-chip">스릴러</button>
                <button className="filter-chip">애니메이션</button>
                <button className="filter-chip">다큐멘터리</button>
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>선택된 결과</h2>
            <p>최신개봉작 · 드라마</p>
          </div>
          <div className="movie-grid">
            <Link className="card-link" to="/movies/10">
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
                  <span className="ghost-btn">상세 보기</span>
                  <div className="meta-list">
                    <span>드라마</span>
                    <span>151분</span>
                    <span>15세</span>
                  </div>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/movies/11">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg"
                  alt="작은 아씨들 포스터"
                />
                <div className="movie-info">
                  <h3>작은 아씨들</h3>
                  <p className="probability">만족 확률 72%</p>
                  <p className="muted">섬세한 인물 성장과 따뜻한 톤을 선호할 때.</p>
                  <span className="ghost-btn">상세 보기</span>
                  <div className="meta-list">
                    <span>드라마</span>
                    <span>135분</span>
                    <span>전체</span>
                  </div>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/movies/12">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/bKthjUmxjHjueYrEzdWjQfMArSg.jpg"
                  alt="그녀의 취미생활 포스터"
                />
                <div className="movie-info">
                  <h3>그녀의 취미생활</h3>
                  <p className="probability">만족 확률 66%</p>
                  <p className="muted">잔잔한 일상과 관계의 결을 좋아할 때.</p>
                  <span className="ghost-btn">상세 보기</span>
                  <div className="meta-list">
                    <span>드라마</span>
                    <span>109분</span>
                    <span>12세</span>
                  </div>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/movies/13">
              <article className="card movie-tile">
                <img
                  className="poster"
                  src="https://image.tmdb.org/t/p/w500/4q2hz2m8hubgvijz8Ez0T2Os2Yv.jpg"
                  alt="듄 포스터"
                />
                <div className="movie-info">
                  <h3>듄</h3>
                  <p className="probability">만족 확률 70%</p>
                  <p className="muted">세계관과 몰입을 원할 때 좋은 선택.</p>
                  <span className="ghost-btn">상세 보기</span>
                  <div className="meta-list">
                    <span>SF</span>
                    <span>155분</span>
                    <span>12세</span>
                  </div>
                </div>
              </article>
            </Link>
          </div>
        </section>
      </main>
    </MainLayout>
  );
}