# EP155 · P14E04 · Number of Islands   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/number-of-islands/description/

---

## 🎬 Hook
> "Nobody hands you a graph here. You get a grid of 1s and 0s, and the moment you see
> that **every cell is a node and its four neighbours are its edges**, this becomes
> yesterday's DFS. The answer isn't something DFS computes. It's how many times you had
> to **start** one."

## 📋 Problem, in your words
```
Given an m x n grid of '1' (land) and '0' (water), count the islands.

  - an island is land connected up / down / left / right (NOT diagonally)
  - everything outside the grid is water
  - the grid holds STRINGS '1' and '0', not ints
```

## 🔢 The example
```
Input:
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1
Output: 3
Why:    top-left 2x2 block, the lone middle cell, the bottom-right pair.
        (2,2) and (3,3) touch only diagonally, so they're separate.

Input:
  1 1 1 1 0
  1 1 0 1 0
  1 1 0 0 0
  0 0 0 0 0
Output: 1        <- one big, oddly shaped island

Input:  [["0"]]  ->  0
```

## 🧸 ELI5
> You're flying over a map with a bucket of paint. You scan it row by row, left to
> right. Whenever you spot land that **isn't painted yet**, you shout "new island!" and
> then paint that whole island, spreading to every piece of land you can walk to.
>
> ```
> scan (0,0): land, unpainted  -> "island 1!"  paint (0,0) (0,1) (1,0) (1,1)
> scan (0,1): painted already  -> ignore
> ...
> scan (2,2): land, unpainted  -> "island 2!"  paint (2,2)
> scan (3,3): land, unpainted  -> "island 3!"  paint (3,3) (3,4)
> scan (3,4): painted already  -> ignore
> ```
>
> You never count an island twice, because by the time the scan reaches its second
> cell, the painting already covered it.

## 🐌 Brute force (say it, don't type it)
Give every land cell its own label, then repeatedly sweep the grid merging labels of
adjacent land cells until nothing changes, and count distinct labels. Each sweep is
O(m·n) and a long snaking island can need O(m·n) sweeps before the labels settle:
**O((m·n)²)**. The flood fill does each cell once.

## 💡 The pattern reveal
**Signal:** a **grid**, and "connected" / "island" / "region".
**Therefore:** Shape B: DFS flood fill, with the outer loop that counts starts.

**Key insight:** one DFS explores exactly one connected component. So the number of
islands is the number of times the outer loop finds unvisited land and has to start a
fresh DFS.

```python
count = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':      # land nobody has painted yet
            count += 1             # every fresh start is a new island
            sink(r, c)             # paint the whole island so it's never counted again
```

The grid is its own `visited` set: overwrite `'1'` with `'0'` ("sink" the land) as you
visit it. No extra memory.

## 🔍 Dry run: the 4 x 5 grid above
Only the cells where the outer loop does something are shown.

| step | outer loop at | cell is | action | cells sunk by this DFS | count |
|---|---|---|---|---|---|
| 1 | (0,0) | `'1'` | **start DFS** | (0,0) (1,0) (0,1) (1,1) | 1 |
| 2 | (0,1) | `'0'` (sunk in step 1) | skip | - | 1 |
| 3 | (1,0), (1,1) | `'0'` (sunk) | skip | - | 1 |
| 4 | (2,2) | `'1'` | **start DFS** | (2,2); its 4 neighbours are all water | 2 |
| 5 | (3,3) | `'1'` | **start DFS** | (3,3) (3,4) | 3 |
| 6 | (3,4) | `'0'` (sunk in step 5) | skip | - | 3 |

Answer **3** ✓. Step 4 is the diagonal trap: (3,3) is diagonal to (2,2), so the DFS
from (2,2) doesn't reach it, and it gets its own start in step 5.

The DFS in step 1, with an explicit stack (pop from the end):

| pop | unvisited land neighbours, sunk and pushed | stack after |
|---|---|---|
| - | (0,0) is sunk and pushed before the loop | `[(0,0)]` |
| (0,0) | (1,0), (0,1) | `[(1,0), (0,1)]` |
| (0,1) | (1,1) | `[(1,0), (1,1)]` |
| (1,1) | none left | `[(1,0)]` |
| (1,0) | none left | `[]` |

## ✅ Optimal solution
```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """Count 4-directionally connected groups of '1' cells.

        Time:  O(m*n), every cell is sunk at most once and checked by at most 4 neighbours.
        Space: O(m*n) worst case for the stack (a grid that is all land).
        """
        rows, cols = len(grid), len(grid[0])
        count = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '1':
                    continue
                count += 1                          # a fresh start is a new island
                grid[r][c] = '0'                    # sink at push: never pushed twice
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    for nr, nc in ((cr+1, cc), (cr-1, cc), (cr, cc+1), (cr, cc-1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            stack.append((nr, nc))

        return count
```
**Time:** O(m·n) · **Space:** O(m·n)

## ⚠️ Gotchas
- **Strings, not ints.** `grid[r][c] == 1` is always `False` and you return 0 for
  everything. The cells are `'1'` and `'0'`.
- **Four directions, not eight.** Diagonal cells are not connected. Add the four
  diagonals and example 1 returns 1: (1,1), (2,2) and (3,3) chain up corner to corner.
- **Iterative, not recursive, for a 300 x 300 grid.** An all-land grid makes recursive
  DFS 90,000 calls deep, far past Python's limit. The stack version has no such limit.
- **Sink at push, not at pop.** Same reason as BFS: sink at pop and a cell reachable
  from two neighbours is pushed twice.
- **You're mutating the input.** Fine on LeetCode, but say it out loud. If the caller
  needs the grid back, use a `visited` set instead (same complexity, O(m·n) extra).
- **Bounds check first.** `0 <= nr < rows` must come before `grid[nr][nc]`, or `-1`
  silently wraps to the last row in Python and you connect cells that aren't adjacent.

## 🎤 Interview talking points
- *"A grid is an implicit graph: each cell is a node, its four neighbours are its
  edges. I never build an adjacency list."*
- *"The answer is the number of times the outer loop has to start a new DFS, because
  each DFS consumes exactly one island."*
- *"I sink cells as I visit them, so the grid doubles as the visited set. If mutation
  isn't allowed, a set of coordinates works the same."*
- *"Iterative DFS because recursion depth could reach m times n."*
- *"Union-Find is the other standard answer, and it shines if land is added cell by
  cell (Number of Islands II)."*

## 🔗 Transfer
Tomorrow (EP156) Number of Provinces is **exactly this count** on an adjacency matrix
instead of a grid, and it's a good test of whether you've seen through the input
format. EP157 keeps the grid and the four neighbours but swaps the stack for a queue,
because it asks *how long*, not *how many*. EP162 Surrounded Regions is this flood fill
started from the border instead of from every cell.

## 📹 Metadata
- **Title:** `Number of Islands, count the starts, not the land | Graphs #4`
- **Thumbnail:** `count += 1` on a map (green block)
- **Short:** the scan line moving across the grid, painting one island per "new
  island!" shout. 40s.
