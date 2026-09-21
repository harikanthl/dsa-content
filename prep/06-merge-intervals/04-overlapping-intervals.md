# EP048 · P06E04 · Overlapping Intervals — does any pair collide?   [Easy]

**Pattern:** Merge Intervals · **Link:** https://www.geeksforgeeks.org/check-if-any-two-intervals-overlap-among-a-given-set-of-intervals/

---

## 🎬 Hook
> "Given a set of intervals, does *any* pair overlap? It's the smallest question in this
> pattern and it hides the pattern's central claim: after sorting by start, you only
> ever have to compare **neighbours**. Not every pair — the one in front. Today is about
> proving that, because every other episode quietly depends on it."

## 📋 Problem, in your words
```
Given n intervals [start, end], return True if ANY two of them overlap,
False if they are all mutually disjoint.

Convention here: intervals are half-open [start, end). A meeting ending
at 4 and one starting at 4 do NOT overlap. Assume start < end.

Classic phrasing: "can one person attend all these meetings?" -- which
is this function, negated.
```

## 🔢 The example
```
Input:  [[1,3], [7,9], [4,6], [10,13]]
Output: False            <- sorted: [1,3] [4,6] [7,9] [10,13]; all clear

Input:  [[1,3], [2,4], [5,7]]
Output: True             <- [1,3] and [2,4] collide

Input:  [[1,3], [3,5]]
Output: False            <- TOUCHING. Half-open, so no collision.
```
That third case is the convention, stated. Under the closed-interval reading of EP45
the same input would be `True`. Nothing about the code decides this — the problem
statement does, and if it doesn't, you ask.

## 🧸 ELI5
> Sort the intervals by start time and lay them on a timeline in that order:
>
> ```
> [1,3]   ###
> [4,6]        ###
> [7,9]             ###
> [10,13]                ####
>         no interval starts before the previous one has finished -> no collisions
> ```
>
> Now walk left to right and ask one question at each step:
>
> > *"Does this one start before the previous one ended?"*
>
> If the answer is ever yes, you've found a collision and you can stop. If it's always
> no, there isn't one — **anywhere** — and that claim is stronger than it looks.

**Why neighbours are enough** (this is the episode):

> Suppose no adjacent pair overlaps. Take any two intervals `i < j` in sorted order.
> Since interval `i+1` doesn't overlap `i`, it starts at or after `i` ends. Since
> `i+2` doesn't overlap `i+1`, it starts at or after `i+1` ends — which is *later still*.
> Walk that chain up to `j`: its start is at or after `i`'s end. So `i` and `j` don't
> overlap either.
>
> **Sorting turns a claim about all pairs into a claim about neighbours.** That is what
> the sort is really buying, in this episode and in all the others.

## 🐌 Brute force (say it, don't type it)
All `n(n−1)/2` pairs, `a.start < b.end and b.start < a.end`. **O(n²)**, no sort, and for
n = 20 it is genuinely the right code to ship. Say it, then say the sorted version is
O(n log n) and — more importantly — that it *generalises*, which the pairwise version
doesn't.

## 💡 The pattern reveal
**Signal:** intervals · "any overlap" / "attend all meetings" / "conflict".
**Therefore:** sort by start, compare each interval to its predecessor only.

**Key insight:** the general two-interval overlap test is

```
a.start < b.end  and  b.start < a.end       (half-open)
```

Sorted by start, `a.start <= b.start < b.end` makes the first half free, so the test
collapses to `b.start < a.end` — and by the chain argument above, `a` need only be the
immediate predecessor.

**🧨 The trap of the episode: `<` or `<=`?** It is the entire behaviour of this
function on touching intervals, and the two readings are both common:

| intervals | meaning | touching `[1,3] [3,5]` | test |
|---|---|---|---|
| half-open `[s, e)` | meetings, bookings, rooms | **no** overlap | `start < prev_end` |
| closed `[s, e]` | line segments, ranges of integers | **yes**, they share the point 3 | `start <= prev_end` |

