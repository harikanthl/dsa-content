# EP006 · P01E06 · Triplet Sum Close to Target (3Sum Closest)   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/3sum-closest/

---

## 🎬 Hook
> "Yesterday we found triplets that hit zero exactly. Today there might not *be* an
> exact hit, so we take the closest. It's the same code with one branch swapped, and
> it teaches a move you'll use for the rest of your career: track the best-so-far."

## 📋 Problem, in your words
```
Given an array and a target, find three numbers whose sum is CLOSEST to the target.
Return the sum itself (not the indices, not the triplet).
Exactly one answer is guaranteed.
```

## 🔢 The example
```
Input:  nums = [-1, 2, 1, -4],  target = 1
Sorted: [-4, -1, 1, 2]
Output: 2
Why:    (-1) + 1 + 2 = 2. Distance from target is |2 - 1| = 1.
        No triplet gets closer.
```

## 🧸 ELI5
> You're throwing darts and aiming for a specific number. You probably won't hit it
> dead on, so you keep a note of *the best throw so far*, and every new throw you
> compare against that note. At the end, the note is your answer.
>
> The walking-two-fingers part is identical to yesterday. The only new idea is
> carrying the note.

## 🐌 Brute force (say it, don't type it)
Three nested loops tracking the minimum distance, **O(n³)**. Correct, too slow.

## 💡 The pattern reveal
**Signal:** *triplet* + *closest to* (not *equal to*).
**Therefore:** identical skeleton to 3Sum, sort, fix one, converge two, with the
equality branch replaced by a **best-so-far** comparison.

**Key insight:** the pointer-movement rule doesn't change at all. `total < target`
still means "I need a bigger sum, move `lo` right." Closeness doesn't affect *where
you walk*; it only affects *what you remember while walking*.

## 🔍 Dry run: sorted `[-4, -1, 1, 2]`, target 1
| i | anchor | lo | hi | total | \|total−1\| | best |
|---|---|---|---|---|---|---|
| 0 | −4 | 1 | 3 | −4−1+2 = −3 | 4 | −3 |
| 0 | −4 | 2 | 3 | −4+1+2 = −1 | 2 | −1 |
| 1 | −1 | 2 | 3 | −1+1+2 = **2** | **1** | **2** ✓ |

Answer: `2`.

## ✅ Optimal solution
```python
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        best = nums[0] + nums[1] + nums[2]            # seed with a REAL triplet

        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]

                if abs(total - target) < abs(best - target):
                    best = total

                if total == target:                    # can't beat exact, bail out
                    return total
                if total < target:
                    lo += 1
                else:
                    hi -= 1

        return best
```
**Time:** O(n²) · **Space:** O(1) beyond the sort

## ⚠️ Gotchas
- **Seed `best` with an actual triplet**, `nums[0]+nums[1]+nums[2]`. Seeding with
  `0`, `float('inf')` or `None` is the classic bug: `inf` isn't a reachable sum, and
  `0` may be closer to target than any real triplet, so you return a sum that doesn't
  exist in the array. Say this out loud, it's a subtle, very common wrong answer.
- **Early return on exact.** Distance 0 is unbeatable. It's a small optimisation but
  interviewers notice you noticed.
- **No duplicate-skipping needed.** Unlike 3Sum, you return a *number*, not a list of
  triplets, so a duplicate triplet is harmless, it just recomputes the same distance.
  Explaining *why* you dropped yesterday's de-dup logic shows you understand it rather
  than having memorised it.
- Use `abs()` on both sides. Comparing raw `total - target` breaks when one is
  negative.

## 🎤 Interview talking points
- *"The traversal is unchanged from 3Sum, I'm only changing what I record. Optimising
  a target becomes tracking a running best."*
- *"I seed the best with a real triplet so the answer is always achievable."*

## 🔗 Transfer
"Track the best-so-far while you scan" is the single most reused idea in all of DSA.
It's literally Kadane's algorithm (EP 39–44), it's the max in Container With Most
Water, it's the diameter accumulator in Tree problems (EP 142). Name it on camera as
a **named technique**, not a one-off.

## 📹 Metadata
- **Title:** `3Sum Closest, same code, one branch changed | Two Pointers #6`
- **Thumbnail:** `TRACK THE BEST` (blue block)
- **Short:** The seeding bug, "why `best = 0` gives you a wrong answer."
