# EP071 · P10E01 · Binary Search   [Easy]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/binary-search/

---

## 🎬 Hook
> "Everyone thinks they can write binary search. When Jon Bentley asked professional
> programmers to, about 90% of them had a bug. Not the idea, the **boundaries**: `<` or `<=`,
> `mid` or `mid - 1`. Today I pick one template, prove it can't loop forever and can't
> skip the answer, and then I never think about boundaries again for 22 episodes."

## 📋 Problem, in your words
```
Given a sorted array of DISTINCT integers and a target,
return the index of target, or -1 if it isn't there.

  - must run in O(log n)
```

## 🔢 The example
```
Input:  nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4

Input:  nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1            <- lower_bound lands on index 2 (value 3), and 3 != 2

Input:  nums = [5], target = 5   -> 0
```

## 🧸 ELI5
> You're looking up "mango" in a paper dictionary. You don't start at "aardvark". You
> open it roughly in the middle, see "lemon", and know mango is **after** this page.
> The whole first half of the book is gone with one look. Open the middle of what's
> left, and again, and again.
>
> ```
> 1000 pages -> 500 -> 250 -> 125 -> 63 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1
> ten looks for a thousand pages
> ```
>
> The only rule you need: **never throw away a page that might be the one.**

## 🐌 Brute force (say it, don't type it)
Walk left to right and compare each element to the target: **O(n)**. It ignores the
one fact the problem hands you, that the array is sorted. Every comparison with a
sorted array tells you about **everything** on one side of it, and the linear scan
throws that information away.

## 💡 The pattern reveal
**Signal:** "sorted array" · "O(log n)".
**Therefore:** Shape A from the pattern card, `lower_bound`.

**Key insight:** don't search for "equal to target". Search for **the first index whose
value is `>= target`**. That question is no, no, no, yes, yes, yes across the array, so
it flips exactly once, and binary search finds flip points. Then check whether the
thing you landed on is the target.

The template, half-open, learned once for the whole pattern:

| piece | code | why |
|---|---|---|
| range | `lo, hi = 0, len(nums)` | `hi` is one past the end: "not found" is a legal answer |
| loop | `while lo < hi` | stops when one candidate is left |
| too small | `lo = mid + 1` | `mid` can't be the answer, drop it |
| big enough | `hi = mid` | `mid` **might** be the answer, keep it |
| answer | `lo` | first index with `nums[i] >= target` |

## 🔍 Dry run: `nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`

| step | lo | hi | mid | nums[mid] | compare | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 5 | 5 < 9 | `lo = 4` |
| 2 | 4 | 6 | 5 | 12 | 12 >= 9 | `hi = 5` |
| 3 | 4 | 5 | 4 | 9 | 9 >= 9 | `hi = 4` |
| 4 | 4 | 4 | - | - | `lo == hi`, stop | `nums[4] == 9` → return **4** ✓ |

Step 3 is the one to say out loud: `nums[mid]` **equals** the target and we don't
return. We set `hi = mid` and keep going. The loop always runs to the end; the check
happens once, after it.

Target 2 on the same array: `mid=3 (5) → hi=3`, `mid=1 (0) → lo=2`, `mid=2 (3) → hi=2`.
Lands on index 2, `nums[2] = 3 != 2` → **-1** ✓.

## ✅ Optimal solution
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Index of target in a sorted array of distinct ints, or -1.

        Time:  O(log n), the range [lo, hi) halves every iteration.
        Space: O(1).
        """
        lo, hi = 0, len(nums)           # answer is in [lo, hi]; hi == n means "past the end"
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1            # mid is too small; it and everything left of it are out
            else:
                hi = mid                # mid could be the answer; keep it in range

        # lo is the first index with nums[lo] >= target (or n if none)
        if lo < len(nums) and nums[lo] == target:
            return lo
        return -1
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **`hi = mid`, never `hi = mid - 1`, in this template.** `mid` passed the `>=` test,
  so it might be the answer. `mid - 1` can throw it away.
- **`lo < len(nums)` before `nums[lo]`.** If the target is bigger than everything, `lo`
  ends at `n` and `nums[n]` is an `IndexError`. Test `target = 13`.
- **Never mix the two styles.** `lo < hi` goes with `hi = mid`. `lo <= hi` goes with
  `hi = mid - 1` and an early `return`. Mixing gives an infinite loop or a skipped
  answer. Pick this one for life.
- **`(lo + hi) // 2` is fine in Python.** In Java or C++ `lo + hi` can overflow; there
  you write `lo + (hi - lo) // 2`. Mention it, it's a classic follow-up.
- **Why it terminates:** `mid < hi` always, so `hi = mid` strictly shrinks the range;
  `lo = mid + 1` strictly grows `lo`. The range loses at least one element per step.

## 🎤 Interview talking points
- *"I search for the first index with a value `>= target`, then check equality once at
  the end. That one template handles every Shape A problem."*
- *"The invariant is 'the answer is in `[lo, hi]`'. Both branches keep it, and the
  range shrinks every step, so it terminates with one candidate."*
- *"`hi` starts at `n`, not `n - 1`, so 'bigger than everything' is representable."*
- *"In a fixed-width language I'd write `lo + (hi - lo) // 2` to avoid overflow."*
- *"If the array weren't sorted there'd be no monotonic question to ask, and I'd use a
  hash set or a scan."*

## 🔗 Transfer
This template is the whole of Shape A. Tomorrow, EP72, keeps it character for
character and changes only what you do with `lo`: return it (ceiling), or search for
`x + 1` instead (first element strictly greater). EP73 and EP74 are two calls to it.
By EP81 the same eight lines will search over **eating speeds**, not array indices.

## 📹 Metadata
- **Title:** `Binary Search, the template you never debug again | Binary Search #1`
- **Thumbnail:** `lo < hi` (blue block)
- **Short:** step 3, `nums[mid] == target` and the loop does NOT return. 40s.
