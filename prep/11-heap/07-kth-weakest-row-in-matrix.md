# EP100 · P11E07 · The K Weakest Rows in a Matrix   [Easy]

**Pattern:** Heap (k-closest) · **Link:** https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/description/

---

## 🎬 Hook
> "Two tools, two directions. **Binary search down each row** to count soldiers, because
> the row is sorted. **A heap across the rows** to keep the k weakest, because the rows
> aren't. Yesterday was 'check if it's sorted'. Today the answer is: *parts* of it are."

## 📋 Problem, in your words
```
A binary matrix: each row is soldiers (1s) followed by civilians (0s),
so every row looks like 1 1 1 0 0.

Row i is weaker than row j if it has fewer soldiers, or the same number
and i < j. Return the indices of the k weakest rows, weakest first.
```

## 🔢 The example
```
Input:  mat = [[1,1,0,0,0],     row 0: 2 soldiers
               [1,1,1,1,0],     row 1: 4
               [1,0,0,0,0],     row 2: 1
               [1,1,0,0,0],     row 3: 2
               [1,1,1,1,1]],    row 4: 5
        k = 3
Output: [2, 0, 3]
Why:    1 soldier (row 2), then 2 soldiers (rows 0 and 3, lower index first)
```

## 🧸 ELI5
> Five castles, and each has its soldiers lined up at the **front of the gate**, then
> the civilians behind them. You want to attack the **3 weakest**.
>
> Counting soldiers: you don't walk the whole line. You jump to the middle and ask
> "soldier or civilian?", then half again, and in a few jumps you've found where the
> soldiers end. That's binary search.
>
> Picking the weakest: you keep a list of 3 castles, and whenever there are 4 on it,
> you cross off **the strongest**.
>
> ```
> castle:     0   1   2   3   4
> soldiers:   2   4   1   2   5
> keep 3:     cross off 1 (4 soldiers), then cross off 4 (5 soldiers)
> left:       2 (1), 0 (2), 3 (2)   -> weakest first: [2, 0, 3]
> ```

## 🐌 Brute force (say it, don't type it)
`sum(row)` for each row, then sort indices by `(soldiers, index)` and take k.
**O(m·n + m log m)**. Honestly, it's what most accepted answers do, and on a 100 × 100
grid it's fine. The episode is about the two upgrades: **log n** per row instead of n,
and **log k** per row instead of log m.

## 💡 The pattern reveal
**Signal:** "k **weakest**" · each row is **sorted** (1s then 0s).
**Therefore:** binary search to compute the key, then Shape B (k smallest by key).

**Key insight:** the key is `(soldiers, index)`, and it's the k **smallest** keys you
want, so the heap is a **max**-heap of size k that evicts the strongest. Negate both
parts:

```python
heapq.heappush(heap, (-soldiers, -i))     # top = most soldiers, then highest index
if len(heap) > k:
    heapq.heappop(heap)                   # evict the strongest
```

Negating the index is the detail: among equal soldiers, the **higher** index is
stronger (it loses the tie), so it must come off first.

Soldier count = the index of the first 0, a lower-bound search:

```python
lo, hi = 0, len(row)
while lo < hi:
    mid = (lo + hi) // 2
    if row[mid] == 1:
        lo = mid + 1        # still soldiers: the first 0 is further right
    else:
        hi = mid
# lo = number of soldiers
```

## 🔍 Dry run: the example, `k = 3`
Heap shown as `(soldiers, index)`, real values:

| row | soldiers | heap after push | size > 3? evict (strongest) | heap after |
|---|---|---|---|---|
| 0 | 2 | {(2,0)} | - | {(2,0)} |
| 1 | 4 | {(2,0), (4,1)} | - | {(2,0), (4,1)} |
| 2 | 1 | {(1,2), (2,0), (4,1)} | - | {(1,2), (2,0), (4,1)} |
| 3 | 2 | {(1,2), (2,0), (2,3), (4,1)} | evict **(4, 1)** | {(1,2), (2,0), (2,3)} |
| 4 | 5 | {…, (5,4)} | evict **(5, 4)** | {(1,2), (2,0), (2,3)} |

Pop everything: strongest first → `3, 0, 2`. Reverse → **`[2, 0, 3]`** ✓.

## ✅ Optimal solution
```python
class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        """Indices of the k weakest rows, weakest first.

        Time:  O(m log n + m log k), a binary search per row, a heap op per row.
        Space: O(k).
        """
        heap = []                               # MAX-heap on (soldiers, index)
        for i, row in enumerate(mat):
            lo, hi = 0, len(row)                # soldiers = index of the first 0
            while lo < hi:
                mid = (lo + hi) // 2
                if row[mid] == 1:
                    lo = mid + 1
                else:
                    hi = mid

            heapq.heappush(heap, (-lo, -i))     # negate both: strongest on top
            if len(heap) > k:
                heapq.heappop(heap)             # evict the strongest

        weakest = []
        while heap:
            weakest.append(-heapq.heappop(heap)[1])   # comes out strongest first
        return weakest[::-1]
```
**Time:** O(m log n + m log k) · **Space:** O(k)

## ⚠️ Gotchas
- **Negate the index too.** `(-soldiers, i)` breaks ties the wrong way: on equal
  soldiers it evicts the *lower* index, which is the weaker one you wanted to keep.
- **Pop order is reversed.** A max-heap gives the strongest first; the answer wants
  weakest first. `[::-1]` at the end.
- **All-soldier row.** `[1,1,1,1,1]`: the search ends at `lo = len(row)` = 5, correct.
  `hi = len(row)`, not `len(row) - 1`, is what makes that work.
- **All-civilian row.** `[0,0,0]` gives 0. Test both edges.
- **`sum(row)` is fine in real life.** Say so. The binary search is the upgrade the
  interviewer is looking for because the rows are sorted.

## 🎤 Interview talking points
- *"Each row is sorted, so the soldier count is a lower-bound binary search: the index
  of the first 0."*
- *"Then k smallest by `(soldiers, index)`: max-heap of size k, both parts negated so
  the strongest, including the tie on index, is on top."*
- *"O(m log n + m log k). The simple version is O(m·n + m log m), and on small grids I'd
  honestly write that."*
- *"This is two patterns at once: binary search within a sorted row, heap across
  unsorted rows."*

## 🔗 Transfer
That's the k-closest family: EP98 computed a distance, EP99 noticed sortedness and
dropped the heap, EP100 used sortedness inside a row and the heap across rows. Tomorrow
(EP101, Merge K Sorted Arrays) starts the **heap as pointer** family: the heap stops
holding "the best k so far" and starts holding "the current front of each list".

## 📹 Metadata
- **Title:** `K Weakest Rows, binary search down, heap across | Heap #7`
- **Thumbnail:** `↓ search  → heap` (green block)
- **Short:** the castle gate, half-jumps to find where the soldiers end. 40s.
