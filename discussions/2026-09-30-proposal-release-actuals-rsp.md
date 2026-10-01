# Proposal — Release actuals and RSP in Market Brief

Date: 2026-09-30
Status: proposal for owner and ChatGPT review. Context, not authority. Nothing is built until the owner rules; then a PRD goes to Claude Code.
Trigger: the journal's first MAJOR gap (`gaps.md`, 2026-09-30 `macro-release`).

## Why

On Sep 30, PCE, GDP and ADP came out at 8:15–8:30 ET (5:15–5:30 AM PT), half an hour before the 6:00 AM PT premarket run. The brief never saw them. Market Brief collects release *times* only, from the BLS calendar, and that feed has returned HTTP 403 on every run. BEA (PCE, GDP) isn't collected at all; it's on the deferred list. So the premarket explained the morning bid as gold short covering, and the opening update blamed the prior day's curve. The day's real driver was soft core PCE, then a GDP revision that pushed the 10Y to 5.29%. Even a working calendar would only have said "PCE at 8:30", not that it was soft.

RSP has no gap logged yet. It's included because it's cheap and directly tests the concentration claim the headlines keep making.

## Part A — Release actuals (the fix for the MAJOR gap)

1. **A0, BLS calendar test (free, no product change).** One manual workflow run requests the BLS calendar with three User-Agents: the current one, the current one plus a contact email, and a browser-style string. It logs status codes only. Another BLS client traced the same 403 to the firewall rejecting certain User-Agents. If the email version passes, the fix is one line.
2. **A1, a calendar that covers BEA.** Add BEA's release schedule beside BLS's, so PCE and GDP days are known. If either calendar is unavailable, say so; never guess dates.
3. **A2, actuals on release days.** When a run follows a scheduled release from a short fixed list, fetch the headline figures from the agency API and admit them as dated, citable evidence rows:
   - **BLS:** CPI and core CPI, payrolls, unemployment rate, average hourly earnings.
   - **BEA:** PCE and core PCE price index, GDP.
   - Each row carries the actual, the prior as currently published (revisions included), the release time and the source.

**Rules**
- **No consensus on the page.** No public-domain source exists. The page says "core PCE 0.2% m/m (prior 0.1%)", never "soft vs expectations". The journal keeps consensus from Macroglide.
- **Fail closed on stale data.** If the API still returns last month's period after the release time, the row is "not yet published", not last month's number.
- **Timing rule, already in the prompt, now with evidence to use.** The analyst interprets the market's reaction to the release, never the release in isolation. It still can't see rates react intraday: the Treasury curve is prior-day.
- **Budget.** No new model call and no schema change. Rows enter only on release days. The light (opening-structure) context has about 2 KB of headroom, so measure it. If a busy day would cross the floor, cap at headline plus core per release, or raise the light limit (the owner's earlier R4 question).
- **Cadence.** PREMARKET (6:00 AM PT) catches 8:30 ET releases; OPEN_30M catches 10:00 ET ones. FOMC at 2 PM ET lands after both syntheses, so the next premarket carries it. The Fed RSS already collects the statement.

**Not in scope:** ADP, ISM and Conference Board (proprietary), Census retail sales (later), surprise scoring, a calendar product, a news scraper.

## Part B — RSP row

- Add RSP (equal-weight S&P 500 ETF) with SPY as its benchmark. It flows through the same table machinery as XLK vs SPY: daily change and 20-session spread vs SPY. Same Alpaca feed, so no licensing change.
- **Owner decision:** `config/universe.json` mirrors Cuttingboard's registry. Either add RSP to Cuttingboard, or allow a small local extension in Market Brief.
- **Placement:** with SPY and QQQ as a benchmark row, not a new section. No "market internals" block.

## Order and cost

A0 → A1 → A2, with B independent and small. All of it is collection and rendering, verified offline with fixtures and replay. No paid calls are needed to build or test it; the next normal release-day premarket is the live check. API keys: BLS v2 and BEA both need a free registration key stored in GitHub secrets.

## Questions for review

1. Is the release list right, or should anything be added or cut?
2. Should rows show m/m, y/y, or both, for PCE and CPI?
3. For RSP: add it to Cuttingboard's registry, or allow a local extension?
4. If the light budget gets tight on release days: cap the rows, or raise the limit?
