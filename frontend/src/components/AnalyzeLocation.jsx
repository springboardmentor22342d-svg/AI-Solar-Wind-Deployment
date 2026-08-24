import React, { useState } from "react";
import { analyzeLocation } from "../services/api";

const initialForm = {
  village: "",
  district: "",
  state: "",
  country: "",
  date: "",
};

export default function AnalyzeLocation({
  onAnalysisComplete,
}) {
  const [formData, setFormData] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ============================================================
  // HANDLE INPUT
  // ============================================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // ============================================================
  // ANALYZE LOCATION
  // ============================================================

  const handleAnalyze = async (e) => {
    e.preventDefault();

    setError("");

    const requiredFields = [
      "village",
      "district",
      "state",
      "country",
      "date",
    ];

    const missingField = requiredFields.find(
      (field) => !String(formData[field]).trim()
    );

    if (missingField) {
      setError(
        "Please fill Village/City, District, State, Country and Date."
      );
      return;
    }

    setLoading(true);

    try {
      // ========================================================
      // SEND LOCATION TO BACKEND
      // ========================================================

      const locationRequest = {
        village: formData.village.trim(),
        district: formData.district.trim(),
        state: formData.state.trim(),
        country: formData.country.trim(),
        date: formData.date,
      };

      console.log(
        "Sending location to backend:",
        locationRequest
      );

      // ========================================================
      // BACKEND RESPONSE
      // ========================================================

      const backendResult =
        await analyzeLocation(locationRequest);

      console.log(
        "BACKEND ANALYSIS RESULT:",
        backendResult
      );

      // ========================================================
      // LOCATION
      // ========================================================

      const backendLocation =
        backendResult?.location || {};

      const latitude = Number(
        backendLocation.latitude ??
          backendResult?.latitude ??
          0
      );

      const longitude = Number(
        backendLocation.longitude ??
          backendResult?.longitude ??
          0
      );

      // ========================================================
      // SOLAR FEATURES
      // ========================================================

      const solarFeatures =
        backendResult?.solar_features || {};

      const solarValue = Number(
        solarFeatures.solar_irradiance ?? 0
      );

      const temperature = Number(
        solarFeatures.temperature ?? 0
      );

      const humidity = Number(
        solarFeatures.relative_humidity ?? 0
      );

      // ========================================================
      // WIND FEATURES
      // ========================================================

      const windFeatures =
        backendResult?.wind_features || {};

      const windValue = Number(
        windFeatures.wind_speed ?? 0
      );

      const windCapacityFactor = Number(
        windFeatures.capacity_factor ?? 0
      );

      const windClass =
        windFeatures.wind_class ?? "";

      const windSiteClassification =
        windFeatures.site_classification ?? "";

      // ========================================================
      // SOLAR SCORE
      // NASA POWER SOLAR DATA IS APPROXIMATELY
      // 0-7 kWh/m²/day
      // ========================================================

      const solarScore = Math.min(
        Math.round((solarValue / 7) * 100),
        100
      );

      // ========================================================
      // WIND SCORE
      // ========================================================

      const windScore = Math.min(
        Math.round((windValue / 12) * 100),
        100
      );

      // ========================================================
      // ENERGY PREDICTION
      // ========================================================

      const energyPrediction =
        backendResult?.energy_prediction || {};

      const solarEnergy = Number(
        energyPrediction
          .solar_energy_kwh_per_year ?? 0
      );

      const windEnergy = Number(
        energyPrediction
          .wind_energy_kwh_per_year ?? 0
      );

      const totalHybridEnergy = Number(
        energyPrediction
          .total_hybrid_energy_kwh_per_year ?? 0
      );

      // ========================================================
      // EVALUATION
      // ========================================================

      const evaluation =
        backendResult?.evaluation || {};

      // IMPORTANT:
      // Backend uses overall_score

      const suitabilityScore = Number(
        evaluation.overall_score ??
          evaluation.score ??
          evaluation.suitability_score ??
          evaluation.total_score ??
          0
      );

      // ========================================================
      // CATEGORY SCORES
      // ========================================================

      const categoryScores =
        evaluation.category_scores || {};

      const evaluationScores = {
        renewableResources: Number(
          categoryScores.renewable_resources ?? 0
        ),

        terrain: Number(
          categoryScores.terrain ?? 0
        ),

        infrastructure: Number(
          categoryScores.infrastructure ?? 0
        ),

        environmental: Number(
          categoryScores.environmental ?? 0
        ),

        economic: Number(
          categoryScores.economic ?? 0
        ),
      };

      // ========================================================
      // SUITABILITY CATEGORY
      // ========================================================

      let suitabilityCategory = "No Analysis";

      if (suitabilityScore >= 80) {
        suitabilityCategory = "Excellent";
      } else if (suitabilityScore >= 65) {
        suitabilityCategory = "Very Good";
      } else if (suitabilityScore >= 50) {
        suitabilityCategory = "Good";
      } else if (suitabilityScore >= 35) {
        suitabilityCategory = "Moderate";
      } else if (suitabilityScore > 0) {
        suitabilityCategory = "Low";
      }

      // ========================================================
      // ESTIMATED CAPACITY
      // ========================================================

      const estimatedCapacity = Number(
        (
          (suitabilityScore / 100) *
          10
        ).toFixed(2)
      );

      // ========================================================
      // FINAL FRONTEND RESULT
      // ========================================================

      const finalResult = {
        // LOCATION
        village: formData.village,
        district: formData.district,
        state: formData.state,
        country: formData.country,
        date: formData.date,

        // COORDINATES
        latitude,
        longitude,

        displayName:
          backendLocation.display_name ??
          `${formData.village}, ${formData.district}, ${formData.state}`,

        // SOLAR
        avgSolar: Number(
          solarValue.toFixed(2)
        ),

        // WIND
        avgWind: Number(
          windValue.toFixed(2)
        ),

        // WEATHER
        temperature: Number(
          temperature.toFixed(2)
        ),

        humidity: Number(
          humidity.toFixed(2)
        ),

        // SCORES
        solarScore,
        windScore,

        suitabilityScore,
        suitabilityCategory,

        // EVALUATION BREAKDOWN
        evaluationScores,

        // WIND ASSESSMENT
        windCapacityFactor,
        windClass,
        windSiteClassification,

        // ENERGY
        solarEnergy,
        windEnergy,
        totalHybridEnergy,

        // CAPACITY
        estimatedCapacity,

        // COMPLETE BACKEND DATA
        backendResult,

        // INDIVIDUAL BACKEND SECTIONS
        solarFeatures,
        windFeatures,
        energyPrediction,
        evaluation,

        forecasting:
          backendResult?.forecasting || {},

        optimization:
          backendResult?.optimization || {},

        analyzedAt:
          new Date().toISOString(),
      };

      // ========================================================
      // DEBUG
      // ========================================================

      console.log(
        "FINAL FRONTEND RESULT:",
        finalResult
      );

      console.log(
        "FINAL SOLAR:",
        finalResult.avgSolar
      );

      console.log(
        "FINAL WIND:",
        finalResult.avgWind
      );

      console.log(
        "FINAL SUITABILITY:",
        finalResult.suitabilityScore
      );

      console.log(
        "EVALUATION SCORES:",
        finalResult.evaluationScores
      );

      // ========================================================
      // SAVE HISTORY
      // ========================================================

      const existingHistory =
        JSON.parse(
          localStorage.getItem(
            "analysisHistory"
          )
        ) || [];

      const updatedHistory = [
        ...existingHistory,
        finalResult,
      ];

      localStorage.setItem(
        "analysisHistory",
        JSON.stringify(
          updatedHistory
        )
      );

      // ========================================================
      // SEND TO DASHBOARD
      // ========================================================

      if (
        typeof onAnalysisComplete ===
        "function"
      ) {
        onAnalysisComplete(
          finalResult
        );
      }

      setError("");
    } catch (err) {
      console.error(
        "ANALYSIS ERROR:",
        err
      );

      setError(
        err?.message ||
          "Unable to analyze this location."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // UI
  // ============================================================

  return (
    <form
      className="analyze-location"
      onSubmit={handleAnalyze}
    >
      <div className="analyze-title">
        <h2>
          Analyze New Location
        </h2>

        <p>
          Enter a location to calculate
          solar, wind and site potential.
        </p>
      </div>

      <div className="form-group">
        <label>
          Village / City
        </label>

        <input
          type="text"
          name="village"
          value={formData.village}
          onChange={handleChange}
          placeholder="e.g. Nalgonda"
        />
      </div>

      <div className="form-group">
        <label>
          District
        </label>

        <input
          type="text"
          name="district"
          value={formData.district}
          onChange={handleChange}
          placeholder="e.g. Nalgonda"
        />
      </div>

      <div className="form-group">
        <label>
          State
        </label>

        <input
          type="text"
          name="state"
          value={formData.state}
          onChange={handleChange}
          placeholder="e.g. Telangana"
        />
      </div>

      <div className="form-group">
        <label>
          Country
        </label>

        <input
          type="text"
          name="country"
          value={formData.country}
          onChange={handleChange}
          placeholder="e.g. India"
        />
      </div>

      <div className="form-group">
        <label>
          Analysis Date
        </label>

        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
        />
      </div>

      <button
        type="submit"
        className="analyze-button"
        disabled={loading}
      >
        {loading
          ? "Analyzing..."
          : "Analyze Site →"}
      </button>

      {error && (
        <div
          style={{
            gridColumn: "1 / -1",
            marginTop: "5px",
            padding: "8px 10px",
            borderRadius: "7px",
            background:
              "rgba(255,60,60,0.08)",
            border:
              "1px solid rgba(255,80,80,0.25)",
            color: "#ff7777",
            fontSize: "10px",
          }}
        >
          {error}
        </div>
      )}
    </form>
  );
}