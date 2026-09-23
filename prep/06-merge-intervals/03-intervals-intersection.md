# EP047 · P06E03 · Intervals Intersection   [Medium]

**Pattern:** Merge Intervals · **Link:** https://leetcode.com/problems/interval-list-intersections/

---

## 🎬 Hook
> "Two people's calendars, both already sorted, both already tidy. Find every slot where
> they're *both* busy. Two pointers, and one decision that makes the whole thing work:
> when you've compared a pair, you advance **whichever interval ends first**: because
> that's the one that can never meet anything else."

## 📋 Problem, in your words
```
Given two lists of closed intervals, each sorted and each internally
disjoint, return the intersection of the two lists -- every interval
of time covered by BOTH.

Closed intervals: [1,3] and [3,5] intersect at the single point [3,3],
and that counts as a result.
```

## 🔢 The example
```
Input:  A = [[0,2], [5,10], [13,23], [24,25]]
        B = [[1,5], [8,12], [15,24], [25,26]]
Output: [[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]

Input:  A = [[1,3], [5,9]], B = []     -> []
```
Note `[5,5]`, `[24,24]` and `[25,25]`, **single-point intersections**. Three of the six
results are degenerate, which is the problem telling you loudly that `lo <= hi` is the
emptiness test, not `lo < hi`.

## 🧸 ELI5
> Lay both calendars on the same timeline, one above the other:
>
> ```
> A:  [0--2]      [5------10]    [13---------23] [24-25]
> B:     [1----5]      [8-----12]     [15--------24]  [25-26]
>        ####        ###   ##          #########  #     #
>        both busy here
> ```
>
> Put a finger on the first interval of each list. The overlap of the two you're
> pointing at, if there is one, is simply:
>
> ```
> from  max(the two starts)   to   min(the two ends)
> ```
>
> and it's real as long as the start isn't past the end.
>
> Then, the only decision: **move the finger on whichever interval finishes first.**
> That interval is done, everything further along in the other list starts even later,
> so it can't possibly meet it. The one that ends later stays put, because it might
> still meet the *next* interval in the other list.

## 🐌 Brute force (say it, don't type it)
Every pair `a` in A, `b` in B, keep `[max(starts), min(ends)]` when non-empty.
**O(n·m)** and it produces the right answers in the right order if you iterate
carefully. The two-pointer version is the same intersection formula with the wasted
comparisons deleted.

## 💡 The pattern reveal
**Signal:** **two** lists of intervals · both already sorted · "common" / "intersection".
**Therefore:** two pointers, O(n + m), O(1) extra space.

**Key insight, the intersection formula is always the same:**

```
lo = max(a.start, b.start)        # the later start
hi = min(a.end,   b.end)          # the earlier end
non-empty  <=>  lo <= hi
```

It's worth saying that out loud as *"latest start, earliest end"*, it holds whether the
intervals overlap partly, one contains the other, or they merely touch.

**And the advance rule, which is the actual algorithm:**

```python
if a.end < b.end:  i += 1      # A's interval is exhausted
else:              j += 1      # B's is (ties: either, pick one)
```

**Why it's the *end* and not the start:** the interval that ends first cannot intersect
anything later in the other list, because everything later in that list starts at or
after the current one's start, and we've already taken what those two had in common.
The one ending later is still live. Advancing by start instead skips real
intersections; it's the mistake to make on camera once, deliberately.

## 🔍 Dry run: the example above
`A = [[0,2], [5,10], [13,23], [24,25]]`, `B = [[1,5], [8,12], [15,24], [25,26]]`.

