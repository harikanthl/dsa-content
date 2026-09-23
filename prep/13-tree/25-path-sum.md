# EP145 · P13E25 · Path Sum   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/path-sum/description/

---

## 🎬 Hook
> "Is there a root-to-leaf path that adds up to 22? Don't add on the way down and compare
> at the bottom. **Subtract.** Carry 'how much is still owed' down the tree, and at a leaf
> the only question is: is the bill paid off, exactly zero? The trap is what counts as
> 'the bottom'."

## 📋 Problem, in your words
```
Given the root of a binary tree and an integer targetSum,
return True if there is a ROOT-TO-LEAF path whose values add up to targetSum.

  - a leaf is a node with NO children
  - values and target can be negative
  - an empty tree has no paths: False, even for target 0
```

## 🔢 The example
```
Input:  root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: True

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1

Why:    5 + 4 + 11 + 2 = 22

Input:  root = [1,2,3], targetSum = 5   ->  False   (paths are 3 and 4)
Input:  root = [1,2],   targetSum = 1   ->  False   (1 alone is NOT a root-to-leaf path:
                                                     the root has a child, so it's not a leaf)
Input:  root = [],      targetSum = 0   ->  False
```

## 🧸 ELI5
> You start at the top of a hill with a bill of 22 rupees to pay. Every stop on the way
> down charges you its number. You can only stop and check your wallet at a **dead
> end**, a place with no more paths down.
>
> ```
> start: owe 22
> at 5:  owe 17
> at 4:  owe 13
> at 11: owe 2
> at 7:  owe -5    dead end, overpaid. no good. walk back up.
> at 2:  owe 0     dead end, exactly paid. FOUND IT.
> ```
>
> Resting halfway down the hill doesn't count, even if the bill happens to be 0 there.
> You have to reach a dead end.

## 🐌 Brute force (say it, don't type it)
Collect every root-to-leaf path into a list, sum each one, check for the target.
**O(n · h)** for building the paths, and wasteful because it stores entire paths when
all you need is one running number, and because it keeps going after the answer is
found. There's no asymptotically bad version of this problem; the lesson is carrying
state **down**.

## 💡 The pattern reveal
**Signal:** "**root to leaf**", "path sum".
**Therefore:** DFS, and the first **top-down** problem of the group: information flows
from parent to child as an argument, not from child to parent as a return.

| | Validation group (EP138–144) | Path Sum group (EP145–147) |
|---|---|---|
| direction | bottom-up: children report to the parent | top-down: parent hands a total to the children |
| lives in | the return value | a parameter |

**Key insight:** subtract as you go. `remaining = target - node.val`. Then a leaf
succeeds iff `remaining == 0`, and every other node asks: *does either child succeed
with what's left?*

## 🔍 Dry run: `[5,4,8,11,null,13,4,7,2,null,null,null,1]`, target 22

| step | node | remaining after subtracting | leaf? | result |
|---|---|---|---|---|
| 1 | 5 | 22 − 5 = 17 | no | ask 4 |
| 2 | 4 | 17 − 4 = 13 | no | ask 11 (right is `None`, only reached if left fails) |
| 3 | 11 | 13 − 11 = 2 | no | ask 7 |
| 4 | 7 | 2 − 7 = **−5** | yes | **False** → ask 2 |
| 5 | 2 | 2 − 2 = **0** | yes | **True** |
| 6 | 11, 4, 5 | - | - | `or` short-circuits: True all the way up |

Answer **True** ✓. The entire right half of the tree, 8, 13, 4 and 1, is never visited,
because `or` stops as soon as the left side says True.

## ✅ Optimal solution
```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """Some root-to-leaf path sums to targetSum.

        Time:  O(n), each node at most once; stops at the first match.
        Space: O(h), the recursion stack.
        """
        if not root:
            return False

        remaining = targetSum - root.val
        if not root.left and not root.right:        # a leaf: the bill must be exact
            return remaining == 0

        return (self.hasPathSum(root.left, remaining)
                or self.hasPathSum(root.right, remaining))
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Check at a leaf, not at `None`.** Writing `if not root: return targetSum == 0` looks
  elegant and is wrong: on `[1,2]` with target 1, the root's missing right child returns
  `1 - 1 == 0`, True, but 1 alone isn't a root-to-leaf path. Same one-child trap as
  EP138.
- **Empty tree is False**, even for target 0. There's no path at all. The `if not root:
  return False` handles it, and it's also what a missing child returns.
- **Negatives mean no early pruning.** You can't stop when `remaining < 0`, because a
  later negative value might bring it back. `[-2, null, -3]` with target -5 is True.
- **`or`, not `and`.** Any one path is enough.
- **Subtract `root.val` before the leaf check.** Checking `targetSum == 0` at the leaf
  without subtracting the leaf's own value is an off-by-one-node error.

## 🎤 Interview talking points
- *"Top-down DFS carrying the remaining sum. At a leaf, check it's exactly zero;
  otherwise ask both children with what's left, and `or` the answers."*
- *"The check must be at a leaf, not at a null. A node with one child isn't the end of a
  path."* ← the bug they're looking for.
- *"I can't prune on a negative remainder because values can be negative."*
- *"O(n) time, O(h) space, and it stops at the first path found."*

## 🔗 Transfer
The bottom-up group (EP139–141) returned a number to the parent. Today the number goes
**down** as an argument. Tomorrow, EP146 Path Sum II, asks for every matching path, not
just whether one exists, so you carry the path itself down as well, and that brings
back Pattern 12's choose / explore / unchoose: `append` on the way down, `pop` on the
way up, `path[:]` when you record.

## 📹 Metadata
- **Title:** `Path Sum, subtract on the way down, check at a leaf | Trees #25`
- **Thumbnail:** `LEAF, not None` (orange block)
- **Short:** `[1,2]` with target 1, the `None` check saying True and the leaf check
  saying False. 35s.
