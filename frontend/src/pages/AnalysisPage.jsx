import { useState } from "react";
import { analyseLocation } from "../services/analysisService";
import AnalysisResults from "../components/AnalysisResults";
import MapView from "../components/MapView";

function AnalysisPage() {
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalysis = async (event) => {
    event.preventDefault();

    // Prevent repeated submissions
    if (loading) {
      return;
    }

    setError("");
    setResult(null);

    setLoading(true);

    try {
      // Backend is responsible for authoritative validation
      const data = await analyseLocation(
        latitude,
        longitude
      );

      setResult(data);
    } catch (err) {
      console.error("Analysis error:", err);

      // Display backend/network error in a user-friendly way
      setError(
        err.message ||
          "Unable to complete the site analysis. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleMapLocationSelect = (lat, lng) => {
    setLatitude(lat.toFixed(6));
    setLongitude(lng.toFixed(6));

    // Remove old analysis when a new location is selected
    setResult(null);
    setError("");
  };

  return (
    <div className="app-container">
      <div className="page-container">

        {/* ================================
            PAGE HEADER
        ================================= */}

        <div className="page-header">
          <h1>
            Solar & Wind Deployment Intelligence
          </h1>

          <p>
            Analyze renewable energy potential for a
            selected location.
          </p>
        </div>

        {/* ================================
            LOCATION INPUT
        ================================= */}

        <div className="analysis-card">
          <h2>Site Analysis</h2>

          <form
            className="analysis-form"
            onSubmit={handleAnalysis}
          >

            {/* Latitude */}

            <div className="form-group">
              <label htmlFor="latitude">
                Latitude
              </label>

              <input
                id="latitude"
                type="number"
                step="any"
                value={latitude}
                onChange={(event) =>
                  setLatitude(event.target.value)
                }
                placeholder="Enter latitude"
                required
                disabled={loading}
              />
            </div>

            {/* Longitude */}

            <div className="form-group">
              <label htmlFor="longitude">
                Longitude
              </label>

              <input
                id="longitude"
                type="number"
                step="any"
                value={longitude}
                onChange={(event) =>
                  setLongitude(event.target.value)
                }
                placeholder="Enter longitude"
                required
                disabled={loading}
              />
            </div>

            {/* Analyse Button */}

            <button
              className="analyse-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Analysing site..."
                : "Analyse Site"}
            </button>

          </form>
        </div>

        {/* ================================
            MAP
        ================================= */}

        <MapView
          latitude={latitude}
          longitude={longitude}
          onLocationSelect={handleMapLocationSelect}
        />

        {/* ================================
            LOADING STATE
        ================================= */}

        {loading && (
          <div className="loading-card">
            <h3>Analysing site...</h3>

            <p>
              Please wait while the renewable energy
              assessment is being performed.
            </p>
          </div>
        )}

        {/* ================================
            ERROR STATE
        ================================= */}

        {error && !loading && (
          <div className="error-card">
            <h3>Analysis Failed</h3>

            <p>{error}</p>
          </div>
        )}

        {/* ================================
            SUCCESS / RESULTS
        ================================= */}

        {result && !loading && !error && (
          <AnalysisResults
            result={result}
            latitude={latitude}
            longitude={longitude}
          />
        )}

      </div>
    </div>
  );
}

export default AnalysisPage;