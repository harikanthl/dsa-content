# EP135 · P13E15 · Lowest Common Ancestor of Deepest Leaves   [Medium]

**Pattern:** Tree (Search) · **Link:** https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/description/

---

## 🎬 Hook
> "Find the lowest node that contains every one of the deepest leaves. You could find
> the depth first, then collect the leaves, then run LCA on all of them. Or you could
> have every node hand its parent **two numbers at once**, how deep it goes and which
> node wins, and get it in one pass."

## 📋 Problem, in your words
```
Given the root of a binary tree, find the deepest leaves (the nodes at the
maximum depth). Return the lowest node that has ALL of them in its subtree.

If there's only one deepest leaf, the answer is that leaf itself.
(Same problem as LeetCode 865, "Smallest Subtree with all the Deepest Nodes".)
```

## 🔢 The example
```
              3
           /     \
          5       1           Input:  [3,5,1,6,2,0,8,null,null,7,4]
         / \     / \          Output: 2
        6   2   0   8         Why:    deepest leaves are 7 and 4 (depth 3);
           / \                        2 is the lowest node holding both
          7   4

Input:  [1]              Output: 1
Input:  [0, 1, 3, null, 2]    Output: 2   (one deepest leaf: itself)
```

## 🧸 ELI5
> A company org chart. The CEO asks: *"who's the lowest-ranked manager who has
> **every one** of our most junior employees reporting up to them?"*
>
> Every manager asks both of their direct reports two things: *"how many levels are
> under you, and who's your answer?"*
>
> - If both sides report the **same** depth, the most junior people are split between
>   them. So **I'm** the answer.
> - If one side is deeper, all the most junior people are over there. Pass that side's
>   answer up, one level deeper.

## 🐌 Brute force (say it, don't type it)
Pass 1: find the max depth. Pass 2: collect every leaf at that depth. Pass 3: fold
EP132's LCA over them pairwise. Each LCA is O(n), and there can be O(n) deepest
leaves, so up to **O(n²)**. Even the smart two-pass version (BFS for the last level,
then one LCA that tracks a whole set) is fiddly. The one-pass pair is simpler.

## 💡 The pattern reveal
**Signal:** "deepest", "lowest common ancestor", a combination of depth and LCA.
**Therefore:** Shape D wearing Shape F's hat. Bottom-up, return a **pair**.

```python
def dfs(node):
    if not node:
        return 0, None                   # depth 0, no answer
    ld, ln = dfs(node.left)
    rd, rn = dfs(node.right)
    if ld == rd:
        return ld + 1, node              # deepest leaves on both sides (or I'm a leaf)
    if ld > rd:
        return ld + 1, ln                # all the deepest are on the left
    return rd + 1, rn                    # all the deepest are on the right
```

**Key insight:** the depth alone decides everything. If the two sides are equally deep,
the deepest leaves exist on **both** sides, so this node is the lowest one covering
them. A leaf is a special case of that: both children report depth 0, equal, so a leaf
names itself.

## 🔍 Dry run: `[3,5,1,6,2,0,8,null,null,7,4]`

Postorder, children before parents. `(d, n)` = (depth of this subtree, answer node).

| step | node | left `(d, n)` | right `(d, n)` | rule | returns |
|---|---|---|---|---|---|
| 1 | 6 | (0, None) | (0, None) | equal | (1, **6**) |
| 2 | 7 | (0, None) | (0, None) | equal | (1, 7) |
| 3 | 4 | (0, None) | (0, None) | equal | (1, 4) |
| 4 | 2 | (1, 7) | (1, 4) | **equal** | (2, **2**) |
| 5 | 5 | (1, 6) | (2, 2) | right deeper | (3, 2) |
| 6 | 0 | - | - | leaf | (1, 0) |
| 7 | 8 | - | - | leaf | (1, 8) |
| 8 | 1 | (1, 0) | (1, 8) | equal | (2, 1) |
| 9 | 3 | (3, 2) | (2, 1) | left deeper | (4, **2**) ✓ |

Row 5 is the teaching moment: 5 has a leaf on each side (6 and 2's subtree), but the
right side is **deeper**, so 5 is not the answer. 2 is carried up.

## ✅ Optimal solution
```python
class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """Lowest node containing every deepest leaf, in one postorder pass.

        Time:  O(n), every node visited once.
        Space: O(h) for the recursion stack.
        """
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if not node:
                return 0, None
            left_depth, left_ans = dfs(node.left)
            right_depth, right_ans = dfs(node.right)
            if left_depth == right_depth:
                return left_depth + 1, node         # deepest leaves on both sides
            if left_depth > right_depth:
                return left_depth + 1, left_ans     # all of them are on the left
            return right_depth + 1, right_ans       # all of them are on the right

        return dfs(root)[1]
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Return the depth + 1, not the child's depth.** Forgetting the `+ 1` makes every
  node look as deep as its child and the comparisons stop meaning anything.
- **Equal depths → return `node`, not a child's answer.** Returning `left_ans` on a tie
  gives the LCA of the left half only.
- **Not the same as EP132.** There's no p and q; the "targets" are defined by depth,
  which is only known once the children report. That's why the depth has to travel up
  alongside the node.
- **`Tuple` needs importing** (`from typing import Tuple`) outside LeetCode, or annotate
  with `tuple[int, ...]` on Python 3.9+.

## 🎤 Interview talking points
- *"Each call returns the depth of its subtree and the answer for that subtree. Equal
  depths mean the deepest leaves are on both sides, so this node is the answer;
  otherwise I pass up the deeper side's answer."*
- *"One postorder pass, O(n), no separate depth computation."*
- *"It's the bottom-up template from Max Depth with an LCA riding along."*

## 🔗 Transfer
The idea "return two things and let the parent combine them" is the backbone of the
Validation family: EP140 Balanced returns a height that doubles as a verdict, EP141
Diameter returns one arm and records two. Tomorrow, EP136 Two Sum IV, is a change of
pace: turn the BST into a sorted list and reuse Pattern 01.

## 📹 Metadata
- **Title:** `LCA of Deepest Leaves, return two things at once | Trees #15`
- **Thumbnail:** `(depth, node)`
- **Short:** row 5, the node with leaves on both sides that still isn't the answer. 45s.
