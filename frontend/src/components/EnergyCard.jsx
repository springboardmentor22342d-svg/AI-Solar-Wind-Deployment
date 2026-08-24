import React from "react";
import { Sun, Wind } from "lucide-react";

export default function EnergyCard({
  type = "solar",
  title,
  value,
  subtitle
}) {

  const isSolar = type === "solar";
  const Icon = isSolar ? Sun : Wind;

  return (
    <div className={`energy-card ${type}`}>

      <div className="energy-icon">
        <Icon size={26} />
      </div>

      <div>
        <span>{title}</span>
        <strong>{value}</strong>
        <small>{subtitle}</small>
      </div>

    </div>
  );
}