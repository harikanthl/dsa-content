# EP143 · P13E23 · Validate Binary Search Tree   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/validate-binary-search-tree/description/

---

## 🎬 Hook
> "Here's a tree where every node is bigger than its left child and smaller than its
> right child, and it is **not** a BST. The 4 in the corner is fine next to its parent
> and illegal next to its grandparent. The fix is to stop asking 'what's my parent?' and
> start asking 'what **range** am I allowed to be in?'"

## 📋 Problem, in your words
```
Given the root of a binary tree, return True if it is a valid BST:

  - every value in a node's LEFT subtree is strictly LESS than the node
  - every value in its RIGHT subtree is strictly GREATER
  - and both subtrees are BSTs themselves

Strict: equal values are NOT allowed.
```

## 🔢 The example
```
Input:  [2,1,3]                 ->  True

Input:  [5,1,6,null,null,4,7]   ->  False

            5
           / \
          1   6
             / \
            4   7

Why:    4 < 6, fine as 6's left child.
        But 4 is in 5's RIGHT subtree, so it must be > 5. It isn't.

Input:  [5,1,4,null,null,3,6]   ->  False   (4 < 5 on the right, caught at once)
Input:  [2,2,2]                 ->  False   (equal is not allowed)
```

## 🧸 ELI5
> Think of a number line, and every node is a signpost that splits it.
>
> The root 5 says: "everything left of me lives in `(-∞, 5)`, everything right lives in
> `(5, ∞)`." Then 6, living in `(5, ∞)`, splits **its** space: its left child lives in
> `(5, 6)`, and its right child lives in `(6, ∞)`.
>
> ```
> -∞ ------------ 5 ------------ 6 ------------ +∞
>    [ left of 5 ]  [ left of 6 ]  [ right of 6 ]
>                        ^
>                   4 must live here, between 5 and 6.  It doesn't.
> ```
>
> Every step down **narrows** the allowed range. Going left caps the top; going right
> raises the floor. A node is legal if it lands inside its range.

## 🐌 Brute force (say it, don't type it)
At every node, find the max of its left subtree and the min of its right subtree and
check `max(left) < node < min(right)`. Correct, but every subtree gets scanned by every
ancestor: **O(n · h)**, O(n²) worst case. The waste: those min/max scans are exactly the
bounds that could have been passed **down** for free.

## 💡 The pattern reveal
**Signal:** "binary **search** tree" + "validate".
**Therefore:** Shape E. Two ways, and you should know both:

| approach | idea |
|---|---|
| **bounds (lead with this)** | pass `(lo, hi)` down; left tightens `hi`, right tightens `lo` |
| inorder | inorder of a BST is strictly increasing; check each value against the previous |

**Key insight:** a node must satisfy **every** ancestor, not just its parent. You don't
need to remember all the ancestors, though: only the **tightest** limit from above and
below. That's two numbers.

**🧨 The trap, the pattern card's gotcha #2:**

```python
# WRONG: passes on [5,1,6,null,null,4,7]
return (not node.left or node.left.val < node.val) and \
       (not node.right or node.right.val > node.val) and ...
```

Every parent-child pair in the example is legal. The illegal pair is 4 and its
**grand**parent 5. A parent-only check never looks there.

## 🔍 Dry run: `[5,1,6,null,null,4,7]`

| step | call `valid(node, lo, hi)` | `lo < val < hi`? | next |
|---|---|---|---|
| 1 | `valid(5, -∞, +∞)` | yes | go left with `hi = 5` |
| 2 | `valid(1, -∞, 5)` | yes | both children `None` → True |
| 3 | back at 5 | - | go right with `lo = 5` |
| 4 | `valid(6, 5, +∞)` | yes | go left with `hi = 6` |
| 5 | `valid(4, 5, 6)` | **5 < 4? no** | **return False** |

Answer **False** ✓. Step 5 is the whole episode: the `lo = 5` was inherited from the
root, two levels up, and it's what catches the 4. Node 7 is never checked; `and`
short-circuits.

## ✅ Optimal solution
```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """Every node lies strictly inside the range its ancestors allow.

        Time:  O(n), each node checked once.
        Space: O(h), the recursion stack.
        """
        def valid(node: Optional[TreeNode], lo: float, hi: float) -> bool:
            if not node:
                return True
            if not (lo < node.val < hi):
                return False
            # going left caps the top at node.val; going right raises the floor
            return (valid(node.left, lo, node.val)
                    and valid(node.right, node.val, hi))

        return valid(root, float('-inf'), float('inf'))
```
**Time:** O(n) · **Space:** O(h)

The inorder version, for when they ask for another way:

```python
prev, stack, node = None, [], root
while stack or node:
    while node:
        stack.append(node)
        node = node.left
    node = stack.pop()
    if prev is not None and prev >= node.val:
        return False            # not strictly increasing
    prev = node.val
    node = node.right
return True
```

## ⚠️ Gotchas
- **Compare against bounds, not the parent.** The parent-only version passes most tests
  and fails the grandparent case. Draw the example; it's the whole point.
- **Strict inequalities.** `lo < val < hi`, not `<=`. `[2,2,2]` must be False. In the
  inorder version that's `prev >= node.val`, not `>`.
- **Infinite bounds, not `INT_MIN`/`INT_MAX`.** Node values can be exactly
  `-2³¹` or `2³¹ - 1`. Using those as sentinels makes a legal tree like `[2147483647]`
  fail. Python's `float('inf')` sidesteps it (in Java/C++, use `Long` or `None`).
- **`prev = None`, not `prev = 0` or `-inf` as an int.** Same reason: the first value
  might be anything.
- **Left gets `(lo, node.val)`, right gets `(node.val, hi)`.** Swap them and every
  valid tree fails.

## 🎤 Interview talking points
- *"A node must be bigger than every ancestor it went right from and smaller than every
  one it went left from. I only need the tightest of each, so I carry a (lo, hi) range
  down and narrow it at every step."*
- *"Comparing with the parent alone is the classic bug: it misses a node that's fine
  next to its parent but on the wrong side of its grandparent."* ← say this before they
  do.
- *"Equivalent approach: inorder of a BST is strictly increasing, so walk inorder and
  compare each value with the previous."*
- *"O(n) time, O(h) space either way."*

## 🔗 Transfer
EP133 used the BST rule to **search**, one branch per level. Today it's used to
**check**, and the bounds version is Shape E exactly as the pattern card writes it.
Tomorrow, EP144 Recover BST, starts from the inorder view instead: a valid BST's
inorder is sorted, and a BST with two nodes swapped has an inorder with exactly one or
two "drops". Find the drops, swap back.

## 📹 Metadata
- **Title:** `Validate BST, why checking the parent isn't enough | Trees #23`
- **Thumbnail:** `4 vs GRANDPARENT` (red block)
- **Short:** the number line, the range narrowing to `(5, 6)`, and 4 landing outside
  it. 40s.
