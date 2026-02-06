import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

export default function LoginPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    const nameValue = name.trim();
    if (nameValue) {
      localStorage.setItem("mw_profile_name", nameValue);
      localStorage.setItem(
        "mw_profile_bio",
        "Enjoying drama and SF with strong emotional arcs."
      );
    }
    localStorage.setItem("mw_logged_in", "true");
    navigate("/mypage");
  };

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>로그인</h1>
        </section>

        <section className="section">
          <article className="card">
            <div className="form-grid">
              <label htmlFor="login-name">아이디</label>
              <input
                id="login-name"
                type="text"
                placeholder="아이디"
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
              <label htmlFor="login-password">비밀번호</label>
              <input
                id="login-password"
                type="password"
                placeholder="********"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <button className="primary-btn" type="button" onClick={handleLogin}>
                로그인
              </button>
            </div>
            <div className="auth-actions">
              <Link className="secondary-btn" to="/signup">회원가입</Link>
              <Link className="secondary-btn" to="/find-id">아이디 찾기</Link>
              <Link className="secondary-btn" to="/signup">비밀번호 찾기</Link>
            </div>
          </article>
        </section>
      </main>
    </MainLayout>
  );
}
