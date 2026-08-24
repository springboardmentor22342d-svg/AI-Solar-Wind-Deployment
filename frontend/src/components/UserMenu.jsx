import { useState } from "react";
import { logoutUser } from "../services/authService";

function UserMenu({ user, onLogout }) {
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logoutUser();

    setOpen(false);

    onLogout();
  };

  const firstLetter =
    user?.name?.charAt(0)?.toUpperCase() || "U";

  return (
    <div className="user-menu">

      <button
        className="user-profile-button"
        onClick={() => setOpen(!open)}
      >

        <div className="user-avatar">
          {firstLetter}
        </div>

        <div className="user-details">

          <strong>
            {user?.name}
          </strong>

          <span>
            Renewable Analyst
          </span>

        </div>

        <span className="user-arrow">
          {open ? "▲" : "▼"}
        </span>

      </button>

      {open && (
        <div className="user-dropdown">

          <div className="dropdown-user">

            <div className="dropdown-avatar">
              {firstLetter}
            </div>

            <div>
              <strong>
                {user?.name}
              </strong>

              <span>
                {user?.email}
              </span>
            </div>

          </div>

          <div className="dropdown-divider" />

          <button className="dropdown-item">
            <span>👤</span>
            My Profile
          </button>

          <button className="dropdown-item">
            <span>📍</span>
            My Analyses
          </button>

          <button className="dropdown-item">
            <span>📁</span>
            My Projects
          </button>

          <button className="dropdown-item">
            <span>📊</span>
            My Reports
          </button>

          <div className="dropdown-divider" />

          <button
            className="dropdown-item logout-item"
            onClick={handleLogout}
          >
            <span>↪</span>
            Logout
          </button>

        </div>
      )}

    </div>
  );
}

export default UserMenu;