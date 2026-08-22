import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

// Leaflet's default marker icon doesn't load correctly with bundlers
// like Vite unless explicitly configured — this fixes that.
const defaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function LocationMap({ latitude, longitude }) {
  return (
    <div className="map-panel">
      <MapContainer
        center={[latitude, longitude]}
        zoom={10}
        style={{ height: "100%", width: "100%" }}
        key={`${latitude}-${longitude}`}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        <Marker position={[latitude, longitude]} icon={defaultIcon}>
          <Popup>
            Analyzed location: {latitude}, {longitude}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default LocationMap;
