function AnalysisResults({
  result,
  latitude,
  longitude,
}) {
  if (!result) {
    return null;
  }

  // -----------------------------
  // Helper functions
  // -----------------------------

  const formatNumber = (value, decimals = 2) => {
    if (value === undefined || value === null) {
      return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return value;
    }

    return number.toFixed(decimals);
  };

  const formatCurrency = (value) => {
    if (value === undefined || value === null) {
      return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "N/A";
    }

    return `₹${number.toLocaleString("en-IN")}`;
  };

  const getValue = (value, fallback = "N/A") => {
    return value !== undefined && value !== null
      ? value
      : fallback;
  };

  // -----------------------------
  // Backend response sections
  // -----------------------------

  const solar = result.solar;
  const wind = result.wind;
  const evaluation = result.evaluation;
  const deployment = result.deployment;
  const technical = result.technical_feasibility;
  const energy = result.energy_yield;
  const financial = result.financial_metrics;

  return (
    <div className="results-dashboard">

      {/* =================================
          RESULTS HEADER
      ================================= */}

      <div className="results-title">
        <h2>ANALYSIS RESULTS</h2>

        <p>
          Renewable energy assessment for the
          selected location.
        </p>
      </div>


      <div className="result-grid">

        {/* =================================
            LOCATION
        ================================= */}

        <section className="result-card">
          <h3>📍 Location</h3>

          <div className="result-row">
            <span className="result-label">
              Latitude
            </span>

            <span className="result-value">
              {getValue(latitude)}
            </span>
          </div>

          <div className="result-row">
            <span className="result-label">
              Longitude
            </span>

            <span className="result-value">
              {getValue(longitude)}
            </span>
          </div>
        </section>


        {/* =================================
            RENEWABLE POTENTIAL
        ================================= */}

        <section className="result-card">
          <h3>☀️ Renewable Potential</h3>

          <div className="potential-grid">

            <div className="potential-item">
              <h4>Solar</h4>

              <strong>
                {typeof solar === "object"
                  ? getValue(
                      solar?.classification ??
                      solar?.class ??
                      solar?.rating
                    )
                  : getValue(solar)}
              </strong>
            </div>


            <div className="potential-item">
              <h4>Wind</h4>

              <strong>
                {typeof wind === "object"
                  ? getValue(
                      wind?.classification ??
                      wind?.wind_class ??
                      wind?.rating
                    )
                  : getValue(wind)}
              </strong>
            </div>


            <div className="potential-item">
              <h4>Deployment</h4>

              <strong>
                 {getValue(result.recommended_deployment)}
              </strong>
            </div>

          </div>
        </section>


        {/* =================================
            TECHNICAL ASSESSMENT
        ================================= */}

        <section className="result-card">
          <h3>⚙️ Technical Assessment</h3>

          <div className="result-row">
            <span className="result-label">
              Suitability Score
            </span>

              <span className="result-value">
      {getValue(
        result.site_suitability?.overall_score
      )}
    </span>
          </div>


          <div className="result-row">
            <span className="result-label">
              Technical Feasibility
            </span>

            <span className="result-value">
              {typeof technical === "object"
                ? technical?.technically_feasible === true
                  ? "Feasible"
                  : technical?.technically_feasible === false
                  ? "Not Feasible"
                  : getValue(
                      technical?.decision ??
                      technical?.status
                    )
                : getValue(technical)}
            </span>
          </div>


          {typeof technical === "object" && (
            <>
              <div className="result-row">
                <span className="result-label">
                  Technical Score
                </span>

                <span className="result-value">
                  {formatNumber(
                    technical?.soft_score ??
                    technical?.technical_score
                  )}
                </span>
              </div>


              <div className="result-row">
                <span className="result-label">
                  Decision
                </span>

                <span className="result-value">
                  {getValue(
                    technical?.decision ??
                    technical?.status
                  )}
                </span>
              </div>
            </>
          )}
        </section>


        {/* =================================
            ENERGY
        ================================= */}

        <section className="result-card">
          <h3>⚡ Energy</h3>

          <div className="result-row">
            <span className="result-label">
              Technology
            </span>

            <span className="result-value">
              {typeof energy === "object"
                ? getValue(energy?.technology)
                : "N/A"}
            </span>
          </div>


          <div className="result-row">
            <span className="result-label">
              Annual Energy Yield
            </span>

            <span className="result-value">
              {typeof energy === "object"
                ? energy?.total_annual_energy_mwh !==
                  undefined
                  ? `${formatNumber(
                      energy.total_annual_energy_mwh
                    )} MWh`
                  : energy?.total_annual_energy_gwh !==
                    undefined
                  ? `${formatNumber(
                      energy.total_annual_energy_gwh
                    )} GWh`
                  : "N/A"
                : getValue(energy)}
            </span>
          </div>


          {typeof energy === "object" &&
            energy?.total_annual_energy_gwh !==
              undefined && (
              <div className="result-row">
                <span className="result-label">
                  Annual Energy
                </span>

                <span className="result-value">
                  {formatNumber(
                    energy.total_annual_energy_gwh
                  )}{" "}
                  GWh
                </span>
              </div>
            )}
        </section>


        {/* =================================
            FINANCIAL
        ================================= */}

        <section className="result-card full-width">
          <h3>💰 Financial</h3>

          <div className="financial-grid">

            <div className="financial-item">
              <span>
                Project Cost
              </span>

              <strong>
                {formatCurrency(
                  financial?.estimated_project_cost
                )}
              </strong>
            </div>


            <div className="financial-item">
              <span>
                Annual Revenue
              </span>

              <strong>
                {formatCurrency(
                  financial?.annual_revenue
                )}
              </strong>
            </div>


            <div className="financial-item">
              <span>
                ROI
              </span>

              <strong>
                {financial?.roi !== undefined &&
                financial?.roi !== null
                  ? `${formatNumber(
                      financial.roi
                    )}%`
                  : "N/A"}
              </strong>
            </div>


            <div className="financial-item">
              <span>
                Payback Period
              </span>

              <strong>
                {financial?.payback_period !==
                  undefined &&
                financial?.payback_period !== null
                  ? `${formatNumber(
                      financial.payback_period
                    )} years`
                  : "N/A"}
              </strong>
            </div>

          </div>
        </section>


        {/* =================================
            RECOMMENDATION
        ================================= */}

        <section className="result-card full-width">
          <div className="recommendation">

            <h3>
              📋 Recommendation
            </h3>

            <p>
              {getValue(
                result?.recommendation_reason,
                "No recommendation information available."
              )}
            </p>

          </div>
        </section>

      </div>
    </div>
  );
}

export default AnalysisResults;