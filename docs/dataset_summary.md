# Dataset Summary

## NASA POWER
- **Source:** NASA Langley Research Center Power API
- **URL:** https://power.larc.nasa.gov/api/temporal/climatology/point
- **Parameters Used:** ALLSKY_SFC_SW_DWN (solar irradiance), T2M (temperature), RH2M (humidity)
- **Format:** JSON (REST API, no download required)
- **Used For:** Solar Prediction, Site Analysis

## Global Wind Atlas
- **Source:** DTU Wind Energy / World Bank
- **URL:** https://globalwindatlas.info
- **Parameters Used:** Wind speed at 10m, 50m, 100m; Wind Power Density
- **Format:** GeoTIFF rasters / REST API
- **Used For:** Wind Prediction, Site Analysis

## SRTM (Shuttle Radar Topography Mission)
- **Source:** NASA / USGS
- **URL:** https://www2.jpl.nasa.gov/srtm/
- **Parameters Used:** Elevation (m), Derived Slope (degrees)
- **Format:** GeoTIFF rasters (1 arc-second resolution)
- **Used For:** Terrain scoring in site suitability

## OpenStreetMap (OSM)
- **Source:** OpenStreetMap Foundation / Geofabrik
- **URL:** https://download.geofabrik.de/
- **Parameters Used:** Road networks, power grid lines, substations
- **Format:** Shapefile / GeoJSON
- **Used For:** Infrastructure proximity in site analysis

## Sentinel-2 (Copernicus)
- **Source:** ESA Copernicus Programme
- **URL:** https://scihub.copernicus.eu/
- **Parameters Used:** NDVI (vegetation index), NDWI (water index), Land Cover Classification
- **Format:** GeoTIFF multispectral rasters
- **Used For:** Environmental scoring in site suitability
