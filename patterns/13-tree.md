# Pattern 13: Tree

**31 episodes · EP 121–151**

---

## The one-sentence version

Every tree problem is **one recursive function**, and the only design question is *what
does this node need from its children, and what does it hand back to its parent?*,
answer that and you've already decided DFS vs BFS, top-down vs bottom-up, and what the
base case returns.

## ELI5

A tree is a family: one ancestor at the top, everyone else has exactly one parent. If you
want to know something about the whole family, you don't interview everyone yourself. You
ask the top person, and they ask their two children, and each of *them* asks their two
children, all the way down to the people with no kids, who answer immediately.

```
        1
       / \
      2   3
     / \
    4   5
```

The person with no kids is the **base case**. Everyone else's job is the same three
lines: *ask left, ask right, combine*. That's the whole pattern. Thirty-one episodes, and
the only thing that changes is what "ask" returns and what "combine" does.

Two ways to visit the family:

| | you go | you use | the question smells like |
|---|---|---|---|
| **DFS** | as deep as you can before turning back | recursion (or an explicit stack) | "path", "depth", "is this tree …", "sum of …" |
| **BFS** | one generation at a time | a queue | "level", "nearest", "minimum depth", "complete" |

## How to recognise it

| Signal | Example |
|---|---|
| a `TreeNode` with `.left` and `.right` | all thirty-one |
| "**level** order", "zigzag", "each level" | EP124, EP125, EP126 |
| "**minimum** depth", "nearest leaf", "complete" | EP138, EP142, the BFS tells |
| "mirror", "symmetric", "same", "subtree of", "flip" | EP127–131, two trees walked in lockstep |
| "**lowest common ancestor**" | EP132, EP134, EP135 |
| the tree is a **BST** and the question mentions order, kth, validate, recover | EP133, EP136, EP137, EP143, EP144, inorder is sorted |
| "path sum", "root to leaf", "any node to any node" | EP145–148 |
| "construct from preorder/inorder/sorted array" | EP149–151 |
| "depth", "balanced", "diameter", a number computed from both children | EP139–141, bottom-up |

**The DFS-vs-BFS tell:** if the answer would still be the same when you swap the
children's order, and it's about the *whole* subtree, it's DFS. If the problem talks
about *which level* something is on, or wants the *closest* thing to the root, it's BFS.

**The BST tell:** the moment the problem says "binary **search** tree", stop thinking
about the tree and start thinking about the sorted array its inorder traversal produces.

## Shape A: DFS, the three orders

One function. The only thing that moves is the line that does the work.

```python
def dfs(node):
    if not node:
        return
    # print(node.val)      # <- PREorder:  root, left, right
    dfs(node.left)
    # print(node.val)      # <- INorder:   left, root, right
    dfs(node.right)
    # print(node.val)      # <- POSTorder: left, right, root
```

```
        1
       / \          preorder:  1 2 4 5 3     (root first  -> copying, serialising)
      2   3         inorder:   4 2 5 1 3     (BST -> sorted)
     / \            postorder: 4 5 2 3 1     (children first -> deleting, sizes)
    4   5
```

Iterative inorder, because interviewers ask for it and because it's how kth-smallest
(EP137) stops early:

```python
stack, node = [], root
while stack or node:
    while node:                 # dive left as far as possible
        stack.append(node)
        node = node.left
    node = stack.pop()          # the leftmost unvisited
    visit(node)                 # <- inorder position
    node = node.right           # then its right subtree
```

## Shape B: BFS, one level at a time

```python
from collections import deque
queue, result = deque([root]), []
while queue:
    level = []
    for _ in range(len(queue)):        # <- exactly the nodes on THIS level
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    result.append(level)
```

The `for _ in range(len(queue))` is the whole trick: `len(queue)` is read *once*, before
the children are appended, so the loop consumes exactly one generation.

| variant | change |
|---|---|
| zigzag (EP125) | `level.reverse()` when the level index is odd |
| level order II (EP126) | `result.reverse()` at the end, or `result.appendleft(level)` |
| minimum depth (EP138) | return the level number the first time you pop a leaf |
| completeness (EP142) | push `None` children too; once you've seen a `None`, any real node afterwards → `False` |

## Shape C: two trees in lockstep

```python
def same(a, b):
    if not a and not b: return True        # both empty
    if not a or not b:  return False       # one empty
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)
```

Every problem in the mirror family is this function with the recursive calls re-wired:

| problem | the recursive line |
|---|---|
| Same Tree (EP129) | `same(a.left, b.left) and same(a.right, b.right)` |
| Symmetric (EP128) | `mirror(a.left, b.right) and mirror(a.right, b.left)`, called as `mirror(root.left, root.right)` |
| Invert (EP127) | not a comparison: `node.left, node.right = invert(node.right), invert(node.left)` |
| Subtree of Another (EP130) | `same(s, t) or subtree(s.left, t) or subtree(s.right, t)`, try `same` at *every* node |
| Flip Equivalent (EP131) | `(eq(a.left, b.left) and eq(a.right, b.right)) or (eq(a.left, b.right) and eq(a.right, b.left))` |

