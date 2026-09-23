# EP102 · P11E09 · Kth Smallest Element in a Sorted Matrix   [Medium]

**Pattern:** Heap (heap as pointer) · **Link:** https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/

---

## 🎬 Hook
> "You've solved this before. In EP91 you binary searched on the **value**. Today you
> solve it again with yesterday's k-way merge, and stop after k pops. Same problem, two
> patterns, and the interesting part is **when each one wins**."

## 📋 Problem, in your words
```
An n x n matrix where every row AND every column is sorted ascending.
Return the k-th smallest element (1-indexed, duplicates count).

  - memory must be better than O(n^2): no flattening into one list
```

## 🔢 The example
```
Input:  matrix = [[ 1,  5,  9],
                  [10, 11, 13],
                  [12, 13, 15]], k = 8
Output: 13
Why:    flattened and sorted: 1 5 9 10 11 12 13 13 15 -> the 8th is 13

Input:  matrix = [[-5]], k = 1
Output: -5
```

## 🧸 ELI5
> It's EP101's supermarket, with the matrix rows as the queues. Each row is sorted, so
> it's a queue of people shortest-first. You don't want *everyone* in one line this
> time, you want to know **who is 8th**. So you run the same bouncer, pull out 7 people,
> and whoever is at the front of the pile now is 8th.
>
> ```
> row 0:  1  5  9
> row 1: 10 11 13
> row 2: 12 13 15
>
> pulled out in order:  1  5  9  10  11  12  13  | next up: 13  <- the 8th
> ```

## 🐌 Brute force (say it, don't type it)
Flatten and sort, `sorted(v for row in matrix for v in row)[k - 1]`: **O(n² log n)**
time and **O(n²)** memory, which the problem explicitly rules out. Using only the
"rows are sorted" half of the structure, the heap does much better.

## 💡 The pattern reveal
**Signal:** "k-th smallest" + "each row is **sorted**".
**Therefore:** Shape C, heap as pointer, over the rows, stopped after k − 1 pops.

**Key insight:** seed the heap with **column 0 of each row** (only the first
`min(n, k)` rows can possibly matter). Pop the smallest, push the element **to its
right**. After k − 1 pops, the heap's top is the k-th smallest.

```python
for _ in range(k - 1):
    val, r, c = heapq.heappop(heap)
    if c + 1 < n:
        heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))   # step right
return heap[0][0]
```

**The side-by-side with EP91:**

| | EP91 binary search on value | EP102 heap over rows |
|---|---|---|
| idea | guess a value, count how many are ≤ it using both sort orders | merge rows, stop at k |
| time | O(n · log(max − min)) | O(min(n,k) + k · log min(n,k)) |
| space | O(1) | O(min(n, k)) |
| wins when | k is large (near n²), or memory is tight | k is small |
| uses | rows **and** columns sorted | rows sorted only |

The last row of that table is the one to say on camera: the heap never uses the
column ordering at all, which is why it's simpler, and why it can't beat EP91 when k is
huge.

## 🔍 Dry run: the example, `k = 8`
Seed: `(1,r0,c0) (10,r1,c0) (12,r2,c0)`. Seven pops:

| pop # | popped (val, r, c) | push right | heap after (values) |
|---|---|---|---|
| 1 | (1, 0, 0) | 5 at (0, 1) | {5, 10, 12} |
| 2 | (5, 0, 1) | 9 at (0, 2) | {9, 10, 12} |
| 3 | (9, 0, 2) | row 0 done | {10, 12} |
| 4 | (10, 1, 0) | 11 at (1, 1) | {11, 12} |
| 5 | (11, 1, 1) | 13 at (1, 2) | {12, 13} |
| 6 | (12, 2, 0) | 13 at (2, 1) | {13, 13} |
| 7 | (13, 1, 2) | row 1 done | {13} |

Top after 7 pops: **`13`** ✓. Pop 6 → 7 shows the tie: two 13s, one from each row, and
the `r` in the tuple decides which comes first without ever comparing anything else.

## ✅ Optimal solution
```python
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        """k-th smallest in a row- and column-sorted n x n matrix.

        Time:  O(m + k log m), m = min(n, k) rows ever enter the heap.
        Space: O(m).
        """
        n = len(matrix)
        # only the first k rows can hold one of the k smallest (each row's head
        # is at least as big as every head above it)
        heap = [(matrix[r][0], r, 0) for r in range(min(n, k))]
        heapq.heapify(heap)

        for _ in range(k - 1):                  # throw away the k - 1 smallest
            val, r, c = heapq.heappop(heap)
            if c + 1 < n:
                heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))

        return heap[0][0]
```
**Time:** O(m + k log m), m = min(n, k) · **Space:** O(m)

## ⚠️ Gotchas
- **`k - 1` pops, then peek.** Or k pops and return the last popped value. Mixing the
  two (k pops, then peek) returns the (k+1)-th.
- **`min(n, k)` rows.** Seeding all n rows is still correct, just wasteful when k is
  small. The reason it's safe: the column is sorted, so row k+1's first element is at
  least as big as k other elements already.
- **Step right, not down.** Pushing both right and down double-counts cells unless you
  add a visited set. Rows as independent lists is the clean model.
- **k can be n².** Then the heap does n² pops, O(n² log n), and EP91 is clearly better.
  That's the talking point, not a bug.

## 🎤 Interview talking points
- *"Treat each row as a sorted list and k-way merge them, stopping after k − 1 pops. The
  top of the heap is the answer."*
- *"O(k log n). If k is small that's great; if k is close to n², I'd switch to binary
  search on the value range, which is O(n log(max − min)) and O(1) space."*
- *"The heap only uses the row ordering. The binary search uses both, which is why it
  scales better with k."*
- *"I'd ask how big k tends to be before picking."* ← the senior answer.

## 🔗 Transfer
This is the EP91 rematch the pattern card promised. EP91 (binary search on the answer)
counted "how many cells are ≤ mid" with a staircase walk; today's heap pops its way to
the answer directly. Keep both: EP92 (k-th smallest in a multiplication table) is the
same problem where the matrix is too big to even touch, and only EP91's approach
survives. Tomorrow starts the **greedy + heap** family with EP103, Last Stone Weight.

## 📹 Metadata
- **Title:** `Kth Smallest in a Sorted Matrix, heap vs binary search | Heap #9`
- **Thumbnail:** `EP91 vs EP102` (blue block)
- **Short:** the side-by-side table, with "k small → heap, k big → binary search". 40s.
