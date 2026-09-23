# EP168 · P14E17 · Bellman-Ford   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1

---

## 🎬 Hook
> "Dijkstra finalises a node the moment it's popped. Add **one negative edge** and that
> promise breaks: a node you called 'done' can get cheaper later. Bellman-Ford makes no
> promises at all. It just relaxes **every edge, V − 1 times**. Dumber, slower, and it
> handles negative weights, and even tells you when the answer doesn't exist."

## 📋 Problem, in your words
```
V nodes (0..V-1), DIRECTED edges [u, v, w] where w can be NEGATIVE,
and a source src. Return dist, the shortest distance from src to each node.

  - unreachable nodes get 10^8
  - if a negative-weight cycle is reachable, distances are meaningless:
    return [-1]
```

## 🔢 The example
```
V = 5, edges = [[1,3,2], [4,3,-1], [2,4,1], [1,2,1], [0,1,5]], src = 0

    0 --5--> 1 --1--> 2
             |        |
             2        1
             v        v
             3 <-(-1)- 4

Output: [0, 5, 6, 6, 7]
Why:    3 via 1 directly costs 5+2 = 7,
        but 0 -> 1 -> 2 -> 4 -> 3 costs 5+1+1-1 = 6. The negative edge wins.

V = 4, edges = [[0,1,4], [1,2,-6], [2,3,5], [3,1,-2]], src = 0
    1 -> 2 -> 3 -> 1 costs -6 + 5 - 2 = -3: loop it forever, distances fall forever.
Output: [-1]
```

## 🧸 ELI5
> You're planning the cheapest trip, but some roads **pay you** to use them (negative
> weights). You can't trust the first price you see, because a longer route with a
> paying road might end up cheaper.
>
> So you do something patient: go through the **whole list of roads**, and for each one
> ask "does this road give its destination a cheaper price than I have written down?"
> Update if yes. Then go through the whole list **again**. And again.
>
> ```
> pass 1: prices correct for trips of at most 1 road
> pass 2: at most 2 roads
> ...
> pass V-1: at most V-1 roads, which is every simple path there is
> ```
>
> If a **V-th** pass still finds a cheaper price, some loop is paying you every time you
> go round it. There's no cheapest trip; you'd drive in circles forever.

## 🐌 Brute force (say it, don't type it)
Enumerate every simple path from src to every node: exponential. Or run Dijkstra and
hope. A Dijkstra that marks nodes done when popped locks node 3 in at 7 (it pops before
node 4, which is also at 7) and never sees the 6. The lazy heap version happens to
recover here, but with negative edges it can re-pop nodes an exponential number of
times. Bellman-Ford's **O(V · E)** is the price of being correct, every time.

## 💡 The pattern reveal
**Signal:** **negative** edge weights, "detect a negative cycle", or a limit on the
number of edges (EP169).
**Therefore:** Shape E: Bellman-Ford, relaxation in rounds.

**Key insight:** a shortest path with no negative cycle is **simple**, so it has at most
V − 1 edges. If each round extends correct distances by one more edge, V − 1 rounds
cover every shortest path. Relaxing from a **snapshot** of the last round makes that
exact: after round `i`, `dist[v]` is the best path using **at most `i` edges**.

```python
for _ in range(V - 1):
    prev = dist[:]                          # last round's answers
    for u, v, w in edges:
        if prev[u] != INF and prev[u] + w < dist[v]:
            dist[v] = prev[u] + w
# one more pass: if anything still improves, there's a negative cycle
```

## 🔍 Dry run: the 5-node example, `src = 0`
Edges are processed in input order: `1→3 (2)`, `4→3 (-1)`, `2→4 (1)`, `1→2 (1)`,
`0→1 (5)`. `∞` = 10⁸.

