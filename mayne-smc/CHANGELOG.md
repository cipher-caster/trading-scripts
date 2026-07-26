# Changelog — Mayne SMC Indicator

All notable changes to the indicator and its guide. Versioning is loosely
[semantic](https://semver.org/): MAJOR for breaking changes to signals/behaviour, MINOR for new
features or inputs, PATCH for fixes and doc/visual tweaks.

## [2.3.0] — 2026-07-26

Audit pass over v2.2 — three correctness fixes plus two robustness tweaks. No new inputs.

- **Fix (signals): order blocks no longer die "mitigated at birth".** The 50% mean-threshold
  check counted the zone's own creation bar. The displacement candle that confirms an OB almost
  always opens *inside* that OB, so most immediate OBs were flagged spent the moment they were
  created — they could never fire a signal, never appeared in the zone table, and their boxes
  froze instantly (a regression introduced by the 2.1 spent-zone fix; FVGs were unaffected,
  which is why charts skewed FVG-heavy). Touches now only count **after** the creation bar,
  matching the documented rule ("the first valid touch is the trade"). Expect more OB signals
  and table entries than in 2.1–2.2 — that's the bug being removed, not a looser rule.
- **Fix (HTF gate): backtests no longer lag one extra HTF bar.** The confirmed-bar fetch used
  `[1]` + `lookahead_off`, which serves historical bars the trend from *two* HTF bars back
  while realtime bars get one — so history ran a staler bias than live and rewrote on reload.
  Switched to the canonical non-repaint idiom (`[1]` + `lookahead_on`): the same one-bar lag
  everywhere; live behaviour unchanged.
- **Fix (table): readable on dark themes.** Zone rows and the RANGE/EQ header values relied on
  `table.cell`'s default black text, invisible on dark charts. Text colors are now explicit
  (`chart.fg_color`; white on headers).
- Alert messages now include `{{ticker}} {{interval}}` (and `{{close}}` on BUY/SELL), so alerts
  fired from multiple charts are tellable apart.
- Non-standard chart types (Heikin Ashi, Renko, Kagi, P&F, Range) are rejected with a clear
  error instead of silently computing structure and zones off synthetic prices.

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
