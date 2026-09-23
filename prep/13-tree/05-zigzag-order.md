# EP125 · P13E05 · Binary Tree Zigzag Level Order Traversal   [Medium]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

---

## 🎬 Hook
> "Zigzag looks like you have to change how you walk the tree: left to right, then
> right to left, then back. You don't. **Walk every level the normal way, and flip the
> list you wrote down on the odd ones.** The tree never knows."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its level order traversal,
but alternate direction:
  level 0 left to right, level 1 right to left, level 2 left to right, ...

An empty tree returns [].
```

## 🔢 The example
```
        3
       / \          Input:  root = [3, 9, 20, null, null, 15, 7]
      9   20        Output: [[3], [20, 9], [15, 7]]
         /  \       Why:    level 1 is read right to left
        15   7

          1
        /   \       Input:  [1, 2, 3, 4, 5, 6, 7]
       2     3      Output: [[1], [3, 2], [4, 5, 6, 7]]
      / \   / \
     4   5 6   7
```

## 🧸 ELI5
> A farmer ploughing a field row by row. He doesn't teleport back to the left edge at
> the end of each row, he turns around and ploughs the next row coming back. Left,
> right, left, right.
>
> But the **field** is the same field. The rows are still the same rows. Only the
> direction he *writes them down* changes. So: collect every row the normal way, and
> on every second row, flip the notebook entry before you save it.

## 🐌 Brute force (say it, don't type it)
Honestly, the "clever" version is the one to avoid: two stacks, or pushing children
right-first on odd levels. It's easy to get the child order wrong and the tree walks
correctly for 3 levels and breaks on the 4th. The simple version, EP124 plus a
`reverse()`, costs the same **O(n)** and has nothing to get wrong.

## 💡 The pattern reveal
**Signal:** "level order" + "alternate" / "zigzag".
**Therefore:** Shape B unchanged, one post-processing line per level.

**Key insight:** the direction only affects the **output**, never the traversal. Keep
enqueuing left then right, always. Reverse `level` when the level index is odd.

```python
if len(result) % 2 == 1:     # the level about to be added is level 1, 3, 5, ...
    level.reverse()
result.append(level)
```

`len(result)` is a free level counter: it's the index the next level will land at.

## 🔍 Dry run: `root = [1, 2, 3, 4, 5, 6, 7]`

| round | queue at start | `level` as collected | `len(result)` | reverse? | appended |
|---|---|---|---|---|---|
| 1 | `[1]` | `[1]` | 0 | no | `[1]` |
| 2 | `[2, 3]` | `[2, 3]` | 1 | **yes** | `[3, 2]` |
| 3 | `[4, 5, 6, 7]` | `[4, 5, 6, 7]` | 2 | no | `[4, 5, 6, 7]` |

Result **`[[1], [3, 2], [4, 5, 6, 7]]`** ✓. Look at round 3's queue: `[4, 5, 6, 7]`,
still left to right, even though round 2 was *written* right to left. The traversal
was never disturbed.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Level order, with every odd level reversed.

        Time:  O(n), each node once, plus reversing each level (total n).
        Space: O(w) for the queue.
        """
        if not root:
            return []
        queue, result = deque([root]), []

        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            if len(result) % 2 == 1:        # odd level: read right to left
                level.reverse()
            result.append(level)

        return result
```
**Time:** O(n) · **Space:** O(w)

## ⚠️ Gotchas
- **Don't change the enqueue order.** Swapping to right-then-left on odd levels reverses
  *that* level correctly and scrambles every level below it.
- **Level 0 is left to right.** `% 2 == 1` reverses levels 1, 3, 5. Using `== 0`
  reverses the root level (harmless, one element) and every level after it wrong.
- **Reversing costs O(level size)**, so the total is still O(n). If an interviewer
  worries about it, write into a `deque` with `appendleft` on odd levels instead. Same
  complexity, no separate pass.

## 🎤 Interview talking points
- *"The zigzag only changes how each level is recorded, not how it's traversed. I run
  normal level order and reverse the odd levels."*
- *"`len(result)` doubles as the level index, so there's no extra counter."*
- *"O(n): the reversals add up to n in total."*
- *"If they want no reversal, I fill each level with a deque, `append` on even levels
  and `appendleft` on odd."*

## 🔗 Transfer
Same trick, different place, tomorrow: EP126 Level Order II reverses the **whole
result** instead of each level. After that, the Mirror family (EP127 to EP131) goes back
to DFS and compares two trees at once, with EP127 Invert Tree swapping children for
real, not just in the output.

## 📹 Metadata
- **Title:** `ZigZag Level Order, the tree never zigzags | Trees #5`
- **Thumbnail:** `.reverse()` on odd rows
- **Short:** the queue staying `[4, 5, 6, 7]` while the output flips. 30s.
