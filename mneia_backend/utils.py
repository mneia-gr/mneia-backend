from datetime import date
from typing import Optional

from babel.dates import format_date, format_skeleton


def prettify_date(year: Optional[int], month: Optional[int], day: Optional[int]) -> Optional[str]:
    """Returns a pretty string for a date, suitable for presentation."""
    # if only the year is known, return the year:
    if year is not None and month is None and day is None:
        return str(year)

    # if the year and month are known, return a formatted string like "Ιανουάριος 2025"
    if year is not None and month is not None and day is None:
        return format_skeleton("MMMM y", date(year, month, 1), locale="el_GR")

    # if the year and month and day are known, return a string like "1 Ιανουαρίου 2025"
    if year is not None and month is not None and day is not None:
        return format_date(date(year, month, day), format="long", locale="el_GR")
