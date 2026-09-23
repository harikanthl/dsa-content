# EP103 · P11E10 · Last Stone Weight   [Easy]

**Pattern:** Heap (greedy + heap) · **Link:** https://leetcode.com/problems/last-stone-weight/description/

---

## 🎬 Hook
> "Smash the two heaviest stones, throw the leftover back in the pile, repeat. The
> problem *tells* you to be greedy. The only question is how to find 'the two heaviest'
> again after every smash, and a sorted list can't keep up. That's the loop every
> greedy-heap problem in this pattern runs: **pop the best, do the step, push back the
> remainder.**"

## 📋 Problem, in your words
```
You have stones with positive integer weights. Each turn:
  - take the two heaviest, x <= y
  - if x == y, both are destroyed
  - otherwise x is destroyed and y becomes y - x
Return the weight of the last stone left, or 0 if none are left.
```

## 🔢 The example
```
Input:  [2, 7, 4, 1, 8, 1]
Output: 1
Why:    8,7 -> 1    pile [2,4,1,1,1]
        4,2 -> 2    pile [2,1,1,1]
        2,1 -> 1    pile [1,1,1]
        1,1 -> 0    pile [1]         -> 1

Input:  [1]     -> 1
Input:  [2, 2]  -> 0
```

## 🧸 ELI5
> A sumo tournament where the two **biggest** wrestlers always fight next. When they
> fight, the smaller one is out, and the bigger one loses weight equal to the smaller
> one's. If they're the same size, both are out.
>
> After every fight the loser leaves and the winner **goes back into the crowd, lighter
> than before**, so the next "two biggest" might be completely different people. You
> need a crowd where **the biggest one is always standing at the front**, no matter who
> walks back in.
>
> ```
> crowd:  8 7 4 2 1 1       8 vs 7 -> 1 goes back
> crowd:  4 2 1 1 1         4 vs 2 -> 2 goes back
> crowd:  2 1 1 1           2 vs 1 -> 1 goes back
> crowd:  1 1 1             1 vs 1 -> both out
> crowd:  1                 the last wrestler weighs 1
> ```

## 🐌 Brute force (say it, don't type it)
Sort, take the last two, compute, insert the remainder back, re-sort. Each turn is
O(n log n) (or O(n) with `bisect.insort`), and there are up to n turns: **O(n² log n)**
or O(n²). The heap makes each turn O(log n): **O(n log n)** total.

## 💡 The pattern reveal
**Signal:** "each turn, take the **heaviest**" · the pile **changes** after each turn.
**Therefore:** Shape D, greedy + heap: a **max**-heap.

**Key insight:** the pattern card's greedy loop, in its cleanest form. Everything
about the problem maps to one line:

| greedy loop step | here |
|---|---|
| pop the best | pop the two heaviest |
| do the step | `a - b` |
| push back the remainder | if `a != b`, push `a - b` |
| stop when | fewer than 2 stones |

Max-heap in Python = negate. Negate going in, negate coming out, and push back
`-(a - b)`.

## 🔍 Dry run: `[2, 7, 4, 1, 8, 1]`
`heap = heapify([-2, -7, -4, -1, -8, -1])`, shown as real weights:

| turn | pop a | pop b | a != b? push | pile after |
|---|---|---|---|---|
| 1 | 8 | 7 | push 1 | {4, 2, 1, 1, 1} |
| 2 | 4 | 2 | push 2 | {2, 1, 1, 1} |
| 3 | 2 | 1 | push 1 | {1, 1, 1} |
| 4 | 1 | 1 | equal, push nothing | {1} |

`len(heap) == 1` → stop. Return **`1`** ✓.

## ✅ Optimal solution
```python
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """Weight of the last stone after repeatedly smashing the two heaviest.

        Time:  O(n log n), at most n - 1 turns, each O(log n).
        Space: O(n), the heap.
        """
        heap = [-s for s in stones]             # MAX-heap via negation
        heapq.heapify(heap)                     # O(n)

        while len(heap) > 1:
            a = -heapq.heappop(heap)            # heaviest
            b = -heapq.heappop(heap)            # second heaviest, b <= a
            if a != b:
                heapq.heappush(heap, -(a - b))  # the survivor goes back in

        return -heap[0] if heap else 0
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **Three negations.** In, out (`-heappop`), and on the push-back, `-(a - b)`. Missing
  the last one pushes a positive number into a negated heap and it sinks to the
  *bottom*, silently.
- **`a - b`, not `b - a`.** `a` came out first, so it's the bigger. Negative weights mean
  you've swapped them.
- **Empty pile → 0.** `[2, 2]` ends with `heap = []`; `heap[0]` would be an IndexError.
- **`while len(heap) > 1`**, not `while heap`. With one stone left there's nothing to
  smash it against.

## 🎤 Interview talking points
- *"The problem literally says 'two heaviest, repeatedly', and the pile changes each
  turn: that's a max-heap."*
- *"Pop two, push the difference if non-zero. O(n log n)."*
- *"Python's heapq is min-only, so I negate everything, including the pushed-back
  difference."*
- *"Constraints are tiny (30 stones), so re-sorting would pass, but the heap is the
  shape that scales and it's the same code length."*

## 🔗 Transfer
This is the clean template for the greedy family. The next five episodes keep the
pop/step/push-back loop and add one complication each: EP104 Task Scheduler makes the
pushed-back item **wait** before it can return, EP105 Reorganize String holds it out for
**exactly one turn**, and EP106 Refueling Stops makes the greedy choice
**retroactively**.

## 📹 Metadata
- **Title:** `Last Stone Weight, the greedy-heap template | Heap #10`
- **Thumbnail:** `pop · smash · push` (green block)
- **Short:** the sumo crowd, winner walking back in lighter. 35s.
