# EP163 · P14E12 · Shortest Path in an Unweighted Graph   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1

---

## 🎬 Hook
> "Shortest path from the source to every node, every edge costs 1. No Dijkstra, no
> heap, no 'relax the edge if it's shorter'. Plain BFS already visits nodes in order
> of distance, so **the first time you reach a node is the shortest way to reach it.**
> You write the distance down once and never touch it again."

## 📋 Problem, in your words
```
Given an undirected graph as an adjacency list adj (nodes 0..V-1) where
every edge has length 1, and a source node src, return dist where
dist[i] = the fewest edges on any path from src to i,
or -1 if i can't be reached.
```

## 🔢 The example
```
adj = [[1,3], [0,2], [1,6], [0,4], [3,5], [4,6], [2,5,7,8], [6,8], [7,6]],  src = 0

    0 --- 1 --- 2
    |           |
    3           |
    |           |
    4 --- 5 --- 6 --- 7
                |    /
                8 --+

Output: [0, 1, 2, 1, 2, 3, 3, 4, 4]
Why:    6 is reachable as 0-1-2-6 (3 edges) or 0-3-4-5-6 (4 edges): it's 3.
        7 and 8 are one step past 6.

adj = [[3], [3], [], [0, 1]],  src = 3   ->  [1, 1, -1, 0]    <- node 2 is isolated
```

## 🧸 ELI5
> You shout from node 0. Everyone 1 step away hears you after 1 second. They shout,
> and everyone 1 step from *them* hears after 2 seconds. Sound travels in rings.
>
> Write down, next to each person, the second they **first** heard it. Nobody can hear
> it *earlier* on a second hearing, because a later ring is always further away. So the
> first number you write is the final answer.
>
> ```
> second 0: 0
> second 1: 1, 3
> second 2: 2, 4
> second 3: 6, 5          6 heard it from 2; the echo from 5 at second 4 changes nothing
> second 4: 7, 8
> ```

## 🐌 Brute force (say it, don't type it)
DFS every simple path from `src` and keep the shortest length to each node: exponential
in the worst case, because a graph can have exponentially many simple paths. A step up:
Bellman-Ford (EP168) with all weights 1, **O(V · E)**. Both waste effort proving
distances that BFS gets right on first contact.

## 💡 The pattern reveal
**Signal:** "shortest path", "fewest steps / moves", and **no weights** (or all equal).
**Therefore:** Shape C: BFS, writing `dist` at push time.

**Key insight:** BFS dequeues nodes in non-decreasing order of distance. So when `u` is
popped and finds an unvisited `v`, `dist[u] + 1` is the best `v` will ever get. The
`dist` array is also the visited array: `-1` means "not reached yet".

```python
dist = [-1] * V
dist[src] = 0
q = deque([src])
while q:
    u = q.popleft()
    for v in adj[u]:
        if dist[v] == -1:            # first arrival IS the shortest
            dist[v] = dist[u] + 1
            q.append(v)
```

No `min()`, no comparison, no re-visiting. That's what you give up the moment edges
have different weights, and why EP164 needs a heap.

## 🔍 Dry run: the 9-node example, `src = 0`

| step | pop (dist) | neighbours | newly set | queue after |
|---|---|---|---|---|
| 0 | - | - | dist[0] = 0 | `[0]` |
| 1 | 0 (0) | 1, 3 | dist[1] = 1, dist[3] = 1 | `[1, 3]` |
| 2 | 1 (1) | 0 ✗, 2 | dist[2] = 2 | `[3, 2]` |
| 3 | 3 (1) | 0 ✗, 4 | dist[4] = 2 | `[2, 4]` |
| 4 | 2 (2) | 1 ✗, 6 | **dist[6] = 3** | `[4, 6]` |
| 5 | 4 (2) | 3 ✗, 5 | dist[5] = 3 | `[6, 5]` |
| 6 | 6 (3) | 2 ✗, 5 ✗, 7, 8 | dist[7] = 4, dist[8] = 4 | `[5, 7, 8]` |
| 7 | 5 (3) | 4 ✗, 6 ✗ | - | `[7, 8]` |
| 8 | 7 (4) | 6 ✗, 8 ✗ | - | `[8]` |
| 9 | 8 (4) | 7 ✗, 6 ✗ | - | `[]` |

✗ = already has a distance, skipped. Answer **`[0, 1, 2, 1, 2, 3, 3, 4, 4]`** ✓.

Step 7 is the proof in miniature: 5 is 3 away and is a neighbour of 6, so it offers 6
a path of length 4. 6 already has 3, and BFS doesn't even look.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def shortestPath(self, adj: List[List[int]], src: int) -> List[int]:
        """Fewest edges from src to every node; -1 where unreachable.

        Time:  O(V + E), each node is queued once, each adjacency entry read once.
        Space: O(V), the dist array and the queue.
        """
        dist = [-1] * len(adj)                      # -1 doubles as "not visited"
        dist[src] = 0
        q = deque([src])

        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1           # first arrival is the shortest
                    q.append(v)

        return dist
```
**Time:** O(V + E) · **Space:** O(V)

## ⚠️ Gotchas
- **Set `dist` at push, not at pop.** Setting it at pop lets a node be pushed by two
  neighbours from the same ring; it still ends with the right number, but it's the
  EP154 mistake and it can blow up the queue.
- **`-1` for unreachable** comes free from the initial fill. Don't use `float('inf')`
  here: GfG wants `-1`.
- **Only for equal weights.** Give one edge weight 5 and BFS returns wrong answers
  without complaint. Say "unweighted, so BFS" out loud, it's the reason the solution
  is allowed to be this short.
- **Directed input?** The code doesn't care: it follows `adj` as given.
- **Want the actual path, not just the length?** Store `parent[v] = u` at the same line
  you set `dist[v]`, then walk back from the target.

## 🎤 Interview talking points
- *"All edges cost 1, so BFS: it visits in order of distance, so the first time I reach
  a node is its shortest distance."*
- *"dist doubles as visited, -1 means unseen. No relaxation step needed."*
- *"O(V + E). With weighted edges I'd switch to Dijkstra; with 0 and 1 weights, a deque
  (0-1 BFS) is enough."*
- *"To reconstruct the path I'd record a parent at the moment I set the distance."*

## 🔗 Transfer
This is EP154's BFS with a number written at push time, and EP157 Rotten Oranges was the
same thing counted by levels instead. Tomorrow (EP164) edges get **weights**, "first
arrival is shortest" stops being true, and the queue becomes a priority queue. Keep this
code open next to it: Dijkstra is these ten lines plus a heap and one stale-entry check.

## 📹 Metadata
- **Title:** `Shortest Path without Dijkstra, BFS already knows | Graphs #12`
- **Thumbnail:** `first arrival = shortest` (green block)
- **Short:** the rings spreading from 0, node 6 getting 3 and ignoring the 4 from node 5.
  35s.
