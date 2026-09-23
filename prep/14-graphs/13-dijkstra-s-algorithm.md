# EP164 · P14E13 · Dijkstra's Algorithm   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1

---

## 🎬 Hook
> "Yesterday, the first time BFS reached a node was the shortest way. Give the edges
> weights and that breaks: one long edge arrives first, three short edges arrive later
> and cheaper. Dijkstra's fix is to stop asking 'who did I find first?' and ask **'who is
> cheapest to reach right now?'** That question is a heap. The rest is yesterday's code."

## 📋 Problem, in your words
```
Given V nodes (0..V-1), undirected weighted edges [u, v, w] with w >= 0,
and a source src, return dist where dist[i] is the minimum total weight
of any path from src to i.

  - weights are NON-NEGATIVE (this is what makes Dijkstra correct)
  - the graph is connected, so every node is reachable
```

## 🔢 The example
```
V = 3, edges = [[0,1,1], [1,2,3], [0,2,6]], src = 2

        0
     1 / \ 6
      /   \
     1 --- 2
        3

Output: [4, 3, 0]
Why:    2 -> 0 directly costs 6, but 2 -> 1 -> 0 costs 3 + 1 = 4.
        BFS would reach 0 first by the direct edge and wrongly keep 6.

V = 2, edges = [[0,1,9]], src = 0   ->   [0, 9]
```

## 🧸 ELI5
> You're a delivery company sending out vans from the depot, and you want the fastest
> time to every house. Rule: **always follow up on the house you can reach soonest**.
>
> When you finalise the soonest house, you can be sure nobody will find a faster way
> there later, because every other route is *already* slower at this point and roads
> never take negative time. From that house, you note down new, maybe-faster times for
> its neighbours.
>
> ```
> depot 2:  house 1 is 3 min away, house 0 is 6 min away
> soonest is house 1 (3 min). from 1, house 0 is 3 + 1 = 4 min. better than 6! update.
> soonest is house 0 (4 min). finalise.
> there's an old note saying "house 0, 6 min". it's stale. throw it away.
> ```
>
> The "old note" is the stale heap entry, and throwing it away is the one line people
> forget.

## 🐌 Brute force (say it, don't type it)
Bellman-Ford (EP168): relax every edge V−1 times, **O(V · E)**. Or the textbook
array-scan Dijkstra: each round, scan all V nodes for the unvisited one with the smallest
distance, **O(V²)**, which is actually fine for dense graphs. The heap turns "find the
smallest" into O(log V), giving **O((V + E) log V)** on sparse graphs.

## 💡 The pattern reveal
**Signal:** "shortest / cheapest / fastest" with **weighted** edges, all **non-negative**.
**Therefore:** Shape E: Dijkstra with a min-heap.

**Key insight:** the node with the smallest tentative distance can't be improved,
because any other route to it goes through a node that's already at least as far, and
weights can't be negative. So pop the smallest, finalise it, relax its edges.

| | BFS (EP163) | Dijkstra (today) |
|---|---|---|
| frontier | `deque` | min-heap of `(dist, node)` |
| a node's distance is final when | it's **pushed** | it's **popped** |
| updating a distance | never | if `d + w < dist[v]`, push a new entry |
| duplicates in the frontier | never | yes, so skip **stale** entries |

```python
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:                   # stale: u was already finalised cheaper
        continue
    for v, w in adj[u]:
        if d + w < dist[v]:           # relax
            dist[v] = d + w
            heapq.heappush(pq, (dist[v], v))
```

Python's `heapq` has no decrease-key, so we push a new entry and leave the old one to be
skipped. That's why the stale check exists.

## 🔍 Dry run: `edges = [[0,1,1], [1,2,3], [0,2,6]]`, `src = 2`
`adj = {0: [(1,1), (2,6)], 1: [(0,1), (2,3)], 2: [(1,3), (0,6)]}`, `dist = [∞, ∞, 0]`.

