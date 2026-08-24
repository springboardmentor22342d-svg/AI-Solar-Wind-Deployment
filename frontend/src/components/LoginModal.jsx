import { useState } from "react";
import { loginUser } from "../services/authService";

function LoginModal({ onClose, onLogin, onCreateAccount }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    setError("");

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    const result = loginUser(email, password);

    if (!result.success) {
      setError(result.message);
      return;
    }

    onLogin(result.user);
  };

  return (
    <div className="auth-overlay" onClick={onClose}>

      <div
        className="auth-modal"
        onClick={(e) => e.stopPropagation()}
      >

        <button
          className="auth-close"
          onClick={onClose}
        >
          ×
        </button>

        <div className="auth-logo">
          ☀️
        </div>

        <h2>Welcome Back</h2>

        <p className="auth-subtitle">
          Sign in to access your renewable energy dashboard
        </p>

        <form onSubmit={handleLogin}>

          <div className="auth-field">

            <label>Email Address</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

          </div>

          <div className="auth-field">

            <label>Password</label>

            <div className="password-wrapper">

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
              >
                {showPassword ? "🙈" : "👁"}
              </button>

            </div>

          </div>

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="auth-submit"
          >
            Login →
          </button>

        </form>

        <div className="auth-divider">
          <span>OR</span>
        </div>

        <p className="auth-register">

          Don't have an account?

          <button
            onClick={onCreateAccount}
          >
            Create Account
          </button>

        </p>

      </div>

    </div>
  );
}

export default LoginModal;