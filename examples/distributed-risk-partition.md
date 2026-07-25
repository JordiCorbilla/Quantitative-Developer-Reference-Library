# Distributed Risk Partition

Related chapter: [41-production-quant-engineering.md](../41-production-quant-engineering.md).

Equal trade counts can create poor shards when products have different runtime costs. This example uses a greedy cost-aware partitioner and verifies that every trade is assigned exactly once.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkItem:
    trade_id: str
    estimated_cost: float


def partition(items: list[WorkItem], shard_count: int) -> list[list[WorkItem]]:
    if shard_count <= 0:
        raise ValueError("shard_count must be positive")

    shards: list[list[WorkItem]] = [[] for _ in range(shard_count)]
    costs = [0.0] * shard_count

    for item in sorted(items, key=lambda row: row.estimated_cost, reverse=True):
        target = min(range(shard_count), key=costs.__getitem__)
        shards[target].append(item)
        costs[target] += item.estimated_cost

    return shards


items = [
    WorkItem("vanilla-1", 1.0),
    WorkItem("vanilla-2", 1.0),
    WorkItem("convertible-1", 8.0),
    WorkItem("exotic-1", 12.0),
    WorkItem("bond-1", 2.0),
]

shards = partition(items, shard_count=2)
assigned = [item.trade_id for shard in shards for item in shard]
assert sorted(assigned) == sorted(item.trade_id for item in items)
assert len(assigned) == len(set(assigned))
```

A production exercise should add:

- stable run and shard IDs;
- idempotent retry behavior;
- expected-shard validation before aggregation;
- structured timing and failure metrics;
- deterministic result aggregation.
