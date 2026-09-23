# EP046 · P06E02 · Insert Interval   [Medium]

**Pattern:** Merge Intervals · **Link:** https://leetcode.com/problems/insert-interval/

---

## 🎬 Hook
> "Insert one interval into a list that's already sorted and already disjoint. The lazy
> answer is 'append it and run yesterday's merge', correct, and O(n log n) for a
> problem that is O(n). The input being sorted is a gift, and the whole episode is about
> not throwing it away."

## 📋 Problem, in your words
```
Given a list of NON-OVERLAPPING intervals sorted by start time, and one
new interval, insert the new interval so the list stays sorted and
non-overlapping -- merging where necessary.

You may assume the input list has both properties. The new interval
may overlap zero, some, or all of them.
```

## 🔢 The example
```
Input:  intervals = [[1,3], [6,9]], new = [2,5]
Output: [[1,5], [6,9]]
Why:    [2,5] overlaps [1,3] -> merged to [1,5]. It does not reach [6,9].

Input:  intervals = [[1,2], [3,5], [6,7], [8,10], [12,16]], new = [4,8]
Output: [[1,2], [3,10], [12,16]]
Why:    [4,8] swallows [3,5], [6,7] and [8,10] -- THREE intervals become one.

Input:  intervals = [], new = [5,7]      -> [[5,7]]
Input:  intervals = [[1,5]], new = [2,3] -> [[1,5]]     <- contained; nothing changes
```

## 🧸 ELI5
> The intervals are already laid out left to right with gaps between them. You're
> dropping one new strip of tape onto the timeline. Walk left to right and everything
> you meet falls into exactly **three** groups:
>
> ```
> intervals:  [1,2]   [3,5]  [6,7]  [8,10]      [12,16]
> new:                   [4=========8]
>             |____|  |________________|        |______|
>              BEFORE        ABSORB              AFTER
>             untouched   merge into one        untouched
> ```
>
> 1. **Before**: ends before the new one starts. Copy them across, unchanged.
> 2. **Absorb**: starts before (or when) the new one ends. Swallow it: stretch the new
>    interval to cover it.
> 3. **After**: everything left. Copy across, unchanged.
>
> Three `while` loops, in that order, and you're done. No sorting, the list was already
> sorted, and the answer stays sorted because you never reorder anything.

## 🐌 Brute force (say it, don't type it)
`intervals.append(new)`, then EP45's sort-and-merge. **O(n log n)**, three lines, and
completely correct, say it, *then* say why you won't: the input's sortedness is already
paid for, and re-sorting throws it away. An interviewer asking this question rather than
EP45 is asking exactly this.

## 💡 The pattern reveal
**Signal:** intervals · **already sorted, already disjoint** · one insertion.
**Therefore:** a three-phase linear scan. O(n), no sort.

**Key insight:** because the list is disjoint and sorted, the intervals that overlap the
new one form a **contiguous block**. You never have to come back, once you've passed an
interval it is settled forever. That is what turns "merge everything" into "find the
block, collapse it".

**The two boundary tests, and why they're different:**

```python
while i < n and intervals[i][1] < start:     # phase 1: ends strictly BEFORE we start
    ...                                       #   `<` -- touching means it must merge
while i < n and intervals[i][0] <= end:      # phase 2: starts at or before we end
    ...                                       #   `<=` -- touching means it must merge
```

Both use "touching counts", spelled two different ways because one compares an end
against a start and the other a start against an end. Flip either to the other
inequality and `[[1,3]] + [3,5]` gives `[[1,3],[3,5]]` instead of `[[1,5]]`.

**🧨 The trap: the new interval is appended in phase 2's place, not before it.** The
merged interval belongs *between* the "before" group and the "after" group. Append it
too early and the output isn't sorted; forget to append it at all when nothing overlaps
(both `while` loops fall straight through) and it vanishes, which is the case
`intervals = [[1,2]], new = [5,7]`.

## 🔍 Dry run: `intervals = [[1,2], [3,5], [6,7], [8,10], [12,16]]`, `new = [4,8]`
`s, e = 4, 8`, `out = []`, `i = 0`.

