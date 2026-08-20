import React, { useState } from 'react';
import { analysisService } from '../api/analysis';
import MapLocator from '../components/MapLocator';
import MonthlyYieldChart from '../components/MonthlyYieldChart';
import ElevationProfileChart from '../components/ElevationProfileChart';
import SavedProjectsTable from '../components/SavedProjectsTable';
import { Target, Leaf, Mountain, Navigation, Compass, Zap, Activity, Info, BarChart2, Briefcase, Download } from 'lucide-react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { useRef } from 'react';

export default function SiteAnalysisPage() {
  const [formData, setFormData] = useState({
    site_name: '',
    latitude: '',
    longitude: ''
  });
  
  const reportRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);
  
  // For the interactive financial slider
  const [targetCapacity, setTargetCapacity] = useState(100); // MW Default

  const validateCoordinates = (lat, lon) => {
    if (isNaN(lat) || lat < -90 || lat > 90) return "Latitude must be a number between -90 and 90.";
    if (isNaN(lon) || lon < -180 || lon > 180) return "Longitude must be a number between -180 and 180.";
    return null;
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setError(null);
    setReport(null);

    const lat = parseFloat(formData.latitude);
    const lon = parseFloat(formData.longitude);
    
    const validationError = validateCoordinates(lat, lon);
    if (validationError) {
      setError(validationError);
      return;
    }

    if (!formData.site_name.trim()) {
      setError("Please provide a site name.");
      return;
    }

    setLoading(true);
    try {
      const data = await analysisService.runAnalysis(lat, lon, formData.site_name);
      setReport(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred while analyzing the site.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!reportRef.current) return;
    setDownloading(true);
    try {
      const element = reportRef.current;
      const canvas = await html2canvas(element, { scale: 2, useCORS: true });
      const imgData = canvas.toDataURL('image/png');
      
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', 0, 10, pdfWidth, pdfHeight);
      pdf.save(`${report?.site_name || 'Site'}_Analysis_Report.pdf`);
    } catch (err) {
      console.error("Error generating PDF:", err);
      alert("Failed to generate PDF report.");
    } finally {
      setDownloading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return '#10b981'; // Green
    if (score >= 55) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  return (
    <div className="page-content" style={{ paddingBottom: '4rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      <div className="page-header" style={{ marginBottom: '1rem' }}>
        <div>
          <h1 className="page-title" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Activity size={32} color="var(--color-primary)" />
            Site Suitability Analysis
          </h1>
          <p className="page-subtitle">Interactive Geospatial Intelligence & Performance Projections</p>
        </div>
      </div>

      {/* Inputs Section */}
      <div className="grid-2" style={{ gap: '2rem' }}>
        <div className="card">
          <h2 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 800, marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Navigation size={24} color="var(--color-primary)" /> Configure Location
          </h2>
          <form onSubmit={handleAnalyze} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Site Name</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="e.g. Kanyakumari Coastal Project"
                value={formData.site_name}
                onChange={(e) => setFormData({...formData, site_name: e.target.value})}
                required
              />
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Latitude</label>
                <input 
                  type="number" 
                  step="any"
                  className="form-input" 
                  placeholder="-90 to 90"
                  value={formData.latitude}
                  onChange={(e) => setFormData({...formData, latitude: e.target.value})}
                  required
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Longitude</label>
                <input 
                  type="number" 
                  step="any"
                  className="form-input" 
                  placeholder="-180 to 180"
                  value={formData.longitude}
                  onChange={(e) => setFormData({...formData, longitude: e.target.value})}
                  required
                />
              </div>
            </div>

            {error && (
              <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', borderRadius: 'var(--radius-md)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                <strong>Validation Error:</strong> {error}
              </div>
            )}

            <button type="submit" className="btn btn-primary" disabled={loading} style={{ marginTop: '0.5rem', padding: '0.75rem', fontSize: '1rem', display: 'flex', justifyContent: 'center', gap: '0.5rem' }}>
              {loading ? (
                <><span className="spinner" /> Running Deep Analysis...</>
              ) : (
                <><Activity size={20} /> Run Complete Analysis</>
              )}
            </button>
          </form>
        </div>

        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
           <MapLocator 
             latitude={report ? report.latitude : (formData.latitude ? parseFloat(formData.latitude) : null)} 
             longitude={report ? report.longitude : (formData.longitude ? parseFloat(formData.longitude) : null)} 
             siteName={report ? report.site_name : formData.site_name}
             onLocationSelect={(lat, lon) => {
               if (!report) {
                 setFormData(prev => ({
                   ...prev,
                   latitude: lat.toFixed(6),
                   longitude: lon.toFixed(6)
                 }));
               }
             }}
           />
        </div>
      </div>

      {loading && (
        <div className="card" style={{ padding: '4rem', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', color: 'var(--text-muted)' }}>
          <span className="spinner" style={{ width: '48px', height: '48px', marginBottom: '1.5rem', borderTopColor: 'var(--color-primary)', borderWidth: '4px' }} />
          <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>Processing Geospatial Data Pipeline...</h3>
          <p>Extracting Terrain, Environment, Weather APIs, and ML models.</p>
        </div>
      )}

      {report && !loading && (
        <div ref={reportRef} style={{ display: 'flex', flexDirection: 'column', gap: '2rem', animation: 'fadeIn 0.6s ease', padding: '1rem', background: 'var(--bg-default)' }}>
          
          {/* Main Dashboard Header */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '-1rem' }}>
            <button 
              className="btn btn-primary" 
              onClick={handleDownloadReport} 
              disabled={downloading}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', zIndex: 10 }}
            >
              {downloading ? <span className="spinner" /> : <Download size={20} />}
              {downloading ? "Generating PDF..." : "Export to PDF Report"}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
            
            {/* Suitability Score Ring */}
            <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '1.5rem' }}>Report Site Location</div>
              <div style={{ color: 'var(--text-secondary)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Compass size={16} /> Coordinates: {report.latitude}, {report.longitude}
              </div>
              
              <div style={{ position: 'relative', width: '180px', height: '180px', marginBottom: '1.5rem' }}>
                <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)', width: '100%', height: '100%' }}>
                  <circle cx="50" cy="50" r="45" fill="none" stroke="var(--bg-border)" strokeWidth="10" />
                  <circle 
                    cx="50" cy="50" r="45" fill="none" 
                    stroke={getScoreColor(report.evaluation.overall_score)} 
                    strokeWidth="10" 
                    strokeDasharray={`${report.evaluation.overall_score * 2.83} 283`}
                    style={{ transition: 'stroke-dasharray 1s ease-out' }}
                  />
                </svg>
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                  <span style={{ fontSize: '2.5rem', fontWeight: 800, color: getScoreColor(report.evaluation.overall_score) }}>{report.evaluation.overall_score}%</span>
                  <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', fontWeight: 600 }}>SUITABILITY</span>
                </div>
              </div>
              
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: getScoreColor(report.evaluation.overall_score) }}>
                {report.deployment.recommended_technology} Recommended
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', width: '100%', borderTop: '1px solid var(--bg-border)', paddingTop: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>Solar Potential</div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 700, color: '#f59e0b' }}>{(report.features.solar_irradiance_kwh / 7.5 * 100).toFixed(1)}%</div>
                </div>
                <div style={{ width: '1px', background: 'var(--bg-border)' }}></div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>Wind Potential</div>
                  <div style={{ fontSize: '1.125rem', fontWeight: 700, color: '#3b82f6' }}>{(report.features.wind_speed_ms / 10 * 100).toFixed(1)}%</div>
                </div>
              </div>
            </div>

            {/* 5 Pillars */}
            <div className="card">
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '1.5rem', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <BarChart2 size={20} color="var(--color-primary)" /> WEIGHTED SCORING MATRIX BREAKDOWN (5 PILLARS)
              </h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                {[
                  { label: "Resource Availability", weight: 35, score: report.pillars?.resource_availability || 0 },
                  { label: "Geographic Suitability", weight: 25, score: report.pillars?.geographic_suitability || 0 },
                  { label: "Infrastructure Access", weight: 15, score: report.pillars?.infrastructure_access || 0 },
                  { label: "Environmental Impact", weight: 15, score: report.pillars?.environmental_impact || 0 },
                  { label: "Economic Feasibility", weight: 10, score: report.pillars?.economic_feasibility || 0 }
                ].map((pillar, idx) => (
                  <div key={idx}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>{pillar.label} <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>({pillar.weight}% Weight)</span></span>
                      <span style={{ fontWeight: 800, color: getScoreColor(pillar.score) }}>{pillar.score}%</span>
                    </div>
                    <div style={{ width: '100%', height: '10px', background: 'var(--bg-secondary)', borderRadius: '5px', overflow: 'hidden' }}>
                      <div style={{ width: `${pillar.score}%`, height: '100%', background: getScoreColor(pillar.score), borderRadius: '5px' }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Geospatial Analytics */}
          <div className="card">
            <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '1.5rem', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Leaf size={20} color="var(--color-green)" /> Geospatial Environmental Analytics
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
              <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #10b981' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontWeight: 600 }}>
                  <Mountain size={16} /> Terrain Slope
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800 }}>{report.geospatial?.terrain_slope}°</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{report.geospatial?.terrain_slope < 10 ? 'Suitable Grade (<10°)' : 'Steep Terrain (>10°)'}</div>
              </div>

              <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #3b82f6' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontWeight: 600 }}>
                  <Leaf size={16} /> Vegetation (NDVI)
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800 }}>{report.geospatial?.ndvi}</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{report.geospatial?.ndvi < 0.4 ? 'Low Biomass Density' : 'High Biomass'}</div>
              </div>

              <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', borderLeft: `4px solid ${report.geospatial?.zoning_status.includes('Restricted') ? '#ef4444' : '#10b981'}` }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontWeight: 600 }}>
                  <Info size={16} /> Zoning & Wilderness
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 800 }}>{report.geospatial?.zoning_status}</div>
              </div>

              <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', borderLeft: '4px solid #f59e0b' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontWeight: 600 }}>
                  <Target size={16} /> Land Cover
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 800 }}>{report.geospatial?.land_cover}</div>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Suitable Land Profile</div>
              </div>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid-2" style={{ gap: '2rem' }}>
            <MonthlyYieldChart data={report.monthly_yields} />
            <ElevationProfileChart centerElevation={report.features.elevation_m} />
          </div>

          {/* Interactive Financial Analysis */}
          <div className="card">
            <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '1.5rem', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Briefcase size={20} color="#f59e0b" /> Financial Analysis & Investment Recommendation
            </h3>

            <div style={{ marginBottom: '2rem', background: 'var(--bg-secondary)', padding: '1.5rem', borderRadius: 'var(--radius-md)' }}>
              <label style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', fontWeight: 700, color: 'var(--text-secondary)' }}>
                TARGET INSTALLATION CAPACITY (MW)
                <span style={{ color: 'var(--text-primary)', fontSize: '1.25rem' }}>{targetCapacity} MW</span>
              </label>
              <input 
                type="range" 
                min="10" 
                max="500" 
                step="10" 
                value={targetCapacity}
                onChange={(e) => setTargetCapacity(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--color-primary)' }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
              <div style={{ borderLeft: '4px solid #ef4444', paddingLeft: '1rem' }}>
                <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '0.25rem' }}>ESTIMATED CAPEX</div>
                <div style={{ fontSize: '2rem', fontWeight: 800 }}>$ {(report.financial_metrics.estimated_project_cost * (targetCapacity / 100) / 1000000).toFixed(2)} M</div>
              </div>
              <div style={{ borderLeft: '4px solid #f59e0b', paddingLeft: '1rem' }}>
                <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '0.25rem' }}>ESTIMATED OPEX / YEAR</div>
                <div style={{ fontSize: '2rem', fontWeight: 800 }}>$ {(report.financial_metrics.estimated_opex * (targetCapacity / 100)).toLocaleString()}</div>
              </div>
              <div style={{ borderLeft: '4px solid #10b981', paddingLeft: '1rem' }}>
                <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '0.25rem' }}>PROJECT ROI / YEAR</div>
                <div style={{ fontSize: '2rem', fontWeight: 800, color: '#10b981' }}>{report.financial_metrics.roi.toFixed(1)} %</div>
              </div>
              <div style={{ borderLeft: '4px solid var(--color-primary)', paddingLeft: '1rem' }}>
                <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '0.25rem' }}>PAYBACK PERIOD</div>
                <div style={{ fontSize: '2rem', fontWeight: 800 }}>{report.financial_metrics.payback_period.toFixed(1)} Yrs</div>
              </div>
            </div>
          </div>

          <SavedProjectsTable />

        </div>
      )}
    </div>
  );
}
