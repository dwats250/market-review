# Gaps

What Market Brief lacked or got wrong that mattered. The daily run logs each gap and bumps its tally. The weekly run marks **candidates** by the rule in README "From gap to candidate": a tag on 3+ trading days in the last 10, or a single valid `MAJOR` line (one that states **Impaired:** and **Evidence:**). Candidates are for owner review only; they authorize no work.

Log line format: `- date · tag · [MAJOR ·] what was missing. [Impaired: … Evidence: …]`

## Tally (last 10 trading days)

| Tag | Days | Last seen | Candidate (rule 1: 3+ days · rule 2: MAJOR) |
|---|---|---|---|
| macro-release | 5 | 2026-10-09 | **Candidate** (rules 1 and 2; W40) |
| consensus | 0 | — | — |
| breadth | 2 | 2026-10-09 | — |
| concentration | 0 | — | — |
| rates-vol | 4 | 2026-10-05 | **Candidate** (rule 1; W40) |
| equity-vol | 0 | — | — |
| timing | 0 | — | — |
| prose | 1 | 2026-09-30 | — |
| defect | 6 | 2026-10-09 | **Candidate** (rule 1; W40). Kinds: missed publications Sep 30, Oct 1, Oct 5; evidence consistency Oct 2, Oct 5; watch adjudication Oct 8, Oct 9; missing index prints Oct 9 (MAJOR) |
| other | 3 | 2026-10-09 | Meets rule 1 (Oct 1, 8, 9); for the weekly to confirm |

Candidate design questions: `weekly/2026/2026-W40.md` section 4. For owner review only.

**Fix status** (recorded so a fixed gap is not treated as open, and a fix is not treated as proven):
- `macro-release`: FIX IMPLEMENTED — FORWARD VERIFICATION REQUIRED. market-brief PRs #47 (BLS calendar) and #48 (BLS Employment Situation and CPI actuals), merged Oct 2 after the close. First test: CPI, Oct 14. Not covered: BEA (PCE, GDP), ISM, DOL claims.
- `defect` (missed publications): FIX IMPLEMENTED — FORWARD VERIFICATION REQUIRED. market-brief PR #46 (scheduler liveness), merged Oct 1. Oct 2 published 9 of 9; Oct 5 missed CLOSE_1M (8 of 9).

## Log

