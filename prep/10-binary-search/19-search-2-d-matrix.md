# EP089 · P10E19 · Search a 2D Matrix   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/search-a-2d-matrix/

---

## 🎬 Hook
> "A matrix where every row is sorted and each row starts after the last one ends. That
> isn't a grid. **It's one sorted array that somebody folded.** Unfold it with one line
> of `divmod` and it's EP71 again."

## 📋 Problem, in your words
```
m x n matrix of integers:
  - each row is sorted ascending
  - the first number of each row is bigger than the last number of the row above

Return True if target is in the matrix. Must be O(log(m * n)).
```

## 🔢 The example
```
matrix = [[ 1,  3,  5,  7],
          [10, 11, 16, 20],
          [23, 30, 34, 60]]

target = 3   -> True
target = 13  -> False   (it would sit between 11 and 16)
target = 61  -> False   (bigger than everything)
```

## 🧸 ELI5
> Read the matrix like a book: left to right, then drop to the next line. Because each
> line starts where the last one stopped, reading it that way gives one long sorted list:
>
> ```
> [[ 1,  3,  5,  7],
>  [10, 11, 16, 20],       read as a book  ->  1 3 5 7 10 11 16 20 23 30 34 60
>  [23, 30, 34, 60]]                          0 1 2 3  4  5  6  7  8  9 10 11
> ```
>
> Position 6 in the long list: `6 // 4 = 1` rows down, `6 % 4 = 2` across. That's 16.
> You never have to build the long list, you just translate each position when you need
> it.

## 🐌 Brute force (say it, don't type it)
Scan every cell: **O(m · n)**. Better: binary search each row, **O(m log n)**, or
binary search the first column to pick a row and then the row, **O(log m + log n)**,
which is actually the same complexity as flattening but twice the code. Flattening is
one search and one line of arithmetic.

## 💡 The pattern reveal
**Signal:** "each row sorted" **and** "first of each row > last of previous row".
**Therefore:** Shape A on a virtual 1-D array of length `m · n`.

**Key insight:** the second condition is what makes the flattening valid. Index `k` in
the virtual array lives at:

```python
r, c = divmod(k, cols)       # row = k // cols, column = k % cols
```

Divide by **columns**, because that's how many cells each row holds. Then it's the
lower-bound template from EP71, word for word:

```python
lo, hi = 0, rows * cols
while lo < hi:
    mid = (lo + hi) // 2
    r, c = divmod(mid, cols)
    if matrix[r][c] < target: lo = mid + 1
    else:                      hi = mid
```

## 🔍 Dry run: the matrix above, `cols = 4`, `rows * cols = 12`

**target = 3**

| step | lo | hi | mid | `divmod(mid, 4)` | value | vs 3 | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 12 | 6 | (1, 2) | 16 | ≥ | `hi = 6` |
| 2 | 0 | 6 | 3 | (0, 3) | 7 | ≥ | `hi = 3` |
| 3 | 0 | 3 | 1 | (0, 1) | 3 | ≥ | `hi = 1` |
| 4 | 0 | 1 | 0 | (0, 0) | 1 | < | `lo = 1` |
| - | 1 | 1 | stop | (0, 1) | **3** | == | **True** ✓ |

**target = 13**

| step | lo | hi | mid | `divmod(mid, 4)` | value | vs 13 | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 12 | 6 | (1, 2) | 16 | ≥ | `hi = 6` |
| 2 | 0 | 6 | 3 | (0, 3) | 7 | < | `lo = 4` |
| 3 | 4 | 6 | 5 | (1, 1) | 11 | < | `lo = 6` |
| - | 6 | 6 | stop | (1, 2) | 16 | ≠ | **False** ✓ |

Index 6 is where 13 *would* go: between 11 and 16. That's the lower bound working as
designed, and the equality check afterwards is EP71's.

## ✅ Optimal solution
```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """Membership test in a row-major sorted matrix.

        Time:  O(log(m * n)), one binary search over the virtual flattened array.
        Space: O(1), nothing is actually flattened.
        """
        rows, cols = len(matrix), len(matrix[0])
        lo, hi = 0, rows * cols
        while lo < hi:
            mid = (lo + hi) // 2
            r, c = divmod(mid, cols)        # virtual index -> (row, column)
            if matrix[r][c] < target:
                lo = mid + 1
            else:
                hi = mid

        if lo == rows * cols:               # target is bigger than everything
            return False
        r, c = divmod(lo, cols)
        return matrix[r][c] == target
```
**Time:** O(log(m·n)) · **Space:** O(1)

## ⚠️ Gotchas
- **`divmod(k, cols)`, not `rows`.** Dividing by rows only works on square matrices, so
  it passes a 3×3 test and fails on 3×4. Test a non-square matrix.
- **Check `lo == rows * cols` before indexing.** Target 61 ends at `lo = 12`, and
  `divmod(12, 4) = (3, 0)` is off the bottom of the matrix.
- **Don't physically flatten.** `sum(matrix, [])` is O(m·n) time and memory, which
  throws away the whole point.
- **This trick needs the "row starts after previous row ends" guarantee.** Without it
  (tomorrow's problem) the virtual array isn't sorted.

## 🎤 Interview talking points
- *"The two guarantees together mean row-major order is fully sorted, so I treat it as
  one array of length m·n."*
- *"Index `k` maps to `divmod(k, cols)`; that's the only new line versus plain binary
  search."*
- *"O(log(m·n)), which equals O(log m + log n), the same as searching the first column
  then a row, with half the code."*

## 🔗 Transfer
EP71's template, now with an index translation. Tomorrow's EP90 removes the second
guarantee: rows and columns are sorted separately, the flattened array is no longer
sorted, and the right tool turns out not to be binary search at all.

## 📹 Metadata
- **Title:** `Search a 2D Matrix, a sorted array somebody folded | Binary Search #19`
- **Thumbnail:** `divmod(k, cols)` (green block)
- **Short:** the matrix unfolding into one row, then index 6 folding back to (1, 2). 30s.
