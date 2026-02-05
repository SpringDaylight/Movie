import { NavLink } from "react-router-dom";

export default function BottomNav() {
  const navClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? "active" : undefined;

  return (
    <nav className="bottom-nav">
      <NavLink to="/" className={navClass} end>
        홈
      </NavLink>
      <NavLink to="/movies" className={navClass}>
        영화
      </NavLink>
      <NavLink to="/group" className={navClass}>
        같이 보기
      </NavLink>
      <NavLink to="/mypage" className={navClass}>
        내 활동
      </NavLink>
    </nav>
  );
}
