# EP177 · P15E06 · 0/1 Knapsack Tabulation   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://www.geeksforgeeks.org/problems/0-1-knapsack-problem0945/1

---

## 🎬 Hook
> "Same knapsack as EP175, now as a table, then squeezed into a **single row**. The
> squeeze works only if one loop runs **backwards**. Run it forwards and the code still
> compiles, still passes the example, and quietly lets you pack the same item twice."

## 📋 Problem, in your words
```
Same as EP175: W = capacity, item i has weight wt[i] and value val[i],
each item taken whole or not at all. Return the best value that fits.

Today's goal: the EP175 memo -> a 2-D table -> a 1-D row,
and be able to explain why the 1-D loop goes from W down to w.
```

## 🔢 The example
```
Input:  W = 7, val = [1, 4, 5, 7], wt = [1, 3, 4, 5]
Output: 9      (items 1 + 2: 3 kg + 4 kg, value 4 + 5)

GfG's examples: W = 4, val = [1, 2, 3], wt = [4, 5, 1]            -> 3
                W = 3, val = [1, 2, 3], wt = [4, 5, 6]            -> 0
                W = 5, val = [10, 40, 30, 50], wt = [5, 4, 2, 3]  -> 80

The trap test:  W = 2, val = [1], wt = [1]
Correct:        1      (one item, take it once)
Forward loop:   2      <- took the same item twice
```

## 🧸 ELI5
> Picture a spreadsheet. Each **row** is "I've now considered one more item", each
> **column** is a bag size from 0 to 7. A cell holds "the best I can do with these
> items and this bag".
>
> To fill a cell, you look at **the row above** in two places: straight up (skip the
> item) and up-and-left by the item's weight (take the item, from a smaller bag).
>
> ```
>           c - w           c
>   row i-1   [take from here]  [skip from here]
>                       \          |
>   row i                 \------> [ this cell ]
> ```
>
> Since you only ever read the row above, you could write each new row **on top of the
> old one**. The catch: you read to the **left**. If you write left to right, the
> left cells are already overwritten with *this* row's values when you read them. Write
> right to left and the left side is still the old row when you need it.

## 🐌 Brute force (say it, don't type it)
All 2ⁿ subsets, O(2ⁿ · n). Already beaten by the EP175 memo at O(n · W). The table
doesn't beat the memo's time: it removes the recursion stack, and then the 1-D version
cuts space from O(n · W) to **O(W)**.

## 💡 The pattern reveal
Run EP176's five questions on the EP175 memo `best(i, c)`:

| # | question | answer |
|---|---|---|
| 1 | arguments and ranges → shape | `i` in `0..n`, `c` in `0..W`: a `(n+1) × (W+1)` grid |
| 2 | index shift | none: `best(0, c)` is already "no items", row 0 |
| 3 | base cells | row 0 is all zeros |
| 4 | what does a cell read? | `dp[i-1][c]` and `dp[i-1][c-w]`: **only row i-1**. So fill row by row, and within a row any order works |
| 5 | answer cell | `dp[n][W]` |

Question 6, how far back: **one row**. So keep one row. But in the 1-D array, "row i-1"
and "row i" are the same memory, and cell `c` reads cell `c - w` **to its left**:

| inner loop direction | when `dp[c]` reads `dp[c - w]` it sees | meaning |
|---|---|---|
| **backwards** (`W` down to `w`) | the **old** row (not yet overwritten) | item used at most once ✓ 0/1 knapsack |
| forwards (`w` up to `W`) | the **new** row (already includes this item) | item can be reused: that's the **unbounded** knapsack |

**Key insight:** the direction of one loop decides which problem you solved. Backwards
is 0/1, forwards is unbounded. Say it before the interviewer asks.

## 🔍 Dry run: `W = 7`, `val = [1, 4, 5, 7]`, `wt = [1, 3, 4, 5]`

The full 2-D table. Row `i` = first `i` items considered.

| row (item added) | c=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0: nothing | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1: (1 kg, 1) | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2: (3 kg, 4) | 0 | 1 | 1 | 4 | 5 | 5 | 5 | 5 |
| 3: (4 kg, 5) | 0 | 1 | 1 | 4 | 5 | 6 | 6 | **9** |
| 4: (5 kg, 7) | 0 | 1 | 1 | 4 | 5 | 7 | 8 | **9** |

