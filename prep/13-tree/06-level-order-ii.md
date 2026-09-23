# EP126 · P13E06 · Binary Tree Level Order Traversal II   [Medium]

**Pattern:** Tree (Traversal) · **Link:** https://leetcode.com/problems/binary-tree-level-order-traversal-ii/description/

> **Homework episode.** Short format: it's EP124 with one change. State the change,
> show why `appendleft` beats inserting at 0 on a list, hand it over. Aim for 5 to 7
> minutes.

---

## 🎬 Hook
> "Level order, but from the bottom up. Your first instinct is to start at the leaves.
> Don't: you can't find the leaves without walking down first. **Walk top-down exactly
> like before, and just stack the levels in the other order.**"

## 📋 Problem, in your words
```
Given the root of a binary tree, return its level order traversal from
the BOTTOM level up to the root. Within each level, still left to right.

An empty tree returns [].
```

## 🔢 The example
```
        3
       / \          Input:  root = [3, 9, 20, null, null, 15, 7]
      9   20        Output: [[15, 7], [9, 20], [3]]
         /  \       Why:    same rows as EP124, listed deepest first;
        15   7              each row is still left to right

Input:  [1]         Output: [[1]]
Input:  []          Output: []
```

## 🧸 ELI5
> Stacking plates. You wash the plates in order, top row first, and put each clean
> plate **on top of the pile**. When you're done, the last one you washed is on top.
>
> The levels are the plates. You still visit them top-down, but each finished level
> goes on the **front** of the answer, so the deepest one ends up first.

## 🐌 Brute force (say it, don't type it)
Run EP124, then `result.reverse()`. That's **O(n)** and completely acceptable. The only
real trap is the "almost right" version: `result.insert(0, level)` on a Python list,
which shifts everything each time and is O(levels²). A `deque` with `appendleft` is the
clean fix.

## 💡 The pattern reveal
**Signal:** "level order" + "bottom-up" / "from leaf to root".
**Therefore:** Shape B, with one change to where each level is stored.

**Key insight:** direction of **output** is not direction of **traversal**. Same lesson
as EP125, one level of zoom out: yesterday we flipped inside a level, today we flip the
list of levels.

```python
result = deque()
...
result.appendleft(level)       # was result.append(level) in EP124
...
return list(result)
```

## 🔍 Dry run: `root = [3, 9, 20, null, null, 15, 7]`

| round | queue at start | `level` | `result` after `appendleft` |
|---|---|---|---|
| 1 | `[3]` | `[3]` | `[[3]]` |
| 2 | `[9, 20]` | `[9, 20]` | `[[9, 20], [3]]` |
| 3 | `[15, 7]` | `[15, 7]` | `[[15, 7], [9, 20], [3]]` ✓ |

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        """Level order traversal, deepest level first.

        Time:  O(n), each node once; appendleft is O(1).
        Space: O(w) for the queue, plus the output.
        """
        if not root:
            return []
        queue, result = deque([root]), deque()

        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.appendleft(level)        # newest level goes to the front

        return list(result)
```
**Time:** O(n) · **Space:** O(w)

## ⚠️ Gotchas
- **Reverse the list of levels, not the values.** `result.reverse()` is right.
  Reversing each `level` as well gives `[[7, 15], [20, 9], [3]]`, which is wrong: each
  level stays left to right.
- **`list.insert(0, ...)` is O(len)** each time. Use `deque.appendleft`, or append and
  reverse once at the end.
- **Return a list.** LeetCode accepts the deque, but `list(result)` matches the
  signature and doesn't surprise anyone.

## 🎤 Interview talking points
- *"I can't start from the leaves, so I traverse top-down as usual and put each level
  at the front of the answer."*
- *"`deque.appendleft` keeps it O(n). A list insert at 0 would be quadratic in the
  number of levels."*

## 🔗 Transfer
That closes Traversal: three DFS orders (EP121 to EP123) and three BFS variants (EP124
to EP126). Tomorrow starts the Mirror family: EP127 Invert Tree, where we stop reading
the tree and start **changing** it.

## 📹 Metadata
- **Title:** `Level Order II, bottom-up without starting at the bottom | Trees #6 (homework)`
- **Thumbnail:** `appendleft`
- **Short:** the three levels landing on the front of the answer one by one. 20s.
