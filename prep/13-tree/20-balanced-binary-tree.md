# EP140 · P13E20 · Balanced Binary Tree   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/balanced-binary-tree/description/

---

## 🎬 Hook
> "Checking if a tree is balanced sounds like: at every node, compute both heights and
> compare. That's O(n²), because you recompute the same heights over and over. The fix
> is a single magic number: **`-1`**. Return a height when things are fine, return `-1`
> when they're not, and the height *and* the verdict travel up together in one pass."

## 📋 Problem, in your words
```
Given a binary tree, return True if it is height-balanced:

  at EVERY node, the heights of the left and right subtrees
  differ by at most 1.

An empty tree is balanced.
```

## 🔢 The example
```
Input:  [3,9,20,null,null,15,7]      ->  True

          3
         / \
        9   20
           /  \
          15   7

Input:  [1,2,2,3,3,null,null,4,4]    ->  False

            1          <- left height 3, right height 1: differ by 2
           / \
          2   2
         / \
        3   3
       / \
      4   4

Input:  [1,2,2,3,null,null,3,4,null,null,4]  ->  False

            1          <- root looks FINE: 3 vs 3
           / \
          2   2        <- but this 2 has left height 2, right height 0
         /     \
        3       3
       /         \
      4           4
```

## 🧸 ELI5
> Every manager must report their team's height **and** whether their team is lopsided.
> The slow way: the CEO asks for heights, then asks every manager separately, and each
> of those re-counts their whole team from scratch.
>
> The smart way: everyone reports **one number** up. If your team is fine, report its
> height. If your team, or anyone under you, is lopsided, report **-1**, meaning
> "broken, don't bother". A manager who hears -1 from either side doesn't even do the
> maths. They just pass -1 up.
>
> ```
> heights are never negative, so -1 can't be confused with a real height.
> ```

## 🐌 Brute force (say it, don't type it)
At every node, call `maxDepth` (EP139) on both children, compare, then recurse into
both children and do it again.

```python
def isBalanced(node):
    if not node: return True
    return (abs(depth(node.left) - depth(node.right)) <= 1
            and isBalanced(node.left) and isBalanced(node.right))
```

Every node's height gets recomputed once by **each of its ancestors**, so the cost is
**O(n · h)**: O(n log n) on a nicely balanced tree, and the O(n²) the pattern card warns
about as the tree gets deep. The waste is that `depth(node.left)` already computed every
height below, and then threw them all away.

## 💡 The pattern reveal
**Signal:** "height-balanced", a verdict that depends on a **number from both
children**.
**Therefore:** Shape D, bottom-up, with the pattern card's **`-1` sentinel**.

| | answer |
|---|---|
| needs from children | their heights, or the news that they already failed |
| hands back to parent | `1 + max(L, R)`, or `-1` if anything failed |
| records as the answer | "did `-1` reach the root?" |

**Key insight:** the height and the verdict can share one integer. A real height is
`>= 0`, so any negative value is free to mean "unbalanced below". That turns two
recursions into one: **O(n²) → O(n)**.

## 🔍 Dry run: `[1,2,2,3,3,null,null,4,4]`

Postorder, in the order calls return:

| step | node | L | R | `abs(L - R)` | returns |
|---|---|---|---|---|---|
| 1 | 4 (left) | 0 | 0 | 0 | 1 |
| 2 | 4 (right) | 0 | 0 | 0 | 1 |
| 3 | 3 (under 2) | 1 | 1 | 0 | 2 |
| 4 | 3 (right of 2) | 0 | 0 | 0 | 1 |
| 5 | 2 (left) | 2 | 1 | 1 | 3 |
| 6 | 2 (right) | 0 | 0 | 0 | 1 |
| 7 | 1 (root) | 3 | 1 | **2 > 1** | **-1** |

`height(root) == -1` → **False** ✓.

And the third example, the one that looks fine at the root: the left `2` has `L = 2`
(from 3 → 4) and `R = 0`, so **it** returns `-1`. The root sees `L == -1` and returns
`-1` immediately, without ever computing the right side. A root-only check would have
seen 3 vs 3 and said True.

## ✅ Optimal solution
```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """Every node's subtree heights differ by at most 1.

        Time:  O(n), one postorder pass; each height is computed once.
        Space: O(h), the recursion stack.
        """
        def height(node: Optional[TreeNode]) -> int:
            """Height of node's subtree, or -1 if it is unbalanced anywhere."""
            if not node:
                return 0

            L = height(node.left)
            if L == -1:
                return -1           # already broken below: skip the right side
            R = height(node.right)
            if R == -1:
                return -1

            if abs(L - R) > 1:
                return -1           # broken right here
            return 1 + max(L, R)

        return height(root) != -1
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Balanced means at every node, not just the root.** The third example is balanced at
  the root and unbalanced one level down. That's the test that catches root-only checks.
- **Check `-1` before using the height.** If you compute `abs(L - R)` with `L = -1`, a
  broken left side of "-1" next to a right side of 0 gives `abs(-1) = 1`, which *passes*.
  The early returns aren't just an optimisation; they're correctness.
- **Don't reuse the name `depth` for both meanings.** A helper that returns "height or
  -1" is not a depth function. Name and docstring it so the sentinel is obvious.
- **`> 1`, not `>= 1`.** A difference of exactly 1 is allowed.
- **Empty tree is True.** `height(None) = 0 != -1`. Free.

## 🎤 Interview talking points
- *"The naive version calls depth at every node, so every height gets recomputed by
  every ancestor: O(n times h), O(n²) in the worst case."*
- *"I compute height bottom-up once, and use -1 as a sentinel for 'unbalanced below'.
  Heights are never negative, so -1 is safe. One pass, O(n)."*
- *"The early return on -1 also means I stop exploring the moment I find a failure."*
- *"The alternative is returning a tuple (is_balanced, height). Same complexity; the
  sentinel is just tighter."*

## 🔗 Transfer
EP139's three lines, plus one comparison and a sentinel. Tomorrow, EP141 Diameter,
keeps the height return but adds a **global best** that's updated at every node: the
first time the value returned to the parent and the value recorded as the answer are
**different things**. That split is the key to EP148 Maximum Path Sum.

## 📹 Metadata
- **Title:** `Balanced Binary Tree, one -1 turns O(n²) into O(n) | Trees #20`
- **Thumbnail:** `return -1` (orange block)
- **Short:** the third example, root says "3 vs 3, fine", then -1 bubbling up from one
  level down. 45s.
