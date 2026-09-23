# EP161 · P14E10 · Is Graph Bipartite? (Graph Colouring)   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/is-graph-bipartite/

---

## 🎬 Hook
> "Can you split everyone into two teams so that nobody is on the same team as someone
> they're connected to? You don't search over all 2ⁿ splits. You put the first person
> on team A, and **everyone else's team is forced**. BFS just follows the forcing, and
> the first contradiction is your answer."

## 📋 Problem, in your words
```
graph[u] lists the neighbours of node u (undirected, no self-loops).
Return True if the nodes can be split into two sets A and B such that
every edge goes between A and B, never inside one set.

  - the graph may be disconnected
```

## 🔢 The example
```
graph = [[1,3], [0,2], [1,3], [0,2]]

    0 --- 1
    |     |
    3 --- 2

Output: True      <- A = {0, 2}, B = {1, 3}. A 4-cycle alternates cleanly.

graph = [[1,2,3], [0,2], [0,1,3], [0,2]]

    0 --- 1
    | \   |
    3 --- 2

Output: False     <- 0, 1, 2 form a triangle. Three people, two teams, one clash.
```

## 🧸 ELI5
> Two teams: red and blue. Rule: if two people are friends, they must be on
> **different** teams.
>
> Put person 0 on red. Then every friend of 0 **must** be blue, no choice. Every friend
> of theirs **must** be red. You just keep following the rule. You fail only if someone
> is told "be blue" when they're already red.
>
> ```
> triangle 0-1-2:
>   0 = red
>   1 = blue  (friend of 0)
>   2 = blue  (friend of 0)
>   but 1 and 2 are friends, and both are blue  -> impossible
> ```
>
> Any loop with an **odd** number of people breaks the rule, and a loop with an even
> number never does. That's the maths fact behind bipartite graphs, and colouring
> finds the odd loop without you looking for it.

## 🐌 Brute force (say it, don't type it)
Try every assignment of two colours to n nodes and check every edge: **O(2ⁿ · E)**.
Wasteful because once one node's colour is fixed, its whole component's colours are
determined; there are only 2 real choices per component, and they're mirror images.

## 💡 The pattern reveal
**Signal:** "split into two groups such that…", "two colours", "no two adjacent…".
**Therefore:** Shape D: **2-colouring by BFS**.

**Key insight:** colour a start node 0, and every neighbour gets `1 - color[u]`. A
neighbour that already has **your** colour is the only way to fail.

| neighbour `v` is… | meaning | action |
|---|---|---|
| uncoloured | not reached yet | paint `1 - color[u]`, push |
| the **other** colour | consistent | nothing |
| **the same** colour | an odd cycle | **return False** |

```python
color[start] = 0
while q:
    u = q.popleft()
    for v in graph[u]:
        if color[v] == -1:
            color[v] = 1 - color[u]; q.append(v)
        elif color[v] == color[u]:
            return False
```

`color` doubles as `visited`: `-1` means unvisited.

## 🔍 Dry run: the triangle graph `[[1,2,3], [0,2], [0,1,3], [0,2]]`
`color = [-1, -1, -1, -1]`.

| step | pop (colour) | neighbour | its colour | action | queue after | color after |
|---|---|---|---|---|---|---|
| 0 | - | - | - | paint 0 → 0 | `[0]` | `[0, -1, -1, -1]` |
| 1 | 0 (0) | 1 | -1 | paint 1 → 1 | `[1]` | `[0, 1, -1, -1]` |
| 2 | 0 (0) | 2 | -1 | paint 2 → 1 | `[1, 2]` | `[0, 1, 1, -1]` |
| 3 | 0 (0) | 3 | -1 | paint 3 → 1 | `[1, 2, 3]` | `[0, 1, 1, 1]` |
| 4 | 1 (1) | 0 | 0 | different, fine | `[2, 3]` | - |
| 5 | 1 (1) | 2 | **1** | **same as 1, return False** | - | - |

**False** ✓. Step 5 is the triangle 0-1-2: 1 and 2 were both forced to colour 1 by
node 0, and they're neighbours.

The square `[[1,3], [0,2], [1,3], [0,2]]` goes: 0 → 0; 1, 3 → 1; then 1 paints 2 → 0;
every later check sees the opposite colour. Queue empties, **True**.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """True if the nodes can be 2-coloured with no edge inside one colour.

        Time:  O(V + E), each node is coloured once, each adjacency entry read once.
        Space: O(V), the colour array and the queue.
        """
        n = len(graph)
        color = [-1] * n                            # -1 = not visited yet

        for start in range(n):                      # every component needs its own start
            if color[start] != -1:
                continue
            color[start] = 0
            q = deque([start])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]     # forced: the opposite of u
                        q.append(v)
                    elif color[v] == color[u]:      # forced both ways: odd cycle
                        return False
        return True
```
**Time:** O(V + E) · **Space:** O(V)

## ⚠️ Gotchas
- **Disconnected graphs.** LeetCode's tests include isolated nodes and separate
  components. BFS from node 0 alone would miss a triangle in another component. Loop
  over every start.
- **Isolated nodes are fine.** A node with no edges gets a colour and never conflicts.
- **Don't treat "already coloured" as failure.** Only the **same** colour is a
  failure; the opposite colour is the expected case (step 4).
- **`1 - color[u]`** flips 0 ↔ 1. `not color[u]` works too but mixes bools and ints.
- **DFS works identically.** The traversal order doesn't matter, only that every
  neighbour is checked. BFS is shown because it reads as "ring by ring alternates".
- **The input is already an adjacency list.** No building step, unlike EP152.

## 🎤 Interview talking points
- *"Colouring a node forces its whole component, so I BFS and give each neighbour the
  opposite colour. A neighbour with my colour means it's not bipartite."*
- *"Equivalently: a graph is bipartite iff it has no odd-length cycle, and the colouring
  finds one if it exists."*
- *"I restart from every uncoloured node, because the graph can be disconnected."*
- *"O(V + E). Union-Find also works: union all of u's neighbours together, and fail if u
  ends up in its neighbours' set."*

## 🔗 Transfer
This is BFS (EP154) where the thing you write at push time is a **colour** instead of a
distance. EP163 writes `dist[u] + 1` at the same spot, and the colour here is really just
that distance mod 2. Tomorrow (EP162) is back on a grid, with a different twist: where
you **start** the search.

## 📹 Metadata
- **Title:** `Is Graph Bipartite, one choice forces all the rest | Graphs #10`
- **Thumbnail:** `red / blue` (split block)
- **Short:** the triangle getting coloured and the third node having nowhere to go. 30s.
