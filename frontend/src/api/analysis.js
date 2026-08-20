const API_BASE_URL = "http://127.0.0.1:8000";

export async function runAnalysis(latitude, longitude, projectName = "", token = "") {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}/analysis`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        project_name: projectName,
      }),
    });
  } catch (networkError) {
    throw new Error(
      "Unable to reach the server. Please check your connection and try again.",
      { cause: networkError }
    );
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    const message = extractErrorMessage(errorData, response.status);
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

function extractErrorMessage(errorData, status) {
  if (!errorData) return `Request failed with status ${status}.`;

  const detail = errorData.detail;

  // FastAPI validation errors: detail is an array of {loc, msg, ...}
  if (Array.isArray(detail)) {
    return detail
      .map((d) => {
        const field = Array.isArray(d.loc) ? d.loc[d.loc.length - 1] : "input";
        return `${field}: ${d.msg}`;
      })
      .join("; ");
  }

  // Simple string detail (e.g. from our own HTTPException calls)
  if (typeof detail === "string") return detail;

  return "An unexpected error occurred. Please try again.";
}

export async function fetchGuidelines() {
  const response = await fetch(`${API_BASE_URL}/guidelines`);
  if (!response.ok) {
    throw new Error("Unable to load guidelines");
  }
  return response.json();
}
