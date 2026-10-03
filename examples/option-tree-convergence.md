# Option Tree Convergence Against Black-Scholes

Related chapters: [../01-options.md](../01-options.md) and [../10-numerical-methods.md](../10-numerical-methods.md).

A price can pass parity and derivative checks while still sharing a mistake with the functions used to check it. Here we value the same European payoff through a second numerical method: a Cox-Ross-Rubinstein tree, then compare it with the chapter's analytic price. The tree uses terminal payoffs and backward risk-neutral expectations; it does not call the analytic formula while pricing.

Both methods assume constant volatility, continuously compounded rates and dividend yield, and no discrete cash dividends. This is a benchmark for that model, not a validation of market quotes or a general American-option engine. The inputs are synthetic, prices are per underlying unit, and time is in years.

## Build The Independent Calculation

For a step of length $\Delta t$, set $u=e^{\sigma\sqrt{\Delta t}}$, $d=1/u$, and $p=(e^{(r-q)\Delta t}-d)/(u-d)$. Roll each node back as $e^{-r\Delta t}[pV_u+(1-p)V_d]$. Require $0<p<1$; a coarse tree can violate that condition even when the continuous model is well-defined. Refining the grid is a numerical choice, not permission to clip an invalid probability.

Run the fence from the repository root, or use the [release check](../QUICKSTART.md). It prints the maximum error over twelve call/put cases at each resolution. The final tolerance is 0.01 per underlying unit; it is a teaching tolerance, not a desk release limit. Errors can oscillate as the strike moves relative to tree nodes, so individual step counts need not improve monotonically.

```python
import math
import re
from pathlib import Path

import numpy as np


def tree_price(spot, strike, time_to_expiry, rate, dividend_yield, volatility, option_type, steps):
    if spot <= 0 or strike <= 0 or time_to_expiry <= 0 or volatility <= 0:
        raise ValueError("This benchmark requires positive spot, strike, time and volatility")
    if option_type not in {"call", "put"} or not isinstance(steps, int) or steps < 1:
        raise ValueError("Invalid payoff or step count")
    dt = time_to_expiry / steps
    up = math.exp(volatility * math.sqrt(dt))
    down = 1 / up
    probability = (math.exp((rate - dividend_yield) * dt) - down) / (up - down)
    if not 0 < probability < 1:
        raise ValueError("Refine the tree: risk-neutral probability is outside (0, 1)")
    terminal = spot * np.exp((2 * np.arange(steps + 1) - steps) * math.log(up))
    sign = 1 if option_type == "call" else -1
    values = np.maximum(sign * (terminal - strike), 0)
    discount = math.exp(-rate * dt)
    for size in range(steps, 0, -1):
        values = discount * ((1 - probability) * values[:size] + probability * values[1:size + 1])
    return float(values[0])


chapter = Path("01-options.md")
fence = chr(96) * 3
blocks = re.findall(fence + r"python\s*\n(.*?)" + fence, chapter.read_text(encoding="utf-8"), re.DOTALL)
assert len(blocks) == 1
namespace = {"__name__": "__documentation_snippet__"}
exec(compile(blocks[0], str(chapter), "exec"), namespace)
analytic = namespace["black_scholes_vanilla"]

# Spot, strike, years, rate, dividend yield, decimal volatility.
cases = [
    (100, 100, 1, .05, 0, .20),
    (100, 110, .25, -.01, .02, .35),
    (80, 100, 2, .03, .01, .25),
    (120, 100, .5, .02, .04, .18),
    (100, 100, 30 / 365, 0, 0, .60),
    (50, 100, 1, .05, 0, .10),
]
maximum_errors = []
for steps in (256, 1024, 4096):
    errors = []
    for inputs in cases:
        for kind in ("call", "put"):
            expected = analytic(*inputs, option_type=kind).price
            actual = tree_price(*inputs, option_type=kind, steps=steps)
            errors.append(abs(actual - expected))
        call = tree_price(*inputs, option_type="call", steps=steps)
        put = tree_price(*inputs, option_type="put", steps=steps)
        spot, strike, tenor, rate, carry, _ = inputs
        parity = spot * math.exp(-carry * tenor) - strike * math.exp(-rate * tenor)
        assert abs(call - put - parity) < 1e-8
    maximum_errors.append(max(errors))
    print(f"CRR steps={steps}: maximum absolute price error={max(errors):.8f}")

assert maximum_errors[-1] < .01
assert maximum_errors[-1] < maximum_errors[0]
try:
    tree_price(100, 100, 1, .50, 0, .01, "call", 1)
except ValueError as error:
    assert "probability" in str(error)
else:
    raise AssertionError("An invalid risk-neutral probability must fail")
```

## What The Result Establishes

Agreement across moneyness, short and longer expiries, negative rates, and nonzero carry gives more evidence than checking a single at-the-money call. The finite-difference Greek checks remain in the [earnings repricing example](option-greeks-and-earnings-repricing.md). Neither benchmark adds early exercise, cash dividends, stochastic volatility, or exchange-specific settlement rules.

Source: Cox, Ross, and Rubinstein, *Option Pricing: A Simplified Approach* (1979), [author paper reprint](https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/7/36891/files/2017/07/CRR79-1yy8av8.pdf).
