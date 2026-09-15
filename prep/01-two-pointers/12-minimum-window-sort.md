# EP012 · P01E12 · Minimum Window Sort   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/shortest-unsorted-continuous-subarray/

---

## 🎬 Hook
> "Find the shortest chunk you could sort to make the whole array sorted. The obvious
> answer — sort a copy and compare — is O(n log n) and it works. But there's an O(n)
> answer that needs nothing but two walks across the array, and it's the perfect
> closer for this pattern."

## 📋 Problem, in your words
```
Given an array, find the SHORTEST contiguous subarray such that sorting just
that subarray makes the ENTIRE array sorted in ascending order.

Return its length. If the array is already sorted, return 0.
```

## 🔢 The example
```
Input:  [2, 6, 4, 8, 10, 9, 15]
Output: 5
Why:    sorting [6, 4, 8, 10, 9] (indices 1..5) gives [2,4,6,8,9,10,15]. Sorted.
        Any shorter window leaves something out of order.
```

## 🧸 ELI5
> A line of people supposed to be standing shortest to tallest, but a few are out of
> place. You want the smallest stretch of the line you could re-shuffle to fix
> everything.
>
> Walk from the left until you find the first person taller than someone behind them —
> that's roughly where the mess starts. Walk from the right until you find the first
> person shorter than someone ahead of them — roughly where it ends.
>
> **But that's not quite enough.** Say the messy stretch contains someone *very*
> short. They don't just belong inside the stretch — they have to move further left,
> past people who *looked* fine. So you widen the boundary until the person just
> outside is genuinely shorter than everyone in the mess.
>
> Same on the right with the tallest person in the mess.

That widening step is the entire difficulty. Everything else is easy.

## 🐌 Brute force (say it, don't type it)
```python
sorted_nums = sorted(nums)
# find first and last index where they differ
```
**O(n log n) time, O(n) space.** Correct, three lines, passes. Show it. Then: *"the
interviewer's follow-up is always O(n) and O(1), and here's how."*

## 💡 The pattern reveal
**Signal:** find a *boundary* from each end of an array.
**Therefore:** Two Pointers scanning inward from both ends — plus a **min/max
extension** pass.

**Key insight:** the unsorted window is defined by two facts:
1. Its **minimum** must be ≥ everything to its left.
2. Its **maximum** must be ≤ everything to its right.

So: find a rough window, take its min and max, then expand the boundaries outward
until both conditions hold.

## 🔍 Dry run — `[2, 6, 4, 8, 10, 9, 15]`
**Step 1 — rough left boundary.** Walk right while ascending:
`2 ≤ 6` ok, `6 > 4` ✗ → stop. `lo = 1`.

**Step 2 — rough right boundary.** Walk left while descending:
`15 ≥ 9` ok, `9 < 10` ✗ → stop. `hi = 5`.

**Step 3 — min and max inside `[1..5]` = `[6,4,8,10,9]`:** min = 4, max = 10.

**Step 4 — extend left** while something to the left exceeds the min:
`nums[0] = 2 > 4`? No → `lo` stays **1**.

**Step 5 — extend right** while something to the right is below the max:
`nums[6] = 15 < 10`? No → `hi` stays **5**.

Answer: `hi - lo + 1` = `5 - 1 + 1` = **5** ✓

> Want a case where extension actually fires? `[1, 3, 2, 0, 5]`. Rough window is
> `[1..3]` = `[3,2,0]`, min = 0. Now `nums[0] = 1 > 0`, so `lo` extends to **0**.
> Answer 4, not 3. **Use this as the second example in the video** — it's the case
> that proves why steps 4 and 5 exist.

## ✅ Optimal solution
```python
class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        lo, hi = 0, n - 1

        # 1. first index from the left that breaks ascending order
        while lo < n - 1 and nums[lo] <= nums[lo + 1]:
            lo += 1
        if lo == n - 1:
            return 0                                # already fully sorted

        # 2. first index from the right that breaks it
        while hi > 0 and nums[hi] >= nums[hi - 1]:
            hi -= 1

        # 3. min and max inside the rough window
        window_min = min(nums[lo:hi + 1])
        window_max = max(nums[lo:hi + 1])

        # 4. extend left: anything bigger than the window's min belongs inside
        while lo > 0 and nums[lo - 1] > window_min:
            lo -= 1

        # 5. extend right: anything smaller than the window's max belongs inside
        while hi < n - 1 and nums[hi + 1] < window_max:
            hi += 1

        return hi - lo + 1
```
**Time:** O(n) — five linear passes · **Space:** O(1)

## ⚠️ Gotchas
- **The early return `if lo == n - 1: return 0`.** Without it, an already-sorted array
  produces a nonsense window. It's also the empty/single-element guard.
- **`<=` and `>=` in the scans**, not `<` and `>`. Equal neighbours are sorted; strict
  comparisons treat `[1,1,1]` as unsorted.
- Steps 4 and 5 are not optional. A test like `[1,3,2,0,5]` fails without them, and
  it's the kind of case LeetCode has and your head doesn't.
- `min(nums[lo:hi+1])` slices, which is technically O(k) space in Python. For strict
  O(1), track min/max with an explicit loop. Worth naming on camera — it shows you
  know what your language is doing under the hood.

## 🎤 Interview talking points
- *"The unsorted window is characterised by its min needing to be ≥ everything left
  of it and its max ≤ everything right of it — so I find a candidate window, then
  expand until those two invariants hold."*
- *"There's also a one-pass version using running max/min from each side. Same
  complexity, slightly denser."* (Knowing an alternative exists, without needing to
  write it, is a good look.)

## 🔗 Transfer
This closes Pattern 1. The technique — *scan from both ends to locate a boundary, then
validate with an invariant* — is the shape behind Container With Most Water, Trapping
Rain Water, and the boundary-finding half of binary search (Pattern 10, EP 74–96).

**🎉 Pattern 1 complete.** Record a 3-minute pattern recap as the playlist's closing
video: the three shapes, the four recognition signals, and the four questions from
`patterns/01-two-pointers.md` under "knowing this in your sleep." Recap videos get
disproportionate watch time because people return to them before interviews.

## 📹 Metadata
- **Title:** `Shortest Unsorted Subarray — O(n), no sorting | Two Pointers #12 (finale)`
- **Thumbnail:** `FIND THE MESS` (blue block)
- **Short:** The `[1,3,2,0,5]` case — "why the obvious answer is wrong."
