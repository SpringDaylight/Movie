import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import HomePage from "./pages/HomePage";
import MoviesPage from "./pages/MoviesPage";
import MovieDetailPage from "./pages/MovieDetailPage";
import GroupPage from "./pages/GroupPage";
import MyPage from "./pages/MyPage";
import TasteAnalysisPage from "./pages/TasteAnalysisPage";
import LogPage from "./pages/LogPage";
import ReviewDetailPage from "./pages/ReviewDetailPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* React 기준 정상 라우트 */}
        <Route path="/" element={<HomePage />} />
        <Route path="/movies" element={<MoviesPage />} />
        <Route path="/movies/:movieId" element={<MovieDetailPage />} />
        <Route path="/group" element={<GroupPage />} />
        <Route path="/mypage" element={<MyPage />} />
        <Route path="/taste-analysis" element={<TasteAnalysisPage />} />
        <Route path="/log" element={<LogPage />} />
        <Route path="/reviews/:reviewId" element={<ReviewDetailPage />} />

        {/* 레거시 HTML 경로 대응 (전환기 안전장치) */}
        <Route path="/home.html" element={<Navigate to="/" replace />} />
        <Route path="/movies.html" element={<Navigate to="/movies" replace />} />
        <Route
          path="/movie-detail.html"
          element={<Navigate to="/movies/1" replace />}
        />
        <Route path="/group.html" element={<Navigate to="/group" replace />} />
        <Route path="/mypage.html" element={<Navigate to="/mypage" replace />} />
        <Route
          path="/taste-analysis.html"
          element={<Navigate to="/taste-analysis" replace />}
        />
        <Route path="/log.html" element={<Navigate to="/log" replace />} />
        <Route
          path="/review-detail.html"
          element={<Navigate to="/reviews/1" replace />}
        />

        {/* fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
