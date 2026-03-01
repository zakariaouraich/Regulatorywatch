from __future__ import annotations

import json
from pathlib import Path

from app.models import FirmProfile

BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = BASE_DIR / "data" / "firm_profile.json"

DEFAULT_FEEDS = [
    "https://www.fca.org.uk/news/rss.xml",
    "https://www.fca.org.uk/publication/feed.xml",
]


def load_firm_profile() -> FirmProfile:
    with PROFILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return FirmProfile.model_validate(data)
