import MainLayout from "../components/layout/MainLayout";

export default function GroupPage() {
  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>모두가 만족할 영화 찾기</h1>
          <p>모임 구성원들의 취향을 합쳐 한 번에 정리해드려요.</p>
        </section>

        <section className="section card">
          <div className="form-grid">
            <label>그룹 선택</label>
            <select defaultValue="개인">
              <option>개인</option>
              <option>친구 모임</option>
              <option>가족</option>
            </select>
            <label>영화 선택</label>
            <input type="text" placeholder="영화 제목 입력" />
            <button className="primary-btn">분석하기</button>
          </div>
        </section>

        <section className="section">
          <article className="card">
            <div className="movie-tile">
              <img
                className="poster"
                src="https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
                alt="기생충 포스터"
              />
              <div className="movie-info">
                <h3>기생충</h3>
                <p className="probability">그룹 만족 확률 67%</p>
                <p className="muted">
                  사회적 메시지와 서스펜스 모두 충족하는 선택지예요.
                </p>
              </div>
            </div>

            <div className="section" style={{ marginTop: 16 }}>
              <h3>멤버별 예상 반응</h3>
              <ul className="list">
                <li>A님: 매우 만족</li>
                <li>B님: 무난</li>
                <li>C님: 다소 지루</li>
              </ul>
            </div>

            <div className="section" style={{ marginTop: 16 }}>
              <h3>해석 요약</h3>
              <p className="muted">
                공통적으로 사회적 풍자와 관계 중심 서사를 선호하지만, 템포
                취향은 다릅니다.
              </p>
            </div>

            <button className="secondary-btn" style={{ marginTop: 18 }}>
              대안 영화 보기
            </button>
          </article>
        </section>
      </main>
    </MainLayout>
  );
}