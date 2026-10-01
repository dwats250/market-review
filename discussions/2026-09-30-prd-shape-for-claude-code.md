# How to write a PRD for Claude Code (Opus 5.5)

For ChatGPT, when drafting work for Claude Code on Market Brief. Written by Claude, 2026-09-30. Context, not authority. The worked examples are `docs/2026-09-25-rates-reading-pass.md` in market-brief and `prd-scheduler-liveness-2026-09-30` (handed to Claude Code with this note).

## What the model does well, and what that means for the PRD

Claude Code reads the repo, runs tests and keeps a plan across a long session. It follows **intent and reasons** better than lists of prohibitions. When a rule comes with its "why", it applies the rule correctly to cases the PRD never named. When a rule comes without one, it follows the letter and misses the edges. So the PRD's job is to set the goal, the facts, the boundaries and the proof, then leave the implementation to the agent that can see the code.

## The shape

1. **Header:** status (who approved what, and any stop gate), base commit, branch, where to save the file, and what's out of scope.
2. **§0 How to work:** read these files first; plan in Progress; tests first for new behavior; local commits only; no paid calls; when to stop and ask. One line on what to do if the code disagrees with the PRD ("record it in Progress, follow the intent").
3. **§1 Why:** the observed problem with evidence (dates, commits, numbers), the goal in one or two sentences, and the editorial or product principle at stake. This section does the most work.
4. **§2 Verified facts:** what is true in the code or production today, each item checked at a named commit. Kept separate from requirements so the agent can re-verify and correct them. Mark anything unverified as inferred.
5. **§3 Requirements:** numbered IDs (R1, R2, … or P1–P6 for investigations). Each says the behavior, the constraint and the reason. Describe behavior, not code. Name files only when the choice matters.
6. **§4 Invariants and non-goals:** what must not change, and ideas considered and deferred. One list each, stated once.
7. **§5 Acceptance:** testable checks, one per behavior, including the edge cases you care about.
8. **§6 Verification:** the exact commands (pytest, ruff, `git diff --check`), fixtures to render, screenshots to look at, measurements to report.
9. **§7 Report:** the exact list the reply must contain: changes by requirement ID, tests added, assertions changed and why, discrepancies found, deferred ideas, owner decisions.
10. **Progress:** an empty section the agent maintains. It is how the work survives a context reset.

## Do

- **Explain each constraint once, with its reason.** "No `cancel-in-progress: true`: a newer wake would cancel an in-flight synthesis or continuity upload."
- **Separate investigation from implementation** when the cause is unknown. Phase 1 is read-only and ends in a report and a stop; Phase 2 starts after the owner reviews it.
- **Ask for evidence labels** (observed / inferred) and allow "root cause not observable" as a legitimate answer.
- **Give numbers and examples:** real values from a real day, the exact strings that should render, the worked case that must pass (for example, "Sep 24 → Bear steepener").
- **Tie thresholds to existing semantics** in the code rather than inventing new clocks or constants.
- **Keep one PRD per change.** Bundled concerns get bundled compromises.
- **State cost and safety limits plainly:** paid calls, pushes, deploys, dispatches.

## Avoid

- **Walls of "Do NOT".** A few hard boundaries are right; dozens of capitalized prohibitions read as anxiety, crowd out intent, and get applied too broadly. Put each in §4 once, with its reason.
- **Prescribing the implementation** ("add function X to file Y") when the agent can read the code and you can't. Prescribe the behavior and the constraint.
- **Repeating rules in several sections.** Repetition makes the model weigh them as extra-important and creates contradictions when one copy is edited.
- **Role-play openers** ("You are a world-class engineer…"). They add nothing; the context does that work.
- **Vague verbs** like "consider", "maybe" or "handle appropriately". Decide, or list it as an owner decision with a default.
- **Hidden scope:** "while you're there…". Anything not listed goes to "Deferred ideas" in the report, not into the diff.
- **Asking for certainty the evidence can't give,** which invites a confident guess.

## Size

Long is fine when it's structured; the rates PRD was long and worked. What hurts is noise: duplicated rules, motivational filler, unexplained bans. If a sentence wouldn't change what the agent does, cut it.
