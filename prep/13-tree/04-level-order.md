# EP124 · P13E04 · Binary Tree Level Order Traversal   [Medium]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-level-order-traversal/description/

---

## 🎬 Hook
> "A queue will happily give you the nodes of a tree in level order. What it won't tell
> you is **where one level ends and the next begins**. One line fixes that:
> `for _ in range(len(queue))`. It reads the length **once**, and that single read is
> the whole episode."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its values level by level,
left to right, as a list of lists: one inner list per depth.

  - the root is level 0, its children level 1, and so on
  - an empty tree returns []
```

## 🔢 The example
```
        3
       / \          Input:  root = [3, 9, 20, null, null, 15, 7]
      9   20        Output: [[3], [9, 20], [15, 7]]
         /  \       Why:    one inner list per row of the drawing
        15   7

Input:  [1]         Output: [[1]]
Input:  []          Output: []
```

## 🧸 ELI5
> A school fire drill, one grade at a time. The teacher calls everyone in grade 1 to
> the door. As each grade-1 kid walks out, they shout the names of their younger
> siblings, who join the **back** of the line.
>
> Problem: the line now has grade-1 kids and grade-2 kids mixed together. How does
> the teacher know when grade 1 is finished?
>
> **She counts the line before anyone moves.** "There are 2 of you. I'll let exactly 2
> out." The siblings who joined during those 2 wait for the next count.
>
> ```
> line: [9, 20]        count = 2 -> let out 9, 20
>                      (20 adds 15, 7 to the back while leaving)
> line: [15, 7]        count = 2 -> next level
> ```

## 🐌 Brute force (say it, don't type it)
DFS with a `depth` parameter, appending each value to `res[depth]`. That's actually
fine, **O(n)**, and a good answer to "can you do it recursively?". What doesn't work is
a plain BFS that never counts: you get `[3, 9, 20, 15, 7]` flat and no way to tell the
levels apart afterwards. The count is the fix.

## 💡 The pattern reveal
**Signal:** the word **"level"**.
**Therefore:** Shape B, BFS with a queue.

**Key insight:** at the top of each outer loop, the queue holds **exactly one level**,
nothing more. So `len(queue)` right then is that level's size. Pop exactly that many;
their children, appended during the pops, are the next level and wait their turn.

```python
while queue:
    level = []
    for _ in range(len(queue)):      # len() is read ONCE, before any children are added
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    result.append(level)
```

## 🔍 Dry run: `root = [3, 9, 20, null, null, 15, 7]`

| outer loop | queue at start | `len` read | pops (and children added) | `level` | `result` |
|---|---|---|---|---|---|
| 1 | `[3]` | 1 | pop 3, add 9, 20 | `[3]` | `[[3]]` |
| 2 | `[9, 20]` | 2 | pop 9 (no kids); pop 20, add 15, 7 | `[9, 20]` | `[[3], [9, 20]]` |
| 3 | `[15, 7]` | 2 | pop 15; pop 7 | `[15, 7]` | `[[3], [9, 20], [15, 7]]` |
| 4 | `[]` | - | loop ends | | ✓ |

Row 2: after popping 20 the queue is `[15, 7]`, but the `for` only runs twice because
the `2` was fixed before the loop started. That's the boundary between levels.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Values grouped by depth, left to right.

        Time:  O(n), every node enqueued and dequeued once.
        Space: O(w), w = the widest level; up to n/2 on a full tree.
        """
        if not root:
            return []
        queue, result = deque([root]), []

        while queue:
            level = []
            for _ in range(len(queue)):     # exactly the nodes on THIS level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)

        return result
```
**Time:** O(n) · **Space:** O(w), O(n) worst case

## ⚠️ Gotchas
- **`deque`, not a list.** `list.pop(0)` is O(n), which makes the whole thing O(n²) on a
  wide tree. `deque.popleft()` is O(1).
- **`for _ in range(len(queue))` vs `while queue` inside.** An inner `while queue` would
  eat the next level too, and you'd get one giant level.
- **Empty tree.** Without `if not root: return []` you get `deque([None])` and a crash
  on `None.val`. The expected output is `[]`, not `[[]]`.
- **Left before right** when enqueuing, or every level comes out mirrored.

## 🎤 Interview talking points
- *"Level means BFS. I use a deque, and at the top of each round I read the queue's
  length once. That's exactly the current level."*
- *"O(n) time. Space is the widest level, which for a full tree is about n/2."*
- *"Recursively, I'd DFS with a depth argument and append to `result[depth]`. Same
  output, O(h) space instead of O(w)."* ← a good answer to the follow-up.

## 🔗 Transfer
This loop is the base of the next two episodes: EP125 ZigZag reverses every other
level, EP126 Level Order II reverses the result. It returns in EP138 Minimum Depth (stop
at the first leaf) and EP142 Completeness. Leave the tree and it's EP154 Graph BFS and
EP157 Rotten Oranges, where "one level" becomes "one minute".

## 📹 Metadata
- **Title:** `Level Order Traversal, the one line that finds the levels | Trees #4`
- **Thumbnail:** `len(queue)` (circled)
- **Short:** the queue holding `[9, 20]`, 20 adding 15 and 7, the count staying at 2. 45s.
