# EP078 · P10E08 · Find Minimum in Rotated Sorted Array   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

---

## 🎬 Hook
> "Take a sorted array, cut it somewhere, swap the two pieces. Find the smallest
> element in O(log n). Everyone's instinct is to compare `mid` with the **left** end.
> That instinct has a bug that only shows up when the array isn't rotated at all.
> Compare with the **right** end and the bug can't happen."

## 📋 Problem, in your words
```
A sorted array of DISTINCT numbers was rotated some number of times:
[0, 1, 2, 4, 5, 6, 7] -> [4, 5, 6, 7, 0, 1, 2].

Return the minimum element. Must be O(log n).
The rotation could be 0 (the array might still be fully sorted).
```

## 🔢 The example
```
Input:  nums = [4, 5, 6, 7, 0, 1, 2]
Output: 0

Input:  nums = [3, 4, 5, 1, 2]
Output: 1

Input:  nums = [11, 13, 15, 17]
Output: 11             <- rotated 0 times (or n times): the trap case
```

## 🧸 ELI5
> A clock face with numbers 0 to 7, but someone spun it so reading from the top you see
> 4, 5, 6, 7, 0, 1, 2. The numbers still go up, until one spot where they **drop**.
> That drop is where 0 is.
>
> ```
> 4   5   6   7 | 0   1   2
> high part       low part
> ```
>
> Every number in the **high part** is bigger than the **last** number, 2.
> Every number in the **low part** is less than or equal to it.
>
> Stand anywhere and compare yourself to the last number. Bigger? You're in the high
> part, the drop is to your right. Smaller or equal? You're in the low part, the drop is
> here or to your left.

## 🐌 Brute force (say it, don't type it)
`min(nums)`, **O(n)**. Or scan for the one index where `nums[i] > nums[i + 1]`. Both
ignore that each half of the array is still sorted, which is the thing that lets you
throw half away per comparison.

## 💡 The pattern reveal
**Signal:** "rotated sorted array" · "O(log n)".
**Therefore:** Shape B, search on a condition.

**Key insight:** the predicate `nums[mid] > nums[hi]` means "mid is in the high part".
Across the array it reads `True, True, True, True, False, False, False`, and the
minimum is the **first False**.

| at mid | meaning | action |
|---|---|---|
| `nums[mid] > nums[hi]` | mid is in the high part; the drop is strictly right of mid | `lo = mid + 1` |
| otherwise | mid is in the low part; mid could be the minimum | `hi = mid` |

**Why `hi` and not `lo`?** Compare with `nums[lo]` instead and the unrotated case
breaks: `[11, 13, 15, 17]` has `nums[mid] > nums[lo]` everywhere, which would say "go
right", away from the minimum at index 0. Comparing with the right end has no such
case: in a sorted range `nums[mid] <= nums[hi]` always, so you go left, correctly.

## 🔍 Dry run: `nums = [4, 5, 6, 7, 0, 1, 2]`

| step | lo | hi | mid | nums[mid] | nums[hi] | mid > hi? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | 2 | yes | `lo = 4` |
| 2 | 4 | 6 | 5 | 1 | 2 | no | `hi = 5` |
| 3 | 4 | 5 | 4 | 0 | 1 | no | `hi = 4` |
| 4 | 4 | 4 | - | | | | return `nums[4]` = **0** ✓ |

**The trap case, `[11, 13, 15, 17]`:**

| step | lo | hi | mid | nums[mid] | nums[hi] | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 1 | 13 | 17 | not bigger → `hi = 1` |
| 2 | 0 | 1 | 0 | 11 | 13 | not bigger → `hi = 0` |
| - | 0 | 0 | | | | **11** ✓ |

No special case for "not rotated". It falls out.

## ✅ Optimal solution
```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        """Minimum of a rotated sorted array of distinct values.

        Time:  O(log n), one comparison per halving.
        Space: O(1).
        """
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1            # mid is in the rotated-up part; the drop is to the right
            else:
                hi = mid                # mid is in the low part; the minimum is mid or left of it
        return nums[lo]
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **Compare with `nums[hi]`, not `nums[lo]`.** The left-end comparison needs an extra
  "is this range already sorted?" check or it fails on unrotated input. The right-end
  comparison doesn't.
- **`nums[hi]` moves.** It's the right end of the *current* range, not `nums[-1]`.
  Both happen to work for distinct values, but `nums[hi]` is the one that generalises
  to the duplicates version.
- **`hi = mid`, not `mid - 1`.** `nums[mid] <= nums[hi]` includes the case where mid
  *is* the minimum.
- **Duplicates break it** (LeetCode 154, `[3, 3, 1, 3]`): when `nums[mid] ==
  nums[hi]` you can't tell which part you're in. The fix is `hi -= 1`, and the worst
  case becomes O(n). Say so if asked.
- **Return `nums[lo]`, not `lo`.** The problem wants the value. Tomorrow's problem
  wants the index.

## 🎤 Interview talking points
- *"Everything before the rotation point is bigger than the last element; everything
  after is at most the last element. That's my monotonic predicate."*
- *"I compare with the right end because it handles the unrotated case with no extra
  code."*
- *"With duplicates, `nums[mid] == nums[hi]` is ambiguous, so I'd shrink `hi` by one
  and accept O(n) worst case."*

## 🔗 Transfer
The index this search lands on, 4 in the example, is the **number of times the array
was rotated**. That's tomorrow's EP79 in its entirety: the same function returning `lo`
instead of `nums[lo]`. Then EP80 uses the same "which part am I in?" reasoning to
search for an arbitrary target, where you have to decide which half is **sorted** before
you can decide where to go.

## 📹 Metadata
- **Title:** `Rotated sorted array, compare with the RIGHT end | Binary Search #8`
- **Thumbnail:** `mid > hi ?` (blue block)
- **Short:** the unrotated `[11, 13, 15, 17]` breaking the left-end version live. 45s.
