# EP150 · P13E30 · Construct Binary Tree from Inorder and Postorder Traversal   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

---

## 🎬 Hook
> "Yesterday the root was the **first** thing in preorder. Postorder visits the root
> **last**, so the root is at the end. Read postorder **backwards** and it goes root,
> right, left. Which means if you eat it from the back one value at a time, you **must**
> build the right subtree before the left. Get that order wrong and the code crashes."

## 📋 Problem, in your words
```
Given the inorder and postorder traversals of a binary tree,
build and return the tree.

  - values are UNIQUE
  - note the argument order on LeetCode: (inorder, postorder)
```

## 🔢 The example
```
Input:  inorder   = [9, 3, 15, 20, 7]
        postorder = [9, 15, 7, 20, 3]
Output: [3,9,20,null,null,15,7]

          3
         / \
        9   20
           /  \
          15   7

Input:  inorder = [-1], postorder = [-1]  ->  [-1]
```

## 🧸 ELI5
> Same two witnesses as yesterday, but the first one now describes the family photo
> **boss last**: "the left group, then the right group, then 3 is in charge."
>
> So read that witness **from the end**: 3 (the boss), then 20 (the boss of the right
> group), then 7, then 15, then 9.
>
> ```
> postorder:          9   15   7   20   3
> reading backwards:  3   20   7   15   9
>                     ^   \_________/   ^
>                   root  right group   left group
> ```
>
> Reading backwards, the right group comes **before** the left group. So when you hand
> out names from the back of the list, the right side has to be built first, or it'll
> get the left side's names.

## 🐌 Brute force (say it, don't type it)
`inorder.index(root)` and sliced lists at every call. **O(n²)**, same as EP149's brute
force, for the same two reasons: linear searches and copies. The hash map fixes both.

## 💡 The pattern reveal
**Signal:** "construct from postorder and inorder".
**Therefore:** Shape G, the mirror of EP149. The pattern card: *`postorder[-1]` is the
root; build right first.*

**Two ways to write it:**

| version | how postorder is consumed | build order |
|---|---|---|
| index ranges (EP149's shape) | `postorder[post_hi]` is the root; carve with `left_size` | either order works |
| **one pointer from the end (today)** | a single `post_i` walks backwards | **right first, mandatory** |

Today uses the pointer version, because it's shorter and because it makes the pattern
card's rule *visible*: backwards postorder is **root, right, left**, so the recursion
must consume in that order.

**Key insight:** with a single pointer, the recursion *is* a reverse-postorder walk. The
inorder range tells each call whether it's empty; the pointer tells it what its root
is. You don't need `left_size` at all.

```python
root = TreeNode(postorder[post_i]); post_i -= 1
mid = idx[root.val]
root.right = rec(mid + 1, in_hi)     # FIRST: the next values from the back are the right subtree's
root.left  = rec(in_lo, mid - 1)
```

## 🔍 Dry run

`idx = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}`, `post_i` starts at 4. Calls are
`rec(in_lo, in_hi)`.

| step | call | inorder range | root = `postorder[post_i]` | `mid` | `post_i` after | next |
|---|---|---|---|---|---|---|
| 1 | `rec(0, 4)` | `[9,3,15,20,7]` | **3** | 1 | 3 | right: `rec(2, 4)` |
| 2 | `rec(2, 4)` | `[15,20,7]` | **20** | 3 | 2 | right: `rec(4, 4)` |
| 3 | `rec(4, 4)` | `[7]` | **7** | 4 | 1 | both children empty |
| 4 | back in 20 | - | - | - | 1 | left: `rec(2, 2)` |
| 5 | `rec(2, 2)` | `[15]` | **15** | 2 | 0 | both children empty |
| 6 | back in 3 | - | - | - | 0 | left: `rec(0, 0)` |
| 7 | `rec(0, 0)` | `[9]` | **9** | 0 | −1 | both children empty |

Result: 3 → (9, 20 → (15, 7)) ✓. The roots were taken in the order 3, 20, 7, 15, 9:
postorder read backwards.

**Swap the two lines** (left first) and step 2 becomes `rec(0, 0)` taking **20** as the
root of the range `[9]`. `idx[20] = 3` is outside that range, the recursion spirals
into nonsense, `post_i` runs past 0 into negative indices (which Python silently wraps),
and it dies with `IndexError: list index out of range`.

## ✅ Optimal solution
```python
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        """Rebuild a tree by reading postorder backwards: root, right, left.

        Time:  O(n), each value becomes a node once; index lookups are O(1).
        Space: O(n) for the index map, plus O(h) recursion.
        """
        idx = {v: i for i, v in enumerate(inorder)}
        post_i = len(postorder) - 1             # next root, consumed from the back

        def rec(in_lo: int, in_hi: int) -> Optional[TreeNode]:
            nonlocal post_i
            if in_lo > in_hi:
                return None                     # no values in this range
            root = TreeNode(postorder[post_i])
            post_i -= 1
            mid = idx[root.val]

            root.right = rec(mid + 1, in_hi)    # right FIRST: backwards postorder
            root.left = rec(in_lo, mid - 1)     # is root, right, left
            return root

        return rec(0, len(inorder) - 1)
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **Right before left.** Only in the one-pointer version, and it's not optional. The
  crash in the dry run is what happens otherwise.
- **`nonlocal post_i`.** It's an int being reassigned inside a nested function. Without
  `nonlocal`, `UnboundLocalError`.
- **Argument order.** LeetCode's signature is `buildTree(inorder, postorder)`, the
  opposite of EP149's `(preorder, inorder)`. Swapping them builds a wrong tree with no
  error.
- **If you use EP149's range version**, the root is `postorder[post_hi]`, the left
  subtree is `postorder[post_lo : post_lo + left_size]`, and the right is the rest
  *minus the last element*. Forgetting `post_hi - 1` puts the root in its own right
  subtree.
- **Unique values required**, same as EP149.

## 🎤 Interview talking points
- *"Postorder ends with the root, so reading it backwards gives root, right subtree,
  left subtree. I consume it with one pointer from the back, split inorder around each
  root, and build the right subtree first so the pointer lines up."*
- *"Hash map for inorder positions, so it's O(n) overall."*
- *"The same idea works for EP149 with a pointer from the front: preorder is root, left,
  right, so there you build left first."* ← shows you see both as one algorithm.

## 🔗 Transfer
EP149 and EP150 are one algorithm: find the root in the traversal that names roots,
split the inorder around it. Tomorrow, EP151 Sorted Array to BST, removes the second
traversal: a sorted array is an inorder with no root information at all, so **you
choose** the root, the middle, and the same split-and-recurse builds a balanced tree.

## 📹 Metadata
- **Title:** `Build a Tree from Postorder + Inorder, why right comes first | Trees #30`
- **Thumbnail:** `RIGHT FIRST` (orange block)
- **Short:** the backwards postorder `3 20 7 15 9`, then the crash when left goes first.
  45s.
