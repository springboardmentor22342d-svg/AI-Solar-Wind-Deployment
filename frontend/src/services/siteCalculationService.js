export function calculateSiteSuitability(data) {
  /*
   * Expected input:
   * solarIrradiance : kWh/m²/day
   * windSpeed       : m/s
   * temperature     : °C
   * humidity        : %
   * elevation       : m
   * slope           : degrees
   * distanceToRoad  : km
   */

  const solarScore = calculateSolarScore(data.solarIrradiance);
  const windScore = calculateWindScore(data.windSpeed);
  const terrainScore = calculateTerrainScore(data.slope);
  const elevationScore = calculateElevationScore(data.elevation);
  const infrastructureScore = calculateInfrastructureScore(
    data.distanceToRoad
  );

  const score =
    solarScore * 0.35 +
    windScore * 0.25 +
    terrainScore * 0.20 +
    elevationScore * 0.10 +
    infrastructureScore * 0.10;

  return {
    total: Math.round(score),

    factors: {
      solar: Math.round(solarScore),
      wind: Math.round(windScore),
      terrain: Math.round(terrainScore),
      elevation: Math.round(elevationScore),
      infrastructure: Math.round(infrastructureScore)
    }
  };
}


/* ---------------- SOLAR ---------------- */

function calculateSolarScore(value) {
  if (value >= 6) return 100;
  if (value >= 5) return 90;
  if (value >= 4) return 75;
  if (value >= 3) return 55;
  return 30;
}


/* ---------------- WIND ---------------- */

function calculateWindScore(value) {
  if (value >= 8) return 100;
  if (value >= 6) return 85;
  if (value >= 4) return 70;
  if (value >= 2) return 50;
  return 25;
}


/* ---------------- TERRAIN ---------------- */

function calculateTerrainScore(slope) {
  if (slope <= 3) return 100;
  if (slope <= 7) return 85;
  if (slope <= 12) return 65;
  if (slope <= 20) return 40;
  return 15;
}


/* ---------------- ELEVATION ---------------- */

function calculateElevationScore(elevation) {
  if (elevation >= 100 && elevation <= 1000) return 100;
  if (elevation < 100) return 80;
  if (elevation <= 1500) return 75;
  return 50;
}


/* ---------------- INFRASTRUCTURE ---------------- */

function calculateInfrastructureScore(distance) {
  if (distance <= 1) return 100;
  if (distance <= 3) return 85;
  if (distance <= 5) return 70;
  if (distance <= 10) return 50;
  return 25;
}


/* =====================================================
   POTENTIAL DISTRIBUTION
===================================================== */

export function calculatePotentialDistribution(score) {
  if (score >= 90) {
    return [
      { name: "Excellent", value: 60 },
      { name: "Very Good", value: 25 },
      { name: "Good", value: 10 },
      { name: "Moderate", value: 4 },
      { name: "Low", value: 1 }
    ];
  }

  if (score >= 75) {
    return [
      { name: "Excellent", value: 35 },
      { name: "Very Good", value: 30 },
      { name: "Good", value: 20 },
      { name: "Moderate", value: 10 },
      { name: "Low", value: 5 }
    ];
  }

  if (score >= 60) {
    return [
      { name: "Excellent", value: 20 },
      { name: "Very Good", value: 25 },
      { name: "Good", value: 30 },
      { name: "Moderate", value: 15 },
      { name: "Low", value: 10 }
    ];
  }

  if (score >= 40) {
    return [
      { name: "Excellent", value: 10 },
      { name: "Very Good", value: 15 },
      { name: "Good", value: 25 },
      { name: "Moderate", value: 30 },
      { name: "Low", value: 20 }
    ];
  }

  return [
    { name: "Excellent", value: 5 },
    { name: "Very Good", value: 10 },
    { name: "Good", value: 15 },
    { name: "Moderate", value: 25 },
    { name: "Low", value: 45 }
  ];
}