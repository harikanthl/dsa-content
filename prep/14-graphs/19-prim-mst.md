# EP170 · P14E19 · Prim's Minimum Spanning Tree   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1

---

## 🎬 Hook
> "Connect every town with roads, spending as little as possible in total. Not the
> shortest route *from* anywhere, the cheapest way to connect *everything*. Prim's
> algorithm is Dijkstra with **one word changed**: the heap is keyed on the edge
> weight, not the total distance. Same loop, different question."

## 📋 Problem, in your words
```
Given V nodes (0..V-1) and undirected weighted edges [u, v, w] of a
connected graph, return the total weight of a minimum spanning tree:

  - a subset of edges that connects all V nodes
  - with no cycles (so exactly V - 1 edges)
  - and the smallest possible total weight
```

## 🔢 The example
```
V = 5, edges = [[0,1,2], [0,3,6], [1,2,3], [1,3,8], [1,4,5], [2,4,7], [3,4,9]]

         2         3
    0 ------ 1 ------ 2
    |      / |       /
   6|   8/   |5    /7
    |  /     |   /
    3 ------ 4
        9

Output: 16      <- edges 0-1 (2), 1-2 (3), 1-4 (5), 0-3 (6)

V = 3, edges = [[0,1,5], [1,2,3], [0,2,1]]   ->  4     <- 0-2 (1) + 1-2 (3)
V = 2, edges = [[0,1,5]]                     ->  5     <- one edge, one tree
```

## 🧸 ELI5
> You're laying cable to connect houses. You start at one house. Every day, you look at
> **every cable you could lay from the houses already connected to a house that isn't
> yet**, and you lay the **cheapest** one. Repeat until every house is connected.
>
> ```
> connected: {0}           options: 0-1 (2), 0-3 (6)                 lay 0-1 for 2
> connected: {0,1}         options: 0-3 (6), 1-2 (3), 1-3 (8), 1-4 (5)  lay 1-2 for 3
> connected: {0,1,2}       options: 0-3 (6), 1-3 (8), 1-4 (5), 2-4 (7)  lay 1-4 for 5
> connected: {0,1,2,4}     options: 0-3 (6), 1-3 (8), 3-4 (9)        lay 0-3 for 6
> all 5 connected, total 2 + 3 + 5 + 6 = 16
> ```
>
> Notice you never compare *routes*. Once house 1 is connected, it doesn't matter how
> far it is from house 0; it's just "in". Only the next cable's price matters.

## 🐌 Brute force (say it, don't type it)
Try every subset of V − 1 edges, keep the ones that connect everything without a cycle,
take the cheapest: **C(E, V−1)** subsets, exponential. The greedy insight (the cheapest
edge crossing from "connected" to "not yet" is always safe to take, the *cut property*)
turns that into **O(E log V)**.

## 💡 The pattern reveal
**Signal:** "connect all", "minimum total cost", "network / cable / roads to every…".
**Therefore:** Shape F: Prim's, a heap of **edges into the tree**.

**Key insight:** Prim and Dijkstra are the same loop. They push different keys.

| | Dijkstra (EP164) | Prim (today) |
|---|---|---|
| heap entry | `(total distance from source, node)` | `(weight of the one edge in, node)` |
| push when | `d + w < dist[v]` | `v` isn't in the tree yet |
| on pop | skip if stale | skip if already in the tree |
| answers | cheapest path *from the source* | cheapest way *into the tree so far* |

```python
w, u = heapq.heappop(pq)
if in_tree[u]: continue           # already connected by a cheaper edge
in_tree[u] = True
total += w                        # w, NOT a running distance
for v, wv in adj[u]:
    if not in_tree[v]:
        heapq.heappush(pq, (wv, v))   # Dijkstra would push (w + wv, v)
```

## 🔍 Dry run: the 5-node example, start at 0
Heap entries are `(edge weight, node)`.

