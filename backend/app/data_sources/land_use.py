from pathlib import Path
import pandas as pd
import reverse_geocoder as rg

class LandUseClient:
    """
    Accesses state-wise land use data (forest %, agricultural %,
    wasteland %, etc.) for a given coordinate. Since the underlying
    dataset is state-level (not point-level like the other sources),
    this client reverse-geocodes the coordinate to a state first,
    then looks up that state's land use percentages.
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    LANDUSE_CSV = BASE_DIR / "datasets" / "sentinel" / "states_land_use_pattern.csv"

    # Known mismatches between reverse_geocoder's state names and this CSV
    STATE_NAME_FIXES = {
        "Maharashtra": "Mahrashtra",
        "Telangana": "Andhra Pradesh",
        "Andaman and Nicobar Islands": "Andaman & Nicobar Islands",
        "Laccadives": "Lakshwadeep",
    }

    def __init__(self):
        self.landuse_df = pd.read_csv(self.LANDUSE_CSV)
        self.geocoder = rg.RGeocoder(mode=1, verbose=False)

    def fetch(self, latitude: float, longitude: float) -> dict:
        try:
            result = self.geocoder.query([(latitude, longitude)])
            state_name = result[0]["admin1"]
            state_name = self.STATE_NAME_FIXES.get(state_name, state_name)

            match = self.landuse_df[
                (self.landuse_df["States/UTs"].str.lower() == state_name.lower()) &
                (self.landuse_df["Category"] == "Percentage to Geographical Area")
            ]
            if match.empty:
                return {
                    "forest_pct": None,
                    "net_area_sown_pct": None,
                    "fallow_land_pct": None,
                    "culturable_wasteland_pct": None,
                }

            row = match.iloc[0]
            return {
                "forest_pct": float(row["Forests"]),
                "net_area_sown_pct": float(row["Net area sown"]),
                "fallow_land_pct": float(row["Current fallows"]),
                "culturable_wasteland_pct": float(row["Culturable wasteland"]),
            }
        except Exception:
            return {
                "forest_pct": None,
                "net_area_sown_pct": None,
                "fallow_land_pct": None,
                "culturable_wasteland_pct": None,
            }
