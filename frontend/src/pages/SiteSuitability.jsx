import React from "react";
import SiteSuitabilityCard from "../components/SiteSuitability";

export default function SiteSuitabilityPage() {

  return (
    <div className="page-content">

      <div className="page-title">
        <div>
          <h1>Site Suitability</h1>

          <p>
            Evaluate locations using solar, wind,
            terrain and infrastructure factors.
          </p>
        </div>
      </div>

      <SiteSuitabilityCard />

    </div>
  );
}