# Catalyst Equity Earnings Bridge

Related chapter: [../42-fundamental-catalyst-equity-analysis.md](../42-fundamental-catalyst-equity-analysis.md).

This example decomposes an earnings surprise into revenue, margin, operating expense, and share-count effects, then distinguishes an EPS revision from a valuation-multiple change.

```python
consensus = {
    "revenue": 1_000.0,
    "gross_margin": 0.40,
    "operating_expense": 250.0,
    "net_interest": 20.0,
    "tax_rate": 0.25,
    "diluted_shares": 100.0,
}
reported = {
    "revenue": 1_060.0,
    "gross_margin": 0.41,
    "operating_expense": 265.0,
    "net_interest": 20.0,
    "tax_rate": 0.25,
    "diluted_shares": 102.0,
}


def statement(case: dict[str, float]) -> dict[str, float]:
    gross_profit = case["revenue"] * case["gross_margin"]
    ebit = gross_profit - case["operating_expense"]
    net_income = (ebit - case["net_interest"]) * (1.0 - case["tax_rate"])
    return {
        "gross_profit": gross_profit,
        "ebit": ebit,
        "net_income": net_income,
        "eps": net_income / case["diluted_shares"],
    }


base = statement(consensus)
actual = statement(reported)

revenue_effect_on_ebit = (
    reported["revenue"] - consensus["revenue"]
) * consensus["gross_margin"]
margin_effect_on_ebit = reported["revenue"] * (
    reported["gross_margin"] - consensus["gross_margin"]
)
opex_effect_on_ebit = -(
    reported["operating_expense"] - consensus["operating_expense"]
)

eps_surprise = actual["eps"] / base["eps"] - 1.0
price_at_old_multiple = 4.30 * 15.0
price_at_lower_multiple = 4.30 * 14.5

assert round(base["eps"], 3) == 0.975
assert round(actual["eps"], 2) == 1.10
assert round(eps_surprise, 4) == 0.1282
assert round(
    revenue_effect_on_ebit + margin_effect_on_ebit + opex_effect_on_ebit, 1
) == 19.6
assert round(price_at_old_multiple, 2) == 64.50
assert round(price_at_lower_multiple, 2) == 62.35
```

The 12.8% EPS beat is a historical calculation. A valuation response still depends on forecast durability, cash conversion, the revised share count, balance-sheet changes, and the multiple investors apply to the new forward EPS.
