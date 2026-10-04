# Point-in-Time Data and Event Systems

Related chapters: [03-equities.md](03-equities.md), [11-market-data.md](11-market-data.md), [16-portfolio-construction-and-backtesting.md](16-portfolio-construction-and-backtesting.md), [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md), and [42-fundamental-catalyst-equity-analysis.md](42-fundamental-catalyst-equity-analysis.md).

## What This Domain Covers
Point-in-time data answers a stricter question than ordinary historical data:

> What values, documents, identifiers, and event states were actually knowable at a specified decision time?

That question controls whether a backtest is credible, whether a historical risk report can be reproduced, and whether a live event strategy reacts once rather than repeatedly. A database that stores only the latest corrected record cannot answer it. Neither can a price history that silently applies today's identifier map, index membership, or corporate-action adjustment to the past.

For a quant developer, point-in-time correctness spans:

- market observations and official closes,
- security and issuer reference data,
- corporate actions and lifecycle events,
- financial statements, estimates, and later restatements,
- merger, tender, financing, and regulatory events,
- model inputs, manual overrides, and derived analytics,
- the code and configuration that transformed those inputs.

The objective is not to prevent corrections. It is to preserve both the corrected economic history and the information history seen by the system.

## Product Taxonomy and Market Structure
Useful systems distinguish several kinds of time and state.

- **Observation data** records a market value at an exchange or vendor timestamp.
- **Reference data** defines instruments, issuers, listings, contracts, currencies, and relationships between securities.
- **Effective-dated data** becomes economically valid on a particular date, such as an index rebalance or coupon reset.
- **Knowledge-dated data** becomes available to the system when received, validated, or published.
- **Event data** records announcements and transitions such as offer launch, amendment, approval, completion, default, conversion, exercise, or cancellation.
- **Derived data** records curves, surfaces, signals, risk, or positions built from versioned inputs.

An issuer can have common shares, several bond issues, loans, CDS references, convertible bonds, options, warrants, ADRs, and legacy identifiers. The security master must represent those as distinct instruments connected to the same economic entity without assuming that every instrument has the same seniority, currency, guarantor, or corporate-action treatment.

Event systems also need an explicit state model. A merger announcement is not the same object as a completed merger; a tender can be extended; a dividend can be declared, revised, go ex, and be paid. Store immutable events and derive current state rather than overwriting the previous state with a status string.

## Quoting and Market Conventions
Every timestamp must declare what it means.

- **Event time**: when the economic event occurred or the observation was valid.
- **Publication time**: when the source made it available.
- **Ingestion time**: when the internal platform received it.
- **Processing time**: when validation or transformation completed.
- **Decision time**: the cutoff used by a strategy, risk run, or report.

All timestamps should carry a time zone or be normalized to UTC while retaining the source zone and market calendar. A date without a time is not automatically safe: an earnings release after the close cannot be used in that day's close-to-close signal.

Corrections need explicit version semantics. Common choices are:

- first-known value,
- latest-known value as of a cutoff,
- final restated value,
- official value for an economic period.

For positions and trades, distinguish trade date, execution timestamp, allocation timestamp, settlement date, and accounting date. For corporate actions, distinguish announcement, record, ex, election, effective, and payment dates.

## Core Pricing Framework
A bitemporal record stores two independent intervals:

1. the **valid-time interval** during which the fact applies economically;
2. the **system-time interval** during which the platform believed that version was current.

For record version $r$, write:

```math
[v_r^{start}, v_r^{end})
```

for valid time and:

```math
[s_r^{start}, s_r^{end})
```

for system time. A point-in-time query at economic time $t$ and knowledge cutoff $\tau$ returns versions satisfying:

```math
v_r^{start} \le t < v_r^{end}
\quad\text{and}\quad
s_r^{start} \le \tau < s_r^{end}.
```

This is different from selecting the row with the latest timestamp. The latest row may be a correction that was unavailable at the historical decision time.

The same discipline applies to derived analytics. A signal should be identified by a dependency tuple such as:

```math
\text{SignalVersion}
=
(\text{data snapshot},\ \text{code version},\ \text{configuration},\ \text{calendar version}).
```

Without that tuple, "rerun the strategy for last Tuesday" is not a stable request.

## Worked Instrument Example
Suppose a company reports quarterly EPS for economic period 2026-Q1:

- 30 April at 21:05 UTC: initial EPS of USD 1.20;
- 2 May at 14:00 UTC: vendor corrects a mapping error to USD 1.02;
- 15 June at 12:00 UTC: the company files a restatement to USD 0.95.

A decision made on 1 May at 13:00 UTC may use USD 1.20. A backtest run in July must not replace that input with USD 0.95 merely because the restatement is now the latest value.

An append-only table can store:

| Value | Valid Period | Known From | Known Until | Version Reason |
| ---: | --- | --- | --- | --- |
| 1.20 | 2026-Q1 | 30 Apr 21:05 | 2 May 14:00 | Initial release |
| 1.02 | 2026-Q1 | 2 May 14:00 | 15 Jun 12:00 | Vendor correction |
| 0.95 | 2026-Q1 | 15 Jun 12:00 | Open | Issuer restatement |

