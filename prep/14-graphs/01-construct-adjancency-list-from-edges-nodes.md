# EP152 · P14E01 · Construct Adjacency List from Edges   [Easy]

**Pattern:** Graphs · **Link:** https://www.geeksforgeeks.org/problems/print-adjacency-list-1587115620/1

---

## 🎬 Hook
> "Twenty graph episodes start here, and not one of them runs an algorithm on a list of
> edges. They all ask the same question a million times: **who are the neighbours of
> `u`?** Today we build the thing that answers it in O(1), and the whole difference
> between a directed and an undirected graph turns out to be **one line**."

## 📋 Problem, in your words
```
You get V (nodes are 0..V-1) and a list of undirected edges [u, v].
Return the adjacency list: adj[u] is the list of every node joined to u.

  - undirected: an edge u-v puts v in adj[u] AND u in adj[v]
  - keep neighbours in the order their edges appear in the input
  - a node with no edges still gets an (empty) list
```

## 🔢 The example
```
V = 5
edges = [[0,1], [0,4], [4,1], [4,3], [1,3], [1,2], [3,2]]

        0 ------- 1
        |       / | \
        |     /   |   2
        |   /     | /
        4 ------- 3

Output:
  adj[0] = [1, 4]
  adj[1] = [0, 4, 3, 2]
  adj[2] = [1, 3]
  adj[3] = [4, 1, 2]
  adj[4] = [0, 1, 3]

V = 4, edges = [[0,1]]   ->   [[1], [0], [], []]   <- 2 and 3 are isolated, still listed
```

## 🧸 ELI5
> The edge list is a pile of handshake photos: "0 shook hands with 1", "0 shook hands
> with 4", and so on. If someone asks *"who did 1 shake hands with?"* you'd have to flip
> through **every** photo.
>
> An adjacency list is a notebook with one page per person. For every photo, you write
> each person's name on the **other** person's page. Now "who did 1 shake hands with?"
> is: open page 1.
>
> ```
> photo 0-1   ->  page 0: [1]         page 1: [0]
> photo 0-4   ->  page 0: [1, 4]      page 4: [0]
> photo 4-1   ->  page 4: [0, 1]      page 1: [0, 4]
> ...
> ```
>
> A handshake goes both ways, so it gets written twice. A one-way street (directed
> edge) would only be written on the page of the person it starts from.

## 🐌 Brute force (say it, don't type it)
Keep the raw edge list and, every time an algorithm needs `u`'s neighbours, scan all E
edges for ones touching `u`. That's **O(E) per lookup**, and DFS/BFS look up every node,
so the traversal becomes **O(V · E)** instead of O(V + E). The other "obvious" choice, a
V × V adjacency matrix, gives O(1) edge checks but costs **O(V²)** memory and O(V) to
list neighbours even for a node with one edge.

## 💡 The pattern reveal
**Signal:** you're handed edges, and every later step wants neighbours.
**Therefore:** Shape A from the pattern card: build the adjacency list once, up front.

**Key insight:** each input edge becomes **two appends** for an undirected graph and
**one** for a directed one. That line is the only thing you change between the two.

| representation | memory | "neighbours of u" | "is u-v an edge?" | use it when |
|---|---|---|---|---|
| edge list | O(E) | O(E) | O(E) | input format, Bellman-Ford (EP168) |
| **adjacency list** | **O(V + E)** | **O(deg u)** | O(deg u) | **almost always** |
| adjacency matrix | O(V²) | O(V) | O(1) | dense graphs, Provinces (EP156) hands you one |

```python
adj = [[] for _ in range(V)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)        # delete this line and the graph is directed
```

## 🔍 Dry run: `V = 5`, the seven edges above
Start: `adj = [[], [], [], [], []]`.

