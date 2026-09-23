# EP166 · P14E15 · Path With Minimum Effort   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/path-with-minimum-effort/

---

## 🎬 Hook
> "You're hiking across a grid of heights, and a route is only as hard as its **single
> steepest step**. Find the easiest route. It looks nothing like Dijkstra, because a
> path's cost isn't a sum. But Dijkstra never needed a sum. It needed a cost that never
> goes down as the path gets longer. Change **one line**, `d + w` to `max(d, w)`, and
> you're done."

## 📋 Problem, in your words
```
heights is a rows x cols grid. You start top-left, finish bottom-right,
and move up/down/left/right.

A route's EFFORT is the largest absolute height difference between two
consecutive cells on it. Return the minimum effort of any route.
```

## 🔢 The example
```
heights = [[1, 2, 2],
           [3, 8, 2],
           [5, 3, 5]]

Output: 2
Why:    1 -> 3 -> 5 -> 3 -> 5 (down the left, along the bottom)
        steps: |3-1|=2, |5-3|=2, |3-5|=2, |5-3|=2    -> effort 2
        1 -> 2 -> 2 -> 2 -> 5 (along the top, down the right)
        steps: 1, 0, 0, 3                            -> effort 3, worse

heights = [[1, 2, 3], [3, 8, 4], [5, 3, 5]]   ->  1
heights = [[7]]                               ->  0     <- already there
```

## 🧸 ELI5
> You're choosing a hiking trail, and all you care about is the **scariest single
> climb**. A trail with a hundred gentle steps is better than one with a single cliff.
>
> So instead of adding up how tired you are, you carry one number: "the scariest step so
> far". Each new step either is scarier (the number goes up) or isn't (it stays put). It
> **never goes down**.
>
> ```
> left trail:   2, 2, 2, 2   -> scariest so far: 2, 2, 2, 2  -> 2
> top trail:    1, 0, 0, 3   -> scariest so far: 1, 1, 1, 3  -> 3
> ```
>
> Always explore from whichever spot has the gentlest "scariest step so far", and the
> first time you reach the end, that's the answer.

## 🐌 Brute force (say it, don't type it)
DFS every simple path from start to end and take the smallest maximum: exponential. A
smarter alternative that *is* a valid answer: **binary search on the effort** E (0 to
10⁶), and for each E run a BFS using only steps ≤ E, asking "can I reach the end?".
**O(R·C · log(max height))**. Mention it, it's a nice cross-over with Pattern 10, but
the Dijkstra version reads the problem directly.

## 💡 The pattern reveal
**Signal:** "minimise the **maximum**" along a path, a grid with weighted steps.
**Therefore:** Shape E: Dijkstra with a **max-cost** path.

**Key insight:** Dijkstra is correct whenever extending a path can never make its cost
**smaller**. `d + w` with `w ≥ 0` has that property. So does `max(d, w)`. Nothing else
in the algorithm cares how the cost is combined.

| | Dijkstra (EP164) | Min Effort (today) |
|---|---|---|
| a path costs | sum of edges | **max** of edges |
| relax | `nd = d + w` | `nd = max(d, w)` |
| edge weight | given | `abs(h[nr][nc] - h[r][c])` |
| nodes | `0..V-1` | grid cells `(r, c)` |
| early exit | - | pop the target → return |

```python
nd = max(d, abs(heights[nr][nc] - heights[r][c]))    # the ONE changed line
```

**Early exit:** the first time the target is **popped** its effort is final, so return
immediately. You don't need the effort of every other cell.

## 🔍 Dry run: `[[1,2,2],[3,8,2],[5,3,5]]`
`best` = smallest effort found so far per cell; heap holds `(effort, r, c)`.

