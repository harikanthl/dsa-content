# EP158 · P14E07 · Cycle Detection in an Undirected Graph   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/detect-cycle-in-an-undirected-graph/1

---

## 🎬 Hook
> "Is there a cycle? Easy: run DFS, and if you ever meet a node you've already visited,
> that's a loop. Try it on a graph with **one edge** and it says yes. Every undirected
> edge points both ways, so the node you just came from always looks visited. The fix
> is one extra variable: **where did I come from?**"

## 📋 Problem, in your words
```
Given V nodes (0..V-1) and a list of undirected edges, return True if the
graph contains a cycle, False otherwise.

  - the graph may be disconnected: a cycle in ANY component counts
  - a cycle needs at least 3 distinct nodes (or a self-loop)
```

## 🔢 The example
```
V = 4, edges = [[0,1], [0,2], [1,2], [2,3]]

      0
     / \
    1---2---3

Output: True      <- 0 - 1 - 2 - 0

V = 4, edges = [[0,1], [1,2], [2,3]]

    0---1---2---3

Output: False     <- a straight line, every node reached exactly one way

V = 5, edges = [[0,1], [2,3], [3,4], [4,2]]   ->  True   (cycle hides in the 2nd component)
```

## 🧸 ELI5
> You're exploring a maze with chalk, and you mark every room you enter. Every corridor
> in this maze is **two-way**. So when you're in room 1 and look around, you'll always
> see the chalk mark in room 0, the room you just walked in from. That's not a loop.
> That's the door behind you.
>
> A loop is when you see chalk through a door that **isn't the one you came in by**.
> Someone (you, earlier) reached that room by a different route, so there are two ways
> to get there, and two ways to get somewhere is a circle.
>
> ```
> 0 -> 1: in room 1, see chalk in 0.  came from 0?  yes -> just the door behind me
> 0 -> 2: in room 2, see chalk in 0.  came from 0?  yes -> door behind me
>         in room 2, see chalk in 1.  came from 0, not 1 -> LOOP (0-1-2-0)
> ```

## 🐌 Brute force (say it, don't type it)
For every edge, remove it and check whether its two endpoints are still connected (a
BFS). If they are, that edge closes a cycle. **O(E · (V + E))**. It's wasteful because
each BFS re-explores the same graph; one traversal already knows, at every step, whether
a node was reached before by another route.

A cheaper shortcut, for a single connected graph only: it's acyclic iff `E == V - 1`.
Say it, because it's elegant, but it breaks on disconnected input and multi-edges, so
don't submit it.

## 💡 The pattern reveal
**Signal:** "cycle" in an **undirected** graph.
**Therefore:** Shape D: DFS that passes the **parent**.

**Key insight:** a visited neighbour is a cycle **unless it's your parent**. The edge
back to your parent is the same edge you just crossed, seen from the other side.

```python
def has_cycle(u, parent):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            if has_cycle(v, u):
                return True
        elif v != parent:          # visited AND not the door behind me
            return True
    return False
```

The submitted solution does exactly this with an explicit stack of `(node, parent)`
pairs, because GfG allows V up to 10⁵ and recursion that deep crashes Python.

## 🔍 Dry run: `V = 4`, `edges = [[0,1], [0,2], [1,2], [2,3]]`
`adj = [[1, 2], [0, 2], [0, 1, 3], [2]]`. Stack holds `(node, parent)`; nodes are
marked when pushed.

| step | pop `(u, parent)` | neighbour `v` | visited? | `v == parent`? | action | stack after |
|---|---|---|---|---|---|---|
| 0 | - | - | - | - | mark 0, push `(0, -1)` | `[(0,-1)]` |
| 1 | `(0, -1)` | 1 | no | - | mark 1, push `(1, 0)` | `[(1,0)]` |
| 2 | `(0, -1)` | 2 | no | - | mark 2, push `(2, 0)` | `[(1,0), (2,0)]` |
| 3 | `(2, 0)` | 0 | yes | **yes** | the door behind me, skip | `[(1,0)]` |
| 4 | `(2, 0)` | 1 | yes | **no** (parent is 0) | **cycle, return True** | - |

Answer **True** ✓. Step 3 is the false alarm the parent check exists for; step 4 is
the real thing: node 1 was reached from 0, and now from 2 as well.

On the straight line `0-1-2-3`, every visited neighbour a node sees is its own parent,
so the loop drains and returns **False**.

## ✅ Optimal solution
```python
class Solution:
    def isCycle(self, V: int, edges: List[List[int]]) -> bool:
        """True if the undirected graph has a cycle in any component.

        Time:  O(V + E), each node is pushed once, each adjacency entry read once.
        Space: O(V + E), the adjacency list, plus O(V) for visited and the stack.
        """
        adj = [[] for _ in range(V)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        visited = [False] * V
        for start in range(V):                      # the graph may be disconnected
            if visited[start]:
                continue
            visited[start] = True
            stack = [(start, -1)]                   # (node, the node we came from)
            while stack:
                u, parent = stack.pop()
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append((v, u))
                    elif v != parent:               # seen before, by another route
                        return True
        return False
```
**Time:** O(V + E) · **Space:** O(V + E)

## ⚠️ Gotchas
- **No parent check → every edge is a cycle.** `V = 2, edges = [[0,1]]` returns True
  without it. The pattern card's gotcha #2.
- **Loop over every start node.** A cycle in the second component is invisible to a DFS
  from node 0. The `V = 5` example catches this.
- **Parent is a node, not "any visited node".** You compare `v != parent`, the one
  specific node you arrived from.
- **Self-loop `[u, u]` is a cycle**, and this code says so: `u` is visited and is not
  its own parent.
- **Parallel edges** (`[0,1]` twice) form a 2-node cycle in a multigraph. The parent
  check by node id misses it; if the input can contain duplicates, track the parent
  **edge index** instead. GfG's inputs don't, but say you know.
- **Undirected only.** On a directed graph the parent trick gives wrong answers both
  ways. That's tomorrow.

## 🎤 Interview talking points
- *"DFS, and a visited neighbour means a cycle, except the parent: in an undirected
  graph the edge I came in on shows up again from the other side."*
- *"I loop over every node as a start, because the graph can be disconnected."*
- *"Iterative with a (node, parent) stack so deep graphs don't hit the recursion
  limit."*
- *"Union-Find also works: process edges, and if both ends already share a root, that
  edge closes a cycle."*
- *"For a connected graph there's a one-liner, E equals V minus 1 means no cycle, but it
  doesn't survive disconnected input."*

## 🔗 Transfer
Tomorrow (EP159) asks the same question on a **directed** graph, and the parent trick
breaks: you can reach a node twice without any cycle. The fix is to remember which
nodes are *on the current path*, not just which were ever visited. EP160 then shows a
third way to find a cycle for free, as a side effect of topological sorting.

## 📹 Metadata
- **Title:** `Cycle in an Undirected Graph, the door behind you isn't a loop | Graphs #7`
- **Thumbnail:** `v != parent` (red block)
- **Short:** one edge reported as a cycle, then the parent check fixing it. 35s.
