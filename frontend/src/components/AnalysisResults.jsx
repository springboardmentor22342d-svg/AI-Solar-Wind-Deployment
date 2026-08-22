import LocationMap from "./LocationMap";

function Section({ title, children }) {
  return (
    <section className="result-section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

function Row({ label, value }) {
  return (
    <div className="result-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Explanation({ text }) {
  if (!text) return null;
  return (
    <p className="result-explanation">
      {text}
    </p>
  );
}

function AnalysisResults({ data }) {
  if (!data.site_valid) {
    return (
      <div className="warning-panel">
        <h3>Location Not Suitable</h3>
        <p>{data.message}</p>
        <ul>
          {Array.isArray(data.validity_reasons) &&
            data.validity_reasons.map((reason, i) => <li key={i}>{reason}</li>)}
        </ul>
      </div>
    );
  }

  return (
    <div className="analysis-results">
      <button
        className="primary-button print-hide"
        onClick={() => window.print()}
        style={{ marginBottom: "1rem" }}
      >
        Download Site Report (PDF)
      </button>

      <Section title="SITE ANALYSIS">
        <Row label="Latitude" value={data.latitude} />
        <Row label="Longitude" value={data.longitude} />
      </Section>

      <LocationMap latitude={data.latitude} longitude={data.longitude} />

      <Section title="RENEWABLE POTENTIAL">
        <Row label="Solar Irradiance" value={`${data.raw_features.solar_irradiance.toFixed(2)} kWh/m²/day`} />
        <Row label="Solar Rating" value={data.solar_rating} />
        <Row label="Wind Speed" value={`${data.raw_features.wind_speed_100m.toFixed(2)} m/s`} />
        <Row label="Wind Rating" value={data.wind_rating} />
        <Row label="Recommended Deployment" value={data.recommended_deployment.deployment} />
        <Row label="Confidence" value={`${data.recommended_deployment.confidence}%`} />
        <Explanation text={data.recommended_deployment.reason} />
        <p className="basis-note">
          <strong>Used for energy & cost analysis below:</strong> {data.analysis_basis}
        </p>
      </Section>

      <Section title="TECHNICAL ASSESSMENT">
        <Row label="Suitability Score" value={`${data.site_suitability.suitability_score} / 100`} />
        <Row label="Suitability Category" value={data.site_suitability.recommendation} />
        <Row label="Technical Feasibility" value={`${data.technical_feasibility.technical_feasibility_pct}%`} />
        <Row label="Feasibility Status" value={data.technical_feasibility.overall_status} />
      </Section>

      <Section title="ENERGY">
        <Row
          label="Annual Energy Yield"
          value={`${(data.energy_yield.annual_energy_kwh || data.energy_yield.total_annual_energy_kwh || 0).toLocaleString()} kWh/year`}
        />
        <Row label="Yield Rating" value={data.energy_yield_rating.rating} />
        <Explanation text={data.energy_yield_rating.explanation} />
        <Explanation text={data.energy_yield.explanation} />
      </Section>

      <Section title="FINANCIAL">
        <Row label="Project Cost" value={`₹${data.financial_metrics.estimated_project_cost_inr.toLocaleString()}`} />
        <Row label="Annual Revenue" value={`₹${data.financial_metrics.annual_revenue_inr.toLocaleString()}`} />
        <Row label="ROI" value={`${data.financial_metrics.roi_pct}%`} />
        <Row label="Payback Period" value={`${data.financial_metrics.payback_period_years} years`} />
      </Section>
    </div>
  );
}

export default AnalysisResults;