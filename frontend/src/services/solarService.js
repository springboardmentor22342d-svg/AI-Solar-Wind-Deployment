import { getSolarFeatures } from "./api";

export async function fetchSolarFeatures(latitude, longitude) {
  return await getSolarFeatures(latitude, longitude);
}