| step | pop | relax (cell: new effort) | heap after |
|---|---|---|---|
| 1 | `(0, 0,0)` | (1,0): max(0,\|3-1\|)=2; (0,1): max(0,1)=1 | `(1,0,1) (2,1,0)` |
| 2 | `(1, 0,1)` | (1,1): max(1,6)=6; (0,2): max(1,0)=1 | `(1,0,2) (2,1,0) (6,1,1)` |
| 3 | `(1, 0,2)` | (1,2): max(1,0)=1 | `(1,1,2) (2,1,0) (6,1,1)` |
| 4 | `(1, 1,2)` | **(2,2): max(1,3)=3** | `(2,1,0) (3,2,2) (6,1,1)` |
| 5 | `(2, 1,0)` | (2,0): max(2,2)=2; (1,1): max(2,5)=5 < 6 | `(2,2,0) (3,2,2) (5,1,1) (6,1,1)` |
| 6 | `(2, 2,0)` | (2,1): max(2,2)=2 | `(2,2,1) (3,2,2) (5,1,1) (6,1,1)` |
| 7 | `(2, 2,1)` | **(2,2): max(2,2)=2 < 3** | `(2,2,2) (3,2,2) ...` |
| 8 | `(2, 2,2)` | **target popped → return 2** | |

Answer **2** ✓. Step 4 reached the target first, via the top route, with effort 3. It
was **not** finished then; it was only pushed. Step 7 found the left route's 2, and
step 8 popped that. The stale `(3, 2,2)` never matters because we've already returned.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """Smallest possible maximum step along any top-left to bottom-right route.

        Time:  O(R*C * log(R*C)), Dijkstra on R*C cells with at most 4 edges each.
        Space: O(R*C), the best-effort grid and the heap.
        """
        rows, cols = len(heights), len(heights[0])
        best = [[float('inf')] * cols for _ in range(rows)]
        best[0][0] = 0
        pq = [(0, 0, 0)]                                    # (effort so far, r, c)

        while pq:
            d, r, c = heapq.heappop(pq)
            if d > best[r][c]:
                continue                                    # stale entry
            if r == rows - 1 and c == cols - 1:
                return d                                    # popped = final
            for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
                if 0 <= nr < rows and 0 <= nc < cols:
                    nd = max(d, abs(heights[nr][nc] - heights[r][c]))   # max, not +
                    if nd < best[nr][nc]:
                        best[nr][nc] = nd
                        heapq.heappush(pq, (nd, nr, nc))
        return 0                                            # unreachable for a valid grid
```
**Time:** O(R·C · log(R·C)) · **Space:** O(R·C)

## ⚠️ Gotchas
- **`max(d, w)`, not `d + w`.** Summing answers "least total climbing", a different
  question. On example 1 the sum-minimising route isn't even the answer route.
- **Return when the target is popped, not when it's pushed.** Step 4 pushed it with 3;
  returning there gives the wrong answer.
- **`abs`.** Going down 6 is as hard as going up 6.
- **1 x 1 grid → 0.** The first pop is the target. The code handles it.
- **The edge weight depends on both cells,** so compute it in the loop; there's nothing
  to precompute into an adjacency list.
- **Why is `max` allowed?** Say it: the cost of a path never decreases when you extend
  it, which is the one property Dijkstra's greedy choice relies on.

## 🎤 Interview talking points
- *"It's a shortest-path problem where path cost is the max edge instead of the sum.
  Dijkstra still works, because extending a path can't lower its max."* ← the insight.
- *"The only line that changes from textbook Dijkstra is `nd = max(d, w)`."*
- *"I return the first time the target is popped; that's when its value is final."*
- *"Alternatives: binary search on the answer with a BFS feasibility check, or Kruskal's
  union-find adding edges in increasing weight until start and end connect."*

## 🔗 Transfer
EP165 changed what you do *after* Dijkstra; today changed what a path *costs*. Tomorrow
(EP167) Swim in Rising Water is the same `max` Dijkstra on a grid, with the weight living
on the **cell** instead of the step, and it's the cleanest proof that you've really
learned the pattern: same code, different wrapper. The binary-search alternative is
Pattern 10's "search on the answer" (EP81 Koko) wearing a graph costume.

## 📹 Metadata
- **Title:** `Path With Minimum Effort, Dijkstra with max() instead of + | Graphs #15`
- **Thumbnail:** `d + w → max(d, w)` (purple block)
- **Short:** the target getting pushed at 3, then improved to 2 before it's popped.
  40s.
