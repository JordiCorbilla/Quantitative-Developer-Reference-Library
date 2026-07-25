# Production Quant Engineering

Related chapters: [10-numerical-methods.md](10-numerical-methods.md), [11-market-data.md](11-market-data.md), [12-pricing-architecture.md](12-pricing-architecture.md), [14-testing-and-validation.md](14-testing-and-validation.md), [15-performance-and-production.md](15-performance-and-production.md), and [40-point-in-time-data-and-event-systems.md](40-point-in-time-data-and-event-systems.md).

## What This Domain Covers
Production quant engineering turns a mathematical method into a controlled service that can price trades, compute risk, replay decisions, and survive real market conditions.

The important skills are broader than writing a correct function:

- representing instruments and market state without ambiguous units,
- separating pure numerical logic from I/O and workflow code,
- processing large position and market-data sets,
- distributing work without losing determinism or diagnostics,
- testing models at formula, component, workflow, and regression levels,
- deploying and observing services safely,
- diagnosing whether a bad number came from data, conventions, models, code, or infrastructure.

A useful learning project should therefore include Python and SQL, typed domain models, batch and service interfaces, automated tests, representative data fixtures, performance measurements, and failure injection. C++ or another compiled language becomes valuable when profiling demonstrates that critical kernels cannot meet latency or throughput requirements in the higher-level implementation.

## Product Taxonomy and Market Structure
Quant platforms commonly support several workload classes.

- **Research workflows** favor iteration speed, point-in-time data access, and reproducibility.
- **Pre-trade analytics** require bounded latency, clear failure modes, and current market state.
- **Intraday risk** requires incremental updates, portfolio aggregation, and scalable scenario evaluation.
- **End-of-day valuation** favors completeness, reconciliation, rerunnability, and official snapshots.
- **Calibration services** build curves and surfaces shared across many downstream calculations.
- **Event processors** consume trades, fills, market updates, and corporate actions in order.
- **Data pipelines** ingest, normalize, validate, version, and publish large financial datasets.

The same pricing kernel may serve several workflows, but the service contract should differ. A notebook may tolerate a partial result with warnings; an official valuation run may need to fail the affected book and prevent publication.

System boundaries should align with ownership of state:

- instrument definition,
- market snapshot,
- model configuration,
- pricing engine,
- scenario definition,
- position and cash ledger,
- results and diagnostics.

## Quoting and Market Conventions
APIs must carry the conventions that formulas often hide.

- Currency, units, notional basis, price multiplier, and quote type.
- Valuation timestamp, market-data snapshot ID, and calendar version.
- Day count, business-day adjustment, settlement lag, and exercise style.
- Bump definition: absolute, relative, basis-point, volatility-point, or scenario replacement.
- Risk aggregation basis: local currency, reporting currency, or hedged base currency.
- Missing-data and fallback policy.
- Model and calibration version.

Numeric types should reflect intent. Do not pass an unlabelled `float` when the value might be a decimal rate, percentage, basis points, money amount, or price per unit. Even when runtime representation remains a floating-point number, typed wrappers or explicit field names prevent unit errors.

SQL schemas should use fixed-precision decimal types for contractual money and quantities where exactness matters. Floating-point types remain appropriate for model parameters and numerical calculations, but final cash ledgers should have documented rounding rules.

## Core Pricing Framework
A production calculation is a function of more than the trade:

$$
R =
F(
T,\ M,\ \Theta,\ S,\ C,\ V
)
$$

where:

- \(T\) is the immutable trade or position definition;
- \(M\) is a versioned market snapshot;
- \(\Theta\) is model and calibration state;
- \(S\) is the scenario or risk request;
- \(C\) is configuration and convention metadata;
- \(V\) is the code/runtime version.

The output \(R\) should include:

- requested measures,
- calculation status,
- diagnostics and warnings,
- input and dependency identifiers,
- timing and resource metrics.

For distributed portfolio risk, let trades be partitioned into deterministic shards \(P_k\). If \(r_i\) is an additive risk vector for trade \(i\), portfolio risk is:

$$
r_{\text{portfolio}}
=
\sum_{k=1}^{K}
\left(
\sum_{i \in P_k} r_i
\right).
$$

Not every measure is additive. VaR, expected shortfall, netting-set exposure, option-implied correlation, and portfolio optimization may require scenario-level or state-level aggregation before the final statistic is computed. The map/reduce boundary must follow the mathematics rather than convenience.

## Worked Instrument Example
Assume an intraday risk request contains 120,000 trades and 250 scenarios. A monolithic worker processes 2,000 trade-scenarios per second:

$$
\frac{120{,}000 \times 250}{2{,}000}
= 15{,}000 \text{ seconds}.
$$

That is more than four hours. With 100 workers and ideal scaling, the lower bound is 150 seconds, but real performance also includes:

- snapshot distribution,
- deserialization,
- curve and model initialization,
- uneven trade complexity,
- retries and failed shards,
- result aggregation.

Suppose measured timings are:

- 18 seconds to distribute immutable shared state,
- 172 seconds for the slowest shard,
- 11 seconds to aggregate and validate.

End-to-end latency is 201 seconds, not the average worker time. The slowest shard dominates. A better partitioner weights trades by historical cost or product complexity rather than allocating equal trade counts.

The run is publishable only if:

- every expected shard reports a terminal status,
- snapshot and code IDs agree across shards,
- duplicate results are rejected,
- additive totals reconcile to independent control totals,
- non-additive metrics are calculated from complete scenario vectors.

