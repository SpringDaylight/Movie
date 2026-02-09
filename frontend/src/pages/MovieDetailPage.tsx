import MainLayout from "../components/layout/MainLayout";
import { Link, useNavigate } from "react-router-dom";

export default function MovieDetailPage() {
  const navigate = useNavigate();

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>영화 상세</h1>
          <p>영화를 선택하면 상세 정보와 나와의 적합도를 함께 볼 수 있어요.</p>
        </section>

        <section className="section">
          <article className="card">
            <div className="movie-tile">
              <img
                className="poster"
                src="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
                alt="인터스텔라 포스터"
              />
              <div className="movie-info">
                <h3>인터스텔라</h3>
                <p className="muted">2014 · SF/드라마 · 169분</p>
                <div className="tag-list" style={{ marginTop: 10 }}>
                  <span className="tag">우주</span>
                  <span className="tag">가족</span>
                  <span className="tag">감정선</span>
                </div>
              </div>
            </div>

            <div className="section" style={{ marginTop: 18 }}>
              <h3>시놉시스</h3>
              <p className="muted">
                지구의 식량 위기 속에서 인류를 구할 새로운 거처를 찾기 위해
                우주로 떠나는 탐사대의 이야기입니다.
              </p>
            </div>

            <div className="section" style={{ marginTop: 18 }}>
              <h3>나와의 적합도</h3>
              <p className="probability">적합 확률 83%</p>
              <ul className="list">
                <li>거대한 세계관과 몰입도 높은 전개를 선호하셨어요.</li>
                <li>가족 서사가 중심인 작품을 좋아하셨어요.</li>
                <li>유사 취향 사용자 반응이 긍정적이었어요.</li>
              </ul>
            </div>

            <div className="section" style={{ marginTop: 18 }}>
              <h3>주의할 점</h3>
              <p className="muted">후반부 과학 설정이 어렵게 느껴질 수 있어요.</p>
            </div>

            <div className="hero-actions" style={{ marginTop: 18 }}>
              <button className="primary-btn">바로 감상하기</button>
            </div>
          </article>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>내 리뷰</h2>
            <p>내가 남긴 코멘트</p>
          </div>
          <article className="card review-card review-empty">
            <p className="muted">아직 이 영화에 대한 내 리뷰가 없어요.</p>
            <button
              className="primary-btn"
              type="button"
              onClick={() => navigate("/log")}
            >
              리뷰 남기기
            </button>
          </article>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>다른 사람들의 리뷰</h2>
            <p>이 영화에 대한 다양한 반응</p>
          </div>
          <div className="review-list">
            <Link className="card-link" to="/reviews/1">
              <article className="card review-card">
                <div className="review-header">
                  <div className="review-user">
                    <div className="review-avatar">HJ</div>
                    <div>
                      <p className="review-name">해진</p>
                      <p className="muted">2026.01.30 · 평점 4.0</p>
                    </div>
                  </div>
                  <button className="ghost-btn">좋아요 24</button>
                </div>
                <p className="review-text">
                  "과학보다 감정이 더 선명하게 남는 작품. 가족 서사가 깊게
                  와닿았다."
                </p>
                <div className="review-actions">
                  <span className="tag">가족</span>
                  <span className="tag">감정선</span>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/reviews/2">
              <article className="card review-card">
                <div className="review-header">
                  <div className="review-user">
                    <div className="review-avatar">MK</div>
                    <div>
                      <p className="review-name">민규</p>
                      <p className="muted">2026.01.29 · 평점 3.5</p>
                    </div>
                  </div>
                  <button className="ghost-btn">좋아요 11</button>
                </div>
                <p className="review-text">
                  "중반부는 숨 막히게 몰입했는데, 후반부는 조금 어렵게
                  느껴졌다."
                </p>
                <div className="review-actions">
                  <span className="tag">몰입</span>
                  <span className="tag">난이도</span>
                </div>
              </article>
            </Link>

            <Link className="card-link" to="/reviews/3">
              <article className="card review-card">
                <div className="review-header">
                  <div className="review-user">
                    <div className="review-avatar">SO</div>
                    <div>
                      <p className="review-name">소연</p>
                      <p className="muted">2026.01.26 · 평점 4.8</p>
                    </div>
                  </div>
                  <button className="ghost-btn">좋아요 52</button>
                </div>
                <p className="review-text">
                  "끝내주는 몰입감. IMAX로 다시 보고 싶은 영화 리스트에
                  추가했다."
                </p>
                <div className="review-actions">
                  <span className="tag">재관람</span>
                  <span className="tag">IMAX</span>
                </div>
              </article>
            </Link>
          </div>
        </section>
      </main>
    </MainLayout>
  );
}
