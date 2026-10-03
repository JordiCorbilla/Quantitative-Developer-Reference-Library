# Robust Portfolio Construction and Research Validation

Related chapters: [13-risk-and-pnl.md](13-risk-and-pnl.md), [14-testing-and-validation.md](14-testing-and-validation.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md), [32-dependence-modelling-and-copulas.md](32-dependence-modelling-and-copulas.md), and [38-deal-level-risk-and-strategy-pnl.md](38-deal-level-risk-and-strategy-pnl.md).

## What This Domain Covers
Imagine two researchers using the same return history. One reports the best of sixty backtests; the other records every trial, fixes the selection rule, and evaluates it on later data. The first number can look much stronger while providing less evidence. The same problem appears in portfolio construction when an optimizer treats an uncertain return estimate as a precise input.

Portfolio weights can be extremely sensitive to estimation error. Sample means are noisy, sample covariance is unstable when the asset count is large relative to the history, and a few observations can dominate Pearson correlation. Research can also make weak signals look convincing through repeated testing or future leakage.

Robust construction addresses uncertain inputs and asymmetric loss; validation asks whether a result survives a realistic simulation of selection and deployment. Make estimator definitions, data vintages, trials, constraints, costs, and out-of-sample evidence reproducible.

## Product Taxonomy and Market Structure
Useful covariance and downside-risk estimators include:

- sample covariance with carefully aligned returns;
- linear or nonlinear shrinkage toward a structured target;
- factor covariance with specific risk;
- robust location/scale estimators and outlier-resistant covariance;
- rank dependence such as Kendall or Spearman measures;
- thresholded co-movement measures such as the Gerber statistic;
- target semivariance and lower-partial-moment matrices;
- stressed or regime-conditioned covariance.

Portfolio methods include minimum variance, risk budgeting, downside-risk optimization, and optimization over uncertainty sets. They still require leverage, concentration, liquidity, factor, turnover, and shorting constraints.

Research validation methods include fixed chronological holdouts, expanding or rolling walk-forward tests, purged cross-validation, embargoes, nested model selection, and multiple-testing corrections. Ordinary shuffled cross-validation is rarely appropriate when labels overlap in time.

## Quoting and Market Conventions
- Specify arithmetic or log total returns, base currency, sampling close, missing-data policy, and annualization factor.
- Record whether covariance is population-style $1/T$ or sample-style $1/(T-1)$ and whether returns are demeaned.
- A threshold such as $h=0.5$ is meaningless without its scale estimator. State whether it means 0.5 sample standard deviations, robust standard deviations, or another unit.
- Define semivariance relative to a target $\tau$: zero, a risk-free return, benchmark return, or required return. Different targets produce different matrices.
- Pairwise deletion can produce an indefinite matrix; optimizer covariance must be symmetric and positive semidefinite (PSD).
- Cross-validation rows need label intervals $[t_0,t_1]$, not only feature timestamps. Purging depends on when label information is realized.
- Define an embargo in observations or calendar time and justify it from label horizon and serial dependence.
- Count all tried signals, transformations, universes, windows, cost models, and hyperparameters in a trial family. Reporting only the saved run understates selection.

## Core Pricing Framework
For return vectors $r_t$, sample covariance is:

$$
S=\frac{1}{T-1}\sum_{t=1}^{T}(r_t-\bar r)(r_t-\bar r)^\top
$$

Linear shrinkage reduces estimation error by blending $S$ with a target $F$:

$$
\widehat\Sigma_{\text{shrunk}}
=(1-\delta)S+\delta F,
\qquad 0\leq\delta\leq1
$$

The target might be diagonal, constant-correlation, or factor-based. Validate $\delta$ out of sample.

### Thresholded Co-Movement

For asset $i$, use robust center $\mu_i$ and scale $s_i$, for example median and scaled median absolute deviation:

$$
s_i=1.4826\,\operatorname{median}_t|r_{i,t}-\operatorname{median}(r_i)|
$$

Classify each standardized return using threshold $h>0$:

$$
z_{i,t}=
\begin{cases}
+1, & r_{i,t}-\mu_i\geq h s_i\\
-1, & r_{i,t}-\mu_i\leq-h s_i\\
0, & \text{otherwise}
\end{cases}
$$

For a pair $(i,j)$, count jointly extreme up/up, down/down, up/down, and down/up observations. One common Gerber-statistic convention is:

$$
g_{ij}=
\frac{n^{UU}_{ij}+n^{DD}_{ij}-n^{UD}_{ij}-n^{DU}_{ij}}
{n^{UU}_{ij}+n^{DD}_{ij}+n^{UD}_{ij}+n^{DU}_{ij}}
$$