The final economic history says EPS was USD 0.95. The information history says a decision on 1 May saw USD 1.20. Both statements are valid and must remain queryable.

## Key Risk Measures and Sensitivities
- Publication-to-ingestion latency by source and event type.
- Ingestion-to-availability latency after validation.
- Correction and restatement frequency.
- Missing-event and duplicate-event rate.
- Percentage of derived outputs lacking full lineage.
- Identifier collision, orphan-security, and ambiguous-issuer counts.
- Point-in-time join failure rate.
- Replay mismatch between archived and recomputed outputs.
- Fallback and manual-override usage.
- Data age at the moment a decision or risk run was produced.

Historical sensitivity should include knowledge-lag scenarios. For example, rerun a strategy with a five-minute, thirty-minute, and next-day availability lag rather than assuming instantaneous publication.

## Required Data, Curves, Surfaces, and Calibration Objects
- Canonical issuer, legal-entity, security, listing, and contract identifiers.
- Cross-reference histories for vendor identifiers, tickers, CUSIPs, ISINs, FIGIs, and internal IDs.
- Source event IDs, sequence numbers, timestamps, payload hashes, and revision reasons.
- Exchange calendars, market sessions, time zones, and publication calendars.
- Raw immutable payloads plus normalized typed records.
- Corporate-action terms and election alternatives.
- Filing metadata, document versions, sections, and extracted terms.
- Trade, order, fill, position, and cash-ledger events.
- Versioned curves, surfaces, models, overrides, and build configurations.
- Code revision, dependency lockfile, runtime image, and feature configuration.

## Numerical and Implementation Approaches
Use an append-only raw layer. Corrections should create a new version and close the previous system-time interval; they should not mutate the source history in place.

A practical decomposition is:

1. **Landing layer**: immutable source payload and receipt metadata.
2. **Normalization layer**: typed fields, units, identifiers, and source semantics.
3. **Mastering layer**: canonical entity and instrument relationships.
4. **Event layer**: deduplicated immutable domain events.
5. **State projections**: current and historical states derived by deterministic reducers.
6. **Snapshot layer**: bounded, versioned inputs for pricing, research, and risk.
7. **Lineage layer**: dependencies from every output to its inputs and code.

Idempotency keys should be based on stable source identifiers where possible, with payload hashes as a secondary control. Late and out-of-order events must be accepted without silently changing already published official outputs. Reprocessing policy should say which outputs are revised, which are frozen, and how revisions are communicated.

Use interval or as-of joins rather than equality joins for histories. Test boundaries explicitly: exact publication timestamp, market close, daylight-saving changes, and half-open interval endpoints.

For event strategies, define a state reducer:

```math
\text{State}_{n} = f(\text{State}_{n-1}, \text{Event}_{n})
```

where $f$ is deterministic, versioned, and rejects invalid transitions. This makes replay and audit much safer than directly updating a mutable row from many services.

## Production Pitfalls and Sanity Checks
- Replacing history with the latest corrected value.
- Using filing period end as though it were publication time.
- Joining today's ticker or sector classification onto old observations.
- Applying a corporate action before its effective or knowable date.
- Treating after-close and before-open announcements identically.
- Losing original units, source timezone, or raw payload.
- Deduplicating two genuine amendments because their business keys match.
- Processing the same message twice because retries lack idempotency.
- Letting late data alter an official NAV or risk report without a revision workflow.
- Replaying data without the original calendar, code, or model configuration.
- Storing a single `updated_at` column and calling the table bitemporal.

Minimum checks:

- each active interval has exactly one visible version per business key;
- intervals do not overlap unless the domain explicitly permits it;
- every normalized record traces to a raw payload;
- a replay from the same snapshot produces the same state and output hash;
- a historical decision never reads a system version created after its cutoff;
- entity and security mappings are valid on the queried date.

## Illustrative Code
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class VersionedValue:
    value: float
    valid_from: datetime
    valid_to: datetime
    known_from: datetime
    known_to: datetime


def as_of_value(
    rows: Iterable[VersionedValue],
    economic_time: datetime,
    knowledge_time: datetime,
) -> float:
    visible = [
        row
        for row in rows
        if row.valid_from <= economic_time < row.valid_to
        and row.known_from <= knowledge_time < row.known_to
    ]
    if len(visible) != 1:
        raise ValueError(f"expected one visible value, found {len(visible)}")
    return visible[0].value
```

The production implementation should use database-native range types or carefully indexed interval columns, enforce non-overlap constraints, and preserve source precision.

## References and Further Reading
- SEC, [EDGAR Application Programming Interfaces](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).
- SEC, [Developer Resources](https://www.sec.gov/about/developer-resources).
- Martin Fowler, [Bitemporal History](https://martinfowler.com/articles/bitemporal-history.html).
- ISO 8601 for date and time representation.
- Exchange and vendor corporate-action specifications used by the production platform.
- Kleppmann. *Designing Data-Intensive Applications*.
- Related chapter: [30-trade-lifecycle-and-operations.md](30-trade-lifecycle-and-operations.md).
- Worked example: [examples/bitemporal-asof-replay.md](examples/bitemporal-asof-replay.md).
