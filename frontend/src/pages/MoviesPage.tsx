import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

type MovieItem = {
  id: number;
  title: string;
  poster: string;
  alt: string;
  probability: string;
  summary: string;
  genres: string[];
  tags: string[];
  meta: string[];
};

const sortFilters = [
  { value: "latest", label: "최신개봉작" },
  { value: "popular", label: "박스오피스 순위" },
  { value: "rating", label: "평점 높은 순" },
  { value: "curation", label: "큐레이션 추천" },
];

const genreFilters = [
  { value: "romance", label: "로맨스" },
  { value: "drama", label: "드라마" },
  { value: "thriller", label: "스릴러" },
  { value: "horror", label: "공포" },
  { value: "action", label: "액션" },
  { value: "crime", label: "범죄" },
  { value: "sf", label: "SF" },
  { value: "fantasy", label: "판타지" },
  { value: "comedy", label: "코미디" },
  { value: "animation", label: "애니메이션" },
  { value: "history", label: "역사" },
  { value: "documentary", label: "다큐멘터리" },
];

const movies: MovieItem[] = [
  {
    id: 10,
    title: "조커",
    poster: "https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg",
    alt: "조커 포스터",
    probability: "만족 확률 78%",
    summary: "인물 심리와 관계 서사를 좋아할 때 추천.",
    genres: ["drama", "thriller"],
    tags: ["popular", "rating"],
    meta: ["드라마", "151분", "15세"],
  },
  {
    id: 11,
    title: "작은 아씨들",
    poster: "https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg",
    alt: "작은 아씨들 포스터",
    probability: "만족 확률 72%",
    summary: "섬세한 인물 성장과 따뜻한 톤을 선호할 때.",
    genres: ["drama"],
    tags: ["latest", "curation"],
    meta: ["드라마", "135분", "전체"],
  },
  {
    id: 12,
    title: "그녀의 취미생활",
    poster: "https://image.tmdb.org/t/p/w500/bKthjUmxjHjueYrEzdWjQfMArSg.jpg",
    alt: "그녀의 취미생활 포스터",
    probability: "만족 확률 66%",
    summary: "잔잔한 일상과 관계의 결을 좋아할 때.",
    genres: ["drama"],
    tags: ["curation"],
    meta: ["드라마", "109분", "12세"],
  },
  {
    id: 13,
    title: "듄",
    poster: "https://image.tmdb.org/t/p/w500/4q2hz2m8hubgvijz8Ez0T2Os2Yv.jpg",
    alt: "듄 포스터",
    probability: "만족 확률 70%",
    summary: "세계관과 몰입을 원할 때 좋은 선택.",
    genres: ["sf"],
    tags: ["popular", "rating"],
    meta: ["SF", "155분", "12세"],
  },
];

export default function MoviesPage() {
  const [selectedSorts, setSelectedSorts] = useState<string[]>([]);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [appliedSorts, setAppliedSorts] = useState<string[]>([]);
  const [appliedGenres, setAppliedGenres] = useState<string[]>([]);

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

  const handleApplyFilters = () => {
    setAppliedSorts(selectedSorts);
    setAppliedGenres(selectedGenres);
  };

  const filteredMovies = useMemo(() => {
    return movies.filter((movie) => {
      const matchGenre =
        appliedGenres.length === 0 ||
        appliedGenres.some((genre) => movie.genres.includes(genre));
      const matchSort =
        appliedSorts.length === 0 ||
        appliedSorts.some((tag) => movie.tags.includes(tag));
      return matchGenre && matchSort;
    });
  }, [appliedGenres, appliedSorts]);

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>영화 목록</h1>
          <p>장르와 분위기에 따라 원하는 기준으로 골라보세요.</p>
        </section>

        <section className="section card">
          <div className="section-search">
            <div className="hero-actions">
              <input
                className="search-input"
                type="text"
                placeholder="영화 제목 검색"
              />
              <button
                className="primary-btn"
                type="button"
                onClick={handleApplyFilters}
              >
                검색 버튼
              </button>
            </div>
          </div>

          {/* <div className="section-header">
            <h2>필터</h2>
            <p>선택한 분류만 보기</p>
          </div> */}

          <div className="filter-group">
            <div>
              <p className="filter-title">분류</p>
              <div className="tag-list">
                {sortFilters.map((filter) => (
                  <button
                    key={filter.value}
                    className={`filter-chip ${
                      selectedSorts.includes(filter.value) ? "active" : ""
                    }`}
                    type="button"
                    onClick={() =>
                      toggleValue(filter.value, selectedSorts, setSelectedSorts)
                    }
                  >
                    {filter.label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <p className="filter-title">장르</p>
              <div className="tag-list">
                {genreFilters.map((filter) => (
                  <button
                    key={filter.value}
                    className={`filter-chip ${
                      selectedGenres.includes(filter.value) ? "active" : ""
                    }`}
                    type="button"
                    onClick={() =>
                      toggleValue(
                        filter.value,
                        selectedGenres,
                        setSelectedGenres
                      )
                    }
                  >
                    {filter.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>선택된 결과</h2>
            <p>선택한 기준으로 추천 영화가 표시됩니다.</p>
          </div>
          <div className="movie-grid">
            {filteredMovies.map((movie) => (
              <Link className="card-link" to={`/movies/${movie.id}`} key={movie.id}>
                <article className="card movie-tile">
                  <img className="poster" src={movie.poster} alt={movie.alt} />
                  <div className="movie-info">
                    <h3>{movie.title}</h3>
                    <p className="probability">{movie.probability}</p>
                    <p className="muted">{movie.summary}</p>
                    <span className="ghost-btn">상세 보기</span>
                    <div className="meta-list">
                      {movie.meta.map((meta) => (
                        <span key={meta}>{meta}</span>
                      ))}
                    </div>
                  </div>
                </article>
              </Link>
            ))}
          </div>
        </section>
      </main>
    </MainLayout>
  );
}
