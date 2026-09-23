# EP154 · P14E03 · Graph BFS   [Easy]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/bfs-traversal-of-graph/1

---

## 🎬 Hook
> "Take yesterday's DFS, swap the stack for a queue, and something much bigger than the
> order changes: BFS visits nodes in **rings of distance from the start**. That one
> property is the reason BFS, and not DFS, answers every 'minimum number of steps'
> question in this pattern. And there's one line that most people put in the wrong
> place."

## 📋 Problem, in your words
```
Given a connected undirected graph as an adjacency list adj (nodes 0..V-1),
return the order BFS visits the nodes, starting at node 0.

  - visit everything 1 edge away, then everything 2 away, and so on
  - within a ring, neighbours go in the order they appear in adj[u]
  - every node appears exactly once
```

## 🔢 The example
```
adj = [[2, 3, 1], [0], [0, 4], [0], [2]]

   ring 0:        0
                / | \
   ring 1:     2  3  1
               |
   ring 2:     4

Output: [0, 2, 3, 1, 4]
Why:    0 first, then all of 0's neighbours (2, 3, 1), then their unvisited
        neighbours (4). Compare DFS on the same graph: [0, 2, 4, 3, 1].

adj = [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]   ->  [0, 1, 2, 3, 4]
```

## 🧸 ELI5
> Drop a stone in a pond. The ripple reaches everything 1 metre away, then everything 2
> metres away, then 3. It never reaches something 3 metres away before something 2
> metres away.
>
> A queue does that for a graph. It's a **line at a shop**: new people join at the back,
> the person at the front gets served. Everyone 1 step from the start joins the line
> before anyone 2 steps away does, so they're all served first.
>
> ```
> line: [0]            serve 0, its friends 2, 3, 1 join the back
> line: [2, 3, 1]      serve 2, its new friend 4 joins the back
> line: [3, 1, 4]      serve 3, nobody new
> line: [1, 4]         serve 1, nobody new
> line: [4]            serve 4
> ```
>
> A **stack** is a pile of plates: the newest plate comes off first. That's DFS: you
> chase the newest discovery, deep before wide.

## 🐌 Brute force (say it, don't type it)
Use a Python `list` as the queue and `pop(0)` from the front. It's correct, and each
`pop(0)` shifts every remaining element, so it's **O(V)** per pop and **O(V²)** overall.
`collections.deque.popleft()` is O(1). Second naive version: mark visited when you
*pop*, not when you *push*. Still correct output here, but a node can sit in the queue
several times, which on a dense graph is O(E) queue entries instead of O(V).

## 💡 The pattern reveal
**Signal:** "level by level", "breadth first", and later "minimum steps / moves".
**Therefore:** Shape C from the pattern card: BFS with a `deque`.

**Key insight:** mark `visited` **when you push**, not when you pop. The moment a node
enters the queue its distance is decided, and nobody else should add it again.

```python
visited[0] = True
q = deque([0])
while q:
    u = q.popleft()
    order.append(u)
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True        # at PUSH time: the line people get wrong
            q.append(v)
```

| | DFS (EP153) | BFS (today) |
|---|---|---|
| container | stack / recursion | `deque` |
| takes next | newest discovery | oldest discovery |
| shape of the walk | one long path, then backtrack | rings of equal distance |
| gives you shortest steps? | **no** | **yes** (EP163) |

## 🔍 Dry run: `adj = [[2, 3, 1], [0], [0, 4], [0], [2]]`

| step | pop | neighbours checked | pushed (and marked) | queue after | order |
|---|---|---|---|---|---|
| 0 | - | - | 0 | `[0]` | `[]` |
| 1 | 0 | 2, 3, 1 | 2, 3, 1 | `[2, 3, 1]` | `[0]` |
| 2 | 2 | 0 (marked), 4 | 4 | `[3, 1, 4]` | `[0, 2]` |
| 3 | 3 | 0 (marked) | - | `[1, 4]` | `[0, 2, 3]` |
| 4 | 1 | 0 (marked) | - | `[4]` | `[0, 2, 3, 1]` |
| 5 | 4 | 2 (marked) | - | `[]` | `[0, 2, 3, 1, 4]` |

Answer **`[0, 2, 3, 1, 4]`** ✓. Look at the queue in step 2: `[3, 1, 4]`. Node 4 is
behind 3 and 1, because it's one ring further out. That ordering is the whole value
of BFS.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def bfs(self, adj: List[List[int]]) -> List[int]:
        """Breadth-first order from node 0, neighbours taken in adj order.

        Time:  O(V + E), each node is queued once, each adjacency entry read once.
        Space: O(V), visited plus a queue that can hold a whole ring.
        """
        visited = [False] * len(adj)
        visited[0] = True
        q = deque([0])
        order = []

        while q:
            u = q.popleft()                 # oldest discovery first
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True       # mark at push: never queued twice
                    q.append(v)

        return order
```
**Time:** O(V + E) · **Space:** O(V)

## ⚠️ Gotchas
- **Mark at push.** Mark at pop and two nodes that share a neighbour both enqueue it.
  On a grid (EP157) that makes the queue up to four times too big and breaks the level
  count. The pattern card's gotcha #1.
- **Mark the start before the loop.** Otherwise the start's neighbours push it back in.
- **`deque`, not `list`.** `list.pop(0)` is O(n); `deque.popleft()` is O(1).
- **BFS has no recursion limit problem.** One reason to prefer it when either would do.
- **Disconnected graph:** same fix as DFS, an outer loop that starts a new BFS from
  every unvisited node.

## 🎤 Interview talking points
- *"Same skeleton as DFS with a queue instead of a stack. The queue makes it visit in
  order of distance from the start."*
- *"I mark visited at push time, so every node enters the queue exactly once."* ← the
  line interviewers watch for.
- *"That distance-order property is why BFS gives shortest paths in an unweighted
  graph: the first time I reach a node is the fewest edges."*
- *"deque for O(1) pops from the front."*

## 🔗 Transfer
EP153 and EP154 are the two engines; the next seventeen episodes are these engines
pointed at different inputs. EP157 Rotten Oranges seeds the queue with **many** starts
and counts rings. EP163 writes `dist[v] = dist[u] + 1` at the push and gets shortest
paths for free. EP164 Dijkstra replaces this `deque` with a heap when edges have
weights.

## 📹 Metadata
- **Title:** `Graph BFS, swap one container and get shortest paths | Graphs #3`
- **Thumbnail:** `stack → queue` (blue block)
- **Short:** DFS and BFS side by side on the same graph, orders diverging at step 2. 40s.
