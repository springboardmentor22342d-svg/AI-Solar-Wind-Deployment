import React from "react";

export default function TopSites({ sites = [] }) {

  const sortedSites = [...sites]
    .sort(
      (a, b) =>
        Number(b.suitabilityScore || 0) -
        Number(a.suitabilityScore || 0)
    )
    .slice(0, 5);

  return (
    <div
      style={{
        padding: "10px",
      }}
    >

      {sortedSites.length === 0 ? (

        <div
          style={{
            textAlign: "center",
            padding: "25px 10px",
            fontSize: "12px",
            opacity: 0.6,
          }}
        >
          No analyzed sites yet.
        </div>

      ) : (

        sortedSites.map((site, index) => {

          const score = Math.round(
            Number(site.suitabilityScore || 0)
          );

          return (
            <div
              key={`${site.latitude}-${site.longitude}-${index}`}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "12px 8px",
                marginBottom: "8px",
                borderRadius: "10px",
                background:
                  "rgba(255,255,255,0.04)",
              }}
            >

              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  minWidth: 0,
                }}
              >

                <strong>
                  #{index + 1}
                </strong>

                <div>

                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: "600",
                    }}
                  >
                    {site.village ||
                      "Unknown Location"}
                  </div>

                  <div
                    style={{
                      fontSize: "10px",
                      opacity: 0.6,
                    }}
                  >
                    {site.district || ""}
                    {site.state
                      ? `, ${site.state}`
                      : ""}
                  </div>

                </div>

              </div>


              <div
                style={{
                  textAlign: "right",
                }}
              >

                <strong>
                  {score}%
                </strong>

                <div
                  style={{
                    fontSize: "9px",
                    opacity: 0.6,
                  }}
                >
                  suitability
                </div>

              </div>

            </div>
          );

        })

      )}

    </div>
  );
}