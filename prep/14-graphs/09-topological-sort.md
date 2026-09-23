# EP160 · P14E09 · Topological Sort   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/topological-sort/1

---

## 🎬 Hook
> "You're putting on clothes. Socks before shoes, underwear before trousers, trousers
> before belt. What order works? Topological sort answers that, and **Kahn's algorithm**
> does it in the most human way possible: start with anything that has no
> prerequisites, cross it off, and see what that unlocks. As a bonus, if it gets stuck,
> you've found a cycle."

## 📋 Problem, in your words
```
Given a DIRECTED ACYCLIC graph with V nodes (0..V-1) and edges [u, v]
meaning "u must come before v", return any ordering of all V nodes such
that for every edge, u appears before v.

  - many valid orders usually exist; any one is accepted
```

## 🔢 The example
```
V = 6, edges = [[5,2], [5,0], [4,0], [4,1], [2,3], [3,1]]

    5 ----> 2 ----> 3
    |               |
    v               v
    0 <---- 4 ----> 1

Output (one valid answer): [4, 5, 2, 0, 3, 1]
Check:  5 before 2 ✓  5 before 0 ✓  4 before 0 ✓  4 before 1 ✓  2 before 3 ✓  3 before 1 ✓

Also valid: [5, 4, 2, 3, 1, 0], [4, 5, 0, 2, 3, 1], ...
Not valid:  [5, 2, 3, 1, 4, 0]    <- 1 appears before 4, but 4 -> 1 is an edge

GfG's own examples (the judge prints "true" if your order is valid):
V = 4, edges = [[3,0], [1,0], [2,0]]                    ->  [1, 2, 3, 0]  (0 must be last)
V = 6, edges = [[1,3], [2,3], [4,1], [4,0], [5,0], [5,2]]  ->  [4, 5, 1, 0, 2, 3]
```

## 🧸 ELI5
> A university course list. Some courses have prerequisites. You can sign up for any
> course whose prerequisites you've **all** finished.
>
> Write next to each course how many prerequisites it still needs. The courses at 0 are
> available right now. Take one, and every course that listed it as a prerequisite
> drops by 1. Anything that hits 0 becomes available.
>
> ```
> needs:  0:2  1:2  2:1  3:1  4:0  5:0     available: 4, 5
> take 4  ->  0:1  1:1                     available: 5
> take 5  ->  2:0  0:0                     available: 2, 0
> take 2  ->  3:0                          available: 0, 3
> take 0  ->  (unlocks nothing)            available: 3
> take 3  ->  1:0                          available: 1
> take 1                                   done: 4 5 2 0 3 1
> ```
>
> If you ever run out of available courses with some still not taken, those courses
> are waiting on each other in a circle. No order exists.

## 🐌 Brute force (say it, don't type it)
Try permutations of the V nodes until one satisfies every edge: **O(V! · E)**. Slightly
less silly: repeatedly scan all nodes for one with no remaining incoming edges, output
it, delete its edges, repeat. That's **O(V · (V + E))** because every round rescans
everything. Kahn's algorithm is that same idea with a queue, so you never rescan.

## 💡 The pattern reveal
**Signal:** "prerequisites", "dependencies", "build order", "must come before".
**Therefore:** Shape D: **Kahn's algorithm**, BFS over in-degree-0 nodes.

**Key insight:** a node with in-degree 0 has nothing that must come before it, so it's
safe to output now. Outputting it removes its outgoing edges, which can drop other
nodes to in-degree 0. The queue holds exactly the "ready right now" set.

```python
q = deque(u for u in range(V) if indeg[u] == 0)
while q:
    u = q.popleft(); order.append(u)
    for v in adj[u]:
        indeg[v] -= 1                 # u is done: one fewer thing v waits on
        if indeg[v] == 0: q.append(v)
# len(order) < V  ->  a cycle kept some nodes from ever reaching 0
```

## 🔍 Dry run: the 6-node example
`adj = {5: [2, 0], 4: [0, 1], 2: [3], 3: [1]}`, in-degrees `[2, 2, 1, 1, 0, 0]`.

