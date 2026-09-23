# EP179 · P15E08 · Target Sum   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://www.geeksforgeeks.org/problems/target-sum-1626326450/1

---

## 🎬 Hook
> "Put a plus or a minus in front of every number and hit the target. That's 2ⁿ sign
> patterns. But **one line of algebra** turns plus-and-minus into 'pick a subset', and
> then it's yesterday's Subset Sum with a `+` where the `or` was."

## 📋 Problem, in your words
```
Given positive integers arr and an integer target (it may be negative),
put '+' or '-' in front of every element.
Count how many sign assignments make the expression equal target.

GfG: totalWays(arr, target), n <= 50, 1 <= arr[i] <= 20, sum(arr) <= 1000,
     -1000 <= target <= 1000.
Same problem as LeetCode 494 (findTargetSumWays), where arr[i] may also be 0.
```

## 🔢 The example
```
Input:  arr = [1, 1, 1, 1, 1], target = 3
Output: 5
Why:    one minus sign, and it can go on any of the 5 ones:
        -1+1+1+1+1, +1-1+1+1+1, +1+1-1+1+1, +1+1+1-1+1, +1+1+1+1-1

Input:  arr = [1, 2, 3], target = 2   -> 1   (+1 -2 +3)
Input:  arr = [1, 2, 3], target = -2  -> 1   (-1 +2 -3: flip every sign of the above)
Input:  arr = [1], target = 1         -> 1
Input:  arr = [0, 0, 1], target = 1   -> 4   (LeetCode only, GfG has no zeros:
                                              each 0 can be +0 or -0, 2 x 2)
Input:  arr = [1, 2], target = 4      -> 0   (4 > total, impossible)
```

## 🧸 ELI5
> Every number goes into one of two buckets: the **plus bucket** or the **minus
> bucket**. The expression's value is (plus bucket total) minus (minus bucket total).
>
> You also know the two buckets together hold **everything**:
>
> ```
>   plus - minus = target      (what we want)
>   plus + minus = total       (always true)
>   ---------------------  add the two lines
>   2 * plus     = target + total
>        plus    = (target + total) / 2
> ```
>
> So the signs don't matter any more. The question is just: **how many ways can I fill
> the plus bucket so it totals `(target + total) / 2`?** Whatever's left over goes in
> the minus bucket automatically.

## 🐌 Brute force (say it, don't type it)
Recurse on each element with both signs, count the leaves that land on the target:
**O(2ⁿ)**. Memoising on `(i, running_sum)` works too, O(n · total) states, but the sum
can be negative so you need a dict or an offset. The algebra below is cleaner, and it's
what the interviewer is waiting to see.

## 💡 The pattern reveal
**Signal:** "**count the ways**" · each element has **two options** · a target total.
**Therefore:** DP, Shape B, knapsack-counting.

**Key insight:** `P = (total + target) / 2`. Two early exits come straight out of it:

| check | why | answer |
|---|---|---|
| `abs(target) > total` | even all-plus or all-minus can't reach it | 0 |
| `(total + target)` is odd | P must be a whole number | 0 |

Otherwise, count subsets that sum to `P`, with the EP178 row and a new verb:

| | Subset Sum (EP178) | Target Sum |
|---|---|---|
| cell means | can I make `c`? | **how many** subsets make `c`? |
| base | `dp[0] = True` | `dp[0] = 1` (one way to make 0: the empty subset) |
| update | `dp[c] = dp[c] or dp[c - x]` | `dp[c] = dp[c] + dp[c - x]` |
| loop | backwards | backwards |

Three episodes, one loop: EP177 maximises, EP178 decides, EP179 counts.

## 🔍 Dry run: `arr = [1, 1, 1, 1, 1]`, `target = 3`

`total = 5`, `P = (5 + 3) / 2 = 4`. Count subsets summing to 4.
Columns are sums 0 to 4; each cell is a count.

