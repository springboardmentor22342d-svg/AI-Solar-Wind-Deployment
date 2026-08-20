import { useAuth } from "./hooks/useAuth";
import LoginPage from "./pages/LoginPage";
import AnalysisPage from "./pages/AnalysisPage";
import "./App.css";

function App() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="app-shell">
      {isLoggedIn ? <AnalysisPage /> : <LoginPage />}
    </main>
  );
}



export default App;
