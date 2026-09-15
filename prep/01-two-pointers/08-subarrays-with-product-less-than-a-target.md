# EP008 · P01E08 · Subarrays with Product Less than a Target   [Medium]

**Pattern:** Two Pointers / Sliding Window · **Link:** https://leetcode.com/problems/subarray-product-less-than-k/

---

## 🎬 Hook
> "Here's the question that decides whether you get this one: when your window is
> valid, how many subarrays did you just find? Not one. The answer is the window's
> length — and once you see why, the code is six lines."

## 📋 Problem, in your words
```
Given an array of POSITIVE integers and an integer k, count how many
CONTIGUOUS subarrays have a product strictly less than k.

Contiguous = the elements are next to each other. [1,2,3] contains [2,3] but not [1,3].
```

## 🔢 The example
```
Input:  nums = [10, 5, 2, 6],  k = 100
Output: 8
Subarrays: [10] [5] [2] [6] [10,5] [5,2] [2,6] [5,2,6]
Not counted: [10,5,2] = 100 (not strictly less), and anything containing it.
```

## 🧸 ELI5
> You're filling a shopping bag, left to right, and the bag bursts if the product of
> the prices goes over k.
>
> Keep adding items to the right. When it's about to burst, start removing items from
> the **left** until it's safe again.
>
> Now the key question: with a safe bag holding items from `lo` to `hi`, how many
> valid shopping trips *ending at item `hi`* have you just found? Every suffix of the
> bag: just `[hi]`, then `[hi−1, hi]`, then `[hi−2, hi]`, all the way to the whole bag.
> That's exactly **`hi − lo + 1`** of them.
>
> So each time you move the right finger, you add the window's current length to your
> total. You never enumerate the subarrays — you count them.

## 🐌 Brute force (say it, don't type it)
Every start, every end, multiply — **O(n²)** or O(n³). For n = 30,000 it times out.

## 💡 The pattern reveal
**Signal:** *contiguous subarrays* + a **monotonic** constraint + **all positive**.
**Therefore:** a sliding window (two pointers, same direction), with batch counting.

**Key insight:** *all values are positive* is not flavour text — it's the load-bearing
condition. Positive values mean growing the window can only **increase** the product
and shrinking can only **decrease** it. That monotonicity is what lets `lo` move
forward and never back. Drop in a zero or a fraction and the whole approach collapses.
Say this out loud; it's the difference between memorising and understanding.

## 🔍 Dry run — `[10, 5, 2, 6]`, k = 100
| hi | num | product | shrink? | window | adds `hi−lo+1` | total |
|---|---|---|---|---|---|---|
| 0 | 10 | 10 | no | `[10]` | 1 | 1 |
| 1 | 5 | 50 | no | `[10,5]` | 2 | 3 |
| 2 | 2 | 100 | **yes** → `lo=1`, product = 10 | `[5,2]` | 2 | 5 |
| 3 | 6 | 60 | no | `[5,2,6]` | 3 | 8 |

Total = **8** ✓

At `hi = 3`, adding 3 counted `[6]`, `[2,6]`, `[5,2,6]` in one step.

## ✅ Optimal solution
```python
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:                        # no positive product is < 1
            return 0

        product, lo, count = 1, 0, 0

        for hi in range(len(nums)):
            product *= nums[hi]           # grow right

            while product >= k:           # shrink left until valid again
                product //= nums[lo]
                lo += 1

            count += hi - lo + 1          # every subarray ENDING at hi

        return count
```
**Time:** O(n) — `lo` and `hi` each traverse the array at most once (amortised).
**Space:** O(1)

## ⚠️ Gotchas
- **`if k <= 1: return 0`.** Without it, `product //= nums[lo]` runs with `lo > hi`
  and you index out of range. All inputs are ≥ 1, so no product is ever < 1.
- **`hi - lo + 1`, with the `+1`.** Contrast with EP7's `hi - lo`. Here you're counting
  *suffixes ending at `hi`*, which includes the single element `[hi]` itself. In EP7
  you were counting elements *strictly between* two fixed pointers. Put both on screen
  side by side — this is a genuinely great teaching moment.
- **`while`, not `if`.** One division may not be enough to get back under `k`.
- Use `//=` (integer division) to undo `*=`. With floats you accumulate rounding error
  and fail on large inputs.
- The while loop looks like it makes this O(n²). It doesn't: `lo` only ever moves
  forward, at most n times *across the entire run*. That's **amortised analysis** —
  naming it out loud is a strong signal.

## 🎤 Interview talking points
- *"The all-positive constraint gives me monotonicity, which is what makes the window
  valid to slide instead of restart."*
- *"Each step I count all subarrays ending at the right pointer — that's the window
  length — so every subarray is counted exactly once, by its endpoint."*
- *"The inner while is amortised O(1): `lo` advances at most n times total."*

## 🔗 Transfer
This is the bridge into **Pattern 3: Sliding Window** (EP 27–38). The "count all
subarrays ending here" trick reappears in Binary Subarrays With Sum and Count Number
of Nice Subarrays. And the "positives give monotonicity" caveat is exactly why
Maximum Product Subarray (EP 41, Kadane) needs a completely different technique —
because it *allows* negatives.

## 📹 Metadata
- **Title:** `Subarray Product Less Than K — why you add the window LENGTH | Two Pointers #8`
- **Thumbnail:** `+1 WINDOW LENGTH` (blue block)
- **Short:** "Why does all-positive matter?" — 55 seconds.