| after element | c=0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| start | 1 | 0 | 0 | 0 | 0 |
| 1st `1` | 1 | 1 | 0 | 0 | 0 |
| 2nd `1` | 1 | 2 | 1 | 0 | 0 |
| 3rd `1` | 1 | 3 | 3 | 1 | 0 |
| 4th `1` | 1 | 4 | 6 | 4 | 1 |
| 5th `1` | 1 | 5 | 10 | 10 | **5** |

Answer `dp[4]` = **5** ✓. (Those are binomial coefficients, Pascal's triangle, because
every element is a 1: "choose 4 of the 5 to be plus".)

Narrate one cell: after the 5th `1`, `dp[4] = old dp[4] + old dp[3] = 1 + 4 = 5`. The
backwards loop guarantees `dp[3]` was still the 4th row's value when it was read.

## ✅ Optimal solution
```python
class Solution:
    def totalWays(self, arr: List[int], target: int) -> int:
        """Count +/- sign assignments whose total is target.

        plus - minus = target and plus + minus = total  =>  plus = (total + target) / 2,
        so count the subsets that sum to that.
        Time:  O(n * P), P = (total + target) / 2 <= total.
        Space: O(P), one row of counts.
        """
        total = sum(arr)
        if abs(target) > total or (total + target) % 2:
            return 0                              # unreachable, or P isn't an integer
        # target may be negative (GfG: -1000..1000); abs() above keeps P >= 0
        P = (total + target) // 2

        dp = [0] * (P + 1)
        dp[0] = 1                                 # one way to make 0: take nothing
        for x in arr:
            for c in range(P, x - 1, -1):         # backwards: each element once
                dp[c] += dp[c - x]                # ways without x, plus ways ending with x
        return dp[P]
```
**Time:** O(n · total) · **Space:** O(total)

## ⚠️ Gotchas
- **Zeros are handled, and double the count** (LeetCode allows zeros; GfG has `arr[i] >= 1`). For `x = 0` the loop runs `c` from P down
  to 0 and does `dp[c] += dp[c]`: every count doubles. That's right, `+0` and `-0` are
  two different assignments. `[0, 0, 1]`, target 1 → 4. Many people add a special case
  for zeros that's actually wrong.
- **Check parity AND range before dividing.** `(total + target)` odd means no solution.
  `target < -total` makes P negative, and `[0] * (negative + 1)` silently builds an empty
  list and crashes on `dp[0]`. The `abs` check covers both directions.
- **Base is 1, not True.** The empty subset is *one way*. With `dp[0] = 0` every count
  is 0.
- **Backwards loop.** Forwards reuses an element within one sweep. `[1, 3]`, target 2:
  total 4, P = 3, and the only subset is `{3}`, so the answer is 1 (`-1 + 3`). A forward
  loop lets the single 1 fill sums 1, 2 and 3 by itself and returns 2. Test that one.
- **Negative target is legal.** By symmetry the answer for `-t` equals the answer for
  `t`, and the formula handles it as long as the range check comes first.

## 🎤 Interview talking points
- *"Every number goes in a plus bucket or a minus bucket. P minus N is the target, P
  plus N is the total, so P is (total + target) / 2."* ← the whole problem in one breath.
- *"If that isn't a non-negative integer, the answer is zero."*
- *"Then it's counting subsets that sum to P: the knapsack row with plus instead of max,
  base dp[0] = 1, looped backwards."*
- *"Zeros double the count automatically, because +0 and -0 are different assignments."*
- *"O(n × total) time, O(total) space."*

## 🔗 Transfer
EP177 to EP179 are the knapsack family in full: one row, one backwards loop, three verbs.
The trick of **re-expressing the problem until a known table fits** is the most reusable
idea in this pattern; it comes back at the end in EP185, where "order of cuts" becomes
"split an interval". Next, EP180 LIS leaves knapsack behind: a cell that looks back at
**every** earlier index, not just one row.

## 📹 Metadata
- **Title:** `Target Sum, one line of algebra turns ± into Subset Sum | DP #8`
- **Thumbnail:** `P = (total + target) / 2`
- **Short:** the two bucket equations, added on screen, P falling out. 30s.
