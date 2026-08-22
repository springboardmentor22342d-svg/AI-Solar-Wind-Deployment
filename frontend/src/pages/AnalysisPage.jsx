import { useState } from "react";
import { runAnalysis } from "../api/analysis";
import AnalysisResults from "../components/AnalysisResults";
import GuidelinesPanel from "../components/GuidelinesPanel";
import { useAuth } from "../context/AuthContext";

function AnalysisPage() {
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const { token } = useAuth();

  const handleAnalyse = async () => {
    setStatus("loading");
    setErrorMessage("");

    try {
      const data = await runAnalysis(latitude, longitude, "", token);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err.message || "Something went wrong. Please try again.");
      setStatus("error");
    }
  };

  return (
    <div className="analysis-view">
      <header className="analysis-header">
        <div>
          <p className="eyebrow">Site suitability workspace</p>
          <h1>Solar & Wind Deployment Intelligence</h1>
        </div>
      </header>

      <section className="analysis-layout">
        <aside className="control-panel">
          <GuidelinesPanel />

          <div className="input-panel">
            <h2>Analyse a Location</h2>

            <label className="field">
              <span>Latitude</span>
              <input
                type="number"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value.replace(/[eE]/g, ""))}
              />
            </label>

            <label className="field">
              <span>Longitude</span>
              <input
                type="number"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value.replace(/[eE]/g, ""))}
              />
            </label>

            <button
              className="primary-button"
              onClick={handleAnalyse}
              disabled={status === "loading"}
            >
              {status === "loading" ? "Analysing site..." : "Analyse"}
            </button>

            {status === "error" && <p className="error-message">{errorMessage}</p>}
          </div>
        </aside>

        <section className="results-panel">
          {status === "idle" && (
            <div className="empty-state">
              <h2>Enter coordinates to begin</h2>
              <p>
                The analysis result will show renewable potential, technical
                feasibility, energy yield, financial metrics, and a map.
              </p>
            </div>
          )}

          {status === "loading" && (
            <div className="empty-state">
              <h2>Analysing site...</h2>
              <p>Fetching resource, terrain, environmental, and financial indicators.</p>
            </div>
          )}

          {status === "success" && result && <AnalysisResults data={result} />}
        </section>
      </section>
    </div>
  );
}

export default AnalysisPage;
