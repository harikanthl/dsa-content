# EP131 · P13E11 · Flip Equivalent Binary Trees   [Medium]

**Pattern:** Tree (Mirror and Symmetry) · **Link:** https://leetcode.com/problems/flip-equivalent-binary-trees/description/

---

## 🎬 Hook
> "Same Tree, but at any node you're allowed to swap the kids. So at every node there
> are two ways to match: straight, or crossed. Try both, join them with `or`. That's
> the whole solution, and the Mirror family closes with Same Tree and Symmetric Tree
> **fused into one line**."

## 📋 Problem, in your words
```
A "flip" swaps the left and right children of one node. Two trees are
flip equivalent if you can make one equal to the other with ANY number of
flips, at any nodes.

Given root1 and root2, return True if they're flip equivalent.
(LeetCode guarantees the values in each tree are unique.)
```

## 🔢 The example
```
root1:          1                 root2:          1
              /   \                             /   \
             2     3                           3     2
            / \   /                             \   / \
           4   5 6                               6 4   5
              / \                                     / \
             7   8                                   8   7

Output: True
Why:    flip at 1 (swap 2 and 3), flip at 3 (6 moves to the right),
        flip at 5 (swap 7 and 8). Everything else lines up.

root1 = [1, 2, 3], root2 = [1, 2, 4]  ->  False (3 vs 4, no flip fixes a value)
root1 = [],        root2 = []         ->  True
```

## 🧸 ELI5
> A mobile hanging over a baby's crib. Every bar can spin, so the left toy and the
> right toy can trade places whenever the wind blows. Two mobiles are "the same mobile"
> if some amount of spinning makes them look identical.
>
> To check a bar: the toy hanging from it must be the same. Then either its two arms
> already match up **straight** (left with left, right with right), or they match up
> **after one spin** (left with right, right with left). Check each arm the same way,
> all the way down.

## 🐌 Brute force (say it, don't type it)
Canonicalise both trees: at every node, put the child with the smaller value on the
left (treating `None` as smallest), then run Same Tree. **O(n)** and valid because
values are unique, but it modifies the trees and needs a careful ordering rule. The
recursive `or` is cleaner and doesn't touch the input.

## 💡 The pattern reveal
**Signal:** "flip", "swap children any number of times", "equivalent".
**Therefore:** Shape C, with **both** wirings allowed.

```python
return (eq(a.left, b.left)  and eq(a.right, b.right)) \
    or (eq(a.left, b.right) and eq(a.right, b.left))
#       ^^^^^^ EP129 Same Tree ^^^^^^         ^^^^^^ EP128 Symmetric ^^^^^^
```

**Key insight:** flips are independent per node. Whether node 5 is flipped has nothing
to do with whether node 1 is. So each node just asks "straight or crossed?" and trusts
the recursion to sort out everything below.

**Why this isn't exponential:** each call can fire four recursive calls, which sounds
like 4^h. But values are unique, so at most **one** pairing can get past the value
check on its children. The wrong pairing dies at its first `a.val != b.val`. Total
work stays O(n).

## 🔍 Dry run: `root1 = [1, 2, 3]`, `root2 = [1, 3, 2]`

| step | call | checks | result |
|---|---|---|---|
| 1 | `eq(1, 1)` | not empty, 1 = 1 | try straight |
| 2 | straight: `eq(2, 3)` | 2 ≠ 3 | **False**, `and` skips `eq(3, 2)` |
| 3 | crossed: `eq(2, 2)` | 2 = 2, children all None → True | True |
| 4 | crossed: `eq(3, 3)` | 3 = 3, children None → True | True |
| 5 | step 1: `False or (True and True)` | | **True** ✓ |

Step 2 is the "wrong pairing dies immediately" argument in action: one comparison, gone.

## ✅ Optimal solution
```python
class Solution:
    def flipEquiv(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        """True if some set of child-swaps turns root1 into root2.

        Time:  O(n): values are unique, so at most one pairing survives past
               the children's value check at each node.
        Space: O(h) for the recursion stack.
        """
        if not root1 and not root2:
            return True
        if not root1 or not root2:
            return False
        if root1.val != root2.val:
            return False
        return ((self.flipEquiv(root1.left, root2.left)         # straight
                 and self.flipEquiv(root1.right, root2.right))
                or (self.flipEquiv(root1.left, root2.right)     # crossed
                    and self.flipEquiv(root1.right, root2.left)))
```
**Time:** O(n) · **Space:** O(h)

Keep it as one expression: `or` short-circuits, so the crossed pairing is only tried
when the straight one fails. Splitting it into two variables always evaluates both.

## ⚠️ Gotchas
- **Both pairings need both halves.** `(L,L) and (R,R)` **or** `(L,R) and (R,L)`. Mixing
  them, e.g. `(L,L) or (L,R)`, lets the left arm match one way and the right arm the
  other, which isn't a flip.
- **The same two null checks** as EP129, same order.
- **Unique values are what keep it O(n).** With duplicates (not this problem) both
  pairings can survive at every level and it degrades to exponential in the worst case.
  Say this if asked "what if values repeat?"
- **Don't actually flip anything.** The problem is a yes/no question; mutating the
  input to test a flip and then un-flipping it is backtracking you don't need.

## 🎤 Interview talking points
- *"At each node the values must match, then the children must match either straight
  or crossed. Straight is Same Tree, crossed is Symmetric Tree."*
- *"Flips at different nodes are independent, so each node decides for itself."*
- *"Four recursive calls per node looks exponential, but with unique values only one
  pairing gets past the first value check, so it's O(n)."* ← the line that impresses.

## 🔗 Transfer
That closes Mirror and Symmetry: Invert (EP127) changes a tree; Symmetric, Same,
Subtree and Flip (EP128 to EP131) compare two with different wirings. Next is the
Search family, starting with EP132 Lowest Common Ancestor, where the recursion stops
returning True/False and starts returning **nodes**.

## 📹 Metadata
- **Title:** `Flip Equivalent Trees, Same Tree OR Symmetric Tree | Trees #11`
- **Thumbnail:** `straight OR crossed`
- **Short:** the one-line return with the two halves labelled EP129 and EP128. 30s.