The two base cases come first, in that order, every time. Swapping them or merging them
is how you get a `None.val` crash.

## Shape D: bottom-up: return a value, update a global

The children compute something; the parent combines it and may also compare it against a
best-so-far that lives *outside* the recursion.

```python
def depth(node):
    if not node:
        return 0
    return 1 + max(depth(node.left), depth(node.right))       # EP139
```

```python
def diameter(root):                                             # EP141
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        L, R = height(node.left), height(node.right)
        best = max(best, L + R)          # the answer uses BOTH arms ...
        return 1 + max(L, R)             # ... but the parent only gets ONE arm
    height(root)
    return best
```

That split, *the return value is the best single arm, the answer is recorded from both
arms*, is the entire idea behind three episodes:

| problem | returns to parent | records as the answer |
|---|---|---|
| Diameter (EP141) | `1 + max(L, R)` | `L + R` |
| Max Path Sum (EP148) | `node.val + max(L, R, 0)` | `node.val + max(L, 0) + max(R, 0)` |
| Balanced (EP140) | height, or **`-1` as a sentinel** meaning "already unbalanced below" | `-1` anywhere → `False` |

The `-1` sentinel in Balanced is what turns the obvious O(n²) (call `depth` at every
node) into O(n): the height and the verdict travel up together in one value.

## Shape E: BST: inorder is sorted

```python
def valid(node, lo=float('-inf'), hi=float('inf')):            # EP143
    if not node:
        return True
    if not (lo < node.val < hi):
        return False
    return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
```

Going left **tightens `hi`**; going right **tightens `lo`**. The alternative is an
inorder walk with a `prev` pointer, checking `prev < node.val` at each step, and that
same walk is the engine for the rest of the family:

| problem | the inorder walk does |
|---|---|
| Kth Smallest (EP137) | count visits; return on the kth (iterative, so you can stop) |
| Recover BST (EP144) | find the two places where `prev > node`; those are the swapped nodes |
| Two Sum IV (EP136) | dump inorder into a sorted list → Pattern 01 opposite-ends two pointers |
| BST basics (EP133) | search/insert: go left if smaller, right if bigger, one branch, O(h) |

## Shape F: Lowest Common Ancestor

```python
def lca(node, p, q):                                            # EP132
    if not node or node is p or node is q:
        return node
    L, R = lca(node.left, p, q), lca(node.right, p, q)
    if L and R:
        return node          # p and q are on different sides: this is the split
    return L or R            # both on one side: pass that side's answer up
```

In a BST (EP134) there's no recursion into both sides, compare and walk: both smaller →
go left, both bigger → go right, otherwise you're standing on the answer. O(h).

LCA of Deepest Leaves (EP135) is Shape D wearing an LCA hat: return `(depth, node)`; if
the depths from both sides are equal, *this* node is the answer, otherwise pass up the
deeper side.

## Shape G: construction from traversals

```python
def build(preorder, inorder):                                   # EP149
    idx = {v: i for i, v in enumerate(inorder)}                 # O(1) lookups
    def rec(pre_lo, pre_hi, in_lo, in_hi):
        if pre_lo > pre_hi:
            return None
        root = TreeNode(preorder[pre_lo])                       # preorder[0] IS the root
        mid = idx[root.val]                                     # find it in inorder
        left_size = mid - in_lo                                 # everything left of it is the left subtree
        root.left  = rec(pre_lo + 1, pre_lo + left_size, in_lo, mid - 1)
        root.right = rec(pre_lo + left_size + 1, pre_hi, mid + 1, in_hi)
        return root
    return rec(0, len(preorder) - 1, 0, len(inorder) - 1)
```

Postorder + inorder (EP150) is the same with the root at `postorder[-1]` and the right
subtree carved off first. Sorted Array to BST (EP151) is the degenerate case: there's no
preorder to consult, so *choose* the root, `mid`, and recurse on the two halves.

## The three things that go wrong

### 1. The null check isn't the first line

`if not node: return <base value>` goes at the top of every DFS, before touching
`.val`, `.left`, or `.right`. In two-tree recursion there are **two** null checks (both
empty, then one empty), and they come in that order. Most tree crashes are this.

### 2. Validate BST by comparing with the parent only

```python
# WRONG: passes on the tree  5 -> (1, 6 -> (4, 7)): the 4 is left of 6 but right of 5
return node.left.val < node.val < node.right.val and ...
```

A node has to be bigger than *every* ancestor it went right from and smaller than *every*
ancestor it went left from. That's what the `(lo, hi)` bounds carry. Compare with the
parent alone and you'll pass 90% of tests and fail the one that matters.

