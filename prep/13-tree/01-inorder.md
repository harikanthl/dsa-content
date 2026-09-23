# EP121 · P13E01 · Binary Tree Inorder Traversal   [Easy]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-inorder-traversal/description/

---

## 🎬 Hook
> "Every tree problem in the next thirty episodes is one function with three lines:
> go left, do something, go right. Today the 'something' is just 'write the value
> down'. And the order you get has a superpower: on a binary search tree, it comes
> out **sorted**."

## 📋 Problem, in your words
```
Given the root of a binary tree, return the values of its nodes in INORDER:
everything in the left subtree, then the node itself, then everything
in the right subtree. Apply that rule at every node, all the way down.

An empty tree returns [].
```

## 🔢 The example
```
        1
       / \          Input:  root = [1, 2, 3, 4, 5]
      2   3         Output: [4, 2, 5, 1, 3]
     / \            Why:    1 waits for its whole left side (4 2 5),
    4   5                   then 1, then its right side (3)

Input:  [1, null, 2, 3]     1               Output: [1, 3, 2]
                             \
                              2
                             /
                            3
Input:  []                  Output: []
```

## 🧸 ELI5
> You're reading a family tree to someone, and you have one rule: **before you say a
> person's name, you must finish reading everyone on their left.** Then you say the
> name. Then you read everyone on their right.
>
> Start at 1. Not allowed to say "1" yet, left first. Go to 2. Not allowed to say "2"
> yet, left first. Go to 4. 4 has nobody on its left, so say **4**. Back up to 2, whose
> left is now done: say **2**. Then 2's right: **5**. 2's whole family is done, so back
> up to 1: say **1**. Then 1's right: **3**.
>
> `4 2 5 1 3`. Nobody is said before their left side is finished.

## 🐌 Brute force (say it, don't type it)
There isn't a slower "real" way: every approach has to touch every node once, so
**O(n)** is the floor. The interesting part is the **two ways to be O(n)**: recursion
(the call stack remembers where to come back to) and an explicit stack (you remember it
yourself). The interviewer almost always asks for the second one after you write the
first.

## 💡 The pattern reveal
**Signal:** a `TreeNode` and the word "inorder".
**Therefore:** Shape A from the pattern card, the DFS template, with the visit **between**
the two recursive calls.

```python
def dfs(node):
    if not node:
        return
    dfs(node.left)
    res.append(node.val)      # <- INorder: between the calls
    dfs(node.right)
```

**Key insight for the iterative version:** the recursion does two things you have to
replace by hand. It **dives left** until it hits `None`, and it **remembers every node
it passed on the way down** so it can come back to them. A stack does the remembering.

| step | recursion does it with | iterative does it with |
|---|---|---|
| dive left | `dfs(node.left)` | `while node: stack.append(node); node = node.left` |
| come back to the parent | the function returns | `node = stack.pop()` |
| visit | `res.append(node.val)` | same line |
| go right | `dfs(node.right)` | `node = node.right` |

## 🔍 Dry run: iterative, `root = [1, 2, 3, 4, 5]`

| step | `node` before | action | stack after (bottom → top) | `res` |
|---|---|---|---|---|
| 1 | 1 | dive: push 1, push 2, push 4, `node = None` | `[1, 2, 4]` | `[]` |
| 2 | None | pop 4, visit, `node = 4.right = None` | `[1, 2]` | `[4]` |
| 3 | None | no dive; pop 2, visit, `node = 2.right = 5` | `[1]` | `[4, 2]` |
| 4 | 5 | dive: push 5, `node = None`; pop 5, visit, `node = None` | `[1]` | `[4, 2, 5]` |
| 5 | None | pop 1, visit, `node = 1.right = 3` | `[]` | `[4, 2, 5, 1]` |
| 6 | 3 | dive: push 3; pop 3, visit, `node = None` | `[]` | `[4, 2, 5, 1, 3]` |
| 7 | None | stack empty and node is None, **stop** | `[]` | ✓ |

Step 5 is the one to point at: the stack is **empty** but we're not done, because
`node` is 3. That's why the loop condition is `while stack or node`, not just
`while stack`.

## ✅ Optimal solution
```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Left subtree, node, right subtree, at every node. Recursive version.

        Time:  O(n), every node is visited exactly once.
        Space: O(h) for the call stack, O(n) on a skewed tree.
        """
        res = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            res.append(node.val)        # inorder: between the two calls
            dfs(node.right)

        dfs(root)
        return res
```

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Same order, explicit stack instead of the call stack.

        Time:  O(n), each node is pushed once and popped once.
        Space: O(h) for the stack.
        """
        res, stack, node = [], [], root

        while stack or node:
            while node:                 # dive left, remembering the way back
                stack.append(node)
                node = node.left
            node = stack.pop()          # leftmost node not yet visited
            res.append(node.val)
            node = node.right           # then its right subtree

        return res
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **`while stack or node`**, not `while stack`. After popping the root, the stack is
  empty but its right subtree hasn't started. Dry-run step 5.
- **The null check is the first line** of `dfs`. Touch `node.left` before it and an
  empty tree crashes.
- **`res` lives outside `dfs`.** Returning and concatenating lists
  (`dfs(l) + [v] + dfs(r)`) works but copies at every level: O(n²) on a skewed tree.
- **Recursion depth.** Python's default limit is 1000. A skewed tree of 2000 nodes
  crashes the recursive version and not the iterative one. That's the honest reason to
  know the iterative form.
- **Don't set `node = None` after visiting.** `node = node.right` already does it when
  there's no right child, and it's the only thing that ends the dive.

## 🎤 Interview talking points
- *"Inorder is left, node, right. The visit sits between the two recursive calls."*
- *"Iteratively, a stack replaces the call stack: dive left pushing everything, pop to
  visit, then step right."*
- *"O(n) time, O(h) space. h is log n when balanced and n when skewed."*
- *"On a BST this comes out sorted, which is why so many BST problems are really
  inorder problems."* ← say it, it sets up EP136, EP137, EP143, EP144.
- *"If they want O(1) space, that's Morris traversal: thread each node's inorder
  predecessor back to it temporarily."* Name it; don't write it unless asked.

## 🔗 Transfer
This is the template for the whole pattern. Tomorrow, EP122 Preorder, moves the visit
**up one line** and nothing else changes in the recursive version. The iterative inorder
loop is the exact engine of EP137 Kth Smallest in a BST, where being able to **stop
early** is the whole point, and of EP144 Recover BST.

## 📹 Metadata
- **Title:** `Inorder Traversal, recursive AND iterative | Trees #1`
- **Thumbnail:** `LEFT · ME · RIGHT`
- **Short:** the stack filling with 1, 2, 4 on the dive, then popping 4 2 5 1 3. 45s.
