# EP038 · P04E06 · Maximum Sum in Circular Array   [Medium]

**Pattern:** Kadane · **Link:** https://leetcode.com/problems/maximum-sum-circular-subarray/

---

## 🎬 Hook
> "The array wraps around, so the best subarray might start near the end and finish near
> the beginning. That sounds like it needs a new algorithm. It needs one line of
> arithmetic: whatever wraps around is just the whole array **minus** something that
> doesn't. So find the worst non-wrapping piece and throw it away."

## 📋 Problem, in your words
```
Given a CIRCULAR integer array (the last element is followed by the first),
find the maximum possible sum of a non-empty subarray.

A subarray may wrap around the end -- but it may not use any element twice.
```

## 🔢 The example
```
Input:  nums = [5, -3, 5]
Output: 10
Why:    take the last 5 and wrap round to the first 5: 5 + 5 = 10.
        The best NON-wrapping answer is the whole array, 7. Wrapping wins.

Input:  nums = [1, -2, 3, -2]
Output: 3        (just [3] -- wrapping doesn't help)

Input:  nums = [-3, -2, -3]
Output: -2       <- the trap. See below.
```

## 🧸 ELI5
> Picture the numbers arranged in a **circle**. Any stretch you pick splits the circle
> into two arcs: the bit you take, and the bit you leave behind.
>
> - If the bit you **take** doesn't cross the join, that's ordinary Kadane.
> - If it **does** cross the join, then the bit you **leave behind** doesn't — it's one
>   continuous piece in the middle.
>
> So a wrapping answer is `total − (the bit left behind)`. To make it as big as
> possible, make the bit left behind as **small** as possible — which is the minimum
> subarray, EP34.
>
> Compute both. Take the better.

```
  [5, -3, 5]        total = 7
   take 5 .. 5 (wrapping)   =  7 - (-3)  = 10
        ^^^^^^ leave behind just the -3
```

## 🐌 Brute force (say it, don't type it)
Duplicate the array (`nums + nums`) and run a sliding window of size ≤ n over it.
**O(n²)** if done naively, O(n) with a deque. It works and it's a legitimate answer to
mention — but it needs care to avoid using an element twice, and the arithmetic trick
below is shorter and cleaner.

## 💡 The pattern reveal
**Signal:** Kadane · the array is **circular**.
**Therefore:** `max(kadane_max, total − kadane_min)` — with one guard.

**Key insight:** every candidate answer falls into exactly one of two cases:

| case | answer is | computed by |
|---|---|---|
| doesn't wrap | a normal subarray | ordinary Kadane (EP33) |
| wraps | `total − (the complementary middle piece)` | `total − ` minimum subarray (EP34) |

The complement of a wrapping subarray is always **contiguous and non-wrapping**, which
is why the minimum-subarray tool applies. Draw the circle and shade the two arcs — it's
obvious the moment you see it and opaque until you do.

**🧨 The guard — the trap of the episode.** If *every* number is negative:

- `kadane_max` is the largest single element, e.g. `−2` for `[−3, −2, −3]`. Correct.
- `kadane_min` is the **whole array** (`−8`), so `total − kadane_min = −8 − (−8) = 0` —
  which corresponds to taking **nothing at all**. The empty subarray. Not allowed.

So: if `kadane_max < 0`, every element is negative, and the answer is simply
`kadane_max`. One `if`, and without it you return `0` on every all-negative input.

## 🔍 Dry run — `[5, -3, 5]`
`total = 7`. Run both Kadanes in one pass, seeded at `nums[0] = 5`.

| i | x | `cur_max` | `best_max` | `cur_min` | `best_min` |
|---|---|---|---|---|---|
| — | 5 | 5 | 5 | 5 | 5 |
| 1 | −3 | max(−3, 2) = **2** | 5 | min(−3, 2) = **−3** | **−3** |
| 2 | 5 | max(5, 7) = **7** | **7** | min(5, 2) = **2** | −3 |

- non-wrapping best = `best_max` = **7**
- wrapping best = `total − best_min` = `7 − (−3)` = **10**
- `best_max = 7 ≥ 0`, so the guard doesn't fire

Answer **`max(7, 10) = 10`** ✓

## 🔍 Dry run — `[-3, -2, -3]` (the guard firing)
`total = −8`.

| i | x | `cur_max` | `best_max` | `cur_min` | `best_min` |
|---|---|---|---|---|---|
| — | −3 | −3 | −3 | −3 | −3 |
| 1 | −2 | max(−2, −5) = **−2** | **−2** | min(−2, −5) = **−5** | −5 |
| 2 | −3 | max(−3, −5) = **−3** | −2 | min(−3, −8) = **−8** | **−8** |

- `total − best_min = −8 − (−8) = 0` ← the empty subarray, illegal
- `best_max = −2 < 0`, so the guard fires → return **−2** ✓

Run this case on camera *without* the guard first and watch it print `0`.

## ✅ Optimal solution
```python
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        """Max sum of a non-empty subarray of a circular array.

        Time:  O(n) — one pass computing both Kadanes.
        Space: O(1).
        """
        total = sum(nums)
        cur_max = best_max = nums[0]
        cur_min = best_min = nums[0]

        for x in nums[1:]:
            cur_max = max(x, cur_max + x)       # EP33
            best_max = max(best_max, cur_max)

            cur_min = min(x, cur_min + x)       # EP34
            best_min = min(best_min, cur_min)

        # All negative: `total - best_min` would be the EMPTY subarray.
        if best_max < 0:
            return best_max

        return max(best_max, total - best_min)
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **The all-negative guard is mandatory.** Without it, `[-3,-2,-3]` returns `0`. This
  is *the* bug on this problem and the reason it's rated Medium rather than Easy.
- **`best_max < 0` is the right test**, not `total < 0` or `max(nums) < 0` — though all
  three coincide here. `best_max < 0` says exactly "no non-empty subarray has a
  non-negative sum," which is the condition you actually mean.
- **Seed both at `nums[0]`.** The empty subarray is not allowed in this problem —
  opposite of EP37. Third episode running where the seed depends on the statement.
- **A wrapping subarray still can't reuse an element**, which is automatic here: the
  complement is a genuine subarray, so `total − complement` uses each element at most
  once.
- **Single element** returns that element, guard or not. Check it.
- If you take the duplicate-the-array route instead, the window must be capped at
  length `n` — without the cap you'll happily sum the array twice.

## 🎤 Interview talking points
- *"Either the answer wraps or it doesn't. If it doesn't, that's ordinary Kadane. If it
  does, its complement is a non-wrapping subarray, so the answer is `total` minus the
  minimum subarray."*
- *"The all-negative case is the trap: `total − min` is the empty subarray there, which
  isn't a legal answer, so I return the plain Kadane maximum when it's negative."* ←
  volunteering this unprompted is exactly what the interviewer is waiting to hear.
- *"Both Kadanes run in the same pass, so it stays O(n) with O(1) space — no need to
  duplicate the array."*

## 🔗 Transfer
This closes Pattern 04. The move — **"the thing I want is the total minus the thing I
don't"** — is genuinely general: it reappears in Pattern 05 (prefix sums are the same
subtraction idea) and in partition-style DP. Next is Pattern 05 (Prefix Sum, EP39–44),
which EP28 and EP37 have already introduced from two different angles.

## 📹 Metadata
- **Title:** `Maximum Sum Circular Subarray — total minus the worst bit | Kadane #6`
- **Thumbnail:** `THROW AWAY THE WORST` (green block)
- **Short:** `[-3,-2,-3]` printing 0 without the guard, then the one-line fix. 50s.
