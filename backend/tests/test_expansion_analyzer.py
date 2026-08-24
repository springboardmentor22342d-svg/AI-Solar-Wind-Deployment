from backend.app.optimization.expansion_analyzer import ExpansionAnalyzer

analyzer = ExpansionAnalyzer()


def test_expandable_site():
    site = {
        "land_area": 250,
        "overall_score": 90
    }

    result = analyzer.analyze(site)

    assert result["expansion_status"] == "Expandable"


def test_limited_expansion_site():
    site = {
        "land_area": 150,
        "overall_score": 70
    }

    result = analyzer.analyze(site)

    assert result["expansion_status"] == "Limited Expansion"


def test_not_expandable_site():
    site = {
        "land_area": 60,
        "overall_score": 50
    }

    result = analyzer.analyze(site)

    assert result["expansion_status"] == "Not Expandable"