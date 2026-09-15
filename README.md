# 186 Problems, 186 Videos

Learning every core DSA pattern by teaching it — one problem, one video, every day.

**Python · Neovim · leetcode.nvim · no browser tab in sight.**

---

## Why this repo exists

Two goals, and they reinforce each other:

1. **Learn the patterns well enough to answer them in my sleep.** Teaching a thing
   out loud is the highest-retention way to learn it. You cannot fake an explanation.
2. **Build a YouTube catalogue that proves it.** 186 videos, 15 playlists, one per
   pattern — a public artefact that shows the work rather than claiming it.

## Layout

```
curriculum/
  CURRICULUM.md      the full 186-episode index, grouped by pattern
  curriculum.json    machine-readable source of truth
  progress.csv       per-episode tracker: prep → solved → recorded → uploaded
patterns/            one master card per pattern — READ BEFORE STARTING A PATTERN
prep/                one prep sheet per episode: hook, ELI5, dry run, solution, gotchas
problems/            the solutions themselves, with tests
scripts/dsa          the CLI that drives all of it
PRODUCTION.md        recording format, gear, titles, thumbnails, cadence
TOOLING.md           nvim/tmux learning ladder, what's installed and why
CODING-STANDARDS.md  how to write code people recognise
```

## The daily loop

```bash
dsa next            # what to record today
dsa start           # scaffold + open the tmux workspace
                    #   left: nvim   right: pytest auto-rerunning on save
                    #   window 2: the prep sheet, rendered
dsa test            # run tests manually
dsa done 5 <url>    # mark recorded + uploaded
dsa rep 5           # log a clean re-solve → schedules the next drill
dsa due             # what's due for re-drilling today
dsa stats           # progress dashboard
dsa doctor          # verify the toolchain
```

## Camera + storage

```bash
pocketcam start      # DJI Pocket 2 as a camera, via DJI Mimo -> local RTMP -> Meld
pocketcam status     # is the phone publishing yet?
pocketcam preview    # watch the stream without Meld (browser or ffplay)
./scripts/camcheck   # does this camera get macOS background replacement?

archive status       # disk space on this Mac and on hkt460s
archive push --purge # copy recordings to hkt460s, SHA-256 verify, free local space
```

This Mac has ~19 GB free; `hkt460s` has 377 GB. Record locally, archive after —
never record straight to the network share.

Add to `~/.zshrc`:
```bash
alias dsa='~/Documents/dsa-content/scripts/dsa'
alias pocketcam='~/Documents/dsa-content/scripts/pocketcam'
alias archive='~/Documents/dsa-content/scripts/archive'
```

## The patterns

| # | Pattern | Videos | Master card |
|---|---|---:|---|
| 01 | Two Pointers | 12 | [card](patterns/01-two-pointers.md) |
| 02 | Fast & Slow Pointers | 8 | — |
| 03 | Sliding Window | 12 | — |
| 04 | Kadane | 6 | — |
| 05 | Prefix Sum | 6 | — |
| 06 | Merge Intervals | 7 | — |
| 07 | In-place Reversal of a LinkedList | 6 | — |
| 08 | Stack | 9 | — |
| 09 | Hash Maps | 4 | — |
| 10 | Binary Search | 23 | — |
| 11 | Heap | 17 | — |
| 12 | Recursion & Backtracking | 10 | — |
| 13 | Tree | 31 | — |
| 14 | Graphs | 20 | — |
| 15 | Dynamic Programming | 15 | — |

Full episode list with links: **[curriculum/CURRICULUM.md](curriculum/CURRICULUM.md)**

## How a prep sheet works

Each sheet is what you read **the night before**, never during the take. It carries a
hook, the problem in plain words, a small worked example, an ELI5 analogy, the brute
force to say-but-not-type, the pattern reveal, a dry-run table, the optimal solution
with complexity, the gotchas, and the interview talking points.

In the morning you re-derive it cold on camera. Re-deriving is what makes it stick;
reading is what makes it feel like it stuck.

## Spaced repetition

`dsa rep <ep>` schedules the re-drill on a **1 → 3 → 7 → 16 → 35 → 90 day** ladder.
`dsa due` tells you what's owed. A problem you can rebuild from scratch after 90 days
is one you own.
