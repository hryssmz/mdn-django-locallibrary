# catalog/utils.py
from datetime import date
from typing import Optional


def format_date(d: Optional[date], empty: str = "") -> str:
    return d.strftime("%b %d, %Y") if d else empty
