import { useState } from "react";
import { login } from "./auth";

export default function Login() {
  const [error, setError] = useState("");
  async function signIn() {
    try {
      setError("");
      await login();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to start sign-in.");
    }
  }

  return (
    <main className="shell">
      <section className="login-card">
        <div className="brand-mark">✚</div>
        <span className="demo-label">NORTHSTAR HEALTH CLINIC</span>
        <h1>ClinicFlow AI</h1>
        <p>Secure appointment operations with human approval built into the workflow.</p>
        <button className="button approve" onClick={signIn}>Sign in securely →</button>
        {error && <div className="request-error">{error}</div>}
      </section>
    </main>
  );
}