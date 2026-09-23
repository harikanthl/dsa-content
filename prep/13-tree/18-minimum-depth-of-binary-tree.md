# EP138 · P13E18 · Minimum Depth of Binary Tree   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/minimum-depth-of-binary-tree/description/

---

## 🎬 Hook
> "Maximum depth is `1 + max(left, right)`. So minimum depth is `1 + min(left, right)`,
> right? **Wrong**, and the tree that proves it is a straight line of five nodes. Today
> the fix is to stop recursing and go level by level: the first leaf you meet is the
> answer, and you never look at the rest of the tree."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its minimum depth:
the number of NODES on the shortest path from the root down to a LEAF.

  - a leaf is a node with NO children
  - an empty tree has depth 0
```

## 🔢 The example
```
Input:  [3,9,20,null,null,15,7]
Output: 2

          3          depth 1
         / \
        9   20       depth 2   <- 9 is a leaf, stop here
           /  \
          15   7     depth 3

Input:  [2,null,3,null,4,null,5,null,6]
Output: 5

        2
         \
          3
           \
            4
             \
              5
               \
                6    <- the ONLY leaf. The root is not a leaf: it has a child.
```

## 🧸 ELI5
> You're at the top of a building with a lot of staircases, and you want the **nearest
> exit on the ground**. You don't walk every staircase to the bottom and compare. You
> send a person down every staircase **one floor at a time, all together**. The first
> person to reach an exit shouts, and that floor number is the answer.
>
> "One floor at a time, all together" is BFS. "First to shout wins" is why BFS gives the
> minimum without seeing the whole tree.
>
> And the trap: a landing with **one** staircase going down is not an exit. Only a
> landing with **no** stairs down is.

## 🐌 Brute force (say it, don't type it)
DFS every root-to-leaf path, record each leaf's depth, return the smallest. **O(n)**,
and actually fine asymptotically. What's wasteful: it walks the entire tree even when
there's a leaf at depth 2 and a million nodes below depth 3. The BFS version stops at
the first leaf.

## 💡 The pattern reveal
**Signal:** "**minimum** depth", the shortest distance from the root to something.
**Therefore:** BFS, Shape B. The pattern card's tell: *closest to the root* means BFS.

**Key insight:** BFS visits nodes in order of depth. So the **first leaf popped** is at
the minimum depth. Return right there.

**🧨 The trap, and why `1 + min(L, R)` fails:**

```python
# WRONG
def minDepth(node):
    if not node: return 0
    return 1 + min(minDepth(node.left), minDepth(node.right))
```

On the straight line `2 → 3 → 4 → 5 → 6`, node 2's left child is `None`, which returns
`0`, so `min(0, 4) = 0` and the answer comes out **1**. But node 2 isn't a leaf; a
missing child is not a path to a leaf. Max depth never hit this because `max` ignores
the 0. Min grabs it.

If you do want DFS, the fix is: *if one child is missing, you must go down the other.*

```python
if not node.left:  return 1 + minDepth(node.right)
if not node.right: return 1 + minDepth(node.left)
return 1 + min(minDepth(node.left), minDepth(node.right))
```

## 🔍 Dry run: `[3,9,20,null,null,15,7]`

| depth | queue at start of level | pop | leaf? | action |
|---|---|---|---|---|
| 1 | `[3]` | 3 | no (9, 20) | push 9, 20 |
| 2 | `[9, 20]` | 9 | **yes** | **return 2** |

Answer **2** ✓. Nodes 20, 15 and 7 are never popped.

Now the trap tree `[2,null,3,null,4,null,5,null,6]`:

| depth | queue | pop | leaf? | action |
|---|---|---|---|---|
| 1 | `[2]` | 2 | no (right = 3) | push 3 |
| 2 | `[3]` | 3 | no | push 4 |
| 3 | `[4]` | 4 | no | push 5 |
| 4 | `[5]` | 5 | no | push 6 |
| 5 | `[6]` | 6 | **yes** | **return 5** |

Answer **5** ✓. BFS never has the `None`-returns-0 problem, because it only asks "is
this node a leaf?" about nodes that exist.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        """Nodes on the shortest root-to-leaf path, by BFS: first leaf wins.

        Time:  O(n) worst case, but stops at the shallowest leaf.
        Space: O(w), the widest level held in the queue.
        """
        if not root:
            return 0

        queue, depth = deque([root]), 1
        while queue:
            for _ in range(len(queue)):         # exactly the nodes on this level
                node = queue.popleft()
                if not node.left and not node.right:
                    return depth                # first leaf is the shallowest
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            depth += 1
```
**Time:** O(n) · **Space:** O(w)

## ⚠️ Gotchas
- **A leaf has no children, both.** A node with one child is not a leaf. This single
  definition is the entire problem.
- **`1 + min(L, R)` is wrong** whenever a node has exactly one child. Test the straight
  line; it's the example that fails.
- **Empty tree returns 0**, and it has to be checked before `deque([root])`, or you pop
  `None` and crash on `.left`.
- **Depth counts nodes, not edges.** A single node has depth 1. (Diameter, EP141, counts
  edges. Don't mix them.)
- **Read `len(queue)` once per level.** That's what the `for _ in range(len(queue))` is
  for. Without it you can't tell which level you're on.

## 🎤 Interview talking points
- *"Minimum depth is a shortest-distance question, so BFS: the first leaf I pop is the
  answer, and I can stop without seeing the rest of the tree."*
- *"The tempting recursion, 1 plus min of the children, is wrong for a node with one
  child: the missing side returns 0 and wins the min, but it isn't a leaf."* ← say this
  unprompted. It's why the problem is asked.
- *"DFS works if I handle the one-child case explicitly, but it always visits every
  node. BFS stops early on bushy trees with a shallow leaf."*

## 🔗 Transfer
EP124 Level Order built the BFS loop; today it gets an early exit. Tomorrow, EP139
Maximum Depth, flips everything: **max** needs every leaf, so there's no early exit and
BFS loses its edge, and the three-line bottom-up recursion becomes the template for the
rest of the Validation group. The "first time BFS reaches it is the shortest" idea comes
back as the engine of EP163 Shortest Path in a Non-Weighted Graph.

## 📹 Metadata
- **Title:** `Minimum Depth, why 1 + min() is a trap | Trees #18`
- **Thumbnail:** `min() LIES` (red block)
- **Short:** the straight-line tree, `1 + min` returning 1, then BFS walking down to 5. 45s.
