# EP080 · P10E10 · Search in Rotated Sorted Array   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/search-in-rotated-sorted-array/description/

---

## 🎬 Hook
> "Search a rotated sorted array. The instinct is to compare `mid` with the target and
> go left or right. In a rotated array that comparison tells you **nothing**. The fix is
> one fact: cut a rotated array anywhere, and **at least one half is perfectly sorted**.
> Find that half, ask 'is the target in it?', and you always know where to go."

## 📋 Problem, in your words
```
A sorted array of DISTINCT integers was rotated at an unknown pivot:
[0, 1, 2, 4, 5, 6, 7] -> [4, 5, 6, 7, 0, 1, 2].

Given the rotated array and a target, return target's index, or -1.
Must be O(log n).
```

## 🔢 The example
```
Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 0
Output: 4

Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 3
Output: -1

Input:  nums = [1], target = 0
Output: -1
```

## 🧸 ELI5
> Two bookshelves pushed together. Each shelf is in alphabetical order, but the second
> shelf (A to M) was put on the **left** of the first (N to Z), so the row reads N...Z,
> A...M.
>
> You open to the middle of the row. The books to one side of you are definitely one
> clean alphabetical run. You can tell which side by checking whether the first book on
> that side comes before you alphabetically.
>
> ```
> [4, 5, 6, 7, 0, 1, 2]
>  lo       mid      hi
> 4 <= 7   -> left side [4..7] is a clean run
> is 0 between 4 and 7?  no  -> it's not there, so go right
> ```
>
> You can only answer "is it in here?" for a clean run. So you always ask about the
> clean side, and if the answer is no, the book is on the other side.

## 🐌 Brute force (say it, don't type it)
Linear scan, **O(n)**. A better "brute force" worth mentioning: find the rotation point
with EP79 in O(log n), then run EP71 on whichever sorted piece could contain the
target. Two binary searches, still O(log n), and completely acceptable. Today's version
does it in one pass.

## 💡 The pattern reveal
**Signal:** "rotated sorted array" · "search for target" · "O(log n)".
**Therefore:** Shape B, find the sorted half, then range-check.

**Key insight:** at any `mid`, one of `[lo..mid]` or `[mid..hi]` is sorted. You can
tell which with one comparison, and for a sorted range you can check membership with
two comparisons. Everything else is the other half.

| step | code | meaning |
|---|---|---|
| found? | `nums[mid] == target` | return `mid` |
| which half is sorted? | `nums[lo] <= nums[mid]` | True: left half. False: right half |
| target in the sorted half? | `nums[lo] <= target < nums[mid]` (or `nums[mid] < target <= nums[hi]`) | yes: go there. no: go to the other half |

**Template note:** this is the first problem in the pattern where the **closed** style
(`lo <= hi`, `hi = mid - 1`, early return) is cleaner, because you're looking for an
exact match, not a flip point, and you need `nums[hi]` to be a real element for the
range check. The pattern card's rule: don't mix the styles *within* one loop. Pick
this one here, knowingly.

## 🔍 Dry run: `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`

| step | lo | hi | mid | nums[mid] | sorted half | target in it? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | left `[4..7]` | 4 <= 0 < 7? no | `lo = 4` |
| 2 | 4 | 6 | 5 | 1 | left `[0..1]` | 0 <= 0 < 1? yes | `hi = 4` |
| 3 | 4 | 4 | 4 | 0 | | | **found**, return **4** ✓ |

Step 2 is worth a pause: after step 1 the range `[0, 1, 2]` is fully sorted, so the
"left half" check succeeds and the problem has become ordinary binary search. Rotated
search degrades gracefully into EP71 once the break is out of range.

**Target 3:** step 1 same (not in `[4..7]`, go right). Step 2: left `[0..1]`, 3 not in
it, `lo = 6`. Step 3: `nums[6] = 2`, left `[2..2]`, not in it, `lo = 7`. `lo > hi` →
**-1** ✓.

## ✅ Optimal solution
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Index of target in a rotated sorted array of distinct values, or -1.

        Time:  O(log n), one halving per iteration.
        Space: O(1).
        """
        lo, hi = 0, len(nums) - 1           # closed interval: exact-match search
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid

            if nums[lo] <= nums[mid]:       # left half [lo..mid] is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1            # target is inside the sorted left half
                else:
                    lo = mid + 1            # not in it, so it can only be on the right
            else:                           # right half [mid..hi] is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1            # target is inside the sorted right half
                else:
                    hi = mid - 1            # not in it, so it can only be on the left
        return -1
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **`nums[lo] <= nums[mid]`, with `<=`.** When `lo == mid` (two elements left, e.g.
  `[3, 1]` searching for 1), the left "half" is just `nums[mid]` and must count as
  sorted. With `<` you'd treat the right half as sorted when it isn't, and miss.
  `[3, 1]`, target 1 is the test case.
- **Strict and non-strict ends of the range check.** `nums[lo] <= target < nums[mid]`:
  `mid` is already known not to be the target, so the upper end is strict. Same on the
  right: `nums[mid] < target <= nums[hi]`.
- **Never compare target with `nums[mid]` alone to pick a direction.** `mid = 7`,
  `target = 0`: "0 < 7, go left" is wrong. Direction only makes sense inside a sorted
  run.
- **Duplicates (LeetCode 81)** break "which half is sorted" when `nums[lo] ==
  nums[mid] == nums[hi]`. Shrink both ends by one and accept O(n) worst case.
- **Closed interval on purpose.** `hi = len(nums) - 1` and `lo <= hi` here. Say why:
  exact match, and `nums[hi]` is read in the range check.

## 🎤 Interview talking points
- *"In a rotated array, one of the two halves around mid is always sorted. I find it by
  comparing `nums[lo]` with `nums[mid]`."*
- *"Membership is only checkable on a sorted range, so I check the target against the
  sorted half. In it: go there. Not in it: go the other way."*
- *"Alternative: find the pivot with the min-search, then binary search one side. Two
  O(log n) passes."*
- *"With duplicates, `nums[lo] == nums[mid]` is ambiguous and it becomes O(n) worst
  case."*

## 🔗 Transfer
That's Shape B done: every problem searched an index range, with a predicate built from
the array's own shape. Tomorrow, EP81 Koko Eating Bananas, is the jump the whole pattern
card is built around. You stop searching the **array** and start searching the
**answer**: possible eating speeds from 1 to `max(piles)`, with "can she finish in time
at this speed?" as the predicate.

## 📹 Metadata
- **Title:** `Search in Rotated Sorted Array, find the sorted half first | Binary Search #10`
- **Thumbnail:** `which half is sorted?` (blue block)
- **Short:** "0 < 7 so go left" failing, then the sorted-half check fixing it. 50s.
