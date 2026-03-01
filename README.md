# Regulatory Watch (Step 1 MVP)

This repository contains the **first step** of a regulatory-watch application for a UK real estate investment management firm.

## What this step delivers

1. **Regulatory update ingestion** from FCA RSS feeds.
2. **Firm profile matching** (permissions + business tags) to determine relevance.
3. **Initial impact analysis** split into:
   - Operational impact
   - Business opportunities
   - Potential policy/procedure review areas
4. **HTTP API** (FastAPI) to run scans and inspect results.

---

## Architecture (Step 1)

```text
FCA RSS feeds --> ingestion client --> relevance engine --> impact engine --> API response
                                        ^
                                        |
                                   firm profile
```

### Components

- `app/fca_client.py`: fetches and parses FCA feed entries.
- `app/relevance.py`: rules-based matching against firm permissions and tags.
- `app/impact.py`: rules-based impact statements by topic.
- `app/main.py`: FastAPI API surface.
- `app/models.py`: shared data structures.

---

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for API docs.

---

## Endpoints

- `GET /health`
- `GET /firm-profile`
- `POST /scan-updates` — runs a scan and returns relevance + impact output

Optional body:

```json
{
  "limit": 20,
  "min_relevance_score": 0.3
}
```


## How to implement this in practice

If you are asking “how do I actually put this in place in my firm?”, use this sequence:

1. Update your real firm permissions/tags in `data/firm_profile.json`.
2. Run the API locally and inspect `/docs`.
3. Run `POST /scan-updates` daily and review results as a compliance team.
4. Tune relevance + impact rules from reviewer feedback.
5. Add persistence + workflow automation (notifications, approvals, audit trail).
6. Add policy/procedure corpus gap analysis as Phase 2.

See the full runbook: **`docs/IMPLEMENTATION_GUIDE.md`**.

---

## Important notes

- This is a **rules-based MVP** for explainability and speed.
- It is designed to be extended with:
  - LLM summarisation
  - policy/procedure corpus analysis
  - workflow integrations (email, Slack, ticketing)
