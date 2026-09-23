# EP110 · P11E17 · Sliding Window Median   [Hard]

**Pattern:** Heap (two heaps + lazy deletion) · **Link:** https://leetcode.com/problems/sliding-window-median/description/

---

## 🎬 Hook
> "Yesterday's two heaps, but now numbers have to **leave**. A heap can only remove its
> top, and the number leaving the window is almost never on top. So you don't remove it.
> You write its name on a **list of ghosts**, and you only throw it out when it floats
> up to the top. Every `len(heap)` becomes a lie, and the whole episode is learning not
> to trust it."

## 📋 Problem, in your words
```
Given nums and a window size k, slide the window from left to right one
step at a time. Return the median of every window.

  - k odd:  the middle value
  - k even: the mean of the two middle values
  - there are len(nums) - k + 1 windows
```

## 🔢 The example
```
Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [1, -1, -1, 3, 5, 6]
Why:    [1 3 -1] -> 1    [3 -1 -3] -> -1    [-1 -3 5] -> -1
        [-3 5 3] -> 3    [5 3 6]   -> 5     [3 6 7]   -> 6

Input:  nums = [1, 4, 2, 3], k = 4
Output: [2.5]
```

## 🧸 ELI5
> It's EP109's short group and tall group, but now the kids are in a **bus queue**, and
> every time a new kid joins at the back, the kid at the front **gets on the bus**.
>
> The problem: the kid who leaves might be buried in the middle of the short group.
> Digging them out means re-sorting everybody. So instead, when a kid leaves, you just
> write their name on a clipboard: **"gone, ignore them."** They stay physically in the
> group. Only when a gone kid ends up at the **front** of a group, where you'd actually
> look at them, do you remove them for real.
>
> ```
> short group (physically): -3  -1  3  5  6
> clipboard ("gone"):       -3  -1     5
> short group (really):              3     6     <- only 2 real kids, 5 bodies
> ```
>
> That's the catch: to keep the groups balanced you must count the **real** kids, not
> the bodies. You can't ask the group "how many of you are there?"

## 🐌 Brute force (say it, don't type it)
For each window, sort it and pick the middle: **O(n · k log k)**. Or keep a sorted
window with `bisect.insort` and `pop(bisect_left(...))`: O(k) per step for the list
shifting, **O(n·k)** total. Honestly that one is short and fast in practice. The two
heaps with lazy deletion are **O(n log n)**, and they're the answer the interviewer is
testing for.

## 💡 The pattern reveal
**Signal:** "**median**" + "**sliding window**".
**Therefore:** Shape E two heaps + **lazy deletion** (Pattern 3 window meets Pattern 11).

**Key insight:** three pieces of bookkeeping replace "remove from the middle":

| problem | fix |
|---|---|
| can't remove `gone` from inside a heap | `stale[gone] += 1`, pop it later when it's a top |
| `len(low)` counts dead elements | track `balance`: the change in *live* `low` minus *live* `high` this step |
| a top might be dead | `prune` both tops before reading the median |

Each step, `balance` starts at -1 (`gone` was in `low`) or +1 (`gone` was in `high`),
then +1 or -1 for which side `x` joined. It ends at -2, 0 or +2, and one move fixes a
±2:

```python
balance = -1 if gone <= -low[0] else 1        # which side just lost a live element
if x <= -low[0]:
    heapq.heappush(low, -x);  balance += 1
else:
    heapq.heappush(high, x);  balance -= 1
if balance > 0:   heapq.heappush(high, -heapq.heappop(low))   # low has the extra
elif balance < 0: heapq.heappush(low, -heapq.heappop(high))   # high has the extra
```

Moving a top is safe because both tops were pruned at the end of the previous step, so
they're live.

## 🔍 Dry run: `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`
First window `[1, 3, -1]`: all into `low`, then move `k // 2 = 1` largest across →
`low = {-1, 1}`, `high = {3}`, median **1**.

| i | out (side) | in (side) | balance | move | low (physical) | high | stale after prune | median |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 (low) | -3 (low) | 0 | - | {-3, -1} (1 pruned from top) | {3} | {} | **-1** |
| 4 | 3 (high) | 5 (high) | 0 | - | {-3, -1} | {5} (3 pruned) | {} | **-1** |
| 5 | -1 (low) | 3 (high) | -2 | 3 high → low | {-3, **-1**, 3} | {5} | {-1} | **3** |
| 6 | -3 (low) | 6 (high) | -2 | 5 high → low | {**-3**, **-1**, 3, 5} | {6} | {-1, -3} | **5** |
| 7 | 5 (low) | 7 (high) | -2 | 6 high → low | {**-3**, **-1**, 3, **5**, 6} | {7} | {-1, -3, 5} | **6** |

