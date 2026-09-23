# EP086 · P10E16 · Capacity to Ship Packages Within D Days   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/description/

---

## 🎬 Hook
> "What's the smallest ship that gets everything delivered in D days? Don't guess the
> range from the constraints. **The data hands it to you**: the ship must carry the
> heaviest package, and it never needs more than all of them at once. Those two numbers
> are the whole setup."

## 📋 Problem, in your words
```
weights[i] is a package; they must ship IN ORDER, on a conveyor belt.
Each day you load packages onto the ship until the next one would
exceed its capacity, then sail.

Return the smallest capacity that ships everything within `days` days.
```

## 🔢 The example
```
Input:  weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5
Output: 15
Why:    [1,2,3,4,5] [6,7] [8] [9] [10]  -> 5 days, heaviest day is 15.
        Capacity 14: [1,2,3,4] [5,6] [7] [8] [9] [10] -> 6 days, too many.

Input:  [3, 2, 2, 4, 1, 4], days = 3  -> 6   ([3,2] [2,4] [1,4])
Input:  [1, 2, 3, 1, 1],    days = 4  -> 3   ([1,2] [3] [1,1])
```

## 🧸 ELI5
> You rent a truck by size. Every morning you load boxes off the belt in order until the
> next box won't fit, then drive.
>
> ```
> belt: 1 2 3 4 5 6 7 8 9 10          must finish in 5 days
>
> truck 32:  [1 2 3 4 5 6 7] [8 9 10]            2 days  ✓ but huge
> truck 15:  [1 2 3 4 5] [6 7] [8] [9] [10]      5 days  ✓
> truck 14:  [1 2 3 4] [5 6] [7] [8] [9] [10]    6 days  ✗
> truck  9:  can't even lift the 10               ✗
> ```
>
> Bigger truck, fewer days. So "done in time?" goes **no, no, no, yes, yes** as the
> truck grows. You want the **first** yes: the cheapest truck that makes it.

## 🐌 Brute force (say it, don't type it)
Try every capacity from `max(weights)` up, simulate the days for each, return the first
that fits. **O(n · (sum − max))**: with 5·10⁴ packages of up to 500 each, the sum is
25 million capacities to try. The simulation is fine; trying capacities one at a time
isn't.

## 💡 The pattern reveal
**Signal:** "the **least** capacity such that it ships within D days" · simulating one
capacity is a single greedy pass.
**Therefore:** Shape C, minimise flavour, the round-down template.

| decision | here |
|---|---|
| what is `x`? | ship capacity |
| what is `feasible(x)`? | greedy fill: start a new day when the next package won't fit; `days_needed(x) <= days` |
| why monotonic? | more capacity never needs more days, the same loading still fits |
| what is the range? | **`[max(weights), sum(weights)]`** |

**Key insight: pull the range from the data.**

- `lo = max(weights)`: anything smaller can't lift the heaviest package, ever. Starting
  at 1 isn't just slower; with `lo = 1` the greedy would have to handle a package that
  never fits, and it quietly miscounts.
- `hi = sum(weights)`: one day, everything at once. Always feasible, since `days >= 1`.

```python
if days_needed(mid) <= days:
    hi = mid          # this ship is enough; maybe a smaller one is too
else:
    lo = mid + 1      # too slow; need a bigger ship
```

## 🔍 Dry run: `[1..10]`, `days = 5`
Range `[10, 55]`.

| step | lo | hi | mid | loading | days | ≤ 5? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 10 | 55 | 32 | [1..7] [8,9,10] | 2 | ✓ | `hi = 32` |
| 2 | 10 | 32 | 21 | [1..6] [7,8] [9,10] | 3 | ✓ | `hi = 21` |
| 3 | 10 | 21 | 15 | [1..5] [6,7] [8] [9] [10] | 5 | ✓ | `hi = 15` |
| 4 | 10 | 15 | 12 | [1..4] [5,6] [7] [8] [9] [10] | 6 | ✗ | `lo = 13` |
| 5 | 13 | 15 | 14 | [1..4] [5,6] [7] [8] [9] [10] | 6 | ✗ | `lo = 15` |
| - | 15 | 15 | stop | | | | answer **15** ✓ |

Five greedy passes instead of up to 46. Notice steps 4 and 5 load identically: capacity
12 and 14 both give six days, and the search didn't need to know why.

## ✅ Optimal solution
```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """Smallest ship capacity that delivers every package, in order, within days.

        Time:  O(n log S), S = sum(weights): log S simulations, each O(n).
        Space: O(1).
        """
        def days_needed(cap: int) -> int:
            d, load = 1, 0
            for w in weights:
                if load + w > cap:          # this package sails tomorrow
                    d += 1
                    load = 0
                load += w
            return d

        lo, hi = max(weights), sum(weights) # must lift the heaviest; one day always works
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid                    # enough; try smaller
            else:
                lo = mid + 1                # too many days; need bigger
        return lo
```
**Time:** O(n log S) · **Space:** O(1)

## ⚠️ Gotchas
- **`lo = max(weights)`.** With `lo = 1`, a capacity below the heaviest package makes
  `days_needed` start a new day and then load the too-heavy package anyway. It reports
  a day count for an impossible ship, and the search can return it.
- **`d` starts at 1.** The first day exists before any package overflows. Starting at 0
  undercounts by one everywhere.
- **In order, no reordering.** That's why this is a greedy fill and not bin packing
  (which is NP-hard). Say it: the conveyor belt is what makes the check O(n).
- **`<= days`, not `== days`.** Finishing early is fine.
- **Reset then add:** on overflow set `load = 0`, then `load += w` for the package that
  starts the new day. Writing `load = w` is equivalent; forgetting the package isn't.

## 🎤 Interview talking points
- *"Binary search on capacity. The check is a greedy fill: load in order until the next
  package won't fit, then start a new day."*
- *"More capacity never needs more days, so feasibility flips once; I want the first
  capacity that works."*
- *"The range comes from the data: at least the heaviest package, at most the total."*
  ← the lesson of the episode.
- *"Greedy is optimal for the check because the order is fixed: filling today as much
  as possible never hurts tomorrow."*

## 🔗 Transfer
Koko (EP81) had the same shape with hours instead of days. Tomorrow, EP87 Book
Allocation, swaps packages for pages and days for students: same greedy, same range,
same code. Then EP88 Split Array Largest Sum is the LeetCode name for EP87. By the end
of that run, "min-max partition of an ordered array" should trigger this loop on sight.

## 📹 Metadata
- **Title:** `Ship Packages in D Days, the range comes from the data | Binary Search #16`
- **Thumbnail:** `[max, sum]` (green block)
- **Short:** trucks 32, 15, 14, 9 loading the belt, one after another. 45s.
