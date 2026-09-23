# EP129 · P13E09 · Same Tree   [Easy]

**Pattern:** Tree (Mirror and Symmetry) · **Link:** https://leetcode.com/problems/same-tree/description/

> **Homework episode.** Short format: it's EP128's `mirror` with the wires straightened.
> Show the two null checks and the one wiring change, then hand it over. Aim for 5 to 7
> minutes. The function written here is reused verbatim tomorrow, so make it clean.

---

## 🎬 Hook
> "Yesterday's symmetric check, with the wires un-crossed. Two null checks, one value
> check, two recursive calls. Get the **order of the null checks** right and you've
> written the helper that the next two episodes stand on."

## 📋 Problem, in your words
```
Given the roots of two binary trees p and q, return True if they're the
same tree: identical shape AND identical value at every position.

Two empty trees are the same.
```

## 🔢 The example
```
    1         1           1         1           1         1
   / \       / \         /           \         / \       / \
  2   3     2   3       2             2       2   1     1   2

 [1,2,3] vs [1,2,3]     [1,2] vs [1,null,2]   [1,2,1] vs [1,1,2]
 True                   False: shape          False: values
```

## 🧸 ELI5
> Two people each hold a copy of a family tree and read it to each other over the
> phone, in lockstep. "I'm at the top, I see 1." "Me too, 1." "Going left, I see 2."
> "Going left... I see **nothing**." Stop. Different trees.
>
> The moment one of you hits an empty spot and the other doesn't, it's over. If you
> **both** hit an empty spot at the same moment, that branch matches and you go back
> up.

## 🐌 Brute force (say it, don't type it)
Serialise both trees (preorder, with a marker for every `None`) and compare the
strings. **O(n)** time, **O(n)** space. It works, but only if you include the `None`
markers: without them, `[1,2]` and `[1,null,2]` both serialise to `1,2`.

## 💡 The pattern reveal
**Signal:** two trees, "same", "identical", "equal".
**Therefore:** Shape C, straight wiring.

```python
def same(p, q):
    if not p and not q: return True        # both empty
    if not p or not q:  return False       # exactly one empty
    return p.val == q.val and same(p.left, q.left) and same(p.right, q.right)
```

**Key insight:** after the first check, "not p or not q" can only mean **exactly one**
is empty. That's why the order matters: the second check relies on the first having
already handled "both".

## 🔍 Dry run: `p = [1, 2]`, `q = [1, null, 2]`

| step | call | both empty? | one empty? | values | result |
|---|---|---|---|---|---|
| 1 | `same(1, 1)` | no | no | 1 = 1 ✓ | check left |
| 2 | `same(p.left=2, q.left=None)` | no | **yes** | | **False** |
| 3 | step 1: `True and False` | | | | short-circuits, **False** ✓ |

The right subtrees are never compared. `and` stops at the first failure.

## ✅ Optimal solution
```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """True if p and q have the same shape and the same values.

        Time:  O(min(n, m)), stops at the first mismatch.
        Space: O(min(h1, h2)) for the recursion stack.
        """
        if not p and not q:
            return True                 # both empty: this branch matches
        if not p or not q:
            return False                # exactly one empty: shapes differ
        return (p.val == q.val
                and self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))
```
**Time:** O(min(n, m)) · **Space:** O(min(h1, h2))

## ⚠️ Gotchas
- **Null checks in order.** Both-empty first, one-empty second. The pattern card's
  gotcha #1.
- **Compare values last**, after both null checks. `p.val` before them crashes on
  `None`.
- **Short-circuit `and`**: put the cheap `p.val == q.val` first so a mismatch skips
  both recursive calls.
- **`p == q` compares object identity**, not structure. Two separately built identical
  trees are `!=`.

## 🎤 Interview talking points
- *"Walk both trees in lockstep. Both empty: match. One empty: mismatch. Otherwise
  compare values and recurse left-with-left, right-with-right."*
- *"It's EP128's mirror check without the cross-wiring."*
- *"Stops at the first difference, so it's O(size of the smaller tree)."*

## 🔗 Transfer
This exact function is the inner loop of tomorrow's EP130, Subtree of Another Tree,
which calls it at every node of the big tree. And EP131 Flip Equivalent is this
function with **both** wirings allowed, joined by `or`.

## 📹 Metadata
- **Title:** `Same Tree, the helper the next two episodes need | Trees #9 (homework)`
- **Thumbnail:** `both? one? values.`
- **Short:** the phone call, "I see nothing", stop. 20s.
