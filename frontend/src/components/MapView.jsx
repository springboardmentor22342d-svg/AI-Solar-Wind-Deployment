import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  useMapEvents,
} from "react-leaflet";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

/*
 * Fix Leaflet marker icons when using Vite.
 */
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",

  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",

  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});


/*
 * Move the map to the selected/analysed location.
 */
function MapCenter({ latitude, longitude }) {
  const map = useMap();

  useEffect(() => {
    if (
      latitude !== null &&
      longitude !== null &&
      latitude !== undefined &&
      longitude !== undefined
    ) {
      map.setView(
        [Number(latitude), Number(longitude)],
        10
      );
    }
  }, [latitude, longitude, map]);

  return null;
}


/*
 * Allow the user to click anywhere on the map
 * and select a location.
 */
function LocationSelector({ onLocationSelect }) {
  useMapEvents({
    click(event) {
      if (onLocationSelect) {
        onLocationSelect(
          event.latlng.lat,
          event.latlng.lng
        );
      }
    },
  });

  return null;
}


/*
 * Main Map Component
 */
function MapView({
  latitude,
  longitude,
  onLocationSelect,
}) {
  const defaultPosition = [20.2961, 85.8245];

  const lat = Number(latitude);
  const lng = Number(longitude);

  const hasLocation =
    latitude !== "" &&
    longitude !== "" &&
    Number.isFinite(lat) &&
    Number.isFinite(lng) &&
    lat >= -90 &&
    lat <= 90 &&
    lng >= -180 &&
    lng <= 180;

  const position = hasLocation
    ? [lat, lng]
    : defaultPosition;

  return (
    <div className="map-card">

      {/* ================================
          MAP TITLE
      ================================= */}

      <h2>LOCATION MAP</h2>

      <p>
        Click anywhere on the map to select a
        location for analysis.
      </p>


      {/* ================================
          MAP
      ================================= */}

      <div className="map-container">

        <MapContainer
          center={position}
          zoom={hasLocation ? 10 : 5}
          scrollWheelZoom={true}
          style={{
            height: "100%",
            width: "100%",
          }}
        >

          {/* OpenStreetMap */}

          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />


          {/* Center map on selected location */}

          {hasLocation && (
            <MapCenter
              latitude={lat}
              longitude={lng}
            />
          )}


          {/* Allow user to select location */}

          <LocationSelector
            onLocationSelect={onLocationSelect}
          />


          {/* Marker */}

          {hasLocation && (
            <Marker position={position}>

              <Popup>
                <strong>
                  Selected Location
                </strong>

                <br />

                Latitude:{" "}
                {lat.toFixed(6)}

                <br />

                Longitude:{" "}
                {lng.toFixed(6)}
              </Popup>

            </Marker>
          )}

        </MapContainer>

      </div>


      {/* ================================
          COORDINATES
      ================================= */}

      {hasLocation && (
        <div className="coordinates">

          <span>
            <strong>Latitude:</strong>{" "}
            {lat.toFixed(6)}
          </span>

          <span>
            <strong>Longitude:</strong>{" "}
            {lng.toFixed(6)}
          </span>

        </div>
      )}

    </div>
  );
}

export default MapView;