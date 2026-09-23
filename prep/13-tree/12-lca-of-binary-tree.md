# EP132 · P13E12 · Lowest Common Ancestor of a Binary Tree   [Medium]

**Pattern:** Tree (Search) · **Link:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/

---

## 🎬 Hook
> "Find the lowest node that has both p and q underneath it. The solution is six lines,
> and each call only ever answers one question: **'did you find anything down there?'**
> If the left says yes and the right says yes, you're standing on the answer."

## 📋 Problem, in your words
```
Given a binary tree and two nodes p and q that are both in it, return
their lowest common ancestor: the deepest node that has BOTH p and q
in its subtree.

A node counts as its own descendant, so if p is above q, the answer is p.
All values are unique. p and q are guaranteed to exist.
```

## 🔢 The example
```
              3
           /     \
          5       1           p = 5, q = 1  ->  3    (split at the root)
         / \     / \          p = 5, q = 4  ->  5    (5 is above 4)
        6   2   0   8         p = 6, q = 4  ->  5    (6 is left of 5, 4 is right)
           / \
          7   4
Input:  root = [3,5,1,6,2,0,8,null,null,7,4]
```

## 🧸 ELI5
> Two cousins, p and q, at a huge family reunion. Who is the **closest** relative they
> both descend from?
>
> Everyone asks both of their children the same question: *"is p or q somewhere in
> your family?"* Each child answers with a name, or "nobody".
>
> - If **both** children name someone, p is down one side and q down the other. **You**
>   are where their lines meet. Say your own name.
> - If only one child names someone, pass that name up unchanged.
> - If you **are** p or q, say your own name straight away. You don't even need to ask
>   your children: if the other one is below you, you're the answer anyway.

## 🐌 Brute force (say it, don't type it)
Find the root-to-p path and the root-to-q path (two DFS with backtracking), then walk
both lists together until they differ. The last shared node is the LCA. **O(n)** time
too, but **O(n)** space for the paths and three passes. It's the best way to *explain*
LCA ("where the two paths split"), and then the recursive version does it in one pass
without storing paths.

## 💡 The pattern reveal
**Signal:** "lowest common ancestor", "deepest node containing both".
**Therefore:** Shape F. Bottom-up, and each call returns **a node or `None`**.

```python
def lca(node, p, q):
    if not node or node is p or node is q:
        return node                      # empty, or found one of them
    L = lca(node.left, p, q)
    R = lca(node.right, p, q)
    if L and R:
        return node                      # one on each side: THIS is the split
    return L or R                        # both on one side (or none): pass it up
```

**Key insight:** the return value means different things at different heights, and
that's fine. Below the split, it means "I found p (or q) here". At the split, it
becomes "here's the LCA", and from there it simply passes up unchanged because the
other side returns `None`.

| `L` | `R` | meaning | return |
|---|---|---|---|
| node | node | p and q on different sides | **`node`** (the answer) |
| node | None | everything found is on the left | `L` |
| None | node | everything found is on the right | `R` |
| None | None | neither is down here | `None` |

## 🔍 Dry run: `p = 6`, `q = 4`

| step | call at | early return? | L | R | returns |
|---|---|---|---|---|---|
| 1 | 6 | **is p** | | | 6 |
| 2 | 7 | no; children None | None | None | None |
| 3 | 4 | **is q** | | | 4 |
| 4 | 2 | no | None (from 7) | 4 | 4 |
| 5 | 5 | no | 6 | 4 | **5** (both sides) |
| 6 | 0 | no | None | None | None |
| 7 | 8 | no | None | None | None |
| 8 | 1 | no | None | None | None |
| 9 | 3 | no | 5 | None | **5** ✓ |

Row 5 is the split. Row 9 shows the answer passing up through the root untouched,
because the right side found nothing.

## ✅ Optimal solution
```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """Deepest node with both p and q in its subtree.

        Time:  O(n), every node visited at most once.
        Space: O(h) for the recursion stack.
        """
        if not root or root is p or root is q:
            return root                     # nothing here, or found one of them
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root                     # p and q split here
        return left or right                # pass up whatever was found
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Returning early at p means you never search under p.** That's correct *because*
  both nodes are guaranteed to exist: if q were under p, p is the answer anyway. If the
  problem didn't guarantee existence, this would wrongly return p when q is missing.
  That's LeetCode 1644, the follow-up.
- **`is`, not `==`.** p and q are node objects. With unique values `==` on `.val` also
  works, but compare nodes to nodes.
- **`return left or right`** handles three rows of the table at once. Don't write four
  `if`s.
- **This is not a BST.** Don't compare values to decide which way to go. That shortcut
  is EP134.

## 🎤 Interview talking points
- *"Each call returns p, q, the LCA, or None. If both children return something, p and
  q are on different sides, so this node is the lowest point that sees both."*
- *"If the current node is p or q, I return it immediately; with both guaranteed
  present, that's already the answer if the other is below."*
- *"O(n) time, O(h) space, one pass, no stored paths."*
- *"If p or q might be missing, I'd track whether each was actually found and only
  trust the answer if both were."*

## 🔗 Transfer
This is the general LCA. EP134 does it on a **BST**, where the values tell you which
way to go, so there's no need to search both sides: O(h), no recursion. EP135 LCA of
Deepest Leaves returns a pair `(depth, node)` instead of a node, the same "combine the
two children's answers" idea with more information travelling up.

## 📹 Metadata
- **Title:** `Lowest Common Ancestor, "did you find anything down there?" | Trees #12`
- **Thumbnail:** `L and R → ME`
- **Short:** 6 and 4 bubbling up and meeting at 5. 45s.
