# EP157 · P14E06 · Rotting Oranges   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/rotting-oranges/

---

## 🎬 Hook
> "Every rotten orange infects its neighbours each minute. How many minutes until
> they're all rotten? The instinct is to run BFS from each rotten orange and take the
> best. That's wrong **and** slow. The fix is to put **every** rotten orange in the
> queue before you start, and let BFS count the minutes as rings."

## 📋 Problem, in your words
```
Grid cells: 0 = empty, 1 = fresh orange, 2 = rotten orange.
Every minute, each fresh orange next to a rotten one (up/down/left/right) rots.

Return the minimum minutes until no fresh orange is left,
or -1 if some fresh orange can never rot.
```

## 🔢 The example
```
Input:  2 1 1        Output: 4
        1 1 0
        0 1 1

  minute 0     minute 1     minute 2     minute 3     minute 4
  2 1 1        2 2 1        2 2 2        2 2 2        2 2 2
  1 1 0        2 1 0        2 2 0        2 2 0        2 2 0
  0 1 1        0 1 1        0 1 1        0 2 1        0 2 2

Input:  2 1 1        Output: -1     <- (2,0) is walled off by empties
        0 1 1
        1 0 1

Input:  [[0, 2]]     Output: 0      <- nothing fresh, zero minutes

Input:  [[2, 1, 1, 1, 2]]  Output: 2   <- two sources, meeting in the middle
```

## 🧸 ELI5
> Think of a rumour at school. At minute 0, a few kids know it. Every minute, each kid
> who knows tells the kids sitting right next to them. How many minutes until the whole
> class knows?
>
> You don't follow one kid's rumour at a time. **All** the kids who know at minute 0
> start talking at the same moment.
>
> ```
> [2, 1, 1, 1, 2]
> minute 0: both ends know
> minute 1: the kid next to each end hears it   [2, 2, 1, 2, 2]
> minute 2: the middle kid hears it from both   [2, 2, 2, 2, 2]
> ```
>
> Run it from the left end alone and you'd say 3 minutes. The answer is 2, because both
> ends spread at once.

## 🐌 Brute force (say it, don't type it)
Simulate: each minute, scan the whole grid, rot every fresh orange next to a rotten one
(into a copy, so new rot doesn't spread twice in one minute), and stop when nothing
changes. Each minute is O(m·n) and there can be O(m·n) minutes (a long snake):
**O((m·n)²)**. The waste is re-scanning cells that are nowhere near the rot front.

The *other* wrong idea: BFS from each rotten orange separately and combine. That's
O(k·m·n) for k sources, and combining the results correctly needs a `min` per cell,
which is multi-source BFS done the slow way.

## 💡 The pattern reveal
**Signal:** "minimum minutes", spreading one step per minute, several starting points.
**Therefore:** Shape C, **multi-source BFS with the level loop**.

**Key insight:** BFS already visits in rings of distance. Seed the queue with every
rotten orange at once and the rings are "rotten at minute 1", "minute 2", and so on.
Process one whole ring per iteration and count iterations.

```python
q = deque(every rotten cell)                   # all sources at distance 0
while q and fresh:
    for _ in range(len(q)):                    # exactly one ring: this minute
        r, c = q.popleft()
        for each fresh neighbour:
            rot it, fresh -= 1, q.append(it)   # mark at push
    minutes += 1
return minutes if fresh == 0 else -1
```

Count the fresh oranges up front. Then `-1` is just "fresh is still above zero when the
queue runs out", no second scan.

## 🔍 Dry run: `[[2,1,1],[1,1,0],[0,1,1]]`
Start: queue `[(0,0)]`, `fresh = 6`, `minutes = 0`.

| minute | ring popped | newly rotten (pushed) | fresh after | queue after |
|---|---|---|---|---|
| 1 | (0,0) | (1,0), (0,1) | 4 | `[(1,0), (0,1)]` |
| 2 | (1,0), (0,1) | (1,1) from (1,0); (0,2) from (0,1) | 2 | `[(1,1), (0,2)]` |
| 3 | (1,1), (0,2) | (2,1) from (1,1) | 1 | `[(2,1)]` |
| 4 | (2,1) | (2,2) | **0** | `[(2,2)]` |

`fresh == 0`, so the loop stops before processing (2,2), and the answer is **4** ✓.

Note minute 2: (1,1) is next to both (1,0) and (0,1). It's rotted and pushed by
(1,0), and when (0,1) looks at it, it's already a 2. Mark-at-push is what stops it
entering the queue twice.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        """Minutes until every fresh orange rots, or -1 if one never can.

        Time:  O(m*n), every cell is queued at most once.
        Space: O(m*n), the queue can hold a whole ring of cells.
        """
        rows, cols = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    q.append((r, c))                # every source, before we start
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0
        while q and fresh:                          # stop the moment nothing is fresh
            for _ in range(len(q)):                 # one ring = one minute
                r, c = q.popleft()
                for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2            # rot at push: queued once
                        fresh -= 1
                        q.append((nr, nc))
            minutes += 1

        return minutes if fresh == 0 else -1
```
**Time:** O(m·n) · **Space:** O(m·n)

## ⚠️ Gotchas
- **`while q and fresh`, not `while q`.** With just `while q`, the last ring (the
  oranges that rotted in the final minute) gets processed too, finds nothing, and adds
  one extra minute: 5 instead of 4. Either stop when `fresh` hits 0, or only count a
  minute when the ring actually rotted something.
- **No fresh oranges at all → 0, not -1.** `[[0, 2]]` and `[[0]]` both return 0. The
  `and fresh` condition gets this for free.
- **`range(len(q))` is evaluated once.** That's what makes it "this ring only": the
  oranges pushed during the loop wait for the next minute.
- **Seed every source first.** Pushing rotten oranges as you find them mid-BFS gives
  some of them a head start and the wrong time.
- **Mark at push.** Rot the orange when you push it, or two rotten neighbours both push
  it and `fresh` goes negative.
- **The `-1` case** is a fresh orange with no path to any rotten one. Counting `fresh`
  up front detects it without re-scanning.

## 🎤 Interview talking points
- *"Multi-source BFS: I put every rotten orange in the queue at time 0, so the BFS rings
  are exactly the minutes."*
- *"I process one ring per iteration with `for _ in range(len(q))` and count rings."*
- *"I count fresh oranges first, so the impossible case is just fresh > 0 at the end."*
- *"O(m·n): each cell enters the queue at most once. Running BFS from each source
  separately would be O(k·m·n)."*

## 🔗 Transfer
EP155 counted components on a grid; today measured **distance** on one, which is why
the stack became a queue. The level loop is the one you wrote for Level Order Traversal
(EP124): a tree is a graph where every ring is a level. EP163 drops the level loop
and writes `dist[v] = dist[u] + 1` instead, and EP171 Word Ladder is this same BFS with
words as cells.

## 📹 Metadata
- **Title:** `Rotting Oranges, put EVERY source in the queue | Graphs #6`
- **Thumbnail:** `multi-source BFS` (orange block)
- **Short:** the 1 x 5 row, single-source saying 3, multi-source saying 2. 35s.
