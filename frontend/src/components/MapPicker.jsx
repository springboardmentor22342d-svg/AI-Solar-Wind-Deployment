import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet default icon paths in React environment
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function MapEventsHandler({ onSelectLocation }) {
  useMapEvents({
    click(e) {
      onSelectLocation(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function MapRecenter({ lat, lng }) {
  const map = useMap();
  useEffect(() => {
    if (lat !== undefined && lng !== undefined) {
      map.flyTo([lat, lng], map.getZoom(), { animate: true });
    }
  }, [lat, lng, map]);
  return null;
}

export default function MapPicker({ latitude, longitude, onSelectLocation }) {
  const defaultCenter = [20.2961, 85.8245]; // Bhubaneswar default
  const position = [
    latitude !== '' && !isNaN(latitude) ? parseFloat(latitude) : defaultCenter[0],
    longitude !== '' && !isNaN(longitude) ? parseFloat(longitude) : defaultCenter[1],
  ];

  return (
    <div className="map-container">
      <MapContainer 
        center={position} 
        zoom={7} 
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapEventsHandler onSelectLocation={onSelectLocation} />
        <MapRecenter lat={position[0]} lng={position[1]} />
        <Marker position={position}>
          <Popup>
            <div style={{ textAlign: 'center', color: '#1e293b' }}>
              <strong>Selected Location</strong><br />
              Lat: {position[0].toFixed(4)}<br />
              Lng: {position[1].toFixed(4)}
            </div>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
