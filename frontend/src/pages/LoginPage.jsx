import { useState } from "react";
import { login } from "../api/auth";
import { useAuth } from "../hooks/useAuth";

function LoginPage({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { loginUser } = useAuth();

  const handleLogin = async () => {
    setError("");
    setIsLoading(true);
    try {
      const data = await login(email, password);
      loginUser(data.access_token);
      if (onLoginSuccess) onLoginSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-view">
      <section className="login-panel">
        <div className="login-copy">
          <p className="eyebrow">Renewable deployment platform</p>
          <h1>Solar & Wind Deployment Intelligence</h1>
          <p>
            Sign in to analyse candidate locations, compare renewable potential,
            and review feasibility outputs.
          </p>
        </div>

        <div className="login-card">
          <h2>Login</h2>

          <label className="field">
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          <button className="primary-button" onClick={handleLogin} disabled={isLoading}>
            {isLoading ? "Logging in..." : "Login"}
          </button>

          {error && <p className="error-message">{error}</p>}
        </div>
      </section>
    </div>
  );
}

export default LoginPage;
