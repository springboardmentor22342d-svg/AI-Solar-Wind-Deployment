import React from "react";

export default function SiteSuitability({
  score = 0,
  solarScore = 0,
  windScore = 0,
  evaluationScores = {},
}) {
  const suitabilityScore = Math.round(
    Number(score) || 0
  );

  const solar = Math.min(
    Math.max(
      Math.round(Number(solarScore) || 0),
      0
    ),
    100
  );

  const wind = Math.min(
    Math.max(
      Math.round(Number(windScore) || 0),
      0
    ),
    100
  );

  // ==========================================================
  // CATEGORY
  // ==========================================================

  let category = "No Analysis";

  if (suitabilityScore >= 80) {
    category = "Excellent";
  } else if (suitabilityScore >= 65) {
    category = "Very Good";
  } else if (suitabilityScore >= 50) {
    category = "Good";
  } else if (suitabilityScore >= 35) {
    category = "Moderate";
  } else if (suitabilityScore > 0) {
    category = "Low";
  }

  // ==========================================================
  // CIRCULAR PROGRESS
  // ==========================================================

  const radius = 62;

  const circumference =
    2 * Math.PI * radius;

  const progress = Math.min(
    Math.max(suitabilityScore, 0),
    100
  );

  const offset =
    circumference -
    (progress / 100) *
      circumference;

  // ==========================================================
  // EVALUATION VALUES
  // ==========================================================

  const renewableResources = Math.min(
    Math.max(
      Number(
        evaluationScores.renewableResources
      ) || 0,
      0
    ),
    100
  );

  const terrain = Math.min(
    Math.max(
      Number(
        evaluationScores.terrain
      ) || 0,
      0
    ),
    100
  );

  const infrastructure = Math.min(
    Math.max(
      Number(
        evaluationScores.infrastructure
      ) || 0,
      0
    ),
    100
  );

  const environmental = Math.min(
    Math.max(
      Number(
        evaluationScores.environmental
      ) || 0,
      0
    ),
    100
  );

  const economic = Math.min(
    Math.max(
      Number(
        evaluationScores.economic
      ) || 0,
      0
    ),
    100
  );

  const evaluationItems = [
    {
      label: "Renewable Resources",
      value: renewableResources,
    },
    {
      label: "Terrain",
      value: terrain,
    },
    {
      label: "Infrastructure",
      value: infrastructure,
    },
    {
      label: "Environmental",
      value: environmental,
    },
    {
      label: "Economic",
      value: economic,
    },
  ];

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div
      className="site-suitability"
      style={{
        padding: "10px",
      }}
    >
      {/* ====================================================
          MAIN SCORE
      ==================================================== */}

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            position: "relative",
            width: "160px",
            height: "160px",
          }}
        >
          <svg
            width="160"
            height="160"
            viewBox="0 0 160 160"
          >
            <circle
              cx="80"
              cy="80"
              r={radius}
              fill="none"
              stroke="currentColor"
              strokeWidth="12"
              opacity="0.08"
            />

            <circle
              cx="80"
              cy="80"
              r={radius}
              fill="none"
              stroke="currentColor"
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={
                circumference
              }
              strokeDashoffset={offset}
              transform="rotate(-90 80 80)"
            />
          </svg>

          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <strong
              style={{
                fontSize: "34px",
              }}
            >
              {suitabilityScore}%
            </strong>

            <span
              style={{
                fontSize: "11px",
                opacity: 0.65,
              }}
            >
              Suitability
            </span>
          </div>
        </div>
      </div>

      {/* ====================================================
          CATEGORY
      ==================================================== */}

      <div
        style={{
          textAlign: "center",
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            opacity: 0.6,
          }}
        >
          Site Classification
        </div>

        <strong
          style={{
            display: "block",
            marginTop: "5px",
            fontSize: "20px",
          }}
        >
          {category}
        </strong>
      </div>

      {/* ====================================================
          SOLAR POTENTIAL
      ==================================================== */}

      <div
        style={{
          marginBottom: "14px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "6px",
            fontSize: "12px",
          }}
        >
          <span>
            Solar Potential
          </span>

          <strong>
            {solar}%
          </strong>
        </div>

        <div
          style={{
            width: "100%",
            height: "8px",
            borderRadius: "10px",
            background:
              "rgba(255,255,255,0.08)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${solar}%`,
              height: "100%",
              borderRadius: "10px",
              background: "#f5a623",
              transition:
                "width 0.5s ease",
            }}
          />
        </div>
      </div>

      {/* ====================================================
          WIND POTENTIAL
      ==================================================== */}

      <div
        style={{
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "6px",
            fontSize: "12px",
          }}
        >
          <span>
            Wind Potential
          </span>

          <strong>
            {wind}%
          </strong>
        </div>

        <div
          style={{
            width: "100%",
            height: "8px",
            borderRadius: "10px",
            background:
              "rgba(255,255,255,0.08)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${wind}%`,
              height: "100%",
              borderRadius: "10px",
              background: "#4287ff",
              transition:
                "width 0.5s ease",
            }}
          />
        </div>
      </div>

      {/* ====================================================
          EVALUATION BREAKDOWN
      ==================================================== */}

      <div
        style={{
          marginTop: "20px",
          paddingTop: "16px",
          borderTop:
            "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div
          style={{
            fontSize: "13px",
            fontWeight: "600",
            marginBottom: "14px",
          }}
        >
          Evaluation Breakdown
        </div>

        {evaluationItems.map(
          (item) => (
            <div
              key={item.label}
              style={{
                marginBottom: "12px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  fontSize: "11px",
                  marginBottom: "5px",
                }}
              >
                <span>
                  {item.label}
                </span>

                <strong>
                  {item.value.toFixed(0)}%
                </strong>
              </div>

              <div
                style={{
                  width: "100%",
                  height: "6px",
                  borderRadius: "10px",
                  background:
                    "rgba(255,255,255,0.08)",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${item.value}%`,
                    height: "100%",
                    borderRadius: "10px",
                    background: "#6c8cff",
                    transition:
                      "width 0.5s ease",
                  }}
                />
              </div>
            </div>
          )
        )}
      </div>

      {/* ====================================================
          NO ANALYSIS
      ==================================================== */}

      {suitabilityScore === 0 && (
        <div
          style={{
            textAlign: "center",
            marginTop: "15px",
            fontSize: "11px",
            opacity: 0.6,
          }}
        >
          Analyze a location to calculate
          site suitability.
        </div>
      )}
    </div>
  );
}