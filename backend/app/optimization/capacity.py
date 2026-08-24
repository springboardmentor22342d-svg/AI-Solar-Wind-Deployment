def recommend_capacity(site):
    land = site.get("land_area",0)
    if land >= 100:
        return 100
    elif land >= 50:
        return 50
    elif land >= 20:
        return 20
    else:
        return 10