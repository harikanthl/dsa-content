# EP034 · P04E02 · Minimum Subarray Sum   [Easy]

**Pattern:** Kadane · **Link:** https://www.geeksforgeeks.org/problems/smallest-sum-contiguous-subarray/1

---

## 🎬 Hook
> "Same algorithm, every comparison flipped. This looks like a throwaway episode and it
> isn't — inverting a algorithm you 'know' is the fastest way to find out whether you
> actually understood it or just memorised the shape of the code."

## 📋 Problem, in your words
```
Given an integer array, find the contiguous subarray with the SMALLEST sum,
and return that sum.

Non-empty, as always.
```

## 🔢 The example
```
Input:  nums = [3, -4, 2, -3, -1, 7, -5]
Output: -6
Why:    [-4, 2, -3, -1] sums to -6, and nothing is lower.

Input:  nums = [2, 6, 8, 1, 4]
Output: 1        <- all positive, so the answer is the smallest single element
```

## 🧸 ELI5
> Yesterday you were collecting points and wanted the biggest haul. Today you're
> collecting **penalties** and you want the worst possible run.
>
> The question at each step is the same shape: *is the penalty I'm carrying making this
> worse?* If your running total is **positive**, it's helping — which is exactly what
> you don't want — so drop it and start fresh.
>
> Every "keep the bigger" becomes "keep the smaller." That's the whole edit.

## 🐌 Brute force (say it, don't type it)
Every start, every end. **O(n²).** Identical waste to EP33.

## 💡 The pattern reveal
**Signal:** contiguous · **minimum** sum · negatives present.
**Therefore:** Kadane, mirrored.

**Key insight:** `current` now means *the **smallest** subarray sum ending at this
index*, and the drop rule inverts: abandon the running total when it is **positive**,
because a positive prefix can only pull a sum **up**, and up is the wrong direction.

```python
current = min(x, current + x)      # was max
best    = min(best, current)       # was max
```

Two tokens changed. Nothing else about the reasoning moves.

**The transferable trick — the one worth the episode:** you don't have to write this at
all. Negate the array, run the maximum version, negate the answer:

```python
return -kadane([-x for x in nums])
```

Because `min(S) = −max(−S)`. That identity is worth saying out loud in an interview: it
shows you see the problem as an instance of a family rather than as a new thing. (It
costs O(n) extra space for the copy, or none if you negate as you go.)

## 🔍 Dry run — `[3, -4, 2, -3, -1, 7, -5]`
Seed: `current = best = 3`.

| i | x | `current + x` | `x` | `current` = min | `best` |
|---|---|---|---|---|---|
| 1 | −4 | −1 | −4 | **−4** (start fresh) | −4 |
| 2 | 2 | −2 | 2 | **−2** (extend) | −4 |
| 3 | −3 | −5 | −3 | **−5** (extend) | −5 |
| 4 | −1 | −6 | −1 | **−6** (extend) | **−6** |
| 5 | 7 | 1 | 7 | **1** (extend) | −6 |
| 6 | −5 | −4 | −5 | **−5** (start fresh) | −6 |

Return **−6** — the run `[−4, 2, −3, −1]`.

Row 1 is the mirror of yesterday's key move: the running total was `+3`, which *helps*
a sum go up, so it was dropped. Row 6 does it again from `+1`.

## ✅ Optimal solution
```python
class Solution:
    def smallestSumSubarray(self, nums: List[int]) -> int:
        """Smallest sum of any non-empty contiguous subarray.

        Time:  O(n) · Space: O(1)
        """
        best = current = nums[0]           # seed with a real element

        for x in nums[1:]:
            current = min(x, current + x)  # a POSITIVE prefix is the one to drop
            best = min(best, current)

        return best
```
**Time:** O(n) · **Space:** O(1)

### Or, by symmetry
```python
def smallestSumSubarray(self, nums: List[int]) -> int:
    best = current = -nums[0]
    for x in nums[1:]:
        current = max(-x, current - x)
        best = max(best, current)
    return -best                            # min(S) = -max(-S)
```
Same thing with no new code path. Show it — but write the direct version as the
answer, because it reads better and doesn't make a reviewer check your signs.

## ⚠️ Gotchas
- **Seed with `nums[0]`, not `0`.** On an all-positive array like `[2, 6, 8, 1, 4]`, a
  zero seed returns `0` — the empty subarray again. The answer is `1`. Same bug as
  EP33, mirrored, and it's worth failing on camera a second time precisely because it
  *is* the same bug: seeding with a hopeful value instead of a real one.
- **Flip *both* comparisons.** Changing `current` to `min` but leaving `best` as `max`
  produces something that runs and is nonsense.
- **The drop rule inverts too.** You're now abandoning positive prefixes. If you catch
  yourself writing "drop when negative" out of muscle memory, that's the memorisation
  showing.
- All-positive and all-negative arrays are the two cases to test, and they're the
  opposite way round from yesterday.

## 🎤 Interview talking points
- *"It's Kadane with the comparisons mirrored: `current` is now the smallest sum ending
  here, and I abandon the running total when it's positive."*
- *"Equivalently, `min(S) = −max(−S)` — I could negate the input, run the maximum
  version, and negate the result."* ← the sentence that shows you see the family.
- *"Seeding matters in the opposite direction: an all-positive array is what breaks a
  zero seed here."*

## 🔗 Transfer
This mirror is not busywork — **EP37 (Maximum Absolute Sum) runs both versions at once**
and takes `max(max_sum, |min_sum|)`, and **EP38 (Circular Subarray)** needs the minimum
subarray to compute the wrapping case. Today's four lines get used directly, twice.

## 📹 Metadata
- **Title:** `Minimum Subarray Sum — Kadane in a mirror | Kadane #2`
- **Thumbnail:** `FLIP EVERY MAX` (green block)
- **Short:** `min(S) = -max(-S)` shown as one line of code. 35s.
