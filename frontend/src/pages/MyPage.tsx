import { useMemo, useState } from "react";
import MainLayout from "../components/layout/MainLayout";
import { Link } from "react-router-dom";

type ViewMode = "posters" | "reviews";

export default function MyPage() {
  const [view, setView] = useState<ViewMode>("posters");

  const isPosters = useMemo(() => view === "posters", [view]);
  const isReviews = useMemo(() => view === "reviews", [view]);

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>마이페이지</h1>
          <p>내 취향과 기록을 한눈에 확인해요.</p>
        </section>

        <section className="section card profile-card">
          <div className="profile-header">
            <div className="profile-avatar">DS</div>
            <div>
              <h2>도슨</h2>
              <p className="muted">감정선 강한 드라마 · SF를 자주 봐요.</p>
              <div className="profile-stats">
                <div>
                  <strong>128</strong>
                  <span>시청작</span>
                </div>
                <div>
                  <strong>42</strong>
                  <span>리뷰</span>
                </div>
                <div>
                  <strong>16</strong>
                  <span>컬렉션</span>
                </div>
              </div>
              <Link className="secondary-btn profile-link" to="/taste-analysis">
                취향 분석 보기
              </Link>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>내 영화 보기</h2>
            <p>포스터 그리드 · 리뷰 목록</p>
          </div>

          <div className="view-toggle" role="tablist" aria-label="내 영화 보기">
            <button
              className={`filter-chip ${isPosters ? "active" : ""}`}
              id="tab-posters"
              data-view="posters"
              role="tab"
              aria-selected={isPosters ? "true" : "false"}
              onClick={() => setView("posters")}
              type="button"
            >
              포스터 그리드
            </button>
            <button
              className={`filter-chip ${isReviews ? "active" : ""}`}
              id="tab-reviews"
              data-view="reviews"
              role="tab"
              aria-selected={isReviews ? "true" : "false"}
              onClick={() => setView("reviews")}
              type="button"
            >
              리뷰 목록
            </button>
          </div>
        </section>

        <section
          className={`section view-section ${isPosters ? "" : "is-hidden"}`}
          data-view="posters"
        >
          <div className="poster-grid">
            <Link to="/movies/2">
              <img
                src="https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg"
                alt="이터널 선샤인 포스터"
              />
            </Link>
            <Link to="/movies/3">
              <img
                src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
                alt="라라랜드 포스터"
              />
            </Link>
            <Link to="/movies/4">
              <img
                src="https://image.tmdb.org/t/p/w500/bgIt92V3IDysoAIcEfOo2ZK9PEv.jpg"
                alt="인셉션 포스터"
              />
            </Link>
            <Link to="/movies/1">
              <img
                src="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
                alt="인터스텔라 포스터"
              />
            </Link>
            <Link to="/movies/5">
              <img
                src="https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
                alt="기생충 포스터"
              />
            </Link>
            <Link to="/movies/6">
              <img
                src="https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
                alt="매트릭스 포스터"
              />
            </Link>
            <Link to="/movies/13">
              <img
                src="https://image.tmdb.org/t/p/w500/4q2hz2m8hubgvijz8Ez0T2Os2Yv.jpg"
                alt="듄 포스터"
              />
            </Link>
            <Link to="/movies/11">
              <img
                src="https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg"
                alt="작은 아씨들 포스터"
              />
            </Link>
            <Link to="/movies/12">
              <img
                src="https://image.tmdb.org/t/p/w500/bKthjUmxjHjueYrEzdWjQfMArSg.jpg"
                alt="그녀의 취미생활 포스터"
              />
            </Link>
            <Link to="/movies/10">
              <img
                src="https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg"
                alt="조커 포스터"
              />
            </Link>
            <Link to="/movies/14">
              <img
                src="https://image.tmdb.org/t/p/w500/2TeJfUZMGolfDdW6DKhfIWqvq8y.jpg"
                alt="조커 속편 포스터"
              />
            </Link>
            <Link to="/movies/15">
              <img
                src="https://image.tmdb.org/t/p/w500/rc7j1oQOMxudcmGeYb5SPbII6e3.jpg"
                alt="조용한 곳 포스터"
              />
            </Link>
          </div>
        </section>

        <section
          className={`section view-section ${isReviews ? "" : "is-hidden"}`}
          data-view="reviews"
        >
          <div className="section-header">
            <h2>최근 리뷰</h2>
            <p>감상 기록에서 가져온 목록</p>
          </div>
          <div className="review-list">
            <Link className="card-link" to="/reviews/101">
              <article className="card review-card">
                <div className="movie-tile">
                  <img
                    className="poster"
                    src="https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
                    alt="매트릭스 포스터"
                  />
                  <div className="movie-info">
                    <h3>매트릭스</h3>
                    <p className="muted">
                      "현실 감각과 선택에 대한 질문이 오래 남았다."
                    </p>
                    <div className="meta-list">
                      <span>2026.02.01</span>
                      <span>여운</span>
                    </div>
                  </div>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/reviews/102">
              <article className="card review-card">
                <div className="movie-tile">
                  <img
                    className="poster"
                    src="https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg"
                    alt="이터널 선샤인 포스터"
                  />
                  <div className="movie-info">
                    <h3>이터널 선샤인</h3>
                    <p className="muted">
                      "관계의 기억을 지우는 선택이 너무 현실적으로 다가왔다."
                    </p>
                    <div className="meta-list">
                      <span>2026.01.26</span>
                      <span>감정선</span>
                    </div>
                  </div>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/reviews/103">
              <article className="card review-card">
                <div className="movie-tile">
                  <img
                    className="poster"
                    src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
                    alt="라라랜드 포스터"
                  />
                  <div className="movie-info">
                    <h3>라라랜드</h3>
                    <p className="muted">
                      "계절이 바뀔 때마다 음악이 다시 생각났다."
                    </p>
                    <div className="meta-list">
                      <span>2026.01.20</span>
                      <span>로맨스</span>
                    </div>
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