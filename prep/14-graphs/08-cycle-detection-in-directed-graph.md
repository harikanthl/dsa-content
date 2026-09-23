# EP159 · P14E08 · Cycle Detection in a Directed Graph   [Medium]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/detect-cycle-in-a-directed-graph/1

---

## 🎬 Hook
> "Yesterday a visited neighbour that wasn't your parent meant a cycle. On a directed
> graph that rule lies: `A → B → C` and `A → C` reaches C twice, and there's **no**
> cycle. 'Visited' isn't enough information. You need to know whether the node is
> **still on the path you're walking right now**. That's three colours instead of two."

## 📋 Problem, in your words
```
Given V nodes (0..V-1) and a list of DIRECTED edges [u, v] (u -> v),
return True if the graph contains a cycle.

  - the graph may be disconnected
  - a self-loop u -> u is a cycle
```

## 🔢 The example
```
V = 4, edges = [[0,1], [1,2], [2,0], [2,3]]

    0 --> 1
    ^     |
    |     v
    +---- 2 --> 3

Output: True       <- 0 -> 1 -> 2 -> 0

V = 4, edges = [[0,1], [0,2], [1,2], [2,3]]

    0 --> 1
    |     |
    v     v
    2 <---+
    |
    v
    3

Output: False      <- 2 is reached twice (via 1, and directly from 0), but no arrow leads back
```

## 🧸 ELI5
> You're following one-way streets, unrolling a ball of string behind you. The string
> marks the route you're **currently on**. When you hit a dead end, you walk back,
> **winding the string up**, but you leave a chalk mark on the corners you've finished.
>
> - Reach a corner with **string** on it: you've come back to your own path. Loop!
> - Reach a corner with only **chalk** on it: you finished exploring it earlier, on a
>   different route. It's just a junction, not a loop.
>
> ```
> no-cycle graph: 0 -> 1 -> 2 -> 3, then back up to 0, then 0 -> 2
>   at 2 the second time: chalk only (finished), no string -> NOT a loop
> cycle graph: 0 -> 1 -> 2 -> 0
>   at 0: string is still there -> LOOP
> ```
>
> String = GRAY. Chalk = BLACK. Untouched = WHITE.

## 🐌 Brute force (say it, don't type it)
For every node `s`, run a DFS from `s` and check whether you can get back to `s`.
**O(V · (V + E))**. The redundancy: nodes already fully explored from an earlier start
are explored again from every later start. BLACK is exactly the memo that stops that.

## 💡 The pattern reveal
**Signal:** "cycle" in a **directed** graph, "deadlock", "circular dependency".
**Therefore:** Shape D: DFS with **three colours**.

**Key insight:** a directed cycle is an edge that points **back to a node on the
current DFS path**. Visited-but-finished nodes are safe. So you need two kinds of
"visited".

| colour | meaning | set when | an edge into it means |
|---|---|---|---|
| WHITE | never seen | start | explore it |
| **GRAY** | on the current path | on **entry** | **cycle** |
| BLACK | finished, all descendants explored | on **exit** | nothing, skip it |

```python
def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY: return True           # back to my own path
        if color[v] == WHITE and dfs(v): return True
    color[u] = BLACK                               # done: off the path
    return False
```

The submitted solution runs the same thing with an explicit stack of `(node, next
neighbour index)`, so that GfG's large V can't blow the recursion limit.

## 🔍 Dry run: the **no-cycle** graph `[[0,1], [0,2], [1,2], [2,3]]`
`adj = [[1, 2], [2], [3], []]`. Colours: W/G/B for nodes 0 1 2 3.

