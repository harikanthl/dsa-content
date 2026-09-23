# EP141 · P13E21 · Diameter of Binary Tree   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/diameter-of-binary-tree/description/

---

## 🎬 Hook
> "The longest path in a tree bends at some node: it comes up one arm and goes down the
> other. So at that node the answer is `left + right`. But when that node reports back
> to its parent, it can only offer **one** arm, because a path can't fork. **Return one
> arm, record both arms.** That sentence is this episode, and it's also the hardest
> tree problem in the series, EP148."

## 📋 Problem, in your words
```
Given the root of a binary tree, return the length of its diameter:
the number of EDGES on the longest path between ANY two nodes.

  - the path does not have to pass through the root
  - a single node has diameter 0
```

## 🔢 The example
```
Input:  [1,2,3,4,5]
Output: 3

            1
           / \
          2   3
         / \
        4   5

Why:    4 -> 2 -> 1 -> 3   (or 5 -> 2 -> 1 -> 3): 3 edges

Input:  [1,2,null,3,4,5,null,null,6]
Output: 4

            1
           /
          2          <- the longest path bends HERE, not at the root
         / \
        3   4
       /     \
      5       6

Why:    5 -> 3 -> 2 -> 4 -> 6: 4 edges. Through the root, the best is only 3.
```

## 🧸 ELI5
> Imagine the tree is made of string and every node is a knot. You want to pick up the
> two knots that are **farthest apart** and pull them tight.
>
> Wherever you hold the string, the tight path goes up from one knot to some **highest
> point**, then down to the other. At that highest point, it used the longest string
> hanging to the left **plus** the longest hanging to the right.
>
> So: at every knot, ask "longest left arm + longest right arm?" and remember the best
> you've ever seen. But when a knot tells its parent how long it is, it can only give
> **one** arm, the longer one, because the parent's path can only continue down one
> side.

## 🐌 Brute force (say it, don't type it)
At every node, compute `maxDepth(left) + maxDepth(right)` with EP139's function, and
take the max over all nodes. Correct, and it's the same waste as EP140's brute force:
every height recomputed by every ancestor, **O(n · h)**, O(n²) worst case.

## 💡 The pattern reveal
**Signal:** a number computed from **both children**, "longest path between any two
nodes".
**Therefore:** Shape D, bottom-up, and the first episode with the pattern card's split:

| problem | returns to parent | records as the answer |
|---|---|---|
| **Diameter (today)** | `1 + max(L, R)` | `L + R` |
| Max Path Sum (EP148) | `node.val + max(L, R, 0)` | `node.val + max(L, 0) + max(R, 0)` |

**Key insight:** the function **returns height** (what the parent needs) and, as a side
effect, **updates a global best** with `L + R` (what the question asks). Those are two
different numbers, and mixing them up is the entire bug surface.

```python
L, R = height(node.left), height(node.right)
best = max(best, L + R)          # the answer uses BOTH arms ...
return 1 + max(L, R)             # ... but the parent only gets ONE arm
```

Why `L + R` is edges: `height` counts nodes, so a left subtree of height 2 contributes 2
edges (the edge down into it, plus one inside it). Two arms: `L + R` edges.

## 🔍 Dry run: `[1,2,3,4,5]`

Postorder, in the order calls return:

| step | node | L | R | `L + R` | best after | returns `1 + max(L, R)` |
|---|---|---|---|---|---|---|
| 1 | 4 | 0 | 0 | 0 | 0 | 1 |
| 2 | 5 | 0 | 0 | 0 | 0 | 1 |
| 3 | 2 | 1 | 1 | 2 | 2 | 2 |
| 4 | 3 | 0 | 0 | 0 | 2 | 1 |
| 5 | 1 | 2 | 1 | **3** | **3** | 3 |

Answer **3** ✓. The root returns 3 (its height), and nobody uses that return. The answer
is in `best`.

On the second example, node 2 records `L + R = 2 + 2 = 4`, and the root records only
`3 + 0 = 3`. `best` keeps the 4. That's why the answer is a global and not the root's
return value.

## ✅ Optimal solution
```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """Edges on the longest path between any two nodes.

        Time:  O(n), one postorder pass.
        Space: O(h), the recursion stack.
        """
        best = 0

        def height(node: Optional[TreeNode]) -> int:
            """Nodes on the longest downward path from node; records the diameter."""
            nonlocal best
            if not node:
                return 0
            L, R = height(node.left), height(node.right)
            best = max(best, L + R)         # the path that bends at this node
            return 1 + max(L, R)            # the parent can only extend one arm

        height(root)
        return best
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **The path doesn't have to pass through the root.** Returning `L + R` at the root only
  passes the first example and fails the second. That's the reason `best` is global.
- **Edges, not nodes.** The diameter of a single node is 0; of two nodes, 1. With
  `height(None) = 0`, `L + R` is already in edges. Adding 1 is the classic off-by-one.
- **`nonlocal best`.** Without it Python treats `best` as a new local the moment you
  assign it, and you get `UnboundLocalError`. (Or use `self.best`, or a one-element
  list.)
- **Return one arm, not both.** `return 1 + L + R` would let the parent build a path
  that forks, which isn't a path.
- **The function's return value is not the answer.** Say it on camera: `height(root)`
  returns 3 here by coincidence. On the second example it returns 4, the height of the
  tree, while the answer is also 4, also by coincidence. Different questions.

## 🎤 Interview talking points
- *"Any path bends at exactly one highest node. At that node its length is left height
  plus right height, so I compute that at every node and keep the max."*
- *"My recursion returns the height, because that's what the parent needs to extend a
  path, and records the diameter on the side. One pass, O(n)."*
- *"The path needn't pass through the root, which is why the answer is a running max
  and not the root's value."*
- *"It's the same shape as Max Path Sum: return one arm, record both."* ← name the
  family.

## 🔗 Transfer
EP139 returned a height. EP140 folded a verdict into the height. Today the answer moves
**out** of the return value entirely, into a global. Tomorrow, EP142 Check Completeness,
goes back to BFS for a question about **position** that DFS can't see. The split you
learned today returns in EP148 Maximum Path Sum, where negative arms mean you also have
to decide whether to take an arm at all.

## 📹 Metadata
- **Title:** `Diameter of a Binary Tree, return one arm, record both | Trees #21`
- **Thumbnail:** `L + R vs max(L, R)` (blue block)
- **Short:** the second example, the root answering 3 while `best` quietly holds 4. 45s.
