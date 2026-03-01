from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class FirmProfile(BaseModel):
    name: str
    regulator: str = "FCA"
    jurisdiction: str = "UK"
    permissions: List[str] = Field(default_factory=list)
    business_tags: List[str] = Field(default_factory=list)


class RegulatoryUpdate(BaseModel):
    id: str
    title: str
    link: str
    summary: str
    published: datetime | None = None
    source: str


class RelevanceResult(BaseModel):
    is_relevant: bool
    score: float = Field(ge=0.0, le=1.0)
    matched_keywords: List[str] = Field(default_factory=list)
    rationale: str


class ImpactAssessment(BaseModel):
    operational_impact: List[str] = Field(default_factory=list)
    business_opportunities: List[str] = Field(default_factory=list)
    policy_gap_review_areas: List[str] = Field(default_factory=list)


class AnalyzedUpdate(BaseModel):
    update: RegulatoryUpdate
    relevance: RelevanceResult
    impact: ImpactAssessment


class ScanRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    min_relevance_score: float = Field(default=0.3, ge=0.0, le=1.0)


class ScanResponse(BaseModel):
    profile: FirmProfile
    scanned_count: int
    relevant_count: int
    results: List[AnalyzedUpdate]
