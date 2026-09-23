# EP022 · P03E02 · Smallest Subarray with a given sum   [Easy]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/minimum-size-subarray-sum/

---

## 🎬 Hook
> "Yesterday the window was a fixed size and you just dragged it along. Today nobody
> tells you how big it is, you have to grow it and shrink it yourself. That one
> change is what makes this pattern worth twelve episodes, and there are exactly two
> rules to get right."

## 📋 Problem, in your words
```
Given an array of POSITIVE integers and a target,
find the length of the SMALLEST contiguous subarray whose sum is >= target.

Return 0 if no such subarray exists.
```

## 🔢 The example
```
Input:  nums = [2, 1, 5, 2, 3, 2],  target = 7
Output: 2
Why:    [5, 2] sums to 7 -- and no single element reaches 7,
        so 2 is the smallest possible length.

Input:  nums = [2, 1, 5, 2, 8],  target = 7
Output: 1        ([8] on its own clears the bar)

Input:  nums = [1, 1, 1],  target = 7
Output: 0        (impossible)
```

## 🧸 ELI5
> You're filling a shopping bag and you need at least £7 of stuff, but you want to
> carry as **few items** as possible.
>
> Keep adding items on the right until the bag is worth £7 or more. Now try to make it
> lighter: drop items from the **left**, one at a time, for as long as the bag is
> *still* worth £7. The moment it drops below, stop, you've found the smallest bag
> ending at this point. Write down its size, then carry on adding.
>
> **You measure the bag while it's still good, just before you break it.** That's the
> rule that separates "shortest" problems from "longest" ones.

## 🐌 Brute force (say it, don't type it)
Every start index, extending until the sum clears target.

```python
best = inf
for i in range(len(nums)):
    total = 0
    for j in range(i, len(nums)):
        total += nums[j]
        if total >= target:
            best = min(best, j - i + 1)
            break
```

**O(n²) time.** The waste: when you move the start from `i` to `i+1`, you throw away
everything you learned and start summing from zero, even though the new window is the
old one minus a single element.

## 💡 The pattern reveal
**Signal:** contiguous · **smallest** · a condition that gets *easier* as the window
grows.
**Therefore:** Sliding Window, Shape C, the shrinking window.

**Key insight:** because all the numbers are **positive**, growing the window can only
increase the sum and shrinking it can only decrease it. That monotonicity is what lets
the left edge move forward and never come back. Without it, if negatives were allowed,
a longer window might have a *smaller* sum, and the whole method collapses.

**The two Shape C rules, which are the mirror of tomorrow's:**

| | Shortest (today) | Longest (EP23 onward) |
|---|---|---|
| shrink `while` | **valid** | **not valid** |
| record the answer | **inside** the loop | **after** the loop |

## 🔍 Dry run: `[2, 1, 5, 2, 3, 2]`, target = 7
| hi | value | sum | window | action | best |
|---|---|---|---|---|---|
| 0 | 2 | 2 | `[2]` | under target | ∞ |
| 1 | 1 | 3 | `[2,1]` | under target | ∞ |
| 2 | 5 | 8 | `[2,1,5]` | ≥ 7 → record len 3, drop `2` → sum 6 | 3 |
| 3 | 2 | 8 | `[1,5,2]` | ≥ 7 → record len 3, drop `1` → sum 7 | 3 |
| | | 7 | `[5,2]` | still ≥ 7 → record len **2**, drop `5` → sum 2 | **2** |
| 4 | 3 | 5 | `[2,3]` | under target | 2 |
| 5 | 2 | 7 | `[2,3,2]` | ≥ 7 → record len 3, drop `2` → sum 5 | 2 |

Return **2**. Note step `hi=3` shrinking **twice**: that's why it's a `while`, not an
`if`. One removal isn't always enough to break validity.

## ✅ Optimal solution
```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """Length of the shortest subarray with sum >= target, or 0.

        Time:  O(n) amortised, lo only moves forward, at most n times in total,
               so the two pointers take at most 2n steps between them.
        Space: O(1), a running sum.
        """
        lo = 0
        window_sum = 0
        best = float('inf')

        for hi, value in enumerate(nums):
            window_sum += value                   # grow right

            while window_sum >= target:           # shrink while STILL valid
                best = min(best, hi - lo + 1)     # measure BEFORE breaking it
                window_sum -= nums[lo]
                lo += 1

        return 0 if best == float('inf') else best
```
**Time:** O(n) · **Space:** O(1)

### Why this isn't O(n²)
The `while` inside the `for` looks quadratic and isn't. `lo` never decreases, and it
can't pass `n`, so across the *entire run* the inner loop body executes at most `n`
times total, not `n` times per outer step. Combined work: at most `2n` pointer moves.
This is **amortised analysis**, and naming it is one of the highest-value sentences in
this whole pattern.

## ⚠️ Gotchas
- **`while`, not `if`.** After removing one element the window can still be valid,
  see `hi=3` above, which shrinks twice. An `if` returns 3 instead of 2 here.
- **Record the length *before* subtracting.** Once you've removed `nums[lo]` the window
  you measured no longer exists. Off by one in the other direction is the classic
  Shape C bug.
- **Return 0, not `inf`.** Sentinel in, real answer out, convert at the boundary.
- **Positive numbers are load-bearing.** With negatives, a longer window can have a
  smaller sum, so shrinking is no longer safe and you'd need prefix sums plus a
  monotonic deque. Say this out loud; it's the follow-up question, and it's EP28's job.
- `hi - lo + 1` for the length, with the `+1`. Same arithmetic as EP8, count the
  indices on your fingers rather than trusting memory.

## 🎤 Interview talking points
- *"All values are positive, so the sum is monotonic in the window size. That's the
  property that lets the left pointer move forward permanently."*
- *"It's O(n), not O(n²), because `lo` only advances, amortised, the inner loop runs
  at most n times over the whole execution."*
- *"For shortest I shrink while the window is still valid and measure before breaking
  it. For longest I'd shrink only while it's invalid and measure after repairing it."*
  ← saying both, unprompted, shows you hold the general shape and not one instance.

## 🔗 Transfer
EP23–27 are all the *longest* mirror of this. EP29 (Minimum Window Substring) is this
exact shape with the condition upgraded from "sum ≥ target" to "contains every
required character," which is the hardest version of the same question. And EP28
revisits this very problem to show the O(n log n) prefix-sum answer, the one you need
the moment negatives are allowed.

## 📹 Metadata
- **Title:** `Smallest Subarray with a Given Sum, grow right, shrink left | Sliding Window #2`
- **Thumbnail:** `SHRINK WHILE IT WORKS` (amber block)
- **Short:** The `hi=3` double-shrink, "this is why it's a while loop", 45s.
