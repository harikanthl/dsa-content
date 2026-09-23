# EP122 · P13E02 · Binary Tree Preorder Traversal   [Easy]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-preorder-traversal/description/

---

## 🎬 Hook
> "Take yesterday's inorder code. Move one line up. That's preorder. The recursive
> version is a one-line diff, and the iterative version gets **simpler**, not harder,
> because the node is visited the moment you touch it."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its values in PREORDER:
the node itself first, then its entire left subtree, then its entire
right subtree. Same rule at every node.

An empty tree returns [].
```

## 🔢 The example
```
        1
       / \          Input:  root = [1, 2, 3, 4, 5]
      2   3         Output: [1, 2, 4, 5, 3]
     / \            Why:    say 1 the moment you arrive, then do all of
    4   5                   the left side (2 4 5), then the right (3)

Input:  [1, null, 2, 3]     Output: [1, 2, 3]
Input:  []                  Output: []
```

## 🧸 ELI5
> You're a tour guide walking through a building. The rule: **announce each room the
> second you walk into it**, then explore the left corridor completely, then the right.
>
> Walk into 1: "One!" Left corridor, walk into 2: "Two!" Left again, 4: "Four!" Dead
> end, back to 2, right: 5: "Five!" 2 is done, back to 1, right: 3: "Three!"
>
> `1 2 4 5 3`. You announce a room **before** you see anything inside it. That's why
> preorder is the order you'd use to **copy** or **save** a tree: the parent always
> comes out before its children, so whoever rebuilds it knows where to hang them.

## 🐌 Brute force (say it, don't type it)
Same as yesterday: every node must be touched once, **O(n)** is the floor. The episode
is about how small the change from inorder is, and about the iterative trick that
inorder didn't need: **push right before left**.

## 💡 The pattern reveal
**Signal:** "preorder", or anything that needs a parent handled before its children
(copy, serialise, pass something down).
**Therefore:** Shape A with the visit **before** both calls.

```python
def dfs(node):
    if not node:
        return
    res.append(node.val)      # <- PREorder: before the calls
    dfs(node.left)
    dfs(node.right)
```

**Key insight for the iterative version:** a stack is last-in, first-out. You want the
left child processed first, so it has to be pushed **last**. Push right, then left.

```
pop 1  -> visit 1 -> push 3, push 2     stack [3, 2]    2 is on top, good
```

## 🔍 Dry run: iterative, `root = [1, 2, 3, 4, 5]`

| step | pop | visit → `res` | push (right first, then left) | stack after (bottom → top) |
|---|---|---|---|---|
| 0 | - | - | push 1 | `[1]` |
| 1 | 1 | `[1]` | 3, then 2 | `[3, 2]` |
| 2 | 2 | `[1, 2]` | 5, then 4 | `[3, 5, 4]` |
| 3 | 4 | `[1, 2, 4]` | none (leaf) | `[3, 5]` |
| 4 | 5 | `[1, 2, 4, 5]` | none | `[3]` |
| 5 | 3 | `[1, 2, 4, 5, 3]` | none | `[]` |
| 6 | stack empty, **stop** | ✓ | | |

Row 2 is the one: 3 has been sitting at the bottom since step 1, waiting for the whole
left subtree to drain above it. That's "finish the left before the right", done by a
stack instead of by recursion.

## ✅ Optimal solution
```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Node, left subtree, right subtree, at every node. Recursive version.

        Time:  O(n), every node visited once.
        Space: O(h) for the call stack.
        """
        res = []

        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            res.append(node.val)        # preorder: before the calls
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return res
```

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        """Same order with an explicit stack.

        Time:  O(n), each node pushed and popped once.
        Space: O(h) for the stack.
        """
        if not root:
            return []
        res, stack = [], [root]

        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.right:              # pushed first so it comes out LAST
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return res
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Right before left.** Push left first and you get `1 3 2 5 4`, a valid traversal of
  the mirror image, and a wrong answer.
- **`if not root: return []`** before seeding the stack. `stack = [None]` pops a `None`
  and crashes on `.val`.
- **Don't push `None` children.** Either guard each push (above) or guard after the pop
  (`if not node: continue`). Pick one; mixing them is how you get both bugs.
- **This iterative shape does NOT generalise to inorder.** Inorder needs the dive loop
  from EP121 because the node can't be visited when it's first popped.

## 🎤 Interview talking points
- *"Preorder visits the node before its subtrees. Recursively, the append moves above
  the two calls."*
- *"Iteratively, a plain stack works because a node is visited the moment it's popped.
  I push right before left so left comes off first."*
- *"Preorder is the natural order for serialising a tree: parents come out before
  children, so a reader can rebuild it."*
- *"O(n) time, O(h) space."*

## 🔗 Transfer
EP123 Postorder moves the visit to the **bottom**, and has a cute iterative trick that
reuses today's code. Preorder comes back for real in EP149, Construct Tree from
Preorder and Inorder, where `preorder[0]` being the root is the entire insight. Every
top-down problem that passes something *down* (EP145 Path Sum, EP147 Sum of Root to
Leaf) is preorder-shaped: do your work on the way in.

## 📹 Metadata
- **Title:** `Preorder Traversal, one line moved | Trees #2`
- **Thumbnail:** `ME · LEFT · RIGHT`
- **Short:** yesterday's code, the append line sliding up, output changing live. 30s.