### 3. Appending the live path list

In Path Sum II (EP146) the `path` list is shared across the whole recursion. `result.
append(path)` stores a reference that keeps changing; you need `result.append(path[:])`.
And every `path.append(node.val)` needs a matching `path.pop()` on the way back up, the
backtracking bookkeeping from Pattern 12.

## Complexity

| Problem | Time | Space |
|---|---|---|
| any single DFS or BFS | O(n) | O(h) recursion / O(w) queue, both O(n) worst case |
| BST search / insert / LCA-of-BST (EP133, EP134) | O(h), O(log n) balanced, O(n) skewed | O(1) iterative |
| Kth Smallest, iterative (EP137) | O(h + k) | O(h) |
| Subtree of Another Tree, naive (EP130) | O(n · m) | O(h) |
| Balanced, the sentinel version (EP140) | O(n) | O(h) |
| Balanced, calling `depth` at every node | **O(n²)** | O(h), the version to avoid |
| Construction with the index map (EP149, EP150) | O(n) | O(n) |
| Construction with `inorder.index()` each call | O(n²) | O(n) |

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 121 | Inorder | Traversal | The recursive template; iterative with a stack. |
| 122 | Preorder | Traversal | Same function, the visit moves up one line. |
| 123 | Postorder | Traversal | Children first, the order for deletes and sizes. |
| 124 | Level Order | Traversal | The queue and `for _ in range(len(queue))`. |
| 125 | ZigZag Order | Traversal | Level order + reverse the odd levels. |
| 126 | Level Order II | Traversal | Level order + reverse the result. |
| 127 | Invert Tree | Mirror | Swap children, recurse. Three lines. |
| 128 | Symmetric Tree | Mirror | `mirror(a.left, b.right)`, the cross-wiring. |
| 129 | Same Tree | Mirror | Two null checks, in order, then compare. |
| 130 | Subtree of Another Tree | Mirror | Run `same` at every node. |
| 131 | Flip Equivalent Tree | Mirror | Straight OR swapped, two `same`s joined by `or`. |
| 132 | LCA of Binary Tree | Search | Return the node from either side; both sides → this is it. |
| 133 | Binary Search Tree | Search | Search/insert: one branch per level, O(h). |
| 134 | LCA of BST | Search | No recursion, compare and walk. |
| 135 | LCA of Deepest Leaves | Search | Return `(depth, node)`; equal depths → this node. |
| 136 | Two Sum IV | Search | Inorder → sorted list → Pattern 01. |
| 137 | Kth Smallest in BST | Search | Iterative inorder so you can stop at k. |
| 138 | Minimum Depth | Validation | BFS, the first leaf you pop is the answer. |
| 139 | Maximum Depth | Validation | `1 + max(L, R)`, the bottom-up template. |
| 140 | Balanced Binary Tree | Validation | Height and verdict in one return; `-1` sentinel. |
| 141 | Diameter | Validation | Return one arm, record both arms. |
| 142 | Check Completeness | Validation | BFS with `None`s; a real node after a `None` fails. |
| 143 | Validate BST | Validation | `(lo, hi)` bounds, tightened per side. |
| 144 | Recover BST | Validation | Inorder finds the two inversions; swap their values. |
| 145 | Path Sum | Path Sum | Subtract on the way down; check at a leaf. |
| 146 | Path Sum II | Path Sum | Carry the path; `path[:]` when recording; pop on return. |
| 147 | Sum of Root to Leaf | Path Sum | `acc = acc * 10 + val` down; sum at leaves. |
| 148 | Maximum Path Sum | Path Sum | Shape D with negatives clamped to 0. |
| 149 | Construct from Preorder + Inorder | Construction | `preorder[0]` is the root; split inorder around it. |
| 150 | Construct from Postorder + Inorder | Construction | `postorder[-1]` is the root; build right first. |
| 151 | Sorted Array to BST | Construction | Pick `mid` as the root; recurse on halves. |

## What "knowing this in your sleep" means

1. What does this node need from its children, and what does it return to its parent?
   *(Answer this before writing anything. It decides top-down vs bottom-up.)*
2. DFS or BFS, and why? *(BFS whenever the problem says "level", "nearest", or
   "minimum depth". Everything else is DFS.)*
3. Where does the visit go for pre/in/post order? *(Before the calls, between them,
   after them. Inorder on a BST is sorted.)*
4. How do you get O(n) for Balanced and Diameter? *(One pass: return the height, record
   the answer on the way up. `-1` as a sentinel for "already failed".)*
5. Why is comparing with the parent not enough to validate a BST? *(A node must satisfy
   every ancestor. Carry `(lo, hi)` bounds and tighten the right one per side.)*
6. How do you build a tree from preorder and inorder? *(`preorder[0]` is the root; its
   inorder index splits both arrays; a hash map makes the lookup O(1).)*
