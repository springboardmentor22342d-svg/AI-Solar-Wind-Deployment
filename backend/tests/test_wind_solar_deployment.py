"""
tests/test_wind_solar_deployment.py – Unit tests for Wind Assessment,
Solar Assessment, and Deployment Strategy services.

Test coverage:
  - Wind classification (all categories + boundaries)
  - Wind capacity factor estimation
  - Wind site classification
  - Solar classification (all categories + boundaries)
  - Solar capacity factor estimation
  - Solar site classification
  - Deployment recommendation (all rule combinations)
  - Confidence score calculation
  - Reason generation
  - Invalid inputs (wrong types, negative values)
  - Boundary values

Run with:
    cd backend
    python -m pytest tests/test_wind_solar_deployment.py -v

"""

import pytest
import sys
import os

# Ensure backend is on the path when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.wind_assessment import (
    calculate_wind_class,
    calculate_capacity_factor,
    classify_wind_site,
    get_wind_assessment_summary,
)
from app.services.solar_assessment import (
    calculate_solar_class,
    calculate_solar_capacity_factor,
    classify_solar_site,
    get_solar_assessment_summary,
)
from app.services.deployment_strategy import (
    recommend_deployment,
    generate_reason,
    confidence_score,
)


# ══════════════════════════════════════════════════════════════════════════════
# WIND ASSESSMENT TESTS
# ══════════════════════════════════════════════════════════════════════════════


class TestCalculateWindClass:
    """Tests for calculate_wind_class()."""

    # ── Normal operation ──────────────────────────────────────────────────────

    def test_class_1_well_below_threshold(self):
        assert calculate_wind_class(1.0) == 1

    def test_class_1_near_boundary(self):
        assert calculate_wind_class(2.9) == 1

    def test_class_1_at_zero(self):
        assert calculate_wind_class(0.0) == 1

    def test_class_2_at_lower_boundary(self):
        """Exactly 3 m/s → Moderate (class 2)."""
        assert calculate_wind_class(3.0) == 2

    def test_class_2_mid(self):
        assert calculate_wind_class(4.0) == 2

    def test_class_2_near_upper_boundary(self):
        assert calculate_wind_class(4.9) == 2

    def test_class_3_at_lower_boundary(self):
        """Exactly 5 m/s → Good (class 3)."""
        assert calculate_wind_class(5.0) == 3

    def test_class_3_mid(self):
        assert calculate_wind_class(6.0) == 3

    def test_class_3_near_upper_boundary(self):
        assert calculate_wind_class(6.9) == 3

    def test_class_4_at_lower_boundary(self):
        """Exactly 7 m/s → Excellent (class 4)."""
        assert calculate_wind_class(7.0) == 4

    def test_class_4_mid(self):
        assert calculate_wind_class(9.0) == 4

    def test_class_4_very_high(self):
        assert calculate_wind_class(20.0) == 4

    def test_accepts_integer_input(self):
        assert calculate_wind_class(5) == 3

    def test_accepts_float_input(self):
        assert calculate_wind_class(5.0) == 3

    # ── Invalid inputs ────────────────────────────────────────────────────────

    def test_negative_wind_speed_raises_value_error(self):
        with pytest.raises(ValueError, match="non-negative"):
            calculate_wind_class(-1.0)

    def test_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_wind_class("5.0")

    def test_none_input_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_wind_class(None)

    def test_list_input_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_wind_class([5.0])


class TestCalculateCapacityFactor:
    """Tests for calculate_capacity_factor()."""

    # ── Normal operation ──────────────────────────────────────────────────────

    def test_below_cut_in_returns_minimum(self):
        """Speeds below 3 m/s return minimal CF."""
        assert calculate_capacity_factor(0.0) == 5.0
        assert calculate_capacity_factor(2.9) == 5.0

    def test_near_cut_in_returns_low_cf(self):
        assert calculate_capacity_factor(3.0) == 15.0
        assert calculate_capacity_factor(3.5) == 15.0

    def test_low_moderate_speed(self):
        assert calculate_capacity_factor(4.0) == 22.0

    def test_moderate_speed(self):
        assert calculate_capacity_factor(5.0) == 30.0

    def test_good_speed(self):
        assert calculate_capacity_factor(6.0) == 38.0

    def test_good_upper_end(self):
        assert calculate_capacity_factor(6.9) == 38.0

    def test_very_good_speed(self):
        assert calculate_capacity_factor(7.0) == 45.0

    def test_excellent_speed(self):
        assert calculate_capacity_factor(8.0) == 52.0

    def test_exceptional_speed(self):
        assert calculate_capacity_factor(9.0) == 58.0
        assert calculate_capacity_factor(15.0) == 58.0

    def test_returns_percentage_in_range(self):
        """All realistic wind speeds should return a CF in [0, 100]."""
        for spd in [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]:
            cf = calculate_capacity_factor(spd)
            assert 0.0 <= cf <= 100.0, f"CF={cf} out of range for speed={spd}"

    # ── Invalid inputs ────────────────────────────────────────────────────────

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_capacity_factor(-0.1)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_capacity_factor("fast")

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_capacity_factor(None)