Narrate three cells:
- **row 2, c=4 → 5:** skip = row 1, c=4 = 1. Take = row 1, c=1 (= 1) + 4 = 5. Take wins.
- **row 3, c=7 → 9:** skip = 5. Take = row 2, c=3 (= 4) + 5 = 9. That's items 1 and 2.
- **row 4, c=7 → 9:** skip = 9. Take = row 3, c=2 (= 1) + 7 = 8. Skip wins.

The 1-D row after each item (backwards loop) is **exactly** rows 1 to 4 above.

The trap test, `W = 2`, one item (1 kg, 1), starting from `dp = [0, 0, 0]`:

| direction | order | step | dp after |
|---|---|---|---|
| backwards | c = 2 | dp[2] = max(0, dp[1] + 1) = 1 (dp[1] still old: 0) | [0, 0, 1] |
| backwards | c = 1 | dp[1] = max(0, dp[0] + 1) = 1 | [0, 1, **1**] ✓ |
| forwards | c = 1 | dp[1] = max(0, dp[0] + 1) = 1 | [0, 1, 0] |
| forwards | c = 2 | dp[2] = max(0, dp[1] + 1) = **2** (dp[1] already includes the item) | [0, 1, **2**] ✗ |

## ✅ Optimal solution
```python
class Solution:
    def knapsack(self, W: int, val: List[int], wt: List[int]) -> int:
        """0/1 knapsack, one row.

        dp[c] = best value with capacity c using the items processed so far.
        Time:  O(n * W), every item touches every capacity once.
        Space: O(W), one row reused for every item.
        """
        dp = [0] * (W + 1)                        # row 0: no items, nothing earned
        for w, v in zip(wt, val):
            for c in range(W, w - 1, -1):         # BACKWARDS: dp[c - w] is still last row's
                dp[c] = max(dp[c],                # skip this item
                            dp[c - w] + v)        # take it, once
        return dp[W]
```
**Time:** O(n · W) · **Space:** O(W)

The 2-D version, to write first if you're asked to show the step:

```python
    def knapsack_2d(self, W: int, val: List[int], wt: List[int]) -> int:
        """dp[i][c] = best value using the first i items with capacity c. O(n*W) time and space."""
        n = len(val)
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            w, v = wt[i - 1], val[i - 1]
            for c in range(W + 1):
                dp[i][c] = dp[i - 1][c]                                  # skip
                if c >= w:
                    dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)       # take
        return dp[n][W]
```

## ⚠️ Gotchas
- **Backwards, from `W` down to `w`, inclusive.** `range(W, w - 1, -1)` stops at `w`.
  Below `w` the item doesn't fit and the cell keeps its old value, so there's nothing to
  do there.
- **Test the trap, not the example.** The example gives 9 with a forward loop too (no
  item is worth taking twice there). `W = 2, [w=1, v=1]` must return 1.
- **`[[0] * (W + 1)] * (n + 1)` is one row repeated.** Every "row" is the same list, so
  writing row 2 rewrites row 1. Use the comprehension.
- **In the 2-D version, any inner order works.** Direction only matters once rows share
  memory. If someone asks "why backwards?", the answer starts with "because I collapsed
  to one row".
- **Unbounded knapsack is the forward loop, on purpose.** Coin Change and "items with
  unlimited copies" use exactly the version that's a bug here.

## 🎤 Interview talking points
- *"Each cell reads only the previous row, so I can keep one row of size W + 1."*
- *"In one row, cell c reads cell c - w to its left. I loop capacity backwards so that
  cell still holds the previous item's row, which enforces 'each item at most once'."*
- *"If I looped forwards I'd be solving the unbounded knapsack instead."* ← say it
  before they ask.
- *"O(nW) time, O(W) space."*

## 🔗 Transfer
This loop is the engine for the next two episodes, almost unchanged. EP178 Subset Sum
swaps `max(dp[c], dp[c-w] + v)` for `dp[c] or dp[c-x]`. EP179 Target Sum swaps it for
`dp[c] + dp[c-x]` (counting). Same row, same backwards loop, three different verbs:
maximise, decide, count.

## 📹 Metadata
- **Title:** `Knapsack in ONE row, and why the loop runs backwards | DP #6`
- **Thumbnail:** `← BACKWARDS ←`
- **Short:** the `W = 2` trap: forward loop turns 1 into 2 in slow motion, backward loop
  doesn't. 40s.