## Key Risk Measures and Sensitivities
- Latency percentiles by product, measure, and book.
- Throughput in trades, scenarios, or cashflows per second.
- Slowest-shard and workload-skew ratio.
- Error, timeout, retry, and fallback rates.
- Queue age and consumer lag.
- Cache hit rate plus invalidation correctness.
- Memory high-water mark and allocation rate.
- Numerical convergence and calibration failure rate.
- Reproducibility hash mismatch rate.
- Percentage of results missing diagnostics or lineage.
- Deployment error-budget consumption.
- Data pipeline completeness, freshness, and duplicate rate.

Risk controls should distinguish business failures from infrastructure failures. "No valid volatility surface" is not the same as "worker unavailable," and the remediation and publication policy should differ.

## Required Data, Curves, Surfaces, and Calibration Objects
- Representative trades and portfolios, including difficult edge cases.
- Versioned market snapshots and calibration fixtures.
- Scenario grids and expected result schemas.
- Historical runtime and memory cost by product.
- Golden prices and risk measures from independent implementations.
- SQL schemas for trades, market data, runs, results, and lineage.
- Service-level objectives and error budgets.
- Deployment manifests, environment configuration, and secrets references.
- Dependency lockfiles and runtime image digests.
- Structured logs, traces, metrics, and correlation IDs.

A learning repository should include small public or synthetic fixtures with explicit licenses and generation rules. Synthetic data is useful for testing known invariants, but it should not be presented as evidence of market realism.

## Numerical and Implementation Approaches
Keep the core calculation as pure as practical:

```text
trade + market + model + request -> result + diagnostics
```

Place database access, network calls, retries, and publication outside the numerical kernel. This makes unit tests deterministic and allows the same engine to run in a notebook, batch job, or service.

Recommended layers:

1. **Domain model**: immutable typed trades, market objects, scenarios, and results.
2. **Numerical kernels**: pricing, calibration, interpolation, simulation, and aggregation.
3. **Application layer**: workflow orchestration and validation policy.
4. **Adapters**: SQL, object storage, message buses, vendors, and service protocols.
5. **Operations layer**: scheduling, deployment, observability, and access control.

Testing should form a quantitative pyramid:

- formula and invariant tests,
- property-based tests over generated inputs,
- component tests with fixed market snapshots,
- cross-model and replication tests,
- workflow integration tests,
- golden-book regression tests,
- load, soak, recovery, and failure-injection tests.

Continuous integration should run fast deterministic tests on every change and deeper regression/performance suites on a schedule or before release. Performance thresholds need tolerances and representative hardware; otherwise benchmarks become noisy gates.

For distributed work:

- use stable run and shard identifiers;
- make workers idempotent;
- checkpoint expensive stages;
- use bounded retries with classified errors;
- preserve partial diagnostics;
- aggregate in a deterministic order when floating-point reproducibility matters;
- separate shared immutable state from task-specific payloads.

Use vectorization and compiled kernels for measured hot paths. Avoid translating an entire system into a lower-level language before profiling. Crossing a language boundary also adds serialization, ownership, debugging, and deployment costs.

## Production Pitfalls and Sanity Checks
- A pricing function reads current global market state during a historical replay.
- Results lack market snapshot, model, or code identifiers.
- A retry publishes the same shard twice.
- Missing shards are treated as zero risk.
- Equal-count partitions create extreme runtime skew.
- Workers use different calendar, curve, or dependency versions.
- Cached values survive a market or configuration change.
- Tests assert only stored numbers and never economic invariants.
- Golden files are regenerated automatically after every failure.
- A vectorized rewrite changes NaN, boundary, or rounding behavior.
- Mean latency improves while tail latency and timeouts worsen.
- Sensitive data or credentials appear in logs.
- Observability records success even when the calculation used a fallback.

Minimum controls:

- put-call parity, monotonicity, cashflow conservation, and aggregation invariants hold;
- repeated runs from the same dependencies yield the same result within declared tolerance;
- every run knows its expected shard set and rejects duplicate terminal output;
- failure and fallback statuses propagate to the portfolio result;
- load tests use a distribution of real product complexity, not one easy trade;
- deployment supports rollback and preserves schema compatibility.

## Illustrative Code
```python
from collections.abc import Iterable
from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class RiskRow:
    trade_id: str
    delta: float
    vega: float


def shard_for(trade_id: str, shard_count: int) -> int:
    if shard_count <= 0:
        raise ValueError("shard_count must be positive")
    digest = sha256(trade_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % shard_count


def aggregate(rows: Iterable[RiskRow]) -> tuple[float, float]:
    ordered = sorted(rows, key=lambda row: row.trade_id)
    delta = sum(row.delta for row in ordered)
    vega = sum(row.vega for row in ordered)
    return delta, vega
```

Stable partitioning helps retries find the same work, while stable aggregation order reduces avoidable floating-point variation. Production systems should also validate run IDs, snapshot IDs, expected shard counts, and duplicate trade results.

## References and Further Reading
- Kleppmann. *Designing Data-Intensive Applications*.
- Fowler. *Patterns of Enterprise Application Architecture*.
- Beyer et al. *Site Reliability Engineering*.
- Python, [Typing documentation](https://docs.python.org/3/library/typing.html).
- NumPy, [CPU and SIMD Optimizations](https://numpy.org/doc/stable/reference/simd/).
- PostgreSQL, [Numeric Types](https://www.postgresql.org/docs/current/datatype-numeric.html).
- OpenTelemetry, [Documentation](https://opentelemetry.io/docs/).
- Related chapters: [14-testing-and-validation.md](14-testing-and-validation.md) and [15-performance-and-production.md](15-performance-and-production.md).
- Worked example: [examples/distributed-risk-partition.md](examples/distributed-risk-partition.md).