class TestClassifyWindSite:
    """Tests for classify_wind_site()."""

    # ── Normal operation ──────────────────────────────────────────────────────

    def test_poor_site(self):
        assert classify_wind_site(0.0) == "Poor"
        assert classify_wind_site(2.9) == "Poor"

    def test_moderate_site_lower_boundary(self):
        assert classify_wind_site(3.0) == "Moderate"

    def test_moderate_site_mid(self):
        assert classify_wind_site(4.0) == "Moderate"

    def test_moderate_site_upper(self):
        assert classify_wind_site(4.99) == "Moderate"

    def test_good_site_lower_boundary(self):
        assert classify_wind_site(5.0) == "Good"

    def test_good_site_mid(self):
        assert classify_wind_site(6.0) == "Good"

    def test_good_site_upper(self):
        assert classify_wind_site(6.99) == "Good"

    def test_excellent_site_lower_boundary(self):
        assert classify_wind_site(7.0) == "Excellent"

    def test_excellent_site_high(self):
        assert classify_wind_site(12.0) == "Excellent"

    # ── Invalid inputs ────────────────────────────────────────────────────────

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            classify_wind_site(-5.0)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            classify_wind_site("good")


class TestGetWindAssessmentSummary:
    """Tests for get_wind_assessment_summary()."""

    def test_returns_all_keys(self):
        result = get_wind_assessment_summary(6.5)
        assert "wind_speed_ms" in result
        assert "wind_class" in result
        assert "classification" in result
        assert "capacity_factor" in result

    def test_values_are_consistent(self):
        """Summary values must agree with the individual functions."""
        spd = 6.5
        summary = get_wind_assessment_summary(spd)
        assert summary["wind_class"] == calculate_wind_class(spd)
        assert summary["classification"] == classify_wind_site(spd)
        assert summary["capacity_factor"] == calculate_capacity_factor(spd)
        assert summary["wind_speed_ms"] == spd

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            get_wind_assessment_summary(-1.0)


# ══════════════════════════════════════════════════════════════════════════════
# SOLAR ASSESSMENT TESTS
# ══════════════════════════════════════════════════════════════════════════════


class TestCalculateSolarClass:
    """Tests for calculate_solar_class()."""

    def test_class_1_poor(self):
        assert calculate_solar_class(0.0) == 1
        assert calculate_solar_class(3.4) == 1

    def test_class_2_moderate_lower_boundary(self):
        assert calculate_solar_class(3.5) == 2

    def test_class_2_moderate_mid(self):
        assert calculate_solar_class(4.0) == 2

    def test_class_2_near_upper(self):
        assert calculate_solar_class(4.49) == 2

    def test_class_3_good_lower_boundary(self):
        assert calculate_solar_class(4.5) == 3

    def test_class_3_good_mid(self):
        assert calculate_solar_class(5.0) == 3

    def test_class_3_near_upper(self):
        assert calculate_solar_class(5.49) == 3

    def test_class_4_excellent_lower_boundary(self):
        assert calculate_solar_class(5.5) == 4

    def test_class_4_excellent_high(self):
        assert calculate_solar_class(8.0) == 4

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_solar_class(-1.0)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_solar_class("sunny")

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_solar_class(None)


class TestCalculateSolarCapacityFactor:
    """Tests for calculate_solar_capacity_factor()."""

    def test_very_low_irradiance(self):
        assert calculate_solar_capacity_factor(0.0) == 5.0
        assert calculate_solar_capacity_factor(1.9) == 5.0

    def test_low_irradiance(self):
        assert calculate_solar_capacity_factor(2.0) == 12.0

    def test_moderate_irradiance(self):
        assert calculate_solar_capacity_factor(3.5) == 17.0

    def test_good_irradiance(self):
        assert calculate_solar_capacity_factor(4.5) == 20.0

    def test_very_good_irradiance(self):
        assert calculate_solar_capacity_factor(5.5) == 24.0

    def test_excellent_irradiance(self):
        assert calculate_solar_capacity_factor(6.5) == 27.0

    def test_exceptional_irradiance(self):
        assert calculate_solar_capacity_factor(7.5) == 30.0
        assert calculate_solar_capacity_factor(10.0) == 30.0

    def test_returns_percentage_in_valid_range(self):
        for irr in [0.0, 2.0, 4.0, 5.5, 7.0, 9.0]:
            cf = calculate_solar_capacity_factor(irr)
            assert 0.0 <= cf <= 100.0

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_solar_capacity_factor(-0.5)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            calculate_solar_capacity_factor("bright")