Neutral observations are excluded from this denominator. Other variants treat neutral regions differently, so persist the exact variant. Too few jointly extreme observations makes the estimate unreliable.

Convert the co-movement matrix $G$ into covariance using annualized scales:

$$
\widehat\Sigma_G=DGD,
\qquad
D=\operatorname{diag}(\sigma_1,\ldots,\sigma_N)
$$

Thresholding reduces the influence of tiny moves and the exact amplitude beyond a threshold. It does not remove regime, asymmetry, missing-data, or threshold risk. Apply a documented nearest-correlation or shrinkage procedure if needed.

### Downside Risk

For target vector $\tau$, define downside deviations:

$$
d_t=\min(r_t-\tau,0)
$$

where the minimum is componentwise. An uncentered target-semivariance matrix is:

$$
\Sigma^-=\frac{1}{T}\sum_{t=1}^{T}d_td_t^\top
$$

It is PSD and measures simultaneous target shortfalls. Conditional semivariance and lower-partial covariance use different denominators and centering, so label reports precisely.

A practical constrained optimizer can combine robust symmetric and downside risk:

$$
\min_w
\lambda w^\top\widehat\Sigma_{\text{robust}}w
+(1-\lambda)w^\top\Sigma^-w
+\kappa\lVert w-w_{\text{prev}}\rVert_1
$$

subject to funding, gross, factor, concentration, liquidity, and turnover constraints. Tail scenarios remain separate controls because neither covariance nor semivariance fully represents gaps.

### Research Selection Risk

If $m$ independent null hypotheses are tested at significance level $\alpha$, the probability of at least one false positive is:

$$
\operatorname{FWER}=1-(1-\alpha)^m
$$

Bonferroni tests each hypothesis at $\alpha/m$; false-discovery-rate procedures answer a different question. With dependent financial trials, consider effective trial count, bootstrap reality checks, superior-predictive-ability tests, or a Deflated Sharpe Ratio.

Purging removes training labels overlapping a test interval; an embargo removes observations immediately after it. Production-style walk-forward training must use only prior information. Nested validation reserves outer folds for performance estimation.

## Worked Instrument Example
Suppose two assets have annualized robust volatility scales of 20% and 30%. Among their jointly extreme observations:

| Count | Value |
| --- | ---: |
| Up/up | 5 |
| Down/down | 3 |
| Up/down | 1 |
| Down/up | 1 |

Their thresholded co-movement is:

$$
g_{12}=\frac{5+3-1-1}{5+3+1+1}=0.60
$$

The robust covariance is $0.60\times0.20\times0.30=0.036$. For a 50/50 portfolio:

$$
\sigma_p
=\sqrt{0.5^2(0.20^2)+0.5^2(0.30^2)
+2(0.5)(0.5)(0.036)}
=22.47\%
$$

Now suppose a researcher tries 60 strategy variants and uses an unadjusted 5% test. Under independent nulls:

$$
1-0.95^{60}=95.4\%
$$

The research record must expose all 60 trials, assess multiplicity, and evaluate the chosen specification on an untouched chronological outer test.

## Key Risk Measures and Sensitivities
- Eigenvalue spectrum, minimum eigenvalue, condition number, and PSD adjustment size.
- Estimator sensitivity to window, threshold, scale, missing-data policy, and stress periods.
- Portfolio volatility, target semideviation, expected shortfall, drawdown, and named scenario loss.
- Marginal and component risk, factor exposure, concentration, gross leverage, turnover, capacity, and liquidity.
- Weight stability under bootstrap, leave-one-period-out, covariance perturbation, and expected-return shrinkage.
- Net PnL, costs, forecast-versus-realized risk, and covariance forecast error.
- Number and dependence of trials, corrected significance, probabilistic or deflated Sharpe, and outer-fold dispersion.
- Leakage checks, fold coverage, purge counts, embargo counts, and performance decay from train to validation to test.

Portfolio PnL should be calculated from lagged executed weights:

$$
\operatorname{PnL}_t
=\operatorname{NAV}_{t-1}w_{t-1}^\top r_t
-\operatorname{cost}(\Delta w_t)
+\operatorname{financing}_t
$$

Attribute factor, specific, carry, rebalance, and cost PnL. Compare ex-ante risk with realized returns and run stressed-correlation, volatility-scaling, liquidity, and gap scenarios.

## Required Data, Curves, Surfaces, and Calibration Objects
Store a bitemporal return panel with instrument, economic and availability timestamps, raw/adjusted price, currency, corporate-action version, and return policy.

An `EstimatorSpec` includes universe, window, frequency, location/scale, outlier policy, threshold variant, shrinkage, semivariance target, annualization, missing-data, and PSD repair. A `CovarianceSnapshot` stores matrix, asset order, diagnostics, cutoff, and code/config versions.

