# EP178 · P15E07 · Subset Sum   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://www.geeksforgeeks.org/problems/subset-sum-problem-1611555638/1

---

## 🎬 Hook
> "Can some of these numbers add up to exactly 9? That's knapsack where every item's
> **value is its weight**, and the only question is yes or no. Change **one operator**
> in yesterday's loop, `max` becomes `or`, and you're done."

## 📋 Problem, in your words
```
Given positive integers arr and a target sum,
return True if some subset of arr adds up to exactly sum, else False.
Each element used at most once. The empty subset sums to 0.

GfG: isSubsetSum(arr, sum) -> bool.  n up to ~200, sum up to ~10^4.
```

## 🔢 The example
```
Input:  arr = [3, 34, 4, 12, 5, 2], sum = 9
Output: True       (4 + 5, also 3 + 4 + 2)

Input:  arr = [3, 34, 4, 12, 5, 2], sum = 30
Output: False

Input:  arr = [1, 2, 3], sum = 6  -> True   (the whole array)

Input:  arr = [1, 2], sum = 0  -> True   (the empty subset)
```

## 🧸 ELI5
> Lay out a row of 10 light switches labelled 0 to 9: "can I make this total?" At the
> start only **switch 0** is on: with no numbers picked, you can make 0.
>
> Now pick up the first number, 3. For every switch that's on, the switch **3 places
> to its right** can turn on too: "whatever I could make before, plus 3".
>
> ```
>  start:     0 . . . . . . . . .       (only 0 reachable)
>  after 3:   0 . . 3 . . . . . .
>  after 4:   0 . . 3 4 . . 7 . .       (0+4, 3+4)
>  after 5:   0 . . 3 4 5 . 7 8 9  <-- 9 is on: 4 + 5
> ```
>
> Each number only lights switches; nothing ever turns off. When you've gone through
> every number, look at switch 9.

## 🐌 Brute force (say it, don't type it)
Try all 2ⁿ subsets, or the include/exclude recursion `can(i, s) = can(i+1, s) or
can(i+1, s - arr[i])` without a memo: **O(2ⁿ)**. With n = 200 that's hopeless. But the
recursion has only `n × (sum + 1)` distinct `(i, s)` pairs, and that's the DP.

## 💡 The pattern reveal
**Signal:** "**is it possible**" · each element **in or out** · a target total.
**Therefore:** DP, Shape B. Knapsack with a boolean.

| | 0/1 Knapsack (EP177) | Subset Sum |
|---|---|---|
| cell means | best **value** at capacity `c` | **can** I make exactly `c`? |
| base | `dp[c] = 0` for all c | `dp[0] = True`, rest `False` |
| update | `dp[c] = max(dp[c], dp[c - w] + v)` | `dp[c] = dp[c] or dp[c - x]` |
| loop | backwards | backwards, same reason |

**Key insight:** it's the same loop because it's the same *choice*: each element is
taken or skipped, once. Only the **verb** changes: maximise became decide. The base
case changes with it: "exactly 0 is reachable, nothing else is yet". That single `True`
is the seed everything else grows from.

## 🔍 Dry run: `arr = [3, 34, 4, 12, 5, 2]`, `sum = 9`

`T` = reachable. Columns are sums 0 to 9.

| after | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | newly lit, from |
|---|---|---|---|---|---|---|---|---|---|---|---|
| start | T | . | . | . | . | . | . | . | . | . | base: empty subset |
| 3 | T | . | . | T | . | . | . | . | . | . | 3 ← 0 |
| 34 | T | . | . | T | . | . | . | . | . | . | nothing: 34 > 9, the loop doesn't run |
| 4 | T | . | . | T | T | . | . | T | . | . | 7 ← 3, 4 ← 0 |
| 12 | T | . | . | T | T | . | . | T | . | . | nothing: 12 > 9 |
| 5 | T | . | . | T | T | T | . | T | T | **T** | 9 ← 4, 8 ← 3, 5 ← 0 |

`dp[9]` = **True** ✓ after the 5, lit from `dp[4]`, i.e. 4 + 5. The early exit in the
code returns here, so 2 is never processed. (Without the early exit, 2 would light 6
and 2, and `dp[9]` would stay True: nothing ever turns off.)

Why backwards matters, in this row: processing 5 **forwards** would light 5 from 0,
then 10 from 5 (if it existed), using 5 twice. Backwards, when `c = 9` reads `dp[4]`,
it's still the value from *before* 5 was considered.

## ✅ Optimal solution
```python
class Solution:
    def isSubsetSum(self, arr: List[int], sum: int) -> bool:
        """Can some subset of arr (each element at most once) sum to exactly target?

        dp[c] = True if some subset of the elements seen so far sums to c.
        Time:  O(n * target), each element sweeps every sum once.
        Space: O(target), one boolean row.
        """
        target = sum                              # GfG's name shadows the built-in sum()
        dp = [False] * (target + 1)
        dp[0] = True                              # the empty subset makes 0
        for x in arr:
            for c in range(target, x - 1, -1):    # backwards: x is used at most once
                if dp[c - x]:
                    dp[c] = True
            if dp[target]:
                return True                       # nothing ever turns off: stop early
        return dp[target]
```
**Time:** O(n · target) · **Space:** O(target)

The memo version (step 3), for when you want to show the recursion first:

```python
@lru_cache(maxsize=None)
def can(i: int, s: int) -> bool:
    if s == 0:
        return True                           # made it exactly
    if i == len(arr) or s < 0:
        return False
    return can(i + 1, s) or can(i + 1, s - arr[i])   # skip it, or take it
```

## ⚠️ Gotchas
- **`dp[0] = True` is the whole seed.** Forget it and nothing is ever reachable: the
  function returns False for every input, including ones that are obviously True.
- **Elements bigger than the target skip themselves.** `range(target, x - 1, -1)` is
  empty when `x > target`. No special case needed; that's rows 34 and 12 above.
- **Backwards loop, again.** Forwards turns this into "can I make it with unlimited
  copies?": `[3]`, target 6 would wrongly return True.
- **Negative numbers break it.** The table index is a sum, and sums would go below 0.
  The problem says positive; if an interviewer adds negatives, you need an offset or a
  set of reachable sums.
- **GfG's parameter is called `sum`.** Keep the name so the signature matches the
  judge, but copy it to `target` on the first line and use that. Inside the method
  `sum` is now an int, so calling `sum(arr)` there raises `TypeError: 'int' object is
  not callable`. You'll want the real `sum()` in the Target Sum follow-up.

## 🎤 Interview talking points
- *"It's 0/1 knapsack where the question is reachability, so the cell is a boolean:
  can I make exactly c?"*
- *"dp[0] is True because the empty subset makes 0; every other sum is built from it."*
- *"I loop sums backwards so each number is used at most once."*
- *"O(n × target) time, O(target) space. Pseudo-polynomial: fine for target ~10⁴."*
- *"Partition Equal Subset Sum is this with target = total / 2, after checking the
  total is even."* ← the classic follow-up, answered before it's asked.

## 🔗 Transfer
EP119 Combination Sum *listed* every subset that hit a target, which is exponential by
necessity. This episode asks only *whether one exists*, and that's what lets the search
collapse into a table of sums. EP179 Target Sum asks *how many*, and turns out to be this
exact problem after one line of algebra: same row, same backwards loop, `or` becomes `+`.

## 📹 Metadata
- **Title:** `Subset Sum, knapsack with a light switch | DP #7`
- **Thumbnail:** `max → or`
- **Short:** the row of switches lighting up number by number until switch 9 turns on. 35s.
