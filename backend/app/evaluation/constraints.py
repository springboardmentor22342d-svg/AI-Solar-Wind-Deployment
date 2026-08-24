MAX_SLOPE = 15
MIN_SOLAR = 5
MIN_WIND = 4
MAX_GRID_DISTANCE = 5
MAX_ROAD_DISTANCE = 2
def check_slope(value):
    return value <= MAX_SLOPE
def check_solar(value):
    return value >= MIN_SOLAR
def check_wind(value):
    return value >= MIN_WIND
def check_grid_distance(value):
    return value <= MAX_GRID_DISTANCE
def check_road_distance(value):
    return value <= MAX_ROAD_DISTANCE