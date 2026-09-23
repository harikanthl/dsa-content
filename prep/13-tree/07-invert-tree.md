# EP127 · P13E07 · Invert Binary Tree   [Easy]

**Pattern:** Tree (Mirror and Symmetry) · **Link:** https://leetcode.com/problems/invert-binary-tree/description/

---

## 🎬 Hook
> "The most famous tree problem on the internet is three lines long. The only way to
> get it wrong is to write it as **two** lines where it should be **one**, and I'll
> show you the version that silently drops half the tree."

## 📋 Problem, in your words
```
Given the root of a binary tree, mirror it: at EVERY node, swap the
left and right children. Return the root.

The same TreeNode objects are rearranged; nothing new is created.
An empty tree returns None.
```

## 🔢 The example
```
Input:  [4, 2, 7, 1, 3, 6, 9]          Output: [4, 7, 2, 9, 6, 3, 1]

         4                                   4
       /   \                               /   \
      2     7          ── mirror ──>      7     2
     / \   / \                           / \   / \
    1   3 6   9                         9   6 3   1

Input:  [2, 1, 3]  ->  [2, 3, 1]
Input:  []         ->  []
```

## 🧸 ELI5
> Hold the tree up to a mirror. Everything on the left is now on the right, and it's
> not just the top: the left part's **own** left and right are swapped too, all the way
> down.
>
> How do you mirror a whole tree? Ask each child to mirror **itself**, then swap them.
> A leaf mirrored is just itself. An empty spot mirrored is still empty. Trust the
> smaller call (the reflex from Pattern 12) and there's nothing else to it.

## 🐌 Brute force (say it, don't type it)
Build a brand new mirrored tree node by node. That's **O(n)** too, but it allocates n
new nodes when the problem only asks you to rearrange pointers. Mention it as "the
non-destructive version, if the caller still needs the original".

## 💡 The pattern reveal
**Signal:** "invert", "mirror", "flip" the tree.
**Therefore:** Shape C's family, but it's not a comparison: one tree, children swapped
after (or before) recursing.

**Key insight:** swapping must be **simultaneous**. Python's tuple assignment evaluates
the whole right-hand side first, then assigns:

```python
root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
```

**🧨 The trap: two separate lines.**

```python
root.left = self.invertTree(root.right)     # left now points at the old right
root.right = self.invertTree(root.left)     # ...so this inverts the OLD RIGHT again
```

The old left subtree is lost, and the old right one appears on both sides. On
`[4, 2, 7]` you get `[4, 7, 7]`: a tree that looks plausible and is wrong.

## 🔍 Dry run: `root = [4, 2, 7, 1, 3, 6, 9]`

The right-hand side `invert(right), invert(left)` is evaluated left to right, so the
right subtree finishes first.

| step | call | what happens | returns |
|---|---|---|---|
| 1 | `invert(4)` | needs `invert(7)` then `invert(2)` | (waiting) |
| 2 | `invert(7)` | needs `invert(9)`, `invert(6)` | (waiting) |
| 3 | `invert(9)` | leaf: children are `invert(None), invert(None)` = None, None | 9 |
| 4 | `invert(6)` | leaf | 6 |
| 5 | back in 7 | `7.left, 7.right = 9, 6` | 7 (now 9, 6) |
| 6 | `invert(2)` | children `invert(3)` → 3, `invert(1)` → 1 | (waiting) |
| 7 | back in 2 | `2.left, 2.right = 3, 1` | 2 (now 3, 1) |
| 8 | back in 4 | `4.left, 4.right = 7, 2` | **4** |

Level order of the result: **`[4, 7, 2, 9, 6, 3, 1]`** ✓. Every swap happens on the
way back **up**: postorder. (Swapping on the way down, preorder, works just as well.)

## ✅ Optimal solution
```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """Mirror the tree in place by swapping children at every node.

        Time:  O(n), every node visited once.
        Space: O(h) for the recursion stack.
        """
        if not root:
            return None
        # one line: both sides are computed BEFORE either pointer is overwritten
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```
**Time:** O(n) · **Space:** O(h)

Iterative, if they ask (any traversal works, BFS shown):
```python
queue = deque([root] if root else [])
while queue:
    node = queue.popleft()
    node.left, node.right = node.right, node.left
    if node.left:  queue.append(node.left)
    if node.right: queue.append(node.right)
return root
```

## ⚠️ Gotchas
- **Two lines instead of one** loses a subtree. See the trap above. If you must use two
  lines, save one side in a temp first.
- **Return `root`.** Forgetting it returns `None` and the grader sees an empty tree.
- **Visit order doesn't matter.** Pre, post, BFS all work, because each node's swap is
  independent. Inorder is the exception: swap between the calls and you recurse into
  the same subtree twice.

## 🎤 Interview talking points
- *"Mirror each subtree, then swap them. Base case: an empty tree is its own mirror."*
- *"I swap in one tuple assignment so both recursive results exist before either
  pointer changes."*
- *"O(n) time, O(h) space. BFS works too, any order except inorder."*

## 🔗 Transfer
Invert **changes** a tree. The next four episodes **compare** trees, and they all use
the lockstep function from Shape C. EP128 Symmetric Tree asks "is this tree equal to its
own inverse?" without building the inverse: it walks both sides at once, cross-wired.

## 📹 Metadata
- **Title:** `Invert Binary Tree, and the two-line bug | Trees #7`
- **Thumbnail:** `[4, 7, 7] ??`
- **Short:** the two-line version producing `[4, 7, 7]`, then the one-line fix. 40s.
