# EP162 · P14E11 · Surrounded Regions   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/surrounded-regions/

---

## 🎬 Hook
> "Flip every region of O's that's completely surrounded by X's. The hard way: for each
> region, check whether it can escape to the edge. The easy way is to **turn the
> question inside out**: start at the edge, mark everything that **can** escape, and
> flip whatever's left. Same flood fill as Number of Islands, different starting line."

## 📋 Problem, in your words
```
An m x n board of 'X' and 'O'. A region is a 4-connected group of 'O's.
A region is SURROUNDED if none of its cells touch the board's border.

Flip every surrounded region's 'O's to 'X', in place. Return nothing.
Any region with at least one 'O' on the border survives untouched.
```

## 🔢 The example
```
Input:                      Output:
  X X X X                     X X X X
  X O O X                     X X X X
  X X O X                     X X X X
  X O X X                     X O X X    <- (3,1) is on the border: it survives

Input:                      Output:
  X X X X X                   X X X X X
  X O X O X                   X X X O X
  X O X O O                   X X X O O   <- right region touches the border at (2,4)
  X X X X X                   X X X X X      left region doesn't: flipped
```

## 🧸 ELI5
> The board is a walled city with a flood coming. The O's are open ground, the X's are
> walls. Water pours in from **outside the city**, through any gap in the outer wall,
> and spreads across all the open ground it can reach.
>
> When the flood stops, any open ground that stayed **dry** was completely sealed in by
> walls. That ground is "surrounded". Fill it in.
>
> ```
> X X X X X
> X O X O X        water enters at (2,4), spreads to (2,3), then (1,3)
> X O X O ~        (1,1) and (2,1) never get wet
> X X X X X        -> they're surrounded -> flip them
> ```
>
> You never had to ask "can this region escape?" region by region. The water answered
> for all of them at once.

## 🐌 Brute force (say it, don't type it)
For each O, run a BFS to see whether its region reaches the border; flip it if not.
That repeats the same region's search once per cell in it: **O((m·n)²)** in the worst
case. Doing it once per *region* is better, but you still need to collect the region
before you know whether to flip it, which is fiddly. Flooding from the border does one
traversal of the whole board and needs no bookkeeping.

## 💡 The pattern reveal
**Signal:** "surrounded", "enclosed", "can't reach the edge".
**Therefore:** Shape B: flood fill **from the border**.

**Key insight:** "surrounded" is hard to test directly, but its opposite, "connected to
the border", is plain reachability from a known set of starts. Mark everything reachable
from a border O as safe; every O that isn't marked is surrounded by definition.

Three passes, all O(m·n):

| pass | what it does |
|---|---|
| 1. flood | from every border `'O'`, DFS and mark reached cells `'S'` (safe) |
| 2. flip | every remaining `'O'` → `'X'` |
| 3. restore | every `'S'` → `'O'` |

Passes 2 and 3 are one loop over the board.

## 🔍 Dry run: the 4 x 5 board
Border cells that are `'O'`: only **(2,4)**.

| step | action | stack | cells marked `'S'` |
|---|---|---|---|
| 1 | border scan finds (2,4), mark `'S'`, push | `[(2,4)]` | (2,4) |
| 2 | pop (2,4): neighbours (3,4) X, (1,4) X, (2,5) off-board, (2,3) **O** | `[(2,3)]` | (2,4) (2,3) |
| 3 | pop (2,3): (3,3) X, (1,3) **O**, (2,4) already S, (2,2) X | `[(1,3)]` | + (1,3) |
| 4 | pop (1,3): (2,3) S, (0,3) X, (1,4) X, (1,2) X | `[]` | done |

Board after the flood, then after the flip/restore pass:

```
after flood           after flip + restore
X X X X X             X X X X X
X O X S X             X X X O X      (1,1): 'O' -> 'X'    (1,3): 'S' -> 'O'
X O X S S             X X X O O      (2,1): 'O' -> 'X'    (2,3), (2,4): 'S' -> 'O'
X X X X X             X X X X X
```

Matches the expected output ✓. The left region was never touched by the flood, so it
was still `'O'` when the flip pass came through.

## ✅ Optimal solution
```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """Flip every 'O' region not connected to the border into 'X', in place.

        Time:  O(m*n), each cell is marked at most once and scanned twice.
        Space: O(m*n) worst case for the DFS stack.
        """
        rows, cols = len(board), len(board[0])

        def flood(r: int, c: int) -> None:
            board[r][c] = 'S'                           # safe: reaches the border
            stack = [(r, c)]
            while stack:
                cr, cc = stack.pop()
                for nr, nc in ((cr+1, cc), (cr-1, cc), (cr, cc+1), (cr, cc-1)):
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O':
                        board[nr][nc] = 'S'
                        stack.append((nr, nc))

        for r in range(rows):                           # left and right columns
            for c in (0, cols - 1):
                if board[r][c] == 'O':
                    flood(r, c)
        for c in range(cols):                           # top and bottom rows
            for r in (0, rows - 1):
                if board[r][c] == 'O':
                    flood(r, c)

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'                   # never reached: surrounded
                elif board[r][c] == 'S':
                    board[r][c] = 'O'                   # reached: put it back
```
**Time:** O(m·n) · **Space:** O(m·n)

## ⚠️ Gotchas
- **Flip and restore in one pass, with `elif`.** Two `if`s in the wrong order would turn
  an `'S'` into `'O'` and then into `'X'`.
- **Use a third marker, not `'X'`.** Marking safe cells `'X'` during the flood makes them
  indistinguishable from walls, and you can't restore them.
- **All four borders.** Scanning only rows 0 and m-1 misses O's on the left and right
  columns. Corners get checked twice; the `== 'O'` test makes that harmless.
- **Single row or single column.** Every cell is a border cell, nothing flips.
  `(0, cols - 1)` is `(0, 0)` when `cols == 1`, which just checks one cell twice.
- **Iterative flood.** A 200 x 200 board of O's is 40,000 cells deep for recursive DFS.
- **It returns `None`.** LeetCode checks the board you mutated. Returning a new board
  does nothing.

## 🎤 Interview talking points
- *"'Surrounded' is hard to check directly, so I invert it: anything connected to the
  border is safe, and I find all of those with one flood fill from the border."*
- *"Three states: O, X, and a temporary S for safe. Then one pass flips O to X and S
  back to O."*
- *"O(m·n) time. Starting from the boundary is the same trick as Pacific Atlantic Water
  Flow."*
- *"Iterative DFS, or BFS, so a big open board can't overflow the stack."*

## 🔗 Transfer
EP155 flooded from every cell and counted starts. Today flooded from a **chosen set** of
starts, the border, and used what it reached. Multi-source again, like EP157, but for
reachability instead of distance. Tomorrow (EP163) goes back to BFS and makes the
distance explicit: `dist[v] = dist[u] + 1`, the foundation for Dijkstra the day after.

## 📹 Metadata
- **Title:** `Surrounded Regions, flood from the edge, not the middle | Graphs #11`
- **Thumbnail:** `start at the border` (blue block)
- **Short:** water pouring in through (2,4) and the dry pocket on the left getting
  filled. 40s.
