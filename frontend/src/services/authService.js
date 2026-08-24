const USERS_KEY = "solar_wind_users";
const CURRENT_USER_KEY = "solar_wind_current_user";

export const registerUser = (name, email, password) => {
  const users = JSON.parse(localStorage.getItem(USERS_KEY) || "[]");

  const existingUser = users.find(
    (user) => user.email.toLowerCase() === email.toLowerCase()
  );

  if (existingUser) {
    return {
      success: false,
      message: "An account with this email already exists."
    };
  }

  const newUser = {
    id: Date.now(),
    name,
    email,
    password
  };

  users.push(newUser);

  localStorage.setItem(USERS_KEY, JSON.stringify(users));

  localStorage.setItem(
    CURRENT_USER_KEY,
    JSON.stringify({
      id: newUser.id,
      name: newUser.name,
      email: newUser.email
    })
  );

  return {
    success: true,
    user: newUser
  };
};

export const loginUser = (email, password) => {
  const users = JSON.parse(localStorage.getItem(USERS_KEY) || "[]");

  const user = users.find(
    (item) =>
      item.email.toLowerCase() === email.toLowerCase() &&
      item.password === password
  );

  if (!user) {
    return {
      success: false,
      message: "Invalid email or password."
    };
  }

  const loggedInUser = {
    id: user.id,
    name: user.name,
    email: user.email
  };

  localStorage.setItem(
    CURRENT_USER_KEY,
    JSON.stringify(loggedInUser)
  );

  return {
    success: true,
    user: loggedInUser
  };
};

export const logoutUser = () => {
  localStorage.removeItem(CURRENT_USER_KEY);
};

export const getCurrentUser = () => {
  const user = localStorage.getItem(CURRENT_USER_KEY);

  return user ? JSON.parse(user) : null;
};

export const isLoggedIn = () => {
  return getCurrentUser() !== null;
};