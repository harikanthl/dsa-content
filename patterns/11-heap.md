# Pattern 11: Heap

**17 episodes · EP 94–110**

---

## The one-sentence version

A heap answers **"what is the current minimum (or maximum)?"** in O(1), and stays
correct through inserts and removals at **O(log n) each**: so any problem that
repeatedly asks for the extreme of a *changing* set is a heap problem, and any problem
that asks for the **top k** of n things is a heap of size k, not a sort: **O(n log n) →
O(n log k)**.

## ELI5

A hospital waiting room doesn't sort every patient into a perfect line. It only needs to
know **who's most urgent right now**. When someone new walks in, they find their rough
place in seconds; when the doctor is free, the top person leaves and the next-most-urgent
bubbles up. Nobody ever knows the full order, and nobody needs to.

That's a heap: a pile that promises the top is the extreme and promises nothing else.

```
min-heap:        1
               /   \
              3     2        <- 3 and 2 are NOT in order relative to each other
             / \   /
            7   4 9          <- only rule: every parent <= its children
```

The bargain is that keeping this loose promise costs O(log n) per change instead of the
O(n) a sorted list would cost to insert into. Every episode in this pattern is one of
five ways to spend that bargain:

| family | what the heap holds | why it beats sorting |
|---|---|---|
| **top-k** | the k best seen so far | k ≪ n, so log k ≪ log n |
| **k-closest** | the k nearest so far | same, with a distance as the key |
| **heap as pointer** | one "current head" per sorted source | k-way merge without concatenating |
| **greedy + heap** | the candidates still available | "take the best, put back the rest" needs a live extreme |
| **two heaps** | the lower half and the upper half | the median lives at the two tops |

## How to recognise it

| Signal | Example |
|---|---|
| **"k-th largest / smallest"** | Kth Smallest (EP94), Kth Largest (EP95) |
| **"top k"**, "k most frequent" | Top K Frequent Elements (EP96), Words (EP97) |
| **"k closest / nearest"** | K Closest Points (EP98), Kth Weakest Row (EP100) |
| "merge k sorted …" | Merge K Sorted Arrays (EP101), Kth Smallest in Sorted Matrix (EP102) |
| a **stream**: "data arrives one at a time" | Find Median from Data Stream (EP109) |
| "median" | EP109, Sliding Window Median (EP110) |
| **schedule / assign / pick the best available** repeatedly | Task Scheduler (EP104), IPO (EP107), Course Schedule III (EP108) |
| "minimum number of steps" where each step consumes the current best | Last Stone Weight (EP103), Refueling Stops (EP106) |
| the words **"repeatedly"** or **"each time"** in your own restatement | all seventeen |

**The tell for greedy + heap specifically:** the problem asks you to make a sequence of
choices, each choice is "the biggest/smallest thing available *right now*", and the set
of what's available changes after each choice. A sorted list can't keep up with the
changes; a heap can.

**The anti-signals.** If you need the **full order**: every element in position, that's
a sort, O(n log n), and a heap gains you nothing. If you need to **look up an arbitrary
element** by key, that's a hash map; a heap can't find anything but its top. If k is
close to n, sorting is simpler and no slower.

## Shape A: Top k with a bounded heap

```python
import heapq

def k_largest(nums, k):
    heap = []                          # a MIN-heap of the k largest so far
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)        # evict the smallest of the k+1 -> k remain
    return heap                        # heap[0] is the k-th largest
```

**Why a min-heap for the k *largest*:** the heap's top is the weakest thing you're
currently keeping. When something new arrives you compare it with the weakest survivor,
not the strongest, so the weakest has to be the thing that's O(1) to reach. This is the
single most counter-intuitive line in the pattern and the one interviewers watch for.

Two Python facts you say out loud every time:

- **`heapq` is a min-heap and only a min-heap.** For a max-heap you push `-x` and negate
  on the way out. There is no flag.
- **Ties are broken by the next tuple element.** For Top K Frequent Words (EP97) you want
  highest frequency, then *alphabetically first*, so push `(-freq, word)`: the negation
  makes big frequencies small, and the untouched `word` sorts ascending, which is the
  order you wanted. When the second element is *also* the wrong way round, you can't
  negate a string; see "what goes wrong" #2.
- `heapq.nlargest(k, iterable, key=...)` and `heapq.nsmallest` do all of this in one
  line. Know they exist; write the loop by hand when asked to.

## Shape B: K closest

