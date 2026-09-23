# EP123 · P13E03 · Binary Tree Postorder Traversal   [Easy]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-postorder-traversal/description/

> **Homework episode.** Short format: the viewer should be able to write this from
> EP121 and EP122 alone. Show the recursive one-line move, reveal the iterative trick,
> hand it over. Aim for 6 to 8 minutes.

---

## 🎬 Hook
> "Your homework: postorder. Recursively, it's the third and last place the append
> line can go. Iteratively, there's a trick so cheap it feels like cheating: run
> **preorder backwards** and reverse the answer."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its values in POSTORDER:
the entire left subtree, then the entire right subtree, then the node
itself. A node is only written down after both its children are done.

An empty tree returns [].
```

## 🔢 The example
```
        1
       / \          Input:  root = [1, 2, 3, 4, 5]
      2   3         Output: [4, 5, 2, 3, 1]
     / \            Why:    1 is last because it waits for everyone;
    4   5                   2 waits for 4 and 5

Input:  [1, null, 2, 3]     Output: [3, 2, 1]
Input:  []                  Output: []
```

## 🧸 ELI5
> Cleaning up after a party in a house of rooms. You can't lock a room until every room
> **inside** it is already locked. So you walk all the way to the innermost rooms, lock
> those first, and work your way back out. The front door is the very last thing you
> lock.
>
> That's why postorder is the order for **deleting** a tree, or for anything where the
> parent's answer depends on the children's answers (sizes, heights, sums). The
> children report first.

## 🐌 Brute force (say it, don't type it)
O(n) is the floor again. The only "wasteful" version is building lists and
concatenating (`post(l) + post(r) + [v]`), which is O(n²) on a skewed tree. Mention it
and move on.

## 💡 The pattern reveal
**Signal:** "postorder", or any answer computed **from** the children's answers.
**Therefore:** Shape A with the visit **after** both calls.

```python
def dfs(node):
    if not node:
        return
    dfs(node.left)
    dfs(node.right)
    res.append(node.val)      # <- POSTorder: after the calls
```

**Key insight for the iterative version:** postorder is left, right, node. Read it
backwards: **node, right, left**. That's preorder with the children swapped. So run
EP122's iterative code, push **left before right** this time, and reverse at the end.

```
modified preorder (node, right, left):  1 3 2 5 4
reversed:                               4 5 2 3 1   = postorder ✓
```

## 🔍 Dry run: iterative, `root = [1, 2, 3, 4, 5]`

| step | pop | append → `res` | push (left first, then right) | stack after |
|---|---|---|---|---|
| 0 | - | - | push 1 | `[1]` |
| 1 | 1 | `[1]` | 2, then 3 | `[2, 3]` |
| 2 | 3 | `[1, 3]` | none | `[2]` |
| 3 | 2 | `[1, 3, 2]` | 4, then 5 | `[4, 5]` |
| 4 | 5 | `[1, 3, 2, 5]` | none | `[4]` |
| 5 | 4 | `[1, 3, 2, 5, 4]` | none | `[]` |
| 6 | reverse | **`[4, 5, 2, 3, 1]`** ✓ | | |

## ✅ Optimal solution
```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Left subtree, right subtree, node, at every node. Recursive version.

        Time:  O(n), every node visited once.
        Space: O(h) for the call stack.
        """
        res = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            res.append(node.val)        # postorder: after both calls

        dfs(root)
        return res
```

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Node-right-left preorder, reversed, is left-right-node postorder.

        Time:  O(n), one pass plus one reverse.
        Space: O(n), the stack plus the reversed output.
        """
        if not root:
            return []
        res, stack = [], [root]

        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.left:               # left pushed first so RIGHT is handled first
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return res[::-1]
```
**Time:** O(n) · **Space:** O(h) recursive, O(n) iterative with the reverse

## ⚠️ Gotchas
- **Push order flips from EP122.** Preorder pushes right then left. This trick pushes
  left then right. Copy-pasting EP122 unchanged reverses plain preorder
  `1 2 4 5 3` into `3 5 4 2 1`, which is nothing useful.
- **The reverse trick produces the right list, not a true postorder visit.** Nodes are
  touched in node-right-left order. If the interviewer needs to *act* on each node in
  postorder (free memory, say), you need the one-stack version with a `prev` pointer.
  Say that out loud; it shows you know the trick's limit.
- **Null check first**, as always.

## 🎤 Interview talking points
- *"Postorder is left, right, node. The append goes after both recursive calls."*
- *"Iteratively, I reverse a node-right-left preorder. It's EP122's loop with the push
  order swapped."*
- *"Postorder is the natural order when a node's answer depends on its children:
  heights, sizes, deleting a tree."* ← this sentence is the bridge to Shape D.

## 🔗 Transfer
All three DFS orders are done. The one to care about most is this one: every
**bottom-up** problem later in the pattern (EP139 Max Depth, EP140 Balanced, EP141
Diameter, EP148 Max Path Sum) is postorder in disguise, because the parent can't answer
until both children have. Next, EP124 leaves DFS behind entirely: one level at a time,
with a queue.

## 📹 Metadata
- **Title:** `Postorder Traversal, the reverse-preorder trick | Trees #3 (homework)`
- **Thumbnail:** `REVERSE IT`
- **Short:** `1 3 2 5 4` flipping into `4 5 2 3 1`. 20s, the whole episode fits.
