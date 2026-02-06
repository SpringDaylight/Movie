import { useState } from "react";
import { Link } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";

export default function FindIdPage() {
  const [email, setEmail] = useState("");

  return (
    <MainLayout>
      <main className="container">
        <section className="page-title">
          <h1>아이디 찾기</h1>
          <p>가입 시 사용한 이메일로 아이디를 찾습니다.</p>
        </section>

        <section className="section">
          <article className="card">
            <div className="form-grid">
              <label htmlFor="find-id-email">이메일</label>
              <input
                id="find-id-email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
              <button className="primary-btn" type="button">
                아이디 찾기
              </button>
            </div>
            <div className="auth-actions">
              <Link className="ghost-btn" to="/login">
                로그인으로 돌아가기
              </Link>
              <Link className="secondary-btn" to="/signup">
                회원가입
              </Link>
            </div>
          </article>
        </section>
      </main>
    </MainLayout>
  );
}
