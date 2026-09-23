# EP130 · P13E10 · Subtree of Another Tree   [Easy]

**Pattern:** Tree (Mirror and Symmetry) · **Link:** https://leetcode.com/problems/subtree-of-another-tree/description/

---

## 🎬 Hook
> "Two recursions, one inside the other. The outer one walks the big tree and asks, at
> every node, **'could it start here?'** The inner one is yesterday's Same Tree. And the
> reason it's harder than it looks: a subtree has to match **all the way down to the
> leaves**, not just the top few levels."

## 📋 Problem, in your words
```
Given two binary trees root and subRoot, return True if some node in root
is the top of a subtree that is EXACTLY subRoot: same shape, same values,
and it must include ALL of that node's descendants.

A tree counts as a subtree of itself.
```

## 🔢 The example
```
root:         3            subRoot:    4          Output: True
             / \                      / \
            4   5                    1   2
           / \
          1   2

root:         3            subRoot:    4          Output: False
             / \                      / \
            4   5                    1   2        Why: under root's 4 there's an
           / \                                    extra 0. The top matches, the
          1   2                                   bottom doesn't.
             /
            0
```

## 🧸 ELI5
> You have a small jigsaw picture and a huge finished jigsaw. Is the small picture
> **exactly** a corner of the big one?
>
> Put your finger on each piece of the big puzzle in turn and ask: "if the small
> picture's top-left went here, would every piece line up, **with nothing extra
> hanging off**?" If yes at any spot, done. If no spot works, it's not in there.
>
> The "nothing extra" part is the second example: the 4, 1, 2 all line up, but the big
> puzzle has a 0 under the 2, and the small one doesn't. Not a match.

## 🐌 Brute force (say it, don't type it)
The brute force **is** the standard answer: try `same` at every node, **O(n · m)**. The
genuinely faster version is O(n + m): serialise both trees in preorder **with null
markers and delimiters**, then do a substring search (KMP from string algorithms, or
tree hashing). Mention it as the follow-up; the nested recursion is what they expect
first.

## 💡 The pattern reveal
**Signal:** "subtree of", "contains this tree".
**Therefore:** Shape C, run `same` at **every** node of the big tree.

```python
def isSubtree(root, sub):
    if not root:
        return False                        # ran out of places to start
    if same(root, sub):
        return True                         # it starts HERE
    return isSubtree(root.left, sub) or isSubtree(root.right, sub)
```

**Key insight:** there are two separate questions, so two separate functions.

| function | question | base case for `None` |
|---|---|---|
| `isSubtree(node, sub)` | can a match **start** somewhere at or below `node`? | `False`: no more starting points |
| `same(a, b)` | does the tree starting at `a` **equal** `b` exactly? | EP129's two checks |

`same` is what makes "all the way to the leaves" automatic: at the 2 in example two,
`same(2, 2)` finds `2.left = 0` vs `None`, one empty, False.

## 🔍 Dry run: example 2, `root = [3,4,5,1,2,null,null,null,null,0]`, `sub = [4,1,2]`

| step | outer call at | `same(node, sub)`? | why | next |
|---|---|---|---|---|
| 1 | 3 | False | 3 ≠ 4 | try left |
| 2 | 4 | False | 4 = 4, 1 = 1 ✓, then `same(2, 2)`: 2 = 2 but `same(0, None)` → one empty | try 4's left |
| 3 | 1 | False | 1 ≠ 4 | children are None → False, False |
| 4 | 2 | False | 2 ≠ 4 | 2's left is 0 |
| 5 | 0 | False | 0 ≠ 4 | children None → False |
| 6 | 5 | False | 5 ≠ 4 | children None → False |
| 7 | every start failed | | | **False** ✓ |

Step 2 is the moment: the match gets three nodes deep and then fails on the hanging 0.

## ✅ Optimal solution
```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """True if some node of root heads a subtree identical to subRoot.

        Time:  O(n * m), try an O(m) comparison at each of n nodes.
        Space: O(h1 + h2), outer recursion plus inner comparison.
        """
        def same(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
            if not a and not b:
                return True
            if not a or not b:
                return False
            return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

        if not root:
            return False                    # no node left to start a match at
        if same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```
**Time:** O(n · m) · **Space:** O(h1 + h2)

## ⚠️ Gotchas
- **Two base cases, two meanings.** `isSubtree(None, sub)` is `False` ("nowhere left to
  start"). `same(None, None)` is `True` ("both ended together"). Mixing them up is the
  bug.
- **Don't recurse the outer function into `same`'s job.** Writing
  `root.val == sub.val and isSubtree(root.left, sub.left) ...` checks "does it start
  here" and "does it continue" with the same function and accepts partial matches.
- **The serialise trick needs delimiters and null markers.** Without a leading
  delimiter, `"12"` contains `"2"`, so a node 12 matches a node 2. Use `",12,#,#"`
  style tokens.
- **Values can repeat.** Several nodes may equal `sub`'s root; you must try every one,
  which is why it's O(n · m) and not O(n + m).

## 🎤 Interview talking points
- *"Two questions, two functions: `isSubtree` asks where a match could start, `same`
  checks whether it does. I call `same` at every node."*
- *"`same` compares right down to the leaves, so extra nodes below make it fail. That's
  what 'subtree' means here."*
- *"O(n · m) worst case. For O(n + m), serialise both with null markers and run KMP, or
  hash each subtree."* ← the follow-up answer.

## 🔗 Transfer
Tomorrow, EP131 Flip Equivalent, keeps `same` but lets each node match with its
children in **either** order. After that the Mirror family is done and Search begins
with EP132 LCA, which is a different kind of recursion: instead of returning
True/False, each call returns **a node**.

## 📹 Metadata
- **Title:** `Subtree of Another Tree, a recursion inside a recursion | Trees #10`
- **Thumbnail:** `same() at EVERY node`
- **Short:** the match getting three deep, then failing on the hanging 0. 40s.
