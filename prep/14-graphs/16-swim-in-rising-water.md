# EP167 · P14E16 · Swim in Rising Water   [Hard]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/swim-in-rising-water/

---

## 🎬 Hook
> "This is a Hard. It's also yesterday's problem with the numbers moved. The water rises
> one unit per second, and you can only swim onto a cell once the water covers it. The
> time you finish is the **highest cell on your route**. Minimise the maximum along a
> path: that's `max(d, w)` Dijkstra again, and the only change is where `w` comes from."

## 📋 Problem, in your words
```
grid is n x n, grid[r][c] = elevation, all values distinct in 0..n²-1.
At time t the water level is t. You can move between 4-adjacent cells
if BOTH are at elevation <= t, and swimming itself takes no time.

Return the least time t at which you can get from (0,0) to (n-1,n-1).
```

## 🔢 The example
```
grid = [[0, 2],
        [1, 3]]
Output: 3        <- (1,1) has elevation 3; you can't stand on it before t = 3

grid = [[0, 1, 6],
        [7, 8, 2],
        [5, 4, 3]]
Output: 6
Why:    0 -> 1 -> 6 -> 2 -> 3   highest cell 6
        0 -> 7 -> 5 -> 4 -> 3   highest cell 7
        anything through the 8  highest cell 8

grid = [[0]]   ->   0
```

## 🧸 ELI5
> A flooded island. Every cell is a rock of some height, and the tide rises by one every
> second. You can hop between neighbouring rocks only when the water is over **both**.
>
> The question is really: *"which route to the far corner has the lowest tallest rock?"*
> Because you'll be stuck waiting until the tide clears that tallest rock, and then you
> can swim the whole route instantly.
>
> ```
> route via 1, 6, 2:  tallest rock 6  -> leave at t = 6
> route via 7, 5, 4:  tallest rock 7  -> leave at t = 7
> ```
>
> Always expand from the reachable rock with the lowest "tallest rock so far", and the
> first time you reach the corner, you're done.

## 🐌 Brute force (say it, don't type it)
Simulate time: for t = 0, 1, 2, …, flood-fill from (0,0) through cells ≤ t, and stop
when the corner is reached. Up to n² values of t, each an O(n²) flood fill:
**O(n⁴)**. Binary search on t cuts it to **O(n² log n)**, a perfectly good answer.
Dijkstra gets the same bound and reads the problem directly.

## 💡 The pattern reveal
**Signal:** "minimise the **maximum**" along a grid path.
**Therefore:** Shape E, max-cost Dijkstra, exactly as in EP166.

**Key insight:** the time to reach a cell along a route is the highest elevation on that
route, including the start cell. So the cost of stepping onto `(nr, nc)` is
`max(d, grid[nr][nc])`, and the weight lives on the **cell**, not the step.

| | Min Effort (EP166) | Swim (today) |
|---|---|---|
| weight of a step | `abs(h[next] - h[cur])` | `grid[next]` |
| starting cost | `0` | **`grid[0][0]`** |
| relax | `max(d, w)` | `max(d, w)` |
| stop | target popped | target popped |

```python
nd = max(d, grid[nr][nc])       # you can't stand on it until the water covers it
```

## 🔍 Dry run: `[[0,1,6],[7,8,2],[5,4,3]]`
Heap holds `(time, r, c)`; start `(0, 0,0)` because `grid[0][0] = 0`.

| step | pop | relax (cell: new time) | heap after |
|---|---|---|---|
| 1 | `(0, 0,0)` | (1,0): max(0,7)=7; (0,1): max(0,1)=1 | `(1,0,1) (7,1,0)` |
| 2 | `(1, 0,1)` | (1,1): max(1,8)=8; (0,2): max(1,6)=6 | `(6,0,2) (7,1,0) (8,1,1)` |
| 3 | `(6, 0,2)` | (1,2): max(6,2)=**6** | `(6,1,2) (7,1,0) (8,1,1)` |
| 4 | `(6, 1,2)` | (2,2): max(6,3)=**6** | `(6,2,2) (7,1,0) (8,1,1)` |
| 5 | `(6, 2,2)` | **target popped → return 6** | |

Answer **6** ✓. Watch steps 3 and 4: once you've waited for the 6, the 2 and the 3 cost
nothing extra, `max` keeps the time at 6. And the whole left side (7, 5, 4) never gets
popped, because 7 is already worse than the answer.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        """Least time t at which a route exists with every cell elevation <= t.

        Time:  O(n^2 log n), Dijkstra on n^2 cells, 4 edges each.
        Space: O(n^2), the best-time grid and the heap.
        """
        n = len(grid)
        best = [[float('inf')] * n for _ in range(n)]
        best[0][0] = grid[0][0]                             # you start standing on it
        pq = [(grid[0][0], 0, 0)]                           # (time so far, r, c)

        while pq:
            t, r, c = heapq.heappop(pq)
            if t > best[r][c]:
                continue                                    # stale entry
            if r == n - 1 and c == n - 1:
                return t
            for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
                if 0 <= nr < n and 0 <= nc < n:
                    nt = max(t, grid[nr][nc])               # wait for the water to cover it
                    if nt < best[nr][nc]:
                        best[nr][nc] = nt
                        heapq.heappush(pq, (nt, nr, nc))
        return -1                                           # unreachable for a valid grid
```
**Time:** O(n² log n) · **Space:** O(n²)

## ⚠️ Gotchas
- **Start at `grid[0][0]`, not 0.** `[[3, 0], [1, 2]]` needs t = 3 before you can even
  stand at the start. Starting the heap at 0 returns 2.
- **Weight on the cell, not the difference.** Copying EP166's `abs(...)` line solves the
  wrong problem.
- **Return at pop.** Same as EP166: a pushed value can still be improved.
- **Values are distinct 0..n²−1**, which is what makes the binary-search and union-find
  alternatives neat, but Dijkstra doesn't rely on it.
- **n = 1** returns `grid[0][0]`, correctly.

## 🎤 Interview talking points
- *"The time to finish a route is its highest cell, so I want the route with the smallest
  maximum: Dijkstra with `max` instead of `+`, like Path With Minimum Effort."*
- *"The cost is on the cell, and it includes the start cell."*
- *"O(n² log n). Alternatives: binary search on t with a flood fill, or process cells in
  elevation order with union-find until (0,0) and (n-1,n-1) join."*
- *"Recognising this as the same problem as Min Effort is the point. The Hard label is
  about the story, not the algorithm."*

## 🔗 Transfer
Three Dijkstra episodes in a row (EP165, 166, 167), and the heap loop never changed. That
repetition is the lesson: identify the cost, check it never decreases along a path, and
Dijkstra applies. Tomorrow (EP168) breaks that assumption on purpose with **negative**
weights, where Dijkstra is wrong and Bellman-Ford takes over.

## 📹 Metadata
- **Title:** `Swim in Rising Water, a Hard that's secretly yesterday's Medium | Graphs #16`
- **Thumbnail:** `max(d, grid[r][c])` (blue block)
- **Short:** the tide rising to 6 and the route 0-1-6-2-3 lighting up at once. 35s.
