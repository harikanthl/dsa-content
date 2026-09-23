# EP090 · P10E20 · Search a 2D Matrix II   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/search-a-2d-matrix-ii/description/

---

## 🎬 Hook
> "An episode in the binary search pattern whose best answer **isn't binary search**.
> Stand in the top-right corner of the matrix. Every step you take throws away a whole
> row or a whole column. Knowing when to put the template down is part of knowing the
> template."

## 📋 Problem, in your words
```
m x n matrix:
  - each row is sorted ascending, left to right
  - each column is sorted ascending, top to bottom
  (but a row does NOT start after the previous row ends)

Return True if target is in the matrix.
```

## 🔢 The example
```
matrix = [[ 1,  4,  7, 11, 15],
          [ 2,  5,  8, 12, 19],
          [ 3,  6,  9, 16, 22],
          [10, 13, 14, 17, 24],
          [18, 21, 23, 26, 30]]

target = 5   -> True
target = 20  -> False
```

## 🧸 ELI5
> Stand at the **top-right** corner, 15. Everything to your left in this row is smaller.
> Everything below you in this column is bigger. So 15 is a **fork in the road**: one
> direction only goes down in value, the other only goes up.
>
> ```
>  1   4   7  11 [15]    looking for 5
>                  ^     15 > 5: nothing below 15 can be 5 (all bigger). Drop this column, step left.
>  1   4   7 [11]        11 > 5: drop column, left.
>  1   4  [7]            7 > 5: drop column, left.
>  1  [4]                4 < 5: nothing left of 4 in this row can be 5 (all smaller). Drop row, step down.
>  2  [5]                found.
> ```
>
> The top-left corner doesn't work: from 1, both right and down go **up**, so a "too
> small" answer doesn't tell you which way to go.

## 🐌 Brute force (say it, don't type it)
Scan all cells: **O(m · n)**. Binary search each row: **O(m log n)**, a genuine
improvement, and the answer most people reach for first because it *looks* like the
pattern. The staircase beats it: **O(m + n)**.

## 💡 The pattern reveal
**Signal:** rows sorted **and** columns sorted, but no "row starts after the previous
ends".
**Therefore:** not Shape A. The flattened order isn't sorted (`15` then `2`). Use the
**staircase** from a corner where the two directions disagree.

**Key insight:** at the top-right cell `v`:

| compare | conclusion | move |
|---|---|---|
| `v == target` | found | return True |
| `v > target` | everything **below** `v` in this column is bigger still | `c -= 1` (drop the column) |
| `v < target` | everything **left** of `v` in this row is smaller still | `r += 1` (drop the row) |

Each step deletes a row or a column, so at most `m + n` steps. The bottom-left corner
works too, mirrored. Top-left and bottom-right don't.

**Honest framing:** this is two pointers, not binary search. Pattern card: *"knowing
that is the point of the episode."*

## 🔍 Dry run

**target = 5**

| step | (r, c) | value | vs 5 | move |
|---|---|---|---|---|
| 1 | (0, 4) | 15 | > | left |
| 2 | (0, 3) | 11 | > | left |
| 3 | (0, 2) | 7 | > | left |
| 4 | (0, 1) | 4 | < | down |
| 5 | (1, 1) | **5** | == | **True** ✓ |

**target = 20**

| step | (r, c) | value | vs 20 | move |
|---|---|---|---|---|
| 1 | (0, 4) | 15 | < | down |
| 2 | (1, 4) | 19 | < | down |
| 3 | (2, 4) | 22 | > | left |
| 4 | (2, 3) | 16 | < | down |
| 5 | (3, 3) | 17 | < | down |
| 6 | (4, 3) | 26 | > | left |
| 7 | (4, 2) | 23 | > | left |
| 8 | (4, 1) | 21 | > | left |
| 9 | (4, 0) | 18 | < | down → `r = 5`, off the grid → **False** ✓ |

Nine steps, and `m + n = 10` is the ceiling. The path is a staircase down and to the
left, which is where the name comes from.

## ✅ Optimal solution
```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """Membership test in a matrix sorted along rows and along columns.

        Time:  O(m + n), each step eliminates one row or one column.
        Space: O(1).
        """
        r, c = 0, len(matrix[0]) - 1        # top-right: left is smaller, down is bigger
        while r < len(matrix) and c >= 0:
            v = matrix[r][c]
            if v == target:
                return True
            if v > target:
                c -= 1                      # whole column below is too big
            else:
                r += 1                      # whole row to the left is too small
        return False
```
**Time:** O(m + n) · **Space:** O(1)

## ⚠️ Gotchas
- **Start top-right (or bottom-left).** From top-left, "too small" means both right and
  down are candidates, and you're back to a search tree.
- **Flattening fails here.** EP89's `divmod` trick assumes row-major order is sorted.
  In this matrix it goes `..., 15, 2, ...`. Try it and a binary search misses 5.
- **Loop bounds: `r < rows and c >= 0`.** You leave the grid either off the bottom or
  off the left edge.
- **It's O(m + n), not O(log).** Don't claim logarithmic. For a square n×n matrix,
  O(n) versus the per-row O(n log n).

## 🎤 Interview talking points
- *"Top-right is the corner where the two directions disagree: left is smaller, down is
  bigger. So every comparison eliminates a row or a column."*
- *"That's O(m + n). Binary searching each row is O(m log n), worse on square
  matrices."*
- *"This is really two pointers. The flattening trick from Search a 2D Matrix I doesn't
  apply because rows don't continue each other."*
- *"There's a divide-and-conquer version, but it's messier and not faster in the worst
  case."*

## 🔗 Transfer
EP89 and EP90 look like the same problem and need completely different tools; the
difference is one guarantee in the statement. And the staircase isn't done: tomorrow in
EP91 it becomes the **counting** step inside a binary search on values: "how many
cells are `<= x`?" is exactly this walk, run once per guess.

## 📹 Metadata
- **Title:** `Search a 2D Matrix II, the binary search episode with no binary search | Binary Search #20`
- **Thumbnail:** `START TOP-RIGHT` (red block)
- **Short:** the staircase path for 20, cells greying out as rows and columns drop. 40s.
