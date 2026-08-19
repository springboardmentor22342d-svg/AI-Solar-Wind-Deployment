import React from 'react';
import { Search, MapPin, Loader2 } from 'lucide-react';

const PRESETS = [
  { name: 'Bhubaneswar (Land)', lat: 20.2961, lng: 85.8245 },
  { name: 'Jaisalmer (Desert Solar)', lat: 26.9157, lng: 70.9083 },
  { name: 'Muppandal (Wind)', lat: 8.1834, lng: 77.5611 },
  { name: 'Arabian Sea (Ocean)', lat: 15.0000, lng: 65.0000 },
  { name: 'Bay of Bengal (Ocean)', lat: 12.0000, lng: 88.0000 },
  { name: 'Indian Ocean (Deep Sea)', lat: -10.0000, lng: 75.0000 },
];

export default function AnalysisForm({ 
  latitude, 
  longitude, 
  setLatitude, 
  setLongitude, 
  onSubmit, 
  isLoading 
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isLoading) {
      onSubmit();
    }
  };

  const handleSelectPreset = (preset) => {
    setLatitude(preset.lat.toString());
    setLongitude(preset.lng.toString());
  };

  return (
    <div className="glass-panel">
      <h2 className="section-title">
        <MapPin size={20} color="#06b6d4" />
        Site Location
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="latitude-input">Latitude (-90 to 90)</label>
          <div className="input-wrapper">
            <input
              id="latitude-input"
              type="number"
              step="any"
              className="form-input"
              placeholder="e.g. 20.2961"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="longitude-input">Longitude (-180 to 180)</label>
          <div className="input-wrapper">
            <input
              id="longitude-input"
              type="number"
              step="any"
              className="form-input"
              placeholder="e.g. 85.8245"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              required
            />
          </div>
        </div>

        <button
          type="submit"
          className="btn-primary"
          disabled={isLoading || !latitude || !longitude}
        >
          {isLoading ? (
            <>
              <Loader2 className="spinner-icon" size={18} style={{ animation: 'spin 1s linear infinite' }} />
              Analysing site...
            </>
          ) : (
            <>
              <Search size={18} />
              Analyse
            </>
          )}
        </button>
      </form>

      <div className="presets-container">
        <div className="presets-title">Location Presets (Land & Ocean)</div>
        <div className="presets-list">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-chip"
              onClick={() => handleSelectPreset(p)}
            >
              {p.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
