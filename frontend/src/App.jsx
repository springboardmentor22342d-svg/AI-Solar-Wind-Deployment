import React, { useState } from 'react';
import { Sun, Wind, Activity, Compass, AlertCircle } from 'lucide-react';
import AnalysisForm from './components/AnalysisForm';
import MapPicker from './components/MapPicker';
import Dashboard from './components/Dashboard';
import ErrorMessage from './components/ErrorMessage';
import { analyzeSite } from './api/analysis';

export default function App() {
  const [latitude, setLatitude] = useState('20.2961');
  const [longitude, setLongitude] = useState('85.8245');
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleSelectLocation = (lat, lng) => {
    setLatitude(lat.toFixed(4));
    setLongitude(lng.toFixed(4));
    setError(null);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await analyzeSite(latitude, longitude);
      setAnalysisResult(result);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during site analysis.');
      setAnalysisResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <header className="app-header">
        <div className="brand-container">
          <div className="brand-icon">
            <Sun size={24} />
          </div>
          <div>
            <h1 className="brand-title">Solar & Wind Deployment Intelligence</h1>
            <div className="brand-subtitle">AI-Powered Geospatial & Financial Site Feasibility Engine</div>
          </div>
        </div>

        <div className="status-badge">
          <span className="status-dot"></span>
          Backend API Operational
        </div>
      </header>

      {/* Error Banner */}
      <ErrorMessage message={error} />

      {/* Main Grid */}
      <main className="main-grid">
        {/* Left Column: Location Input & Interactive Map */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <AnalysisForm 
            latitude={latitude}
            longitude={longitude}
            setLatitude={setLatitude}
            setLongitude={setLongitude}
            onSubmit={handleAnalyze}
            isLoading={isLoading}
          />

          <div className="glass-panel">
            <h2 className="section-title">
              <Compass size={20} color="#06b6d4" />
              Interactive Location Map
            </h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
              Click anywhere on the map to pin geographic coordinates for analysis.
            </p>
            <MapPicker 
              latitude={latitude}
              longitude={longitude}
              onSelectLocation={handleSelectLocation}
            />
          </div>
        </section>

        {/* Right Column: Dashboard or State Views */}
        <section>
          {isLoading ? (
            <div className="glass-panel loading-box">
              <div className="spinner"></div>
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', marginBottom: '8px' }}>
                Analysing site...
              </h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', maxWidth: '400px' }}>
                Fetching geospatial features, processing ML predictions, evaluating hard/soft constraints, and generating financial ROI models.
              </p>
            </div>
          ) : analysisResult ? (
            <Dashboard data={analysisResult} />
          ) : (
            <div className="glass-panel empty-state">
              <Activity className="empty-icon" />
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', marginBottom: '8px', color: '#fff' }}>
                Ready for Site Assessment
              </h3>
              <p style={{ maxWidth: '420px', fontSize: '0.88rem' }}>
                Enter coordinates or select a location preset from the left panel, then click <strong>Analyse</strong> to execute the full renewable energy pipeline.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
