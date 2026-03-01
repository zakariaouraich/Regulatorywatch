# Regulatory Watch — GitHub Setup (Step-by-Step)

This is the exact process to take the files in this GitHub repo and get the app running on your machine.

## What you need first

- A GitHub account with access to the repository.
- Git installed.
- Python 3.11+ installed.
- A terminal (PowerShell, Terminal, iTerm, etc.).

---

## 1) Clone the repository from GitHub

Replace `<your-org-or-username>` if needed:

```bash
git clone https://github.com/<your-org-or-username>/Regulatorywatch.git
cd Regulatorywatch
```

If you already have the repo cloned, just pull latest:

```bash
git pull
```

---

## 2) Create and activate a Python virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4) Configure your real firm details

Open this file and replace the example values with your real FCA permissions/tags:

- `data/firm_profile.json`

At minimum, update:
- `name`
- `permissions`
- `business_tags`

This is important because relevance scoring uses this file.

---

## 5) Start the app

```bash
uvicorn app.main:app --reload
```

You should now see the API running at:
- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

---

## 6) Test that it works in the browser

In `/docs`, run these endpoints in order:

1. `GET /health` → should return `{ "status": "ok" }`
2. `GET /firm-profile` → should show your edited profile
3. `POST /scan-updates` with body:

```json
{
  "limit": 20,
  "min_relevance_score": 0.3
}
```

You should get back relevant FCA updates and impact suggestions.

---

## 7) Daily usage process (non-technical)

Once running, your daily process can be:

1. Open `/docs`
2. Run `POST /scan-updates`
3. Review returned items
4. Mark which are applicable
5. Assign actions for impacted policies/procedures

---

## 8) Save your changes back to GitHub

If you edit profile/rules/docs and want to save to GitHub:

```bash
git checkout -b chore/update-profile-and-rules
git add .
git commit -m "Update firm profile and relevance rules"
git push -u origin chore/update-profile-and-rules
```

Then open a Pull Request in GitHub.

---

## 9) Common issues

### `ModuleNotFoundError` when running tests/app

Usually fixed by activating `.venv` and reinstalling:

```bash
source .venv/bin/activate  # or Windows equivalent
pip install -r requirements.txt
```

### RSS feed/network issue

Try again later or from a network that can reach `fca.org.uk`.

### Port already in use

Run on another port:

```bash
uvicorn app.main:app --reload --port 8001
```

---

## 10) Next recommended step

After this is working locally, the next practical enhancement is:

- persist scan results to a database, and
- schedule one automatic daily scan.

That creates an audit trail and removes manual repetition.
