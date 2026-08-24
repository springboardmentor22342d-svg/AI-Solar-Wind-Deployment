def recommend(score):
    if score >= 85:
        return "Highly Suitable"
    if score >= 70:
        return "Suitable"
    if score >= 50:
        return "Moderately Suitable"
    return "Not Recommended"