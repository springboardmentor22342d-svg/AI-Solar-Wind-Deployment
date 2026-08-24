export async function geocodeLocation({
  village,
  district,
  state,
  country
}) {
  const query = [
    village,
    district,
    state,
    country
  ]
    .filter(Boolean)
    .join(", ");

  console.log("Searching:", query);

  const url =
    `https://nominatim.openstreetmap.org/search` +
    `?format=json` +
    `&q=${encodeURIComponent(query)}` +
    `&limit=5` +
    `&addressdetails=1`;

  try {
    const response = await fetch(url, {
      headers: {
        Accept: "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`Geocoding HTTP error: ${response.status}`);
    }

    const results = await response.json();

    console.log("Geocoding results:", results);

    if (!results || results.length === 0) {
      return null;
    }

    const result = results[0];

    return {
      latitude: Number(result.lat),
      longitude: Number(result.lon),
      displayName: result.display_name
    };

  } catch (error) {
    console.error("Geocoding error:", error);
    throw error;
  }
}