| step | pop `(d, u)` | stale? | relaxations | dist after | heap after |
|---|---|---|---|---|---|
| 0 | - | - | - | `[∞, ∞, 0]` | `[(0,2)]` |
| 1 | `(0, 2)` | no | 1: 0+3=3 < ∞ ✓; 0: 0+6=6 < ∞ ✓ | `[6, 3, 0]` | `[(3,1), (6,0)]` |
| 2 | `(3, 1)` | no | 0: 3+1=**4 < 6** ✓; 2: 3+3=6, no | `[4, 3, 0]` | `[(4,0), (6,0)]` |
| 3 | `(4, 0)` | no | 1: 4+1=5, no; 2: 4+6=10, no | `[4, 3, 0]` | `[(6,0)]` |
| 4 | `(6, 0)` | **yes**, 6 > dist[0]=4 | skipped | `[4, 3, 0]` | `[]` |

Answer **`[4, 3, 0]`** ✓.

Step 2 is Dijkstra's reason to exist: node 0 had a distance (6) and it got *better*.
Step 4 is the stale entry from step 1, still in the heap, correctly ignored.

## ✅ Optimal solution
```python
import heapq

class Solution:
    def dijkstra(self, V: int, edges: List[List[int]], src: int) -> List[int]:
        """Shortest distances from src with non-negative edge weights.

        Time:  O((V + E) log V), each edge can push one heap entry; each pop is log.
        Space: O(V + E), the adjacency list and up to E heap entries.
        """
        adj = [[] for _ in range(V)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))                   # undirected

        dist = [float('inf')] * V
        dist[src] = 0
        pq = [(0, src)]                             # (distance so far, node)

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue                            # stale: a cheaper entry already won
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))

        return dist
```
**Time:** O((V + E) log V) · **Space:** O(V + E)

## ⚠️ Gotchas
- **The stale check.** Without `if d > dist[u]: continue`, the answer is still right,
  but every stale entry re-relaxes all its edges. On dense graphs that's the difference
  between O(E log V) and much worse.
- **`(dist, node)` order in the tuple.** The heap sorts by the first element. Push
  `(node, dist)` and you get "smallest node id first", which is not Dijkstra.
- **Non-negative weights only.** One negative edge can make a popped node improvable
  later, and Dijkstra never revisits. Negative weights → Bellman-Ford (EP168).
- **Unreachable nodes stay `inf`.** GfG's graph is connected, but LeetCode variants want
  `-1`; convert at the end.
- **Directed or undirected?** GfG's edges here are undirected (two appends). Network
  Delay tomorrow is directed (one).
- **Finalised at pop, not at push.** The opposite of BFS. A node can be pushed several
  times; it's settled the first time it comes off the heap.

## 🎤 Interview talking points
- *"Dijkstra is BFS with a min-heap keyed on distance. The smallest tentative distance
  can't improve, since all weights are non-negative, so I finalise it when I pop it."*
- *"heapq has no decrease-key, so I push duplicates and skip stale ones with
  `d > dist[u]`."* ← the line that shows you've implemented it, not memorised it.
- *"O((V + E) log V). For a dense graph the O(V²) array version is just as good."*
- *"Negative weights break it; that's Bellman-Ford's job."*

## 🔗 Transfer
EP163's BFS, with the `deque` swapped for a heap and one `continue` added. The next three
episodes are this exact code wearing different clothes: EP165 Network Delay reads
`max(dist)`, EP166 Min Effort changes `d + w` to `max(d, w)`, and EP167 Swim in Rising
Water does the same on a grid. EP170 Prim's MST changes the heap key once more.

## 📹 Metadata
- **Title:** `Dijkstra's Algorithm, BFS with a heap (and the line everyone forgets) | Graphs #13`
- **Thumbnail:** `if d > dist[u]: continue` (red block)
- **Short:** node 0 improving from 6 to 4, then the stale `(6, 0)` popping and being
  skipped. 45s.