- 2026-09-30 · `macro-release` · Tuesday's Conference Board confidence (81.9 vs 89.2 consensus, 88.6 prior) and JOLTS (7.08M vs 7.23M) never reached the brief. Today's premarket read gold's bounce as short covering; a haven bid after a big confidence miss is the competing explanation it couldn't weigh.
- 2026-09-30 · `prose` · At the opening update the energy watch (horizon "into the close") moved to "Earlier watches · ended without a verdict" hours before its horizon: it was displaced by the carry limit, not expired. Known review item F7 (label wording).
- 2026-09-30 · `macro-release` · MAJOR · The day's 8:15/8:30 ET releases (ADP +90k, GDP Q2 revised to 2.2% from 1.5%, August core PCE 0.2% m/m and 3.0% y/y, goods trade) were missing from both syntheses (BLS 403, BEA not collected). Impaired: the premarket bid was read as gold short covering plus "easier front-end rates", and the 7:02 page said the prior-day steepener "explains none of it". Evidence: the releases came before the 6:02 AM PT page; the S&P went from about +0.7% to −0.25% as the 10Y rose +3 bp to 5.29% (Treasury, Sep 30).
- 2026-09-30 · `defect` · HOURLY_1300, HOURLY_1400, HOURLY_1500 and CLOSE_1M never published (5 of 9); no page covered the reversal or the close.
- 2026-09-30 · `rates-vol` · Rates block showed only Tuesday's par curve (live yields not collected); the intraday move to a 2002-high 10Y never reached the page.
- 2026-10-01 · `defect` · OPEN_30M never published (7:00 AM PT): no post-open synthesis; the premarket read stood all day and the opening-hour watch had no print inside its horizon.
- 2026-10-01 · `rates-vol` · Rates block showed only Wednesday's par curve (live yields not collected); the morning spike to a 5.34% 10Y and its retreat, which set the equity path, never reached the page.
- 2026-10-01 · `macro-release` · ISM manufacturing (prices paid 77.9 from 71.1), jobless claims (197k) and construction spending never reached the brief (BLS 403; ISM and Census not collected).
- 2026-10-01 · `other` · Crude and DXY not collected: XLE +1.97% appeared without its cause (China fuel-export halt, Brent above $100) or the dollar's +0.65%.
- 2026-10-02 · `macro-release` · MAJOR · The September jobs report (payrolls +29k vs ~84–90k; −60k revisions; unemployment 4.2%), out at 5:30 AM PT, was absent from the 6:02 premarket. Impaired: the bid in tech and gold was explained as "falling front-end yields in the prior-day curve"; the session was a payrolls repricing (October hike odds ~28% → 12–14%) that partly reversed. Evidence: the release preceded the page by 32 minutes; the page cites only Thursday's curve; the close page lists the release under Events with no figures. Fix landed after the close (PRs #47, #48); forward verification at CPI, Oct 14.
- 2026-10-02 · `defect` · Evidence consistency: the 7:02 miners-watch verdict "no current GDX print" was carried onto the 11:00, 1:00 PM and close pages, which showed GDX prints (+1.15% vs GLD −0.68% at 12:59). The confirm condition was met on the page's own figures but left "unresolved". The SPY 50DMA watch likewise still read "no close has printed yet" on the close page.
- 2026-10-02 · `rates-vol` · Rates block showed only Thursday's par curve; the page called the prior-day bull steepener "a friendlier backdrop" all day while yields fell on the payrolls report and the front end closed higher (2Y +5 bp, 10Y +4 bp).
- 2026-10-05 · `defect` · CLOSE_1M never published (1:01 PM PT); last page the 12:02 PM PT refresh. First miss since PR #46.
- 2026-10-05 · `defect` · Evidence consistency: the 7:02 "industrials slip" read (XLI −0.61%) was carried through 12:02, when the page's own table showed XLI +0.33% and all sectors but XLRE up; no SPY print all day.
- 2026-10-05 · `macro-release` · ISM services (prices 74.0 from 72.6; headline 54.9 from 55.4), out at 7:00 AM PT, never reached the brief (ISM not collected; no synthesis after 7:02).
- 2026-10-05 · `rates-vol` · Rates block showed only Friday's curve; the 10Y's new 2002 high (~5.31–5.35%) and bear steepening never reached the page.
- 2026-10-08 · `defect` · Watch adjudication: the close page left the staples watch (into the close) without a verdict, although its own table met the confirm (XLP +2.07%, XLK −1.79%), and carried "No current XLE print" beside XLE +2.90%. Cause: by design, not model reasoning. Refresh and close pages carry watches unchanged ("nothing is reassessed", `continuity.py` `carried_state`). Whether the Oct 2 and Oct 5 cases share this cause is not checked.
- 2026-10-08 · `other` · Missing evidence: crude and news not collected. XLE +2.90% shown "with no news here to explain it" on a day WTI settled +3.64% and Brent +4.07% on Hormuz headlines. The Brief flagged the gap itself.
- 2026-10-08 · `breadth` · Missing evidence plus cadence: no constituent breadth and no analysis after 7:02. The thrust came after 12:30 ET (SPX median +0.82%, 67.5% advancing at 3:55 PM ET) with the Nasdaq-100 down (lab); the 7:02 read fit breadth at the time.
- 2026-10-09 · `defect` · MAJOR · No SPY, QQQ or NVDA print on any page after 6:02 AM PT; three watches untested and the 7:03 read "can't tell whether it lifts the tape". Impaired: the 7:03 "technology stalls" rotation call stood all day. Evidence: the page's own words; S&P 500 +0.59%, Dow +0.83%; lab SPX 63.5% advancing, NDX 69.0% at 10:00 ET.
- 2026-10-09 · `defect` · Watch adjudication, fourth time: gold/miners watch unjudged with its confirm met on the page's own table (GLD +1.57%, GDX +2.95%); XLV and SPY-vs-QQQ watches without verdicts. Same `carried_state` cause as Oct 8.
- 2026-10-09 · `macro-release` · UMich October prelim (46.3 from 48.1; 1-yr inflation expectations 4.7%) at 10:00 ET not collected. Not MAJOR.
- 2026-10-09 · `breadth` · Constituent breadth not collected: a broad advance (lab SPX 62.7% advancing, NDX median +0.58% at the close) behind a flat cap-weighted XLK at 7:03.
- 2026-10-09 · `other` · News not collected: the premarket IRGC tanker strike preceded the gold bid the page called "a first hint of haven demand" without a cause.
