import React from "react";
import { Wind } from "lucide-react";

export default function WindAnalysis() {

  return (
    <div className="page-content">

      <div className="page-title">
        <Wind />

        <div>
          <h1>Wind Analysis</h1>

          <p>
            Analyze wind speed, direction and wind
            energy potential.
          </p>
        </div>
      </div>

      <div className="analysis-cards">

        <div className="analysis-card">
          <span>Average Wind Speed</span>
          <strong>6.8</strong>
          <small>m/s</small>
        </div>

        <div className="analysis-card">
          <span>Best Wind Location</span>
          <strong>Jaisalmer</strong>
          <small>Rajasthan</small>
        </div>

        <div className="analysis-card">
          <span>Wind Potential</span>
          <strong>89%</strong>
          <small>Excellent</small>
        </div>

      </div>

      <div className="large-panel">

        <h3>Wind Speed Overview</h3>

        <div className="resource-chart wind-bars">

          {[45, 60, 70, 55, 78, 65, 88, 72, 92].map(
            (height, index) => (
              <i
                key={index}
                style={{ height: `${height}%` }}
              />
            )
          )}

        </div>

      </div>

    </div>
  );
}