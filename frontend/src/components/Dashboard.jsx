import React from 'react';
import { 
  Sun, 
  Wind, 
  Zap, 
  DollarSign, 
  CheckCircle2, 
  XCircle, 
  MapPin, 
  ShieldCheck, 
  TrendingUp, 
  Clock, 
  Cpu,
  AlertOctagon
} from 'lucide-react';

export default function Dashboard({ data }) {
  if (!data) return null;

  const {
    location = {},
    features = {},
    site_score = {},
    feasibility = {},
    deployment = {},
    deployment_plan = {},
    energy_estimation = {},
    financial = {},
    ml_analysis = {}
  } = data;

  const recType = (deployment.recommendation || 'Solar').toLowerCase();
  const badgeClass = recType === 'unfeasible' || recType === 'not recommended'
    ? 'badge-unfeasible' 
    : recType === 'hybrid' 
    ? 'badge-hybrid' 
    : recType === 'wind' 
    ? 'badge-wind' 
    : 'badge-solar';

  const failures = feasibility.constraint_summary?.hard_constraints?.failures || [];

  return (
    <div className="dashboard-grid">
      
      {/* 1. SITE ANALYSIS */}
      <div className="dash-section">
        <h3 className="section-title">
          <MapPin size={20} color="#0284c7" />
          SITE ANALYSIS
        </h3>
        <div className="metrics-row">
          <div className="kpi-card">
            <div className="kpi-label">Latitude</div>
            <div className="kpi-value">{location.latitude?.toFixed(4)}°</div>
            <div className="kpi-subtext">Geographic Position</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Longitude</div>
            <div className="kpi-value">{location.longitude?.toFixed(4)}°</div>
            <div className="kpi-subtext">Geographic Position</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Land Area</div>
            <div className="kpi-value">{features.land_area || 0} <span style={{ fontSize: '0.9rem' }}>Acres</span></div>
            <div className="kpi-subtext">{location.is_ocean ? 'Open Ocean Zone' : 'Available Plot Size'}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Elevation</div>
            <div className="kpi-value">{features.elevation || 0} <span style={{ fontSize: '0.9rem' }}>m</span></div>
            <div className="kpi-subtext">Terrain Elevation</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Grid Distance</div>
            <div className="kpi-value">{features.distance_to_grid || 1.8} <span style={{ fontSize: '0.9rem' }}>km</span></div>
            <div className="kpi-subtext">Nearest Substation</div>
          </div>
        </div>
      </div>

      {/* 2. RENEWABLE POTENTIAL */}
      <div className="dash-section">
        <h3 className="section-title">
          <Sun size={20} color="#f59e0b" />
          RENEWABLE POTENTIAL & RECOMMENDATION
        </h3>
        
        <div className="recommendation-card" style={recType === 'unfeasible' ? { background: 'rgba(239, 68, 68, 0.08)', borderColor: 'rgba(239, 68, 68, 0.3)' } : {}}>
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Recommended Technology</div>
            <div className={`recommendation-badge ${badgeClass}`}>
              {deployment.recommendation || 'Hybrid'}
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '8px' }}>
              {deployment.reason || 'Optimal site suitability for deployment.'}
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div className="kpi-label">Confidence Score</div>
            <div className="kpi-value" style={{ color: recType === 'unfeasible' ? '#ef4444' : 'var(--hybrid-emerald)' }}>
              {deployment.confidence_score !== undefined ? `${deployment.confidence_score}%` : '0%'}
            </div>
          </div>
        </div>

        <div className="metrics-row">
          <div className="kpi-card">
            <div className="kpi-label"><Sun size={16} color="#f59e0b" /> Solar Resource</div>
            <div className="kpi-value" style={{ color: '#f59e0b' }}>
              {deployment.solar?.solar_class || 'Good'}
            </div>
            <div className="kpi-subtext">{features.solar_irradiance} kWh/m²/day</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label"><Wind size={16} color="#06b6d4" /> Wind Resource</div>
            <div className="kpi-value" style={{ color: '#06b6d4' }}>
              {deployment.wind?.wind_class || 'Good'}
            </div>
            <div className="kpi-subtext">{features.wind_speed} m/s @ 10m</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label"><Cpu size={16} color="#93c5fd" /> ML Solar Forecast</div>
            <div className="kpi-value" style={{ color: '#93c5fd' }}>
              {ml_analysis.predicted_solar_irradiance || features.solar_irradiance}
            </div>
            <div className="kpi-subtext">Tuned RF Model Prediction</div>
          </div>
        </div>
      </div>

      {/* 3. TECHNICAL ASSESSMENT */}
      <div className="dash-section">
        <h3 className="section-title">
          <ShieldCheck size={20} color="#10b981" />
          TECHNICAL ASSESSMENT & FEASIBILITY
        </h3>
        
        {failures.length > 0 && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '14px 18px', borderRadius: '10px', marginBottom: '16px', color: '#fca5a5', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '700', color: '#ef4444', marginBottom: '4px' }}>
              <AlertOctagon size={18} /> Hard Constraint Violations Detected:
            </div>
            <ul style={{ paddingLeft: '24px', margin: '4px 0 0 0' }}>
              {failures.map((fail, i) => (
                <li key={i}>{fail}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="metrics-row">
          <div className="kpi-card">
            <div className="kpi-label">Suitability Score</div>
            <div className="kpi-value" style={{ color: location.is_ocean ? '#ef4444' : '#38bdf8' }}>
              {site_score.overall_suitability_score || site_score.overall_score || 0}%
            </div>
            <div className="kpi-subtext">Category: {site_score.suitability_category || 'Unfeasible'}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Feasibility Status</div>
            <div className="kpi-value" style={{ fontSize: '1.2rem', color: feasibility.technical_feasible ? '#10b981' : '#ef4444' }}>
              {feasibility.technical_feasible ? (
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={20} /> Feasible
                </span>
              ) : (
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                  <XCircle size={20} /> Unfeasible
                </span>
              )}
            </div>
            <div className="kpi-subtext">{feasibility.recommendation || 'Technical constraint check'}</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Feasibility Score</div>
            <div className="kpi-value">{feasibility.feasibility_score || 0}/100</div>
            <div className="kpi-subtext">Soft Constraints Passed</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Planned Capacity</div>
            <div className="kpi-value">{deployment_plan.recommended_capacity_kw || 0} <span style={{ fontSize: '0.9rem' }}>kW</span></div>
            <div className="kpi-subtext">Recommended Sizing</div>
          </div>
        </div>
      </div>

      {/* 4. ENERGY YIELD */}
      <div className="dash-section">
        <h3 className="section-title">
          <Zap size={20} color="#38bdf8" />
          ANNUAL ENERGY YIELD ESTIMATION
        </h3>
        <div className="metrics-row">
          <div className="kpi-card">
            <div className="kpi-label">Annual Solar Generation</div>
            <div className="kpi-value">{Number(energy_estimation.annual_solar_energy_kwh || 0).toLocaleString()} <span style={{ fontSize: '0.8rem' }}>kWh</span></div>
            <div className="kpi-subtext">Solar PV Output</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Annual Wind Generation</div>
            <div className="kpi-value">{Number(energy_estimation.annual_wind_energy_kwh || 0).toLocaleString()} <span style={{ fontSize: '0.8rem' }}>kWh</span></div>
            <div className="kpi-subtext">Turbine Output</div>
          </div>
          <div className="kpi-card" style={{ borderColor: 'var(--wind-cyan)', background: 'rgba(6, 182, 212, 0.08)' }}>
            <div className="kpi-label"><Zap size={16} color="#06b6d4" /> Total Energy Yield</div>
            <div className="kpi-value" style={{ color: '#06b6d4' }}>
              {Number(energy_estimation.total_annual_energy_kwh || 0).toLocaleString()} <span style={{ fontSize: '0.9rem' }}>kWh/yr</span>
            </div>
            <div className="kpi-subtext">Combined Generation</div>
          </div>
        </div>
      </div>

      {/* 5. FINANCIAL ANALYSIS */}
      <div className="dash-section">
        <h3 className="section-title">
          <DollarSign size={20} color="#10b981" />
          FINANCIAL & INVESTMENT ANALYSIS
        </h3>
        <div className="metrics-row">
          <div className="kpi-card">
            <div className="kpi-label">Estimated Project Cost</div>
            <div className="kpi-value">${Number(financial.estimated_project_cost || 0).toLocaleString()}</div>
            <div className="kpi-subtext">CAPEX + Installation</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label">Annual Revenue</div>
            <div className="kpi-value" style={{ color: '#10b981' }}>${Number(financial.annual_revenue || 0).toLocaleString()}</div>
            <div className="kpi-subtext">OPEX Generation Income</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label"><TrendingUp size={16} color="#10b981" /> Return on Investment (ROI)</div>
            <div className="kpi-value" style={{ color: '#10b981' }}>{financial.roi}%</div>
            <div className="kpi-subtext">Annual Financial Return</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-label"><Clock size={16} color="#f59e0b" /> Payback Period</div>
            <div className="kpi-value" style={{ color: '#f59e0b' }}>{financial.payback_period} {financial.payback_period !== 'N/A' && <span style={{ fontSize: '0.9rem' }}>Years</span>}</div>
            <div className="kpi-subtext">Capital Amortization</div>
          </div>
        </div>
      </div>

    </div>
  );
}
