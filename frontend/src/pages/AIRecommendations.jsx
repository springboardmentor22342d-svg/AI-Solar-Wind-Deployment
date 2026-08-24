import React from "react";
import { Bot, Sparkles } from "lucide-react";

export default function AIRecommendations() {

  return (
    <div className="page-content">

      <div className="page-title">

        <Bot />

        <div>
          <h1>AI Recommendations</h1>

          <p>
            AI-powered recommendations for renewable
            energy deployment.
          </p>
        </div>

      </div>

      <div className="recommendation-panel">

        <Sparkles size={35} />

        <h2>
          Recommended Locations
        </h2>

        <p>
          Based on solar irradiance, wind speed,
          terrain and infrastructure availability,
          these locations show strong potential.
        </p>

        <div className="recommendation-list">

          <div>
            <strong>Kutch, Gujarat</strong>
            <span>92% suitability</span>
          </div>

          <div>
            <strong>Jaisalmer, Rajasthan</strong>
            <span>89% suitability</span>
          </div>

          <div>
            <strong>Anantapur, Andhra Pradesh</strong>
            <span>86% suitability</span>
          </div>

        </div>

      </div>

    </div>
  );
}