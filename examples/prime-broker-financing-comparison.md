# Prime-Broker Financing Comparison

Related chapter: [43-prime-brokerage-counterparty-and-funding.md](../43-prime-brokerage-counterparty-and-funding.md).

Two financing providers quote different debit, rebate, and special-borrow terms for the same USD 20m long / USD 20m short portfolio.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    name: str
    debit_rate: float
    rebate_rate: float
    special_borrow_fee: float
    extra_margin: float


def thirty_day_cost(
    quote: Quote,
    long_debit: float = 20_000_000.0,
    short_proceeds: float = 20_000_000.0,
    special_short: float = 5_000_000.0,
) -> float:
    yf = 30.0 / 360.0
    financing_pnl = (
        -long_debit * quote.debit_rate * yf
        + short_proceeds * quote.rebate_rate * yf
        - special_short * quote.special_borrow_fee * yf
    )
    margin_liquidity_charge = quote.extra_margin * 0.06 * yf
    return -(financing_pnl - margin_liquidity_charge)


quotes = [
    Quote("A", debit_rate=0.0575, rebate_rate=0.0425, special_borrow_fee=0.09, extra_margin=1_000_000),
    Quote("B", debit_rate=0.0600, rebate_rate=0.0450, special_borrow_fee=0.05, extra_margin=3_000_000),
]

costs = {quote.name: thirty_day_cost(quote) for quote in quotes}
best = min(costs, key=costs.get)

assert best in {"A", "B"}
assert all(cost > 0.0 for cost in costs.values())
```

The cheapest financing spread is not automatically the cheapest allocation. A fuller exercise should add:

- margin stress rather than one flat liquidity charge;
- counterparty concentration limits;
- borrow recall probability and buy-in cost;
- settlement and collateral-transfer timing;
- capacity constraints across several positions.