| step | edge | appends | adj after |
|---|---|---|---|
| 1 | `[0,1]` | adj[0] += 1, adj[1] += 0 | `[[1], [0], [], [], []]` |
| 2 | `[0,4]` | adj[0] += 4, adj[4] += 0 | `[[1,4], [0], [], [], [0]]` |
| 3 | `[4,1]` | adj[4] += 1, adj[1] += 4 | `[[1,4], [0,4], [], [], [0,1]]` |
| 4 | `[4,3]` | adj[4] += 3, adj[3] += 4 | `[[1,4], [0,4], [], [4], [0,1,3]]` |
| 5 | `[1,3]` | adj[1] += 3, adj[3] += 1 | `[[1,4], [0,4,3], [], [4,1], [0,1,3]]` |
| 6 | `[1,2]` | adj[1] += 2, adj[2] += 1 | `[[1,4], [0,4,3,2], [1], [4,1], [0,1,3]]` |
| 7 | `[3,2]` | adj[3] += 2, adj[2] += 3 | `[[1,4], [0,4,3,2], [1,3], [4,1,2], [0,1,3]]` |

Seven edges, fourteen appends: **the sum of all list lengths is 2E**. That fact is
where the "+ E" in every O(V + E) bound comes from.

## ✅ Optimal solution
```python
class Solution:
    def printGraph(self, V: int, edges: List[List[int]]) -> List[List[int]]:
        """Adjacency list of an undirected graph with nodes 0..V-1.

        Time:  O(V + E), V empty lists, then two O(1) appends per edge.
        Space: O(V + E), V lists holding 2E entries in total.
        """
        adj = [[] for _ in range(V)]        # NOT [[]] * V: that's one shared list

        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)                # undirected: the edge works both ways

        return adj
```
**Time:** O(V + E) · **Space:** O(V + E)

## ⚠️ Gotchas
- **`[[]] * V` is V references to one list.** Every append lands in all of them and
  every node ends up with every neighbour. Use the comprehension.
- **Directed or undirected? Ask.** Undirected is two appends. Directed is one, and
  it's `adj[u].append(v)` (from `u`, to `v`), not the other way round.
- **Isolated nodes must exist.** Building from a `defaultdict(list)` is fine for
  lookups, but if you *return* it, nodes with no edges are missing. With a fixed `V`,
  preallocate.
- **Weighted edges store pairs.** `[u, v, w]` becomes `adj[u].append((v, w))`. Dijkstra
  (EP164) and Prim (EP170) both need this form.
- **Self-loop `[2, 2]`** appends 2 to adj[2] twice under the undirected rule. That's
  the honest representation (degree 2), but mention it if the input can contain one.
- **Neighbour order matters on GfG.** The judge compares against input order, so don't
  sort, and don't use a set.

## 🎤 Interview talking points
- *"First three questions: directed? weighted? and are the nodes given explicitly, or
  implicit like grid cells?"* ← the pattern card's opener, say it every graph problem.
- *"Adjacency list is O(V + E) memory and gives me a node's neighbours in O(degree).
  A matrix is O(V²) and only wins on dense graphs or O(1) edge queries."*
- *"The lists add up to 2E for an undirected graph. That's why traversal is O(V + E)."*
- *"If node ids were strings, I'd use `defaultdict(list)` instead of a preallocated
  list, and remember isolated nodes separately."*

## 🔗 Transfer
Every episode through EP171 opens with these four lines, so this is the one to have in
your fingers. Tomorrow (EP153) takes this `adj` and walks it with DFS; EP154 walks the
same `adj` with BFS. When grids arrive (EP155) the adjacency list vanishes: neighbours
are computed on the fly as the four cells around you, which is the same idea with no
storage at all.

## 📹 Metadata
- **Title:** `Adjacency List, the one line between directed and undirected | Graphs #1`
- **Thumbnail:** `edges → adj[u]` (blue block)
- **Short:** the seven-row table filling up, then deleting `adj[v].append(u)` and
  watching half the arrows disappear. 40s.
