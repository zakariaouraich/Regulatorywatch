from __future__ import annotations

from app.models import FirmProfile, RegulatoryUpdate, RelevanceResult

BASE_KEYWORDS = {
    "mifid": 0.25,
    "client money": 0.2,
    "conduct": 0.15,
    "governance": 0.15,
    "prudential": 0.2,
    "financial crime": 0.2,
    "market abuse": 0.2,
    "reporting": 0.15,
    "fund": 0.1,
    "investment": 0.1,
    "real estate": 0.1,
}


def assess_relevance(update: RegulatoryUpdate, profile: FirmProfile) -> RelevanceResult:
    text = f"{update.title} {update.summary}".lower()

    score = 0.0
    matched = []

    for keyword, weight in BASE_KEYWORDS.items():
        if keyword in text:
            score += weight
            matched.append(keyword)

    for permission in profile.permissions:
        p = permission.lower()
        if p in text:
            score += 0.25
            matched.append(permission)

    for tag in profile.business_tags:
        t = tag.lower()
        if t in text:
            score += 0.15
            matched.append(tag)

    capped_score = min(score, 1.0)
    relevant = capped_score >= 0.3

    rationale = (
        "Potentially relevant to firm permissions/business model."
        if relevant
        else "Low confidence relevance based on current keyword model."
    )

    return RelevanceResult(
        is_relevant=relevant,
        score=round(capped_score, 2),
        matched_keywords=sorted(set(matched)),
        rationale=rationale,
    )
