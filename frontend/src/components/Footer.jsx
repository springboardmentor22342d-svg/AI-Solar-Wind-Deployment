function Footer() {
  return (
    <footer style={{ marginTop: "3rem", padding: "1rem", borderTop: "1px solid #ddd", fontSize: "0.8rem", color: "#666", textAlign: "center" }}>
      <p>
        Location and infrastructure data © OpenStreetMap contributors, available under the{" "}
        <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">
          Open Database License
        </a>
        . Solar data: NASA POWER / Global Solar Atlas. Wind data: Global Wind Atlas. Elevation: SRTM (OpenTopography). Land boundaries: Natural Earth.
      </p>
    </footer>
  );
}

export default Footer;