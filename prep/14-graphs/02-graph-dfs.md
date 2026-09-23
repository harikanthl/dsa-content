# EP153 · P14E02 · Graph DFS   [Easy]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/depth-first-traversal-for-a-graph/1

---

## 🎬 Hook
> "You already know DFS. You wrote it for trees in Pattern 13 without calling it that.
> A graph adds exactly **one** thing: cycles. Walk `0 → 2 → 0 → 2` and you never
> stop. So today's whole lesson is one set called `visited`, and where you put the
> line that fills it."

## 📋 Problem, in your words
```
Given a connected undirected graph as an adjacency list adj (nodes 0..V-1),
return the order DFS visits the nodes, starting at node 0.

  - go as deep as possible before backing up
  - try neighbours in the order they appear in adj[u]
  - every node appears exactly once in the output
```

## 🔢 The example
```
adj = [[2, 3, 1], [0], [0, 4], [0], [2]]

            0
          / | \
         2  3  1
         |
         4

Output: [0, 2, 4, 3, 1]
Why:    0 -> first neighbour 2 -> its first unvisited neighbour 4 -> dead end,
        back up to 0 -> next neighbour 3 -> dead end -> next neighbour 1.

adj = [[1, 2], [0, 2], [0, 1, 3, 4], [2], [2]]   ->  [0, 1, 2, 3, 4]
        (0-1-2 is a triangle: without visited, 0 -> 1 -> 2 -> 0 -> 1 ... forever)
```

## 🧸 ELI5
> You're in a cave with a piece of chalk. Every chamber you walk into, you chalk an X
> on the wall. Then you take the **first** tunnel out that leads somewhere without an X.
> When every tunnel from here leads to an X, you walk back the way you came and try the
> next tunnel from the chamber before.
>
> ```
> chamber 0: chalk it. tunnels: 2, 3, 1.  take 2.
>   chamber 2: chalk it. tunnels: 0 (X!), 4.  take 4.
>     chamber 4: chalk it. tunnels: 2 (X!).  dead end, walk back.
>   chamber 2: nothing left. walk back.
> chamber 0: next tunnel 3.
>   chamber 3: chalk it. tunnels: 0 (X!). walk back.
> chamber 0: next tunnel 1.
>   chamber 1: chalk it. tunnels: 0 (X!). walk back.
> done: 0, 2, 4, 3, 1
> ```
>
> The chalk is `visited`. The "walk back the way you came" is the call stack.

## 🐌 Brute force (say it, don't type it)
There isn't a slower correct traversal worth naming; the "brute force" here is DFS
**without** `visited`, and it isn't slow, it's **infinite** on the first cycle. The
nearest correct naive version checks "have I seen this?" with `v in result` on a list,
which is **O(V)** per check and turns the traversal into **O(V²)**. A set or a boolean
array makes that check O(1).

## 💡 The pattern reveal
**Signal:** "traverse", "reach", "explore everything connected to…".
**Therefore:** Shape B from the pattern card: DFS with a `visited` array.

**Key insight:** it's tree preorder (Pattern 13) plus **one guard**. In a tree each
node has one parent, so you can never arrive twice. In a graph you can, so you mark a
node the moment you enter it and skip anything already marked.

```python
def dfs(u):
    visited[u] = True         # chalk the wall FIRST
    order.append(u)
    for v in adj[u]:
        if not visited[v]:    # the only line a tree didn't need
            dfs(v)
```

| | tree DFS (EP122) | graph DFS (today) |
|---|---|---|
| children | `node.left`, `node.right` | `adj[u]`, any number |
| can revisit? | no, one parent each | **yes**, cycles and shared neighbours |
| guard | none | `visited` |

## 🔍 Dry run: `adj = [[2, 3, 1], [0], [0, 4], [0], [2]]`
Indent = depth of the call stack.

