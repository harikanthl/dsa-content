# EP077 · P10E07 · Find Peak Element   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/find-peak-element/

---

## 🎬 Hook
> "Yesterday there was one mountain. Today it's a whole mountain **range**: up, down,
> up, down, as many peaks as it likes. I'm going to paste yesterday's code, not change
> a character, and it passes. The interesting part isn't the code. It's the one-line
> argument for why it can't get lost."

## 📋 Problem, in your words
```
Given an array where no two neighbours are equal, return the index of
ANY peak: an element strictly greater than its neighbours.

  - pretend nums[-1] and nums[n] are -infinity (the edges are cliffs)
  - any peak is accepted if there are several
  - must be O(log n)
```

## 🔢 The example
```
Input:  nums = [1, 2, 3, 1]
Output: 2              <- 3 is bigger than 2 and 1

Input:  nums = [1, 2, 1, 3, 5, 6, 4]
Output: 5              <- 6. Index 1 (value 2) is also a peak; either is accepted.

Input:  nums = [5, 4, 3]  -> 0   (the left edge counts, nums[-1] is -infinity)
```

## 🧸 ELI5
> You're dropped somewhere in a hilly range, in fog, with a cliff on both ends of the
> map. You don't need the **highest** peak, just **a** peak. The rule:
>
> **walk uphill.**
>
> If the ground rises to your right, go right. You're going up, and at worst you'll hit
> the right cliff, but the cliff is a drop, so the last spot before it is a peak. You
> can't go uphill forever on a finite map. **Uphill always ends at a peak.**
>
> ```
> nums:     1   2   1   3   5   6   4
>                   standing at 3, ground rises ->
>                   so there's a peak somewhere to the right, guaranteed
> ```

## 🐌 Brute force (say it, don't type it)
Scan for the first `i` with `nums[i] > nums[i + 1]` (or the last index if none):
**O(n)**. Or `nums.index(max(nums))`, also O(n). The global max is always a peak, but
you don't need the global max, just any peak, and that's what makes O(log n) possible.

## 💡 The pattern reveal
**Signal:** "peak" · "any peak is fine" · "O(log n)" · edges are -infinity.
**Therefore:** Shape B, EP76's exact code.

**Key insight:** the array as a whole is **not** monotonic, so the predicate isn't
globally "True...True False...False". But binary search doesn't need that. It needs,
at every step, **a guarantee that the half you keep contains an answer**:

| at mid | guarantee | keep |
|---|---|---|
| `nums[mid] < nums[mid + 1]` | walking right from `mid + 1` goes uphill until it can't; the right edge is a cliff. So `[mid + 1, hi]` contains a peak | `lo = mid + 1` |
| `nums[mid] > nums[mid + 1]` | same argument walking left from `mid`. `[lo, mid]` contains a peak | `hi = mid` |

The invariant is "**`[lo, hi]` contains a peak**", and both branches preserve it.
That's the real lesson: you can binary search whenever you can always tell which half
still holds an answer.

## 🔍 Dry run: `nums = [1, 2, 1, 3, 5, 6, 4]`

| step | lo | hi | mid | nums[mid] | nums[mid+1] | rising? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 3 | 5 | yes | `lo = 4` |
| 2 | 4 | 6 | 5 | 6 | 4 | no | `hi = 5` |
| 3 | 4 | 5 | 4 | 5 | 6 | yes | `lo = 5` |
| 4 | 5 | 5 | - | | | | return **5** ✓ (6 > 5 and 6 > 4) |

Step 1 threw away the left half, **including the peak at index 1**. That's fine: we
only promised to keep *a* peak, and the right half has one. Say this on camera, it's
the moment people get uncomfortable.

## ✅ Optimal solution
```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        """Index of any element strictly greater than both neighbours.

        Time:  O(log n), the range halves each step.
        Space: O(1).
        """
        lo, hi = 0, len(nums) - 1
        # invariant: [lo, hi] always contains a peak (edges count as -infinity)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1            # uphill to the right: a peak lies that way
            else:
                hi = mid                # downhill to the right: mid or something left is a peak
        return lo
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **"The array isn't sorted, so binary search is invalid."** This is the objection
  you'll hear. Answer with the invariant: the kept half always contains a peak.
- **No equal neighbours is essential.** `nums[i] != nums[i + 1]` is in the
  constraints. With plateaus (`[1, 2, 2, 2, 1]`) the `else` branch can't tell up from
  flat, and the guarantee breaks. Mention it.
- **The -infinity edges are why `lo` is always a peak at the end.** A single-element
  array returns 0. A strictly decreasing array returns 0. A strictly increasing one
  returns `n - 1`.
- **You won't necessarily get the highest peak.** In the example, index 5 (value 6) is
  returned, not because it's the tallest but because the search went right first.
- **`hi = n - 1`**, same reason as EP76: `mid + 1` must be in bounds.

## 🎤 Interview talking points
- *"If the next element is bigger, walking uphill from there must end at a peak before
  or at the right edge, because the edge counts as minus infinity. So I can discard the
  left half."*
- *"The invariant is 'there's a peak in `[lo, hi]`', not 'the array is sorted'."*
- *"It's the exact code from Peak Index in a Mountain Array. The mountain version is
  the special case with one peak."*
- *"It relies on adjacent elements being different; with plateaus it's O(n) worst
  case."*

## 🔗 Transfer
EP76 and EP77 compared `mid` to its **neighbour**. EP78, Find Minimum in a Rotated
Sorted Array, compares `mid` to the **right end** of the range, `nums[hi]`, which asks a
different monotonic question: "am I in the part that got rotated to the front?" Same
two-branch template, third predicate.

## 📹 Metadata
- **Title:** `Find Peak Element, same code, many peaks, still O(log n) | Binary Search #7`
- **Thumbnail:** `walk uphill` (blue block)
- **Short:** step 1 throwing away a real peak, and why that's fine. 45s.
