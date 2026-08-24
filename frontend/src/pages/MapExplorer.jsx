import React from "react";
import MapView from "../components/MapView";

export default function MapExplorer() {

  return (
    <div className="page-content">

      <div className="page-title">

        <div>
          <h1>Map Explorer</h1>

          <p>
            Explore renewable energy potential
            across different regions.
          </p>
        </div>

      </div>

      <MapView />

    </div>
  );
}