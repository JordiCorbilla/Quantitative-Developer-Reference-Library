# Event Volatility Implied Move

Related chapter: [../37-volatility-relative-value-and-event-volatility.md](../37-volatility-relative-value-and-event-volatility.md).

Two option expiries bracket one scheduled event:

| Input | Before event | After event |
| --- | ---: | ---: |
| Time to expiry | 20/365 years | 27/365 years |
| At-the-money implied volatility | 30% | 44% |

Assume diffuse volatility during the seven days between expiries is 28%. Work in total variance, $W=\sigma^2T$:

$$
W_1=0.30^2\frac{20}{365}=0.004932
$$

$$
W_2=0.44^2\frac{27}{365}=0.014321
$$

Under a deliberately simplified independent-Gaussian event model, subtract the diffuse variance between expiries to obtain an effective event variance:

$$
q_{\text{event}}^{\text{eff}}
=W_2-W_1-0.28^2\frac{7}{365}
=0.007886
$$

The Gaussian-equivalent one-standard-deviation implied log jump is:

$$
\sqrt{q_{\text{event}}^{\text{eff}}}=8.88\%
$$

This is a model-dependent screening number, not a model-free estimate of $E^Q[J^2]$ or a forecast of the realized move. A generic jump distribution, skewed surface, or nonzero jump mean does not map exactly from two ATM Black volatilities into one additive variance. A model-free implied-variance calculation instead uses an out-of-the-money option strip across strikes.

```python
from math import sqrt


def event_variance(
    t_before: float,
    vol_before: float,
    t_after: float,
    vol_after: float,
    diffuse_vol: float,
) -> float:
    if not 0.0 < t_before < t_after:
        raise ValueError("expiries must be ordered")
    value = (
        vol_after**2 * t_after
        - vol_before**2 * t_before
        - diffuse_vol**2 * (t_after - t_before)
    )
    if value < 0.0:
        raise ValueError("negative event variance")
    return value


q_event_effective = event_variance(20 / 365, 0.30, 27 / 365, 0.44, 0.28)
implied_move = sqrt(q_event_effective)
assert abs(q_event_effective - 0.007886027397260274) < 1e-12
assert abs(implied_move - 0.08880330735541483) < 1e-12
```

For USD 10m notional per unit of decimal event variance, a realized absolute log jump of 12% gives:

$$
10{,}000{,}000(0.12^2-0.00788603)
=\text{USD }65{,}140
$$

This calculation is a diagnostic, not an option price. Before using it, verify forward and moneyness alignment, expiry timestamps, event-time version history, diffuse-variance choice, bid/ask execution, post-event surface behavior, and the variance-notional unit.
