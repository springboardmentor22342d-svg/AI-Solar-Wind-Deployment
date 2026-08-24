def expansion_status(site):
    land = site.get("land_area",0)
    if land >= 100:
        return "Expandable"
    elif land >= 40:
        return "Limited Expansion"
    else:
        return "Not Expandable"