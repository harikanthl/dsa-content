# Pattern 14: Graphs

**20 episodes · EP 152–171**

---

## The one-sentence version

Every graph problem is the same loop, **visit nodes along edges without revisiting**,
and the only thing that changes is *what you keep the frontier in*: a **stack** gives you
DFS, a **queue** gives you BFS and shortest paths in steps, a **priority queue** gives you
Dijkstra and shortest paths in weight. Pick the container and the algorithm writes itself.

## ELI5

You're exploring a cave system with a torch and a piece of chalk. Every chamber you enter,
you chalk an X on the wall so you never waste time going back in. That X is the `visited`
set, and it's the one thing every episode here has in common.

What differs is *how you decide which unexplored tunnel to take next*:

| you carry a… | you always take… | you get | this is |
|---|---|---|---|
| **stack** (a to-do list you add to the top of) | the tunnel you found *most recently* | you go deep before you go wide | **DFS** |
| **queue** (a line you add to the back of) | the tunnel you found *earliest* | you explore in rings of equal distance | **BFS** |
| **priority queue** (a line sorted by cheapness) | the tunnel that is *cheapest to reach so far* | you reach every chamber by its cheapest route | **Dijkstra** |

Grids are graphs (every cell is a node, its four neighbours are its edges). Course
prerequisites are graphs. Words that differ by one letter are graphs. The word "graph"
is almost never in the problem statement; the *shape* is.

## How to recognise it

| Signal | Example |
|---|---|
| a **grid** and "connected" / "region" / "island" | Number of Islands (EP155), Surrounded Regions (EP162) |
| "connected components", "groups", "provinces" | Number of Provinces (EP156) |
| **"minimum steps / minutes / moves"** on unweighted moves | Rotten Oranges (EP157), Shortest Path (EP163), Word Ladder (EP171) |
| "prerequisites", "dependencies", "order to take courses" | Topological Sort (EP160), cycle in directed graph (EP159) |
| "can it be split into two groups such that…" | Bipartite (EP161) |
| edges have **weights** and you want the cheapest route | Dijkstra (EP164), Network Delay (EP165) |
| the path cost is the **maximum** edge, not the sum | Min Effort (EP166), Swim in Rising Water (EP167) |
| **negative** weights, or "at most k stops / edges" | Bellman-Ford (EP168), Cheapest Flights (EP169) |
| "connect all of them at minimum total cost" | Prim's MST (EP170) |
| nodes aren't listed, you have to *generate* neighbours | Word Ladder (EP171): neighbours are one-letter edits |

**Two questions pick the algorithm.** Do I need distances at all? No → DFS (components,
cycles, flood fill, topo order). Yes → unweighted is BFS, non-negative weights is
Dijkstra, negative weights or an edge-count bound is Bellman-Ford.

**The anti-signal:** a tree is a graph with no cycles and one parent per node, so if the
input is a `TreeNode` you don't need `visited`, that's Pattern 13.

## Shape A: Representation

Before any algorithm: turn the input into "give me the neighbours of `u`".

```python
from collections import defaultdict

# edges -> adjacency dict (EP152)
adj = defaultdict(list)
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)          # drop this line for a directed graph

# grid -> neighbours computed on the fly, never stored
def neighbours(r, c):
    for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

visited = set()               # or a 2-D bool grid, or overwrite the cell in place
```

Say three things out loud first: **directed?** **weighted?** (then store `(v, w)` pairs)
and is the node set **explicit** (an edge list) or **implicit** (grid cells, words)?

## Shape B: DFS: components and flood fill

```python
def dfs(u):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v)

components = 0
for u in nodes:
    if u not in visited:
        components += 1        # every fresh start is a new component
        dfs(u)
```

The outer `for` is the part people forget. One DFS explores **one** component; counting
islands (EP155) or provinces (EP156) is counting how many times you had to start over.

The iterative form is the BFS code below with `stack.pop()` instead of `popleft()`,
use it past ~10⁴ nodes, where Python's recursion limit bites.

**Flood fill from the border (EP162):** don't test each region for an escape route,
flood from every `O` on the grid's edge and mark what you reach as safe. Everything
unmarked is surrounded. Starting at the boundary turns a hard question into plain DFS.

## Shape C: BFS: levels and shortest paths in steps

```python
from collections import deque

dist = {start: 0}
q = deque([start])
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:          # visited check at PUSH time
            dist[v] = dist[u] + 1
            q.append(v)
```

BFS visits in rings of equal distance, so the first arrival at a node **is** its shortest
path (EP163). No relaxation, no comparison.

