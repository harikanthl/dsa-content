# EP174 · P15E03 · House Robber   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/house-robber/

---

## 🎬 Hook
> "Rob the richest houses, never two next door. Greedy says grab the biggest one first,
> and greedy loses money. The fix is a question you ask at every single house, and it
> only has two answers: **rob it, or skip it**."

## 📋 Problem, in your words
```
nums[i] = cash in house i. Houses are in a row.
Robbing two ADJACENT houses sets off the alarm.
Return the most cash you can take.

1 <= len(nums) <= 100, 0 <= nums[i] <= 400.
```

## 🔢 The example
```
Input:  nums = [2, 7, 9, 3, 1]
Output: 12
Why:    rob houses 0, 2, 4: 2 + 9 + 1 = 12

Input:  nums = [1, 2, 3, 1]  -> 4       (1 + 3)
Input:  nums = [2, 1, 1, 2]  -> 4       (the two ends: gaps can be longer than one)
```

## 🧸 ELI5
> You walk down the street with a bag. At each door you decide.
>
> If you **skip** this house, your best is whatever your best was at the last house.
> If you **rob** it, you couldn't have robbed the last house, so your best is your best
> from **two** houses back, plus this house's cash.
>
> ```
> house:     0    1    2    3    4
> cash:      2    7    9    3    1
> best so far: 2   7   11   11   12
>                      ^ 9 + best-two-back (2) beats skipping (7)
> ```
>
> You never have to remember *which* houses you robbed. Only two numbers: your best one
> house ago, and your best two houses ago.

## 🐌 Brute force (say it, don't type it)
Try every subset of houses with no two adjacent and keep the richest: **O(2ⁿ)** subsets
(well, Fibonacci-many valid ones, which is still exponential). Greedy "rob the biggest,
cross off its neighbours" fails: on `[3, 4, 3]` greedy takes 4 and stops at 4, while
3 + 3 = 6. Kill greedy with that one example.

## 💡 The pattern reveal
**Signal:** "**maximum**" · a **take-or-skip choice** at each element · a constraint
linking neighbours.
**Therefore:** DP, Shape A. This is the pattern card's worked example of the four steps.

| step | House Robber |
|---|---|
| 1. state | `f(i)` = the most I can rob from houses `0..i` |
| 2. recurrence | `f(i) = max(f(i-1), f(i-2) + nums[i])` · skip or rob |
| 3. memo | `@lru_cache` on `f`: O(n) |
| 4. table → shrink | reads two back, so two variables |

**Key insight:** the adjacency rule is exactly why the state reaches back to `i - 2`.
"Rob house i" means house i-1 is off limits, and `f(i-2)` is precisely "the best that
never touched i-1". The constraint is encoded in *where the recurrence looks*, not in a
flag.

```python
def f(i):
    if i < 0: return 0
    return max(f(i - 1),              # skip house i
               f(i - 2) + nums[i])    # rob it, so i-1 is off limits
```

## 🔍 Dry run: `nums = [2, 7, 9, 3, 1]`

`prev1` = f(i-1), `prev2` = f(i-2). Both start at 0: "no houses yet".

| i | cash | skip = prev1 | rob = prev2 + cash | f(i) = max | (prev2, prev1) after |
|---|---|---|---|---|---|
| start | - | - | - | - | (0, 0) |
| 0 | 2 | 0 | 0 + 2 = 2 | **2** | (0, 2) |
| 1 | 7 | 2 | 0 + 7 = 7 | **7** | (2, 7) |
| 2 | 9 | 7 | 2 + 9 = 11 | **11** | (7, 11) |
| 3 | 3 | 11 | 7 + 3 = 10 | **11** (skip) | (11, 11) |
| 4 | 1 | 11 | 11 + 1 = 12 | **12** | (11, 12) |

Answer **12** ✓. Row 3: robbing house 3 would give 10, skipping keeps 11. That's the
moment a greedy "always take it if you can" gets wrong.

## ✅ Optimal solution
```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        """Most cash from non-adjacent houses.

        f(i) = max(f(i-1), f(i-2) + nums[i]): skip house i, or rob it and fall back two.
        Time:  O(n), one pass.
        Space: O(1), f only reads two cells back.
        """
        prev2, prev1 = 0, 0                      # f(i-2), f(i-1); "no houses" = 0
        for cash in nums:
            prev2, prev1 = prev1, max(prev1,           # skip this house
                                      prev2 + cash)    # rob it
        return prev1
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **The tuple assignment matters.** `prev2, prev1 = prev1, max(prev1, prev2 + cash)`
  evaluates the right side with the **old** values. Split it into two lines and you
  overwrite `prev2` before using it.
- **Gaps can be longer than one.** `[2, 1, 1, 2]` → 4 by robbing both ends. People who
  hard-code "every other house" get 3. The `max` with skip handles any gap length.
- **Starting both at 0 handles n = 1 and n = 2** with no special cases. If you write
  `dp[0] = nums[0], dp[1] = max(nums[0], nums[1])`, guard `len(nums) == 1` or you'll
  index out of range.
- **The answer is `prev1`, not `max(nums)` or `prev2`.** f is "best from 0..i", so it's
  already monotone: the last value is the best.

## 🎤 Interview talking points
- *"Greedy fails on [3, 4, 3], so I need to consider both choices at every house."*
- *"State: the best I can do from houses 0..i. At house i I skip it and keep f(i-1), or
  rob it and add to f(i-2), since i-1 is then forbidden."*
- *"The adjacency rule lives in the recurrence reaching back two, not in any flag."*
- *"Only two previous values are read, so O(n) time and O(1) space."*
- *"House Robber II puts the houses in a circle: run this twice, once without the first
  house and once without the last, and take the max."* ← the follow-up, answered first.

## 🔗 Transfer
EP173 was *count* (add the two cases). This is *optimise* (max the two cases), and every
remaining episode is one of those two verbs. The take-or-skip choice is about to grow a
second dimension: EP175 0/1 Knapsack is "rob or skip" where each house also has a weight
and your bag has a capacity. Pattern 04's Max Subarray Sum with One Deletion (EP36) was a
two-state version of this same idea in disguise.

## 📹 Metadata
- **Title:** `House Robber, greedy loses, one question wins | DP #3`
- **Thumbnail:** `ROB or SKIP`
- **Short:** `[3, 4, 3]`: greedy grabs 4, then the DP row fills and shows 6. 40s.
