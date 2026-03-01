from app.models import FirmProfile, RegulatoryUpdate
from app.relevance import assess_relevance


def test_relevance_flags_mifid_real_estate_content():
    profile = FirmProfile(
        name="Test",
        permissions=["portfolio management"],
        business_tags=["real estate"],
    )
    update = RegulatoryUpdate(
        id="1",
        title="FCA updates MiFID reporting expectations for real estate portfolios",
        link="https://example.com",
        summary="Changes to conduct and reporting obligations.",
        source="test",
    )

    result = assess_relevance(update, profile)

    assert result.is_relevant is True
    assert result.score >= 0.3
    assert "mifid" in result.matched_keywords
