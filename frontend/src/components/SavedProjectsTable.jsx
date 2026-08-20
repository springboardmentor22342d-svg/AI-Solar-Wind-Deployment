import React, { useState, useEffect } from 'react';
import { analysisService } from '../api/analysis';

export default function SavedProjectsTable() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await analysisService.getHistory();
      setProjects(data);
    } catch (err) {
      console.error("Failed to fetch history", err);
      setError("Failed to load saved projects.");
    } finally {
      setLoading(false);
    }
  };

  const toggleSelect = (id) => {
    setSelectedIds(prev => {
      if (prev.includes(id)) {
        return prev.filter(x => x !== id);
      } else {
        if (prev.length >= 3) {
          alert("You can only compare up to 3 projects at a time.");
          return prev;
        }
        return [...prev, id];
      }
    });
  };

  const getStatusColor = (score) => {
    if (score >= 75) return '#10b981'; // green
    if (score >= 55) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };

  if (loading) return <div className="card" style={{ padding: '2rem', textAlign: 'center' }}><span className="spinner"></span> Loading Saved Projects...</div>;
  if (error) return <div className="card" style={{ padding: '2rem', color: '#ef4444' }}>{error}</div>;
  if (projects.length === 0) return null;

  const selectedProjects = projects.filter(p => selectedIds.includes(p.id));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', marginTop: '2rem' }}>
      
      {/* Table Section */}
      <div className="card">
        <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '1.5rem' }}>Saved Projects (Database)</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--bg-border)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '1rem', width: '40px' }}></th>
                <th style={{ padding: '1rem' }}>Site Name</th>
                <th style={{ padding: '1rem' }}>Coordinates</th>
                <th style={{ padding: '1rem' }}>Suitability Score</th>
                <th style={{ padding: '1rem' }}>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {projects.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--bg-border)', background: selectedIds.includes(p.id) ? 'rgba(37,99,235,0.05)' : 'transparent' }}>
                  <td style={{ padding: '1rem' }}>
                    <input 
                      type="checkbox" 
                      checked={selectedIds.includes(p.id)} 
                      onChange={() => toggleSelect(p.id)} 
                      style={{ cursor: 'pointer' }}
                    />
                  </td>
                  <td style={{ padding: '1rem', fontWeight: 600 }}>{p.site_name}</td>
                  <td style={{ padding: '1rem', color: 'var(--text-secondary)' }}>
                    {p.latitude.toFixed(4)}, {p.longitude.toFixed(4)}
                  </td>
                  <td style={{ padding: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: getStatusColor(p.suitability_score) }}></div>
                      {p.suitability_score ? p.suitability_score.toFixed(1) + '%' : 'N/A'}
                    </div>
                  </td>
                  <td style={{ padding: '1rem' }}>{p.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Comparison Grid */}
      {selectedProjects.length > 0 && (
        <div className="card" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--bg-border)' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Site Suitability Comparison Grid</h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: `minmax(200px, 1fr) repeat(${selectedProjects.length}, 1fr)`, gap: '1px', background: 'var(--bg-border)' }}>
            
            {/* Headers */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Metric</div>
            {selectedProjects.map(p => (
              <div key={`head-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 700, color: 'var(--text-primary)', borderTop: `4px solid ${getStatusColor(p.suitability_score)}` }}>
                {p.site_name}
              </div>
            ))}

            {/* Coordinates */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Coordinates</div>
            {selectedProjects.map(p => (
              <div key={`coord-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem' }}>
                {p.latitude.toFixed(4)}, {p.longitude.toFixed(4)}
              </div>
            ))}

            {/* Suitability Score */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Suitability Score</div>
            {selectedProjects.map(p => (
              <div key={`score-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 800, color: getStatusColor(p.suitability_score) }}>
                {p.suitability_score ? p.suitability_score.toFixed(1) + '%' : 'N/A'}
              </div>
            ))}

            {/* Elevation */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Elevation (m)</div>
            {selectedProjects.map(p => (
              <div key={`elev-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem' }}>
                {p.elevation_m ? p.elevation_m.toFixed(1) : 'N/A'}
              </div>
            ))}

            {/* Solar Irradiance */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Solar (GHI) kWh/m²</div>
            {selectedProjects.map(p => (
              <div key={`solar-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem' }}>
                {p.solar_irradiance_kwh ? p.solar_irradiance_kwh.toFixed(1) : 'N/A'}
              </div>
            ))}

            {/* Wind Speed */}
            <div style={{ background: 'var(--bg-card)', padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Wind Speed (m/s)</div>
            {selectedProjects.map(p => (
              <div key={`wind-${p.id}`} style={{ background: 'var(--bg-card)', padding: '1rem' }}>
                {p.wind_speed_50m_ms ? p.wind_speed_50m_ms.toFixed(1) : 'N/A'}
              </div>
            ))}

          </div>
        </div>
      )}
    </div>
  );
}
