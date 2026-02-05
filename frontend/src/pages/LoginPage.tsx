import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

export default function LoginPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
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
          <p>계정을 입력하면 바로 로그인됩니다.</p>
        </section>

        <section className="section">
          <article className="card">
            <div className="form-grid">
              <label htmlFor="login-name">이름</label>
              <input
                id="login-name"
                type="text"
                placeholder="이름"
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
              <label htmlFor="login-email">이메일</label>
              <input
                id="login-email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
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
            <p className="auth-link">
              계정이 없나요? <Link to="/signup">회원가입</Link>
            </p>
          </article>
        </section>
      </main>
    </MainLayout>
  );
}
