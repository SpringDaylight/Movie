import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

type ViewMode = "posters" | "reviews";

export default function ActivityPage() {
  const [view, setView] = useState<ViewMode>("posters");
  const navigate = useNavigate();

  return (
    <MainLayout>
      <main className="container">
        
        <section className="section">
          <article className="card taste-preview">
            <div className="taste-preview-header">
              <h2>취향 분석 대시보드</h2>
              <p>최근 평가 기반 요약</p>
            </div>
            <div className="taste-preview-body">
              <div>
                <p className="muted">선호 키워드</p>
                <div className="tag-list" style={{ marginTop: 8 }}>
                  <span className="tag">감정선</span>
                  <span className="tag">몰입</span>
                  <span className="tag">여운</span>
                </div>
              </div>
              <div>
                <p className="muted">가장 높은 장르</p>
                <p className="probability">드라마 · SF</p>
              </div>
            </div>
            <button
              className="primary-btn taste-preview-cta"
              type="button"
              onClick={() => navigate("/taste-analysis")}
            >
              자세히보기
            </button>
          </article>
        </section>
        {/*  
        <section className="page-title">
          <h1>내 활동</h1>
          <p>내가 본 영화와 남긴 리뷰를 관리해요.</p>
        </section> */}

        <section className="section card">
          <div className="section-header centered">
            
            {/* <p>시청/리뷰/컬렉션 현황</p> */}
          </div>  
          <div className="activity-stats">
            <div className="stat full">
              <h2>활동 요약</h2>
              <p>내가 본 영화와 남긴 리뷰를 관리해요.</p>
            </div>
            <div
              className="stat bottom-left clickable hoverable"
              role="button"
              tabIndex={0}
              onClick={() => {
                setView("posters");
                setTimeout(() => {
                  const target = document.getElementById("posters-section");
                  if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                  }
                }, 0);
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  setView("posters");
                  setTimeout(() => {
                    const target = document.getElementById("posters-section");
                    if (target) {
                      target.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                  }, 0);
                }
              }}
            >
              <strong>128</strong>
              <span>시청작</span>
            </div>
            <div
              className="stat bottom-right clickable hoverable"
              role="button"
              tabIndex={0}
              onClick={() => {
                setView("reviews");
                setTimeout(() => {
                  const target = document.getElementById("reviews-section");
                  if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                  }
                }, 0);
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  setView("reviews");
                  setTimeout(() => {
                    const target = document.getElementById("reviews-section");
                    if (target) {
                      target.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                  }, 0);
                }
              }}
            >
              <strong>42</strong>
              <span>리뷰</span>
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
              className={`filter-chip ${view === "posters" ? "active" : ""}`}
              id="tab-posters"
              data-view="posters"
              role="tab"
              aria-selected={view === "posters"}
              type="button"
              onClick={() => setView("posters")}
            >
              포스터 그리드
            </button>
            <button
              className={`filter-chip ${view === "reviews" ? "active" : ""}`}
              id="tab-reviews"
              data-view="reviews"
              role="tab"
              aria-selected={view === "reviews"}
              type="button"
              onClick={() => setView("reviews")}
            >
              리뷰 목록
            </button>
          </div>
        </section>

        {view === "posters" && (
          <section className="section view-section" data-view="posters" id="posters-section">
            <div className="poster-grid">
              <Link to="/movies/1">
                <img
                  src="https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg"
                  alt="이터널 선샤인 포스터"
                />
              </Link>
              <Link to="/movies/2">
                <img
                  src="https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"
                  alt="라라랜드 포스터"
                />
              </Link>
              <Link to="/movies/3">
                <img
                  src="https://image.tmdb.org/t/p/w500/bgIt92V3IDysoAIcEfOo2ZK9PEv.jpg"
                  alt="인셉션 포스터"
                />
              </Link>
              <Link to="/movies/4">
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
              <Link to="/movies/7">
                <img
                  src="https://image.tmdb.org/t/p/w500/4q2hz2m8hubgvijz8Ez0T2Os2Yv.jpg"
                  alt="듄 포스터"
                />
              </Link>
              <Link to="/movies/8">
                <img
                  src="https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg"
                  alt="작은 아씨들 포스터"
                />
              </Link>
              <Link to="/movies/9">
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
              <Link to="/movies/11">
                <img
                  src="https://image.tmdb.org/t/p/w500/2TeJfUZMGolfDdW6DKhfIWqvq8y.jpg"
                  alt="조커 속편 포스터"
                />
              </Link>
              <Link to="/movies/12">
                <img
                  src="https://image.tmdb.org/t/p/w500/rc7j1oQOMxudcmGeYb5SPbII6e3.jpg"
                  alt="조용한 곳 포스터"
                />
              </Link>
            </div>
          </section>
        )}

        {view === "reviews" && (
          <section className="section view-section" data-view="reviews" id="reviews-section">
            <div className="section-header">
              <h2>최근 리뷰</h2>
              <p>감상 기록에서 가져온 목록</p>
            </div>
            <div className="review-list">
              <Link className="card-link" to="/reviews/1">
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
              <Link className="card-link" to="/reviews/2">
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
              <Link className="card-link" to="/reviews/3">
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
        )}
      </main>
    </MainLayout>
  );
}
