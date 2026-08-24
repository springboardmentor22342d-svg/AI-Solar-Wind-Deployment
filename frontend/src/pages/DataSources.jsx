import React from "react";
import { Database } from "lucide-react";

export default function DataSources() {

  const sources = [
    ["NASA POWER", "Solar and climate data"],
    ["Global Wind Atlas", "Wind resource data"],
    ["SRTM DEM", "Elevation and terrain"],
    ["OpenStreetMap", "Infrastructure and roads"]
  ];

  return (
    <div className="page-content">

      <div className="page-title">

        <Database />

        <div>
          <h1>Data Sources</h1>

          <p>
            Data sources used by the platform.
          </p>
        </div>

      </div>

      <div className="source-grid">

        {sources.map(([name, description]) => (

          <div
            className="source-card"
            key={name}
          >

            <Database size={25} />

            <h3>{name}</h3>

            <p>{description}</p>

            <span>Connected</span>

          </div>

        ))}

      </div>

    </div>
  );
}