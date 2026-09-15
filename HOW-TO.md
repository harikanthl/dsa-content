# HOW-TO — read this first

Orientation for anyone (me, or a future Claude session) picking this project up cold.

---

## What this is

Harikanth is learning every core DSA pattern by **teaching each problem on camera**.
186 problems, 186 videos, 15 patterns, one YouTube playlist per pattern.

Two goals at once, and they reinforce each other: learn the patterns well enough to
answer them cold in an interview, and build a public catalogue that proves it. He's
38, MS in EE, five years out of work — so **public, dated, visible evidence of skill**
is the thing that matters most. Bias every decision toward producing that.

## Decisions already made — don't relitigate these

| Decision | Value | Why |
|---|---|---|
| Language | **Python** | Fastest to type on camera, standard for interviews |
| Camera | **Logitech Brio 300** | Decided 2026-09-14. DJI Pocket 2 path works but is parked for the trailer only |
| Recording | **Meld Studio**, 1080p30, two scenes (`TALK` / `CODE`) | Mac-native, GPU-accelerated |
| Editor | **nvim** (kickstart, `vim.pack`) + `leetcode.nvim` | Solving in-terminal is the channel's visual identity |
| Video format | Locked, 10 beats — see `PRODUCTION.md` §1 | Consistency is what makes it a series |
| Episode order | Sheet order (global `ep` 1–186) | Already well sequenced |
| Storage | Record to `~/Movies/dsa`, archive to `hkt460s` | Mac has only ~19 GB free |
| Repo | `github.com/harikanthl/dsa-content` — **private** as of 2026-09-14 | He may flip it public |

## Where everything lives

```
curriculum/CURRICULUM.md   the 186-episode index, grouped by pattern
curriculum/curriculum.json SOURCE OF TRUTH — ep numbers, slugs, links, prep paths
curriculum/progress.csv    per-episode state: prep_ready, recorded, uploaded, reps
patterns/NN-<name>.md      pattern master card — the deep explainer
prep/NN-<pattern>/NN-*.md  one prep sheet per episode
problems/                  solutions + pytest cases
scripts/dsa                the CLI
scripts/pocketcam          DJI Pocket 2 RTMP path (parked, still works)
scripts/archive            rsync recordings to hkt460s with SHA-256 verification
tools/camcheck.swift       does this webcam get macOS background replacement?
PRODUCTION.md              format, gear, titles, thumbnails, cadence
TOOLING.md                 nvim/tmux learning ladder
CODING-STANDARDS.md        how to write code people recognise
```

`scripts/build_index.py` regenerates `CURRICULUM.md` and **merges** `progress.csv`
from the JSON. **Edit the JSON, then rerun it** — never hand-edit `CURRICULUM.md`.
The merge preserves per-episode state (recorded, reps, URLs) and is idempotent, so
it's safe to run any time.

## Progress

Track it honestly, here, at the end of every session.

| Pattern | Card | Prep sheets | Episodes |
|---|---|---|---|
| 01 Two Pointers | ✅ | ✅ 12/12 | 1–12 |
| 02 Fast & Slow pointers | ✅ | ◐ **2/8** (13–14 done; 15–20 to write) | 13–20 |
| 03 Sliding Window | ☐ | ☐ 0/12 | 21–32 |
| 04 Kadane | ☐ | ☐ 0/6 | 33–38 |
| 05 Prefix Sum | ☐ | ☐ 0/6 | 39–44 |
| 06 Merge Intervals | ☐ | ☐ 0/7 | 45–51 |
| 07 In-place Reversal of a LinkedList | ☐ | ☐ 0/6 | 52–57 |
| 08 Stack | ☐ | ☐ 0/9 | 58–66 |
| 09 Hash Maps | ☐ | ☐ 0/4 | 67–70 |
| 10 Binary Search | ☐ | ☐ 0/23 | 71–93 |
| 11 Heap | ☐ | ☐ 0/17 | 94–110 |
| 12 Recursion & Backtracking | ☐ | ☐ 0/10 | 111–120 |
| 13 Tree | ☐ | ☐ 0/31 | 121–151 |
| 14 Graphs | ☐ | ☐ 0/20 | 152–171 |
| 15 DP | ☐ | ☐ 0/15 | 172–186 |

**Next up: finish Pattern 02 (EP 15–20), then Pattern 03 Sliding Window (EP 21–32).**

Paused on prep sheets 2026-09-14 — 14 sheets is enough runway to start
recording. Resume when the backlog gets thin.

## How to write a prep sheet

This is the part that matters. The bar is set by `prep/01-two-pointers/*.md` — read
EP001 and EP009 before writing new ones, and match them.

**Structure** (also in `templates/PREP-TEMPLATE.md`):

1. `🎬 Hook` — one sentence, the *insight*, not the problem. Must make a scroller stop.
2. `📋 Problem, in your words` — 3–5 plain lines. This is what he types on screen.
3. `🔢 The example` — tiny, 5–7 elements, fits one screen line.
4. `🧸 ELI5` — a real-world analogy that survives being told to a 10-year-old.
5. `🐌 Brute force` — state it, say *why* it's wasteful. Explicitly "don't type this."
6. `💡 The pattern reveal` — the **signal** in the problem, then the key insight.
7. `🔍 Dry run` — a markdown table, stepping the actual example. Non-negotiable.
8. `✅ Optimal solution` — commented Python, then Time/Space with *reasoning*.
9. `⚠️ Gotchas` — the real bugs, especially off-by-ones. Be specific.
10. `🎤 Interview talking points` — sentences he can literally say out loud.
11. `🔗 Transfer` — what this unlocks; name the future episode number.
12. `📹 Metadata` — title, thumbnail text, which beat makes the Short.

**Quality rules learned so far:**

- **Name the trap.** Every Medium has one line everyone gets wrong (the `mid` pointer
  in Dutch National Flag; `hi-lo` vs `hi-lo+1`). Find it and build the episode on it.
- **Contrast sibling problems.** EP7 uses `hi - lo`, EP8 uses `hi - lo + 1`. Putting
  them side by side teaches more than either alone.
- **Be honest about the brute force.** If `sorted()` passes on LeetCode, *say so*,
  then say why the interviewer still wants the O(n) version.
- **Give the correctness argument**, not just the code — the "why can I discard `lo`?"
  paragraph is what separates a hire from a no-hire, and he should be able to say it.
- **Close each pattern** with a recap-video note in the last episode's Transfer section.
- Prefer one general solution that subsumes the variants (the `k`-copies Remove
  Duplicates, the recursive `kSum`) — that reveal is the moment a viewer subscribes.

After writing a batch, mark `prep_ready=Y` for those episodes in `progress.csv` and
update the table above.

## Commands

```bash
dsa next / start / test / prep / done / rep / due / stats / doctor
archive status | push [--purge] | pull <file>
pocketcam start | stop | status | preview [browser|ff]     # parked
python3 scripts/build_index.py                              # after editing the JSON
```

## Tone

He asked for ELI5 and he means it. Write like you're explaining to a smart friend who
is tired. Short sentences. Concrete analogies. No hedging, no "simply", no cheerleading.
Say the hard part is hard, then make it easy.