| step | pop | in tree? | action | total | pushed | heap after |
|---|---|---|---|---|---|---|
| 1 | `(0, 0)` | no | add 0 | 0 | `(2,1) (6,3)` | `(2,1) (6,3)` |
| 2 | `(2, 1)` | no | add 1 via 0-1 | 2 | `(3,2) (8,3) (5,4)` | `(3,2) (5,4) (6,3) (8,3)` |
| 3 | `(3, 2)` | no | add 2 via 1-2 | 5 | `(7,4)` | `(5,4) (6,3) (7,4) (8,3)` |
| 4 | `(5, 4)` | no | add 4 via 1-4 | 10 | `(9,3)` | `(6,3) (7,4) (8,3) (9,3)` |
| 5 | `(6, 3)` | no | add 3 via 0-3 | **16** | - | `(7,4) (8,3) (9,3)` |

All 5 nodes are in the tree, so the loop stops. Answer **16** ✓.

The heap still holds `(7,4)`, `(8,3)`, `(9,3)`: edges to nodes that already got in more
cheaply. Without the early stop they'd pop and be skipped by the `in_tree` check. Step 5
is worth pausing on: node 3 was offered at 8 (step 2) and 9 (step 4), but the 6 from
node 0 had been waiting since step 1 and was still the cheapest way in.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def spanningTree(self, V: int, edges: List[List[int]]) -> int:
        """Total weight of a minimum spanning tree, by Prim's algorithm.

        Time:  O(E log E) = O(E log V), each edge pushed at most twice.
        Space: O(V + E), the adjacency list and the heap.
        """
        adj = [[] for _ in range(V)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        in_tree = [False] * V
        total, added = 0, 0
        pq = [(0, 0)]                               # (weight of edge into the tree, node)

        while pq and added < V:
            w, u = heapq.heappop(pq)
            if in_tree[u]:
                continue                            # got in earlier, more cheaply
            in_tree[u] = True
            total += w                              # the edge weight, not a distance
            added += 1
            for v, wv in adj[u]:
                if not in_tree[v]:
                    heapq.heappush(pq, (wv, v))

        return total
```
**Time:** O(E log V) · **Space:** O(V + E)

## ⚠️ Gotchas
- **Push `wv`, not `w + wv`.** That's Dijkstra, and it builds the shortest-path tree,
  which is generally **not** the MST. Triangle 0-1 (2), 0-2 (2), 1-2 (1): from 0,
  Dijkstra keeps both edges out of 0 (total 4); the MST is 1-2 plus one of them (3).
- **Check `in_tree` at pop.** A node can be pushed once per neighbour already in the
  tree. Only the first (cheapest) pop counts.
- **Start weight 0.** The first node joins for free; it's the V − 1 edges after it that
  cost.
- **Disconnected graph?** There is no spanning tree. `added < V` at the end detects it;
  GfG guarantees connectivity, but say it.
- **Parallel edges and self-loops** are harmless: a self-loop points into the tree and is
  skipped, a duplicate edge just loses to its cheaper twin.
- **Kruskal is the other standard answer:** sort edges, add each one whose endpoints are
  in different union-find sets. Same O(E log E). Prim reuses the heap loop you already
  know; Kruskal needs union-find.

## 🎤 Interview talking points
- *"Prim's: grow a tree from any node, and repeatedly add the cheapest edge from the tree
  to a node outside it. That's safe by the cut property."*
- *"It's Dijkstra's loop with the heap keyed on the single edge weight instead of the
  path distance."* ← the line that shows you understand both.
- *"Lazy version: push duplicates, skip nodes already in the tree at pop. O(E log V)."*
- *"Kruskal with union-find is the alternative; it's nicer when edges are already
  sorted or the graph is given as an edge list."*

## 🔗 Transfer
The heap has now done three jobs: Dijkstra's path length (EP164), the max-cost of
EP166/167, and today's edge weight. Same container, same stale-skip, different key.
Tomorrow (EP171) Word Ladder closes the pattern by going back to plain BFS, on a graph
you never actually build.

## 📹 Metadata
- **Title:** `Prim's MST, Dijkstra with one word changed | Graphs #19`
- **Thumbnail:** `w, not d + w` (green block)
- **Short:** the tree growing one cheapest cable at a time, node 3 finally joining via
  the 6 that waited since step 1. 45s.
