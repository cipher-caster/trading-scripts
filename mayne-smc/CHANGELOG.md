# Changelog — Mayne SMC Indicator

All notable changes to the indicator and its guide. Versioning is loosely
[semantic](https://semver.org/): MAJOR for breaking changes to signals/behaviour, MINOR for new
features or inputs, PATCH for fixes and doc/visual tweaks.

## [1.0.0] — 2026-06-07

Initial public release.

- Pine v6 indicator (`Mayne-SMC-Indicator.pine`): order blocks, fair value gaps, MSB/MSS
  market-structure bias, dealing-range premium/discount + 50% equilibrium, and BUY/SELL signals
  on POI retests in the correct half of the range.
- Nearest buy/sell **zone table** (top-right) with entry range, 50% mean threshold, and distance.
- Zones freeze once mitigated so spent boxes stop blocking the chart.
- Interactive **`guide.html`**: illustrated, single-page walkthrough of the full Mayne SMC method
  (candle diagrams for every concept) plus how to read this indicator. Self-contained, offline.
