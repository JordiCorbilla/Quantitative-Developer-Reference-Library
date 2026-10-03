# Index Divisor And Portfolio Weights

Related chapter: [../29-etfs-index-products-and-rebalances.md](../29-etfs-index-products-and-rebalances.md).

An index level comes from a methodology-defined basket and divisor. Portfolio weights tell you each constituent's share of basket value. They answer different questions. This synthetic single-currency price-index example follows the basket through a price move, a split, and a constituent replacement.

Start with 10 adjusted shares of A at 50 and 20 adjusted shares of B at 25. Each contributes 500, so both weights are 50%. Basket value is 1,000 and a divisor of 10 produces an index level of 100. If A rises 10% and B falls 4%, the fixed-holdings basket earns $0.5(10\%)+0.5(-4\%)=3\%$, and the index becomes 103. Multiplying weights by price levels would instead give 37.5 initially, which is neither basket value nor the index.

```python
import math


def basket_value(shares, prices):
    assert shares.keys() == prices.keys()
    return sum(shares[name] * prices[name] for name in shares)


shares = {"A": 10.0, "B": 20.0}
prices = {"A": 50.0, "B": 25.0}
divisor = 10.0
initial_value = basket_value(shares, prices)
weights = {name: shares[name] * prices[name] / initial_value for name in shares}
assert initial_value == 1_000.0
assert weights == {"A": 0.5, "B": 0.5}
assert initial_value / divisor == 100.0

moved_prices = {"A": 55.0, "B": 24.0}
basket_return = basket_value(shares, moved_prices) / initial_value - 1.0
weighted_return = sum(weights[name] * (moved_prices[name] / prices[name] - 1)
                      for name in shares)
assert math.isclose(basket_return, 0.03, abs_tol=1e-12)
assert math.isclose(basket_return, weighted_return, abs_tol=1e-12)

# At the initial marks, a two-for-one split preserves basket value.
split_shares = {"A": 20.0, "B": 20.0}
split_prices = {"A": 25.0, "B": 25.0}
assert basket_value(split_shares, split_prices) / divisor == 100.0

# Replace B at a common event timestamp. New basket value is 1,300.
# The divisor changes to 13 so the non-market change does not create a return.
replacement_shares = {"A": 10.0, "C": 40.0}
replacement_prices = {"A": 50.0, "C": 20.0}
new_value = basket_value(replacement_shares, replacement_prices)
new_divisor = divisor * new_value / initial_value
assert new_divisor == 13.0
assert new_value / new_divisor == initial_value / divisor
```

The split and replacement are separate scenarios at the original marks. Provider rules determine which events change share counts, float factors, cash components, or the divisor. Total-return indices also account for distributions; multi-currency indices require FX marks. A production reconstruction must use point-in-time membership and event-effective data, rather than today's constituents projected backward.
