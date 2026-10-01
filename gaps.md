# Gaps

What Market Brief lacked or got wrong that mattered. The daily run logs each gap and bumps its tally. The weekly run marks **candidates** by the rule in README "From gap to candidate": a tag on 3+ trading days in the last 10, or a single valid `MAJOR` line (one that states **Impaired:** and **Evidence:**). Candidates are for owner review only; they authorize no work.

Log line format: `- date · tag · [MAJOR ·] what was missing. [Impaired: … Evidence: …]`

## Tally (last 10 trading days)

| Tag | Days | Last seen | Candidate (rule 1: 3+ days · rule 2: MAJOR) |
|---|---|---|---|
| macro-release | 2 | 2026-10-01 | MAJOR logged 2026-09-30 (weekly to confirm rule 2) |
| consensus | 0 | — | — |
| breadth | 0 | — | — |
| concentration | 0 | — | — |
| rates-vol | 2 | 2026-10-01 | — |
| equity-vol | 0 | — | — |
| timing | 0 | — | — |
| prose | 1 | 2026-09-30 | — |
| defect | 2 | 2026-10-01 | — |
| other | 1 | 2026-10-01 | — |

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