**Phase 1, copy everything ending before 4:**

| i | `intervals[i]` | `end < 4`? | action |
|---|---|---|---|
| 0 | `[1,2]` | 2 < 4 ✓ | copy → `out = [[1,2]]` |
| 1 | `[3,5]` | 5 < 4 ✗ | stop |

**Phase 2, absorb everything starting at or before 8:**

| i | `intervals[i]` | `start <= 8`? | `s = min(...)` | `e = max(...)` |
|---|---|---|---|---|
| 1 | `[3,5]` | 3 ≤ 8 ✓ | min(4, **3**) = **3** | max(8, 5) = 8 |
| 2 | `[6,7]` | 6 ≤ 8 ✓ | 3 | max(8, 7) = 8 |
| 3 | `[8,10]` | 8 ≤ 8 ✓ | 3 | max(8, **10**) = **10** |
| 4 | `[12,16]` | 12 ≤ 8 ✗ | - | stop |

Append the merged `[3, 10]` → `out = [[1,2], [3,10]]`.

**Phase 3, copy the rest:** `out = [[1,2], [3,10], [12,16]]` ✓

Two rows do the teaching. **`[3,5]`** is why `s = min(s, ...)` exists: the merged
interval starts at 3, *earlier* than the interval you were told to insert. And
**`[8,10]`** is why phase 2 uses `<=`: `8 <= 8` is a touch, and it's what stretches the
answer out to 10.

## ✅ Optimal solution
```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """Insert one interval into a sorted, disjoint list, merging as needed.

        Time:  O(n), one pass, no sort: the input is already ordered.
        Space: O(n), the output.
        """
        out = []
        i, n = 0, len(intervals)
        start, end = newInterval

        # 1. everything that finishes strictly before we begin
        while i < n and intervals[i][1] < start:
            out.append(intervals[i])
            i += 1

        # 2. everything that starts at or before we end -- swallow it
        while i < n and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        out.append([start, end])          # goes HERE: after `before`, before `after`

        # 3. everything left, untouched
        out.extend(intervals[i:])

        return out
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **Don't sort.** If you reach for `.sort()` you've turned an O(n) problem into
  O(n log n) and missed the point of the question being asked.
- **`min` on the start as well as `max` on the end.** The new interval can be swallowed
  *from the left*, `[[1,5]] + [2,3]` must stay `[[1,5]]`, and only the `min`/`max` pair
  gets that right.
- **Append the merged interval exactly once, between phases 2 and 3.** If both loops
  fall through (the new interval sits in a gap), that single append is the only thing
  putting it in the output.
- **`<` in phase 1, `<=` in phase 2.** They're comparing different ends. Test
  `[[1,3]] + [3,5]` → must be `[[1,5]]`.
- **Empty input.** Both loops do nothing, the append fires, `extend` adds nothing:
  `[[5,7]]` ✓. No special case needed, verify that rather than adding a guard.
- **Return type is a list of lists**, and phase 3's `extend` shares the original row
  objects. Fine for LeetCode; worth a comment in real code.

## 🎤 Interview talking points
- *"The list is already sorted and disjoint, so I won't re-sort, that's O(n log n) work
  the input already paid for."* ← say this first.
- *"The intervals that overlap the new one are contiguous, so it's three phases: copy
  before, absorb the block, copy after."*
- *"I take min of the starts and max of the ends, because the block can extend past the
  new interval on both sides."*
- *"O(n) time, and the only allocation is the output."*

## 🔗 Transfer
EP45 and EP46 are the same sweep with the sort turned on and off. Tomorrow (EP47) keeps
the input sorted but doubles it: **two** sorted lists, walked with two pointers, where
the question stops being "what merges" and becomes "what do they have in common".

## 📹 Metadata
- **Title:** `Insert Interval, three phases, no sort | Merge Intervals #2`
- **Thumbnail:** `BEFORE · ABSORB · AFTER` (green block)
- **Short:** `[4,8]` swallowing three intervals at once on the timeline. 40s.
