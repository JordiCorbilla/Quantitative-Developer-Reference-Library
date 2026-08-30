# Yield-Curve Interpolation Between Market Nodes

A curve is observed only through liquid instruments at selected maturities, while a pricing engine needs values on every cashflow date. This example starts after bootstrapping: the continuously compounded zero-rate nodes are treated as already constructed, and two exact interpolators answer the same off-node question differently.

The synthetic nodes are:

| Maturity | Continuously compounded zero rate |
| ---: | ---: |
| 1 year | 3.80% |
| 2 years | 3.65% |
| 5 years | 3.40% |
| 10 years | 3.55% |
| 30 years | 3.85% |

The target is 7.3 years, between the 5-year and 10-year nodes. Linear-zero interpolation connects the two zero rates. Log-linear discount-factor interpolation first converts each node using \(P(0,T)=e^{-z(T)T}\), connects \(\log P(0,T)\), and converts the result back to a zero rate.

```python
from math import exp, isfinite, log


def interval_index(maturities: list[float], target: float) -> int:
    if len(maturities) < 2 or not all(isfinite(value) for value in maturities):
        raise ValueError("maturities must contain at least two finite values")
    if any(right <= left for left, right in zip(maturities, maturities[1:])):
        raise ValueError("maturities must be strictly increasing")
    if not maturities[0] <= target <= maturities[-1]:
        raise ValueError("target is outside the interpolation domain")
    for index, (left, right) in enumerate(zip(maturities, maturities[1:])):
        if left <= target <= right:
            return index
    raise RuntimeError("interpolation interval was not found")


def interpolation_weight(left_time: float, right_time: float, target: float) -> float:
    return (target - left_time) / (right_time - left_time)


def linear_zero_rate(
    maturities: list[float], zero_rates: list[float], target: float
) -> float:
    if len(maturities) != len(zero_rates):
        raise ValueError("maturity and zero-rate counts must match")
    index = interval_index(maturities, target)
    left_time, right_time = maturities[index : index + 2]
    left_rate, right_rate = zero_rates[index : index + 2]
    weight = interpolation_weight(left_time, right_time, target)
    return left_rate + weight * (right_rate - left_rate)


def log_linear_discount_factor(
    maturities: list[float], zero_rates: list[float], target: float
) -> float:
    if len(maturities) != len(zero_rates):
        raise ValueError("maturity and zero-rate counts must match")
    index = interval_index(maturities, target)
    left_time, right_time = maturities[index : index + 2]
    left_rate, right_rate = zero_rates[index : index + 2]
    weight = interpolation_weight(left_time, right_time, target)
    left_log_discount = -left_rate * left_time
    right_log_discount = -right_rate * right_time
    target_log_discount = left_log_discount + weight * (
        right_log_discount - left_log_discount
    )
    return exp(target_log_discount)


def interval_forward_from_log_discounts(
    left_time: float,
    right_time: float,
    left_zero_rate: float,
    right_zero_rate: float,
) -> float:
    left_log_discount = -left_zero_rate * left_time
    right_log_discount = -right_zero_rate * right_time
    return -(right_log_discount - left_log_discount) / (right_time - left_time)


maturities = [1.0, 2.0, 5.0, 10.0, 30.0]
zero_rates = [0.0380, 0.0365, 0.0340, 0.0355, 0.0385]
target = 7.3

linear_zero = linear_zero_rate(maturities, zero_rates, target)
linear_zero_discount = exp(-linear_zero * target)
log_linear_discount = log_linear_discount_factor(maturities, zero_rates, target)
log_linear_zero = -log(log_linear_discount) / target

left_index = interval_index(maturities, target)
left_time, right_time = maturities[left_index : left_index + 2]
left_rate, right_rate = zero_rates[left_index : left_index + 2]
zero_slope = (right_rate - left_rate) / (right_time - left_time)
linear_zero_forward_at_target = linear_zero + target * zero_slope
log_linear_interval_forward = interval_forward_from_log_discounts(
    left_time, right_time, left_rate, right_rate
)

assert abs(linear_zero - 0.0346900000) < 1e-12
assert abs(linear_zero_discount - 0.7762838807) < 1e-10
assert abs(log_linear_discount - 0.7748390102) < 1e-10
assert abs(log_linear_zero - 0.0349452055) < 1e-10
assert abs((log_linear_zero - linear_zero) * 10_000 - 2.5520548) < 1e-6
assert abs(linear_zero_forward_at_target - 0.03688) < 1e-12
assert abs(log_linear_interval_forward - 0.03700) < 1e-12
```

Both interpolators exactly recover the 5-year and 10-year node values, yet at 7.3 years they produce discount factors of about 0.776284 and 0.774839. The corresponding zero rates differ by about 2.55 basis points. Log-linear discount factors imply a constant 3.70% instantaneous forward within this interval; linear zero rates imply 3.688% at the target and a forward that varies with maturity.

This is a representation comparison, not a calibration or recommendation. A production choice also has to reprice every calibration instrument, remain stable under quote bumps, produce explainable discount/zero/forward shapes, define extrapolation, and be validated against PV and PV01 materiality.
