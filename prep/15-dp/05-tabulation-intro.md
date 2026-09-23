# EP176 · P15E05 · Tabulation Intro   [Concept]

**Pattern:** DP (Dynamic Programming) · **Link:** builds on EP174 House Robber, https://leetcode.com/problems/house-robber/

---

## 🎬 Hook
> "Every DP so far started at the answer and recursed down. Today we flip it: start at
> the **bottom** and build up, no recursion, no stack. It's the step where most people
> lose the thread, so we do it slowly, on a problem you already know, with **five
> questions** that work on every DP you'll ever write."

## 📋 Problem, in your words
```
Not a new problem. A new technique, on House Robber (EP174):

  f(i) = max(f(i - 1), f(i - 2) + nums[i]),   f(negative) = 0

Take that memoised recursion and rewrite it as a loop that fills an array,
then shrink the array to two variables. Nothing about the answer changes.
```

## 🔢 The example
```
Input:  nums = [2, 7, 9, 3, 1]
Output: 12

The table we'll build (dp[k] = best from the first k houses):
k:      0   1   2   3    4    5
dp[k]:  0   2   7   11   11   12
```

## 🧸 ELI5
> **Memo (top-down)** is a lazy student. Asked "what's the answer for house 4?", they
> say "depends on house 3 and 2, let me go ask", and write each answer down when it
> comes back. They only work out what they're asked.
>
> **Table (bottom-up)** is an organised student. Before anyone asks anything, they
> fill in house 0, then house 1, then house 2, in order, so that when they get to any
> house, **everything it needs is already on the page**.
>
> ```
>   top-down asks:     f(4) -> f(3) -> f(2) -> f(1) -> f(0)      (down the stack)
>   memo is written:   f(0),   f(1),   f(2),   f(3),   f(4)      (on the way back up)
>   bottom-up fills:   dp[0],  dp[1],  dp[2],  dp[3],  dp[4]...  (just do that directly)
> ```
>
> The table's fill order is the order the memo *got written*: the reverse of the order
> it was asked.

## 🐌 Brute force (say it, don't type it)
The un-memoised recursion, O(2ⁿ). You've already beaten it with a memo. So the honest
question is **why bother tabulating** at all? Three real reasons, say them:

1. **No recursion limit.** Python stops at ~1000 frames. n = 10⁵ kills the memo, not
   the loop.
2. **Cheaper constants.** No function calls, no hash lookups, just array reads.
3. **Space optimisation is only visible in a table.** You can't "keep only the last two
   rows" of a memo dictionary. You can of an array.

## 💡 The pattern reveal
**The recipe. Five questions, asked of the memo, answered in order.**

| # | question | House Robber answer |
|---|---|---|
| 1 | **What are the memo's arguments, and their ranges?** That's the table's shape. | one argument `i` in `-1..n-1`, so a 1-D array of `n + 1` cells |
| 2 | **Shift indices so the base case is a real cell.** | `f(-1)` can't be `dp[-1]`, so let `dp[k]` = f(k - 1) = "best from the first k houses". `dp[0]` = no houses. |
| 3 | **Base cases become the first cells you write.** | `dp[0] = 0` (no houses), `dp[1] = nums[0]` (one house) |
| 4 | **Which cells does a cell read? Fill those first.** | `dp[k]` reads `dp[k-1]` and `dp[k-2]`, both to the left, so fill left to right |
| 5 | **Where's the original call?** That cell is the answer. | `f(n-1)` = `dp[n]` |

Then the bonus sixth question: **how far back does a cell ever read?** Two cells. So
two variables replace the array.

**Key insight:** tabulation isn't a different algorithm. It's the **same recurrence**,
with you deciding the evaluation order instead of the call stack. Question 4 is the only
one that takes thought, and it has a mechanical answer: draw an arrow from each cell to
the cells it reads, and fill in an order where arrows only point backwards.

```
  dp[k-2]   dp[k-1]   dp[k]
     ^_________^________|       arrows point left  =>  fill left to right
```

That arrow picture decides every table in this pattern: left to right here, row by row
for knapsack (EP177), and by increasing interval length for Cut a Stick (EP185).

## 🔍 Dry run: `nums = [2, 7, 9, 3, 1]`, the full table

`dp[k] = max(dp[k-1], dp[k-2] + nums[k-1])`: skip house `k-1`, or rob it.

