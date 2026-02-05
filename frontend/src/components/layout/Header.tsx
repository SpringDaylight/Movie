import { useCallback, useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";

export default function Header() {
  const navClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? "active" : undefined;
  const [profileHref, setProfileHref] = useState("/login");
  const [profileLabel, setProfileLabel] = useState("로그인");

  const syncProfile = useCallback(() => {
    const isLoggedIn = localStorage.getItem("mw_logged_in") === "true";
    const savedName = localStorage.getItem("mw_profile_name");

    if (isLoggedIn) {
      setProfileHref("/profile");
      setProfileLabel(savedName ? savedName.slice(0, 2) : "DS");
    } else {
      setProfileHref("/login");
      setProfileLabel("로그인");
    }
  }, []);

  useEffect(() => {
    syncProfile();
    const handleAuthChange = () => syncProfile();
    window.addEventListener("mw_auth_change", handleAuthChange);
    window.addEventListener("storage", handleAuthChange);

    return () => {
      window.removeEventListener("mw_auth_change", handleAuthChange);
      window.removeEventListener("storage", handleAuthChange);
    };
  }, [syncProfile]);

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
            내 활동
          </NavLink>
        </nav>

        <div className="top-actions">
          <Link className="profile-chip" to={profileHref}>
            {profileLabel}
          </Link>
        </div>
      </div>
    </header>
  );
}
