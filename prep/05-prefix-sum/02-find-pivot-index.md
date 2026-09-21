# EP040 · P05E02 · Find Pivot Index   [Easy]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/find-pivot-index/

---

## 🎬 Hook
> "Find the index where everything on the left sums to everything on the right. The
> obvious solution slices the array at every index — O(n²). But the right side is never
> a mystery: it's `total − left − nums[i]`. One number you already know, minus two you
> are already carrying. This is Pattern 05 with the dictionary taken away."

## 📋 Problem, in your words
```
Given an integer array nums, return the LEFTMOST index i such that

    sum(nums[0 .. i-1])  ==  sum(nums[i+1 .. n-1])

The pivot element itself belongs to NEITHER side. If no such index
exists, return -1. An empty side sums to 0 -- so index 0 and index
n-1 are legal candidates.
```

## 🔢 The example
```
Input:  nums = [1, 7, 3, 6, 5, 6]
Output: 3
Why:    left  = 1 + 7 + 3 = 11
        right = 5 + 6     = 11        (nums[3] = 6 is excluded)

Input:  nums = [1, 2, 3]
Output: -1

Input:  nums = [2, 1, -1]
Output: 0                <- left side is EMPTY (sum 0), right is 1 + (-1) = 0
```
That third case is the whole episode. If you initialise anything to "the first element"
you will miss it.

## 🧸 ELI5
> Think of the array as a plank with weights on it, and you're looking for the point
> where it balances.
>
> ```
>   [ 1   7   3 ] [ 6 ] [ 5   6 ]
>     left = 11   pivot  right = 11
>   ------------------------------
>        total = 28 = 11 + 6 + 11
> ```
>
> Here's the trick: **the whole plank weighs the same no matter where you stand.** So
> once you know the total and what's behind you, what's ahead of you is forced:
>
> ```
> right = total − left − nums[i]
> ```
>
> Walk left to right carrying `left`. At each index, compute `right` by subtraction and
> compare. No slicing, no second loop, no dictionary — the "prefix map" of the other
> episodes collapses to a single integer here, because there is only ever one earlier
> position that matters: the one directly behind you.

## 🐌 Brute force (say it, don't type it)
For each `i`, `sum(nums[:i]) == sum(nums[i+1:])`. **O(n²)** — the slices re-add the same
elements n times. In Python it is one readable line and it is the right thing to say
first, precisely because the fix is so small: hoist `total` out, and accumulate `left`
instead of recomputing it.

## 💡 The pattern reveal
**Signal:** repeated **range sums** over the same array · a left/right split.
**Therefore:** one prefix accumulator and one total. O(n) time, **O(1) space**.

**Key insight:** the three quantities are not independent.

```
total = left + nums[i] + right        (always, for every i)
=>  right = total - left - nums[i]
```

So the balance test `left == right` becomes `left == total − left − nums[i]`, or
equivalently `2*left + nums[i] == total` — both are fine, and saying the second one out
loud in an interview shows you rearranged it rather than memorised it.

**Why this episode exists.** EP39 made prefix sums look like they *are* a hash map.
They aren't. The map is a lookup structure bolted on when you need arbitrary earlier
positions; when you only need the position immediately behind you, the whole pattern is
one running variable. Recognising which of the two you need is the actual skill.

## 🔍 Dry run — `nums = [1, 7, 3, 6, 5, 6]`
`total = 28`, `left = 0`.

| i | `nums[i]` | `left` | `right = 28 − left − nums[i]` | balanced? |
|---|---|---|---|---|
| 0 | 1 | 0 | 28 − 0 − 1 = 27 | no |
| 1 | 7 | 1 | 28 − 1 − 7 = 20 | no |
| 2 | 3 | 8 | 28 − 8 − 3 = 17 | no |
| 3 | 6 | 11 | 28 − 11 − 6 = **11** | **yes → return 3** |
| 4 | 5 | 17 | 28 − 17 − 5 = 6 | no |
| 5 | 6 | 22 | 28 − 22 − 6 = 0 | no |

Answer **3** ✓

Notice row 0: `left = 0` before anything is added. That is the empty-prefix idea from
EP39 wearing different clothes — and it is what makes `[2, 1, −1]` return 0 instead
of −1.

## 🔍 Dry run — `nums = [2, 1, -1]` (the empty-side case)
`total = 2`, `left = 0`.

| i | `nums[i]` | `left` | `right` | balanced? |
|---|---|---|---|---|
| 0 | 2 | **0** | 2 − 0 − 2 = **0** | **yes → return 0** |

Both sides are zero: the left because there's nothing there, the right because `1` and
`−1` cancel. Answer **0** ✓ — and any solution that starts the scan at `i = 1`, or seeds
`left = nums[0]`, returns −1 here.

## ✅ Optimal solution
```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        """Leftmost index where the sums either side are equal.

        Time:  O(n) — one pass for the total, one to scan.
        Space: O(1) — two integers. No map needed.
        """
        total = sum(nums)
        left = 0                       # the EMPTY left side, worth 0

        for i, x in enumerate(nums):
            right = total - left - x   # what's ahead is forced by what's behind
            if left == right:
                return i               # leftmost, so return on the first hit
            left += x                  # only now does x join the left side

        return -1
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`left += x` goes *after* the comparison.** Move it up one line and the pivot gets
  counted on its own left side — every test fails, including the LeetCode example.
- **Start at `i = 0` with `left = 0`.** An empty side is a legal side. `[2, 1, −1] → 0`
  is the test that catches this, and `[−1, 1, 2] → 2` catches the mirror image at the
  far end.
- **Return on the first hit.** The problem says *leftmost*. `[0, 0, 0]` has three valid
  pivots and the answer is **0**.
- **Negatives are fine and they matter.** They're why you can't stop early when `left`
  exceeds half the total — the sum is not monotonic. Don't add that "optimisation".
- **No map.** If you find yourself building a dictionary here, you have pattern-matched
  on EP39 rather than read the question. Only one earlier position is ever relevant.
- **Don't recompute `total` inside the loop.** That's the O(n²) brute force with extra
  steps.

## 🎤 Interview talking points
- *"The right side is `total − left − nums[i]`, so I never need to sum it — one pass for
  the total, one to walk."*
- *"Equivalently `2*left + nums[i] == total`, which avoids the subtraction entirely."*
  ← shows the algebra is yours.
- *"Index 0 is a real candidate because an empty side sums to zero, so I start the scan
  there with `left = 0`."*
- *"O(1) space — unlike the rest of this pattern, there's nothing to remember except the
  running total."*

## 🔗 Transfer
This is the smallest possible prefix-sum problem and the one that isolates the
arithmetic from the data structure. Everything after it adds a lookup structure *on top*
of exactly this running total: a count map in EP41, a first-index map in EP42, a
monotonic deque in EP43. Tomorrow (EP41) puts the map back, with one twist — the key
isn't the running total itself, it's the running total **mod k**.

## 📹 Metadata
- **Title:** `Find Pivot Index — the right side is already known | Prefix Sum #2`
- **Thumbnail:** `RIGHT = TOTAL − LEFT − x` (green block)
- **Short:** `[2,1,-1]` → 0, the empty-left-side case that breaks most first attempts. 40s.