| round | edges that improve (from the snapshot) | dist after | meaning |
|---|---|---|---|
| start | - | `[0, ∞, ∞, ∞, ∞]` | 0 edges |
| 1 | `0→1`: 0+5 = 5 | `[0, 5, ∞, ∞, ∞]` | best with ≤ 1 edge |
| 2 | `1→3`: 5+2 = 7; `1→2`: 5+1 = 6 | `[0, 5, 6, 7, ∞]` | ≤ 2 edges |
| 3 | `2→4`: 6+1 = 7 | `[0, 5, 6, 7, 7]` | ≤ 3 edges |
| 4 | **`4→3`: 7−1 = 6 < 7** | `[0, 5, 6, 6, 7]` | ≤ 4 edges |
| check | nothing improves | - | no negative cycle |

Answer **`[0, 5, 6, 6, 7]`** ✓. Round 4 is the one Dijkstra would have skipped: node 3
already had a price (7), and a 4-edge path through a negative edge beat it.

**Negative-cycle example**, V = 4: after 3 rounds `dist = [0, 4, -2, 3]`. The check pass
tries `3→1`: 3 − 2 = 1 < 4, still improving after V − 1 rounds → **`[-1]`** ✓.

## ✅ Optimal solution
```python
class Solution:
    def bellmanFord(self, V: int, edges: List[List[int]], src: int) -> List[int]:
        """Shortest distances from src with negative weights allowed.

        Time:  O(V * E), up to V-1 rounds over every edge, plus one check pass.
        Space: O(V), dist and the per-round snapshot.
        """
        INF = 10**8
        dist = [INF] * V
        dist[src] = 0

        for _ in range(V - 1):
            prev = dist[:]                              # relax FROM last round only
            changed = False
            for u, v, w in edges:
                if prev[u] != INF and prev[u] + w < dist[v]:
                    dist[v] = prev[u] + w
                    changed = True
            if not changed:
                break                                   # settled early

        for u, v, w in edges:                           # the V-th pass
            if dist[u] != INF and dist[u] + w < dist[v]:
                return [-1]                             # still improving: negative cycle
        return dist
```
**Time:** O(V · E) · **Space:** O(V)

## ⚠️ Gotchas
- **`dist[u] != INF` before relaxing.** With a negative `w`, `10⁸ + (-1) < 10⁸`, so an
  unreachable node would "improve" its neighbour and you'd report a fake distance of
  99,999,999.
- **V − 1 rounds, not V.** A simple path has at most V − 1 edges. The V-th pass is the
  cycle check, and it must be separate.
- **Snapshot or in place?** For plain Bellman-Ford both are correct; in place just
  converges in fewer rounds. For EP169's edge limit the snapshot is **mandatory**. Use
  it here so the habit is already there. Pattern card gotcha #3.
- **Early exit.** A round with no change means every later round is identical. Worth
  having; worst case is still O(V · E).
- **Directed edges.** An undirected negative edge is itself a negative cycle (u → v →
  u), so Bellman-Ford on undirected graphs with negative weights always returns `[-1]`.
- **Only reachable cycles count.** A negative cycle nobody can reach from src doesn't
  affect any distance, and the `!= INF` guard makes the check ignore it.

## 🎤 Interview talking points
- *"Negative weights break Dijkstra's greedy finalisation, so Bellman-Ford: relax every
  edge V − 1 times, since a shortest simple path has at most V − 1 edges."*
- *"After round i, dist holds the best path using at most i edges; the snapshot makes
  that exact."* ← sets up the K-stops question.
- *"One extra pass detects negative cycles: if anything still improves, there's no
  shortest path."*
- *"O(V · E). Dijkstra is O(E log V), so I only reach for this when I need negatives or
  an edge-count limit."*

## 🔗 Transfer
The first shortest-path algorithm here that doesn't use a queue or a heap at all. Its
superpower isn't really the negative weights, it's the **round structure**: round `i`
means "at most `i` edges". Tomorrow (EP169) Cheapest Flights Within K Stops is a
Dijkstra-looking problem that Dijkstra gets wrong, and it's solved by running this code
for exactly K + 1 rounds.

## 📹 Metadata
- **Title:** `Bellman-Ford, when Dijkstra's promise breaks | Graphs #17`
- **Thumbnail:** `relax × (V − 1)` (red block)
- **Short:** node 3 dropping from 7 to 6 in round 4 via the negative edge. 40s.
