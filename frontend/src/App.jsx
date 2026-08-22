import { useState } from "react";
import { useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AnalysisPage from "./pages/AnalysisPage";
import Footer from "./components/Footer";
import "./App.css";

function App() {
  const { isLoggedIn, logoutUser } = useAuth();
  const [showRegister, setShowRegister] = useState(false);

  if (!isLoggedIn) {
    return showRegister ? (
      <RegisterPage onSwitchToLogin={() => setShowRegister(false)} />
    ) : (
      <LoginPage onSwitchToRegister={() => setShowRegister(true)} />
    );
  }

  return (
    <div>
      <div style={{ textAlign: "right", padding: "1rem" }}>
        <button onClick={logoutUser} style={{ padding: "0.4rem 0.8rem" }}>Logout</button>
      </div>
      <AnalysisPage />
      <Footer />
    </div>
  );
}

export default App;