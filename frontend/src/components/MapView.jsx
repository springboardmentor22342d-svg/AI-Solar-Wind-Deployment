import React, { useEffect } from "react";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";

// ============================================================
// LEAFLET MARKER ICON FIX
// ============================================================

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

// ============================================================
// MAP LOCATION UPDATER
// ============================================================

function MapLocationUpdater({
  latitude,
  longitude,
}) {
  const map = useMap();

  useEffect(() => {
    // --------------------------------------------------------
    // Do nothing if coordinates are invalid
    // --------------------------------------------------------

    if (
      !Number.isFinite(latitude) ||
      !Number.isFinite(longitude)
    ) {
      return;
    }

    // Do not fly to [0, 0] during initial empty state
    if (
      latitude === 0 &&
      longitude === 0
    ) {
      return;
    }

    console.log(
      "Map received coordinates:"
    );

    console.log(
      "Latitude:",
      latitude
    );

    console.log(
      "Longitude:",
      longitude
    );

    // --------------------------------------------------------
    // Move map to analyzed location
    // --------------------------------------------------------

    map.flyTo(
      [latitude, longitude],
      13,
      {
        animate: true,
        duration: 1.5,
      }
    );

  }, [
    latitude,
    longitude,
    map,
  ]);

  return null;
}

// ============================================================
// MAP VIEW
// ============================================================

export default function MapView({
  analysis,
}) {

  // ==========================================================
  // SAFELY READ ANALYSIS DATA
  // ==========================================================

  const latitude = Number(
    analysis?.latitude
  );

  const longitude = Number(
    analysis?.longitude
  );

  // ==========================================================
  // CHECK VALID LOCATION
  // ==========================================================

  const hasValidLocation =
    Number.isFinite(latitude) &&
    Number.isFinite(longitude) &&
    !(latitude === 0 && longitude === 0);

  // ==========================================================
  // LOCATION INFORMATION
  // ==========================================================

  const village =
    analysis?.village ||
    "Analyzed Location";

  const district =
    analysis?.district ||
    "";

  const state =
    analysis?.state ||
    "";

  const country =
    analysis?.country ||
    "";

  const displayName =
    analysis?.displayName ||
    "";

  // ==========================================================
  // BACKEND SOLAR DATA
  // ==========================================================

  const avgSolar = Number(
    analysis?.avgSolar || 0
  );

  // ==========================================================
  // BACKEND WIND DATA
  // ==========================================================

  const avgWind = Number(
    analysis?.avgWind || 0
  );

  // ==========================================================
  // BACKEND ENERGY DATA
  // ==========================================================

  const solarEnergy = Number(
    analysis?.solarEnergy || 0
  );

  const windEnergy = Number(
    analysis?.windEnergy || 0
  );

  const totalHybridEnergy = Number(
    analysis?.totalHybridEnergy || 0
  );

  // ==========================================================
  // DEBUG
  // ==========================================================

  console.log(
    "MapView analysis:",
    analysis
  );

  console.log(
    "MapView coordinates:",
    latitude,
    longitude
  );

  // ==========================================================
  // RETURN MAP
  // ==========================================================

  return (
    <div
      className="map-container"
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
      }}
    >

      {/* ======================================================
          LEAFLET MAP
      ====================================================== */}

      <MapContainer
        center={[20, 0]}
        zoom={2}
        minZoom={2}
        maxZoom={18}
        scrollWheelZoom={true}
        style={{
          width: "100%",
          height: "100%",
        }}
      >

        {/* ====================================================
            OPEN STREET MAP TILES
        ==================================================== */}

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* ====================================================
            UPDATE MAP POSITION
        ==================================================== */}

        <MapLocationUpdater
          latitude={latitude}
          longitude={longitude}
        />

        {/* ====================================================
            LOCATION MARKER
        ==================================================== */}

        {hasValidLocation && (

          <Marker
            position={[
              latitude,
              longitude,
            ]}
          >

            <Popup>

              <div
                style={{
                  minWidth: "220px",
                  lineHeight: "1.5",
                }}
              >

                {/* LOCATION */}

                <strong>
                  {village}
                </strong>

                <br />

                {district && (
                  <>
                    {district}
                    <br />
                  </>
                )}

                {state && (
                  <>
                    {state}
                    <br />
                  </>
                )}

                {country && (
                  <>
                    {country}
                    <br />
                  </>
                )}

                {/* DISPLAY NAME */}

                {displayName && (
                  <>
                    <br />

                    <small>
                      {displayName}
                    </small>
                  </>
                )}

                <hr />

                {/* COORDINATES */}

                <strong>
                  Coordinates
                </strong>

                <br />

                Latitude:{" "}
                {latitude.toFixed(6)}

                <br />

                Longitude:{" "}
                {longitude.toFixed(6)}

                <hr />

                {/* SOLAR */}

                <strong>
                  Solar Resource
                </strong>

                <br />

                Irradiance:{" "}

                {avgSolar > 0
                  ? `${avgSolar.toFixed(2)} W/m²`
                  : "--"}

                <br />

                {/* WIND */}

                <strong>
                  Wind Resource
                </strong>

                <br />

                Speed:{" "}

                {avgWind > 0
                  ? `${avgWind.toFixed(2)} m/s`
                  : "--"}

                <hr />

                {/* ENERGY */}

                <strong>
                  Predicted Energy
                </strong>

                <br />

                Solar:{" "}

                {solarEnergy > 0
                  ? `${solarEnergy.toFixed(2)} kWh/year`
                  : "--"}

                <br />

                Wind:{" "}

                {windEnergy > 0
                  ? `${windEnergy.toFixed(2)} kWh/year`
                  : "--"}

                <br />

                Hybrid:{" "}

                {totalHybridEnergy > 0
                  ? `${totalHybridEnergy.toFixed(2)} kWh/year`
                  : "--"}

              </div>

            </Popup>

          </Marker>

        )}

      </MapContainer>

      {/* ======================================================
          EMPTY MAP MESSAGE
      ====================================================== */}

      {!hasValidLocation && (

        <div
          style={{
            position: "absolute",
            top: "15px",
            left: "50%",
            transform: "translateX(-50%)",
            zIndex: 1000,
            background:
              "rgba(0, 0, 0, 0.75)",
            color: "#fff",
            padding: "8px 14px",
            borderRadius: "8px",
            fontSize: "12px",
            pointerEvents: "none",
          }}
        >
          Analyze a location to view it on the map
        </div>

      )}

      {/* ======================================================
          MAP LEGEND
      ====================================================== */}

      <div className="map-legend">

        <div className="legend-title">
          Site Suitability
        </div>

        <div className="legend-item">
          <span className="legend-dot excellent"></span>
          Excellent
        </div>

        <div className="legend-item">
          <span className="legend-dot very-good"></span>
          Very Good
        </div>

        <div className="legend-item">
          <span className="legend-dot good"></span>
          Good
        </div>

        <div className="legend-item">
          <span className="legend-dot moderate"></span>
          Moderate
        </div>

        <div className="legend-item">
          <span className="legend-dot low"></span>
          Low
        </div>

      </div>

    </div>
  );
}