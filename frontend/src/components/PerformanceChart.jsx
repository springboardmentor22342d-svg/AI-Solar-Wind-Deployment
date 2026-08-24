import React from "react";

export default function PerformanceChart({ analysis }) {

  const solar = Number(analysis?.avgSolar || 0);
  const wind = Number(analysis?.avgWind || 0);

  // ----------------------------------------------------------
  // Convert values into chart positions
  // ----------------------------------------------------------

  const maxSolar = 1000;
  const maxWind = 12;

  const solarHeight = Math.min(
    (solar / maxSolar) * 150,
    150
  );

  const windHeight = Math.min(
    (wind / maxWind) * 150,
    150
  );

  // ----------------------------------------------------------
  // Create visible lines based on real values
  // ----------------------------------------------------------

  const solarY = 190 - solarHeight;
  const windY = 190 - windHeight;

  return (
    <section className="panel performance-panel">

      <div className="panel-header">

        <h3>
          Performance Overview
        </h3>

        <select>
          <option>This Year</option>
          <option>Last Year</option>
        </select>

      </div>


      {/* ======================================================
          LEGEND
      ====================================================== */}

      <div className="chart-legend">

        <span className="solar-line">
          ● Solar Potential
          {" "}
          ({solar.toFixed(1)} W/m²)
        </span>

        <span className="wind-line">
          ● Wind Potential
          {" "}
          ({wind.toFixed(1)} m/s)
        </span>

      </div>


      {/* ======================================================
          CHART
      ====================================================== */}

      <div
        className="performance-chart"
        style={{
          width: "100%",
          overflow: "hidden",
        }}
      >

        <svg
          viewBox="0 0 600 220"
          width="100%"
          height="220"
          preserveAspectRatio="none"
        >

          {/* GRID */}

          <line
            x1="0"
            y1="190"
            x2="600"
            y2="190"
            stroke="rgba(255,255,255,0.15)"
          />

          <line
            x1="0"
            y1="145"
            x2="600"
            y2="145"
            stroke="rgba(255,255,255,0.08)"
          />

          <line
            x1="0"
            y1="100"
            x2="600"
            y2="100"
            stroke="rgba(255,255,255,0.08)"
          />

          <line
            x1="0"
            y1="55"
            x2="600"
            y2="55"
            stroke="rgba(255,255,255,0.08)"
          />


          {/* ==================================================
              SOLAR LINE
          ================================================== */}

          <polyline
            points={`
              0,${solarY}
              50,${solarY - 8}
              100,${solarY + 5}
              150,${solarY - 15}
              200,${solarY + 3}
              250,${solarY - 10}
              300,${solarY + 8}
              350,${solarY - 5}
              400,${solarY - 18}
              450,${solarY + 4}
              500,${solarY - 12}
              550,${solarY + 5}
              600,${solarY}
            `}
            fill="none"
            stroke="#f5a623"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />


          {/* ==================================================
              WIND LINE
          ================================================== */}

          <polyline
            points={`
              0,${windY}
              50,${windY + 8}
              100,${windY - 5}
              150,${windY + 12}
              200,${windY - 4}
              250,${windY + 6}
              300,${windY - 8}
              350,${windY + 5}
              400,${windY - 10}
              450,${windY + 7}
              500,${windY - 4}
              550,${windY + 9}
              600,${windY}
            `}
            fill="none"
            stroke="#4287ff"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />


          {/* ==================================================
              SOLAR POINT
          ================================================== */}

          <circle
            cx="300"
            cy={solarY - 1}
            r="5"
            fill="#f5a623"
          />


          {/* ==================================================
              WIND POINT
          ================================================== */}

          <circle
            cx="300"
            cy={windY - 1}
            r="5"
            fill="#4287ff"
          />

        </svg>

      </div>


      {/* ======================================================
          MONTHS
      ====================================================== */}

      <div className="months">

        <span>Jan</span>
        <span>Feb</span>
        <span>Mar</span>
        <span>Apr</span>
        <span>May</span>
        <span>Jun</span>
        <span>Jul</span>
        <span>Aug</span>
        <span>Sep</span>
        <span>Oct</span>
        <span>Nov</span>
        <span>Dec</span>

      </div>


      {/* ======================================================
          CURRENT VALUES
      ====================================================== */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: "15px",
          fontSize: "12px",
        }}
      >

        <div>
          <strong style={{ color: "#f5a623" }}>
            Solar
          </strong>

          <br />

          {solar > 0
            ? `${solar.toFixed(2)} W/m²`
            : "No solar data"}
        </div>


        <div
          style={{
            textAlign: "right",
          }}
        >

          <strong style={{ color: "#4287ff" }}>
            Wind
          </strong>

          <br />

          {wind > 0
            ? `${wind.toFixed(2)} m/s`
            : "No wind data"}

        </div>

      </div>

    </section>
  );
}