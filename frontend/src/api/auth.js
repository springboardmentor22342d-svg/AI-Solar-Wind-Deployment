const API_BASE_URL = "http://127.0.0.1:8000";

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email); // FastAPI's OAuth2 form expects "username"
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Invalid email or password.");
  }

  return response.json(); // { access_token, token_type }
}

export async function register(name, email, password) {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Registration failed.");
  }

  return response.json();
}