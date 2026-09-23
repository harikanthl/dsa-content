# EP109 · P11E16 · Find Median from Data Stream   [Hard]

**Pattern:** Heap (two heaps) · **Link:** https://leetcode.com/problems/find-median-from-data-stream/description/

---

## 🎬 Hook
> "Numbers arrive one at a time, and at any moment someone asks for the median. Keeping
> a sorted list costs O(n) per insert. Instead, split the numbers into a **lower half**
> and an **upper half**, and the median is always sitting on the **tops** of the two
> piles. Two heaps, three lines per insert, and not a single `if x < median`."

## 📋 Problem, in your words
```
Design a class with two methods:
  addNum(num)   -> add an integer from the stream
  findMedian()  -> the median of everything added so far

Median: the middle value, or the mean of the two middle values if the
count is even.
```

## 🔢 The example
```
addNum(1), addNum(2)  -> findMedian() = 1.5
addNum(3)             -> findMedian() = 2.0

Stream 5, 15, 1, 3, 8, medians after each: 5, 10, 5, 4, 5
```

## 🧸 ELI5
> A class lines up by height, but they arrive one at a time and you never want to
> re-sort the whole line. So you split them into two groups:
> - the **short group**, where you only ever need to know **the tallest** short kid;
> - the **tall group**, where you only ever need to know **the shortest** tall kid.
>
> Keep the groups the same size (the short group may have one extra). Then the middle
> kid is the tallest short kid, or halfway between the two group leaders.
>
> ```
>    short group        |      tall group
>    1   3   [5]        |      [8]   15
>            ^ tallest short     ^ shortest tall
> 5 kids, short group has one extra -> median = 5
> ```
>
> Every new kid goes into the short group first, then the tallest short kid is sent
> over to the tall group, then if the tall group got bigger, its shortest kid comes
> back. Three moves, and the groups are always correct.

## 🐌 Brute force (say it, don't type it)
Append to a list, sort on every `findMedian`: **O(n log n)** per query. Keep the list
sorted with `bisect.insort`: O(log n) to find the spot but **O(n)** to shift elements,
so O(n) per insert. The two heaps make every insert **O(log n)** and every query
**O(1)**.

## 💡 The pattern reveal
**Signal:** "**median**" · "**stream**" (data arrives over time, queries in between).
**Therefore:** Shape E, two heaps.

**Key insight:** two invariants, nothing else:
1. **Every element of `low` ≤ every element of `high`.**
2. **`len(low) - len(high)` is 0 or 1.**

`low` is a **max**-heap (negated) so its largest is on top; `high` is a min-heap so its
smallest is on top. The median is `low`'s top when the sizes differ, otherwise the mean
of both tops.

The add that keeps both invariants without branching on the value:

```python
heapq.heappush(self.low, -num)                            # 1. enter through low
heapq.heappush(self.high, -heapq.heappop(self.low))       # 2. low's max crosses over
if len(self.high) > len(self.low):                        # 3. rebalance sizes
    heapq.heappush(self.low, -heapq.heappop(self.high))
```

Step 2 is what makes invariant 1 hold for free: whatever just came in, the biggest of
`low` goes to `high`, so nothing in `low` can be bigger than what's in `high`.

## 🔍 Dry run: stream `5, 15, 1, 3, 8`

| add | after step 1 (low) | step 2: low's max → high | step 3: high bigger? | low | high | median |
|---|---|---|---|---|---|---|
| 5 | {5} | 5 → high | yes, 5 back | {5} | {} | **5** |
| 15 | {5, 15} | 15 → high | no | {5} | {15} | (5+15)/2 = **10** |
| 1 | {1, 5} | 5 → high | yes, 5 back | {1, 5} | {15} | **5** |
| 3 | {1, 3, 5} | 5 → high | no | {1, 3} | {5, 15} | (3+5)/2 = **4** |
| 8 | {1, 3, 8} | 8 → high | yes, 5 back | {1, 3, 5} | {8, 15} | **5** |

Row 3 is the one to narrate: 1 goes into `low`, but it's `5` that crosses, because
it's `low`'s max, and then comes back to rebalance. Values get shuffled; the invariants
never break.

## ✅ Optimal solution
```python
class MedianFinder:
    """Running median with two heaps.

    low:  MAX-heap (negated), the smaller half; may hold one extra.
    high: MIN-heap, the larger half.
    Invariants: max(low) <= min(high), and len(low) - len(high) in {0, 1}.

    addNum:     O(log n), at most three heap operations.
    findMedian: O(1), reads the tops.
    Space:      O(n).
    """

    def __init__(self):
        self.low = []
        self.high = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.low, -num)                          # always enter low
        heapq.heappush(self.high, -heapq.heappop(self.low))     # low's max -> high
        if len(self.high) > len(self.low):                      # keep low >= high
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```
**Time:** add O(log n), median O(1) · **Space:** O(n)

## ⚠️ Gotchas
- **`low` is the max-heap.** It holds the small numbers but you need its *largest*. Same
  logic as EP94: the top is the one at the boundary.
- **Negation discipline.** Three minus signs in `addNum`. The most common bug is moving
  from `high` to `low` without negating, which puts a positive number in a negated heap.
- **Which side gets the extra?** Pick one (`low` here) and make `findMedian` agree. If
  `add` lets `high` get the extra but `findMedian` reads `low`, odd counts are wrong.
- **`/ 2`, not `// 2`.** Integer division turns 1.5 into 1.
- **Branching on `num < median`** also works, but it has an empty-heap edge case on the
  first insert. The three-step add has none; that's why it's the template.

## 🎤 Interview talking points
- *"Two heaps: a max-heap for the lower half, a min-heap for the upper half. The median
  is on the tops."*
- *"Two invariants: everything in low ≤ everything in high, and low has the same size or
  one more."*
- *"Add is O(log n): push into low, move low's max to high, rebalance. Median is O(1)."*
- *"Follow-up: if all numbers are in 0..100, a count array of 101 buckets gives O(1)
  add and O(100) median. If 99% are in range, buckets for the range plus two heaps for
  the outliers."* ← the classic follow-up, have an answer.

## 🔗 Transfer
This is Shape E exactly as on the pattern card. Tomorrow (EP110, Sliding Window Median)
adds the one thing heaps can't do, **remove an element from the middle**, because in a
sliding window old numbers have to leave. The fix is lazy deletion, and it turns every
`len(heap)` in today's code into a lie you have to correct for. It's also Pattern 3's
sliding window meeting Pattern 11.

## 📹 Metadata
- **Title:** `Median from a Data Stream, the answer is on two tops | Heap #16`
- **Thumbnail:** `low | high` (blue block)
- **Short:** the short-group / tall-group split, and 5 crossing over and back. 50s.
