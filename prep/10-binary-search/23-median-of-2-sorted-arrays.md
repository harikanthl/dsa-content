# EP093 · P10E23 · Median of Two Sorted Arrays   [Hard]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/median-of-two-sorted-arrays/

---

## 🎬 Hook
> "The most famous Hard on LeetCode, and the trick is to stop looking for the median.
> Look for a **cut**: split both arrays so the left pieces together hold exactly half
> the numbers, and every number on the left is at most every number on the right. Pick
> the cut in the shorter array, and the other cut is forced. Now it's binary search on
> one integer."

## 📋 Problem, in your words
```
Two sorted arrays nums1 (length m) and nums2 (length n).
Return the median of all m + n numbers together.

Required: O(log(m + n)). Either array may be empty (not both).
```

## 🔢 The example
```
Input:  nums1 = [1, 3], nums2 = [2]          -> 2.0
Input:  nums1 = [1, 2], nums2 = [3, 4]       -> 2.5   ((2 + 3) / 2)

The one we'll trace:
nums1 = [1, 3, 8, 9, 15]
nums2 = [7, 11, 18, 19, 21, 25]
merged: 1 3 7 8 9 11 15 18 19 21 25   (11 numbers)
median: the 6th -> 11
```

## 🧸 ELI5
> Two sorted queues of kids, and you want the middle kid of everyone. Instead of merging
> the queues, put **one rope** across each queue. Everyone in front of the ropes is the
> "short half", everyone behind is the "tall half".
>
> ```
> queue A:   1   3   8   9 |  15
> queue B:   7  11 |  18  19  21  25
>            left half: 1 3 8 9 7 11  (6 kids)   right half: 15 18 19 21 25
> ```
>
> The ropes are in the right place when **the tallest kid in front of either rope is no
> taller than the shortest kid behind either rope**: 9 ≤ 18 and 11 ≤ 15. ✓ Then the
> middle kid is the tallest of the front: `max(9, 11) = 11`.
>
> You only choose where rope A goes. Rope B has to go wherever makes the front half
> exactly 6 kids. So it's a search over one number, the rope position in A.

## 🐌 Brute force (say it, don't type it)
Merge the two arrays and take the middle: **O(m + n)** time and space. Or walk two
pointers to the middle without storing: **O(m + n)** time, O(1) space. Both are fine in
real life; the problem demands log. There's also a "find the kth of two arrays"
recursion at **O(log(m + n))**, correct and harder to get right on a whiteboard.

## 💡 The pattern reveal
**Signal:** "two **sorted** arrays" · "median" · "O(log(m + n))".
**Therefore:** Shape D / C, binary search the **cut position** in the shorter array.

Let `i` = how many elements of `nums1` go left, `j` = how many of `nums2`. The left
half must hold `half = (m + n + 1) // 2` elements, so **`j = half - i`**. Only `i` is
free, and it ranges over `[0, m]`.

Name the four numbers around the two cuts:

```
nums1:  ... a_left | a_right ...        a_left = nums1[i-1], a_right = nums1[i]
nums2:  ... b_left | b_right ...        b_left = nums2[j-1], b_right = nums2[j]
```

Each array is already sorted, so `a_left <= a_right` and `b_left <= b_right` for free.
The cut is valid when the **cross** comparisons hold too:

| check | if it fails | move |
|---|---|---|
| `a_left <= b_right` | too much of `nums1` on the left | `hi = i - 1` (take fewer from nums1) |
| `b_left <= a_right` | too little of `nums1` on the left | `lo = i + 1` (take more) |

When both hold: odd total → `max(a_left, b_left)`; even total →
`(max(a_left, b_left) + min(a_right, b_right)) / 2`.

**Edges:** a cut at the very start or end has no neighbour on one side. Use `-inf` for
a missing left and `+inf` for a missing right, and the checks just work.

## 🔍 Dry run: `nums1 = [1, 3, 8, 9, 15]` (m = 5), `nums2 = [7, 11, 18, 19, 21, 25]` (n = 6)
`nums1` is already the shorter. `half = (5 + 6 + 1) // 2 = 6`. Search `i` in `[0, 5]`.

