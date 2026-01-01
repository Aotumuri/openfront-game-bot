import datetime as dt
from typing import Optional


def format_iso(ts: Optional[str]) -> str:
    if not ts:
        return "N/A"
    try:
        parsed = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return ts
    return parsed.strftime("%Y-%m-%d %H:%M:%S UTC")