| `A[i]` | `B[j]` | `lo = max` | `hi = min` | `lo <= hi`? | emit | advance |
|---|---|---|---|---|---|---|
| `[0,2]` | `[1,5]` | 1 | 2 | ✓ | **`[1,2]`** | A ends at 2 < 5 → **i++** |
| `[5,10]` | `[1,5]` | 5 | 5 | ✓ | **`[5,5]`** ← a single point | B ends at 5 < 10 → **j++** |
| `[5,10]` | `[8,12]` | 8 | 10 | ✓ | **`[8,10]`** | A ends at 10 < 12 → **i++** |
| `[13,23]` | `[8,12]` | 13 | 12 | ✗ (13 > 12) | - | B ends at 12 < 23 → **j++** |
| `[13,23]` | `[15,24]` | 15 | 23 | ✓ | **`[15,23]`** | A ends at 23 < 24 → **i++** |
| `[24,25]` | `[15,24]` | 24 | 24 | ✓ | **`[24,24]`** | B ends at 24 < 25 → **j++** |
| `[24,25]` | `[25,26]` | 25 | 25 | ✓ | **`[25,25]`** | A ends at 25 < 26 → **i++** → A exhausted, stop |

Answer **`[[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]`** ✓

Three rows to narrate:

- **Row 2** emits `[5,5]`. `lo == hi` is a legal, non-empty intersection under closed
  intervals. A `lo < hi` test drops it, along with two more later.
- **Row 4** emits nothing: `lo = 13 > hi = 12`. The pointers still advance, a miss is
  progress, not a failure.
- **Row 6**: `A[3] = [24,25]` stays put while B moves, and is immediately rewarded with
  a second intersection at row 7. That is exactly what "keep the one that ends later"
  buys you.

## ✅ Optimal solution
```python
class Solution:
    def intervalIntersection(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """Every interval covered by both sorted, disjoint lists.

        Time:  O(n + m), each pointer only moves forward.
        Space: O(1) beyond the output.
        """
        out = []
        i = j = 0

        while i < len(A) and j < len(B):
            lo = max(A[i][0], B[j][0])       # latest start
            hi = min(A[i][1], B[j][1])       # earliest end
            if lo <= hi:                     # `<=`: a single point counts
                out.append([lo, hi])

            # the one that ends first can't meet anything further along
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1

        return out
```
**Time:** O(n + m) · **Space:** O(1) extra

## ⚠️ Gotchas
- **`lo <= hi`, not `lo < hi`.** Half the expected output of the example problem is
  single-point intersections. This is the failure that passes three tests and fails the
  fourth.
- **Advance by end, never by start.** Compare `A[i][1] < B[j][1]`. If you find yourself
  comparing starts to decide who moves, you're writing a merge, not an intersection.
- **Ties: advance either one, but only one.** `A[i][1] == B[j][1]` means both are
  finished; advancing just one costs a single wasted iteration and keeps the code
  simple. Advancing *both* is also correct here, but if you do, say why.
- **Don't merge anything.** Both lists are already disjoint, so the output is
  automatically sorted and disjoint. No post-processing.
- **Either list empty** → the `while` never runs → `[]` ✓.
- **This is not the two-pointer of Pattern 01.** There, two pointers walk one array from
  both ends. Here they walk two arrays in the same direction. Same name, different
  animal, worth saying so when the interviewer asks "what pattern is this?"

## 🎤 Interview talking points
- *"The intersection of two intervals is the latest start to the earliest end, and it's
  real if that start is at most that end."*
- *"I advance whichever interval ends first, because it can't intersect anything later
  in the other list."* ← the sentence being tested.
- *"Closed intervals, so a single-point overlap like `[5,5]` counts, I'd confirm that
  convention first."*
- *"O(n + m), constant extra space, because both inputs are already sorted."*

## 🔗 Transfer
This is the only two-list episode in Pattern 06, and "advance the earlier end" is the
same greedy instinct that runs EP49 and EP50, where a heap picks out the earliest end
for you instead of a comparison. Tomorrow (EP48) goes back to one list for the pattern's
simplest question, *does any pair overlap at all?*, and proves why checking only
**adjacent** pairs is enough.

## 📹 Metadata
- **Title:** `Interval List Intersections, advance the earlier end | Merge Intervals #3`
- **Thumbnail:** `MAX START · MIN END` (green block)
- **Short:** the two-calendar timeline, and why `[5,5]` is a real answer. 45s.