| step | lo | hi | i | j = 6 − i | a_left | a_right | b_left | b_right | checks | action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 4 | 3 | 8 | 19 | 21 | `3 <= 21` ✓, `19 <= 8` ✗ | too few from nums1: `lo = 3` |
| 2 | 3 | 5 | 4 | 2 | 9 | 15 | 11 | 18 | `9 <= 18` ✓, `11 <= 15` ✓ | **valid** |

Total 11 is odd → median = `max(9, 11)` = **11** ✓

```
step 1:  [1 3 | 8 9 15]     [7 11 18 19 | 21 25]     19 on the left > 8 on the right: rope A too far left
step 2:  [1 3 8 9 | 15]     [7 11 | 18 19 21 25]     every left <= every right
```

## ✅ Optimal solution
```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """Median of two sorted arrays by binary searching the cut in the shorter one.

        Time:  O(log min(m, n)), one binary search over cut positions in the shorter.
        Space: O(1).
        """
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1     # search the shorter: j = half - i stays in range
        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2             # left half size; the extra one goes left when odd

        lo, hi = 0, m                       # i = how many of nums1 go to the left half
        while lo <= hi:
            i = (lo + hi) // 2
            j = half - i
            a_left  = nums1[i - 1] if i > 0 else float('-inf')
            a_right = nums1[i]     if i < m else float('inf')
            b_left  = nums2[j - 1] if j > 0 else float('-inf')
            b_right = nums2[j]     if j < n else float('inf')

            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                hi = i - 1                  # took too many from nums1
            else:
                lo = i + 1                  # took too few from nums1
```
**Time:** O(log min(m, n)) · **Space:** O(1)

## ⚠️ Gotchas
- **Search the shorter array.** If `nums1` is longer, `j = half - i` can go negative or
  past `n`, and `nums2[j - 1]` indexes garbage (or wraps around with Python's negative
  indices, silently). The swap on line one prevents it.
- **`half = (m + n + 1) // 2`.** The `+ 1` puts the extra element on the left for odd
  totals, so the median is always `max` of the left. Without it you'd need `min` of the
  right for odd totals: pick one convention and keep it.
- **`-inf` / `+inf` at the edges.** `i = 0` means nothing from `nums1` on the left;
  there's no `a_left`, and `-inf` makes `a_left <= b_right` automatically true.
- **Closed loop, `lo <= hi`, `hi = i - 1`.** This is the pattern card's second style,
  and it's safe here because the answer is returned from inside the loop. A valid cut
  always exists, so the loop never falls through.
- **Even totals average two numbers.** `/ 2`, not `// 2`: `[1, 2]` and `[3, 4]` is 2.5,
  and integer division would say 2.

## 🎤 Interview talking points
- *"I don't look for the median directly. I look for a cut that splits all m + n
  numbers into a left half and a right half, with everything left ≤ everything right."*
- *"Choosing `i` from the shorter array forces `j = half - i`, so it's a binary search
  on one integer."*
- *"The cut is valid when `a_left <= b_right` and `b_left <= a_right`; each failure
  tells me which way to move `i`."* ← the monotonic predicate, say it.
- *"O(log min(m, n)), which is within the required O(log(m + n))."*
- *"If they'd accept O(m + n), I'd merge with two pointers and stop halfway."*

## 🔗 Transfer
The finale of the pattern, and still the same idea as EP71: a question that flips once
("is `i` too small?"), halved until it's answered. Shape C searched capacities (EP86)
and values (EP91); here it searches a **cut**. The two-heaps episodes in the Heap
pattern, **EP109 Find Median from Data Stream**, solve the median when numbers arrive
one at a time instead of in sorted arrays: the same left-half / right-half picture, kept
live with two heaps.

## 📹 Metadata
- **Title:** `Median of Two Sorted Arrays, search the cut not the median | Binary Search #23`
- **Thumbnail:** `FIND THE CUT` (red block)
- **Short:** the two ropes moving from step 1 to step 2, and 11 dropping out as the median. 50s.
