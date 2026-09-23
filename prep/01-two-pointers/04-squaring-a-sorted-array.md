# EP004 · P01E04 · Squaring a Sorted Array   [Easy]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/squares-of-a-sorted-array/

---

## 🎬 Hook
> "Square a sorted array and it stops being sorted. Negative numbers ruin everything.
> But here's the thing, the biggest square is *always* at one of the two ends. So
> build the answer backwards, and it's one pass."

## 📋 Problem, in your words
```
Given an array sorted in non-decreasing order, return an array of the squares
of each number, also sorted in non-decreasing order.

The catch: the input can contain negatives.
```

## 🔢 The example
```
Input:  [-4, -1, 0, 3, 10]
Squares: [16,  1, 0, 9, 100]   <-- not sorted!
Output: [0, 1, 9, 16, 100]
```

Walk through this on camera slowly. The moment the viewer sees `[16, 1, 0, 9, 100]`
they understand why this isn't a one-liner.

## 🧸 ELI5
> Think of the number line as a road, and **0 is your house**. Squaring a number just
> asks *"how far is it from my house?"*, direction stops mattering, only distance.
>
> The array is sorted, so the numbers furthest from home are at the **two ends**,
> the most negative on the left, the most positive on the right. You don't know which
> of those two is further, so you check both.
>
> Whichever is further away, that's the **largest** square. So you fill your answer
> array **from the back**, because you're finding biggest-first. Then step that
> pointer inward and ask again.

## 🐌 Brute force (say it, don't type it)
```python
return sorted(x * x for x in nums)     # O(n log n)
```
Honest note for the video: **this passes on LeetCode.** Say so. Then say why the
interviewer doesn't want it: the input was handed to you already sorted, and this
throws that information away and pays to rebuild it. The follow-up is always
*"can you do it in O(n)?"*, and the answer is today's episode.

## 💡 The pattern reveal
**Signal:** sorted input, negatives present, "return sorted output."
**Therefore:** Two Pointers, Shape A, converging from the ends, but **writing
backwards**.

**Key insight:** squaring is a *distance from zero*. On a sorted array, the maximum
distance from zero lives at one of the two extremes, never in the middle. So the
largest element of the answer is decidable in O(1), and you can fill the result
right-to-left.

## 🔍 Dry run: `[-4, -1, 0, 3, 10]`
| step | lo | hi | \|nums[lo]\| vs \|nums[hi]\| | winner | write | result |
|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 4 vs 10 | right | `100` at idx 4 | `[_,_,_,_,100]` |
| 2 | 0 | 3 | 4 vs 3 | left | `16` at idx 3 | `[_,_,_,16,100]` |
| 3 | 1 | 3 | 1 vs 3 | right | `9` at idx 2 | `[_,_,9,16,100]` |
| 4 | 1 | 2 | 1 vs 0 | left | `1` at idx 1 | `[_,1,9,16,100]` |
| 5 | 2 | 2 | 0 vs 0 | either | `0` at idx 0 | `[0,1,9,16,100]` |

## ✅ Optimal solution
```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        lo, hi = 0, n - 1

        for write in range(n - 1, -1, -1):     # fill BACKWARDS: biggest first
            left, right = nums[lo] * nums[lo], nums[hi] * nums[hi]
            if left > right:
                result[write] = left
                lo += 1
            else:
                result[write] = right
                hi -= 1

        return result
```
**Time:** O(n) · **Space:** O(n) for the output, which is required, not overhead.
If asked "can you do O(1) space?", the answer is no: you must return a new array, and
you can't safely overwrite the input because the value you'd clobber may still be needed.

## ⚠️ Gotchas
- **Fill backwards.** The instinct is to write left-to-right, but you can only cheaply
  identify the *largest* remaining square, not the smallest. Trying to go forwards
  means comparing toward the middle, where the smallest lives, and you don't know
  where that is without a search.
- Compare the **squares**, not the raw values. `-4 < 3` is true but `16 > 9`. If you
  compare raw values you get it backwards for negatives. (You can also compare
  `abs()`, which some find clearer, mention both.)
- `while lo <= hi` / `range(n-1, -1, -1)` must include the final single element.
  Stopping at `lo < hi` drops one value and returns a zero in slot 0.

## 🎤 Interview talking points
- *"Squaring maps the array to distance-from-zero, so sortedness is preserved on each
  side of zero but the array folds at zero. The two pointers are effectively merging
  two sorted sequences, the negatives descending and the positives ascending."*
  ← That merge framing is the elegant version. It directly connects to merge sort.
- *"I fill the output from the back because the max is O(1) to find and the min isn't."*

## 🔗 Transfer
This is secretly the **merge step of merge sort** on two sorted runs. That framing
comes back in EP 99 (Merge K Sorted Arrays) and in the two-heap problems. Also: the
"fill backwards to avoid overwriting" trick is the exact technique in Merge Sorted
Array (LC 88), worth a mention as homework.

## 📹 Metadata
- **Title:** `Squares of a Sorted Array, why you must build it backwards | Two Pointers #4`
- **Thumbnail:** `BUILD IT BACKWARDS` (blue block)
- **Short:** Beat 3, show `[16,1,0,9,100]` and ask "why isn't this sorted?"
