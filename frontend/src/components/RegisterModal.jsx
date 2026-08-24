import { useState } from "react";
import { registerUser } from "../services/authService";

function RegisterModal({
  onClose,
  onLogin,
  onRegistered
}) {
  const [name, setName] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [error, setError] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    setError("");

    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill in all fields.");
      return;
    }

    if (password.length < 6) {
      setError(
        "Password must contain at least 6 characters."
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const result = registerUser(
      name,
      email,
      password
    );

    if (!result.success) {
      setError(result.message);
      return;
    }

    onRegistered(result.user);
  };

  return (
    <div
      className="auth-overlay"
      onClick={onClose}
    >

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
          🌱
        </div>

        <h2>Create Account</h2>

        <p className="auth-subtitle">
          Start analyzing renewable energy potential
        </p>

        <form onSubmit={handleRegister}>

          <div className="auth-field">

            <label>Full Name</label>

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) =>
                setName(e.target.value)
              }
            />

          </div>

          <div className="auth-field">

            <label>Email Address</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
            />

          </div>

          <div className="auth-field">

            <label>Password</label>

            <div className="password-wrapper">

              <input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Create a password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
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

          <div className="auth-field">

            <label>Confirm Password</label>

            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) =>
                setConfirmPassword(e.target.value)
              }
            />

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
            Create Account →
          </button>

        </form>

        <div className="auth-divider">
          <span>OR</span>
        </div>

        <p className="auth-register">

          Already have an account?

          <button onClick={onLogin}>
            Login
          </button>

        </p>

      </div>

    </div>
  );
}

export default RegisterModal;