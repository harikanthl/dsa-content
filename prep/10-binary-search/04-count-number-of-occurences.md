# EP074 · P10E04 · Count Number of Occurrences   [Easy]

**Pattern:** Binary Search · **Link:** https://www.geeksforgeeks.org/problems/number-of-occurrence2259/1

---

## 🎬 Hook
> "How many times does 2 appear in a sorted array? One line. `lower_bound(3) -
> lower_bound(2)`. No loop, no counter, no `if found`. When the target is missing, the
> two searches land in the same place and the answer is zero on its own."

## 📋 Problem, in your words
```
Given a sorted array and a target, return how many times target appears.

  - if it doesn't appear, return 0
  - expected O(log n)
```

## 🔢 The example
```
Input:  arr = [1, 1, 2, 2, 2, 2, 3], target = 2
Output: 4

Input:  arr = [1, 1, 2, 2, 2, 2, 3], target = 4
Output: 0              <- both searches return 7; 7 - 7 = 0

Input:  arr = [8, 9, 10, 12, 12, 12], target = 12
Output: 3
```
All three are GfG's own examples.

## 🧸 ELI5
> Books on a shelf sorted by page count. How many books have exactly 200 pages? Put a
> bookmark where the first 200-page book **would** go, and another where the first
> 201-page book **would** go. Count the books between the bookmarks.
>
> ```
> arr:    1   1   2   2   2   2   3
> index:  0   1   2   3   4   5   6   7
>                 ^ bookmark for 2      (index 2)
>                                 ^ bookmark for 3   (index 6)
> count = 6 - 2 = 4
> ```
>
> No 200-page books at all? Both bookmarks go in the same gap. Zero books between them.

## 🐌 Brute force (say it, don't type it)
`arr.count(target)` or a loop: **O(n)**. Also O(n): find the target with one binary
search and walk outward counting, because the walk is as long as the run of copies.

## 💡 The pattern reveal
**Signal:** "sorted" · "count occurrences".
**Therefore:** Shape A, the difference of two lower bounds.

**Key insight:** in a sorted array every copy of `x` is contiguous, and a contiguous
block is fully described by where it starts and where the next value starts.

```
count(x) = lower_bound(x + 1) - lower_bound(x)
```

This is EP73 without the `- 1` and without the presence check. The subtraction makes
the "absent" case correct automatically: if `x` isn't there, both calls return the same
insertion point.

## 🔍 Dry run: `arr = [1, 1, 2, 2, 2, 2, 3]`, `target = 2`

**`lower_bound(2)`**

| step | lo | hi | mid | arr[mid] | action |
|---|---|---|---|---|---|
| 1 | 0 | 7 | 3 | 2 (>= 2) | `hi = 3` |
| 2 | 0 | 3 | 1 | 1 (< 2) | `lo = 2` |
| 3 | 2 | 3 | 2 | 2 (>= 2) | `hi = 2` |
| - | 2 | 2 | | | → **2** |

**`lower_bound(3)`**

| step | lo | hi | mid | arr[mid] | action |
|---|---|---|---|---|---|
| 1 | 0 | 7 | 3 | 2 (< 3) | `lo = 4` |
| 2 | 4 | 7 | 5 | 2 (< 3) | `lo = 6` |
| 3 | 6 | 7 | 6 | 3 (>= 3) | `hi = 6` |
| - | 6 | 6 | | | → **6** |

`6 - 2 =` **4** ✓

**Target 4:** every element is `< 4` and every element is `< 5`, so both calls walk
`lo` up to 7. `7 - 7 = 0` ✓. No special case was written for it.

## ✅ Optimal solution
```python
class Solution:
    def countFreq(self, arr, target):
        """How many times target appears in a sorted array.

        Time:  O(log n), two lower_bound calls.
        Space: O(1).
        """
        # every copy of target sits in [lower_bound(target), lower_bound(target + 1))
        return self.lower_bound(arr, target + 1) - self.lower_bound(arr, target)

    def lower_bound(self, arr, x):
        """First index i with arr[i] >= x, or len(arr)."""
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **No `if found` needed.** Absent target → both bounds equal → 0. Adding a check is
  noise and suggests you don't trust the subtraction.
- **Half-open interval, so no `+ 1`.** `[start, end)` has `end - start` elements.
  EP73's `last - first + 1` is the same number written with a closed interval. Mixing
  them gives off-by-one counts.
- **Find-and-walk is O(n)** for the same reason as EP73: all-copies arrays.
- **Python has this built in:** `bisect_right(arr, x) - bisect_left(arr, x)`. Name it
  after writing your own, so they see you know both.

## 🎤 Interview talking points
- *"Copies of x are contiguous in a sorted array, so the count is the width of that
  block: lower bound of x plus one, minus lower bound of x."*
- *"When x is missing, both searches return the same insertion point and the count is
  zero with no special case."*
- *"That's `bisect_right - bisect_left` in Python's standard library."*

## 🔗 Transfer
Shape A is nearly done: every question so far has been "where does x go?". Tomorrow's
EP75 removes the one thing the template takes for granted, **`hi = len(arr)`**. With no
length, you have to find the right edge before you can search. After that, EP76 moves
to Shape B, where the array isn't sorted at all and the monotonic thing is a
comparison between neighbours.

## 📹 Metadata
- **Title:** `Count occurrences in one line, no if-statement | Binary Search #4`
- **Thumbnail:** `lb(3) − lb(2)` (blue block)
- **Short:** the two bookmarks on the shelf, then target 4 giving 7 − 7 = 0. 30s.
