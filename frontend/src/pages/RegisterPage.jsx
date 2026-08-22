import { useState } from "react";
import { register } from "../api/auth";

function RegisterPage({ onRegisterSuccess, onSwitchToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Renewable Energy Planner");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async () => {
    setError("");
    setIsLoading(true);
    try {
      await register(name, email, password, role);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div style={{ maxWidth: "400px", margin: "4rem auto", padding: "2rem", border: "1px solid #ccc", borderRadius: "8px", textAlign: "center" }}>
        <h2>Registration Successful</h2>
        <p>You can now log in with your new account.</p>
        <button onClick={onSwitchToLogin} style={{ padding: "0.6rem 1.2rem" }}>Go to Login</button>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: "400px", margin: "4rem auto", padding: "2rem", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h2>Register</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label>Full Name</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }} />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }} />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }} />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Role</label>
        <select value={role} onChange={(e) => setRole(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }}>
          <option>Renewable Energy Planner</option>
          <option>GIS Analyst</option>
          <option>Project Manager</option>
          <option>Administrator</option>
        </select>
      </div>

      <button onClick={handleRegister} disabled={isLoading} style={{ width: "100%", padding: "0.6rem" }}>
        {isLoading ? "Registering..." : "Register"}
      </button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      <p style={{ marginTop: "1rem", textAlign: "center" }}>
        Already have an account?{" "}
        <button onClick={onSwitchToLogin} style={{ background: "none", border: "none", color: "blue", cursor: "pointer", textDecoration: "underline" }}>
          Login
        </button>
      </p>
    </div>
  );
}

export default RegisterPage;