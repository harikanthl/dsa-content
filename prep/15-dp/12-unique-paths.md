# EP183 · P15E12 · Unique Paths   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/unique-paths/description/

---

## 🎬 Hook
> "A robot can only move right or down. How many routes from the top-left corner to the
> bottom-right? It's Climbing Stairs on a **grid**: ask where the last move came from,
> and every cell is the sum of the cell **above** and the cell to the **left**."

## 📋 Problem, in your words
```
An m x n grid. A robot starts at the top-left cell and must reach the bottom-right.
Each move is one cell RIGHT or one cell DOWN.
Count the distinct paths.

1 <= m, n <= 100. The answer fits in 2 * 10^9.
```

## 🔢 The example
```
Input:  m = 3, n = 7
Output: 28

Input:  m = 3, n = 2
Output: 3        (R D D, D R D, D D R)

Input:  m = 1, n = 1  -> 1   (already there: the empty path)
```

## 🧸 ELI5
> Stand on any cell and ask "how could I have arrived here?" Only two ways: **from
> above** (moved down) or **from the left** (moved right). Every path to you went
> through one of those two cells, and never both as the last step. So:
>
> ```
>   paths(here) = paths(above) + paths(left)
> ```
>
> The top row: you can only get there by moving right, right, right. One way each.
> The left column: down, down, down. One way each. Everything else is a sum.
>
> ```
>   1   1   1   1
>   1   2   3   4
>   1   3   6  10      <- each number = the one above + the one to the left
> ```

## 🐌 Brute force (say it, don't type it)
Recurse from the start trying right and down, count arrivals: **O(2^(m+n))**. The same
cell is reached from many different routes and its count is recomputed every time.
(And the math answer: a path is `m-1` downs and `n-1` rights in some order, so it's
`C(m+n-2, m-1)`. Mention it; the DP is what generalises to obstacles and costs.)

## 💡 The pattern reveal
**Signal:** a **grid** · moves only **right/down** · "**how many** paths".
**Therefore:** DP, Shape D (grid: the state is a pair `(r, c)`).

| step | Unique Paths |
|---|---|
| state | `dp[r][c]` = number of paths from the start to cell `(r, c)` |
| recurrence | `dp[r][c] = dp[r-1][c] + dp[r][c-1]` (last move was down, or right) |
| base | top row and left column are all **1** |
| fill order | reads up and left, so row by row, left to right |
| answer | `dp[m-1][n-1]` |

**Key insight:** it's LCS's grid with **two** neighbours instead of three and a `+`
instead of a `max`. And like knapsack, each row only reads the row above, so one row is
enough. Here the in-place update runs **forwards**, the opposite of knapsack, and the
reason is worth saying: `row[c-1]` should be the **new** value (the cell to the left, in
this same row), and `row[c]` before the update still holds the cell above.

```
row[c]   += row[c - 1]
  ^  old = above         ^ new = left (already updated this row)
```

## 🔍 Dry run: `m = 3`, `n = 7`

The full grid:

| r \ c | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 2 | 1 | 3 | 6 | 10 | 15 | 21 | **28** |

The one-row version, row after each pass (this is exactly what the code stores):

| after | row |
|---|---|
| init (row 0) | [1, 1, 1, 1, 1, 1, 1] |
| row 1 | [1, 2, 3, 4, 5, 6, 7] |
| row 2 | [1, 3, 6, 10, 15, 21, **28**] |

Narrate one update: row 2, c = 3. `row[3]` is still 4 (the cell above), `row[2]` is
already 6 (the cell to the left, this row). 4 + 6 = 10 ✓.

Answer **28** ✓, and `C(8, 2) = 28` agrees.

## ✅ Optimal solution
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """Right/down paths from top-left to bottom-right of an m x n grid.

        dp[r][c] = dp[r-1][c] + dp[r][c-1], borders are 1. Kept as one row:
        row[c] holds 'above' before the update and 'here' after it.
        Time:  O(m * n), every cell once.
        Space: O(n), one row.
        """
        row = [1] * n                         # row 0: one way to each cell, all rights
        for _ in range(1, m):
            for c in range(1, n):             # column 0 stays 1: all downs
                row[c] += row[c - 1]          # above (old row[c]) + left (new row[c-1])
        return row[-1]
```
**Time:** O(m · n) · **Space:** O(n)

The 2-D version, if you want to show the table first:

```python
dp = [[1] * n for _ in range(m)]              # borders are 1; interior gets overwritten
for r in range(1, m):
    for c in range(1, n):
        dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
return dp[m - 1][n - 1]
```

## ⚠️ Gotchas
- **Borders are 1, not 0.** A 0 border makes every cell 0. The "empty thing has one way"
  rule from the pattern card, again: one path along an edge.
- **Loops start at 1.** `range(1, n)` leaves column 0 alone. Starting at 0 reads
  `row[-1]` (Python wraps to the *last* column) and gives a wrong number with no error.
- **Forwards here, backwards in knapsack.** Here you *want* the current row's left
  neighbour. In knapsack you wanted the *previous* row's. Direction follows from which
  row the left-hand read should come from.
- **`m = 1` or `n = 1` → 1.** The loops don't run (or only touch column 0); `row[-1]`
  is 1. Correct for free.
- **Unique Paths II (obstacles):** set an obstacle cell to 0, and the border is 1 only
  *until* the first obstacle. That's why the DP beats the formula.

## 🎤 Interview talking points
- *"Every path into a cell came from above or from the left, so paths add: up plus
  left. Top row and left column are 1."*
- *"O(mn) time. Each row only needs the previous one, so a single row of size n works,
  updated left to right: before the update it holds 'above', and the left neighbour is
  already the new row."*
- *"Combinatorially it's C(m+n-2, m-1), but the DP handles obstacles and costs, which
  the formula doesn't."*
- *"Minimum Path Sum is the same grid with min plus the cell's cost instead of a sum."*

## 🔗 Transfer
LCS (EP182) gave you the 2-D table; this gives you the **grid** reading of it, and the
realisation that "one row, which direction?" always depends on whether the left read
should see the old row or the new one. Unique Paths II, Minimum Path Sum, Dungeon Game
and Cherry Pickup all start from this table. EP184 goes back to 1-D, but with a state
that finally needs more than one number per day.

## 📹 Metadata
- **Title:** `Unique Paths, Climbing Stairs on a grid | DP #12`
- **Thumbnail:** `↑ + ←`
- **Short:** the 3 x 7 grid filling in, each number the sum of above and left, ending at
  28. 30s.