class TestClassifySolarSite:
    """Tests for classify_solar_site()."""

    def test_poor_site(self):
        assert classify_solar_site(0.0) == "Poor"
        assert classify_solar_site(3.4) == "Poor"

    def test_moderate_site_lower_boundary(self):
        assert classify_solar_site(3.5) == "Moderate"

    def test_moderate_site_mid(self):
        assert classify_solar_site(4.0) == "Moderate"

    def test_good_site_lower_boundary(self):
        assert classify_solar_site(4.5) == "Good"

    def test_good_site_mid(self):
        assert classify_solar_site(5.0) == "Good"

    def test_excellent_site_lower_boundary(self):
        assert classify_solar_site(5.5) == "Excellent"

    def test_excellent_site_high(self):
        assert classify_solar_site(9.0) == "Excellent"

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            classify_solar_site(-1.0)

    def test_string_raises_type_error(self):
        with pytest.raises(TypeError):
            classify_solar_site("high")


class TestGetSolarAssessmentSummary:
    """Tests for get_solar_assessment_summary()."""

    def test_returns_all_keys(self):
        result = get_solar_assessment_summary(5.0)
        assert "solar_irradiance_kwh" in result
        assert "solar_class" in result
        assert "classification" in result
        assert "capacity_factor" in result

    def test_values_are_consistent(self):
        irr = 5.0
        summary = get_solar_assessment_summary(irr)
        assert summary["solar_class"] == calculate_solar_class(irr)
        assert summary["classification"] == classify_solar_site(irr)
        assert summary["capacity_factor"] == calculate_solar_capacity_factor(irr)
        assert summary["solar_irradiance_kwh"] == irr

    def test_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            get_solar_assessment_summary(-1.0)


# ══════════════════════════════════════════════════════════════════════════════
# DEPLOYMENT STRATEGY TESTS
# ══════════════════════════════════════════════════════════════════════════════