**Level loop**: when you need "how many rounds", process a whole ring per iteration:

```python
q = deque(all_rotten)          # multi-source: seed the queue with EVERY source (EP157)
minutes = 0
while q:
    for _ in range(len(q)):    # exactly one ring
        r, c = q.popleft()
        for nr, nc in neighbours(r, c):
            if grid[nr][nc] == FRESH:
                grid[nr][nc] = ROTTEN
                q.append((nr, nc))
    if q: minutes += 1
```

Multi-source BFS is BFS with several things in the queue at the start. Rotten Oranges is
not "BFS from each rotten one" (O(n²)), seed them all and run once.

**Implicit graph (EP171):** in Word Ladder nodes are words and an edge is "differs by one
letter". Don't compare every pair. Bucket words by wildcard pattern, `hot` → `*ot`,
`h*t`, `ho*`, and a word's neighbours are everything sharing one of its patterns. The
buckets *are* the adjacency list; the graph is never built.

## Shape D: Cycles, ordering, colouring

**Undirected cycle (EP158):** a visited neighbour means a cycle, *unless it's the node
you just came from*. Pass the parent.

```python
def has_cycle(u, parent):
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            if has_cycle(v, u): return True
        elif v != parent:          # visited AND not where we came from
            return True
    return False
```

**Directed cycle (EP159):** the parent trick is not enough, `A→B, A→C, B→C` reaches C
twice with no cycle. Three colours: WHITE unvisited, **GRAY on the current path**, BLACK
finished. Set `GRAY` on entry, `BLACK` on exit; meeting a GRAY neighbour is a cycle,
meeting a BLACK one is just a shared descendant.

**Topological sort, Kahn's (EP160):** BFS whose queue holds nodes with no remaining
prerequisites.

```python
q = deque(u for u in nodes if indeg[u] == 0)
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
return order if len(order) == len(nodes) else []   # short -> a cycle ate the rest
```

Cycle detection comes free: a short order means something never reached in-degree 0.

**Bipartite (EP161)** is 2-colouring by BFS: every neighbour gets the opposite colour,
and a neighbour that already has *your* colour is the failure. Start from every
uncoloured node, the graph may be disconnected.

## Shape E: Weighted shortest paths

**Dijkstra (EP164):** BFS with a heap keyed on distance, plus one guard.

```python
import heapq
dist = {start: 0}
pq = [(0, start)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist.get(u, float('inf')):   # stale entry: a shorter path already popped
        continue
    for v, w in adj[u]:
        nd = d + w
        if nd < dist.get(v, float('inf')):
            dist[v] = nd
            heapq.heappush(pq, (nd, v))
```

We push duplicates instead of decrease-key, so a node can sit in the heap several times;
the `continue` on a stale entry is what keeps the running time honest.

- **Network Delay (EP165):** run Dijkstra, answer is `max(dist.values())`, or `-1` if
  some node was never reached.
- **Min Effort (EP166), Swim in Rising Water (EP167):** a path costs its **worst edge**,
  not the sum. One line changes: `nd = max(d, w)` instead of `d + w`. Say that out loud,
  it's the whole insight.

**Bellman-Ford (EP168):** relax every edge, V−1 times. Slower, but it survives negative
weights, and every round `i` gives you the best path using **at most `i` edges**.

```python
for _ in range(n - 1):
    prev = dist[:]                       # relax FROM last round's snapshot
    for u, v, w in edges:
        dist[v] = min(dist[v], prev[u] + w)
```

**Cheapest Flights Within K Stops (EP169):** K stops = K+1 edges, so run **K+1** rounds
instead of V−1. The snapshot is mandatory here: relaxing in place lets one round chain
several edges and blows the limit.

## Shape F: Minimum spanning tree

**Prim's (EP170)** is Dijkstra with one word changed: the heap is keyed on the
**edge weight** to reach a node, not the total path length.

```python
pq = [(0, start)]; seen = set(); total = 0
while pq and len(seen) < n:
    w, u = heapq.heappop(pq)
    if u in seen: continue
    seen.add(u); total += w
    for v, wv in adj[u]:
        if v not in seen: heapq.heappush(pq, (wv, v))
```

Dijkstra: cheapest way *from the source*. Prim: cheapest way *into the tree so far*.
Same loop, different key.

## The three things that go wrong

### 1. Marking visited at pop instead of at push (BFS)

Mark at *dequeue* and several neighbours can enqueue the same node first. On a grid the
queue holds each cell up to four times and the level count (EP157) goes wrong. Mark it
the moment you enqueue it. Dijkstra is the exception, there you decide at pop, which is
what the stale-entry check is for.

