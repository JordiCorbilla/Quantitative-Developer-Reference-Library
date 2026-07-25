# SPAC Unit and Warrant Reconciliation

Related chapter: [../36-warrants-rights-pipes-and-spacs.md](../36-warrants-rights-pipes-and-spacs.md).

This example reconciles a unit with its separately traded common and warrant components, then computes the common share's trust-value basis. It does not assume separation or redemption is operationally frictionless.

```python
unit_price = 10.38
common_price = 10.06
warrant_price = 0.58
warrants_per_unit = 0.5
estimated_net_trust_value = 10.12
days_to_redemption = 120

implied_warrant = (unit_price - common_price) / warrants_per_unit
component_package = common_price + warrants_per_unit * warrant_price
unit_residual = unit_price - component_package
trust_discount = estimated_net_trust_value - common_price
annualized_trust_convergence = (
    (estimated_net_trust_value / common_price) ** (365.0 / days_to_redemption) - 1.0
)

assert round(implied_warrant, 2) == 0.64
assert round(component_package, 2) == 10.35
assert round(unit_residual, 2) == 0.03
assert round(trust_discount, 2) == 0.06
assert round(annualized_trust_convergence, 4) == 0.0183
```

Before interpreting the USD 0.03 residual, add bid-ask spreads, separation fees, minimum quantities, processing time, settlement risk, and any borrow required for the offsetting legs. Before interpreting the trust discount, verify redemption eligibility, instruction deadlines, estimated taxes and withdrawals, and the cash-receipt date.
