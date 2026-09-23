# EP092 · P10E22 · Kth Smallest Number in Multiplication Table   [Hard]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/description/

---

## 🎬 Hook
> "A 30,000 by 30,000 multiplication table has nine hundred million cells. You can't
> build it, and you don't need to. **Row `i` is just `i, 2i, 3i, ...`**, so how many
> cells in that row are at most `x` is one division. Yesterday's value search, with a
> matrix that only exists in arithmetic."

## 📋 Problem, in your words
```
The m x n multiplication table has table[i][j] = i * j (1-indexed).
Return the kth smallest number in it (duplicates count separately).

m, n up to 3 * 10^4, so the table has up to 9 * 10^8 cells.
```

## 🔢 The example
```
Input:  m = 3, n = 3, k = 5
Table:  1  2  3
        2  4  6
        3  6  9
Sorted: 1 2 2 3 3 4 6 6 9      -> the 5th is 3
Output: 3

Input:  m = 2, n = 3, k = 6  -> 6   (the largest cell, 2 * 3)
```

## 🧸 ELI5
> Row 2 of the table is the 2-times table: 2, 4, 6, 8, ... How many of those are 5 or
> less? You don't count them one by one. You ask *"how many 2s fit in 5?"*: `5 // 2 = 2`.
> The only catch is that the row stops at `n` entries, so it's `min(5 // 2, n)`.
>
> ```
> how many cells are <= 5?     (m = n = 3)
>
> row 1:  1  2  3      5 // 1 = 5, but only 3 cells  -> 3
> row 2:  2  4  6      5 // 2 = 2                    -> 2
> row 3:  3  6  9      5 // 3 = 1                    -> 1
>                                              total    6
> ```
>
> Then it's the EP91 game: shout a number, count who's at most that, go up or down.

## 🐌 Brute force (say it, don't type it)
Build all `m · n` products and sort: **O(mn log mn)** time and **O(mn)** memory, nine
hundred million integers at the limit. A heap merging the rows (EP102's approach) is
**O(k log m)**, and k can be `m · n` too. The value search is **O(m log(mn))**, about
30,000 × 30 operations.

## 💡 The pattern reveal
**Signal:** "kth smallest" in a table sorted along rows and columns · the table is too
big to store.
**Therefore:** Shape D / C, EP91's value search with an arithmetic count.

| decision | here |
|---|---|
| what is `x`? | a candidate value |
| what is `feasible(x)`? | `count_le(x) >= k` |
| how do I count? | `sum(min(x // i, n) for i in 1..m)`, row `i` holds multiples of `i` |
| what is the range? | `[1, m * n]`, the top-left and bottom-right cells |

**Key insight:** EP91 needed the staircase because matrix values were arbitrary. Here
row `i` is an arithmetic sequence, so "how many are `<= x`" has a closed form. Same
search, cheaper count, and no matrix in memory at all.

Same guarantee as EP91: the smallest `x` with `count_le(x) >= k` is always an actual
product, because if it weren't, `x - 1` would have the same count.

## 🔍 Dry run: `m = n = 3`, `k = 5`
Range `[1, 9]`.

| step | lo | hi | mid | per row `min(mid // i, 3)` | count | ≥ 5? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 9 | 5 | 3, 2, 1 | 6 | ✓ | `hi = 5` |
| 2 | 1 | 5 | 3 | 3, 1, 1 | 5 | ✓ | `hi = 3` |
| 3 | 1 | 3 | 2 | 2, 1, 0 | 3 | ✗ | `lo = 3` |
| - | 3 | 3 | stop | | | | answer **3** ✓ |

Check against the sorted list: `1 2 2 3 3 ...`, three values `<= 2` and five `<= 3`.
The 5th smallest is the first value whose count reaches 5.

## ✅ Optimal solution
```python
class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        """kth smallest entry of the m x n multiplication table.

        Time:  O(m log(mn)): log(mn) guesses, each counted row by row in O(m).
        Space: O(1), the table is never built.
        """
        def count_le(x: int) -> int:
            # row i is i, 2i, ..., n*i: x // i of them are <= x, capped at n
            return sum(min(x // i, n) for i in range(1, m + 1))

        lo, hi = 1, m * n
        while lo < hi:
            mid = (lo + hi) // 2
            if count_le(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
```
**Time:** O(m log(mn)) · **Space:** O(1)

## ⚠️ Gotchas
- **`min(x // i, n)`.** Without the cap, row 1 with `x = 5` counts 5 cells in a row of
  3. The count is inflated and the answer comes out too small.
- **1-indexed rows.** `range(1, m + 1)`; `range(m)` divides by zero on the first row.
- **Loop over the smaller dimension.** The table is symmetric, so swap `m` and `n` if
  `m > n` for O(min(m, n)) per count. Mention it; it's a free win.
- **`>= k`.** Duplicates (`2` appears twice, `3` twice) make the count jump by more
  than one, same as EP91.

## 🎤 Interview talking points
- *"I can't build nine hundred million cells, so I binary search the value and count
  cells `<= x` per row."*
- *"Row `i` is the multiples of `i`, so its count is `min(x // i, n)`, O(1) per row."*
- *"This is Kth Smallest in a Sorted Matrix where the staircase is replaced by
  arithmetic."* ← naming the family.
- *"The result is always a real product: the smallest value with count ≥ k can't be
  missing from the table."*

## 🔗 Transfer
EP91 and EP92 are one idea: search the value, count with whatever the structure gives
you. That idea generalises further than it looks: "kth smallest pair distance" and
"kth smallest prime fraction" are the same loop with a two-pointer count. Tomorrow,
EP93 Median of Two Sorted Arrays, is the pattern's finale: Shape C where `x` is a
**cut position**.

## 📹 Metadata
- **Title:** `Kth Smallest in a Multiplication Table, a matrix that never exists | Binary Search #22`
- **Thumbnail:** `min(x // i, n)` (green block)
- **Short:** "how many 2s fit in 5?", the three rows collapsing into one division each. 35s.
