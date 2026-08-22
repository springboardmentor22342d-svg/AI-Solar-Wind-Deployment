import { useState, useEffect } from "react";
import { fetchGuidelines } from "../api/analysis";

function GuidelinesPanel() {
  const [guidelines, setGuidelines] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    fetchGuidelines()
      .then(setGuidelines)
      .catch(() => setGuidelines(null));
  }, []);

  if (!guidelines) return null;

  return (
    <div className="guidelines-panel">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="guidelines-toggle"
      >
        {isOpen ? "▼" : "▶"} What makes a good site? (Guidelines)
      </button>

      {isOpen && (
        <div className="guidelines-content">
          <h4>Solar Irradiance</h4>
          <table className="guidelines-table">
            <tbody>
              {guidelines.solar_irradiance_guide.map((g, i) => (
                <tr key={i}>
                  <td>{g.range}</td>
                  <td>{g.rating}</td>
                  <td>{g.description}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h4>Wind Speed</h4>
          <table className="guidelines-table">
            <tbody>
              {guidelines.wind_speed_guide.map((g, i) => (
                <tr key={i}>
                  <td>{g.range}</td>
                  <td>{g.rating}</td>
                  <td>{g.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default GuidelinesPanel;