class TestRecommendDeployment:
    """Tests for recommend_deployment()."""

    # ── Key rule scenarios ────────────────────────────────────────────────────

    def test_excellent_solar_poor_wind_recommends_solar(self):
        result = recommend_deployment(solar_irradiance=6.0, wind_speed=1.0)
        assert result["deployment"] == "Solar"
        assert result["solar_class"] == "Excellent"
        assert result["wind_class"] == "Poor"

    def test_poor_solar_excellent_wind_recommends_wind(self):
        result = recommend_deployment(solar_irradiance=2.0, wind_speed=8.0)
        assert result["deployment"] == "Wind"
        assert result["solar_class"] == "Poor"
        assert result["wind_class"] == "Excellent"

    def test_excellent_solar_excellent_wind_recommends_hybrid(self):
        result = recommend_deployment(solar_irradiance=6.0, wind_speed=8.0)
        assert result["deployment"] == "Hybrid"

    def test_good_solar_good_wind_recommends_hybrid(self):
        result = recommend_deployment(solar_irradiance=5.0, wind_speed=6.0)
        assert result["deployment"] == "Hybrid"

    def test_moderate_solar_excellent_wind_recommends_wind(self):
        result = recommend_deployment(solar_irradiance=4.0, wind_speed=8.0)
        assert result["deployment"] == "Wind"

    def test_excellent_solar_moderate_wind_recommends_solar(self):
        result = recommend_deployment(solar_irradiance=6.0, wind_speed=4.0)
        assert result["deployment"] == "Solar"

    def test_poor_solar_poor_wind_not_recommended(self):
        result = recommend_deployment(solar_irradiance=1.0, wind_speed=1.0)
        assert result["deployment"] == "Not Recommended"

    # ── Response structure ────────────────────────────────────────────────────

    def test_response_contains_required_keys(self):
        result = recommend_deployment(6.0, 8.0)
        assert "deployment" in result
        assert "confidence" in result
        assert "reason" in result
        assert "solar_class" in result
        assert "wind_class" in result

    def test_deployment_is_valid_category(self):
        valid_deployments = {"Solar", "Wind", "Hybrid", "Not Recommended"}
        result = recommend_deployment(5.5, 7.0)
        assert result["deployment"] in valid_deployments

    def test_confidence_is_within_valid_range(self):
        result = recommend_deployment(5.5, 7.0)
        assert 10 <= result["confidence"] <= 99

    def test_reason_is_non_empty_string(self):
        result = recommend_deployment(5.5, 7.0)
        assert isinstance(result["reason"], str)
        assert len(result["reason"]) > 0

    # ── All 16 rule combinations ──────────────────────────────────────────────

    @pytest.mark.parametrize("solar_irr,wind_spd,expected_deployment", [
        # Excellent Solar (≥5.5) + all wind classes
        (6.0, 8.0, "Hybrid"),           # Exc + Exc
        (6.0, 6.0, "Hybrid"),           # Exc + Good
        (6.0, 4.0, "Solar"),            # Exc + Moderate
        (6.0, 1.0, "Solar"),            # Exc + Poor
        # Good Solar (4.5–5.5) + all wind classes
        (5.0, 8.0, "Hybrid"),           # Good + Exc
        (5.0, 6.0, "Hybrid"),           # Good + Good
        (5.0, 4.0, "Solar"),            # Good + Moderate
        (5.0, 1.0, "Solar"),            # Good + Poor
        # Moderate Solar (3.5–4.5) + all wind classes
        (4.0, 8.0, "Wind"),             # Moderate + Exc
        (4.0, 6.0, "Wind"),             # Moderate + Good
        (4.0, 4.0, "Solar"),            # Moderate + Moderate
        (4.0, 1.0, "Solar"),            # Moderate + Poor
        # Poor Solar (<3.5) + all wind classes
        (2.0, 8.0, "Wind"),             # Poor + Exc
        (2.0, 6.0, "Wind"),             # Poor + Good
        (2.0, 4.0, "Wind"),             # Poor + Moderate
        (2.0, 1.0, "Not Recommended"),  # Poor + Poor
    ])
    def test_all_16_rule_combinations(self, solar_irr, wind_spd, expected_deployment):
        result = recommend_deployment(solar_irr, wind_spd)
        assert result["deployment"] == expected_deployment, (
            f"solar={solar_irr}, wind={wind_spd} → expected {expected_deployment!r}, "
            f"got {result['deployment']!r}"
        )

    # ── Invalid inputs ────────────────────────────────────────────────────────

    def test_negative_solar_raises_value_error(self):
        with pytest.raises(ValueError):
            recommend_deployment(solar_irradiance=-1.0, wind_speed=5.0)

    def test_negative_wind_raises_value_error(self):
        with pytest.raises(ValueError):
            recommend_deployment(solar_irradiance=5.0, wind_speed=-1.0)

    def test_string_solar_raises_type_error(self):
        with pytest.raises(TypeError):
            recommend_deployment(solar_irradiance="high", wind_speed=5.0)

    def test_string_wind_raises_type_error(self):
        with pytest.raises(TypeError):
            recommend_deployment(solar_irradiance=5.0, wind_speed="fast")

    def test_none_solar_raises_type_error(self):
        with pytest.raises(TypeError):
            recommend_deployment(solar_irradiance=None, wind_speed=5.0)


class TestGenerateReason:
    """Tests for generate_reason()."""

    def test_excellent_solar_poor_wind_reason(self):
        reason = generate_reason("Excellent", "Poor")
        assert isinstance(reason, str)
        assert len(reason) > 0
        assert "solar" in reason.lower() or "wind" in reason.lower()

    def test_poor_solar_excellent_wind_reason(self):
        reason = generate_reason("Poor", "Excellent")
        assert "wind" in reason.lower()

    def test_excellent_both_reason(self):
        reason = generate_reason("Excellent", "Excellent")
        assert isinstance(reason, str)
        assert len(reason) > 0

    def test_invalid_solar_class_raises_value_error(self):
        with pytest.raises(ValueError):
            generate_reason("Outstanding", "Good")

    def test_invalid_wind_class_raises_value_error(self):
        with pytest.raises(ValueError):
            generate_reason("Good", "Extraordinary")

    def test_invalid_type_raises_type_error(self):
        with pytest.raises(TypeError):
            generate_reason(4, "Good")

    def test_all_valid_combinations_return_strings(self):
        classes = ["Poor", "Moderate", "Good", "Excellent"]
        for solar_c in classes:
            for wind_c in classes:
                result = generate_reason(solar_c, wind_c)
                assert isinstance(result, str), (
                    f"Reason for ({solar_c}, {wind_c}) is not a string: {result!r}"
                )


