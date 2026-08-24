import React from "react";
import { Bell, AlertTriangle } from "lucide-react";

export default function Alerts() {

  return (
    <div className="page-content">

      <div className="page-title">

        <Bell />

        <div>
          <h1>Alerts</h1>

          <p>
            Important platform and site alerts.
          </p>
        </div>

      </div>

      <div className="alert-card warning">

        <AlertTriangle />

        <div>
          <strong>
            High solar potential detected
          </strong>

          <p>
            Kutch, Gujarat currently has a
            92% suitability score.
          </p>
        </div>

      </div>

      <div className="alert-card">

        <Bell />

        <div>
          <strong>
            New wind dataset available
          </strong>

          <p>
            Updated wind resource information
            is available.
          </p>
        </div>

      </div>

    </div>
  );
}