| k | house k-1 | cash | skip = dp[k-1] | rob = dp[k-2] + cash | dp[k] |
|---|---|---|---|---|---|
| 0 | - | - | - | - | **0** (base: no houses) |
| 1 | 0 | 2 | - | - | **2** (base: one house) |
| 2 | 1 | 7 | 2 | 0 + 7 = 7 | **7** |
| 3 | 2 | 9 | 7 | 2 + 9 = 11 | **11** |
| 4 | 3 | 3 | 11 | 7 + 3 = 10 | **11** |
| 5 | 4 | 1 | 11 | 11 + 1 = 12 | **12** |

Answer `dp[5]` = **12** ✓, and it's exactly the EP174 run: the rolling variables were
this table's last two cells all along.

The same recipe on Climbing Stairs (EP173), to prove it transfers:

| question | Climbing Stairs |
|---|---|
| shape | `ways(i)` for `i` in `0..n`: array of `n + 1` |
| index shift | none needed, `ways(0)` is already a real index |
| base cells | `dp[0] = 1`, `dp[1] = 1` |
| fill order | reads `i-1`, `i-2`: left to right |
| answer | `dp[n]` |

## ✅ Optimal solution
Step by step, all three versions side by side. They return the same number on every
input.

```python
from functools import lru_cache


class Solution:
    def rob_memo(self, nums: List[int]) -> int:
        """Step 3: top-down. O(n) time, O(n) memo + O(n) stack."""

        @lru_cache(maxsize=None)
        def f(i: int) -> int:
            if i < 0:
                return 0
            return max(f(i - 1), f(i - 2) + nums[i])

        return f(len(nums) - 1)

    def rob_table(self, nums: List[int]) -> int:
        """Step 4: bottom-up. dp[k] = best from the first k houses.

        Time:  O(n), each cell filled once from two earlier cells.
        Space: O(n) for the table, no recursion.
        """
        n = len(nums)
        dp = [0] * (n + 1)
        dp[1] = nums[0]                               # base: one house, rob it
        for k in range(2, n + 1):
            dp[k] = max(dp[k - 1],                    # skip house k-1
                        dp[k - 2] + nums[k - 1])      # rob house k-1
        return dp[n]

    def rob(self, nums: List[int]) -> int:
        """Step 4, shrunk: dp[k] only reads two cells back, so keep two.

        Time:  O(n).
        Space: O(1).
        """
        prev2, prev1 = 0, 0                           # dp[k-2], dp[k-1]
        for cash in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + cash)
        return prev1
```
**Time:** O(n) for all three · **Space:** O(n), O(n), O(1)

## ⚠️ Gotchas
- **The index shift is where bugs live.** `dp[k]` answers `f(k - 1)`, so the house is
  `nums[k - 1]`. Mixing the two conventions gives an answer that's right on the example
  and off by one house on others. Write the meaning of `dp[k]` as a comment above the
  array, every time.
- **`dp[1] = nums[0]` needs `n >= 1`.** LeetCode guarantees it. If empty input is
  possible, guard it or use the rolling version, which handles `[]` for free.
- **Fill order isn't always left to right.** It's "whatever order makes every read
  already filled". For 1-D look-back problems that happens to be left to right. EP185
  fills by interval length, and a wrong order there reads zeros that look like answers.
- **The table computes every state, the memo only reachable ones.** Usually that's the
  same set. For knapsack it isn't (EP175 touched 11 of 32 states), so the table can do
  more work while still being faster in practice.

## 🎤 Interview talking points
- *"I'll write the recursion first because it's the easiest to get right, then convert
  it."* ← the order a senior engineer uses.
- *"The table's shape comes from the memo's arguments, the base cells from its base
  cases, and the fill order from which cells each cell reads."*
- *"Each cell reads only the previous two, so I can drop to two variables: O(1) space."*
- *"Bottom-up also removes the recursion-depth limit, which matters in Python past about
  a thousand."*

## 🔗 Transfer
The five questions are the tool; every tabulation from here on is them applied to a
bigger memo. EP177 runs them on the 2-D knapsack memo from EP175 and then asks the sixth
question, "how far back does a cell read?", where the answer ("one row") forces the
famous **backwards** inner loop. EP181 runs them on the LIS memo from EP180.

## 📹 Metadata
- **Title:** `Memo to Table, the 5 questions that flip ANY DP | DP #5`
- **Thumbnail:** `TOP-DOWN ⇄ BOTTOM-UP`
- **Short:** the House Robber call stack going down, the memo filling up, then the same
  cells filling left to right with no stack at all. 50s.
