# Bitemporal As-Of Replay

Related chapter: [40-point-in-time-data-and-event-systems.md](../40-point-in-time-data-and-event-systems.md).

An estimate for the same economic period is first published at 100, corrected to 94, and later restated to 91. A point-in-time query should return the value that was known at the decision cutoff, not the final restatement.

```python
from datetime import datetime, timezone

UTC = timezone.utc
OPEN_END = datetime(9999, 12, 31, tzinfo=UTC)

versions = [
    {
        "value": 100.0,
        "known_from": datetime(2026, 4, 30, 21, 5, tzinfo=UTC),
        "known_to": datetime(2026, 5, 2, 14, 0, tzinfo=UTC),
    },
    {
        "value": 94.0,
        "known_from": datetime(2026, 5, 2, 14, 0, tzinfo=UTC),
        "known_to": datetime(2026, 6, 15, 12, 0, tzinfo=UTC),
    },
    {
        "value": 91.0,
        "known_from": datetime(2026, 6, 15, 12, 0, tzinfo=UTC),
        "known_to": OPEN_END,
    },
]


def value_known_at(cutoff: datetime) -> float:
    visible = [
        row["value"]
        for row in versions
        if row["known_from"] <= cutoff < row["known_to"]
    ]
    if len(visible) != 1:
        raise ValueError(f"expected one version, found {len(visible)}")
    return visible[0]


assert value_known_at(datetime(2026, 5, 1, 13, 0, tzinfo=UTC)) == 100.0
assert value_known_at(datetime(2026, 5, 3, 13, 0, tzinfo=UTC)) == 94.0
assert value_known_at(datetime(2026, 7, 1, 13, 0, tzinfo=UTC)) == 91.0
```

Production extensions:

- add valid-time intervals as well as knowledge time;
- enforce non-overlapping versions in the database;
- retain source payload hashes and revision reasons;
- replay downstream signals with the original code and configuration version.
