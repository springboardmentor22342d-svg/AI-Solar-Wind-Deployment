import React from "react";
import { Settings } from "lucide-react";

export default function SettingsPage() {

  return (
    <div className="page-content">

      <div className="page-title">

        <Settings />

        <div>
          <h1>Settings</h1>

          <p>
            Configure your platform preferences.
          </p>
        </div>

      </div>

      <div className="settings-card">

        <h3>Appearance</h3>

        <label>
          <span>Dark Mode</span>
          <input
            type="checkbox"
            defaultChecked
          />
        </label>

      </div>

      <div className="settings-card">

        <h3>Notifications</h3>

        <label>
          <span>Site alerts</span>
          <input
            type="checkbox"
            defaultChecked
          />
        </label>

        <label>
          <span>AI recommendations</span>
          <input
            type="checkbox"
            defaultChecked
          />
        </label>

      </div>

    </div>
  );
}