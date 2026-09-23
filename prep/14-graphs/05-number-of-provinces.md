# EP156 · P14E05 · Number of Provinces   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/number-of-provinces/description/

---

## 🎬 Hook
> "This looks like a grid problem. It's an n by n matrix of 1s and 0s, just like
> yesterday. Flood-fill it like a grid and you get the **wrong answer**. It's not a
> map, it's a **friendship table**, and once you read it that way, it's yesterday's
> code with one loop changed."

## 📋 Problem, in your words
```
There are n cities. isConnected[i][j] = 1 means city i and city j have a
direct road; 0 means they don't. The matrix is symmetric and isConnected[i][i] = 1.

A province is a group of cities connected directly or through other cities.
Return the number of provinces.
```

## 🔢 The example
```
Input:  [[1,1,0],
         [1,1,0],
         [0,0,1]]
Output: 2          <- {0, 1} and {2}

Input:  [[1,0,0,1],
         [0,1,1,0],
         [0,1,1,0],
         [1,0,0,1]]
Output: 2          <- {0, 3} and {1, 2}

        0 ----- 3        1 ----- 2

Input:  3 x 3 identity  ->  3     <- nobody is connected to anybody else
```

## 🧸 ELI5
> The matrix is a **seating chart of who knows whom**. Row 0 is city 0's contact list:
> a 1 in column 3 means "0 knows 3". It is *not* a picture where neighbouring 1s touch.
>
> So you do what you'd do at a party: pick someone nobody has talked to yet, and
> have them introduce you to everyone they know, and everyone *those* people know,
> until the chain runs dry. That's one friend group. Then pick the next person nobody
> has talked to.
>
> ```
> matrix row 0: [1, 0, 0, 1]   -> 0 knows 3
> matrix row 3: [1, 0, 0, 1]   -> 3 knows 0   (already met)
> group 1 = {0, 3}
>
> next stranger: 1
> matrix row 1: [0, 1, 1, 0]   -> 1 knows 2
> group 2 = {1, 2}
> ```
>
> Read it like a grid and you'd say (1,1), (1,2), (2,1), (2,2) are one "island" and
> (0,0), (0,3), (3,0), (3,3) are **four** separate ones: 5 islands, wrong.

## 🐌 Brute force (say it, don't type it)
Compute full reachability: for every city, run a search, record the set it reaches,
then count distinct sets. That's n searches of O(n²) each on a matrix: **O(n³)**. It's
redundant because two cities in the same province compute the same set; once a city's
province is known, you never need to search from it again.

## 💡 The pattern reveal
**Signal:** "connected directly or indirectly", "groups", "provinces".
**Therefore:** Shape B: count connected components, the outer loop from EP155.

**Key insight:** the matrix is an **adjacency matrix**. The nodes are the n cities (the
rows), not the n² cells. `u`'s neighbours are every column `v` with a 1 in row `u`.

| | Number of Islands (EP155) | Number of Provinces (today) |
|---|---|---|
| input | m x n grid | n x n adjacency matrix |
| a node is | a cell `(r, c)` | a row `i` |
| neighbours of a node | the 4 cells around it | every `j` with `isConnected[i][j] == 1` |
| visited | sink the cell | `visited[i]` |
| answer | number of DFS starts | number of DFS starts |

## 🔍 Dry run: the 4-city example
`visited = [F, F, F, F]`, `provinces = 0`.

| step | outer `i` | action | DFS path | visited after | provinces |
|---|---|---|---|---|---|
| 1 | 0 | unvisited, **start** | visit 0; row 0 has 1s at 0, 3; 3 unvisited, visit 3; row 3 has 1s at 0, 3, both visited | `[T, F, F, T]` | 1 |
| 2 | 1 | unvisited, **start** | visit 1; row 1 has 1s at 1, 2; visit 2; row 2 all visited | `[T, T, T, T]` | 2 |
| 3 | 2 | visited, skip | - | - | 2 |
| 4 | 3 | visited, skip | - | - | 2 |

Answer **2** ✓. Step 1 jumps from city 0 straight to city 3, skipping 1 and 2. On a
grid that jump would be impossible, and that's the difference.

## ✅ Optimal solution
```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """Count connected components of the graph given as an adjacency matrix.

        Time:  O(n^2), each city is visited once and scans its whole row of n entries.
        Space: O(n), the visited array and a recursion stack up to n deep.
        """
        n = len(isConnected)
        visited = [False] * n

        def dfs(u: int) -> None:
            visited[u] = True
            for v in range(n):                      # a row of the matrix is u's neighbours
                if isConnected[u][v] == 1 and not visited[v]:
                    dfs(v)

        provinces = 0
        for i in range(n):
            if not visited[i]:
                provinces += 1                      # a fresh start is a new province
                dfs(i)
        return provinces
```
**Time:** O(n²) · **Space:** O(n)

## ⚠️ Gotchas
- **Don't flood-fill the matrix like a grid.** The 4-city example returns 5 if you do.
  The nodes are rows, and "adjacent" means a 1 in the row, not a neighbouring cell.
- **The diagonal is all 1s.** `isConnected[u][u] = 1` means `u` lists itself as a
  neighbour. Harmless, because `u` is already visited when you check it, but it's why
  you can't count provinces by counting rows with a single 1.
- **O(n²) is optimal here.** The input itself has n² entries; you can't answer without
  reading them. Converting to an adjacency list first doesn't beat it.
- **Recursion depth is at most n = 200**, so recursive DFS is safe here, unlike a
  300 x 300 grid.
- **Only scan half the matrix? No.** It's symmetric, but DFS needs every neighbour of
  `u`, which is the whole row.

## 🎤 Interview talking points
- *"This is an adjacency matrix, not a grid: n nodes, and row u lists u's
  neighbours."* ← the whole problem is noticing this.
- *"Count connected components: DFS from every unvisited city, count the starts."*
- *"O(n²), which is the size of the input, so it's optimal."*
- *"Union-Find works too: union every (i, j) with a 1, then count roots. Same bound
  with near-constant union and find."*

## 🔗 Transfer
EP155 and EP156 are the same algorithm on two input formats, a grid and a matrix. Keep
both in mind, because EP161 Bipartite hands you a third format (an adjacency list) and
the same "start from every unvisited node" loop. Tomorrow (EP157) stays on a grid but
asks *how long*, which is the cue to switch from DFS to BFS.

## 📹 Metadata
- **Title:** `Number of Provinces, it's not a grid (and that's the trap) | Graphs #5`
- **Thumbnail:** `rows are nodes` (red block)
- **Short:** grid flood-fill counting 5 on the 4-city matrix, then the row-reading DFS
  counting 2. 45s.
