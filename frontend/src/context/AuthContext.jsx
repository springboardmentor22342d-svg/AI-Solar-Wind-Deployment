import { useState } from "react";
import { AuthContext } from "./AuthContextObject";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token"));

  const loginUser = (accessToken) => {
    localStorage.setItem("access_token", accessToken);
    setToken(accessToken);
  };

  const logoutUser = () => {
    localStorage.removeItem("access_token");
    setToken(null);
  };

  const isLoggedIn = !!token;

  return (
    <AuthContext.Provider value={{ token, loginUser, logoutUser, isLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
}