Output **`[1, -1, -1, 3, 5, 6]`** ✓.

Look at the last row: `low` physically holds **5** numbers and only **2** of them (3
and 6) are in the window. `len(low)` says 5, the truth is 2. Using `len` for balancing
here would move the wrong things and the median would drift. The bold ghosts are
harmless because they're **buried**: the median only reads tops, and both tops are live.

## ✅ Optimal solution
```python
class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        """Median of every window of size k.

        Time:  O(n log n), each element pushed once and popped at most once (a heap
               can hold stale entries, so its size is bounded by n, not k).
        Space: O(n), the heaps plus the stale counts.
        """
        low, high = [], []              # low: MAX-heap (negated), high: MIN-heap
        stale = defaultdict(int)        # value -> copies that left the window but
                                        # are still physically inside a heap

        def prune(heap, sign):
            # pop dead tops; sign turns a stored key back into its real value
            while heap and stale[sign * heap[0]]:
                stale[sign * heap[0]] -= 1
                heapq.heappop(heap)

        def median():
            return float(-low[0]) if k % 2 else (-low[0] + high[0]) / 2

        for x in nums[:k]:              # first window: low gets the extra one
            heapq.heappush(low, -x)
        for _ in range(k // 2):
            heapq.heappush(high, -heapq.heappop(low))

        out = [median()]
        for i in range(k, len(nums)):
            x, gone = nums[i], nums[i - k]

            stale[gone] += 1                            # delete lazily
            balance = -1 if gone <= -low[0] else 1      # change in live(low) - live(high)

            if x <= -low[0]:
                heapq.heappush(low, -x)
                balance += 1
            else:
                heapq.heappush(high, x)
                balance -= 1

            if balance > 0:                             # low has one too many live
                heapq.heappush(high, -heapq.heappop(low))
            elif balance < 0:                           # high has one too many live
                heapq.heappush(low, -heapq.heappop(high))

            prune(low, -1)                              # tops must be live before reading
            prune(high, 1)
            out.append(median())

        return out
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **Never balance on `len(heap)`.** That's the pattern card's gotcha #3 and the reason
  this problem is Hard. `balance` counts live elements; `len` counts bodies.
- **Prune before every read.** The median reads `low[0]` and `high[0]`; either could be
  a ghost. Pruning at the end of each step keeps both tops live for the next step too.
- **Which side did `gone` leave?** Compare with `low`'s top (`gone <= -low[0]` → low).
  Equal values on both sides are fine: the stale count is by value, and any copy of the
  same value is interchangeable.
- **`sign` in `prune`.** `low` stores negatives, so the real value is `-low[0]`. Checking
  `stale[low[0]]` looks up the wrong number and never prunes.
- **Overflow isn't a Python problem**, but in Java/C++ `(a + b) / 2` on two large ints
  overflows. Mention `a / 2 + b / 2` or a `long`.
- **Test a window that slides off its own median.** `[2, 1, 3, 4]`, k = 3: the 2 leaves
  right after being the median. That's the case the card warns about.

## 🎤 Interview talking points
- *"Two heaps for the halves, like the streaming median. Heaps can't delete from the
  middle, so I delete lazily: count the value as stale and pop it only when it reaches a
  top."*
- *"Because the heaps contain dead elements, I track the balance of live elements
  myself instead of using their lengths."*
- *"O(n log n): every element is pushed once and popped at most once."*
- *"In production I'd use a sorted container (e.g. `SortedList`) with O(log k) insert and
  delete; it's the same complexity with far less bookkeeping. Lazy deletion is what you
  do when all you have is a binary heap."*

## 🔗 Transfer
That's the whole heap pattern: top-k, k-closest, heap as pointer, greedy + heap, and
two heaps, with lazy deletion as the final boss. Lazy deletion shows up again in EP164
Dijkstra: when a shorter path to a node is found, you don't update its old heap entry,
you push a new one and skip the stale one when it's popped. Next up is Pattern 12,
Recursion and Backtracking, starting with EP111 Fibonacci.

## 📹 Metadata
- **Title:** `Sliding Window Median, heaps full of ghosts | Heap #17`
- **Thumbnail:** `len(heap) lies` (red block)
- **Short:** the bus-queue clipboard, and `low` holding 5 bodies but 2 real kids. 50s.