| step | pop | in-degree changes | newly ready (pushed) | queue after | order |
|---|---|---|---|---|---|
| 0 | - | - | 4, 5 | `[4, 5]` | `[]` |
| 1 | 4 | 0: 2→1, 1: 2→1 | - | `[5]` | `[4]` |
| 2 | 5 | 2: 1→**0**, 0: 1→**0** | 2, 0 | `[2, 0]` | `[4, 5]` |
| 3 | 2 | 3: 1→**0** | 3 | `[0, 3]` | `[4, 5, 2]` |
| 4 | 0 | - (no outgoing edges) | - | `[3]` | `[4, 5, 2, 0]` |
| 5 | 3 | 1: 1→**0** | 1 | `[1]` | `[4, 5, 2, 0, 3]` |
| 6 | 1 | - | - | `[]` | `[4, 5, 2, 0, 3, 1]` |

`len(order) == 6 == V`, so the graph was acyclic and **`[4, 5, 2, 0, 3, 1]`** is valid ✓.

Node 1 had two prerequisites (4 and 3). Step 1 dropped it to 1, but it only became
ready at step 5 when the second one finished. The count is what makes it wait.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def topoSort(self, V: int, edges: List[List[int]]) -> List[int]:
        """A topological order of a DAG, by Kahn's algorithm.

        Time:  O(V + E), each node is queued once, each edge decrements once.
        Space: O(V + E), the adjacency list, in-degrees and the queue.
        """
        adj = [[] for _ in range(V)]
        indeg = [0] * V
        for u, v in edges:
            adj[u].append(v)                        # u must come before v
            indeg[v] += 1

        q = deque(u for u in range(V) if indeg[u] == 0)   # nothing blocks these
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1                       # one prerequisite of v is done
                if indeg[v] == 0:
                    q.append(v)

        return order if len(order) == V else []     # short: a cycle blocked the rest
```
**Time:** O(V + E) · **Space:** O(V + E)

## ⚠️ Gotchas
- **Edge direction.** `[u, v]` means u before v, so it's `adj[u].append(v)` and
  `indeg[v] += 1`. Flip it and you get a valid order of the *reversed* graph, which is
  the exact opposite of what was asked.
- **Seed with every in-degree-0 node,** not just node 0. Disconnected pieces each have
  their own sources.
- **A short order means a cycle.** GfG promises a DAG, but LeetCode's Course Schedule
  (207, 210) doesn't. `len(order) < V` is the free cycle check.
- **Any valid order is accepted,** so don't panic when yours differs from the sample.
  Check it against the edges instead.
- **Decrement then test, in that order.** Testing `indeg[v] == 1` before decrementing
  works too, but it's the kind of off-by-one that reads wrong on camera.
- **DFS version:** push each node onto a list when it **finishes** (BLACK, from EP159),
  then reverse the list. Valid too, but it needs the three-colour machinery to detect
  cycles; Kahn's gets it for free.

## 🎤 Interview talking points
- *"Kahn's algorithm: in-degree counts, a queue of nodes with no remaining
  prerequisites, and each pop decrements its neighbours."*
- *"If the output has fewer than V nodes, the rest are stuck behind a cycle, so the same
  code answers 'is this schedulable?'"* ← Course Schedule I in one line.
- *"O(V + E): every node enters the queue once, every edge is decremented once."*
- *"The DFS alternative is reverse post-order, and it's what yesterday's BLACK colour
  was secretly computing."*

## 🔗 Transfer
EP159 found cycles with colours; today found them by counting, and produced an order as
well. The in-degree trick shows up again whenever something "unlocks" when all its
inputs are done: build systems, spreadsheet recalculation, course planning. Tomorrow
(EP161) goes back to undirected graphs and asks a colouring question instead of an
ordering one.

## 📹 Metadata
- **Title:** `Topological Sort, take what's ready, unlock what's next | Graphs #9`
- **Thumbnail:** `indeg == 0` (purple block)
- **Short:** node 1 counting down from 2 to 1 to 0 and only then joining the queue. 40s.
