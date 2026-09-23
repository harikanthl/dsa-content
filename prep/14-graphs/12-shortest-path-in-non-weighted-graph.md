# EP163 · P14E12 · Shortest Path in an Unweighted Graph   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1

---

## 🎬 Hook
> "Shortest path from src to dest, every edge costs 1. No Dijkstra, no heap, no
> 'relax the edge if it's shorter'. Plain BFS already visits nodes in order of
> distance, so **the first time you reach a node is the shortest way to reach it.**
> The moment dest gets a number, you're done."

## 📋 Problem, in your words
```
Given an undirected graph with V nodes (0..V-1) as an edge list, where every
edge has length 1, and two nodes src and dest, return the fewest edges on
any path from src to dest, or -1 if dest can't be reached.
```

## 🔢 The example
```
V = 9
edges = [[0,1], [0,3], [1,2], [3,4], [4,5], [2,6], [5,6], [6,7], [6,8], [7,8]]
src = 0, dest = 8

    0 --- 1 --- 2
    |           |
    3           |
    |           |
    4 --- 5 --- 6 --- 7
                |    /
                8 --+

Output: 4
Why:    0-1-2-6-8 is 4 edges. The other way round, 0-3-4-5-6-8, is 5.

V = 4, edges = [[0,3], [1,3]], src = 3, dest = 2   ->  -1   <- node 2 has no edges
```

## 🧸 ELI5
> You shout from node 0. Everyone 1 step away hears you after 1 second. They shout,
> and everyone 1 step from *them* hears after 2 seconds. Sound travels in rings.
>
> Write down, next to each person, the second they **first** heard it. Nobody can hear
> it *earlier* on a second hearing, because a later ring is always further away. So the
> first number you write is the final answer, and the moment `dest` hears you, you can
> stop shouting.
>
> ```
> second 0: 0
> second 1: 1, 3
> second 2: 2, 4
> second 3: 6, 5          6 heard it from 2; the echo from 5 changes nothing
> second 4: 7, 8          8 is dest: answer 4, stop
> ```

## 🐌 Brute force (say it, don't type it)
DFS every simple path from `src` to `dest` and keep the shortest: exponential in the
worst case, because a graph can have exponentially many simple paths. A step up:
Bellman-Ford (EP168) with all weights 1, **O(V · E)**. Both waste effort proving
distances that BFS gets right on first contact.

## 💡 The pattern reveal
**Signal:** "shortest path", "fewest steps / moves", and **no weights** (or all equal).
**Therefore:** Shape C: BFS, writing `dist` at push time.

**Key insight:** BFS dequeues nodes in non-decreasing order of distance. So when `u` is
popped and finds an unvisited `v`, `dist[u] + 1` is the best `v` will ever get. The
`dist` array is also the visited array: `-1` means "not reached yet". And because the
first number written is final, you can **return the moment `dest` gets one**.

```python
dist = [-1] * V
dist[src] = 0
q = deque([src])
while q:
    u = q.popleft()
    for v in adj[u]:
        if dist[v] == -1:            # first arrival IS the shortest
            dist[v] = dist[u] + 1
            if v == dest:
                return dist[v]       # final already, stop here
            q.append(v)
return -1
```

No `min()`, no comparison, no re-visiting. That's what you give up the moment edges
have different weights, and why EP164 needs a heap.

## 🔍 Dry run: the 9-node example, `src = 0`, `dest = 8`

Built from the edge list, `adj = [[1,3], [0,2], [1,6], [0,4], [3,5], [4,6], [2,5,7,8],
[6,8], [6,7]]`.

| step | pop (dist) | neighbours | newly set | queue after |
|---|---|---|---|---|
| 0 | - | - | dist[0] = 0 | `[0]` |
| 1 | 0 (0) | 1, 3 | dist[1] = 1, dist[3] = 1 | `[1, 3]` |
| 2 | 1 (1) | 0 ✗, 2 | dist[2] = 2 | `[3, 2]` |
| 3 | 3 (1) | 0 ✗, 4 | dist[4] = 2 | `[2, 4]` |
| 4 | 2 (2) | 1 ✗, 6 | **dist[6] = 3** | `[4, 6]` |
| 5 | 4 (2) | 3 ✗, 5 | dist[5] = 3 | `[6, 5]` |
| 6 | 6 (3) | 2 ✗, 5 ✗, 7, 8 | dist[7] = 4, **dist[8] = 4 = dest, return 4** | (stopped) |

✗ = already has a distance, skipped. Answer **4** ✓. Node 5 is still in the queue when
we return; nothing it could do would beat a number that's already final.

Step 6 is the proof in miniature: 5 is 3 away and is a neighbour of 6, so it could
offer 6 a path of length 4. 6 already has 3, and BFS doesn't even look.

Second example: `adj = [[3], [3], [], [0, 1]]`, start at 3, reach 0 and 1, queue
empties, 2 never gets a number: **-1** ✓.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def shortestPath(self, V, edges, src, dest):
        """Fewest edges from src to dest in an undirected unweighted graph, or -1.

        Time:  O(V + E), each node is queued at most once, each edge read twice.
        Space: O(V + E), the adjacency list, plus O(V) for dist and the queue.
        """
        adj = [[] for _ in range(V)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)                        # undirected: both directions

        if src == dest:
            return 0

        dist = [-1] * V                             # -1 doubles as "not visited"
        dist[src] = 0
        q = deque([src])

        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1           # first arrival is the shortest
                    if v == dest:
                        return dist[v]              # already final, stop early
                    q.append(v)

        return -1                                   # queue ran dry: unreachable
```
**Time:** O(V + E) · **Space:** O(V + E)

## ⚠️ Gotchas
- **Build the adjacency list both ways.** The input is an edge list of an *undirected*
  graph. Add only `u -> v` and example 1 still passes by luck, but `src = 8, dest = 0`
  returns -1.
- **`src == dest` returns 0.** The early exit only fires when a node is *pushed*, and
  `src` is never pushed, so without that line the answer for `src == dest` is -1.
- **Set `dist` at push, not at pop.** Setting it at pop lets a node be pushed by two
  neighbours from the same ring; it still ends with the right number, but it's the
  EP154 mistake and it can blow up the queue.
- **Return at push, not at pop, is also fine and slightly faster.** Checking at pop
  (`if u == dest: return dist[u]`) is correct too; it just processes one more ring.
- **`-1` for unreachable** comes free: the queue empties without ever reaching `dest`.
- **Only for equal weights.** Give one edge weight 5 and BFS returns wrong answers
  without complaint. Say "unweighted, so BFS" out loud, it's the reason the solution
  is allowed to be this short.
- **The classic version** of this problem (older GfG, and most textbooks) returns
  `dist` for **every** node from `src`. Same BFS: drop the early exit and return
  `dist`. If the interviewer asks for all distances, that's a one-line change.
- **Want the actual path, not just the length?** Store `parent[v] = u` at the same line
  you set `dist[v]`, then walk back from `dest`.

## 🎤 Interview talking points
- *"All edges cost 1, so BFS: it visits in order of distance, so the first time I reach
  a node is its shortest distance."*
- *"That also means I can return as soon as dest gets a distance. No need to finish the
  search."*
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
- **Short:** the rings spreading from 0, node 6 getting 3 and ignoring the 4 from node 5,
  then 8 lighting up and the search stopping.
  35s.
