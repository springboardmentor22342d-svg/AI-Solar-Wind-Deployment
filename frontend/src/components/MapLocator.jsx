import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Helper component to center map when coordinates change
function RecenterMap({ lat, lon }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lon], map.getZoom());
  }, [lat, lon, map]);
  return null;
}

// Map events for clicking
function MapEvents({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      if (onLocationSelect) {
        onLocationSelect(e.latlng.lat, e.latlng.lng);
      }
    },
  });
  return null;
}

export default function MapLocator({ latitude, longitude, siteName, onLocationSelect }) {
  const defaultLat = latitude || 20.5937; // Default to India center
  const defaultLon = longitude || 78.9629;

  return (
    <div>
      <div style={{ height: '400px', width: '100%', borderRadius: 'var(--radius-md)', overflow: 'hidden', boxShadow: 'var(--shadow-sm)', border: '1px solid var(--bg-border)' }}>
        <MapContainer 
          center={[defaultLat, defaultLon]} 
          zoom={latitude ? 10 : 4} 
          style={{ height: '100%', width: '100%', cursor: onLocationSelect ? 'crosshair' : 'grab' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapEvents onLocationSelect={onLocationSelect} />
          {latitude && longitude && (
            <>
              <RecenterMap lat={latitude} lon={longitude} />
              <Marker position={[latitude, longitude]}>
                <Popup>
                  <strong>{siteName || 'Selected Location'}</strong><br/>
                  Lat: {latitude}, Lon: {longitude}
                </Popup>
              </Marker>
            </>
          )}
        </MapContainer>
      </div>
      {onLocationSelect && (
        <p style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)', marginTop: '0.5rem', textAlign: 'center' }}>
          📍 Click anywhere on the map to auto-fill coordinates
        </p>
      )}
    </div>
  );
}
