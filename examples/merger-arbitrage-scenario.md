# Merger-Arbitrage Scenario Valuation

Related chapter: [../33-event-driven-and-merger-arbitrage.md](../33-event-driven-and-merger-arbitrage.md).

This compact example values a cash transaction under close, delay, and break outcomes. Terminal values are already net of outcome-specific carry; the base USD 0.20 cost applies in all cases.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    terminal_value: float


entry = 46.20
base_cost = 0.20
scenarios = [
    Scenario("close", 0.82, 50.00),
    Scenario("delay", 0.06, 48.60),
    Scenario("break", 0.12, 35.40),
]

assert abs(sum(s.probability for s in scenarios) - 1.0) < 1e-12

expected_terminal = sum(s.probability * s.terminal_value for s in scenarios)
expected_pnl = expected_terminal - base_cost - entry
expected_return = expected_pnl / entry
implied_completion_probability = (entry - 35.40) / (50.00 - 35.40)
jump_to_break = 35.40 - entry - base_cost

assert round(expected_terminal, 3) == 48.164
assert round(expected_pnl, 3) == 1.764
assert round(expected_return, 4) == 0.0382
assert round(implied_completion_probability, 4) == 0.7397
assert round(jump_to_break, 2) == -11.00
```

The expected return is positive, but the break loss is almost six times the expected PnL. Change the break value, closing probability, and delay payoff independently; those sensitivities are more informative than the headline annualized spread.
