# EP099 · P11E06 · Find K Closest Elements   [Medium]

**Pattern:** Heap (k-closest), and why you shouldn't use one · **Link:** https://leetcode.com/problems/find-k-closest-elements/description/

---

## 🎬 Hook
> "This is a heap episode where the heap is the **wrong answer**. It works, it's
> O(n log k), and it ignores the one word in the problem that matters: **sorted**. On
> sorted input the k closest are always **next to each other**, so the question
> becomes *where does the window start*, and that's binary search."

## 📋 Problem, in your words
```
Given a SORTED integer array arr, an integer k and a target x, return
the k elements closest to x, in ascending order.

  - "closer" means smaller |a - x|
  - tie on distance -> the smaller element wins
  - x may not be in the array, or even inside its range
```

## 🔢 The example
```
Input:  arr = [1, 2, 3, 4, 5], k = 4, x = 3
Output: [1, 2, 3, 4]
Why:    distances 2,1,0,1,2. 1 and 5 tie at 2; the smaller (1) wins.

Input:  arr = [1, 2, 3, 4, 5, 6, 7, 8, 9], k = 3, x = 6
Output: [5, 6, 7]

Input:  arr = [1, 1, 2, 3, 4, 5], k = 4, x = -1
Output: [1, 1, 2, 3]       <- x is off the left edge
```

## 🧸 ELI5
> Houses on a straight street, numbered in order. You live at number 6 and want to
> invite the **3 nearest** neighbours. Would you ever invite number 5 and number 8 but
> **skip** number 7? Never: 7 is between you and 8, so it's closer.
>
> So the guests are always a **block of houses in a row**. You don't need to rank every
> house on the street; you just need to decide where the block **starts**.
>
> ```
> street:  1  2  3  4  5  6  7  8  9
>                      [5  6  7]         <- a window of 3 with no gaps
> ```
>
> To decide, compare the two houses **just outside** each possible edge: if the house
> at the left edge is farther from you than the house just past the right edge, slide
> the whole block right.

## 🐌 Brute force (say it, don't type it)
Two "brute" answers, both worth naming:
1. Sort by `(|a - x|, a)`, take k, sort again: **O(n log n)**.
2. The heap from EP98: max-heap on `(|a - x|, a)` of size k, then sort the k:
   **O(n log k + k log k)**.

Both treat the array as if it were a random bag. The sorted order is free information
they throw away.

## 💡 The pattern reveal
**Signal:** "k closest" **+ "sorted array"**.
**Therefore:** not a heap. The answer is a **contiguous window**, so binary search for
its **left edge** (Pattern 10 thinking, borrowed into Pattern 11).

**Key insight:** the window starts somewhere in `[0, n - k]`. For a candidate start
`mid`, compare the element you'd **drop** on the left, `arr[mid]`, with the element
you'd **gain** on the right, `arr[mid + k]`:

```python
if x - arr[mid] > arr[mid + k] - x:     # left edge is strictly farther
    lo = mid + 1                        # the window must start further right
else:
    hi = mid                            # mid (or earlier) is good enough
```

Ties go left (`>` not `>=`), which gives "smaller element wins" for free.

**🧨 The trap: no `abs()`.** It's tempting to write `abs(x - arr[mid]) >
abs(arr[mid + k] - x)`. With duplicates it's wrong: `arr = [1,1,2,2,2,2,2,3,3]`,
`k = 3`, `x = 3` returns `[2, 2, 2]` instead of `[2, 3, 3]`. The signed version works
because `arr[mid] <= arr[mid + k]`, so the two signed differences say *which side of x*
each element is on, not just how far.

## 🔍 Dry run: `arr = [1..9]`, `k = 3`, `x = 6`
`lo = 0`, `hi = n - k = 6`.

| lo | hi | mid | arr[mid] | arr[mid+k] | x - arr[mid] | arr[mid+k] - x | move |
|---|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 4 | 7 | 2 | 1 | 2 > 1 → `lo = 4` |
| 4 | 6 | 5 | 6 | 9 | 0 | 3 | no → `hi = 5` |
| 4 | 5 | 4 | 5 | 8 | 1 | 2 | no → `hi = 4` |

`lo == hi == 4`. Answer `arr[4:7]` = **`[5, 6, 7]`** ✓. Already sorted, no second
sort needed.

## ✅ Optimal solution
```python
class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        """k elements of a sorted array closest to x, ascending; ties -> smaller.

        Time:  O(log(n - k) + k), binary search the window start, then slice.
        Space: O(1) beyond the output.
        """
        lo, hi = 0, len(arr) - k            # every legal window start
        while lo < hi:
            mid = (lo + hi) // 2
            # signed on purpose: arr[mid] <= arr[mid + k], so this compares the
            # element we'd drop on the left with the one we'd gain on the right
            if x - arr[mid] > arr[mid + k] - x:
                lo = mid + 1                # left edge strictly farther: slide right
            else:
                hi = mid                    # ties stay left: smaller element wins

        return arr[lo:lo + k]
```
**Time:** O(log(n − k) + k) · **Space:** O(1) extra

## ⚠️ Gotchas
- **`hi = n - k`, not `n - 1`.** The window must fit: `mid + k` is read, so `mid` can be
  at most `n - k - 1` inside the loop, and `lo` can end at `n - k`.
- **No `abs`.** See the trap above. Keep the duplicate test in your pocket.
- **`>` not `>=`.** `>=` sends ties right and breaks the "smaller wins" rule: `[1,2,3,4,5]`,
  k = 4, x = 3 returns `[2,3,4,5]`.
- **x outside the array.** `x = -1` drives `hi` down to 0; `x = 100` drives `lo` up to
  `n - k`. Both work without special cases. Show one.
- **The heap is still a valid answer.** If you blank on the binary search, the heap
  passes. Say "this is O(n log k); the sorted input lets me do better" and then try.

## 🎤 Interview talking points
- *"The input is sorted, so the k closest must be contiguous. I binary search the left
  edge of the window over `[0, n - k]`."*
- *"At each mid I compare what I'd drop on the left with what I'd gain on the right.
  Signed differences, not absolute, because of duplicates."*
- *"O(log(n - k) + k). The heap would be O(n log k) and wouldn't use the sortedness."*
- *"The general rule: before reaching for a heap, check whether the input is sorted
  and the answer is contiguous."* ← the lesson of the episode.

## 🔗 Transfer
This is the anti-signal episode from the pattern card: sorted input and a contiguous
answer beat a heap. Tomorrow (EP100, Kth Weakest Row) uses **both** tools: binary search
*inside* each sorted row to get a key, then a heap *across* rows to pick the k weakest.
The binary search here is the same left-edge search you built in Pattern 10 (EP73,
first and last position).

## 📹 Metadata
- **Title:** `K Closest Elements, when the heap is the WRONG answer | Heap #6`
- **Thumbnail:** `sorted? no heap` (red block)
- **Short:** the street of houses and the window sliding to [5, 6, 7]. 45s.
