import React, { useState } from "react";

export default function AIInsights({ analysis = {} }) {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ==========================================================
  // ASK AI
  // ==========================================================

  const handleAskAI = async () => {

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setError("");
    setAnswer("");
    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ai/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question.trim(),

            analysis: {
              village: analysis.village,
              district: analysis.district,
              state: analysis.state,

              latitude: analysis.latitude,
              longitude: analysis.longitude,

              solar: analysis.avgSolar,
              wind: analysis.avgWind,

              suitability:
                analysis.suitabilityScore,

              category:
                analysis.suitabilityCategory,

              solarEnergy:
                analysis.solarEnergy,

              windEnergy:
                analysis.windEnergy,

              totalEnergy:
                analysis.totalHybridEnergy,
            },
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `AI request failed: ${response.status}`
        );
      }

      const data = await response.json();

      setAnswer(
        data.answer ||
        data.response ||
        data.message ||
        "No AI response received."
      );

    } catch (err) {

      console.error(
        "ASK AI ERROR:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to AI service."
      );

    } finally {

      setLoading(false);

    }
  };


  // ==========================================================
  // ENTER KEY
  // ==========================================================

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      e.preventDefault();
      handleAskAI();
    }

  };


  return (

    <section className="panel ai-insights">

      {/* ====================================================
          HEADER
      ==================================================== */}

      <div className="panel-header">

        <div>

          <h3>
            AI Site Assistant
          </h3>

          <p>
            Ask questions about the analyzed location
          </p>

        </div>

      </div>


      {/* ====================================================
          LOCATION SUMMARY
      ==================================================== */}

      {analysis.latitude && analysis.longitude && (

        <div
          style={{
            padding: "10px",
            marginBottom: "12px",
            borderRadius: "8px",
            background:
              "rgba(255,255,255,0.04)",
            fontSize: "11px",
          }}
        >

          <strong>
            Current Site
          </strong>

          <div style={{ marginTop: "4px" }}>

            {analysis.village},{" "}
            {analysis.district},{" "}
            {analysis.state}

          </div>

          <div
            style={{
              marginTop: "3px",
              opacity: 0.6,
            }}
          >

            Solar:{" "}
            {Number(
              analysis.avgSolar || 0
            ).toFixed(2)}
            {" W/m²"}

            {" • "}

            Wind:{" "}
            {Number(
              analysis.avgWind || 0
            ).toFixed(2)}
            {" m/s"}

            {" • "}

            Suitability:{" "}
            {Number(
              analysis.suitabilityScore || 0
            ).toFixed(1)}
            %

          </div>

        </div>

      )}


      {/* ====================================================
          QUESTION INPUT
      ==================================================== */}

      <div
        style={{
          display: "flex",
          gap: "8px",
          padding: "10px",
        }}
      >

        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask about this site..."
          disabled={loading}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border:
              "1px solid rgba(255,255,255,0.12)",
            background:
              "rgba(255,255,255,0.05)",
            color: "inherit",
            outline: "none",
          }}
        />

        <button
          type="button"
          onClick={handleAskAI}
          disabled={loading}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            cursor: loading
              ? "not-allowed"
              : "pointer",
          }}
        >

          {loading
            ? "Thinking..."
            : "Ask AI"}

        </button>

      </div>


      {/* ====================================================
          ERROR
      ==================================================== */}

      {error && (

        <div
          style={{
            margin: "0 10px 10px",
            padding: "9px",
            borderRadius: "8px",
            background:
              "rgba(255,60,60,0.08)",
            color: "#ff7777",
            fontSize: "11px",
          }}
        >

          {error}

        </div>

      )}


      {/* ====================================================
          AI ANSWER
      ==================================================== */}

      {answer && (

        <div
          style={{
            margin: "0 10px 10px",
            padding: "12px",
            borderRadius: "10px",
            background:
              "rgba(255,255,255,0.04)",
            border:
              "1px solid rgba(255,255,255,0.08)",
            fontSize: "12px",
            lineHeight: "1.6",
          }}
        >

          <strong>
            AI Recommendation
          </strong>

          <p
            style={{
              marginTop: "8px",
              marginBottom: 0,
            }}
          >
            {answer}
          </p>

        </div>

      )}

    </section>
  );
}