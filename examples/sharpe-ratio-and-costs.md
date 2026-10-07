# Sharpe Ratio: Extra Return, Variability, And Costs

Related chapters: [portfolio construction](../16-portfolio-construction-and-backtesting.md#sharpe-ratio-is-the-extra-return-worth-the-ride) and [research validation](../44-robust-portfolio-and-research-validation.md).

Two funds expect the same return, but one takes twice the volatility. The chapter's synthetic annual assumptions give Sharpe ratios of 0.8 and 0.4. Now move from expected inputs to twelve synthetic monthly observations. Subtract matching cash returns, estimate sample variability, and see how a constant monthly cost lowers the estimated Sharpe even though it leaves that variability unchanged.

The monthly cash return is a supplied 0.2%, not an annual quote divided blindly by twelve. The six alternating excess-return observations are repeated to make the arithmetic easy; this constructed sequence is not evidence of independent returns or a real trading edge. We show conventional annualization as arithmetic only. Its validity for actual data requires the assumptions explained in the chapter.

```python
import math
from statistics import mean, stdev


def sample_sharpe(portfolio, cash, periods_per_year=None):
    if len(portfolio) != len(cash) or len(portfolio) < 2:
        raise ValueError("Require aligned returns with at least two observations")
    if not all(math.isfinite(value) for value in [*portfolio, *cash]):
        raise ValueError("Returns must be finite; missing observations require an explicit policy")
    excess = [total - safe for total, safe in zip(portfolio, cash)]
    volatility = stdev(excess)
    if volatility == 0:
        raise ValueError("Sharpe is undefined for zero sample excess-return volatility")
    result = mean(excess) / volatility
    if periods_per_year is not None:
        if not math.isfinite(periods_per_year) or periods_per_year <= 0:
            raise ValueError("Annualization frequency must be positive and finite")
        result *= math.sqrt(periods_per_year)
    return result


assert math.isclose((.10 - .02) / .10, .8)
assert math.isclose((.10 - .02) / .20, .4)
cash = [.002] * 12
excess = [-.01, .01, .03, -.01, .01, .03] * 2
gross = [safe + extra for safe, extra in zip(cash, excess)]
cost = .002  # Synthetic additive cost of 20 basis points each month.
net = [value - cost for value in gross]
expected_volatility = math.sqrt(.0032 / 11)
assert math.isclose(mean(excess), .01)
assert math.isclose(stdev(excess), expected_volatility)
monthly = sample_sharpe(gross, cash)
annualized = sample_sharpe(gross, cash, 12)
net_annualized = sample_sharpe(net, cash, 12)
assert math.isclose(monthly, .01 / expected_volatility)
assert math.isclose(annualized, monthly * math.sqrt(12))
assert math.isclose(net_annualized, annualized * .8)
assert math.isclose(stdev([value - safe for value, safe in zip(net, cash)]), expected_volatility)

for portfolio, safe in (([.01], [.002]), ([.01, .02], [.002]), ([0, 0], [0, 0])):
    try:
        sample_sharpe(portfolio, safe)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid inputs must fail instead of reporting a plausible ratio")

print(f"Monthly sample Sharpe: {monthly:.6f}")
print(f"Conventional annualized gross Sharpe: {annualized:.6f}")
print(f"Conventional annualized net Sharpe: {net_annualized:.6f}")
```

The gross and net estimates are conventionally annualized to approximately 2.031010 and 1.624808. Those attractive numbers come from invented observations; they demonstrate the calculation, not strategy quality. Real time-varying costs also change the denominator, and stale or overlapping observations can distort the annualization. Keep the return series, cash series, observation dates, cost basis, and sampling assumptions with every reported ratio.
