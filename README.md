# Market Review

A daily and weekly record of what the market did, what Market Brief said about it, and what we each made of it. It exists to learn the market and to find out, with evidence, what the brief misses.

## Layout

```text
daily/2026/2026-09-30.md       one file per trading day
weekly/2026/2026-W40.md        one file per ISO week
notes/                         Dustin's drop zone: pasted ChatGPT chats, week-in-review, anything
discussions/                   product discussions (ideas, not decisions)
hypotheses.md                  living regime hypotheses
gaps.md                        what the brief missed, tallied by tag
templates/                     daily.md, weekly.md
ROUTINE.md                     exactly what Claude's scheduled runs do
```

## Who writes what

- **Claude, weekdays ~4:40 PM PT:** today's entry (the brief's calls, the close, a scorecard, an independent read, gaps). It first reconciles the previous entry if Dustin added notes, and backfills consensus figures from the morning's Macroglide recap.
- **Claude, Saturday ~8:45 AM PT:** the weekly review and updates to `hypotheses.md` and `gaps.md`.
- **Dustin, any time:** write in section 4 of a daily file, or drop a file in `notes/` named `YYYY-MM-DD-topic.md`. Pasting into the Market Brief Claude Project and asking Claude to file it works too.
- **On demand:** "reconcile today" (or "this week") in the Project chat.

## Rules

1. **Context, not authority.** Nothing here overrides Market Brief's `CLAUDE.md`, `PROJECT_STATE.md`, `DECISIONS.md` or a current owner instruction. Product work starts only from an explicit owner ruling.
2. **Independence.** Claude writes its read from sources before reading Dustin's or ChatGPT's notes. Disagreement is the point.
3. **Sources.** Official data first (Treasury, BLS, BEA, Census, Fed, Cboe, issuers). News only to explain why, paraphrased and linked, never pasted.
4. **Clocks.** Every figure carries its observation time or date. The Treasury par curve and index closes are end-of-day values.
5. **Macroglide stays here.** Its figures come from a personal subscription: numbers only, credited, and never copied into the Market Brief page.
6. **Small.** A daily entry fits on about two phone screens. No numeric scoring until 20 sessions exist.

## From gap to candidate

This section is the canonical candidate rule; `ROUTINE.md`, `gaps.md` and the templates point here.

A gap becomes a **candidate** when either:

1. the same tag appears on **3+ trading days in the last two weeks** (10 trading days); or
2. one occurrence is marked **MAJOR** because the missing information materially changed, constrained, or could have reversed that day's market interpretation.

A MAJOR mark:

- is never earned by the event's name alone. CPI, FOMC, payrolls and the like are not automatically MAJOR;
- must state, in the same gap line, **Impaired:** the interpretation that was affected, and **Evidence:** what shows it mattered (prices, timing, the brief's own words);
- without both, it is an ordinary gap and counts only toward rule 1;
- can be added or removed by Dustin, or by a later reconcile when new evidence arrives.

A candidate is for owner review only. It does not authorize product work: gap → candidate → owner ruling → Market Brief PRD → implementation. No numeric scoring, no priority ranking. Context, not authority.
