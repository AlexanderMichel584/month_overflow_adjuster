# month_overflow_adjuster

Adds or subtracts whole months to a `date` or `datetime`, clamping the day to
the last day of the target month instead of overflowing into the following one.

```python
from datetime import date
from month_overflow_adjuster import add_months

add_months(date(2023, 1, 31), 1)    # date(2023, 2, 28)
add_months(date(2024, 1, 31), 1)    # date(2024, 2, 29)
add_months(date(2024, 3, 31), -1)   # date(2024, 2, 29)
add_months(date(2023, 1, 15), 1)    # date(2023, 2, 15)
```

## Why this exists

`date` and `datetime` only understand `timedelta`, which counts days. Treating
"one month" as 30 days gives the wrong answer at month ends: January 31 plus 30
days is March 2, and the calendar month is skipped entirely. The behaviour people
expect from a monthly schedule is to stay on the same day of month when the
target month allows it, and to land on the last day of the target month when it
does not.

The trade-off is that the operation is not invertible at the boundary.
`add_months(add_months(date(2023, 1, 31), 1), -1)` returns `date(2023, 1, 28)`,
not the original date, because the clamping information is lost. That is
inherent to clamping and is accepted here; the alternative, carrying the
overflow forward, produces dates in the wrong month, which is worse for
billing, scheduling, and reporting code.

## The awkward edge

February is the case that bites. `add_months(date(2023, 1, 31), 1)` gives
`2023-02-28`, and `add_months(date(2024, 1, 31), 1)` gives `2024-02-29`. The
result depends on the year, so any test or caller that assumes a fixed February
length will be wrong every fourth year.

## API

### `add_months(value, months)`

Returns a new `date` (or `datetime`, if `value` is one) shifted by `months`
calendar months. `months` may be zero or negative. The time components of a
`datetime` are preserved unchanged.

Raises `TypeError` if `value` is not a `date`/`datetime`, or if `months` is not
an `int` (booleans are rejected too, since `add_months(d, True)` is almost
certainly a mistake).
