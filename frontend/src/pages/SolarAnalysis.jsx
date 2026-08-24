import React from "react";
import { Sun } from "lucide-react";

export default function SolarAnalysis() {

  return (
    <div className="page-content">

      <div className="page-title">
        <Sun />
        <div>
          <h1>Solar Analysis</h1>
          <p>
            Analyze solar irradiance and photovoltaic
            potential across locations.
          </p>
        </div>
      </div>

      <div className="analysis-cards">

        <div className="analysis-card">
          <span>Average Solar Irradiance</span>
          <strong>5.21</strong>
          <small>kWh/m²/day</small>
        </div>

        <div className="analysis-card">
          <span>Best Solar Location</span>
          <strong>Kutch</strong>
          <small>Gujarat</small>
        </div>

        <div className="analysis-card">
          <span>Solar Potential</span>
          <strong>92%</strong>
          <small>Excellent</small>
        </div>

      </div>

      <div className="large-panel">

        <h3>Solar Resource Overview</h3>

        <div className="resource-chart">

          {[50, 65, 58, 75, 82, 70, 90, 78, 94].map(
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