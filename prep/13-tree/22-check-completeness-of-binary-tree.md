# EP142 · P13E22 · Check Completeness of a Binary Tree   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/check-completeness-of-a-binary-tree/description/

---

## 🎬 Hook
> "A complete tree fills up like reading a book: left to right, top to bottom, no gaps.
> So read it like a book. Do level order, **push the empty children too**, and the rule
> is one line: once you've seen an empty spot, you should never see a real node again."

## 📋 Problem, in your words
```
Given the root of a binary tree, return True if it is COMPLETE:

  every level is completely full, except possibly the last,
  and the last level's nodes are packed as far LEFT as possible.

In other words: reading the tree level by level, left to right,
there are no holes before the last node.
```

## 🔢 The example
```
Input:  [1,2,3,4,5,6]          ->  True

            1
          /   \
         2     3
        / \   /
       4   5 6            <- last level packed to the left

Input:  [1,2,3,4,5,null,7]     ->  False

            1
          /   \
         2     3
        / \     \
       4   5  _  7        <- a HOLE where 3's left child should be, then 7

Reading order:  1 2 3 4 5 _ 7   <- a real node after a gap
```

## 🧸 ELI5
> Cinema seats are filled strictly in order: row 1 left to right, then row 2 left to
> right, and so on. You're the usher checking nobody broke the rule.
>
> You walk the seats **in that same order**. The first empty seat you see is fine,
> maybe the cinema just isn't full. But if you ever see a person sitting **after** an
> empty seat, someone skipped ahead. Rule broken.
>
> ```
> 1 2 3 4 5 6 _ _ _ ...    fine: all the gaps are at the end
> 1 2 3 4 5 _ 7            broken: 7 is sitting after a gap
> ```

## 🐌 Brute force (say it, don't type it)
Count the nodes, n. Give every node a position number: root is 1, the children of `i`
are `2i` and `2i + 1` (the heap layout from Pattern 11). The tree is complete iff the
biggest position is exactly n. That's actually **O(n)** and a fine answer. Mention it
as the "heap indexing" view. The BFS version is more direct and doesn't need the second
number.

## 💡 The pattern reveal
**Signal:** "complete", a question about **position within a level**.
**Therefore:** BFS, Shape B, with the pattern card's completeness twist: push `None`
children too.

**Key insight:** BFS already visits positions in exactly the "book order" that
completeness is defined by. If you let the empty children into the queue as `None`, the
queue *is* that reading order, gaps included. Then:

```python
if node is None:
    seen_gap = True
elif seen_gap:
    return False          # a real node after a gap
```

DFS can't do this naturally. A DFS goes deep first, and completeness is a
left-to-right-across-a-level property.

## 🔍 Dry run: `[1,2,3,4,5,null,7]`

| step | pop | seen_gap before | action | queue after |
|---|---|---|---|---|
| 1 | 1 | F | push 2, 3 | `[2, 3]` |
| 2 | 2 | F | push 4, 5 | `[3, 4, 5]` |
| 3 | 3 | F | push `None`, 7 | `[4, 5, None, 7]` |
| 4 | 4 | F | push `None`, `None` | `[5, None, 7, None, None]` |
| 5 | 5 | F | push `None`, `None` | `[None, 7, None, None, None, None]` |
| 6 | `None` | F | **seen_gap = True** | `[7, None, None, None, None]` |
| 7 | 7 | **T** | real node after a gap → **return False** | - |

Answer **False** ✓.

For `[1,2,3,4,5,6]`, the first `None` is 3's right child, popped after 6, and every
pop after it is also `None`. The loop drains and returns **True**.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def isCompleteTree(self, root: Optional[TreeNode]) -> bool:
        """Level order including empty children; no real node may follow a gap.

        Time:  O(n), each node pushed and popped once (plus n + 1 None slots).
        Space: O(w), the widest level, with its None placeholders.
        """
        queue = deque([root])
        seen_gap = False

        while queue:
            node = queue.popleft()
            if node is None:
                seen_gap = True
            else:
                if seen_gap:
                    return False            # someone sat down after an empty seat
                queue.append(node.left)     # push children even when None:
                queue.append(node.right)    # the gaps are the whole point

        return True
```
**Time:** O(n) · **Space:** O(w)

## ⚠️ Gotchas
- **Push `None` children.** The normal BFS template has `if node.left:` guards. Keep
  them and you'll never see a gap, so every tree looks complete.
- **No `range(len(queue))` needed.** You don't care where one level ends; completeness is
  one continuous reading order across all levels. Per-level loops add nothing here.
- **The first gap is not a failure.** A tree whose last level is half full is complete.
  Only a real node *after* a gap fails.
- **A missing left child with a present right child** fails too, and the same rule
  catches it: the left `None` is enqueued before the right node.
- **Can stop early.** Once `seen_gap` is set, everything left must be `None`. The loop
  above keeps going to check exactly that; a real node ends it immediately.

## 🎤 Interview talking points
- *"Completeness is defined in level order, so I do level order and include the empty
  children. The tree is complete iff no real node appears after the first empty slot."*
- *"The alternative is heap indexing: root is 1, children 2i and 2i+1, and it's complete
  iff the largest index equals the node count."* ← shows you know why heaps are stored
  in arrays.
- *"O(n) time, O(w) space."*

## 🔗 Transfer
This is exactly why a heap (Pattern 11) can live in a flat array: a complete tree has no
gaps, so index `i`'s children are always at `2i + 1` and `2i + 2`. Today you checked
that property. Tomorrow, EP143 Validate BST, checks a different one, the ordering rule,
and it's the problem where comparing with just the parent looks right and fails.

## 📹 Metadata
- **Title:** `Complete Binary Tree, the usher and the empty seat | Trees #22`
- **Thumbnail:** `_ then 7 = ✗` (red block)
- **Short:** the reading order `1 2 3 4 5 _ 7`, with 7 flashing red. 30s.
