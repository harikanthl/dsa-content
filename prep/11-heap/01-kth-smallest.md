# EP094 · P11E01 · Kth Smallest Element   [Medium]

**Pattern:** Heap (top-k) · **Link:** https://www.geeksforgeeks.org/problems/kth-smallest-element5635/1

---

## 🎬 Hook
> "Find the 3rd smallest number in a million. Everyone sorts the whole million. You
> only ever need to remember **three** numbers, and the trick is to keep them in a
> **max**-heap, so the one you'd throw out is always sitting on top."

## 📋 Problem, in your words
```
Given an array of integers and a number k, return the k-th smallest
element (1-indexed: k = 1 is the minimum).

  - the array is NOT sorted
  - k is always valid: 1 <= k <= len(arr)
  - duplicates count separately: [1, 1, 2], k = 2 -> 1
```

## 🔢 The example
```
Input:  arr = [7, 10, 4, 3, 20, 15], k = 3
Output: 7
Why:    sorted it's [3, 4, 7, 10, 15, 20]; the 3rd one is 7

Input:  arr = [10, 5, 4, 3, 48, 6, 2, 33, 53, 10], k = 4
Output: 5              <- sorted: [2, 3, 4, 5, 6, 10, 10, ...]; the 4th is 5

Input:  arr = [5], k = 1
Output: 5
```
The first two are GfG's own examples.

## 🧸 ELI5
> You're picking the **3 shortest kids** for the front row of a class photo, and kids
> walk in one at a time. You keep three chairs. Whenever a fourth kid shows up, somebody
> has to leave, and it's always **the tallest of the four**.
>
> So the only question you ever ask is *"who's the tallest one sitting down?"* Keep that
> kid on top of the pile and the whole job is: sit the new kid down, and if there are
> four, send the tallest home.
>
> ```
> chairs (3):   7          7 10        4 7 10        3 4 7   <- 10 sent home
>                                                         ^ tallest in the chairs = the answer
> ```
>
> When everyone has walked in, the **tallest of the three shortest** is the 3rd
> shortest. That's the answer, and it's on top of the pile already.

## 🐌 Brute force (say it, don't type it)
`sorted(arr)[k - 1]`. **O(n log n)** time. It's correct and honestly fine for one
query, but it orders all n elements when you only care about k of them. The heap
version pays log k per element instead of log n, and uses O(k) memory, which matters
when the data is a stream you can't hold.

## 💡 The pattern reveal
**Signal:** "**k-th** smallest" · unsorted input.
**Therefore:** top-k, Shape A on the pattern card: a heap bounded at size k.

**Key insight:** the heap holds the k smallest seen so far, and its top must be the
one you'd **evict**. The one you evict from "the k smallest" is the **largest** of them.
So the k *smallest* live in a **max**-heap. And `heapq` only does min-heaps, so you
push `-x`.

```python
heapq.heappush(heap, -x)       # negate: heapq is a min-heap, we need a max-heap
if len(heap) > k:
    heapq.heappop(heap)        # evicts the LARGEST of the k + 1
```

At the end the top is the largest of the k smallest, which is the k-th smallest:
`-heap[0]`.

## 🔍 Dry run: `arr = [7, 10, 4, 3, 20, 15]`, `k = 3`

Showing the heap as real values (it stores negatives underneath):

| x | push, heap size | evict? | heap holds (real values) | top (`-heap[0]`) |
|---|---|---|---|---|
| 7 | 1 | - | {7} | 7 |
| 10 | 2 | - | {7, 10} | 10 |
| 4 | 3 | - | {4, 7, 10} | 10 |
| 3 | 4 > 3 | evict **10** | {3, 4, 7} | 7 |
| 20 | 4 > 3 | evict **20** (it was the biggest the moment it arrived) | {3, 4, 7} | 7 |
| 15 | 4 > 3 | evict **15** | {3, 4, 7} | 7 |

Answer **`7`** ✓. Rows 5 and 6 are the point: a big newcomer gets pushed and
immediately evicted. The heap never grows past k + 1.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def kthSmallest(self, arr, k):
        """k-th smallest element of an unsorted array (k is 1-indexed).

        Time:  O(n log k), n pushes, each on a heap of at most k + 1 entries.
        Space: O(k), the heap.
        """
        heap = []                       # MAX-heap (negated) of the k smallest so far
        for x in arr:
            heapq.heappush(heap, -x)
            if len(heap) > k:
                heapq.heappop(heap)     # drop the largest; k smallest remain

        return -heap[0]                 # largest of the k smallest = k-th smallest
```
**Time:** O(n log k) · **Space:** O(k)

## ⚠️ Gotchas
- **Max-heap for the smallest.** It feels backwards. Say it out loud: *"the top is the
  one I'd kick out, and I'd kick out the biggest."*
- **Negate on the way in AND the way out.** `-heap[0]`, not `heap[0]`. Forgetting the
  second minus returns `-7`.
- **Push, then pop if over.** Checking `if x < -heap[0]` before pushing is a valid
  micro-optimisation, but it needs an extra "is the heap full yet" branch. Push-then-trim
  has no branches to get wrong.
- **Duplicates are separate elements.** `[1, 1, 2]`, k = 2 gives 1. The heap handles it
  for free; a `set()` would break it.
- **1-indexed k.** `sorted(arr)[k]` in the brute force is an off-by-one that returns the
  (k+1)-th.

## 🎤 Interview talking points
- *"I keep a max-heap of the k smallest so far. Its top is the one I'd evict, so it's
  also the k-th smallest when I'm done."*
- *"O(n log k) instead of O(n log n), and O(k) memory, so it works on a stream."*
- *"`heapq` is min-only in Python, so I negate."* ← say this before they ask.
- *"If they want better average time: Quickselect is O(n) average, O(n²) worst case, and
  mutates the array. The heap is the predictable one."*
- *"If I could hold everything and k were close to n, I'd just sort."*

## 🔗 Transfer
This is the template for the whole pattern. Tomorrow, EP95 Kth Largest, is the same six
lines with the minus sign removed, and that tiny flip is where people get confused about
which heap to use. EP96 and EP97 keep the exact shape and change only *what* gets pushed.

## 📹 Metadata
- **Title:** `Kth Smallest, why the SMALLEST lives in a MAX-heap | Heap #1`
- **Thumbnail:** `MAX heap for min?` (red block)
- **Short:** the class-photo ELI5, three chairs, tallest kid sent home. 40s.