```python
def k_closest(points, k):
    heap = []
    for x, y in points:
        d = x * x + y * y                        # no sqrt: monotone, so ordering is identical
        heapq.heappush(heap, (-d, x, y))         # MAX-heap on distance: top = farthest kept
        if len(heap) > k:
            heapq.heappop(heap)                  # evict the farthest
    return [(x, y) for _, x, y in heap]
```

Same shape as A with the key swapped for a distance. The heap is a **max-heap on
distance** because the thing you evict is the *farthest* of the k you're keeping.

**The exception that proves the rule:** Find K Closest Elements (EP99) gives you a
**sorted** array. Sorted input means the k closest form a **contiguous window**, so the
right tool is binary search for the window's left edge, O(log(n−k) + k), and a heap is
the slow answer. This episode exists to make you check for sortedness before reaching for
the heap.

## Shape C: Heap as a merged pointer

```python
def merge_k(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]   # (value, which list, index)
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))       # advance THAT list's pointer
    return out
```

The heap holds **one candidate per source**: the current head of each list. Pop the
smallest head, then push its successor from the *same* list. The heap never exceeds k
entries, so the merge is O(N log k) for N total elements instead of O(N log N) for
concatenate-and-sort.

Kth Smallest in a Sorted Matrix (EP102, a repeat of EP91) is this with rows as the
lists: seed the heap with column 0 of every row, pop k times, and after each pop push the
element to the right. EP91 solves the same problem by binary searching on the *value*;
EP102 is here to show the two solutions side by side and argue about which is faster
when k is small versus when it's near n².

## Shape D: Greedy + heap

```python
def last_stone_weight(stones):
    heap = [-s for s in stones]                   # max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)                  # the two heaviest
        b = -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))        # push back what's left
    return -heap[0] if heap else 0
```

The loop is always: **pop the best, do the step, push back the remainder.** The heap is
what lets "the best" stay correct after the remainder goes back in. The six episodes
differ only in what "best" means and what "remainder" means:

| EP | pop the … | push back … | the twist |
|---|---|---|---|
| 103 Last Stone Weight | two heaviest | their difference | none, the clean template |
| 104 Task Scheduler | most frequent task | count − 1, *after the cooldown* | a queue holds tasks that are cooling; pop from heap, park in queue, re-push when ready |
| 105 Reorganize String | most frequent char | count − 1, *one step later* | hold the previous char out of the heap for exactly one turn so it can't repeat |
| 106 Refueling Stops | biggest station **passed** | nothing, stations are consumed | drive as far as you can; only when stranded, retroactively "refuel" at the best station you already drove past |
| 107 IPO | most profitable **affordable** project | nothing, but capital grows | **two heaps**: a min-heap by capital of locked projects, a max-heap by profit of unlocked ones; each round, move everything newly affordable across, then pop one |
| 108 Course Schedule III | the **longest course taken so far** | nothing, it's dropped | sort by deadline, take every course, and when over the deadline, *undo the longest one you took*, the heap remembers which that was |

EP106 and EP108 share the deepest idea in this pattern: **the heap lets you make a
greedy decision *retroactively*.** You don't decide at a gas station whether to stop;
you decide later, when you run dry, which past station you *should* have stopped at.
Say that sentence in the interview and the rest follows.

## Shape E: Two heaps for a running median

