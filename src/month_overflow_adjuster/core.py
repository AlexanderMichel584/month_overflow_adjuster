"""Month arithmetic that clamps to the end of the target month.

``date``/``datetime`` arithmetic in the standard library is deliberately
literal: adding ``timedelta(days=30)`` to January 31 lands on March 2, which is
not what "one month later" means to a human. The usual fix is to keep the day
of month when possible and clamp when the target month is shorter. That is the
rule this module implements, and it is the only rule: the day is clamped, never
carried forward into the next month.
"""

from __future__ import annotations

import calendar
from datetime import date, datetime

__all__ = ["add_months"]


def _clamp_day(year: int, month: int, day: int) -> int:
    """Return ``day`` clamped to the number of days in ``year``-``month``.

    ``calendar.monthrange`` already knows about leap years, so we do not need a
    separate leap-year branch here.
    """
    last_day = calendar.monthrange(year, month)[1]
    return day if day <= last_day else last_day


def _shift_months(year: int, month: int, months: int) -> tuple[int, int]:
    """Move ``months`` months from ``year``-``month``, normalising the result.

    ``month`` is 1-based. The offset is applied to a 0-based month index so
    that negative offsets and year boundaries fall out of ordinary integer
    arithmetic with ``divmod``.
    """
    index = year * 12 + (month - 1) + months
    new_year, new_month0 = divmod(index, 12)
    return new_year, new_month0 + 1


def add_months(value: date, months: int) -> date:
    """Return ``value`` shifted by ``months`` calendar months.

    The day of month is preserved when the target month is long enough and
    clamped to the target month's last day otherwise. ``months`` may be zero
    or negative; a negative offset moves backwards and clamps the same way.

    ``datetime`` is a subclass of ``date``, so passing one in returns a
    ``datetime`` with the time components untouched. The concrete type is
    preserved because callers who pass a ``datetime`` almost always want one
    back, and re-wrapping by hand is easy to get wrong.

    Raises:
        TypeError: if ``value`` is not a ``date`` or ``months`` is not an
            ``int`` (``bool`` is rejected even though it is an ``int``
            subclass, because ``add_months(d, True)`` is a bug, not a feature).
    """
    if not isinstance(value, date):
        raise TypeError("value must be a date or datetime instance")
    if isinstance(months, bool) or not isinstance(months, int):
        raise TypeError("months must be an int")

    new_year, new_month = _shift_months(value.year, value.month, months)
    new_day = _clamp_day(new_year, new_month, value.day)

    if isinstance(value, datetime):
        return value.replace(year=new_year, month=new_month, day=new_day)
    return date(new_year, new_month, new_day)
