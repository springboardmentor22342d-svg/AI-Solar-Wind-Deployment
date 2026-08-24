const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Analyze a renewable-energy site.
 *
 * Backend endpoint:
 * POST /analysis
 *
 * The FastAPI endpoint expects these values
 * as query parameters:
 *
 * village
 * district
 * state
 * country
 * date
 */
export async function getAnalysis({
  village,
  district,
  state,
  country,
  date,
}) {
  const params = new URLSearchParams({
    village: village || "",
    district: district || "",
    state: state || "",
    country: country || "",
    date: date || "",
  });

  const response = await fetch(
    `${API_BASE_URL}/analysis?${params.toString()}`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
    }
  );

  if (!response.ok) {
    let errorMessage = `Backend request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (errorData?.detail) {
        errorMessage =
          typeof errorData.detail === "string"
            ? errorData.detail
            : JSON.stringify(errorData.detail);
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}