| step | at | edge | colour of target | action | colours after |
|---|---|---|---|---|---|
| 1 | 0 | - | - | enter 0 | `G W W W` |
| 2 | 0 | 0 → 1 | WHITE | enter 1 | `G G W W` |
| 3 | 1 | 1 → 2 | WHITE | enter 2 | `G G G W` |
| 4 | 2 | 2 → 3 | WHITE | enter 3 | `G G G G` |
| 5 | 3 | none left | - | **finish 3** | `G G G B` |
| 6 | 2 | none left | - | finish 2 | `G G B B` |
| 7 | 1 | none left | - | finish 1 | `G B B B` |
| 8 | 0 | 0 → 2 | **BLACK** | skip: finished earlier, not on my path | `G B B B` |
| 9 | 0 | none left | - | finish 0 | `B B B B` |

**False** ✓. Step 8 is the whole episode: yesterday's rule ("visited and not my parent")
would call 0 → 2 a cycle. BLACK says it's just a second road into a finished node.

**The cycle graph** `[[0,1], [1,2], [2,0], [2,3]]`: enter 0, enter 1, enter 2, then
edge 2 → 0 finds 0 **GRAY**, still on the path. **True** ✓.

## ✅ Optimal solution
```python
class Solution:
    def isCyclic(self, V: int, edges: List[List[int]]) -> bool:
        """True if the directed graph has a cycle.

        Time:  O(V + E), each node is entered and finished once, each edge read once.
        Space: O(V + E), the adjacency list, plus O(V) for colours and the stack.
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        adj = [[] for _ in range(V)]
        for u, v in edges:
            adj[u].append(v)                        # directed: one append

        color = [WHITE] * V
        for start in range(V):
            if color[start] != WHITE:
                continue
            color[start] = GRAY
            stack = [(start, 0)]                    # (node, index of next neighbour to try)
            while stack:
                u, i = stack[-1]
                if i < len(adj[u]):
                    stack[-1] = (u, i + 1)
                    v = adj[u][i]
                    if color[v] == GRAY:            # points back onto the current path
                        return True
                    if color[v] == WHITE:
                        color[v] = GRAY
                        stack.append((v, 0))
                else:
                    color[u] = BLACK                # all neighbours done: leave the path
                    stack.pop()
        return False
```
**Time:** O(V + E) · **Space:** O(V + E)

## ⚠️ Gotchas
- **Two colours are not enough.** A plain `visited` set reports step 8 as a cycle.
  The pattern card's gotcha #2, the directed half.
- **BLACK on exit, not on entry.** Set it when you enter and you've thrown away GRAY:
  nothing is ever "on the path", and you never find a cycle.
- **The iterative version must keep its place in `adj[u]`.** A plain "pop a node, push
  all neighbours" stack doesn't know when a node is *finished*, so it can't set BLACK at
  the right moment. That's why the stack holds `(node, i)`.
- **Self-loop `u → u`**: entering `u` makes it GRAY, and the edge to itself finds GRAY.
  Correctly a cycle.
- **Loop over every start**, same as every component problem.
- **Kahn's algorithm is the other answer.** If a topological sort (EP160) can't place
  every node, there's a cycle. Mention it; it avoids recursion entirely.

## 🎤 Interview talking points
- *"In a directed graph, reaching a visited node doesn't mean a cycle; two paths can
  merge. A cycle is an edge back to a node that's still on the current DFS path."*
- *"So three states: WHITE unseen, GRAY on the path, BLACK finished. GRAY on entry,
  BLACK on exit, and a GRAY neighbour is a cycle."*
- *"BLACK is also a memo: a finished node is never explored again, so it's O(V + E)
  across all starts."*
- *"Alternatively, Kahn's topological sort: if fewer than V nodes come out, the rest are
  on or behind a cycle."*

## 🔗 Transfer
Cycle detection on directed graphs is really "can this be ordered?", and tomorrow
(EP160) answers that question directly: topological sort produces the order, and fails
exactly when today's function returns True. The finish order you just watched (3, 2, 1,
0) reversed is already a valid topological order; that's the DFS version of EP160.

## 📹 Metadata
- **Title:** `Cycle in a Directed Graph, why you need a THIRD colour | Graphs #8`
- **Thumbnail:** `WHITE GRAY BLACK` (grey block)
- **Short:** step 8, the BLACK node that a visited set would have called a cycle. 45s.
