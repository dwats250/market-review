#!/usr/bin/env python3
"""Hermetic tests for scripts/review.py: a fake `claude`, a fixture Market Brief repo and a local
bare remote. No network, no model calls.

    python3 -m unittest scripts/test_review.py -v
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True  # leave no scripts/__pycache__ in the checkout
import review  # noqa: E402

DAY = "2026-10-02"
AFTER_CLOSE = "2026-10-02T16:40:00-07:00"
HANDOFF_SENTENCE = ("The outside control group filled meaningful causal blind spots: same-day macro releases, "
                    "long-end rate behavior, oil, and direct breadth/concentration evidence.")
BRIEF_SENTENCE = "Megacap tech and gold both bid strongly before the open while miners lag the metal badly"
SECTION5 = ("The driver was the payrolls miss, and capital went to megacap tech while the equal-weight index lagged. "
            "Mixed on breadth. What would change the read: RSP beating SPY on an up day.")
SECTION5A = "After the brief: the read holds, but the brief never saw the payrolls report before its premarket page."

FAKE_CLAUDE = r'''#!/usr/bin/env python3
import json, os, sys
d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), "fake")  # env is scrubbed
args = sys.argv[1:]
if args[:1] == ["--version"]:
    print(os.environ.get("FAKE_VERSION", "2.1.292 (Claude Code)")); sys.exit(0)
prompt = sys.stdin.read()
tools = args[args.index("--tools") + 1]
call = "A" if tools else ("B" if "<page role=" in prompt else "C")
with open(os.path.join(d, call + ".prompt.txt"), "w") as f: f.write(prompt)
with open(os.path.join(d, call + ".argv.json"), "w") as f: json.dump(args, f)
with open(os.path.join(d, call + ".env.json"), "w") as f: json.dump(sorted(os.environ), f)
with open(os.path.join(d, call + ".cwd.json"), "w") as f: json.dump(sorted(os.listdir(os.getcwd())), f)
hook = os.path.join(d, call + ".hook.sh")
if os.path.exists(hook): os.system("sh " + hook)
if os.path.exists(os.path.join(d, call + ".fail")):
    print(json.dumps({"type": "result", "subtype": "success", "is_error": True,
                      "result": open(os.path.join(d, call + ".fail")).read()})); sys.exit(1)
out = json.load(open(os.path.join(d, call + ".json")))
init_tools = ["StructuredOutput"] + ([t for t in tools.split(",") if t])
extra = os.path.join(d, call + ".tools.json")
if os.path.exists(extra): init_tools += json.load(open(extra))
ev = [{"type": "system", "subtype": "init", "tools": init_tools, "model": "fake"}]
uses = json.load(open(os.path.join(d, call + ".uses.json"))) if os.path.exists(os.path.join(d, call + ".uses.json")) else []
for i, u in enumerate(uses):
    tid = "t%d" % i
    ev.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": tid, "name": u["name"], "input": u["input"]}]}})
    blk = {"type": "tool_result", "tool_use_id": tid, "content": u["result"]}
    if u.get("is_error"): blk["is_error"] = True
    ev.append({"type": "user", "message": {"content": [blk]}})
text = os.path.join(d, call + ".text.txt")
if os.path.exists(text):
    ev.append({"type": "assistant", "message": {"content": [{"type": "text", "text": open(text).read()}]}})
ev.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "so", "name": "StructuredOutput", "input": out}]}})
ev.append({"type": "result", "subtype": "success", "is_error": False, "num_turns": 3, "total_cost_usd": 0.01,
           "result": json.dumps(out), "structured_output": out})
for e in ev: print(json.dumps(e))
'''


def a_output():
    closes = []
    for cid in review.CLOSE_IDS:
        if cid == "WTI":
            closes.append({"id": cid, "close": "unavailable", "day": "", "source": "EIA", "url": None,
                           "time": "checked 4:45 PM PT", "note": ""})
        elif cid in ("10Y", "30Y", "2s10s"):
            closes.append({"id": cid, "close": "5.28%", "day": "+4 bp", "source": "Treasury par curve",
                           "url": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView",
                           "time": "Oct 2", "note": ""})
        else:
            closes.append({"id": cid, "close": "100.00", "day": "+0.50%", "source": "stockanalysis",
                           "url": f"https://stockanalysis.com/etf/{cid.lower()}/history/", "time": "Oct 2 close",
                           "note": ""})
    return {
        "closes": closes,
        "releases": [{"release": "Nonfarm payrolls, Sep", "et": "8:30", "actual": "+29k", "prior": "+133k",
                      "source": "BLS", "url": "https://www.bls.gov/news.release/empsit.nr0.htm"}],
        "moved": [{"text": "Payrolls missed and tech rallied.",
                   "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/markets/oct-02"}]},
                  {"text": "Yields closed higher anyway.",
                   "sources": [{"name": "Treasury", "url": "https://home.treasury.gov/x"}]}],
        "drivers": [{"driver": "Payrolls miss cuts hike odds", "control_group": "CAPTURED", "note": "TheStreet"},
                    {"driver": "Yields close higher", "control_group": "ABSENT", "note": ""}],
        "control_reached": ["TheStreet"],
        "control_not_reached": ["Reuters"],
        "section5": SECTION5,
    }


def a_uses():
    return [
        {"name": "WebSearch", "input": {"query": "markets oct 2"},
         "result": 'Web search results for query: "markets oct 2"\n\nLinks: [{"title":"x","url":"https://www.thestreet.com/markets/oct-02"}]\n\nSummary.'},
        {"name": "WebFetch", "input": {"url": "https://home.treasury.gov/resource-center/x", "prompt": "p"},
         "result": "10Y 5.28"},
        {"name": "WebFetch", "input": {"url": "https://stockanalysis.com/etf/spy/history/", "prompt": "p"},
         "result": "SPY 769.64"},
        {"name": "WebFetch", "input": {"url": "https://www.bls.gov/news.release/empsit.nr0.htm", "prompt": "p"},
         "result": "payrolls"},
        {"name": "WebFetch", "input": {"url": "https://github.com/dwats250/market-review", "prompt": "p"},
         "result": "WebFetch denied access to domain:github.com.", "is_error": True},
    ]


def b_output():
    page = {"note": "", "headline": "Megacap tech and gold bid", "take": "chip-led", "verdicts": "strengthened",
            "watches": "QQQ holds"}
    return {
        "publications": "Publications: 9 of 9 expected checkpoints published. Missing or late: none",
        "premarket": page, "opening": dict(page, note="the last analysis"),
        "scorecard": [{"watch": "QQQ holds above prior close", "result": "held", "why": "QQQ +1.02%"}],
        "opening_by_close": {"result": "held", "why": "QQQ led SPY."},
        "got_right": "chips as the engine", "didnt_know": "the payrolls miss",
        "coverage": [{"driver": 1, "brief": "ABSENT", "note": "no figures on the page"},
                     {"driver": 2, "brief": "UNIQUE", "note": "page showed it"}],
        "gaps": [{"tag": "macro-release", "major": True, "text": "Payrolls absent from the premarket.",
                  "impaired": "the premarket's explanation", "evidence": "release preceded the page by 32 minutes"},
                 {"tag": "rates-vol", "major": False, "text": "Prior-day curve only.", "impaired": "", "evidence": ""}],
        "section5a": SECTION5A,
        "handoff": "",
    }


def c_output():
    return {"observations": [{"observation": "SPX breadth 68% advancers", "label": "qualifying",
                              "why": "broader than the read implied"}]}


LAB = textwrap.dedent("""\
    # Market Lab — 2026-10-02
    ## CLOSE
    SPX: adv 68.1%, median 0.48%; NDX: adv 63.0%.
    WATCHING 18:31 UTC FJ USO: NYMEX WTI crude futures settle at $89.44 a barrel, up 1 cent
    """)


def sh(args, cwd, env=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise AssertionError(f"{args} failed: {p.stderr}")
    return p.stdout


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="review-test-")
        self.fake = os.path.join(self.tmp, "fake")
        self.bin = os.path.join(self.tmp, "bin")
        os.makedirs(self.fake)
        os.makedirs(self.bin)
        claude = os.path.join(self.bin, "claude")
        with open(claude, "w") as f:
            f.write(FAKE_CLAUDE)
        os.chmod(claude, os.stat(claude).st_mode | stat.S_IEXEC)
        self.put("A", a_output(), a_uses())
        self.put("B", b_output())
        self.put("C", c_output())
        self.make_brief()
        self.make_repo()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def put(self, call, out, uses=None):
        with open(os.path.join(self.fake, call + ".json"), "w") as f:
            json.dump(out, f)
        if uses is not None:
            with open(os.path.join(self.fake, call + ".uses.json"), "w") as f:
                json.dump(uses, f)

    def make_brief(self, checkpoints=None):
        self.brief = os.path.join(self.tmp, "brief")
        os.makedirs(os.path.join(self.brief, "src", "market_brief"))
        os.makedirs(os.path.join(self.brief, "publish"))
        sh(["git", "init", "-q", "-b", "main"], self.brief)
        with open(os.path.join(self.brief, "src", "market_brief", "schedule.py"), "w") as f:
            f.write('CHECKPOINT_KINDS = {"PREMARKET": "synthesis"}\n'
                    'CHECKPOINT_TITLES = {"PREMARKET": "Premarket", "OPEN_30M": "Opening structure", '
                    '"CLOSE_1M": "Close +1M"}\n')
        times = checkpoints or [("PREMARKET", "13:02:35"), ("OPEN_1M", "13:32:07"), ("OPEN_30M", "14:02:23"),
                                ("HOURLY_1100", "15:02:08"), ("CLOSE_1M", "20:02:08")]
        env = dict(os.environ, GIT_AUTHOR_NAME="b", GIT_AUTHOR_EMAIL="b@x", GIT_COMMITTER_NAME="b",
                   GIT_COMMITTER_EMAIL="b@x")
        sh(["git", "add", "."], self.brief)
        env.update(GIT_AUTHOR_DATE="2026-10-01T12:00:00+00:00", GIT_COMMITTER_DATE="2026-10-01T12:00:00+00:00")
        sh(["git", "commit", "-q", "-m", "schedule"], self.brief, env)
        for name, t in times:
            with open(os.path.join(self.brief, "publish", "index.html"), "w") as f:
                f.write(f"<html><head><style>.x{{}}</style><script>var s=1;</script></head><body>"
                        f"<h1>{BRIEF_SENTENCE}</h1><p>Checkpoint {name} at {t}.</p></body></html>")
            sh(["git", "add", "."], self.brief)
            stamp = f"{DAY}T{t}+00:00"
            env.update(GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
            sh(["git", "commit", "-q", "-m", f"Publish {name} brief"], self.brief, env)

    def make_repo(self):
        self.remote = os.path.join(self.tmp, "remote.git")
        self.work = os.path.join(self.tmp, "work")
        sh(["git", "init", "-q", "--bare", "-b", "main", self.remote], self.tmp)
        shutil.copytree(REPO, self.work, ignore=shutil.ignore_patterns(".git", "__pycache__", "shadow"))
        os.makedirs(os.path.join(self.work, "shadow"))
        shutil.copy(os.path.join(REPO, "shadow", "README.md"), os.path.join(self.work, "shadow", "README.md"))
        for p in os.listdir(os.path.join(self.work, "lab")):
            if p.startswith(DAY):
                os.remove(os.path.join(self.work, "lab", p))
        sh(["git", "init", "-q", "-b", "main"], self.work)
        sh(["git", "add", "-A"], self.work)
        sh(["git", "-c", "user.name=t", "-c", "user.email=t@x", "commit", "-q", "-m", "seed"], self.work)
        sh(["git", "remote", "add", "origin", self.remote], self.work)
        sh(["git", "push", "-q", "origin", "main"], self.work)
        sh(["git", "branch", "-q", "--set-upstream-to=origin/main"], self.work)

    def run_review(self, *extra, now=AFTER_CLOSE, date=DAY):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GITHUB_")}
        env.update(PATH=self.bin + os.pathsep + os.environ["PATH"], FAKE_DIR=self.fake,
                   REVIEW_BRIEF_URL=self.brief, CLAUDE_CODE_OAUTH_TOKEN="fake-token",
                   GITHUB_TOKEN="must-not-reach-claude", FAKE_REMOTE=self.remote)
        args = [sys.executable, os.path.join(self.work, "scripts", "review.py"), "--now", now]
        if date:
            args += ["--date", date]
        p = subprocess.run(args + list(extra), cwd=self.work, capture_output=True, text=True, env=env)
        return p.returncode, p.stdout + p.stderr

    def remote_log(self):
        return sh(["git", "--git-dir", self.remote, "log", "--format=%H%x1f%an%x1f%B%x1e", "main"], self.tmp)

    def remote_file(self, rel):
        p = subprocess.run(["git", "--git-dir", self.remote, "show", f"main:{rel}"], capture_output=True, text=True)
        return p.stdout if p.returncode == 0 else None

    def prompt(self, call):
        p = os.path.join(self.fake, call + ".prompt.txt")
        return open(p).read() if os.path.exists(p) else None

    def commit_to_work(self, rel, text, msg):
        path = os.path.join(self.work, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        sh(["git", "add", rel], self.work)
        sh(["git", "-c", "user.name=t", "-c", "user.email=t@x", "commit", "-q", "-m", msg], self.work)
        sh(["git", "push", "-q", "origin", "main"], self.work)


ENTRY = f"shadow/daily/2026/{DAY}.md"


class FullRun(Harness):
    def test_full_run_writes_one_valid_shadow_entry(self):
        before = self.remote_log().count("\x1e")
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        log = self.remote_log()
        self.assertEqual(log.count("\x1e"), before + 1)
        head = log.split("\x1e")[0].split("\x1f")
        self.assertEqual(head[1], "github-actions[bot]")
        self.assertIn(f"Shadow daily {DAY}", head[2])
        self.assertIn("Co-Authored-By: Claude <noreply@anthropic.com>", head[2])
        changed = sh(["git", "--git-dir", self.remote, "diff", "--name-only", "main~1", "main"], self.tmp).split()
        self.assertEqual(changed, [ENTRY])
        entry = self.remote_file(ENTRY)
        secs = review.sections(entry)
        self.assertEqual(secs["5"].strip(), SECTION5)
        self.assertTrue(secs["5a"].strip().startswith(SECTION5A))
        self.assertTrue(review.is_empty(secs["4"]) and review.is_empty(secs["6"]))
        self.assertTrue(review.is_empty(secs["8"]))
        self.assertIn("| WTI | unavailable |", entry)
        self.assertIn("| pending |", entry)
        self.assertIn("`macro-release` · MAJOR · ", entry)
        self.assertIn("[premarket 6:02 AM PT](https://github.com/dwats250/market-brief/blob/", entry)
        self.assertIn("[last: Close +1M 1:02 PM PT]", entry)
        self.assertEqual(review.headings(entry), review.template_headings() + review.SHADOW_EXTRA_HEADINGS)

    def test_evidence_boundaries(self):
        self.commit_to_work(f"lab/{DAY}.md", LAB, "Lab handoff")
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        pa, pb, pc = self.prompt("A"), self.prompt("B"), self.prompt("C")
        self.assertNotIn(BRIEF_SENTENCE, pa)              # A never sees the brief
        self.assertNotIn("SPX: adv 68.1%", pa)            # nor the lab file
        self.assertNotIn("SPX: adv 68.1%", pb)
        self.assertIn("SPX: adv 68.1%", pc)
        self.assertNotIn(BRIEF_SENTENCE, pc)
        self.assertIn("H1 | Long-end Treasury yields", pb)  # B gets the same hypotheses as A
        self.assertNotIn(HANDOFF_SENTENCE[:60], pa)       # nor handoffs
        self.assertIn(BRIEF_SENTENCE, pb)                 # B does
        self.assertNotIn(SECTION5[:60], pb)               # but never A's Section 5
        self.assertNotIn(HANDOFF_SENTENCE[:60], pb)
        self.assertNotIn("var s=1", pb)                   # script and style stripped
        for call in ("A", "B"):
            env = json.load(open(os.path.join(self.fake, call + ".env.json")))
            self.assertNotIn("GITHUB_TOKEN", env)
            self.assertEqual(json.load(open(os.path.join(self.fake, call + ".cwd.json"))), [])
            argv = json.load(open(os.path.join(self.fake, call + ".argv.json")))
            self.assertIn("--restricted", argv)
            self.assertEqual(argv[argv.index("--tools") + 1], "WebSearch,WebFetch" if call == "A" else "")
        self.assertNotIn(SECTION5, out)                   # logs carry no model output
        self.assertNotIn(BRIEF_SENTENCE, out)

    def test_second_run_is_a_no_op(self):
        self.assertEqual(self.run_review()[0], 0)
        sh(["git", "pull", "-q"], self.work)
        before = self.remote_log()
        os.remove(os.path.join(self.fake, "A.prompt.txt"))
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.remote_log(), before)
        self.assertIsNone(self.prompt("A"))

    def test_lab_pass_adds_only_the_lab_section(self):
        self.assertEqual(self.run_review()[0], 0)
        sh(["git", "pull", "-q"], self.work)
        first = self.remote_file(ENTRY)
        self.commit_to_work(f"lab/{DAY}.md", LAB, "Lab handoff")
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertIn("plan=lab", out)
        second = self.remote_file(ENTRY)
        self.assertEqual(review.split_at_lab(first)[0], review.split_at_lab(second)[0])
        self.assertIn("**qualifying**", review.split_at_lab(second)[1])
        self.assertIn(f"Shadow lab {DAY}", self.remote_log().split("\x1e")[0])
        pc = self.prompt("C")
        self.assertIn(SECTION5, pc)
        self.assertNotIn(SECTION5A, pc)
        self.assertNotIn(BRIEF_SENTENCE, pc)
        sh(["git", "pull", "-q"], self.work)
        before = self.remote_log()
        self.assertEqual(self.run_review()[0], 0)
        self.assertEqual(self.remote_log(), before)

    def test_full_run_with_lab_runs_c(self):
        self.commit_to_work(f"lab/{DAY}.md", LAB, "Lab handoff")
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertIn("**qualifying**", self.remote_file(ENTRY))

    def test_push_rejected_then_retried(self):
        hook = (f"cd {self.tmp} && rm -rf other && git clone -q {self.remote} other && cd other && "
                "echo x > notes/race.md && git add notes/race.md && "
                "git -c user.name=o -c user.email=o@x commit -q -m race && git push -q origin main")
        with open(os.path.join(self.fake, "B.hook.sh"), "w") as f:
            f.write(hook)
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertIn("push rejected (attempt 1/3)", out)
        self.assertIsNotNone(self.remote_file(ENTRY))
        self.assertIsNotNone(self.remote_file("notes/race.md"))

    def test_missing_premarket_is_not_published(self):
        shutil.rmtree(self.brief)
        self.make_brief([("OPEN_30M", "14:02:23"), ("CLOSE_1M", "20:02:08")])
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertIn('<page role="PREMARKET">\nnot published', self.prompt("B"))
        entry = self.remote_file(ENTRY)
        self.assertIn("premarket: not published", entry)
        self.assertIn("**Premarket** — not published.", entry)


class MissingOpening(Harness):
    def test_missing_open_30m_is_not_scored(self):
        shutil.rmtree(self.brief)
        self.make_brief([("PREMARKET", "13:02:35"), ("CLOSE_1M", "20:02:08")])
        b = b_output()
        self.put("B", b)
        rc, out = self.run_review()
        self.assertEqual(rc, 1, out)                     # 'held' is invalid when OPEN_30M is missing
        self.assertIn("opening_by_close", out)
        b["opening_by_close"] = {"result": "not published", "why": ""}
        self.put("B", b)
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)
        self.assertIn("Opening headline by the close: not scored (OPEN_30M not published).", self.remote_file(ENTRY))


class FailsClosed(Harness):
    def assert_failed_without_commit(self, *extra, text=None):
        before = self.remote_log()
        rc, out = self.run_review(*extra)
        self.assertEqual(rc, 1, out)
        self.assertIn("FAIL:", out)
        self.assertEqual(self.remote_log(), before)
        if text:
            self.assertIn(text, out)
        return out

    def test_injected_bad_tag(self):
        self.assert_failed_without_commit("--inject", "bad-tag", text="validation: call B failed")

    def test_injected_leak(self):
        self.assert_failed_without_commit("--inject", "leak", text="leak backstop")
        self.assertIsNone(self.prompt("B"))

    def test_inject_on_existing_entry_still_fails(self):
        self.assertEqual(self.run_review()[0], 0)
        sh(["git", "pull", "-q"], self.work)
        self.assert_failed_without_commit("--inject", "bad-tag")

    def test_real_leak_in_search_results(self):
        uses = a_uses() + [{"name": "WebSearch", "input": {"query": "q"},
                            "result": "Links: []\n\n" + HANDOFF_SENTENCE}]
        self.put("A", a_output(), uses)
        self.assert_failed_without_commit(text="handoffs/chatgpt-latest.md")

    def test_brief_text_in_transcript_is_a_leak(self):
        with open(os.path.join(self.fake, "A.text.txt"), "w") as f:
            f.write("I found: " + BRIEF_SENTENCE.upper() + "!")
        self.assert_failed_without_commit(text="brief page")

    def test_text_a_received_is_not_a_leak(self):
        hyp = "Long-end Treasury yields are restrictive (30Y in the mid-5s) and weigh on rate-sensitive equities"
        self.commit_to_work("notes/2026-10-02-chat.md", "Pasted: " + hyp + ".\n", "note")
        with open(os.path.join(self.fake, "A.text.txt"), "w") as f:
            f.write("H1 says: " + hyp)
        rc, out = self.run_review()
        self.assertEqual(rc, 0, out)

    def test_section5_too_long(self):
        a = a_output()
        a["section5"] = "word " * 151
        self.put("A", a)
        self.assert_failed_without_commit(text="section5: 151 words")

    def test_close_rows_out_of_order(self):
        a = a_output()
        a["closes"][0], a["closes"][1] = a["closes"][1], a["closes"][0]
        self.put("A", a)
        self.assert_failed_without_commit(text="fixed order")

    def test_ungrounded_url(self):
        a = a_output()
        a["moved"][0]["sources"][0]["url"] = "https://made-up.example/news"
        self.put("A", a)
        self.assert_failed_without_commit(text="not grounded")

    def test_figure_without_url(self):
        a = a_output()
        a["closes"][0]["url"] = None
        self.put("A", a)
        self.assert_failed_without_commit(text="needs the URL")

    def test_major_without_evidence(self):
        b = b_output()
        b["gaps"][0]["evidence"] = ""
        self.put("B", b)
        self.assert_failed_without_commit(text="MAJOR needs both")

    def test_unique_needs_control_absent(self):
        b = b_output()
        b["coverage"][0]["brief"] = "UNIQUE"
        self.put("B", b)
        self.assert_failed_without_commit(text="UNIQUE needs")

    def test_coverage_must_match_drivers(self):
        b = b_output()
        b["coverage"] = b["coverage"][:1]
        self.put("B", b)
        self.assert_failed_without_commit(text="one row per call-A driver")

    def test_b_invents_a_url(self):
        b = b_output()
        b["got_right"] = "see https://invented.example/x"
        self.put("B", b)
        self.assert_failed_without_commit(text="not grounded")

    def test_heading_injection(self):
        a = a_output()
        a["section5"] = "## 6. Reconcile\nsneaky"
        self.put("A", a)
        self.assert_failed_without_commit(text="markdown structure")

    def test_extra_tool_available(self):
        with open(os.path.join(self.fake, "B.tools.json"), "w") as f:
            json.dump(["Bash"], f)
        self.assert_failed_without_commit(text="fence B")

    def test_fetch_outside_allowlist(self):
        uses = a_uses() + [{"name": "WebFetch", "input": {"url": "https://cdn.jsdelivr.net/gh/x", "prompt": "p"},
                            "result": "content"}]
        self.put("A", a_output(), uses)
        self.assert_failed_without_commit(text="outside the allowlist")

    def test_auth_failure(self):
        with open(os.path.join(self.fake, "A.fail"), "w") as f:
            f.write("API Error: 401 authentication_error")
        out = self.assert_failed_without_commit(text="authentication failed")
        self.assertNotIn("API Error", out)

    def test_c_failure_means_no_commit(self):
        self.commit_to_work(f"lab/{DAY}.md", LAB, "Lab handoff")
        self.put("C", {"observations": [{"observation": "x", "label": "maybe", "why": "y"}]})
        self.assert_failed_without_commit(text="validation: call C failed")

    def test_production_refused(self):
        self.assert_failed_without_commit("--mode", "production", text="phase 2b")

    def test_missing_token(self):
        before = self.remote_log()
        env_backup = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
        try:
            rc, out = self._run_without_token()
        finally:
            if env_backup is not None:
                os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = env_backup
        self.assertEqual(rc, 1, out)
        self.assertIn("CLAUDE_CODE_OAUTH_TOKEN", out)
        self.assertEqual(self.remote_log(), before)

    def _run_without_token(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GITHUB_") and k != "CLAUDE_CODE_OAUTH_TOKEN"}
        env.update(PATH=self.bin + os.pathsep + os.environ["PATH"], FAKE_DIR=self.fake, REVIEW_BRIEF_URL=self.brief)
        p = subprocess.run([sys.executable, os.path.join(self.work, "scripts", "review.py"), "--now", AFTER_CLOSE,
                            "--date", DAY], cwd=self.work, capture_output=True, text=True, env=env)
        return p.returncode, p.stdout + p.stderr


class Calendar(Harness):
    def test_holiday_and_weekend_exit_zero_without_calls(self):
        for d in ("2026-11-26", "2026-10-03"):
            rc, out = self.run_review(date=d, now="2026-11-30T16:40:00-07:00")
            self.assertEqual(rc, 0, out)
            self.assertIn("not an NYSE session", out)
        self.assertIsNone(self.prompt("A"))

    def test_uncovered_year_fails(self):
        rc, out = self.run_review(date="2028-01-03", now="2028-01-03T16:40:00-07:00")
        self.assertEqual(rc, 1, out)
        self.assertIn("2028", out)

    def test_before_the_close_exits_zero(self):
        rc, out = self.run_review(now="2026-10-02T12:00:00-07:00")
        self.assertEqual(rc, 0, out)
        self.assertIn("has not closed", out)

    def test_off(self):
        rc, out = self.run_review("--mode", "off")
        self.assertEqual(rc, 0, out)

    def test_latest_session(self):
        D = review.Date.fromisoformat
        self.assertEqual(review.latest_session(D("2026-10-05")), D("2026-10-05"))
        self.assertEqual(review.latest_session(D("2026-10-04")), D("2026-10-02"))
        self.assertEqual(review.latest_session(D("2026-11-26")), D("2026-11-25"))
        self.assertEqual(review.latest_session(D("2027-01-01")), D("2026-12-31"))
        self.assertIn("early close", review.describe_session(D("2026-11-27")))
        self.assertIn("11:00 AM PT", review.describe_session(D("2026-11-27")))  # EST vs permanent UTC-7


class Units(unittest.TestCase):
    def test_shingles_ignore_punctuation_and_case(self):
        a = review.shingles("The outside control group filled meaningful causal blind spots: same-day macro")
        b = review.shingles("the OUTSIDE control-group... no; the outside control group filled meaningful "
                            "causal blind spots — same-day macro")
        self.assertTrue(a & b)

    def test_schema_errors_name_paths_not_values(self):
        errs = review.schema_errors({"observations": [{"observation": "SECRET", "label": "nope", "why": "x"}]},
                                    review.C_SCHEMA)
        self.assertEqual(errs, ["$.observations[0].label: not an allowed value"])

    def test_page_text_strips_script_and_style(self):
        t = review.page_text("<style>a{}</style><script>x()</script><p>Hello &amp; bye</p>")
        self.assertEqual(t, "Hello & bye")


if __name__ == "__main__":
    unittest.main()
