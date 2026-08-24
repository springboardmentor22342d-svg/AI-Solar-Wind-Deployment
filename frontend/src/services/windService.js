export function getWindFeatures(analysisData) {
  if (!analysisData) {
    return null;
  }

  return analysisResult.wind_features || null;
}