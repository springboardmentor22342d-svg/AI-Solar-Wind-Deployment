import React from "react";

export default function PotentialDistribution({ score = 0 }) {

  const suitabilityScore = Math.round(
    Number(score) || 0
  );

  // Calculate distribution percentages
  const excellent =
    suitabilityScore >= 80
      ? suitabilityScore
      : 0;

  const veryGood =
    suitabilityScore >= 65 && suitabilityScore < 80
      ? suitabilityScore
      : 0;

  const good =
    suitabilityScore >= 50 && suitabilityScore < 65
      ? suitabilityScore
      : 0;

  const moderate =
    suitabilityScore >= 35 && suitabilityScore < 50
      ? suitabilityScore
      : 0;

  const low =
    suitabilityScore > 0 && suitabilityScore < 35
      ? suitabilityScore
      : 0;


  return (
    <div
      className="potential-distribution"
      style={{
        padding: "10px",
      }}
    >

      {/* SCORE */}

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
          Current Site Potential
        </div>

        <strong
          style={{
            display: "block",
            fontSize: "32px",
            marginTop: "5px",
          }}
        >
          {suitabilityScore}%
        </strong>

      </div>


      {/* DISTRIBUTION */}

      <div>

        <DistributionRow
          label="Excellent"
          value={excellent}
        />

        <DistributionRow
          label="Very Good"
          value={veryGood}
        />

        <DistributionRow
          label="Good"
          value={good}
        />

        <DistributionRow
          label="Moderate"
          value={moderate}
        />

        <DistributionRow
          label="Low"
          value={low}
        />

      </div>


      {/* NO ANALYSIS */}

      {suitabilityScore === 0 && (

        <div
          style={{
            textAlign: "center",
            marginTop: "15px",
            fontSize: "11px",
            opacity: 0.6,
          }}
        >
          Analyze a location to view
          potential distribution.
        </div>

      )}

    </div>
  );
}


// ==========================================================
// DISTRIBUTION ROW
// ==========================================================

function DistributionRow({
  label,
  value,
}) {

  return (
    <div
      style={{
        marginBottom: "12px",
      }}
    >

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: "11px",
          marginBottom: "5px",
        }}
      >

        <span>
          {label}
        </span>

        <strong>
          {value}%
        </strong>

      </div>


      <div
        style={{
          width: "100%",
          height: "7px",
          borderRadius: "10px",
          background:
            "rgba(255,255,255,0.08)",
          overflow: "hidden",
        }}
      >

        <div
          style={{
            width: `${value}%`,
            height: "100%",
            borderRadius: "10px",
            background: "currentColor",
            transition:
              "width 0.5s ease",
          }}
        />

      </div>

    </div>
  );
}