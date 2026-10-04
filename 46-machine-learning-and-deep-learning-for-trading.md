# Machine Learning and Deep Learning for Trading

Related chapters: [11-market-data.md](11-market-data.md), [14-testing-and-validation.md](14-testing-and-validation.md), [15-performance-and-production.md](15-performance-and-production.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [20-execution-microstructure-and-tca.md](20-execution-microstructure-and-tca.md), [23-probability-statistics-and-regression.md](23-probability-statistics-and-regression.md), [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md), [41-production-quant-engineering.md](41-production-quant-engineering.md), [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md), [45-time-series-forecasting-and-state-space-models.md](45-time-series-forecasting-and-state-space-models.md), [47-reinforcement-learning-for-trading-and-execution.md](47-reinforcement-learning-for-trading-and-execution.md), and [48-factor-models-and-systematic-signals.md](48-factor-models-and-systematic-signals.md).

## What This Domain Covers
Machine learning for trading estimates a conditional quantity from data: a return, direction, rank, volatility, fill probability, cost, default event, or regime. Deep learning extends the function class with learned nonlinear representations and sequence models. Neither category creates an economic edge by itself. A useful model must connect a well-defined information set to an executable decision and survive costs, capacity limits, nonstationarity, and realistic out-of-sample testing.

The practical workflow is:

1. define the decision time, prediction target, horizon, and economic action;
2. assemble only features that were available at that time;
3. choose the simplest model compatible with the data geometry;
4. select and calibrate it inside leakage-safe validation;
5. convert predictions into constrained positions or orders;
6. account for spread, impact, borrow, funding, and missed fills;
7. deploy a versioned artifact with monitoring, fallbacks, and PnL attribution.

A high cross-validation score is not the objective. The objective is stable, risk-adjusted, net economic value under the intended trading protocol.

## Product Taxonomy and Market Structure
Model families solve different problems. Treat this as a choice of inductive bias, not a leaderboard.

| Family | Typical fit | Strengths | Main cautions |
| --- | --- | --- | --- |
| OLS | Continuous target with approximately linear effects | Transparent baseline, fast, easy attribution | Collinearity, unstable coefficients, outliers |
| Ridge | Many correlated features with diffuse signal | Stabilizes coefficients through an $L_2$ penalty | Retains every feature; scale-sensitive |
| Lasso | Sparse linear signal | Shrinkage and variable selection | Unstable selection among correlated features |
| Elastic net | Sparse groups of correlated features | Combines $L_1$ selection and $L_2$ stability | Two penalties must be selected without leakage |
| Logistic regression | Binary event or direction probability | Interpretable log-odds, strong calibrated baseline | Linear decision boundary unless features are expanded |
| Decision tree | Threshold interactions and rule-like effects | Handles nonlinear splits, easy local path | High variance and poor extrapolation |
| Random forest | Nonlinear tabular data with noisy interactions | Bagging reduces tree variance | Can be large; probabilities often need calibration |
| Gradient-boosted trees | Structured tabular data and heterogeneous interactions | Strong nonlinear tabular baseline | Sensitive to depth, learning rate, leakage, and drift |
| SVM | Moderate-size data with a meaningful margin | Effective linear or kernel boundary | Scaling and kernel choice matter; probability output is indirect |
| k-nearest neighbours | Local analogues in a stable metric space | Simple nonparametric benchmark | Distance degrades in high dimensions; slow scoring without indexing |
| Naive Bayes | Sparse counts or a credible conditional-independence approximation | Fast, data-efficient baseline | Independence assumption can distort probabilities |
| Feed-forward ANN | Large nonlinear cross-sectional or tabular problem | Learns smooth interactions and representations | Data hungry; sensitive to scaling and regularization |
| LSTM or GRU | Ordered sequences with persistent state | Gated memory can capture lag structure | Slow recurrence; state, masking, and resets must be explicit |
| Temporal CNN | Local and multi-scale causal sequence patterns | Parallel convolutions and stable receptive fields | Padding and causal alignment are easy to get wrong |
| Transformer | Long-range interactions across tokens or time | Flexible attention and representation learning | Compute/data intensive; masks and positional time matter |
| Temporal Fusion Transformer | Multi-horizon forecasting with known and observed covariates | Gating, variable selection, quantiles, multi-horizon outputs | Complex validation and interpretation; not a default for small data |

The major boosted-tree designs are related but not identical:

- **XGBoost concepts** include regularized additive trees, shrinkage, row/column subsampling, missing-value routing, and second-order loss approximations.
- **LightGBM concepts** include histogram split search, leaf-wise growth, and techniques for sparse or high-dimensional inputs. Leaf-wise growth can overfit small samples unless constrained.
- **CatBoost concepts** include ordered target statistics and ordered boosting to reduce target leakage from categorical encodings, commonly with symmetric tree structures.

These names identify algorithm designs. The production decision must still consider feature semantics, categorical cardinality, latency, memory, governance, and artifact portability.

Market structure determines the correct sampling unit. Cross-sectional equity selection may have thousands of instruments per date but far fewer independent dates. An execution model may have millions of order-book events but only a small number of regimes and parent orders. Credit events are sparse and censored. Options observations share underlying, expiry, and surface state. Effective sample size is governed by dependence, not raw row count.

Common tasks include:

- **regression:** forward return, realized volatility, slippage, spread, volume, or recovery;
- **classification:** direction, barrier hit, fill, cancel, default, or event outcome;
- **ranking:** relative attractiveness within a point-in-time universe;
- **quantile or distribution forecasting:** conditional tails, intervals, or scenarios;
- **representation learning:** embeddings of instruments, events, text, or order flow;
- **sequence forecasting:** multi-step paths or state-dependent horizons.

Sequential control is a different problem from supervised prediction. See [47-reinforcement-learning-for-trading-and-execution.md](47-reinforcement-learning-for-trading-and-execution.md) when actions change subsequent state, fills, inventory, or reward.

## Quoting and Market Conventions
Every dataset should have a prediction contract:

- decision timestamp and timezone;
- feature cutoff and publication-lag policy;
- universe membership as known at the cutoff;
- label definition, units, horizon, and interval $[t_0,t_1]$;
- executable entry and exit price convention;
- corporate-action, roll, currency, and missing-data policy;
- sampling rule: calendar time, business time, event time, or volume time;
- output meaning: return, probability, rank, volatility, cost, or quantile;
- intended rebalance frequency, holding period, and order type.

For a forward simple return label:

```math
y_{i,t}^{(h)}
=
\frac{P^{\text{exit}}_{i,t+h}}{P^{\text{entry}}_{i,t}}-1
```

$P^{\text{entry}}$ must be a price that could be acted on after the feature cutoff. A close-to-close label is invalid if the feature includes the same closing auction result and assumes execution at that close.

A directional label can be defined as:

```math
y_{i,t}
=
\mathbb{1}\left(r_{i,t:t+h}>c_{i,t}+b\right)
```

where $c_{i,t}$ is an estimated round-trip cost and $b$ is a required edge buffer. This is different from predicting whether the raw return is merely positive. Persist the threshold used to create the label.

For cross-sectional ranking, define the group explicitly, for example all eligible securities on a date. Do not let delisted securities, future index constituents, or securities without borrow disappear retrospectively. For volatility and volume targets, specify annualization, trading calendar, overnight treatment, and zero-volume intervals.

Features require both economic time and availability time. A value for period $t$ published or revised at $\tau$ cannot enter a decision before $\tau$. Point-in-time joins should follow [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md).

## Core Pricing Framework
Let $x_{i,t}$ be a point-in-time feature vector and $y_{i,t}$ a label. Supervised learning estimates:

```math
\widehat f
=
\arg\min_{f\in\mathcal F}
\sum_{(i,t)\in\mathcal T}
w_{i,t}\mathcal L\left(y_{i,t},f(x_{i,t})\right)
+\Omega(f)
```

where $\mathcal T$ is a training fold, $w_{i,t}$ controls sampling or economic importance, $\mathcal L$ is the loss, and $\Omega$ regularizes complexity. Weights do not make overlapping observations independent; validation must still respect time and entity dependence.

### Linear and Generalized Linear Models

OLS minimizes squared error:

```math
\widehat\beta_{\text{OLS}}
=
\arg\min_\beta
\lVert y-X\beta\rVert_2^2
```

Ridge adds an $L_2$ penalty:

```math
\widehat\beta_{\text{ridge}}
=
\arg\min_\beta
\left(
\lVert y-X\beta\rVert_2^2+\lambda\lVert\beta\rVert_2^2
\right)
```

Lasso and elastic net use:

```math
\widehat\beta_{\text{EN}}
=
\arg\min_\beta
\left[
\frac{1}{2n}\lVert y-X\beta\rVert_2^2
+\lambda\left(
\alpha\lVert\beta\rVert_1
+\frac{1-\alpha}{2}\lVert\beta\rVert_2^2
\right)
\right]
```

$\alpha=1$ is lasso and $\alpha=0$ is ridge under this parameterization. Standardize continuous features within each training fold, usually leave the intercept unpenalized, and store the exact transformation with the model.

Logistic regression maps a score to an event probability:

```math
p(y=1\mid x)
=
\sigma(\beta_0+x^\top\beta)
=
\frac{1}{1+\exp[-(\beta_0+x^\top\beta)]}
```

Fit it using log loss, then test probability calibration. A profitable decision threshold need not be 0.5.

### Trees, Margins, and Local Models

A decision tree partitions the feature space and assigns a constant prediction to each leaf. A random forest averages trees fitted to bootstrapped observations with randomized feature subsets:

```math
\widehat f_{\text{RF}}(x)
=
\frac{1}{B}\sum_{b=1}^{B}T_b(x)
```

Boosting builds an additive model:

```math
F_M(x)
=
F_0(x)+\sum_{m=1}^{M}\eta\,h_m(x)
```

where each $h_m$ targets the current loss residual or gradient and $\eta$ is a learning rate. Depth, leaf size, subsampling, number of rounds, and early stopping define effective complexity.

A support-vector classifier seeks a large-margin boundary; kernels replace explicit feature expansion with similarity calculations. kNN predicts from nearby training observations and therefore requires a stable distance metric, scaled inputs, and a policy for ties and stale analogues. Naive Bayes combines class priors and conditionally independent feature likelihoods; its probabilities can be badly calibrated when correlated features repeat the same evidence.

### Neural and Sequence Models

A feed-forward neural layer is:

```math
h^{(\ell)}
=
\phi\left(W^{(\ell)}h^{(\ell-1)}+b^{(\ell)}\right)
```

LSTMs and GRUs add gates that control the retention and update of recurrent state. They are useful when a fixed lag vector hides state persistence, but the implementation must define sequence boundaries, padding, masks, and what happens after gaps or instrument changes.

A causal temporal CNN applies convolutions only to current and past inputs. Dilation can expand the receptive field without recurrence. Its left padding must not introduce future values.

Transformer attention is:

```math
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V
```

where the mask $M$ blocks unavailable or padded observations. Time encoding should represent order, elapsed time, calendar effects, and irregular gaps where relevant. The Temporal Fusion Transformer combines recurrent processing, gating, variable selection, attention, static covariates, and multi-horizon quantile outputs. Its additional structure is justified only when the forecasting problem and sample support it.

Model output is not a position. Let $\widehat c_{i,t}\geq0$ be the expected per-unit implementation hurdle in return units. First apply a symmetric no-trade band:

```math
\widehat e_{i,t}
:=
\operatorname{sign}(\widehat\mu_{i,t})
\max\left(
\lvert\widehat\mu_{i,t}\rvert-\widehat c_{i,t},
0
\right).
```

A simple cost-aware mapping is then:

```math
q_{i,t}
=
\operatorname{clip}
\left(
\frac{\widehat e_{i,t}}
{\gamma\,\widehat\sigma^2_{i,t}},
-q_i^{\max},
+q_i^{\max}
\right)
```

subject to portfolio, factor, liquidity, borrow, and turnover constraints. This maps a zero forecast to zero and never creates a short merely because costs are positive. The complete portfolio construction and PnL convention belongs in [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md).

## Worked Instrument Example
Suppose a ridge model predicts a one-day return from standardized momentum, value, and volatility features:

| Input | Value | Coefficient | Contribution |
| --- | ---: | ---: | ---: |
| Intercept | 1.00 | 0.0005 | 0.0005 |
| Momentum | 0.50 | 0.0040 | 0.0020 |
| Value | -0.20 | -0.0030 | 0.0006 |
| Volatility | 0.30 | -0.0020 | -0.0006 |

The forecast is:

```math
\widehat r
=
0.0005+(0.50)(0.0040)+(-0.20)(-0.0030)+(0.30)(-0.0020)
=
0.0025
```

or 25 basis points. Estimated spread and fees are 6 bp, impact is 5 bp at the intended size, and the strategy requires a 4 bp uncertainty buffer:

```math
\text{deployable edge}
=
25-6-5-4
=
10\text{ bp}
```

This is a candidate trade, not proof of profitability. The ridge penalty, standardization parameters, feature set, cost estimate, and 4 bp buffer must have been selected without looking at the outer test period. The final assessment uses executed prices, rejected orders, partial fills, financing, and capacity stress.

For a probability model, economics can set the threshold. If a calibrated classifier estimates $p_{\text{up}}=0.58$, conditional up and down returns are +70 bp and -60 bp, and round-trip costs are 8 bp:

```math
\mathbb E[r_{\text{net}}]
=
0.58(70)+0.42(-60)-8
=
7.4\text{ bp}
```

The result is sensitive to calibration and conditional payoff estimates, not just classification accuracy.

## Key Risk Measures and Sensitivities
Prediction quality:

- regression error, rank correlation, information coefficient, and quantile coverage;
- log loss, Brier score, precision/recall, ROC and precision-recall curves;
- reliability curves and calibration error by time, instrument group, and regime;
- residual autocorrelation, heteroskedasticity, and error by horizon;
- fold dispersion and train-to-validation-to-test decay.

Economic quality:

- gross and net PnL, turnover, spread, fees, impact, borrow, funding, and opportunity cost;
- net information ratio, drawdown, expected shortfall, tail and gap scenarios;
- capacity curves under participation, ADV, spread, and impact stress;
- hit rate conditional on payoff, exposure, holding time, and rejected fills;
- marginal contribution by feature, model, instrument, sector, regime, and trade cohort.

Model and data stability:

- coefficient path and sign stability for linear models;
- tree depth, leaf support, prediction concentration, and feature-use stability;
- gradient, activation, attention, and embedding diagnostics where material;
- feature missingness, distribution distance, category novelty, and train-serving skew;
- prediction, calibration, residual, turnover, and PnL drift;
- sensitivity to seeds, folds, windows, hyperparameters, cost assumptions, and delayed data.

Interpretability should match the model and question. Coefficients describe conditional association in their fitted scale, not causality. Tree split counts are not economic importance. Use time-blocked permutation tests, accumulated local effects or carefully bounded response curves, local decision traces, counterfactual stress, and ablation against a simple baseline. Explanations must be calculated from the same model version and feature snapshot as the prediction.

## Required Data, Curves, Surfaces, and Calibration Objects
A production dataset should include:

- instrument/entity identifier and point-in-time universe membership;
- decision time, economic time, availability time, source revision, and timezone;
- raw input, transformed value, units, missingness flag, and feature definition version;
- label start, label end, entry/exit convention, horizon, and label version;
- corporate actions, rolls, symbology, calendars, currency, and survivorship policy;
- spreads, depth, volume, borrow, fees, funding, latency, and realized fills;
- grouping keys for date, instrument, issuer, event, parent order, and correlated labels.

Useful immutable objects include:

- `FeatureDefinition`: source fields, point-in-time join, transformation, lag, and validity rules;
- `DatasetManifest`: universe, cutoffs, label contract, row hash, source versions, exclusions, and lineage;
- `FoldManifest`: train/validation/test intervals, entity groups, purged rows, embargo, and seed;
- `TransformState`: imputation, scaling, clipping, vocabulary, category statistics, and training cutoff;
- `ModelSpec`: objective, architecture, regularization, hyperparameters, feature order, and random seeds;
- `ModelArtifact`: fitted parameters, transform state, calibration mapping, code/config versions, and checksums;
- `PredictionRecord`: model ID, feature snapshot ID, raw score, calibrated output, decision, and timestamp;
- `ExecutionOutcome`: target, order, fill, cost, exposure, and realized PnL linkage.

Do not serialize only fitted weights. A model is unusable without feature order, transformations, category handling, label semantics, and training lineage.

## Numerical and Implementation Approaches
Start with a naive forecast, historical mean, OLS/logistic model, or shallow tree. A complex model should demonstrate incremental net value and robustness against that baseline.

Build validation from the deployment clock:

1. choose a chronological outer holdout for unbiased performance estimation;
2. inside each outer training period, use chronological or walk-forward inner folds for model and hyperparameter selection;
3. purge training labels whose intervals overlap a validation/test interval;
4. embargo observations after a validation/test interval when label horizon or serial dependence justifies it;
5. fit imputers, scalers, category encoders, feature selection, dimensionality reduction, and calibration only on the appropriate training fold;
6. generate out-of-fold predictions for threshold selection, stacking, and calibration;
7. refit the selected specification on permitted history, then evaluate the untouched outer fold once.

Purging and embargo solve different problems. Purging removes overlapping label information; embargo reduces near-boundary dependence after the test block. Neither repairs a feature that was itself unavailable at decision time. See [44-robust-portfolio-and-research-validation.md](44-robust-portfolio-and-research-validation.md).

Calibration methods such as logistic scaling or isotonic mapping require their own out-of-sample predictions. Check both global and conditional calibration. Recalibration can improve probabilities while leaving ranking unchanged, but frequent reactive recalibration can chase noise.

Implementation guidance by family:

- standardize linear, penalized, SVM, kNN, and neural inputs inside folds; tree splits usually do not require scale normalization;
- encode categorical variables without using future target information;
- use training-only clipping and missing-value policies, while preserving missingness indicators when informative;
- tune tree depth, leaf support, subsampling, and rounds jointly with early stopping on a chronological validation block;
- reset recurrent state at economic sequence boundaries and use explicit causal masks;
- keep known-future covariates separate from observed-only covariates in multi-horizon models;
- use stable losses and numerics for extreme logits, rare classes, and heavy-tailed targets;
- preserve raw economic outputs alongside any normalized training reward or target.

Reproducibility requires versioned source snapshots, feature code, label code, manifests, seeds, environment, model artifacts, and a deterministic scoring contract. Where exact arithmetic reproducibility is not available, define tolerance-based equivalence and record the execution environment. Retraining should be idempotent for a fixed manifest or should explain every accepted source of variation.

Deployment should use shadow scoring before capital, then constrained canaries. Monitor feature freshness, schema, prediction distribution, calibration, exposures, costs, and realized attribution. Provide a simple fallback or no-trade mode when data, model, or risk checks fail.

## Production Pitfalls and Sanity Checks
- Randomly splitting observations with overlapping forward labels.
- Standardizing, imputing, selecting features, or encoding categories before the fold split.
- Tuning on the outer holdout and continuing to call it out of sample.
- Using revised fundamentals, future constituents, backfilled estimates, or today's corporate-action map.
- Creating the label from a price unavailable at the assumed execution time.
- Treating thousands of securities on one date as thousands of independent time observations.
- Optimizing classification accuracy when positive events are rare or payoffs are asymmetric.
- Using an uncalibrated score as a probability or choosing 0.5 by habit.
- Reporting feature importance as causality or omitting instability across folds.
- Letting lasso's arbitrary choice among correlated features drive an economic narrative.
- Overfitting tree depth, sequence length, architecture, or random seed through repeated trials.
- Leaking future data through centered rolling windows, bidirectional sequence layers, padding, or attention masks.
- Forward-filling a feature across an interval when it would have become stale or invalid.
- Ignoring spread, impact, borrow, funding, partial fills, latency, and capacity.
- Measuring drift only in features while calibration, residuals, or execution costs deteriorate.
- Retraining silently after an upstream revision without retaining the previous model and dataset manifest.
- Running live with unseen categories, nonfinite features, stale inputs, or a mismatched feature order.

Release checks should fail on point-in-time violations, fold overlap, unexpected row loss, nonfinite transformations, materially uncalibrated probabilities, unstable outer-fold results, impossible turnover, cost-sensitive sign reversals, missing lineage, or absent rollback artifacts.

## Illustrative Code
```python
from dataclasses import dataclass
import math
from numbers import Integral


@dataclass(frozen=True)
class Sample:
    feature_time: int
    label_start: int
    label_end: int
    features: tuple[float, ...]
    target: float


def purged_past_training_rows(
    samples: list[Sample],
    test_rows: set[int],
) -> list[int]:
    if not test_rows:
        raise ValueError("test_rows cannot be empty")
    if any(
        not isinstance(i, Integral)
        or isinstance(i, bool)
        or i < 0
        or i >= len(samples)
        for i in test_rows
    ):
        raise ValueError("test row index is out of range")
    for sample in samples:
        timestamps = (
            sample.feature_time,
            sample.label_start,
            sample.label_end,
        )
        if any(
            not isinstance(value, Integral) or isinstance(value, bool)
            for value in timestamps
        ):
            raise ValueError("sample timestamps must be finite integers")
        if (
            sample.feature_time > sample.label_start
            or sample.label_start > sample.label_end
        ):
            raise ValueError("sample timestamps are not chronologically ordered")
        if not all(
            math.isfinite(value)
            for value in (*sample.features, sample.target)
        ):
            raise ValueError("sample features and targets must be finite")
    test_intervals = [
        (samples[i].label_start, samples[i].label_end) for i in test_rows
    ]
    first_test_start = min(start for start, _ in test_intervals)
    first_test_feature = min(samples[i].feature_time for i in test_rows)
    kept: list[int] = []
    for i, candidate in enumerate(samples):
        if i in test_rows:
            continue
        # A walk-forward outer holdout trains only on information whose
        # complete label is known before the first test label begins.
        if (
            candidate.feature_time >= first_test_feature
            or candidate.label_end >= first_test_start
        ):
            continue
        overlaps = any(
            candidate.label_start <= test_end
            and test_start <= candidate.label_end
            for test_start, test_end in test_intervals
        )
        if not overlaps:
            kept.append(i)
    return kept


def logistic_probability(intercept: float, coefficients: tuple[float, ...],
                         features: tuple[float, ...]) -> float:
    if len(coefficients) != len(features):
        raise ValueError("coefficient and feature dimensions differ")
    if not all(
        math.isfinite(value)
        for value in (intercept, *coefficients, *features)
    ):
        raise ValueError("logistic inputs must be finite")
    score = intercept + sum(b * x for b, x in zip(coefficients, features))
    if score >= 0.0:
        return 1.0 / (1.0 + math.exp(-score))
    exp_score = math.exp(score)
    return exp_score / (1.0 + exp_score)


def expected_net_return(
    probability_up: float,
    return_if_up: float,
    return_if_down: float,
    round_trip_cost: float,
) -> float:
    if not all(
        math.isfinite(value)
        for value in (
            probability_up,
            return_if_up,
            return_if_down,
            round_trip_cost,
        )
    ):
        raise ValueError("expected-return inputs must be finite")
    if not 0.0 <= probability_up <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    if round_trip_cost < 0.0:
        raise ValueError("round-trip cost must be non-negative")
    gross = (
        probability_up * return_if_up
        + (1.0 - probability_up) * return_if_down
    )
    return gross - round_trip_cost
```

## References and Further Reading
- Hastie, Tibshirani, and Friedman. *The Elements of Statistical Learning*.
- James, Witten, Hastie, Tibshirani, and Taylor. *An Introduction to Statistical Learning*.
- Breiman. "Random Forests." *Machine Learning*, 2001.
- Chen and Guestrin. "XGBoost: A Scalable Tree Boosting System." KDD, 2016.
- Ke et al. "LightGBM: A Highly Efficient Gradient Boosting Decision Tree." NeurIPS, 2017.
- Prokhorenkova et al. "CatBoost: Unbiased Boosting with Categorical Features." NeurIPS, 2018.
- Hochreiter and Schmidhuber. "Long Short-Term Memory." *Neural Computation*, 1997.
- Bai, Kolter, and Koltun. "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling." 2018.
- Vaswani et al. "Attention Is All You Need." NeurIPS, 2017.
- Lim et al. "Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting." *International Journal of Forecasting*, 2021.
- Lopez de Prado. *Advances in Financial Machine Learning*, chapters on financial labels and purged cross-validation.
- Gu, Kelly, and Xiu. "Empirical Asset Pricing via Machine Learning." *Review of Financial Studies*, 2020.
- Related example: [examples/purged-regularized-signal-model.md](examples/purged-regularized-signal-model.md).
