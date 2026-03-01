from __future__ import annotations

from app.models import ImpactAssessment, RegulatoryUpdate

IMPACT_RULES = {
    "client money": {
        "operational": "Review client money handling workflows and reconciliation controls.",
        "opportunity": "Strengthening client asset safeguards can support investor confidence.",
        "policy": "Client Money and Asset Protection Policy",
    },
    "market abuse": {
        "operational": "Assess surveillance, insider list controls, and escalation procedures.",
        "opportunity": "Enhancing market abuse controls can support institutional mandates.",
        "policy": "Market Abuse and Personal Account Dealing Policy",
    },
    "prudential": {
        "operational": "Revisit capital and liquidity monitoring, stress testing, and ICARA assumptions.",
        "opportunity": "Stronger prudential planning can support growth initiatives.",
        "policy": "Prudential Risk Management and ICARA Framework",
    },
    "governance": {
        "operational": "Review governance forums, MI quality, and board reporting cadence.",
        "opportunity": "Improved governance can accelerate strategic decision-making.",
        "policy": "Governance and Senior Management Responsibilities Policy",
    },
    "financial crime": {
        "operational": "Update AML/KYC controls and transaction monitoring scenarios where relevant.",
        "opportunity": "Enhanced financial crime controls can streamline onboarding of high-quality clients.",
        "policy": "Financial Crime, AML and Sanctions Policy",
    },
}


def assess_impact(update: RegulatoryUpdate) -> ImpactAssessment:
    text = f"{update.title} {update.summary}".lower()

    operational = []
    opportunities = []
    policy_gaps = []

    for keyword, rules in IMPACT_RULES.items():
        if keyword in text:
            operational.append(rules["operational"])
            opportunities.append(rules["opportunity"])
            policy_gaps.append(rules["policy"])

    if not operational:
        operational.append(
            "Perform manual review to determine process, controls, and reporting implications."
        )
    if not opportunities:
        opportunities.append(
            "Assess whether proactive implementation could improve market positioning or client trust."
        )
    if not policy_gaps:
        policy_gaps.append(
            "Map update to existing compliance policies/procedures and identify any gaps."
        )

    return ImpactAssessment(
        operational_impact=operational,
        business_opportunities=opportunities,
        policy_gap_review_areas=policy_gaps,
    )
