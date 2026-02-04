import { Link, NavLink } from "react-router-dom";

export default function Header() {
  const navClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? "active" : undefined;

  return (
    <header className="top-bar">
      <div className="top-bar-inner">
        <Link className="brand" to="/">
          <div className="brand-mark">W</div>
          <div>
            <p className="brand-title">오늘 뭐 볼까?</p>
            <p className="brand-sub">취향 기반 영화 탐색</p>
          </div>
        </Link>

        <nav className="top-nav">
          <NavLink to="/" className={navClass} end>
            찾기
          </NavLink>
          <NavLink to="/movies" className={navClass}>
            영화
          </NavLink>
          <NavLink to="/group" className={navClass}>
            같이 정하기
          </NavLink>
          <NavLink to="/mypage" className={navClass}>
            마이페이지
          </NavLink>
        </nav>

        <div className="top-actions">
          <button className="profile-chip">DS</button>
        </div>
      </div>
    </header>
  );
}