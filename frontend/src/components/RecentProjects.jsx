import React from "react";

export default function RecentProjects({
  projects = [],
}) {

  const recentProjects = [...projects]
    .reverse()
    .slice(0, 5);

  return (
    <div
      style={{
        padding: "10px",
      }}
    >

      {recentProjects.length === 0 ? (

        <div
          style={{
            textAlign: "center",
            padding: "25px 10px",
            fontSize: "12px",
            opacity: 0.6,
          }}
        >
          No recent analyses.
        </div>

      ) : (

        recentProjects.map(
          (project, index) => {

            const score = Math.round(
              Number(
                project.suitabilityScore || 0
              )
            );

            const date =
              project.date ||
              project.analyzedAt;

            return (

              <div
                key={`${project.latitude}-${project.longitude}-${index}`}
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  alignItems: "center",
                  padding: "11px 8px",
                  marginBottom: "8px",
                  borderBottom:
                    "1px solid rgba(255,255,255,0.06)",
                }}
              >

                <div>

                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: "600",
                    }}
                  >
                    {project.village ||
                      "Unknown Location"}
                  </div>

                  <div
                    style={{
                      fontSize: "10px",
                      opacity: 0.6,
                      marginTop: "3px",
                    }}
                  >
                    {project.district || ""}
                    {project.state
                      ? `, ${project.state}`
                      : ""}
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
                    {date || "Analyzed"}
                  </div>

                </div>

              </div>

            );
          }
        )

      )}

    </div>
  );
}