This episode uses half-open, matching EP49 and EP50 (and disagreeing with EP45, which
merges touching intervals on purpose). One character, opposite answers, and an
interviewer who hears you name the choice will not ask about it again.

**One more trap: `start < end` is assumed.** A degenerate interval like `[4,4]` has no
duration, and whether it "overlaps" `[1,10]` is undefined rather than hard — ask, or
filter them out and say so.

## 🔍 Dry run — `[[1,3], [7,9], [4,6], [10,13]]` (no collision)
Sorted by start: `[1,3], [4,6], [7,9], [10,13]`.

| i | interval | previous end | `start < prev_end`? | verdict |
|---|---|---|---|---|
| 1 | `[4,6]` | 3 | 4 < 3 ✗ | clear |
| 2 | `[7,9]` | 6 | 7 < 6 ✗ | clear |
| 3 | `[10,13]` | 9 | 10 < 9 ✗ | clear |

Answer **False** ✓ — and note the sort is doing real work: in the input order, `[7,9]`
is followed by `[4,6]`, which *looks* like a collision until you sort.

## 🔍 Dry run — `[[1,3], [2,4], [5,7]]` (collision)
Already sorted.

| i | interval | previous end | `start < prev_end`? | verdict |
|---|---|---|---|---|
| 1 | `[2,4]` | 3 | **2 < 3 ✓** | **overlap → return True immediately** |

Answer **True** ✓ — return on the first hit; there's nothing to gain by finishing the
walk.

## ✅ Optimal solution
```python
class Solution:
    def anyOverlap(self, intervals: List[List[int]]) -> bool:
        """True if any two intervals overlap. Half-open [start, end): touching is fine.

        Time:  O(n log n) — the sort; the scan is O(n).
        Space: O(1) beyond the sort.
        """
        intervals.sort(key=lambda iv: iv[0])

        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:   # starts before the last ends
                return True                             # one is enough

        return False
```
**Time:** O(n log n) · **Space:** O(1)

> **"Can this person attend all meetings?"** is `not anyOverlap(intervals)` — the same
> function with the answer flipped. Say that when the interviewer phrases it that way,
> rather than writing a second function.

## ⚠️ Gotchas
- **Compare against the previous interval's END, not its start.** `intervals[i-1][1]`.
  Comparing starts is always false after sorting and returns `False` on everything.
- **`<` here, `<=` in EP45.** Half-open vs closed. Name the convention before you write
  the character.
- **Return early.** The first collision is the answer; a `found = True` flag that keeps
  looping is a code smell the interviewer will notice.
- **Zero or one interval** → the loop body never runs → `False` ✓. No guard needed.
- **Sorting mutates the caller's list.** `sorted(intervals)` instead of
  `intervals.sort()` if that matters — a real-code concern, not a LeetCode one.
- **Don't reach for a heap.** That's EP49, and it answers *how many* overlap. Here the
  answer is a yes/no and a heap is over-engineering.

## 🎤 Interview talking points
- *"Sort by start, then only adjacent pairs can be the first collision — if no
  neighbouring pair overlaps, the ends are increasing, so no pair does."* ← the proof in
  one sentence, and the reason this episode exists.
- *"I'm assuming half-open intervals, so a meeting ending at 4 and one starting at 4
  don't conflict. If they're closed, it's `<=`."*
- *"O(n log n), all of it the sort. Below ~20 intervals I'd just check all pairs and
  skip the sort."* ← knowing when the simple thing wins is a senior signal.
- *"'Attend all meetings' is this, negated."*

## 🔗 Transfer
This is the yes/no version. Tomorrow (EP49) asks the quantitative one — *how many
overlap at the same time?* — and one sorted sweep no longer suffices, because you have
to remember **all** the intervals still running, not just the last one. That's what the
heap is for, and the next two episodes are both built on it.

## 📹 Metadata
- **Title:** `Do any intervals overlap? — why neighbours are enough | Merge Intervals #4`
- **Thumbnail:** `CHECK NEIGHBOURS ONLY` (green block)
- **Short:** the chain argument on the timeline, in one take. 40s.