class TestConfidenceScore:
    """Tests for confidence_score()."""

    # ── Score range validation ────────────────────────────────────────────────

    def test_all_scores_within_valid_range(self):
        classes = ["Poor", "Moderate", "Good", "Excellent"]
        for solar_c in classes:
            for wind_c in classes:
                score = confidence_score(solar_c, wind_c)
                assert 10 <= score <= 99, (
                    f"Score={score} for ({solar_c}, {wind_c}) is outside [10, 99]"
                )

    # ── Specific values ───────────────────────────────────────────────────────

    def test_both_excellent_highest_confidence(self):
        score = confidence_score("Excellent", "Excellent")
        assert score >= 90, f"Expected high confidence for dual-Excellent, got {score}"

    def test_both_poor_lowest_confidence(self):
        score = confidence_score("Poor", "Poor")
        assert score <= 30, f"Expected low confidence for dual-Poor, got {score}"

    def test_returns_integer(self):
        score = confidence_score("Good", "Good")
        assert isinstance(score, int)

    # ── Invalid inputs ────────────────────────────────────────────────────────

    def test_invalid_solar_class_raises_value_error(self):
        with pytest.raises(ValueError):
            confidence_score("Unknown", "Good")

    def test_invalid_wind_class_raises_value_error(self):
        with pytest.raises(ValueError):
            confidence_score("Good", "None")

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            confidence_score(None, "Good")

    def test_integer_raises_type_error(self):
        with pytest.raises(TypeError):
            confidence_score("Good", 3)


# ══════════════════════════════════════════════════════════════════════════════
# BOUNDARY VALUE TESTS (cross-cutting)
# ══════════════════════════════════════════════════════════════════════════════


class TestBoundaryValues:
    """Precise boundary value tests to prevent off-by-one errors."""

    # Wind speed boundaries
    def test_wind_boundary_at_3ms(self):
        """3.0 m/s is the exact lower bound of Moderate."""
        assert classify_wind_site(3.0) == "Moderate"
        assert calculate_wind_class(3.0) == 2

    def test_wind_boundary_just_below_3ms(self):
        assert classify_wind_site(2.999) == "Poor"
        assert calculate_wind_class(2.999) == 1

    def test_wind_boundary_at_5ms(self):
        """5.0 m/s is the exact lower bound of Good."""
        assert classify_wind_site(5.0) == "Good"
        assert calculate_wind_class(5.0) == 3

    def test_wind_boundary_just_below_5ms(self):
        assert classify_wind_site(4.999) == "Moderate"

    def test_wind_boundary_at_7ms(self):
        """7.0 m/s is the exact lower bound of Excellent."""
        assert classify_wind_site(7.0) == "Excellent"
        assert calculate_wind_class(7.0) == 4

    def test_wind_boundary_just_below_7ms(self):
        assert classify_wind_site(6.999) == "Good"

    # Solar irradiance boundaries
    def test_solar_boundary_at_3_5(self):
        """3.5 kWh/m²/day is the exact lower bound of Moderate."""
        assert classify_solar_site(3.5) == "Moderate"
        assert calculate_solar_class(3.5) == 2

    def test_solar_boundary_just_below_3_5(self):
        assert classify_solar_site(3.499) == "Poor"

    def test_solar_boundary_at_4_5(self):
        """4.5 kWh/m²/day is the exact lower bound of Good."""
        assert classify_solar_site(4.5) == "Good"
        assert calculate_solar_class(4.5) == 3

    def test_solar_boundary_just_below_4_5(self):
        assert classify_solar_site(4.499) == "Moderate"

    def test_solar_boundary_at_5_5(self):
        """5.5 kWh/m²/day is the exact lower bound of Excellent."""
        assert classify_solar_site(5.5) == "Excellent"
        assert calculate_solar_class(5.5) == 4

    def test_solar_boundary_just_below_5_5(self):
        assert classify_solar_site(5.499) == "Good"

    # Zero inputs (edge case)
    def test_zero_wind_speed_is_poor(self):
        assert classify_wind_site(0.0) == "Poor"
        assert calculate_wind_class(0.0) == 1
        assert calculate_capacity_factor(0.0) == 5.0

    def test_zero_solar_irradiance_is_poor(self):
        assert classify_solar_site(0.0) == "Poor"
        assert calculate_solar_class(0.0) == 1
        assert calculate_solar_capacity_factor(0.0) == 5.0
