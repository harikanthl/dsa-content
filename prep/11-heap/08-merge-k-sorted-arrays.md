# EP101 · P11E08 · Merge K Sorted Arrays   [Medium]

**Pattern:** Heap (heap as pointer) · **Link:** https://www.geeksforgeeks.org/problems/merge-k-sorted-arrays/1

---

## 🎬 Hook
> "Merging **two** sorted arrays is two pointers: compare the fronts, take the smaller.
> Merging **k** of them is the same thing, except now you'd compare k fronts every
> step. So put the k fronts **in a heap**, and 'which front is smallest' costs log k
> instead of k."

## 📋 Problem, in your words
```
Given k sorted arrays, return one sorted array with every element.

  - GfG gives a k x k matrix; the code works for any lengths
  - duplicates are kept
  - don't just concatenate and sort (that's the brute force)
```

## 🔢 The example
```
Input:  [[1, 4, 7],
         [2, 5, 8],
         [3, 6, 9]]
Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

Input:  [[1, 2, 3, 4], [2, 2, 3, 4], [5, 5, 6, 6], [7, 8, 9, 9]]
Output: [1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 9, 9]
```

## 🧸 ELI5
> Three checkout queues at a supermarket, and in each queue people are already lined up
> **shortest to tallest**. You want one single line of everyone, shortest to tallest.
>
> You don't need to look at everyone. The shortest person overall must be **at the
> front of one of the three queues**. So you only ever look at the three people at the
> front, pull out the shortest, and the person behind them steps up.
>
> ```
> queue 0:  1  4  7          fronts: 1, 2, 3  -> take 1 (queue 0), 4 steps up
> queue 1:  2  5  8          fronts: 4, 2, 3  -> take 2 (queue 1), 5 steps up
> queue 2:  3  6  9          fronts: 4, 5, 3  -> take 3 (queue 2), 6 steps up
>                            fronts: 4, 5, 6  -> take 4 ...
> ```
>
> The heap is the bouncer who always knows which of the fronts is shortest.

## 🐌 Brute force (say it, don't type it)
Concatenate everything and sort: **O(N log N)** for N total elements. It throws away
the fact that each array is already sorted. The other brute force, "scan all k fronts
each step", is **O(N·k)**. The heap gets **O(N log k)**.

## 💡 The pattern reveal
**Signal:** "merge **k sorted**".
**Therefore:** Shape C, heap as a merged pointer.

**Key insight:** the heap holds **one entry per array**, its current front, as
`(value, which array, index in that array)`. Pop the smallest, then push the **next
element from the same array**. The heap never holds more than k things.

```python
val, i, j = heapq.heappop(heap)
out.append(val)
if j + 1 < len(arr[i]):
    heapq.heappush(heap, (arr[i][j + 1], i, j + 1))    # that queue steps up
```

`i` and `j` aren't just bookkeeping. `i` also breaks ties between equal values from
different arrays, so the tuple never has to compare anything but ints.

## 🔍 Dry run: `[[1,4,7],[2,5,8],[3,6,9]]`
Seed: `heapify([(1,0,0), (2,1,0), (3,2,0)])`.

| pop | from (array, idx) | push successor | heap after (values) | out |
|---|---|---|---|---|
| 1 | (0, 0) | 4 from (0, 1) | {2, 3, 4} | 1 |
| 2 | (1, 0) | 5 from (1, 1) | {3, 4, 5} | 1 2 |
| 3 | (2, 0) | 6 from (2, 1) | {4, 5, 6} | 1 2 3 |
| 4 | (0, 1) | 7 from (0, 2) | {5, 6, 7} | … 4 |
| 5 | (1, 1) | 8 from (1, 2) | {6, 7, 8} | … 5 |
| 6 | (2, 1) | 9 from (2, 2) | {7, 8, 9} | … 6 |
| 7 | (0, 2) | array 0 empty | {8, 9} | … 7 |
| 8 | (1, 2) | array 1 empty | {9} | … 8 |
| 9 | (2, 2) | array 2 empty | {} | … 9 |

Answer **`[1..9]`** ✓. The heap size is 3 for six steps, then drains as arrays run out.

## ✅ Optimal solution
```python
import heapq

def merge_k_arrays(arr: list[list[int]], k: int) -> list[int]:
    """Merge k sorted arrays into one sorted list.

    Time:  O(N log k), N total elements, each pushed and popped once on a heap of <= k.
    Space: O(k) for the heap, plus O(N) for the output.
    """
    # one entry per array: (current front value, which array, index in it)
    heap = [(row[0], i, 0) for i, row in enumerate(arr) if row]
    heapq.heapify(heap)

    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(arr[i]):
            heapq.heappush(heap, (arr[i][j + 1], i, j + 1))   # advance THAT array

    return out
```
**Time:** O(N log k) · **Space:** O(k) + output

## ⚠️ Gotchas
- **Push from the same array you popped from.** Pushing "the next smallest overall"
  isn't something you can know. `i` in the tuple is how you know where to look.
- **`if row` when seeding.** An empty array has no `row[0]`. GfG's are all k long;
  LeetCode's linked-list version (LC 23) has empty lists.
- **Tie-breaker.** `(val, i, j)` never compares beyond ints. For LC 23 with list
  **nodes**, `(node.val, node)` crashes on equal values because nodes don't define `<`.
  Use `(node.val, i, node)`.
- **`heapify` the seed.** k pushes would be O(k log k); `heapify` is O(k). Small, but
  it's the same point as EP97.

## 🎤 Interview talking points
- *"The heap holds one entry per array: the current front. Pop the smallest, push that
  array's next element."*
- *"O(N log k). Concatenate-and-sort is O(N log N); comparing all fronts each step is
  O(N·k)."*
- *"The alternative is divide and conquer: merge arrays in pairs like merge sort, log k
  rounds of O(N) each, also O(N log k), and no heap."* ← good second answer.
- *"I include the array index in the tuple so ties never compare the payload."*

## 🔗 Transfer
This is the k-way merge that powers external sorting and log merging in real systems.
Tomorrow (EP102) points the same heap at a **sorted matrix**, rows as the k arrays, and
stops after k pops instead of merging everything. EP91 solved that exact problem with
binary search on the value, so tomorrow is a head-to-head.

## 📹 Metadata
- **Title:** `Merge K Sorted Arrays, a heap of the fronts | Heap #8`
- **Thumbnail:** `only the fronts` (green block)
- **Short:** the three supermarket queues and the bouncer. 45s.
