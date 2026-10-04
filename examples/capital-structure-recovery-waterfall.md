# Capital-Structure Recovery Waterfall

Related chapter: [../34-capital-structure-relative-value.md](../34-capital-structure-relative-value.md).

This example allocates stressed enterprise value through three debt classes. It is an analytical starting point, not a legal opinion: guarantees, collateral silos, disputed claims, new-money priority, and negotiated plan value can change the result.

Assume:

- first-lien allowed claim: USD 300m,
- senior unsecured allowed claim: USD 400m,
- subordinated allowed claim: USD 250m,
- administrative and restructuring costs: USD 20m.

For enterprise value $EV$, distributable value is:

```math
A=\max(EV-20m,0).
```

Claims are paid from most senior to most junior:

```math
R_i=\min(F_i,\max(A-\text{recoveries already allocated},0)).
```

## Downside Case

Let enterprise value be USD 570m. Distributable value is USD 550m:

| Claim | Allowed claim | Recovery value | Recovery rate |
| --- | ---: | ---: | ---: |
| First lien | USD 300m | USD 300m | 100.0% |
| Senior unsecured | USD 400m | USD 250m | 62.5% |
| Subordinated | USD 250m | USD 0m | 0.0% |

The allocation conserves value:

```math
300m+250m+0=550m.
```

Now suppose USD 10m face of the senior unsecured bond was purchased at 82 clean and matched with USD 10m CDS protection. If the bond and CDS auction both settle at the 62.5% recovery assumption:

```math
\text{bond recovery}=10m\times62.5\%=USD\ 6.25m,
```

```math
\text{CDS protection payment}=10m\times(1-62.5\%)=USD\ 3.75m.
```

Total default settlement is USD 10m versus USD 8.2m clean purchase cost. The difference must fund CDS premiums, accrued interest, financing, transaction costs, and legal/delivery basis. If the auction recovery differs from the owned bond's recovery, the package does not settle to par.

## Scenario Grid

| Scenario | Enterprise value | First-lien recovery | Unsecured recovery | Subordinated recovery |
| --- | ---: | ---: | ---: | ---: |
| Severe | USD 320m | 100.0% | 0.0% | 0.0% |
| Downside | USD 570m | 100.0% | 62.5% | 0.0% |
| Base restructuring | USD 800m | 100.0% | 100.0% | 32.0% |
| Full coverage | USD 970m | 100.0% | 100.0% | 100.0% |

In the severe case, costs leave exactly USD 300m for the first lien. In the base restructuring case, USD 80m remains for subordinated debt after costs and the two senior classes, so subordinated recovery is $80/250=32\%$.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    name: str
    allowed: float


def waterfall(
    enterprise_value: float,
    costs: float,
    claims: list[Claim],
) -> dict[str, dict[str, float]]:
    remaining = max(enterprise_value - costs, 0.0)
    result: dict[str, dict[str, float]] = {}
    for claim in claims:
        paid = min(claim.allowed, remaining)
        result[claim.name] = {
            "recovery_value": paid,
            "recovery_rate": paid / claim.allowed,
        }
        remaining -= paid
    return result


claims = [
    Claim("first_lien", 300_000_000),
    Claim("senior_unsecured", 400_000_000),
    Claim("subordinated", 250_000_000),
]

downside = waterfall(
    enterprise_value=570_000_000,
    costs=20_000_000,
    claims=claims,
)

assert downside["first_lien"]["recovery_rate"] == 1.0
assert downside["senior_unsecured"]["recovery_rate"] == 0.625
assert downside["subordinated"]["recovery_rate"] == 0.0
assert sum(x["recovery_value"] for x in downside.values()) == 550_000_000
```

Production extensions should add separate collateral pools, guarantor contribution, claim caps, priority changes, non-cash plan securities, discounting to expected resolution date, and scenario probabilities. Preserve document and valuation provenance for every assumption.
