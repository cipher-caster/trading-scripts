# Mayne SMC Indicator

**Version 2.4.0** · [changelog](./CHANGELOG.md)

A Pine Script v6 (TradingView) indicator that mechanically marks the entry pieces of the Trader
Mayne Smart Money Concepts system: **order blocks, fair value gaps, market-structure bias, the
dealing-range 50%, and BUY/SELL signals**, with optional HTF-bias and liquidity-sweep gates.

- **`Mayne-SMC-Indicator.pine`** — paste into TradingView's Pine Editor (install steps below).
- **`Mayne-SMC-Strategy.pine`** — the same engine as a TradingView **strategy**: risk-sized
  entries, stop/target brackets, per-POI-type trade IDs for the Strategy Tester. See
  [Backtesting](#backtesting-the-strategy-file).
- **`guide.html`** — open in any browser for an interactive, illustrated walkthrough of the whole
  Mayne SMC method (candle diagrams for every concept) plus how to read this indicator. Start there
  if the concepts are new.

> **Not financial advice.** This is a study/testing tool. The signals are a mechanical
> approximation of a discretionary method. Backtest before you trust anything it prints, and size
> your own risk.

## Preview

The indicator on a daily BTC/USDT chart — BUY/SELL labels, MSS markers, order-block / FVG zones,
and the nearest buy/sell **zone table** (top-right):

![Mayne SMC indicator on BTCUSDT daily](./screenshots/chart-btcusdt-daily.png)

Same indicator on ETH/USDT:

![Mayne SMC indicator on ETHUSDT](./screenshots/chart-ethusdt.png)

The interactive `guide.html` — illustrated candle diagrams for every concept, with a sidebar,
collapsible rules, and a light/dark toggle:

![Visual guide — FVG section](./screenshots/guide.png)

### Source & attribution

Derived from **Trader Mayne**'s free educational series on YouTube:

- Channel: <https://www.youtube.com/@TraderMayne>
- Playlist (Trading Bootcamp / Whiteboard Series): <https://www.youtube.com/playlist?list=PLKItFyoma4GeQSNjY7LM5qtEgTFUidxYI>

This is an **independent, unofficial fan implementation** — not affiliated with, sponsored by, or
endorsed by Trader Mayne. All credit for the trading method is his; the code and notes here are my
own interpretation. Watch the original videos for the full teaching and chart examples.

---

## Which timeframe do I put this on?

The indicator reads bias and fires signals off whatever chart you open it on, and can optionally
**enforce one higher timeframe for you**: set *Signals → HTF bias timeframe* (e.g. `240` while
charting M15) and signals that disagree with that HTF's trend are suppressed. Mayne still trades
**top-down across the whole stack**, so the full hierarchy read stays yours. His stack (from Ep3,
high-timeframe bias):

| Timeframe | Job | Role here |
|---|---|---|
| **Weekly** | Macro direction — the "boss" | HTF bias |
| **Daily** | Major swings / where you are in the trend | HTF bias |
| **H4** | Local trend (last few days–2 weeks) | bridge |
| **H1 / M15** | Where you actually enter | LTF entries |

**The two execution pairs he names** (Ep3): read bias on the higher chart, take the entry on the
lower. Run the indicator on both — BIAS row on the top one, BUY/SELL signals on the bottom one.

| HTF (read BIAS) | LTF (take the signal) | Use when |
|---|---|---|
| **H12** | **H1** | Standard / swing pace. Pairs with a bearish-or-bullish Weekly above it. |
| **H4** | **M15** | Faster, smaller setups (tighter stops, more frequent). |

Don't jump Weekly straight to an hourly entry — step down through the hierarchy. Keep the Weekly
open just to confirm you're not fighting the macro.

**How to use it:** open the indicator on the **Weekly + Daily** first to read the macro bias (the
BIAS row in the table). Then move to one of the execution pairs above — bias on the higher chart,
signals on the lower. Only take the BUY/SELL labels that agree with the HTF bias you read up top.
The highest timeframe wins: if Weekly + Daily are bearish, the best M15 trade is a short, even in
an M15 uptrend. You can swap Daily for H12; the only rule is go high→low. The *HTF bias timeframe*
input can hard-enforce the immediate pair (e.g. H4 over M15), but the read above it — Weekly/Daily
— is the judgment call Mayne wants you making yourself.

---

## Install (2 minutes)

1. Open TradingView, bottom panel → **Pine Editor**.
2. Open `Mayne-SMC-Indicator.pine`, copy the whole file, paste it over the editor contents.
3. Click **Add to chart**.
4. (Optional) Gear icon on the indicator → tune the inputs (below).
5. (Optional) Right-click a signal → **Add alert** → pick "Mayne SMC BUY" / "SELL".

---

## What you'll see on the chart

| Element | On by default? | Meaning |
|---|---|---|
| **"BUY·OB 2.3R" / "SELL·FVG 1.8R" labels** | yes | A signal fired (rules below) — the suffix names the POI type that triggered it (order block vs fair value gap), and the trailing number is the trade's reward:risk at the trigger (*Risk / RR* inputs). The thing you actually trade off. |
| **Blue / purple boxes** | yes | Fair Value Gaps — blue = bullish, purple = bearish. |
| **Green / red boxes** | yes | Order Blocks — green = bullish (demand), red = bearish (supply). |
| **Dots above/below bars** | yes | **MSB** — structure break in the trend direction (continuation). Green dot below = bullish, red dot above = bearish. |
| **"MSS" labels** | yes | **MSS** — the first break *against* the trend (potential reversal / change of character). It flips the bias. Lime up / orange down. |
| **Gray lines (high / low)** | **off** | Dealing range: last swing high (BSL above) / swing low (SSL below). Toggle: *Show range high/low + equilibrium lines*. |
| **Orange line** | **off** | Equilibrium — the **50%** of the range. Above = premium, below = discount. Same toggle as above. |
| **Green/red background tint** | **off** | Trend bias on every bar. Floods the chart, so it's off by default — toggle: *Tint background by bias*. |

**Zones stop extending once used.** A box only stretches to the live bar while price *hasn't*
reached it. The moment price trades into a zone's 50% mean threshold, that zone is "mitigated"
(spent) and its box **freezes** at the bar it was hit — so old, filled zones become short
historical boxes instead of long bars blocking the chart, and only the still-actionable
(untouched) zones reach the present. Toggle: *Zone display → Stop extending zones once mitigated*
(on by default; turn off to extend every box to the present like before).

**Zones also expire from old age.** A zone untouched for *Max zone age* bars (default 500) goes
stale: its box freezes where it died, it drops off the table, and it can no longer fire a signal.
Old POIs decay — the dealing range resets every MSB, so an ancient zone isn't a real retest
candidate. The fixed bar count self-scales: 500 bars is ~5 days on M15 (fast decay where charts
get crowded) but ~10 months on 12h (HTF zones persist, correctly). Set it to 0 to let zones live
until invalidated. The visual language stays consistent either way: a box reaching the live bar =
actionable, a frozen short box = history.

If the chart still feels busy, the **boxes** are the next thing to thin out: raise *Swing length*
and *Displacement >= ATR x*, or turn off *Show FVGs* / *Show Order Blocks* to leave only the
BUY/SELL labels — though note a hidden POI type stops firing signals too (in the strategy file
that's deliberate: it lets you backtest OB-only / FVG-only variants).

---

## The zone table (top-right)

A panel that reads off the nearest **buy zones below price** (demand: bullish OBs/FVGs) and
**sell zones above price** (supply: bearish OBs/FVGs), so you can see where price is likely
headed next without eyeballing the boxes.

```
BIAS   Bullish        PRICE   42,180
RANGE  Discount       EQ      41,900
SELL ZONES (above)
 Type  Entry (range)     50%      Dist    RR
 OB    42,900 – 43,200   43,050   1.71%   2.6R
 FVG   43,400 – 43,560   43,480   2.89%   1.9R
BUY ZONES (below)
 Type  Entry (range)     50%      Dist    RR
 FVG   41,650 – 41,790   41,720   0.92%   3.1R
 OB    41,050 – 41,350   41,200   1.97%   2.2R
```

- **Type** — OB (order block) or FVG (fair value gap).
- **Entry (range)** — the full zone, bottom – top. You ladder your order across it rather than
  filling at one price — the "spray across the zone" approach.
- **50%** — the zone's mean threshold, the optimal-fill point and the level the on-chart BUY/SELL
  signal fires at. A strong zone shouldn't trade past its 50%.
- **Dist** — how far the **near edge** of the zone is from current price, in % (i.e. how far price
  has to travel to first touch the zone).
- **RR** — the reward:risk a trade triggered at that zone would offer right now (stop = far edge
  ± ATR buffer, target per *Target for RR*). Indicative: targets move as the range and zones
  evolve; the label shows the final number when a signal actually fires.

Zones are listed **nearest-first**, ranked by the near edge (the level price touches first), and
**only live zones are shown** — a zone disappears from the table once it has fired a signal or been
mitigated (price reached its 50%), so the map never lists already-spent levels. Controls live in the
**Zone Table** input group: toggle it on/off, set how many zones per side (1–6), and pick the corner.

> The table lists *candidate* zones (everywhere price could react). A zone only becomes an actual
> **BUY/SELL signal** when price reaches it **and** bias + premium/discount agree — that's when the
> label prints on the chart. Read the table as "here's the map," the labels as "here's the trigger."

---

## How a signal is generated

A **BUY** prints only when **all** of these line up on the same bar:

1. **Bias is bullish** — price has broken structure to the upside (green MSB dot; enable *Tint background by bias* for the full tint).
2. **Price is in discount** — below the orange 50% line (toggle: *Require correct half*).
3. **Price retests a bullish POI** — it trades back into a bullish order block or bullish FVG,
   reaching that zone's **50% mean threshold** (toggle: *Trigger at zone 50%*). A genuine retest
   only: the bar that *created* the zone can never fire it, and a zone whose 50% was already
   consumed on an earlier bar (mitigated) is spent — the first valid touch is the trade.
4. **(Optional) HTF bias agrees** — if *HTF bias timeframe* is set (e.g. chart on M15, input on
   240/H4), the same structure read on that higher timeframe must also be bullish. This is the
   §4 master filter, mechanized. Uses the last **confirmed** HTF bar (no repaint, one HTF
   bar of lag). Blank = off.
5. **(Optional) A liquidity sweep happened first** — if *Require liquidity sweep first* is on,
   price must have recently run the range low and closed back above it (run + rejection, §2)
   within the lookback. Off by default; cuts signals hard.
6. **(Optional) The RR clears the bar** — if *Min RR* > 0, the trade's reward:risk at the
   trigger (stop = zone far edge ± ATR buffer, target = range extreme or nearest opposing
   zone, per the *Risk / RR* inputs) must be at least that. Default 0 = readout only, no gate.

**SELL** is the exact mirror: bearish bias + premium + retest into a bearish OB/FVG (+ HTF
bearish / range-high sweep if the optional gates are on).

By default signals **confirm on bar close** (toggle: *Confirm signals on bar close*) — a label and
its alert only fire when the bar finishes, so they never appear mid-bar and vanish. Turn it off to
fire intra-bar on first touch (earlier entry, but the live bar can repaint).

Each zone fires **once**. A zone is deleted when price closes through it (invalidated), so the
chart self-cleans. This maps to the system's non-negotiables: bias first, longs in discount /
shorts in premium, enter at the POI mean threshold.

---

## Inputs that matter

| Input | Default | Raise it to… |
|---|---|---|
| **Swing length** | 2 | Catch only bigger, more significant structure (fewer, cleaner swings). |
| **Marker distance from candle (×ATR)** | 0.1 | Push BUY/SELL/MSB/MSS markers further from the candle; lower = flush, 0 = right at the high/low. |
| **Displacement: range >= ATR x** | 1.5 | Demand stronger displacement candles before trusting an FVG/OB. |
| **Require displacement on middle candle** (FVG) | on | Filter weak gaps; off = mark every 3-candle gap. |
| **Only OBs whose move breaks structure** | on | Keep only order blocks whose displacement broke structure (highest-prob). |
| **Require correct half (discount/premium)** | on | Enforce the buy-low/sell-high rule. Turn off to see every POI retest. |
| **Trigger at zone 50%** | on | Signal at the zone midpoint (mean threshold). Off = signal on first touch of the zone edge. |
| **HTF bias timeframe** | blank (off) | Set it (e.g. `240` for H4 while charting M15) to only allow signals that agree with the higher-timeframe trend — the §4 master filter. Must be higher than the chart TF; equal/lower disables it. |
| **Confirm signals on bar close** | on | Signals/alerts wait for the bar to close — no intra-bar flicker. Off = fire on first touch. |
| **Require liquidity sweep first** | off | Only signal after a recent run + rejection of the range low (longs) / high (shorts). The §2 sweep rule; strict, so opt-in. |
| **Sweep lookback (bars)** | 20 | How recent that sweep must be. |
| **Stop buffer beyond far edge (×ATR)** | 0.25 | Give the stop more room past the zone's far edge (feeds the RR readout and the strategy's brackets). |
| **Target for RR** | Range extreme | Switch to *Nearest opposing zone* for more conservative targets (first obstacle instead of the full range). |
| **Min RR to allow a signal** | 0 (off) | Suppress signals that don't offer at least this reward:risk at the trigger. |
| **Max zone age (bars)** | 500 | Expire zones untouched for this long (frozen box, no table, no signals). Lower it to declutter LTF charts faster; 0 = never expire. |

---

## Backtesting (the strategy file)

`Mayne-SMC-Strategy.pine` is the indicator's engine wrapped in a TradingView **strategy**, so the
Strategy Tester can put numbers on the signals. Install it exactly like the indicator (paste into
the Pine Editor → Add to chart), then open the **Strategy Tester** tab.

- **Same signals, same gates.** Inputs mirror the indicator (the *Zone Table* group is dropped; a
  *Backtest* group is added). One semantic change: *Use FVGs / Order Blocks as POIs* removes that
  zone type from the system entirely, so you can score an OB-only or FVG-only variant.
- **Entries** fill on the bar **after** a signal confirms (no peeking), sized so the distance to
  the stop risks *Risk per trade* % of current equity (compounding). Risk is measured from the
  signal bar's close (the fill proxy), while the RR label is computed at the zone trigger — so a
  trade's realized RR can come in under the labeled number when price closed away from the
  trigger.
- **Exits** are a bracket attached to every entry: stop = zone far edge ± the ATR buffer, limit =
  the RR target. Opposite signals reverse the position; signals with no computable stop/target
  are skipped, so every recorded trade has a full bracket.
- **Per-POI-type results:** entry IDs are `L-OB` / `L-FVG` / `S-OB` / `S-FVG` — read the List of
  Trades (or export CSV) to see which zone kind actually performs.
- **Honest numbers:** set your venue's real commission in Properties (default 0.05%/side). Margin
  isn't simulated, so a tight stop can imply notional > equity — keep *Risk per trade* small if
  you'd never lever. A wide bar that spans both stop and target resolves by TradingView's OHLC
  heuristic; enable **Bar Magnifier** (paid plans) for finer intrabar fills. Results are
  estimates, not promises.

---

## Honest limits — what it does NOT do

- **The HTF gate is one timeframe, not the full stack.** *HTF bias timeframe* enforces agreement
  with one higher chart, but Mayne's read is Weekly → Daily → H4 → entry. The top-down judgment
  across the whole hierarchy — and spotting when the HTF is mid-pullback vs reversing — is still
  yours. Keep the Weekly open.
- **The sweep filter is mechanical, not the full §2 definition.** It checks run + rejection on the
  current unbroken swing level only — it can't judge equal highs/lows further back, sweep quality,
  or whether displacement followed (OBs require displacement anyway; FVGs optionally).
- **No SMT / kill-zone / Judas logic.** Those are the discretionary edges; the script can't
  judge them. And while there is now an RR readout/gate and a backtest bracket, its stops and
  targets are mechanical conventions (zone edge ± ATR, range extreme / next zone) — sane
  defaults, not Mayne's read of an individual setup. A signal means "a POI is being retested in
  the right context" — not "take this trade."
- **Confirms with lag (not a bug).** Swings need `Swing length` bars to the right before they
  confirm, the HTF gate uses the last closed HTF bar, and signals default to bar-close
  confirmation — everything appears a few bars late rather than repainting.
- **Standard charts only.** Heikin Ashi / Renko / Kagi / P&F / Range charts are rejected at
  load — their synthetic OHLC would fabricate structure levels, zones, and signals.
