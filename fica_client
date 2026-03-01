from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List

import feedparser
import httpx

from app.models import RegulatoryUpdate


async def fetch_feed(url: str) -> List[RegulatoryUpdate]:
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    parsed = feedparser.parse(response.text)
    updates: List[RegulatoryUpdate] = []

    for entry in parsed.entries:
        published = _parse_date(
            getattr(entry, "published", None) or getattr(entry, "updated", None)
        )
        title = getattr(entry, "title", "Untitled update")
        link = getattr(entry, "link", "")
        summary = getattr(entry, "summary", "")
        item_id = getattr(entry, "id", link or title)

        updates.append(
            RegulatoryUpdate(
                id=item_id,
                title=title,
                link=link,
                summary=summary,
                published=published,
                source=url,
            )
        )

    return updates


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
