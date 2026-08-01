import requests
import rasterio
from rasterio.merge import merge


url = "https://portal.opentopography.org/API/globaldem"
API_KEY = "9c0015ef25d572a2019fb11abba84a7f"  

bands = [
    {"south": 8.0, "north": 16.67, "name": "south"},
    {"south": 16.67, "north": 25.33, "name": "central"},
    {"south": 25.33, "north": 34.0, "name": "north"},
]

if __name__ == "__main__":
    for band in bands:
        params = {
            "demtype": "SRTMGL3",
            "south": band["south"], "north": band["north"],
            "west": 68.0, "east": 97.5,
            "outputFormat": "GTiff",
            "API_Key": API_KEY,
        }
        response = requests.get(url, params=params)
        filename = f"../datasets/srtm/india_{band['name']}.tif"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved {filename} — status {response.status_code}, size {len(response.content)} bytes")


files = [
    "../datasets/srtm/india_south.tif",
    "../datasets/srtm/india_central.tif",
    "../datasets/srtm/india_north.tif",
]

if __name__ == "__main__":
    datasets = [rasterio.open(f) for f in files]
    merged_array, merged_transform = merge(datasets)

    out_meta = datasets[0].meta.copy()
    out_meta.update({
        "height": merged_array.shape[1],
        "width": merged_array.shape[2],
        "transform": merged_transform,
    })

    with rasterio.open("../datasets/srtm/india_elevation.tif", "w", **out_meta) as dest:
        dest.write(merged_array)

    for d in datasets:
        d.close()

    print("Merged file saved to datasets/srtm/india_elevation.tif")