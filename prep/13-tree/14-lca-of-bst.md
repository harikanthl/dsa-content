# EP134 · P13E14 · Lowest Common Ancestor of a Binary Search Tree   [Medium]

**Pattern:** Tree (Search) · **Link:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/

---

## 🎬 Hook
> "Two episodes ago, finding the lowest common ancestor meant searching the whole
> tree. In a BST you don't search at all. **Walk down from the root while p and q
> want to go the same way. The first node where they disagree is the answer.**"

## 📋 Problem, in your words
```
Given a BST and two nodes p and q in it, return their lowest common
ancestor: the deepest node that has both in its subtree
(a node counts as its own descendant).

Values are unique; p and q both exist.
```

## 🔢 The example
```
                6
             /     \
            2       8          p = 2, q = 8  ->  6   (they split at the root)
           / \     / \         p = 2, q = 4  ->  2   (2 is above 4)
          0   4   7   9        p = 3, q = 5  ->  4
             / \
            3   5
Input:  root = [6,2,8,0,4,7,9,null,null,3,5]
```

## 🧸 ELI5
> Two friends are walking down from the top of a hill to two different houses, and at
> every fork there's a sign: *"smaller numbers left, bigger numbers right"*.
>
> As long as both houses are on the same side, they walk together. The first fork
> where one needs to go left and the other right, they split up. **That fork is their
> lowest common ancestor.** Also, if one friend's house is **at** the fork, that's the
> answer too: the other friend is somewhere beyond it.

## 🐌 Brute force (say it, don't type it)
Use EP132's general LCA, which ignores the ordering and may visit every node: **O(n)**
time, O(h) stack. Correct, and it wastes the BST property. With it, you only ever
walk one path: **O(h)** time, **O(1)** space.

## 💡 The pattern reveal
**Signal:** "lowest common ancestor" + "binary **search** tree".
**Therefore:** Shape F's BST variant: compare and walk, like EP133.

```python
node = root
while node:
    if p.val < node.val and q.val < node.val:
        node = node.left                 # both smaller: the split is further left
    elif p.val > node.val and q.val > node.val:
        node = node.right                # both bigger: the split is further right
    else:
        return node                      # they disagree, or one IS this node
```

**Key insight:** the `else` covers three situations in one branch, and all three mean
"this is the answer":

| situation | why it's the LCA |
|---|---|
| p < node < q (or the other way round) | they go different ways from here |
| p is node | q is below p, so p is the lowest node containing both |
| q is node | same, the other way round |

## 🔍 Dry run: `p = 3`, `q = 5`

| step | `node` | p=3 vs node | q=5 vs node | move |
|---|---|---|---|---|
| 1 | 6 | smaller | smaller | both left → 2 |
| 2 | 2 | bigger | bigger | both right → 4 |
| 3 | 4 | smaller | bigger | **disagree → return 4** ✓ |

Three nodes looked at, out of nine. Now `p = 2`, `q = 4`: step 1 at 6, both smaller,
go left. Step 2 at 2: p is **equal**, neither "both smaller" nor "both bigger", so
`else` → return 2 ✓.

## ✅ Optimal solution
```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """Walk down while p and q are on the same side; stop where they split.

        Time:  O(h), one node per level.
        Space: O(1), no recursion.
        """
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left            # both in the left subtree
            elif p.val > node.val and q.val > node.val:
                node = node.right           # both in the right subtree
            else:
                return node                 # split point, or node is p or q
        return None                         # unreachable when p and q exist
```
**Time:** O(h) · **Space:** O(1)

## ⚠️ Gotchas
- **Strict comparisons.** `<` and `>`, not `<=`/`>=`. With `<=`, when node **is** p you
  keep walking past it and miss the answer.
- **Don't assume p < q.** The two `and` conditions work whichever is smaller. Swapping
  them first is harmless but unnecessary.
- **O(h), not O(log n)**, for the same reason as EP133: a skewed BST has h = n.
- **Don't reach for EP132's code.** It's correct here but loses the whole point of the
  episode. If an interviewer says "BST", they're asking for this.

## 🎤 Interview talking points
- *"In a BST the values tell me which side p and q are on. While both are smaller I
  go left, while both are bigger I go right. The first node where that stops being true
  is the LCA."*
- *"That includes the case where the node is p or q itself."*
- *"O(h) time, O(1) space. EP132's general version would be O(n)."*

## 🔗 Transfer
EP132 (search everywhere) versus EP134 (walk one path) is the clearest example in the
pattern of **what the BST property buys you**. Tomorrow, EP135 LCA of Deepest Leaves,
goes back to a plain binary tree, and the recursion returns **two things at once**:
how deep, and which node.

## 📹 Metadata
- **Title:** `LCA of a BST, walk until they disagree | Trees #14`
- **Thumbnail:** `same way? keep going`
- **Short:** the two friends splitting at 4. 30s.
