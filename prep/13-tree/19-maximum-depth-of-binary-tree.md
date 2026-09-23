# EP139 · P13E19 · Maximum Depth of Binary Tree   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/description/

---

## 🎬 Hook
> "This is the most important three lines in the whole tree series. `if not node: return
> 0`, then `return 1 + max(left, right)`. Every hard tree problem coming up, balanced,
> diameter, maximum path sum, is these three lines with one extra line bolted on. Learn
> this one so well you could type it asleep."

## 📋 Problem, in your words
```
Given the root of a binary tree, return its maximum depth:
the number of NODES on the longest path from the root down to a leaf.

  - an empty tree has depth 0
  - a single node has depth 1
```

## 🔢 The example
```
Input:  [3,9,20,null,null,15,7]
Output: 3

          3          depth 1
         / \
        9   20       depth 2
           /  \
          15   7     depth 3   <- the deepest leaves

Input:  [1,null,2]   ->  2
Input:  []           ->  0
```

## 🧸 ELI5
> Ask the boss of a company "how many layers of management are there?". The boss doesn't
> know. So they ask each of their two direct reports the same question, take the
> **bigger** answer, and add **one for themselves**.
>
> Each report does the exact same thing with their own reports. Someone with nobody
> under them? They... still add one for themselves. And an **empty chair** (nobody
> there at all) answers **0**.
>
> ```
> 15 says: my reports are empty chairs, max(0, 0) + 1 = 1
>  7 says: 1
> 20 says: max(1, 1) + 1 = 2
>  9 says: max(0, 0) + 1 = 1
>  3 says: max(1, 2) + 1 = 3   <- the answer
> ```

## 🐌 Brute force (say it, don't type it)
List every root-to-leaf path and take the longest. It's O(n) in time but builds every
path explicitly, O(n · h) memory in the worst case, for a question whose answer is a
single number. There isn't a genuinely slow version of this problem; the lesson is the
*shape* of the clean answer.

## 💡 The pattern reveal
**Signal:** a number computed from **both children**, "depth".
**Therefore:** Shape D, bottom-up. The pattern card's one design question: *what does
this node need from its children, and what does it hand back?*

| | answer |
|---|---|
| needs from children | their depths, `L` and `R` |
| hands back to parent | `1 + max(L, R)` |
| base case | `None` → `0` |

**Key insight:** you don't compute depth *from the top down*. You let the leaves answer
first and the answers **flow up**. That's postorder: both calls finish before this node
does its one line of work.

## 🔍 Dry run: `[3,9,20,null,null,15,7]`

The calls in the order they **return** (postorder):

| step | node | L | R | returns `1 + max(L, R)` |
|---|---|---|---|---|
| 1 | 9 | 0 (`None`) | 0 (`None`) | **1** |
| 2 | 15 | 0 | 0 | **1** |
| 3 | 7 | 0 | 0 | **1** |
| 4 | 20 | 1 (from 15) | 1 (from 7) | **2** |
| 5 | 3 | 1 (from 9) | 2 (from 20) | **3** |

Answer **3** ✓. Root 3 is the first node *called* and the last to *return*. That
"first in, last out" is the call stack, and it's why this is O(h) space.

## ✅ Optimal solution
```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """Nodes on the longest root-to-leaf path, computed bottom-up.

        Time:  O(n), every node is visited once.
        Space: O(h), the recursion stack; O(n) for a skewed tree.
        """
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```
**Time:** O(n) · **Space:** O(h)

BFS version (count levels), for when they ask for iterative:

```python
if not root:
    return 0
queue, depth = deque([root]), 0
while queue:
    depth += 1
    for _ in range(len(queue)):
        node = queue.popleft()
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
return depth
```

## ⚠️ Gotchas
- **`None` returns 0, not 1 and not -1.** 0 makes a leaf come out as 1 automatically.
  If a problem counts **edges** instead of nodes (EP141 Diameter does), the numbers shift
  by one. Know which you're counting.
- **The null check is the first line.** Before `.left`, before `.right`. Pattern card
  gotcha #1.
- **`max` is safe here, `min` isn't.** A missing child's 0 never wins a `max`. It does
  win a `min`, which is exactly the EP138 trap. Mention it.
- **Deep skewed trees hit Python's recursion limit** (1000 by default). On an interview
  whiteboard, say it; in production, use the BFS version.

## 🎤 Interview talking points
- *"Bottom-up: each node asks its children for their depths and returns one plus the
  bigger. The empty tree is depth zero."*
- *"It's a postorder: both children answer before the node can."*
- *"O(n) time, O(h) space for the stack, which is O(log n) balanced and O(n) skewed. If
  recursion depth is a concern, BFS counting levels gives the same answer."*
- *"This return-a-value-from-both-children template is what Balanced and Diameter build
  on."* ← sets up the next two episodes.

## 🔗 Transfer
Yesterday's EP138 needed BFS because the **nearest** leaf wins. Today the **farthest**
leaf wins, so every node must be seen and the recursion is simplest. Tomorrow, EP140
Balanced Binary Tree, is this exact function with one extra check; EP141 Diameter is
this function plus one line that records `L + R`. EP148 Maximum Path Sum is the same
again, with values instead of counts.

## 📹 Metadata
- **Title:** `Maximum Depth, the three lines every tree problem uses | Trees #19`
- **Thumbnail:** `1 + max(L, R)` (green block)
- **Short:** the ELI5 managers answering upward, ending with 3. 35s.
