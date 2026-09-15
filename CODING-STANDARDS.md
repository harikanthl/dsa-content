# Coding Standards — how to write code people recognise

You said you want people to recognise your work and ability. That doesn't come from
solving hard problems; plenty of people solve hard problems. It comes from your code
being *obviously* clear to someone reading it in thirty seconds.

These are the habits. They're small, and they compound over 186 repetitions.

---

## 1. Name things for the reader, not the writer

```python
# no
for i in range(len(a)):
    if a[i] == 0: c += 1

# yes
for index, value in enumerate(nums):
    if value == 0:
        zero_count += 1
```

Exception, and it's a real one: in a two-pointer or binary-search loop, `lo` / `hi` /
`mid` are **more** readable than `left_boundary` / `right_boundary`, because they're
the field's standard vocabulary. Conventional short names beat invented long ones.
The rule is "use the name a reader expects," not "use long names."

## 2. State the complexity in the code, every time

```python
def three_sum(nums: List[int]) -> List[List[int]]:
    """Find all unique triplets summing to zero.

    Time:  O(n^2) — n anchors, each with an O(n) two-pointer scan.
    Space: O(1) beyond the output (O(log n) for the sort's stack).
    """
```

Two reasons. One: interviewers ask, and having it written means you've thought about
it rather than guessed. Two: writing *why* — "n anchors × O(n) scan" — is what catches
you when you're wrong.

## 3. Type-hint everything

```python
def two_sum(numbers: List[int], target: int) -> List[int]:
```

It's free documentation, it makes your LSP useful, and it's standard in every Python
codebase you'd be hired into. Your kickstart config already has pyright wired up, so
you get red squiggles for free the moment you're inconsistent.

## 4. Tests before solution — always

Every scaffold from `dsa start` puts `CASES` **above** the solution. Fill it in from
the LeetCode examples *before* you write a line of logic.

```python
CASES = [
    (([2, 7, 11, 15], 9), [1, 2]),
    (([2, 3, 4], 6),      [1, 3]),
    (([-1, 0], -1),       [1, 2]),
]
```

This is not ceremony. It forces you to state the contract precisely, and it's the
only reliable way to find off-by-ones before the grader does. It also makes great
video: viewers see you define "correct" before chasing it.

`entr` reruns them on every save in the right-hand tmux pane. You get a green/red
signal without ever leaving nvim.

## 5. Handle the edge cases explicitly, at the top

```python
def find_unsorted(nums: List[int]) -> int:
    if len(nums) < 2:
        return 0
    ...
```

Guard clauses at the top, then the main logic unindented below. Never bury the real
algorithm inside three levels of `if`. The five edges that bite in DSA, in order of
frequency: **empty input · single element · all identical · already sorted ·
target absent**.

## 6. One idea per line, one responsibility per function

If a line needs a comment explaining *what* it does, split it. Comments should explain
**why**, never what.

```python
# no — comment explains what
count += hi - lo  # add hi minus lo to count

# yes — comment explains why
count += hi - lo  # every index between lo and hi also satisfies the bound
```

## 7. Commit like someone will read it (because they will)

Your GitHub is a public artefact. A recruiter who opens this repo and sees 186
commits reading `update` learns nothing. One reading
`two-pointers: 3Sum with duplicate-skip on all three indices` tells them you think
clearly.

Format:
```
<pattern>: <problem> — <the one-line insight>

Time O(n^2), Space O(1). Skips duplicate anchors on i, and duplicate
values on lo/hi after recording a hit.
```

Commit **once per problem**, when it passes. A green commit history with one
meaningful commit a day, for six months, is a genuinely strong signal on its own —
it reads as discipline, which is the thing five years out of work most needs to
demonstrate.

## 8. Write the brute force in a comment, not in code

Every scaffold has this:
```python
# --- brute force (say it out loud, then discard) ---
# O(n^2): check every pair.
# Wasteful because sortedness already tells us the direction to move.
```

In an interview you must *state* the brute force before optimising — it proves you
understand the problem before you optimise it, and it buys thinking time. Writing it
down as a comment builds that reflex.

## 9. The three-pass rule for every problem

1. **Pass 1 — solve it.** Any working solution. Ugly is fine.
2. **Pass 2 — clean it.** Rename, extract, add hints, add the docstring.
3. **Pass 3 — explain it.** Say it out loud as if to a person. *If you can't, you
   haven't understood it.* This is the pass most people skip, and it's the one the
   videos force you to do — which is exactly why making them will teach you faster
   than solving twice as many problems silently.

## 10. Re-solve from scratch, not from memory

Rereading a solution feels like learning and isn't. The only thing that transfers is
producing it cold.

```bash
dsa due     # what's due for a re-drill today
dsa rep 5   # log a clean re-solve; schedules the next one
```

The ladder is **1 → 3 → 7 → 16 → 35 → 90 days**. A problem you can rebuild from
scratch after 90 days is one you actually own. That's what "answer them in my sleep"
means, mechanically.

---

## The Python subset to know cold

You will reach for these constantly. Know them without looking:

```python
from collections import Counter, defaultdict, deque
import heapq
from functools import lru_cache
import bisect

Counter(s)                       # frequency map in one line
defaultdict(list)                # no KeyError on first append
deque()                          # O(1) popleft — BFS queue, sliding window
heapq.heappush / heappop         # MIN-heap; push -x for a max-heap
heapq.nlargest(k, iterable)
bisect.bisect_left(arr, x)       # binary search without writing binary search
@lru_cache(maxsize=None)         # memoisation for free (DP pattern)
nums.sort(key=lambda p: p[1])    # sort by a field
float('inf'), float('-inf')      # sentinel initial values
a, b = b, a                      # swap, no temp
```

`heapq` is a **min**-heap only. For a max-heap you push negatives and negate on the
way out. You will use this constantly in Pattern 11 (EP 97–113) — burn it in now.

---

## Repo hygiene

```
problems/   your solutions, mirrored by pattern folder
prep/       the video prep sheets
patterns/   the pattern master cards — read these before starting a pattern
curriculum/ CURRICULUM.md (the index), progress.csv (the tracker)
scripts/    the dsa CLI
```

One file per problem. Never edit a solved file to solve a different problem — the
history *is* the portfolio.
