import { useState } from "react";
import { useNavigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

const moodOptions = ["편안한", "감성적인", "몰입감 있는", "짜릿한", "유쾌한"];
const genreOptions = ["드라마", "로맨스", "SF", "스릴러", "애니메이션", "다큐"];

export default function TasteSurveyPage() {
  const navigate = useNavigate();
  const [moods, setMoods] = useState<string[]>([]);
  const [genres, setGenres] = useState<string[]>([]);
  const [watchTime, setWatchTime] = useState("90");

  const toggleValue = (
    value: string,
    list: string[],
    setList: (next: string[]) => void
  ) => {
    if (list.includes(value)) {
      setList(list.filter((item) => item !== value));
      return;
    }
    setList([...list, value]);
  };

  const handleSubmit = () => {
    localStorage.setItem("mw_taste_moods", JSON.stringify(moods));
    localStorage.setItem("mw_taste_genres", JSON.stringify(genres));
    localStorage.setItem("mw_taste_watch_time", watchTime);
    navigate("/");
  };

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>취향 분석 설문</h1>
          <p>당신에게 맞는 영화를 추천하기 위해 간단한 질문을 할게요.</p>
        </section>

        <section className="section">
          <article className="card">
            <div className="form-grid centered">
              <div>
                <h4 className="filter-title">선호하는 분위기</h4>
                <div className="tag-list">
                  {moodOptions.map((mood) => (
                    <button
                      key={mood}
                      className={`filter-chip ${moods.includes(mood) ? "active" : ""}`}
                      type="button"
                      onClick={() => toggleValue(mood, moods, setMoods)}
                    >
                      {mood}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="filter-title">좋아하는 장르</h4>
                <div className="tag-list">
                  {genreOptions.map((genre) => (
                    <button
                      key={genre}
                      className={`filter-chip ${genres.includes(genre) ? "active" : ""}`}
                      type="button"
                      onClick={() => toggleValue(genre, genres, setGenres)}
                    >
                      {genre}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="filter-title">선호 러닝타임</h4>
                <div className="tag-list">
                  {["90", "120", "150"].map((time) => (
                    <button
                      key={time}
                      className={`filter-chip ${watchTime === time ? "active" : ""}`}
                      type="button"
                      onClick={() => setWatchTime(time)}
                    >
                      {time}분 내외
                    </button>
                  ))}
                </div>
              </div>

              <button className="primary-btn" type="button" onClick={handleSubmit}>
                설문 완료하고 추천 받기
              </button>
            </div>
          </article>
        </section>
      </main>
    </MainLayout>
  );
}
