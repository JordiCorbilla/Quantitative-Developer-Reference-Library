# Market Data for Quant Systems

Related chapters: [00-overview.md](00-overview.md), [06-interest-rates.md](06-interest-rates.md), [10-numerical-methods.md](10-numerical-methods.md), and [12-pricing-architecture.md](12-pricing-architecture.md).

## What This Domain Covers
Market data is not a support function around pricing. It is part of the pricing model. Quant systems are only as good as their identifiers, timestamps, quote conventions, cleaning rules, and transformation pipelines.

## Product Taxonomy and Market Structure
- Reference data: instrument definitions, calendars, identifiers, contract specs
- Real-time prices and end-of-day closes
- Curves, surfaces, cubes, and fixings
- Vendor data, broker runs, exchange feeds, and internally derived data
- Golden-source and consensus-mark workflows

## Quoting and Market Conventions
- Every quote must carry type, units, timestamp, source, and market context.
- Bid, ask, mid, last, evaluated, and broker quote are different objects.
- Curves and surfaces inherit conventions from the quoting instruments used to build them.
- Time zones, market close definitions, and fixing windows matter.

## Core Pricing Framework
The key market-data problem is transformation:
- raw observations,
- validation and outlier handling,
- normalization to internal conventions,
- derived objects such as curves and surfaces,
- versioned snapshots consumed by analytics.

Quant developers should distinguish:
- observed data,
- cleaned data,
- consensus or official marks,
- derived model state.

## Key Risk Measures and Sensitivities
- Sensitivity of valuation to missing or stale market inputs
- Sensitivity of downstream analytics to interpolation or cleaning rules
- Data-quality KPIs: staleness, completeness, outlier rate, fallback usage
- Exposure to vendor mapping or symbology errors

## Required Data, Curves, Surfaces, and Calibration Objects
- Instrument master and canonical identifiers
- Calendar and schedule metadata
- Historical time series with adjustment policy
- Quote-convention metadata for every asset class
- Versioned curve and surface snapshots
- Audit trail for overrides, manual marks, and consensus processes

## Numerical and Implementation Approaches
- Build explicit schemas for each quote type; do not rely on loosely typed maps.
- Separate feed handlers from normalized market-state objects.
- Version derived curves and surfaces with both input lineage and build configuration.
- Use hard validation for impossible data and soft validation for suspicious-but-possible data.
- Design for replay: historical analytics should be reproducible from archived market snapshots.

## Production Pitfalls and Sanity Checks
- Timestamps from different time zones merged as if they were synchronous.
- Curve builds succeeding with partial or stale inputs without a visible warning.
- Identifier remaps breaking historical joins.
- Manual overrides applied without lineage or expiry.
- Derived objects cached across market dates.

## Illustrative Code
```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Quote:
    symbol: str
    value: float
    quote_type: str
    source: str
    timestamp: datetime


def is_stale(quote: Quote, now: datetime, max_age_seconds: int) -> bool:
    return (now - quote.timestamp).total_seconds() > max_age_seconds
```

## References and Further Reading
- Vendor and exchange data dictionaries used in your stack
- Enterprise data-management patterns for golden-source and lineage control
- Chapter links: [12-pricing-architecture.md](12-pricing-architecture.md) and [14-testing-and-validation.md](14-testing-and-validation.md)
