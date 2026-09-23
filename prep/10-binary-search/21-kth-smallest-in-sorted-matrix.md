# EP091 · P10E21 · Kth Smallest Element in a Sorted Matrix   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/

---

## 🎬 Hook
> "Find the 8th smallest number in a matrix, without sorting it and without a heap. You
> don't search **positions**, because in this matrix positions don't line up with rank.
> You search **values**: guess a number, count how many cells are at most that, and
> halve. The count is yesterday's staircase."

## 📋 Problem, in your words
```
n x n matrix, every row sorted ascending, every column sorted ascending.
Return the kth smallest element (counting duplicates: kth in sorted order,
not kth distinct).

Aim for better than O(n^2) memory.
```

## 🔢 The example
```
matrix = [[ 1,  5,  9],
          [10, 11, 13],
          [12, 13, 15]],   k = 8

Output: 13
Why:    sorted: 1 5 9 10 11 12 13 13 15
                               ^  ^
                           7th  8th   -> the 8th is 13 (the second 13)

matrix = [[-5]], k = 1  -> -5
```

## 🧸 ELI5
> You want the 8th shortest kid in a school where every row and every column is lined up
> by height, but the rows don't continue each other. So you don't try to find "position
> 8". You shout a height instead:
>
> ```
> "everyone 12 or shorter, stand up!"   -> 6 kids stand.   not enough, go taller
> "everyone 14 or shorter, stand up!"   -> 8 kids stand.   enough, maybe go shorter
> "everyone 13 or shorter, stand up!"   -> 8 kids stand.   enough, maybe go shorter
> ```
>
> The shortest height where **at least 8 kids** stand up is the answer. As the height
> goes up, the count only grows, so "at least 8?" flips once: **no, no, yes, yes**.
> That's binary search on the height.

## 🐌 Brute force (say it, don't type it)
Flatten and sort: **O(n² log n)** time, **O(n²)** space. Better: a max-heap of size k,
or a min-heap merging the rows (that's EP102's episode, O(k log n)). The value search
is **O(n log(max − min))** time and **O(1)** space, and the counting step is the
staircase you already know.

## 💡 The pattern reveal
**Signal:** "kth smallest" in something sorted in **two directions**.
**Therefore:** Shape D / C, binary search on the **value**, count with the staircase.

| decision | here |
|---|---|
| what is `x`? | a candidate **value** (not an index) |
| what is `feasible(x)`? | `count_le(x) >= k`: at least k cells are `<= x` |
| why monotonic? | a bigger `x` can only count more cells |
| what is the range? | `[matrix[0][0], matrix[-1][-1]]`, the corners are the min and max |

**Counting `<= x` in O(n)** with EP90's staircase, starting top-right: for each row,
slide left past the cells bigger than `x`; everything left of the pointer counts. The
column pointer only ever moves left, so the whole count is O(n), not O(n²).

```python
count, c = 0, n - 1
for r in range(n):
    while c >= 0 and matrix[r][c] > x:
        c -= 1                     # this cell and everything below it is > x
    count += c + 1                 # cells 0..c in this row are <= x
```

**🧨 Why the answer is a real matrix value:** the loop returns the *smallest* `x` with
`count_le(x) >= k`. If that `x` weren't in the matrix, `x - 1` would have exactly the
same count, so `x` wouldn't be the smallest. Say this; it's the question you'll get.

## 🔍 Dry run: the matrix above, `k = 8`
Range `[1, 15]`.

| step | lo | hi | mid | ≤ mid per row | count | ≥ 8? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 15 | 8 | 2, 0, 0 | 2 | ✗ | `lo = 9` |
| 2 | 9 | 15 | 12 | 3, 2, 1 | 6 | ✗ | `lo = 13` |
| 3 | 13 | 15 | 14 | 3, 3, 2 | 8 | ✓ | `hi = 14` |
| 4 | 13 | 14 | 13 | 3, 3, 2 | 8 | ✓ | `hi = 13` |
| - | 13 | 13 | stop | | | | answer **13** ✓ |

Step 3 is the argument in action: **14 isn't in the matrix**, and it has the same count
as 13. The search didn't stop at 14 because 14 isn't the *smallest* value with count 8.

## ✅ Optimal solution
```python
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        """kth smallest value in a row- and column-sorted n x n matrix.

        Time:  O(n log R), R = max - min: log R guesses, each counted in O(n).
        Space: O(1).
        """
        n = len(matrix)

        def count_le(x: int) -> int:
            count, c = 0, n - 1             # staircase from the top-right
            for r in range(n):
                while c >= 0 and matrix[r][c] > x:
                    c -= 1                  # never moves right again: rows below are bigger
                count += c + 1
            return count

        lo, hi = matrix[0][0], matrix[-1][-1]
        while lo < hi:
            mid = (lo + hi) // 2
            if count_le(mid) >= k:
                hi = mid                    # at least k values <= mid; answer is mid or less
            else:
                lo = mid + 1
        return lo
```
**Time:** O(n log R) · **Space:** O(1)

## ⚠️ Gotchas
- **`>= k`, not `== k`.** Duplicates make the count jump: `count_le(12) = 6` and
  `count_le(13) = 8`, so **no** value has count exactly 7. Ask for `k = 7` with `==`
  and the search never succeeds; with `>=` it returns 13, which is right.
- **`(lo + hi) // 2` with negatives.** Python's `//` floors toward −∞, so it's safe for
  `lo = -5, hi = -4`. In Java/C++ integer division truncates toward 0: use
  `lo + (hi - lo) / 2`.
- **The column pointer must not reset per row.** Resetting makes the count O(n²) and
  the whole thing O(n² log R), worse than the heap.
- **Range is values, not indices.** `lo, hi = 0, n*n - 1` is the classic slip from
  EP89's habits.

## 🎤 Interview talking points
- *"Positions don't correspond to rank here, so I binary search the value and ask how
  many cells are at most that value."*
- *"Counting is the staircase from Search 2D Matrix II: O(n) per guess because the
  column pointer only moves left."*
- *"The smallest value with count ≥ k must be in the matrix: otherwise one less would
  have the same count."* ← the proof they want.
- *"The heap approach is O(k log n); which is better depends on k and the value range.
  For k near n², the value search wins."*

## 🔗 Transfer
Shape C came back, searching a value with a count as the check, and EP90's staircase
became the check. Tomorrow's EP92 is the same search where the matrix is never even
stored: the multiplication table counts with `min(x // i, n)`. And in the Heap pattern,
**EP102 is this exact problem solved with a min-heap**: one pointer per row, pop k
times. Solve it both ways and compare on camera.

## 📹 Metadata
- **Title:** `Kth Smallest in a Sorted Matrix, search values not positions | Binary Search #21`
- **Thumbnail:** `COUNT ≤ x` (green block)
- **Short:** the "stand up if you're 13 or shorter" moment, and 14 having the same count. 45s.