### 2. Forgetting the parent in undirected cycle detection

Every undirected edge is two directed edges, so where you came from is always "already
visited". Without `v != parent`, a graph with one edge reports a cycle. And the trick is
undirected-only, directed needs GRAY/BLACK.

### 3. Bellman-Ford relaxing in place

Reading `dist[u]` that was updated *this* round lets one pass propagate across many
edges. Harmless for plain Bellman-Ford (it converges faster); a wrong answer for EP169,
where a path of more than K+1 edges gets counted. Copy `dist` at the top of every round.

## Complexity

| Problem | Time | Space |
|---|---|---|
| DFS / BFS on an adjacency list | O(V + E) | O(V), visited + stack/queue |
| DFS / BFS on a grid | O(R·C), V = R·C, E ≤ 4V | O(R·C) |
| Kahn's topological sort, bipartite | O(V + E) | O(V) |
| Dijkstra, Prim's (binary heap) | O((V + E) log V) | O(V + E) |
| Bellman-Ford | O(V · E) | O(V) |
| Cheapest Flights, K stops | O(K · E) | O(V) |
| Word Ladder with pattern buckets | O(N · L²), L = word length | O(N · L) |
| recursive DFS you should be nervous about | - | O(V) call stack; go iterative past ~10⁴ |

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 152 | Adjacency List from Edges | representation | Edges → `defaultdict(list)`; directed vs undirected is one line. |
| 153 | Graph DFS | DFS | Recursive and iterative; `visited` is non-negotiable. |
| 154 | Graph BFS | BFS | Queue instead of stack; mark visited at push. |
| 155 | Number of Islands | DFS, grid | Count the *starts*. Cells are nodes, 4 neighbours are edges. |
| 156 | Number of Provinces | DFS | Same count, adjacency matrix instead of a grid. |
| 157 | Rotten Oranges | multi-source BFS | Seed every source; level loop counts minutes. |
| 158 | Cycle in Undirected Graph | DFS | A visited neighbour is a cycle unless it's your parent. |
| 159 | Cycle in Directed Graph | DFS, 3 colours | GRAY means "on the current path". Parent is not enough. |
| 160 | Topological Sort | Kahn's | Peel in-degree-0 nodes; a short order means a cycle. |
| 161 | Bipartite / Graph Coloring | BFS | 2-colour; a same-colour neighbour is the failure. |
| 162 | Surrounded Regions | DFS, grid | Flood from the **border**; unreached is surrounded. |
| 163 | Shortest Path, Unweighted | BFS | First arrival is the shortest. No relaxation needed. |
| 164 | Dijkstra's Algorithm | heap | BFS with a heap; the stale-entry `continue`. |
| 165 | Network Delay Time | Dijkstra | Answer is `max(dist)`; `-1` if anything unreached. |
| 166 | Path With Minimum Effort | Dijkstra, max-cost | `nd = max(d, w)`, the only line that changes. |
| 167 | Swim in Rising Water | Dijkstra, max-cost | Same as EP166 with the cell value as the edge weight. |
| 168 | Bellman-Ford | relaxation | V−1 rounds from a snapshot; negative weights are fine. |
| 169 | Cheapest Flights Within K Stops | Bellman-Ford | K stops = K+1 rounds, and the snapshot is mandatory. |
| 170 | Prim's MST | heap | Dijkstra keyed on edge weight instead of path length. |
| 171 | Word Ladder | BFS, implicit graph | Neighbours via `*ot` patterns; never build the edge list. |

## What "knowing this in your sleep" means

1. Stack, queue, or priority queue, and why? *(Stack: I only need reachability or
   structure. Queue: I need fewest steps. Priority queue: edges have weights.)*
2. Where exactly do I mark `visited`? *(At push for BFS and iterative DFS; at pop for
   Dijkstra, with the stale-entry check.)*
3. How do I detect a cycle, and does the answer change if the graph is directed?
   *(Undirected: parent check. Directed: GRAY/BLACK, or Kahn's order coming up short.)*
4. What's the one line that turns Dijkstra into Min Effort, and into Prim's?
   *(`max(d, w)` for the path cost; `w` alone for the heap key.)*
5. Why does Bellman-Ford copy `dist` each round, and how many rounds for K stops?
   *(So one round uses at most one more edge. K stops → K+1 rounds.)*
6. Where's the graph in Word Ladder? *(It's implicit. Words are nodes, one-letter
   patterns are the buckets that give you neighbours in O(L).)*
