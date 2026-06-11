# Changelog — Mayne SMC Indicator

All notable changes to the indicator and its guide. Versioning is loosely
[semantic](https://semver.org/): MAJOR for breaking changes to signals/behaviour, MINOR for new
features or inputs, PATCH for fixes and doc/visual tweaks.

## [2.2.0] — 2026-06-11

- **Zone age expiry** (new input *Max zone age*, default 500 bars): a zone untouched for that
  many bars goes stale — its box freezes where it died, it drops off the table, and it can no
  longer fire a signal. The fixed bar count self-scales (≈5 days on M15, ≈10 months on 12h). Set
  to 0 to keep the old "live until invalidated" behaviour.

## [2.1.0] — 2026-06-11

- **Fix:** a spent (mitigated) zone can no longer fire a signal on a later revisit — only the
  first valid touch is a trade.
- **Fix:** the HTF bias gate self-disables when the selected timeframe is not strictly higher than
  the chart's, instead of silently comparing a timeframe to itself.

## [2.0.0] — 2026-06-11

Signals overhaul — adds the two discretionary gates from the method as optional filters, plus
several correctness fixes. MINOR-flagged behaviour changes to signals, hence the major bump.

- **HTF bias gate** (new input *HTF bias timeframe*): suppress signals that disagree with a higher
  timeframe's trend — the §4 master filter, mechanized. Uses the last confirmed HTF bar (no
  repaint). Blank = off.
- **Liquidity-sweep filter** (new input *Require liquidity sweep first* + *Sweep lookback*): only
  signal after a recent run + rejection of the range low/high (§2). Off by default.
- **Bar-close confirmation** (new input *Confirm signals on bar close*, on by default): labels and
  alerts wait for the bar to finish, so they never appear mid-bar and vanish.
- **Retest fix:** the bar that *creates* a zone can no longer fire it on the same bar.
- **Order-block dedup:** a single candle can only be claimed as one order block.
- **Zone table** now hides spent (fired/mitigated) zones, so the map lists only live levels.
- **BUY·OB / SELL·FVG labels:** the signal label now names which POI type triggered it.
- True box origins (boxes anchor at the bar that formed the zone).

## [1.0.0] — 2026-06-07

Initial public release.

- Pine v6 indicator (`Mayne-SMC-Indicator.pine`): order blocks, fair value gaps, MSB/MSS
  market-structure bias, dealing-range premium/discount + 50% equilibrium, and BUY/SELL signals
  on POI retests in the correct half of the range.
- Nearest buy/sell **zone table** (top-right) with entry range, 50% mean threshold, and distance.
- Zones freeze once mitigated so spent boxes stop blocking the chart.
- Interactive **`guide.html`**: illustrated, single-page walkthrough of the full Mayne SMC method
  (candle diagrams for every concept) plus how to read this indicator. Self-contained, offline.
