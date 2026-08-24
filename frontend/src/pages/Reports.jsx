import React from "react";
import { FileText, Download } from "lucide-react";

export default function Reports() {

  return (
    <div className="page-content">

      <div className="page-title">

        <FileText />

        <div>
          <h1>Reports</h1>

          <p>
            Renewable energy analysis reports.
          </p>
        </div>

      </div>

      <div className="report-card">

        <FileText size={35} />

        <div>
          <h3>Site Analysis Report</h3>

          <p>
            Solar, wind, terrain and infrastructure
            assessment.
          </p>
        </div>

        <button>
          <Download size={16} />
          Download
        </button>

      </div>

      <div className="report-card">

        <FileText size={35} />

        <div>
          <h3>Regional Potential Report</h3>

          <p>
            Renewable energy potential by region.
          </p>
        </div>

        <button>
          <Download size={16} />
          Download
        </button>

      </div>

    </div>
  );
}