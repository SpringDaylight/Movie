import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

export default function SignupPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [nickname, setNickname] = useState("");
  const [userId, setuserId] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const handleSignup = () => {
    const nameValue = name.trim();
    if (nameValue) {
      localStorage.setItem("mw_profile_name", nameValue);
      localStorage.setItem(
        "mw_profile_bio",
        "Enjoying drama and SF with strong emotional arcs."
      );
    }
    localStorage.setItem("mw_logged_in", "true");
    navigate("/taste-survey");
  };

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>회원가입</h1>
          <p>계정을 만들면 바로 로그인됩니다.</p>
        </section>

        <section className="section">
          <article className="card">
            <div className="form-grid">
              <label htmlFor="signup-name">이름</label>
              <input
                id="signup-name"
                type="text"
                placeholder="이름"
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
              <label htmlFor="signup-nickname">닉네임</label>
              <input
                id="signup-nickname"
                type="text"
                placeholder="닉네임"
                value={nickname}
                onChange={(event) => setNickname(event.target.value)}
              />
              <label htmlFor="signup-userid">아이디</label>
              <input
                id="signup-userid"
                type="text"
                placeholder="아이디"
                value={userId}
                onChange={(event) => setuserId(event.target.value)}
              />
              <label htmlFor="signup-password">비밀번호</label>
              <input
                id="signup-password"
                type="password"
                placeholder="********"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <label htmlFor="signup-confirm">비밀번호 확인</label>
              <input
                id="signup-confirm"
                type="password"
                placeholder="********"
                value={confirm}
                onChange={(event) => setConfirm(event.target.value)}
              />
              <label htmlFor="signup-email">이메일</label>
              <input
                id="signup-email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
              <button className="primary-btn" type="button" onClick={handleSignup}>
                회원가입
              </button>
            </div>
            <p className="auth-link">
              이미 계정이 있나요? <Link to="/login">로그인</Link>
            </p>
          </article>
        </section>
        <section>
          <div className="social-login">
              <p className="muted">소셜 계정으로 회원가입하기</p>
              <div className="social-login-buttons">
                <button className="secondary-btn social-btn" type="button">???? ????</button>
                <button className="secondary-btn social-btn" type="button">??? ????</button>
              </div>
            </div>
        </section>
      </main>
    </MainLayout>
  );
}