```python
class MedianFinder:
    def __init__(self):
        self.low = []      # MAX-heap (negated): the smaller half
        self.high = []     # MIN-heap: the larger half

    def add(self, x):
        heapq.heappush(self.low, -x)                          # 1. always enter through low
        heapq.heappush(self.high, -heapq.heappop(self.low))   # 2. low's max moves to high
        if len(self.high) > len(self.low):                    # 3. keep low >= high in size
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

Two invariants and nothing else: **every element in `low` ≤ every element in `high`**,
and **`len(low) − len(high)` is 0 or 1**. The three-step add above preserves both
without any `if x < median` branching, which is where the bugs usually live.

Sliding Window Median (EP110) is this plus **removal**, and heaps can't remove from the
middle. The trick is **lazy deletion**: keep a dict of "elements that have left the
window but are still physically in a heap," and whenever a top is in that dict, pop it
and decrement before reading. The size bookkeeping has to count *live* elements only, so
the balance step compares logical sizes, not `len(heap)`.

## The three things that go wrong

### 1. Forgetting that `heapq` is a min-heap

Every max-heap in Python is a min-heap of negated keys. The failure is silent: the code
runs, the answer is the k *smallest* instead of the k largest, and one test passes by
coincidence. Write the negation the moment you type `heappush`, and negate again on the
way out, `-heapq.heappop(h)`, never `heapq.heappop(h)` followed by a fix-up three lines
later.

### 2. Tuple comparison reaching an uncomparable element

`heappush(h, (dist, point))` works until two points have the same distance, then Python
compares the second elements, and if those are lists, dicts, or custom objects, you get
`TypeError: '<' not supported` at a random moment on a random input. The fix is a
tie-breaker that's always comparable, usually the index: `(dist, i, point)`. For "highest
frequency, then alphabetical" the tuple `(-freq, word)` happens to work because strings
compare ascending; for "highest frequency, then *reverse* alphabetical" you need a
wrapper class with `__lt__`, because you can't negate a string.

### 3. Trusting `heap[0]` in a sliding window

Once elements can *leave*, the top of the heap may be an element that's no longer in the
window. Anything that reads `heap[0]`, the median, the balance check, the size, has to
first evict stale tops. The bug shows up as a median that's off by one element and only
on inputs where the departing element was the current median. Test with a window that
slides off its own median deliberately.

## Complexity

| Shape | Time | Space |
|---|---|---|
| A / B, top k, k closest | O(n log k) | O(k) |
| A with `heapify` on the whole input, then k pops | O(n + k log n) | O(n) |
| C, k-way merge of N total elements | O(N log k) | O(k) |
| D, greedy, n pops and pushes | O(n log n) | O(n) |
| E, median, per insert | O(log n) | O(n) |
| E, sliding window median, n windows | O(n log n) with lazy deletion (stale entries can pile up) | O(n) worst case |
| the sort you're beating | O(n log n) | O(n) |

Build a heap from n items with `heapify` in **O(n)**, not O(n log n), it's the
follow-up question after "why not sort", and the answer is that most nodes are leaves
and sift down a short distance.

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 94 | Kth Smallest | top-k | The template. Max-heap of size k, via negation. |
| 95 | Kth Largest | top-k | Same code, flip the sign. Why a **min**-heap keeps the largest. |
| 96 | Top K Frequent Elements | top-k | Count first, then heap on `(freq, value)`. |
| 97 | Top K Frequent Words | top-k | Tie-breaking inside the tuple: `(-freq, word)`. |
| 98 | K Closest Points to Origin | k-closest | Distance as the key; skip the `sqrt`. |
| 99 | Find K Closest Elements | k-closest | Sorted input → the answer is a window → binary search beats the heap. |
| 100 | Kth Weakest Row | k-closest | Compute the key per row (soldiers via binary search), then top-k. |
| 101 | Merge K Sorted Arrays | pointer | One head per list; pop and push the successor. |
| 102 | Kth Smallest in Sorted Matrix | pointer | EP91 again, heap over rows vs binary search on value, side by side. |
| 103 | Last Stone Weight | greedy | Pop two, push the difference. The clean template. |
| 104 | CPU Task Scheduler | greedy | A cooling queue next to the heap; idle slots when the heap runs dry. |
| 105 | Reorganize String | greedy | Hold the last-used char out for one turn. |
| 106 | Min Refueling Stops | greedy | Retroactive greedy: refuel at the best station you already passed. |
| 107 | IPO | greedy | Two heaps: unlock by capital, choose by profit. |
| 108 | Course Schedule III | greedy | Sort by deadline, take everything, undo the longest when late. |
| 109 | Find Median from Data Stream | two heaps | Low is a max-heap, high is a min-heap, sizes differ by ≤ 1. |
| 110 | Sliding Window Median | two heaps | Lazy deletion; logical size ≠ `len(heap)`. |

## What "knowing this in your sleep" means

1. Why a **min**-heap for the k **largest**? *(The heap's top is the one you'd evict,
   the weakest survivor, so it has to be the thing that's O(1) to reach.)*
2. Why is top-k O(n log k) and not O(n log n)? *(The heap never holds more than k
   elements, so every push and pop costs log k.)*
3. How do you get a max-heap in Python? *(Negate the key on the way in and out. There
   is no other way with `heapq`.)*
4. What does the heap hold in a k-way merge? *(One entry per source: the current head.
   Popping one means pushing its successor from the same source.)*
5. What's the invariant in the two-heap median? *(Everything in `low` ≤ everything in
   `high`, and `len(low) − len(high) ∈ {0, 1}`. Median is `low`'s top, or the mean of
   both tops.)*
6. What does "retroactive greedy" mean? *(Take the step now, and when it turns out you
   needed a resource earlier, the heap tells you which past option was best, refueling
   stops, Course Schedule III.)*
7. When is a heap the wrong tool? *(Full order needed → sort. Lookup by key → hash map.
   Sorted input and a contiguous answer → binary search or two pointers.)*
