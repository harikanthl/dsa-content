# EP165 · P14E14 · Network Delay Time   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/network-delay-time/

---

## 🎬 Hook
> "A signal leaves node k. How long until **every** node has it? It sounds like a new
> problem. It isn't. The time each node hears the signal is its shortest-path distance,
> and 'everyone has it' is the **slowest** of those. That's yesterday's Dijkstra,
> followed by one call to `max`."

## 📋 Problem, in your words
```
n nodes labelled 1..n. times[i] = [u, v, w]: a DIRECTED edge u -> v that
takes w time. A signal starts at node k.

Return the minimum time for ALL n nodes to receive it,
or -1 if some node can never receive it.
```

## 🔢 The example
```
times = [[2,1,1], [2,3,1], [3,4,1]], n = 4, k = 2

    2 --1--> 1
    |
    1
    v
    3 --1--> 4

Output: 2       <- 1 and 3 hear at t=1, 4 hears at t=2

times = [[1,2,1], [1,3,4], [2,3,2]], n = 3, k = 1

    1 --1--> 2
     \       |
      4      2
       \     v
        +--> 3

Output: 3       <- 3 hears via 1->2->3 at t=3, not the direct t=4

times = [[1,2,1]], n = 2, k = 2   ->   -1     <- edges are one-way; 1 never hears
```

## 🧸 ELI5
> Light a fuse at node k. Every wire is a fuse that burns in `w` seconds, and at every
> node the flame splits and runs down every outgoing wire. A node "has the signal" the
> first moment **any** flame reaches it.
>
> When is the *whole* network lit? When the **last** node catches. And each node catches
> at its fastest possible arrival, which is exactly the shortest path.
>
> ```
> k = 1:  node 1 at t=0
>         node 2 at t=1 (1 -> 2)
>         node 3 at t=3 (1 -> 2 -> 3), beats the direct fuse at t=4
>         whole network lit at max(0, 1, 3) = 3
> ```

## 🐌 Brute force (say it, don't type it)
Simulate time tick by tick, spreading the signal along edges as they finish: the number
of ticks depends on the weights (up to 100 per edge here), not the graph size, and each
tick scans all edges. Or run Bellman-Ford, **O(n · E)**. Both correct; Dijkstra is
**O(E log n)** and is exactly what the question is asking for.

## 💡 The pattern reveal
**Signal:** weighted directed edges, a single source, "how long until all…".
**Therefore:** Shape E: Dijkstra, then **aggregate**.

**Key insight:** "time for all nodes to receive" = `max` over nodes of "time for this
node to receive" = `max(dist)`. And if any `dist` is still infinity, some node is
unreachable, so the answer is `-1`.

```python
# ... EP164's Dijkstra from k ...
worst = max(dist[1:])                 # 1-indexed: skip slot 0
return worst if worst < inf else -1
```

Two changes from EP164: edges are **directed** (one append), and nodes are **1-indexed**.

## 🔍 Dry run: `times = [[1,2,1], [1,3,4], [2,3,2]]`, `n = 3`, `k = 1`
`adj = {1: [(2,1), (3,4)], 2: [(3,2)]}`, `dist = [-, 0, ∞, ∞]` (slot 0 unused).

| step | pop `(d, u)` | stale? | relaxations | dist[1..3] after | heap after |
|---|---|---|---|---|---|
| 0 | - | - | - | `[0, ∞, ∞]` | `[(0,1)]` |
| 1 | `(0, 1)` | no | 2: 0+1=1 ✓; 3: 0+4=4 ✓ | `[0, 1, 4]` | `[(1,2), (4,3)]` |
| 2 | `(1, 2)` | no | 3: 1+2=**3 < 4** ✓ | `[0, 1, 3]` | `[(3,3), (4,3)]` |
| 3 | `(3, 3)` | no | no outgoing edges | `[0, 1, 3]` | `[(4,3)]` |
| 4 | `(4, 3)` | **yes**, 4 > 3 | skipped | `[0, 1, 3]` | `[]` |

`max(0, 1, 3) = 3`, nothing is infinity → **3** ✓.

For `[[1,2,1]], n = 2, k = 2`: node 2 has no outgoing edges, the heap empties at once,
`dist[1]` is still ∞, so **-1** ✓.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """Time for a signal from k to reach every node, or -1 if some never do.

        Time:  O((n + E) log n), Dijkstra with a binary heap.
        Space: O(n + E), the adjacency list and heap.
        """
        adj = [[] for _ in range(n + 1)]            # 1-indexed; slot 0 unused
        for u, v, w in times:
            adj[u].append((v, w))                   # directed: one append

        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        pq = [(0, k)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue                            # stale entry
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))

        worst = max(dist[1:])                       # the last node to hear it
        return worst if worst < float('inf') else -1
```
**Time:** O((n + E) log n) · **Space:** O(n + E)

## ⚠️ Gotchas
- **`max(dist[1:])`, not `max(dist)`.** Slot 0 is an unused infinity, and including it
  returns -1 for every input.
- **Directed.** Adding the reverse edge answers a different question and turns the third
  example's -1 into 1.
- **`max`, not `sum`.** The signal travels down every branch at once. The total time is
  the slowest arrival, not the sum of all delays.
- **-1 check after Dijkstra, not during.** You can't know a node is unreachable until
  the heap is empty.
- **Early exit is possible:** count finalised nodes and stop when you've popped n of
  them. Worth saying; not needed.
- **n = 1** with no edges: `dist[1:] = [0]`, answer 0. Correct.

## 🎤 Interview talking points
- *"Every node receives the signal at its shortest-path time from k, so this is
  single-source shortest paths with non-negative weights: Dijkstra."*
- *"The answer is the maximum of those distances, or -1 if any is still infinite."*
- *"Edges are directed and nodes are 1-indexed; I size arrays n + 1 and skip slot 0."*
- *"O(E log n). With n ≤ 100 Bellman-Ford would also pass, but Dijkstra is the right
  tool for non-negative weights."*

## 🔗 Transfer
EP164 plus a `max`. That aggregation step is the only new idea, and it's a useful one:
many graph questions are "run the standard algorithm, then summarise the dist array".
Tomorrow (EP166) keeps Dijkstra but changes what a path **costs**: not the sum of its
edges, but its single worst edge.

## 📹 Metadata
- **Title:** `Network Delay Time, Dijkstra plus one max() | Graphs #14`
- **Thumbnail:** `max(dist)` (orange block)
- **Short:** the fuse burning through the 3-node graph, node 3 catching at t=3 via the
  detour. 35s.
