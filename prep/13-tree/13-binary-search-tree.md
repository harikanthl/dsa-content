# EP133 · P13E13 · Search in a Binary Search Tree   [Easy]

**Pattern:** Tree (Search) · **Link:** https://leetcode.com/problems/search-in-a-binary-search-tree/

---

## 🎬 Hook
> "Every tree problem so far has visited every node. This one visits **one node per
> level**, because a binary search tree tells you which way to go before you go.
> It's binary search from Pattern 10, with the array replaced by pointers."

## 📋 Problem, in your words
```
A binary search tree (BST): for every node, everything in its LEFT subtree
is smaller and everything in its RIGHT subtree is larger.

Given the root of a BST and a value, return the node that holds that value
(the subtree rooted there). If it isn't in the tree, return None.
```

## 🔢 The example
```
          4
         / \          Input:  root = [4, 2, 7, 1, 3], val = 2
        2   7         Output: [2, 1, 3]     (the subtree rooted at 2)
       / \
      1   3           Input:  val = 5
                      Output: []            (5 would be 7's left child: not there)
```

## 🧸 ELI5
> A choose-your-own-adventure book where every page says: *"If your number is smaller
> than 4, turn to the left page. If bigger, turn to the right page."*
>
> Looking for 2? Page 4 says go left. Page 2: found it. Two pages, done.
>
> Looking for 5? Page 4 says go right. Page 7 says go left. The left page is **blank**.
> 5 isn't in the book, and you know that without reading any other page, because if 5
> existed it could only have been there.

## 🐌 Brute force (say it, don't type it)
Any traversal from EP121 to EP124 that checks every node: **O(n)**. It ignores the one
thing a BST gives you. With the ordering, each comparison throws away an entire
subtree, so it's **O(h)**: O(log n) on a balanced tree.

## 💡 The pattern reveal
**Signal:** "binary **search** tree" + find / insert / exists.
**Therefore:** Shape E, the one-branch walk. No recursion into both sides, ever.

```python
node = root
while node and node.val != val:
    node = node.left if val < node.val else node.right
return node          # the match, or None if we walked off the tree
```

**Key insight:** the loop ends for exactly two reasons, and **both** are handled by
`return node`: we found it (`node.val == val`) or we fell off (`node is None`). No
separate "not found" branch.

**Insert** (LeetCode 701, the other half of this episode) is the same walk. The place
you fall off the tree is exactly where the new value belongs.

```python
def insert(node, val):
    if not node:
        return TreeNode(val)             # fell off: this is the spot
    if val < node.val:
        node.left = insert(node.left, val)
    else:
        node.right = insert(node.right, val)
    return node
```

## 🔍 Dry run: search `val = 5` in `[4, 2, 7, 1, 3]`

| step | `node` | compare | move |
|---|---|---|---|
| 1 | 4 | 5 > 4 | right → 7 |
| 2 | 7 | 5 < 7 | left → None |
| 3 | None | loop ends | **return None** ✓ |

Three steps; 2, 1 and 3 were never looked at. And insert 5 follows the same path and
hangs the new node at step 2's empty left: `[4, 2, 7, 1, 3, 5]`.

## ✅ Optimal solution
```python
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Walk one branch: left if smaller, right if bigger.

        Time:  O(h), one node per level; O(log n) balanced, O(n) skewed.
        Space: O(1), iterative.
        """
        node = root
        while node and node.val != val:
            node = node.left if val < node.val else node.right
        return node                         # the match, or None if we fell off
```
**Time:** O(h) · **Space:** O(1)

## ⚠️ Gotchas
- **O(h) is not O(log n).** Insert 1, 2, 3, 4, 5 in order and the "tree" is a linked
  list: h = n. Balanced trees (AVL, red-black) exist to keep h at log n. Say "O(h), log
  n if balanced".
- **Return the node, not `True`.** LeetCode wants the subtree.
- **Check `node` before `node.val`** in the loop condition. `while node.val != val and
  node` crashes when you fall off.
- **Insert must reattach.** `insert(node.left, val)` without `node.left = ...` creates
  the new node and throws it away.

## 🎤 Interview talking points
- *"In a BST every comparison rules out a whole subtree, so I only walk one path: O(h)
  time, O(1) space iteratively."*
- *"h is log n if balanced and n if skewed, which is why self-balancing trees exist."*
- *"Insert is the same walk; where search falls off is where insert attaches."*
- *"It's binary search. The midpoint is the root; left and right halves are the
  subtrees."* ← the connection to Pattern 10.

## 🔗 Transfer
The one-branch walk comes straight back tomorrow in EP134, LCA of a BST: same loop,
but it stops when p and q **stop going the same way**. The other big BST fact, inorder
is sorted, drives EP136 Two Sum IV and EP137 Kth Smallest.

## 📹 Metadata
- **Title:** `Search a BST, one branch per level | Trees #13`
- **Thumbnail:** `O(h), not O(n)`
- **Short:** looking for 5, two turns, a blank page. 30s.
