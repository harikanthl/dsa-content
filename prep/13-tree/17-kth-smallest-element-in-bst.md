# EP137 · P13E17 · Kth Smallest Element in a BST   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/kth-smallest-element-in-a-bst/description/

---

## 🎬 Hook
> "The kth smallest number in a BST is sitting in plain sight: walk the tree **inorder**
> and the values come out sorted. The only real question is how to **stop** at k
> instead of walking all million nodes, and that's why this episode writes inorder
> with a stack instead of recursion."

## 📋 Problem, in your words
```
Given the root of a binary SEARCH tree and an integer k,
return the kth smallest value in the tree (k is 1-indexed).

  - 1 <= k <= number of nodes, so the answer always exists
  - values are unique
```

## 🔢 The example
```
Input:  root = [5,3,6,2,4,null,null,1], k = 3
Output: 3

            5
           / \
          3   6
         / \
        2   4
       /
      1

Why:    inorder = 1, 2, 3, 4, 5, 6  ->  the 3rd is 3

Input:  root = [3,1,4,null,2], k = 1   ->  1
```

## 🧸 ELI5
> A BST is a bookshelf where every book to the **left** of a book has a smaller number
> and every book to the **right** has a bigger one. You want the 3rd smallest.
>
> You don't pull every book off the shelf and sort the pile. You go to the **far left
> end**, and count: one, two, three. Stop. Done.
>
> Going "to the far left end" in a tree means: keep stepping left until you can't, and
> leave a breadcrumb (push onto a stack) at every node you pass, so you can come back
> to it. Each time you come back to a breadcrumb, that's the next book in order.

## 🐌 Brute force (say it, don't type it)
Do a full recursive inorder into a list, return `values[k - 1]`. **O(n)** time and
**O(n)** space, and it's correct. What's wasteful: it visits every node even when k is
1, and it stores every value when you only ever need a counter. Say it, then say "I can
stop at the kth visit if I control the loop myself."

## 💡 The pattern reveal
**Signal:** "binary **search** tree" + "kth smallest" (an **order** question).
**Therefore:** the BST tell from the pattern card: stop thinking about the tree, think
about the **sorted array its inorder produces**. Shape E, the inorder walk as engine.

**Key insight:** kth smallest in a sorted array is index `k - 1`. Inorder *is* that
sorted array, generated one value at a time. So count visits and return on the kth.

**Why iterative?** A recursive inorder can stop, but only by threading a flag or a
`nonlocal` counter back up through every frame. The iterative version is a plain
`while` loop, so "stop" is just `return`.

```python
while stack or node:
    while node:                 # dive left, leaving breadcrumbs
        stack.append(node)
        node = node.left
    node = stack.pop()          # the next value in sorted order
    k -= 1
    if k == 0:
        return node.val         # <- the early exit that recursion makes awkward
    node = node.right
```

## 🔍 Dry run: `[5,3,6,2,4,null,null,1]`, `k = 3`

| step | action | stack (bottom → top) | node | k after |
|---|---|---|---|---|
| 1 | dive left from 5: push 5, 3, 2, 1 | `[5,3,2,1]` | `None` | 3 |
| 2 | pop **1**, visit | `[5,3,2]` | 1 | 2 |
| 3 | go to 1.right (`None`), nothing to dive | `[5,3,2]` | `None` | 2 |
| 4 | pop **2**, visit | `[5,3]` | 2 | 1 |
| 5 | go to 2.right (`None`), nothing to dive | `[5,3]` | `None` | 1 |
| 6 | pop **3**, visit, k hits 0 → **return 3** | `[5]` | 3 | 0 |

Answer **3** ✓. Nodes 4 and 6 are never touched, and 5 never leaves the stack. That's
the whole point: **O(h + k)**, not O(n).

## ✅ Optimal solution
```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """kth smallest value in a BST, by an inorder walk that stops early.

        Time:  O(h + k), h to dive to the minimum, then k pops (each pop may dive,
               but every node is pushed at most once).
        Space: O(h), the stack holds at most one root-to-leaf path.
        """
        stack, node = [], root

        while stack or node:
            while node:                 # dive left as far as possible
                stack.append(node)
                node = node.left

            node = stack.pop()          # next value in sorted order
            k -= 1
            if k == 0:
                return node.val

            node = node.right           # then its right subtree, in order
```
**Time:** O(h + k) · **Space:** O(h)

## ⚠️ Gotchas
- **k is 1-indexed.** Decrement *then* check `k == 0`. Checking before the decrement
  returns the (k+1)th.
- **`while stack or node`, both.** `while stack` alone never starts (the stack is empty
  at the beginning); `while node` alone stops the first time you pop a node with no
  right child.
- **`node = node.right` is unconditional.** Don't guard it with `if node.right`. When it's
  `None`, the inner `while` just doesn't run and the next pop climbs back up. That's
  the mechanism.
- **Don't sort.** Collecting values and calling `sorted()` is O(n log n) and ignores
  the one fact the problem gave you.
- **Skewed tree = O(n).** A BST built from sorted inserts is a linked list, and `h = n`.
  "O(h + k)" is only fast when the tree is balanced. Say that.

## 🎤 Interview talking points
- *"Inorder on a BST is sorted, so the kth smallest is the kth node an inorder walk
  visits."*
- *"I write inorder iteratively so I can return the moment the count hits k. That's
  O(h + k) instead of O(n)."*
- *"Follow-up, if the tree is modified often and this is queried often: store the
  subtree size in each node. Then at each node compare k with the left subtree's size
  and go left, return, or go right with k reduced. O(h) per query."* ← the standard
  follow-up; have it ready.
- *"Recursive works too, with a `nonlocal` counter, but stopping means checking a flag
  after every call."*

## 🔗 Transfer
EP136 Two Sum IV dumped the inorder into a list and used it as a sorted array. Today
the same walk is used *lazily*, one value at a time, so it can stop. The next time this
exact loop appears is EP144 Recover BST, where instead of counting visits it compares
each visited node with the one before it. Tomorrow, EP138, switches families entirely:
Validation, and the first problem where BFS beats DFS.

## 📹 Metadata
- **Title:** `Kth Smallest in a BST, stop the inorder at k | Trees #17`
- **Thumbnail:** `STOP AT k` (green block)
- **Short:** the dry run table, with nodes 4 and 6 greyed out as "never touched". 40s.
