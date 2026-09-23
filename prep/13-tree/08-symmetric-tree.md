# EP128 · P13E08 · Symmetric Tree   [Easy]

**Pattern:** Tree (Mirror and Symmetry) · **Link:** https://leetcode.com/problems/symmetric-tree/description/

---

## 🎬 Hook
> "Is this tree its own mirror image? You can't answer it by looking at one node at a
> time, because the thing on the far left has to match the thing on the far right. So
> walk **two pointers** through the tree at once, and **cross the wires**: left goes
> with right, right goes with left."

## 📋 Problem, in your words
```
Given the root of a binary tree, return True if it's symmetric around
its centre line: the left subtree is a mirror image of the right subtree.

Values AND shape must mirror. An empty tree is symmetric.
```

## 🔢 The example
```
          1                         1
        /   \                     /   \
       2     2                   2     2
      / \   / \                   \     \
     3   4 4   3                   3     3

Input:  [1,2,2,3,4,4,3]          Input:  [1,2,2,null,3,null,3]
Output: True                     Output: False
                                 Why:    the 3s are both RIGHT children;
                                         a mirror needs one left, one right
```

## 🧸 ELI5
> Fold a sheet of paper down the middle, with the tree drawn on it. If every blob lands
> on another blob with the same number, it's symmetric.
>
> When you fold, the **outside** edges meet (far left meets far right) and the
> **inside** edges meet (the two in the middle). So you compare:
>
> ```
> outer pair: left's LEFT  with right's RIGHT     3 and 3
> inner pair: left's RIGHT with right's LEFT      4 and 4
> ```
>
> That's the cross-wiring. Then do the same fold one level lower, on each pair.

## 🐌 Brute force (say it, don't type it)
Copy the tree, invert the copy with EP127, and run Same Tree (EP129) on the original
and the copy. **O(n)** time but **O(n)** extra space for the copy, and three functions
where one will do. It's a great way to *explain* the problem ("symmetric means equal to
its own inverse"), and then you do it without building anything.

## 💡 The pattern reveal
**Signal:** "symmetric", "mirror of itself".
**Therefore:** Shape C, two trees in lockstep, with the recursive calls **cross-wired**.

```python
def mirror(a, b):
    if not a and not b: return True          # both empty: fine
    if not a or not b:  return False         # exactly one empty: shape differs
    return (a.val == b.val
            and mirror(a.left,  b.right)     # outer pair
            and mirror(a.right, b.left))     # inner pair
```

called as `mirror(root.left, root.right)`.

Compare with EP129 Same Tree: identical except the calls are `(a.left, b.left)` and
`(a.right, b.right)`. **One wiring change turns "same" into "mirror".**

## 🔍 Dry run: `[1, 2, 2, 3, 4, 4, 3]`

Call it as `mirror(L2, R2)`, where L2 and R2 are the two 2s.

| step | call | both empty? | one empty? | values | next |
|---|---|---|---|---|---|
| 1 | `mirror(L2, R2)` | no | no | 2 = 2 ✓ | outer pair |
| 2 | `mirror(3, 3)` (L2.left, R2.right) | no | no | 3 = 3 ✓ | its children |
| 3 | `mirror(None, None)` ×2 | **yes** → True | | | back to step 1 |
| 4 | `mirror(4, 4)` (L2.right, R2.left) | no | no | 4 = 4 ✓ | children all None → True |
| 5 | step 1 has `True and True and True` | | | | **True** ✓ |

On `[1, 2, 2, null, 3, null, 3]`: step 2 is `mirror(L2.left, R2.right)` =
`mirror(None, 3)`. Both empty? No. One empty? **Yes → False**, and `and`
short-circuits the rest.

## ✅ Optimal solution
```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        """True if the left subtree is a mirror image of the right subtree.

        Time:  O(n), each node is compared once.
        Space: O(h) for the recursion stack.
        """
        def mirror(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if not a and not b:
                return True             # both empty
            if not a or not b:
                return False            # exactly one empty
            return (a.val == b.val
                    and mirror(a.left, b.right)     # outside pair
                    and mirror(a.right, b.left))    # inside pair

        return mirror(root.left, root.right) if root else True
```
**Time:** O(n) · **Space:** O(h)

Iterative, if asked: a queue of **pairs**. Seed it with `(root.left, root.right)`; pop
a pair, apply the same three checks, push `(a.left, b.right)` and `(a.right, b.left)`.

## ⚠️ Gotchas
- **The two null checks, in that order.** "Both empty" first, then "one empty". Swap
  them and `mirror(None, None)` returns False. Skip the second and `a.val` crashes.
- **Cross the wires.** `mirror(a.left, b.left)` is Same Tree, and it passes
  `[1, 2, 2]` (so the bug hides) and fails `[1,2,2,3,4,4,3]`.
- **Compare `root.left` with `root.right`**, not `root` with `root`. `mirror(root, root)`
  also works but does every comparison twice.
- **Values alone aren't enough.** Level order `[1,2,2,null,3,null,3]` reads 2,2 and
  3,3 per level but the shapes don't mirror. The null checks are what catch shape.

## 🎤 Interview talking points
- *"Symmetric means the left subtree mirrors the right. I walk both at once: outer pair
  `(a.left, b.right)`, inner pair `(a.right, b.left)`."*
- *"Two base cases: both empty is True, one empty is False. Then compare values."*
- *"It's Same Tree with the recursive calls cross-wired."* ← the pattern-level sentence.
- *"O(n) time, O(h) space; iteratively, a queue of pairs."*

## 🔗 Transfer
Yesterday, EP127, *built* the mirror. Today we checked for one without building it.
Tomorrow's homework, EP129 Same Tree, is today's function with the wires straightened,
and then EP130 runs that function at every node of a bigger tree.

## 📹 Metadata
- **Title:** `Symmetric Tree, cross the wires | Trees #8`
- **Thumbnail:** `left ↔ right` (X-shaped arrows)
- **Short:** the paper fold: outer pair, inner pair, one level down. 40s.
