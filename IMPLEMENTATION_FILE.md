# Regulatory Watch — Implementation Guide (UK FCA / MiFID)

This guide explains **how to implement and operationalise** the MVP in this repository inside your compliance function.

## 1) Define your firm profile (first thing to do)

Update `data/firm_profile.json` with your real permissions, business model terms, and key products.

Suggested approach:
- Copy FCA permission wording from your permissions notice/register entry.
- Include common internal synonyms used in policy documents and committee packs.
- Add business tags by strategy (e.g., value-add real estate, debt, listed securities, etc.).

This profile directly drives relevance scoring in Step 1.

## 2) Run the service locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and test:
- `GET /health`
- `GET /firm-profile`
- `POST /scan-updates`

## 3) Validate relevance and impact output

Start with a small limit (e.g. 10–20 updates) and review:
- False positives: updates flagged as relevant but not applicable.
- False negatives: updates missed but should be relevant.

Tune by editing `app/relevance.py` and `app/impact.py`:
- Add/remove keywords.
- Adjust weights.
- Add policy area mappings.

## 4) Add daily monitoring workflow

Operational pattern:
1. Run `/scan-updates` daily (cron or scheduler).
2. Persist results to a database.
3. Notify compliance team for items above threshold.
4. Track actions to closure in your governance process.

Minimum governance controls:
- Keep an immutable record of scan outputs.
- Record who reviewed each update and final applicability decision.
- Record policy/procedure changes and effective dates.

## 5) Add policy/procedure gap analysis (next phase)

Once Step 1 is stable:
1. Ingest policy/procedure documents into a searchable corpus.
2. Map each relevant update to impacted obligations.
3. Compare obligations vs controls/policies to identify gaps.
4. Produce action plans with owners and deadlines.

Recommended data model additions:
- `regulatory_obligations`
- `internal_controls`
- `policy_documents`
- `gap_assessments`
- `remediation_actions`

## 6) GitHub implementation cadence

A practical delivery cadence:
- **Sprint 1**: calibrate relevance rules + add persistence.
- **Sprint 2**: notifications + reviewer workflow + audit trail.
- **Sprint 3**: policy corpus ingestion + gap engine.
- **Sprint 4**: management reporting dashboard.

For each sprint:
- Create a branch from `main`.
- Implement one cohesive feature.
- Add/extend tests.
- Open PR with evidence (sample outputs, screenshots if UI).
- Merge after compliance sign-off.

## 7) Production readiness checklist

Before production deployment:
- [ ] Authentication/authorisation on API.
- [ ] Secrets management and environment separation.
- [ ] Monitoring (uptime, failed feed pulls, scoring drift).
- [ ] Data retention policy and backup.
- [ ] Incident and change management procedures.
- [ ] Model/rule governance documentation.

---

If helpful, the next implementation step can be: **adding persistent storage and a daily scheduled scan job**, so outputs are tracked over time and can feed governance reporting.
