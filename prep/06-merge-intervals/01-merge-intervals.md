# EP045 · P06E01 · Merge Intervals   [Medium]

**Pattern:** Merge Intervals · **Link:** https://leetcode.com/problems/merge-intervals/

---

## 🎬 Hook
> "Merge every pair of overlapping intervals. Unsorted, any interval can overlap any
> other and you're comparing all n² pairs. Sort them by start time and something
> wonderful happens: each interval can only ever overlap **the one you're currently
> holding**. Sorting doesn't speed the algorithm up, sorting *is* the algorithm."

## 📋 Problem, in your words
```
Given an array of intervals [start, end], merge all overlapping
intervals and return the non-overlapping intervals that cover exactly
the same ground.

The input is NOT sorted. Intervals are closed: [1,4] and [4,5] touch,
and touching counts as overlapping here.
```

## 🔢 The example
```
Input:  [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]
Why:    [1,3] and [2,6] overlap (2 <= 3), so they become [1,6].

Input:  [[1,4], [4,5]]
Output: [[1,5]]          <- TOUCHING counts. Closed intervals.

Input:  [[1,4], [2,3]]
Output: [[1,4]]          <- the trap. [2,3] is INSIDE [1,4]; the answer must not shrink.
```
That third case is the whole episode. Get it wrong and you output `[1,3]`.

## 🧸 ELI5
> Think of them as strips of tape on a timeline, and you're pressing them flat into as
> few strips as possible.
>
> Unsorted, it's chaos, any strip might touch any other:
>
> ```
> [1,3]      ---
> [8,10]              ---
> [2,6]       -----
> [15,18]                    ---
> ```
>
> Sort by where each strip *starts*, and walk left to right holding one strip:
>
> ```
> [1,3]   ---
> [2,6]    -----        starts at 2, and I'm holding up to 3  -> overlaps, absorb it
> [8,10]          ---   starts at 8, I'm holding up to 6      -> gap! put mine down
> [15,18]                ---
> ```
>
> You're never comparing with anything except the strip in your hand. Everything to the
> left is finished, it started earlier *and* whatever it covered has already been
> pressed into what you're holding.

## 🐌 Brute force (say it, don't type it)
Repeatedly scan all pairs, merge any two that overlap, restart, until a full pass makes
no change. **O(n²)** per pass and awkward to get right (merging changes the list you're
iterating). Worth 20 seconds, mostly to motivate the sort.

## 💡 The pattern reveal
**Signal:** a list of `[start, end]` pairs · "merge" / "overlapping".
**Therefore:** sort by start, sweep once, hold one interval.

**Key insight:** two intervals overlap iff `a.start <= b.end and b.start <= a.end`,
**two** comparisons. Once sorted by start, `a.start <= b.start <= b.end` is automatic,
so the first comparison is always true and only one remains:

```
b.start <= a.end
```

That collapse from two tests to one is what sorting buys, and it's why nothing further
back than the interval in your hand can ever matter.

**🧨 The trap of the episode: `max(prev_end, end)`.** Sorting by start does **not**
sort by end. When you absorb an interval you must keep the *further* end:

```python
out[-1][1] = max(out[-1][1], end)     # correct
out[-1][1] = end                      # WRONG: [[1,4],[2,3]] -> [[1,3]]
```

`[1,4]` then `[2,3]` is the two-interval input that catches it. Every staircase-shaped
example passes with the buggy line, which is exactly why this bug survives to
submission.

## 🔍 Dry run: `[[1,3], [2,6], [8,10], [15,18]]`
After sorting by start (already in order here): `[1,3], [2,6], [8,10], [15,18]`.

| interval | `out[-1]` in hand | `start <= end_in_hand`? | action | `out` after |
|---|---|---|---|---|
| `[1,3]` | - | - | nothing held: take it | `[[1,3]]` |
| `[2,6]` | `[1,3]` | 2 ≤ 3 ✓ | absorb: end = max(3, 6) = **6** | `[[1,6]]` |
| `[8,10]` | `[1,6]` | 8 ≤ 6 ✗ | **gap** → put it down, pick up the new one | `[[1,6], [8,10]]` |
| `[15,18]` | `[8,10]` | 15 ≤ 10 ✗ | gap → new one | `[[1,6], [8,10], [15,18]]` |

Answer **`[[1,6], [8,10], [15,18]]`** ✓

## 🔍 Dry run: `[[1,4], [2,3]]` (the containment trap)

| interval | in hand | overlap? | with `max` | with plain `end` |
|---|---|---|---|---|
| `[1,4]` | - | - | `[[1,4]]` | `[[1,4]]` |
| `[2,3]` | `[1,4]` | 2 ≤ 4 ✓ | end = max(4, **3**) = **4** → `[[1,4]]` ✓ | end = 3 → `[[1,3]]` ✗ |

Two intervals, four numbers, and the whole difference is one `max`. Type the wrong
version on camera first and let the output say `[[1,3]]`.

## ✅ Optimal solution
```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """Merge all overlapping intervals.

        Time:  O(n log n), the sort; the sweep is O(n).
        Space: O(n), the output (O(1) beyond it, if sorting in place counts as free).
        """
        intervals.sort(key=lambda iv: iv[0])     # sorting IS the algorithm

        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1]:      # `<=`: touching counts
                merged[-1][1] = max(merged[-1][1], end)   # MAX -- the contained case
            else:
                merged.append([start, end])            # a real gap

        return merged
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **`max(merged[-1][1], end)`.** Say it out loud every time you write this loop.
  `[[1,4],[2,3]]` is the two-line test.
- **`<=` vs `<`.** Here `[1,4]` and `[4,5]` merge, so `<=`. In EP49's meeting rooms they
  *don't* conflict. Same pattern, opposite character, ask which convention applies
  before writing it.
- **Sort by start only.** `key=lambda iv: iv[0]` is enough; sorting by `(start, end)`
  is harmless but unnecessary, and sorting by end is a different algorithm (that's the
  greedy for "erase overlap intervals", not this).
- **Don't mutate the input intervals and reuse them.** `merged.append([start, end])`
  appends a *new* list. Appending the original row and then editing it in place works
  here, but it silently corrupts the caller's data, a real code-review comment.
- **Empty input** returns `[]`; the `if merged` guard handles it with no special case.
- **The output is sorted and non-touching** by construction. Worth stating, several
  follow-up questions (EP51's free time) depend on it.

## 🎤 Interview talking points
- *"Sorting by start means each interval can only overlap the one I'm currently holding,
  so one pass suffices."* ← the sentence the question is asking for.
- *"Overlap is normally two comparisons; sorted by start, one of them is free."*
- *"I take the max of the ends because sorting by start doesn't sort by end, one
  interval can contain another."* ← volunteer this; it's the follow-up.
- *"O(n log n), dominated entirely by the sort. If the input arrived sorted it'd be
  O(n)."* ← and that is literally tomorrow's problem.

## 🔗 Transfer
Every other episode in Pattern 06 is this sweep with one thing changed. Tomorrow (EP46)
hands you the list **already sorted and disjoint**, so the sort disappears and the sweep
becomes three explicit phases, and EP51 will take the *gaps* this loop skips over and
call them the answer.

## 📹 Metadata
- **Title:** `Merge Intervals, sorting IS the algorithm | Merge Intervals #1`
- **Thumbnail:** `SORT BY START` (green block)
- **Short:** `[[1,4],[2,3]]` returning `[[1,3]]` without the `max`, then the fix. 40s.