| step | call stack | at node | checks neighbour | action | order |
|---|---|---|---|---|---|
| 1 | `dfs(0)` | 0 | - | mark 0 | `[0]` |
| 2 | `dfs(0)` | 0 | 2 | unvisited, **go deeper** | `[0]` |
| 3 | `dfs(0) > dfs(2)` | 2 | - | mark 2 | `[0, 2]` |
| 4 | `dfs(0) > dfs(2)` | 2 | 0 | visited, skip | `[0, 2]` |
| 5 | `dfs(0) > dfs(2)` | 2 | 4 | unvisited, go deeper | `[0, 2]` |
| 6 | `dfs(0) > dfs(2) > dfs(4)` | 4 | - | mark 4 | `[0, 2, 4]` |
| 7 | `dfs(0) > dfs(2) > dfs(4)` | 4 | 2 | visited, skip; **return** | `[0, 2, 4]` |
| 8 | `dfs(0) > dfs(2)` | 2 | - | no more neighbours, **return** | `[0, 2, 4]` |
| 9 | `dfs(0)` | 0 | 3 | unvisited, go deeper | |
| 10 | `dfs(0) > dfs(3)` | 3 | 0 | mark 3; 0 visited, skip; return | `[0, 2, 4, 3]` |
| 11 | `dfs(0)` | 0 | 1 | unvisited, go deeper | |
| 12 | `dfs(0) > dfs(1)` | 1 | 0 | mark 1; 0 visited, skip; return | `[0, 2, 4, 3, 1]` |

Answer **`[0, 2, 4, 3, 1]`** ✓. Steps 4, 7, 10 and 12 are the four times `visited`
saved us from walking straight back into node 0 or 2.

## ✅ Optimal solution
```python
class Solution:
    def dfs(self, adj: List[List[int]]) -> List[int]:
        """Depth-first order from node 0, neighbours tried in adj order.

        Time:  O(V + E), each node is entered once, each adjacency entry read once.
        Space: O(V), visited plus a recursion stack as deep as the longest path.
        """
        visited = [False] * len(adj)
        order = []

        def go(u: int) -> None:
            visited[u] = True               # mark on entry, before any neighbour
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    go(v)

        go(0)
        return order
```
**Time:** O(V + E) · **Space:** O(V)

**Iterative version**, for when the graph is deep enough to hit Python's recursion
limit (~1000 by default). Push neighbours **reversed** so the first one is on top and
the order matches the recursive version:

```python
        visited = [False] * len(adj)
        order, stack = [], [0]
        while stack:
            u = stack.pop()
            if visited[u]:
                continue                    # pushed twice before we got to it
            visited[u] = True
            order.append(u)
            for v in reversed(adj[u]):
                if not visited[v]:
                    stack.append(v)
        return order
```

## ⚠️ Gotchas
- **Mark on entry, not on exit.** Mark after the loop and a cycle recurses forever,
  because you re-enter `u` from its own neighbour before `u` is marked.
- **The recursion limit is real.** A path graph of 10⁴ nodes is a `RecursionError` in
  Python. Say so, and offer the iterative version.
- **Iterative DFS marks at pop, not at push, if you want the true DFS order.** Marking
  at push gives a valid traversal but a different order from the recursive one, and
  the GfG judge checks the order.
- **Reversed push.** A stack pops the last thing pushed, so pushing `[2, 3, 1]` in
  order visits 1 first. Reverse it to visit 2 first.
- **Disconnected graphs.** This version only reaches node 0's component. If the graph
  might be disconnected, loop over every node and start a fresh `go(u)` for each
  unvisited one. That loop is tomorrow-after-next's whole episode (EP155).

## 🎤 Interview talking points
- *"It's tree preorder plus a visited set, because a graph can have cycles and a node
  can be reached from several neighbours."*
- *"O(V + E): each node is entered once, and over all nodes I read each adjacency entry
  once, which is 2E for an undirected graph."*
- *"Recursive is clearest; iterative with an explicit stack if depth could exceed the
  recursion limit. I'd push neighbours reversed to keep the same order."*
- *"If it's disconnected, an outer loop over all nodes restarts DFS in each component."*

## 🔗 Transfer
EP152 built `adj`; today we walked it deep-first. Tomorrow (EP154) keeps the same
`visited` and swaps the stack for a **queue**, and the order changes from "deep first"
to "rings of equal distance". Then EP155 wraps today's function in an outer loop and
counts how many times it had to start over: that count is the number of islands.

## 📹 Metadata
- **Title:** `Graph DFS, it's tree traversal plus one set | Graphs #2`
- **Thumbnail:** `visited = ✓` (green block)
- **Short:** the triangle 0-1-2 looping forever without `visited`, then stopping cleanly
  with it. 35s.
