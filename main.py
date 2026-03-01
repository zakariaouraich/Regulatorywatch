from __future__ import annotations

from fastapi import FastAPI

from app.config import DEFAULT_FEEDS, load_firm_profile
from app.fca_client import fetch_feed
from app.impact import assess_impact
from app.models import AnalyzedUpdate, ScanRequest, ScanResponse
from app.relevance import assess_relevance

app = FastAPI(title="Regulatory Watch API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/firm-profile")
def get_firm_profile():
    return load_firm_profile()


@app.post("/scan-updates", response_model=ScanResponse)
async def scan_updates(req: ScanRequest) -> ScanResponse:
    profile = load_firm_profile()

    all_updates = []
    for feed in DEFAULT_FEEDS:
        updates = await fetch_feed(feed)
        all_updates.extend(updates)

    deduped = {u.id: u for u in all_updates}
    sorted_updates = sorted(
        deduped.values(), key=lambda x: x.published or 0, reverse=True
    )[: req.limit]

    analyzed: list[AnalyzedUpdate] = []
    for update in sorted_updates:
        relevance = assess_relevance(update, profile)
        if relevance.score < req.min_relevance_score:
            continue
        impact = assess_impact(update)
        analyzed.append(AnalyzedUpdate(update=update, relevance=relevance, impact=impact))

    return ScanResponse(
        profile=profile,
        scanned_count=len(sorted_updates),
        relevant_count=len(analyzed),
        results=analyzed,
    )
