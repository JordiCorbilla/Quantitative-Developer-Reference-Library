# VWAP And TWAP Comparison

Related chapter: [../20-execution-microstructure-and-tca.md](../20-execution-microstructure-and-tca.md).

Assume these intraday market prints:

| Bucket | Price | Volume |
| ---: | ---: | ---: |
| 1 | 100.00 | 20,000 |
| 2 | 100.10 | 10,000 |
| 3 | 100.20 | 10,000 |
| 4 | 100.50 | 60,000 |

TWAP:

```math
\frac{100.00 + 100.10 + 100.20 + 100.50}{4} = 100.20
```

VWAP:

```math
\frac{100.00 \times 20k + 100.10 \times 10k + 100.20 \times 10k + 100.50 \times 60k}{100k} = 100.33
```

```python
prices = [100.00, 100.10, 100.20, 100.50]
volumes = [20_000, 10_000, 10_000, 60_000]

twap = sum(prices) / len(prices)
vwap = sum(price * volume for price, volume in zip(prices, volumes)) / sum(volumes)

assert abs(twap - 100.20) < 1e-12
assert abs(vwap - 100.33) < 1e-12
```

Interpretation:
- TWAP treats each time bucket equally.
- VWAP weights the high-volume final bucket more heavily.
- An execution algo should be evaluated against the benchmark it was designed to optimize.
