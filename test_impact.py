from app.impact import assess_impact
from app.models import RegulatoryUpdate


def test_impact_returns_targeted_rules_for_financial_crime():
    update = RegulatoryUpdate(
        id="1",
        title="FCA guidance on financial crime systems",
        link="https://example.com",
        summary="firms should enhance AML controls",
        source="test",
    )

    impact = assess_impact(update)

    assert any("AML" in item for item in impact.operational_impact)
    assert any("Financial Crime" in item for item in impact.policy_gap_review_areas)
