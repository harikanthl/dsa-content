# EP076 · P10E06 · Peak Index in a Mountain Array   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/peak-index-in-a-mountain-array/

---

## 🎬 Hook
> "This array isn't sorted. It goes up, then down. And binary search still finds the
> top in O(log n). Because binary search never needed a sorted array. It needed **a
> question whose answer flips once**, and 'am I still going uphill?' flips exactly
> once, at the peak."

## 📋 Problem, in your words
```
A mountain array strictly increases, reaches one peak, then strictly
decreases. It has at least 3 elements.

Return the INDEX of the peak. Must be O(log n).
```

## 🔢 The example
```
Input:  arr = [1, 3, 5, 7, 6, 4, 2]
Output: 3              <- arr[3] = 7

Input:  arr = [0, 10, 5, 2]
Output: 1

Input:  arr = [0, 1, 0]
Output: 1
```

## 🧸 ELI5
> You're hiking in thick fog. You can only see the ground one step ahead. You want the
> summit. At any spot, look one step forward:
>
> - ground goes **up**? The summit is ahead of you.
> - ground goes **down**? You're on the far side, or standing on the summit. It's here
>   or behind you.
>
> ```
> heights:  1   3   5   7   6   4   2
> uphill?:  Y   Y   Y   N   N   N   -
>                       ^ first N is the peak
> ```
>
> Now teleport to the middle of the trail instead of walking. One look forward tells
> you which half the summit is in.

## 🐌 Brute force (say it, don't type it)
Scan for the first `i` where `arr[i] > arr[i + 1]`, or just `arr.index(max(arr))`:
**O(n)**. Walking the whole uphill side when every single step already tells you which
direction the peak is in.

## 💡 The pattern reveal
**Signal:** "mountain" · "peak" · "O(log n)" on an array that is not sorted.
**Therefore:** Shape B, search on a condition.

**Key insight:** the predicate `arr[mid] < arr[mid + 1]` ("still climbing") is
`True, True, True, False, False, False`. The peak is the **first False**. That's
exactly what the template finds: replace "`nums[mid] < target`" with "`arr[mid] <
arr[mid + 1]`" and nothing else changes.

| predicate at mid | meaning | action |
|---|---|---|
| `arr[mid] < arr[mid + 1]` | uphill: peak is strictly to the right | `lo = mid + 1` |
| otherwise | downhill or at the peak: peak is `mid` or left | `hi = mid` |

One change from EP71: `hi` starts at `len(arr) - 1`, not `len(arr)`. The peak is always
a real index, and `mid + 1` must stay in bounds.

## 🔍 Dry run: `arr = [1, 3, 5, 7, 6, 4, 2]`

| step | lo | hi | mid | arr[mid] | arr[mid+1] | climbing? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 7 | 6 | no | `hi = 3` |
| 2 | 0 | 3 | 1 | 3 | 5 | yes | `lo = 2` |
| 3 | 2 | 3 | 2 | 5 | 7 | yes | `lo = 3` |
| 4 | 3 | 3 | - | | | | return **3** ✓ |

Step 1 landed **on** the peak and didn't return. It set `hi = 3` and then proved,
in steps 2 and 3, that nothing left of it is higher. Same "keep going after a hit" as
EP71 step 3.

## ✅ Optimal solution
```python
class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        """Index of the single peak in a strictly up-then-down array.

        Time:  O(log n), the range halves each step.
        Space: O(1).
        """
        lo, hi = 0, len(arr) - 1        # the peak is a real index, so hi = n - 1
        while lo < hi:
            mid = (lo + hi) // 2        # mid < hi, so mid + 1 is always in bounds
            if arr[mid] < arr[mid + 1]:
                lo = mid + 1            # still climbing: peak is to the right
            else:
                hi = mid                # going down (or at the top): peak is here or left
        return lo
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **`hi = len(arr) - 1`, not `len(arr)`.** With `hi = n`, `mid` can be `n - 1` and
  `arr[mid + 1]` is out of range. With `hi = n - 1`, `mid < hi` guarantees
  `mid + 1 <= hi`.
- **Compare with the neighbour, not with a target.** There is no target. The thing you
  search for is a *change* in the array's direction.
- **`hi = mid`, not `mid - 1`.** When the ground goes down, `mid` might be the peak
  itself (step 1 above). Throwing it away loses the answer.
- **Don't write three cases** (`mid` is peak / left / right) with an early return. It
  works, but it's the closed-interval style, needs `mid - 1` bounds checks, and is
  exactly where off-by-ones come from. Two branches.
- **`arr.index(max(arr))` is O(n).** It's fine as the brute force; it fails the
  "must be O(log n)" requirement.

## 🎤 Interview talking points
- *"The array isn't sorted, but 'is `arr[mid]` less than `arr[mid + 1]`' is true up to
  the peak and false after. The peak is the first false."*
- *"So it's the same lower-bound template with a different predicate."*
- *"I set `hi` to n minus 1 so `mid + 1` is always a valid index."*
- *"Binary search needs a monotonic predicate, not a sorted array. This is the proof."*

## 🔗 Transfer
Tomorrow's EP77, Find Peak Element, removes the guarantee that there's exactly one
peak. The array can wiggle up and down any number of times. Astonishingly, the code is
**character for character the same**, and the episode is about why it's still correct.
EP78 then keeps the "compare to a neighbour" idea but compares `mid` to `arr[hi]`
instead, to find the break in a rotated array.

## 📹 Metadata
- **Title:** `Binary search on an UNSORTED array, the mountain | Binary Search #6`
- **Thumbnail:** `uphill?` (blue block) over a mountain sketch
- **Short:** the foggy hike, "look one step ahead", then the Y Y Y N N N row. 40s.
