# EP149 · P13E29 · Construct Binary Tree from Preorder and Inorder Traversal   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

---

## 🎬 Hook
> "Two lists of numbers, and you have to rebuild the tree they came from. Each list alone
> is hopeless. Together they're a lock and key: **preorder tells you who the root is**,
> and **inorder tells you who's on its left and who's on its right**. Do that once,
> recurse on both halves, and the tree falls out."

## 📋 Problem, in your words
```
Given the preorder and inorder traversals of a binary tree,
build and return the tree.

  - values are UNIQUE (this is what makes the answer unique)
  - both lists have the same length, 1 to 3000
```

## 🔢 The example
```
Input:  preorder = [3, 9, 20, 15, 7]
        inorder  = [9, 3, 15, 20, 7]
Output: [3,9,20,null,null,15,7]

          3
         / \
        9   20
           /  \
          15   7

Input:  preorder = [-1], inorder = [-1]  ->  [-1]
```

## 🧸 ELI5
> Two witnesses describe a family photo.
>
> The **preorder** witness always names the **boss first**: "3 is in charge, then 3's
> left group, then 3's right group." The **inorder** witness names people **left to
> right as they stood**: "9, then 3, then 15, 20, 7."
>
> Preorder's first name, 3, is the boss. Find 3 in the inorder line: everyone standing
> to the **left** of 3 (just 9) is the left group; everyone to the **right** (15, 20, 7)
> is the right group.
>
> ```
> inorder:   [ 9 ]  3  [ 15  20  7 ]
>             left  ^      right
>                 root
> ```
>
> Now each group is a smaller family photo. Same trick. Keep going until the groups are
> empty.

## 🐌 Brute force (say it, don't type it)
The same recursion, but finding the root in inorder with `inorder.index(root_val)` and
passing **sliced** lists down: `preorder[1:1+k]`, `inorder[:k]`, and so on. Correct and
readable, and **O(n²)**: every `.index()` is a linear scan, and every slice copies. On a
skewed tree of 3000 nodes that's millions of wasted steps. The fix is a hash map and
index ranges instead of slices.

## 💡 The pattern reveal
**Signal:** "construct from preorder and inorder".
**Therefore:** Shape G, exactly as the pattern card writes it.

**Key insight:** three facts, used together.

| fact | why it's true | what you do with it |
|---|---|---|
| `preorder[0]` is the root | preorder visits the root **first** | make the node |
| in inorder, everything left of the root is the left subtree | inorder is left, root, right | `left_size = mid - in_lo` |
| in preorder, the root is followed by exactly `left_size` left-subtree values | preorder is root, **all** of left, **all** of right | carve preorder at `pre_lo + left_size` |

```
preorder: [ 3 | 9 | 20 15 7 ]        inorder: [ 9 | 3 | 15 20 7 ]
           root left  right                    left root  right
                 ^^^ left_size = 1 in both
```

`left_size` is the one number that translates between the two lists.

## 🔍 Dry run

`idx = {9: 0, 3: 1, 15: 2, 20: 3, 7: 4}`. Calls are `rec(pre_lo, pre_hi, in_lo, in_hi)`.

| step | call | root = `preorder[pre_lo]` | `mid` | `left_size` | left call | right call |
|---|---|---|---|---|---|---|
| 1 | `rec(0, 4, 0, 4)` | **3** | 1 | 1 | `rec(1, 1, 0, 0)` | `rec(2, 4, 2, 4)` |
| 2 | `rec(1, 1, 0, 0)` | **9** | 0 | 0 | `rec(2, 1, …)` → `None` | `rec(2, 1, …)` → `None` |
| 3 | `rec(2, 4, 2, 4)` | **20** | 3 | 1 | `rec(3, 3, 2, 2)` | `rec(4, 4, 4, 4)` |
| 4 | `rec(3, 3, 2, 2)` | **15** | 2 | 0 | `None` | `None` |
| 5 | `rec(4, 4, 4, 4)` | **7** | 4 | 0 | `None` | `None` |

Result: 3 with left 9 and right 20; 20 with left 15 and right 7 ✓. Every "`None`" is a
call where `pre_lo > pre_hi`: an empty range.

## ✅ Optimal solution
```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """Rebuild a tree: preorder names the root, inorder splits left from right.

        Time:  O(n), each value becomes a node once; index lookups are O(1).
        Space: O(n) for the index map, plus O(h) recursion.
        """
        idx = {v: i for i, v in enumerate(inorder)}     # value -> inorder position

        def rec(pre_lo: int, pre_hi: int, in_lo: int, in_hi: int) -> Optional[TreeNode]:
            if pre_lo > pre_hi:
                return None                             # empty range: no subtree
            root = TreeNode(preorder[pre_lo])           # preorder's first IS the root
            mid = idx[root.val]                         # where it stands in inorder
            left_size = mid - in_lo                     # how many are on its left

            root.left = rec(pre_lo + 1, pre_lo + left_size, in_lo, mid - 1)
            root.right = rec(pre_lo + left_size + 1, pre_hi, mid + 1, in_hi)
            return root

        return rec(0, len(preorder) - 1, 0, len(inorder) - 1)
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`left_size = mid - in_lo`, not `mid`.** `mid` is an index into the *whole* inorder
  list; in any right subtree, `in_lo` isn't 0. Using `mid` directly is right at the root
  and wrong one level down: on the example it carves preorder at the wrong place and
  crashes with `IndexError`.
- **Unique values are required.** With duplicates, `idx` can't tell which 3 is the root
  and the answer isn't unique. Say this as the stated assumption.
- **`.index()` + slicing is O(n²).** Fine to *say* as the first version; build the hash
  map before they ask.
- **Preorder + inorder, or postorder + inorder. Not preorder + postorder.** Without
  inorder you can't tell a lone left child from a lone right child: `[1,2]` preorder and
  `[2,1]` postorder fit both shapes.
- **Ranges are inclusive** here (`pre_hi = len - 1`), so the empty check is `lo > hi`.
  Mixing inclusive and exclusive bounds is the other off-by-one.

## 🎤 Interview talking points
- *"The first value in preorder is the root. Finding it in inorder splits the rest into
  left and right subtrees, and the size of the left part tells me where to split
  preorder too. Recurse on both halves."*
- *"I precompute a value-to-index map for inorder, so each split is O(1), and I pass
  index ranges instead of slicing, so the whole build is O(n)."*
- *"This needs unique values, and it needs inorder: preorder plus postorder alone is
  ambiguous for single-child nodes."*

## 🔗 Transfer
Every traversal from EP121–123 was a way of *reading* a tree. Today two of those
readings are enough to *write* one. Tomorrow, EP150, gets postorder instead of
preorder: the root moves to the **end**, and if you consume it from the back with a
single pointer, you're forced to build the **right** subtree first. EP151 then drops the
traversals entirely and **chooses** the root itself.

## 📹 Metadata
- **Title:** `Build a Tree from Preorder + Inorder, the lock and key | Trees #29`
- **Thumbnail:** `[ 9 ] 3 [ 15 20 7 ]` (blue block)
- **Short:** the inorder line splitting around 3, then around 20. 40s.
