from app.services.score_normalizer import ScoreNormalizer

normalizer = ScoreNormalizer()

print("Solar Score :", normalizer.normalize_solar(6.8))
print("Wind Score :", normalizer.normalize_wind(8.4))
print("Slope Score :", normalizer.normalize_slope(5))
print("Grid Score :", normalizer.normalize_grid_distance(3))
print("Road Score :", normalizer.normalize_road_distance(1.5))