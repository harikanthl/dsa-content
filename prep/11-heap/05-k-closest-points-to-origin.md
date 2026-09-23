# EP098 · P11E05 · K Closest Points to Origin   [Medium]

**Pattern:** Heap (k-closest) · **Link:** https://leetcode.com/problems/k-closest-points-to-origin/description/

---

## 🎬 Hook
> "Find the k points nearest the origin. It's top-k with a **distance** for a key, and
> it has two free wins in it: you never need a square root, and the heap you want is the
> one that keeps the **farthest** point on top."

## 📋 Problem, in your words
```
Given a list of points [x, y] on a plane and k, return the k points
closest to (0, 0).

  - distance is ordinary Euclidean: sqrt(x^2 + y^2)
  - any order of output is fine
  - the answer is guaranteed unique
```

## 🔢 The example
```
Input:  points = [[1, 3], [-2, 2]], k = 1
Output: [[-2, 2]]
Why:    1 + 9 = 10 vs 4 + 4 = 8; 8 is closer

Input:  points = [[3, 3], [5, -1], [-2, 4]], k = 2
Output: [[3, 3], [-2, 4]]
Why:    squared distances 18, 26, 20 -> keep 18 and 20
```

## 🧸 ELI5
> Three friends are lost in a park and the ice-cream van can only pick up the **2
> nearest**. The driver keeps two seats. Each new friend who calls in gets a seat, and
> if the van is over-full, **the one farthest away** gets told to walk.
>
> The driver doesn't need a tape measure accurate to the centimetre, only *"who's
> farther?"* And if one friend is farther, their **distance squared** is farther too, so
> skip the square root.
>
> ```
> (3,3)  -> 18       seats: [18]
> (5,-1) -> 26       seats: [18, 26]
> (-2,4) -> 20       seats: [18, 20, 26] -> 26 walks
> ```

## 🐌 Brute force (say it, don't type it)
`sorted(points, key=lambda p: p[0]**2 + p[1]**2)[:k]`: **O(n log n)**. Fine as an
opener. The heap keeps only k points and is **O(n log k)**, which matters when n is a
million GPS pings and k is 10.

## 💡 The pattern reveal
**Signal:** "k **closest**" · a distance you can compute per item.
**Therefore:** Shape B on the pattern card: top-k with a distance key.

**Key insight:** it's EP94 (k *smallest*), with the key being distance. Keeping the k
smallest distances means evicting the **largest** one, so it's a **max-heap on
distance**: push `-d`.

```python
d = x * x + y * y                       # no sqrt: same ordering, no floats
heapq.heappush(heap, (-d, x, y))        # max-heap on distance
if len(heap) > k:
    heapq.heappop(heap)                 # evict the farthest
```

Push `(-d, x, y)`, not `(-d, [x, y])`. If two points tie on distance, Python compares
the next element, and ints always compare. It's the habit the pattern card's gotcha #2
is about.

## 🔍 Dry run: `points = [[3, 3], [5, -1], [-2, 4]]`, `k = 2`

| point | d = x² + y² | push | heap (as real distances) | size > 2? evict |
|---|---|---|---|---|
| (3, 3) | 18 | (-18, 3, 3) | {18} | - |
| (5, -1) | 26 | (-26, 5, -1) | {18, 26}, top = 26 | - |
| (-2, 4) | 20 | (-20, -2, 4) | {18, 20, 26}, top = 26 | evict **(5, -1)** |

Heap left: `(3, 3)` and `(-2, 4)`. Answer **`[[3, 3], [-2, 4]]`** ✓ (any order).

## ✅ Optimal solution
```python
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """The k points nearest the origin, any order.

        Time:  O(n log k), heap never exceeds k + 1.
        Space: O(k).
        """
        heap = []                               # MAX-heap on squared distance
        for x, y in points:
            d = x * x + y * y                   # sqrt is monotone, so skip it
            heapq.heappush(heap, (-d, x, y))
            if len(heap) > k:
                heapq.heappop(heap)             # drop the farthest of the k + 1

        return [[x, y] for _, x, y in heap]
```
**Time:** O(n log k) · **Space:** O(k)

## ⚠️ Gotchas
- **No `sqrt`.** It's slower, introduces floats, and changes nothing: if a < b then
  √a < √b. Say "monotone" out loud.
- **Max-heap, so `-d`.** A plain `(d, x, y)` keeps the k *farthest*. It's EP95's
  mistake in reverse.
- **Tuple, not nested list.** `(-d, [x, y])` works until two distances tie, then Python
  compares lists, which happens to work for lists of ints, but it's a habit that
  crashes on anything else. Flat ints are always safe.
- **Negative coordinates.** `(-2)² = 4`. Squaring handles the sign; `abs(x) + abs(y)` is
  Manhattan distance, a different problem.

## 🎤 Interview talking points
- *"Max-heap of size k on squared distance. The top is the farthest I'm keeping, so
  it's the one I evict."*
- *"No square root: it's monotone, so it doesn't change the order."*
- *"O(n log k), O(k) space, streams fine."*
- *"Quickselect on distance is O(n) average if they want to push, same caveats as
  EP95."*

## 🔗 Transfer
Tomorrow's problem also says "k closest", and a heap solves it, but it's the **wrong**
tool: EP99's input is **sorted**, and sorted input means the k closest are a contiguous
window you can find with binary search. The whole point of EP99 is to check for
sortedness before typing `heapq`.

## 📹 Metadata
- **Title:** `K Closest Points, no square roots needed | Heap #5`
- **Thumbnail:** `sqrt? skip it` (green block)
- **Short:** the ice-cream van seats, 26 told to walk. 35s.