Each labeled sample needs feature time, label interval, entity/group, and feature availability. A `FoldDefinition` stores IDs, purge/embargo rules, and future-data policy.

An append-only `TrialRegistry` contains hypothesis family, parameter hash, data/code versions, seed, costs, all metrics, and selection status. A `PortfolioRun` links estimator, forecast, constraints, target/executed weights, and PnL.

## Numerical and Implementation Approaches
Start with shrinkage or a factor benchmark. Use robust location and scale consistently; a median threshold with an outlier-contaminated scale weakens the design.

Validate symmetry, finite values, diagonal positivity, eigenvalues, and covariance/correlation conversion. Prefer nearest-correlation repair that preserves a unit diagonal. Test small data perturbations.

Split by time and by any economic unit that can leak information. Purge overlapping labels, embargo where justified, fit transforms on training data, nest selection, and retain an untouched final holdout.

Register trials before evaluation when possible. Report net performance, turnover, capacity, drawdown, scenario loss, confidence intervals, and outer-fold dispersion.

## Production Pitfalls and Sanity Checks
- Winsorizing or standardizing on the full sample before splitting.
- Using revised constituents, fundamentals, or corporate actions before their availability dates.
- Randomly splitting rows whose forward-return labels overlap.
- Applying an embargo but forgetting to purge training labels that cross into the test interval.
- Selecting a model on outer test results and still calling them out of sample.
- Ignoring failed trials when correcting for multiple testing.
- Using pairwise covariances that form an indefinite matrix.
- Choosing a robust threshold because it gives the best backtest on the same period.
- Optimizing noisy expected returns to many decimal places.
- Reporting gross Sharpe while hiding turnover, borrow, impact, and rejected fills.
- Treating semivariance, expected shortfall, and maximum drawdown as interchangeable.

Release controls should fail on data leakage, nonfinite matrix entries, material PSD repair, breached constraints, impossible turnover, unreconciled PnL, missing trial lineage, or absent outer-fold results.

## Illustrative Code
```python
from dataclasses import dataclass


def gerber_pair(states_a: list[int], states_b: list[int]) -> float:
    if len(states_a) != len(states_b) or not states_a:
        raise ValueError("aligned non-empty state series are required")
    concordant = sum(
        1 for a, b in zip(states_a, states_b) if a != 0 and b != 0 and a == b
    )
    discordant = sum(
        1 for a, b in zip(states_a, states_b) if a != 0 and b != 0 and a == -b
    )
    denominator = concordant + discordant
    if denominator == 0:
        raise ValueError("no jointly extreme observations")
    return (concordant - discordant) / denominator


@dataclass(frozen=True)
class LabelInterval:
    start: int
    end: int


def purged_train_indices(
    labels: list[LabelInterval],
    test_indices: set[int],
    embargo_end: int,
) -> list[int]:
    test_intervals = [labels[i] for i in test_indices]
    test_end = max(interval.end for interval in test_intervals)
    kept: list[int] = []
    for i, candidate in enumerate(labels):
        if i in test_indices:
            continue
        overlaps = any(
            candidate.start <= test.end and test.start <= candidate.end
            for test in test_intervals
        )
        embargoed = test_end < candidate.start <= embargo_end
        if not overlaps and not embargoed:
            kept.append(i)
    return kept


def familywise_false_positive_rate(alpha: float, trials: int) -> float:
    if not 0.0 < alpha < 1.0 or trials < 1:
        raise ValueError("invalid alpha or trial count")
    return 1.0 - (1.0 - alpha) ** trials
```

## References and Further Reading
- Ledoit and Wolf. [“A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices”](https://doi.org/10.1016/S0047-259X(03)00096-4).
- Gerber, Markowitz, Ernst, Miao, Javid, and Sargen. [“The Gerber Statistic: A Robust Co-Movement Measure for Portfolio Optimization”](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3880054).
- Markowitz. *Portfolio Selection: Efficient Diversification of Investments*, including semivariance.
- White. [“A Reality Check for Data Snooping”](https://doi.org/10.1111/1468-0262.00152).
- Hansen. [“A Test for Superior Predictive Ability”](https://doi.org/10.1198/073500105000000063).
- Bailey and López de Prado. [“The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality”](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551).
- Harvey, Liu, and Zhu. [“… and the Cross-Section of Expected Returns”](https://doi.org/10.1093/rfs/hhv059).
- López de Prado. *Advances in Financial Machine Learning*, chapters on purged and embargoed cross-validation.
- Related example: [examples/gerber-co-movement.md](examples/gerber-co-movement.md).
