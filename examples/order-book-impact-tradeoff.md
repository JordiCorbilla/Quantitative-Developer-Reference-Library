# Order-Book And Impact Trade-Off

Related chapter: [../20-execution-microstructure-and-tca.md](../20-execution-microstructure-and-tca.md).

A 200,000-share buy order must trade over four buckets. Compare quantities in thousands of shares:

- even schedule: $[50,50,50,50]$;
- front-loaded schedule: $[80,60,40,20]$.

For a toy temporary-impact exposure proportional to $\sum_k n_k^2$:

```math
E_{\text{even}}=4(50^2)=10{,}000,
```

```math
E_{\text{front}}=80^2+60^2+40^2+20^2=12{,}000.
```

The front-loaded schedule has $12{,}000/10{,}000-1=20\%$ more temporary-impact exposure under this assumption. It also reduces remaining inventory faster:

| End of bucket | Even inventory | Front-loaded inventory |
| ---: | ---: | ---: |
| 0 | 200 | 200 |
| 1 | 150 | 120 |
| 2 | 100 | 60 |
| 3 | 50 | 20 |
| 4 | 0 | 0 |

Suppose displayed best-level quantities are 120,000 bid and 80,000 ask. Snapshot order-book imbalance is:

```math
I=\frac{120{,}000-80{,}000}{120{,}000+80{,}000}=0.20.
```

```python
even = [50.0, 50.0, 50.0, 50.0]
front_loaded = [80.0, 60.0, 40.0, 20.0]

even_impact = sum(quantity**2 for quantity in even)
front_impact = sum(quantity**2 for quantity in front_loaded)
imbalance = (120_000.0 - 80_000.0) / (120_000.0 + 80_000.0)

assert even_impact == 10_000.0
assert front_impact == 12_000.0
assert round(front_impact / even_impact - 1.0, 6) == 0.20
assert round(imbalance, 6) == 0.20
```

This does not select an execution schedule. A production optimizer needs calibrated temporary and permanent impact, volatility, spread, urgency, alpha decay, participation and limit constraints, fill probability, venue state, and model uncertainty. Displayed imbalance must be derived from a sequenced feed and tested after queue position, latency, cancellations, and fees.
