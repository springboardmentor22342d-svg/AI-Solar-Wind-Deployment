import API_URL from "../api/config";

export async function analyseLocation(latitude, longitude) {
  const controller = new AbortController();

  const timeoutId = setTimeout(() => {
    controller.abort();
  }, 30000);

  try {
    const response = await fetch(`${API_URL}/analysis`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        latitude: Number(latitude),
        longitude: Number(longitude),
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      let errorMessage = "Analysis request failed.";

      try {
        const errorData = await response.json();

        // Use the actual validation/business error
        // returned by FastAPI.
        if (errorData.detail) {
          if (typeof errorData.detail === "string") {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail
              .map((error) => {
                if (typeof error === "string") {
                  return error;
                }

                return (
                  error.msg ||
                  error.message ||
                  JSON.stringify(error)
                );
              })
              .join(", ");
          } else {
            errorMessage = JSON.stringify(errorData.detail);
          }
        }
      } catch {
        // Keep default error message.
      }

      const error = new Error(errorMessage);

      // Keep HTTP status available to the UI.
      error.status = response.status;

      throw error;
    }

    return await response.json();
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error(
        "The analysis request timed out. Please try again."
      );
    }

    if (error instanceof TypeError) {
      throw new Error(
        "Unable to connect to the backend. Please make sure the server is running."
      );
    }

    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}