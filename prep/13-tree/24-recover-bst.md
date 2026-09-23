# EP144 · P13E24 · Recover Binary Search Tree   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/recover-binary-search-tree/description/

---

## 🎬 Hook
> "Two nodes in a BST got swapped by mistake. Find them without looking at the tree at
> all: look at its **inorder**, which should be sorted. Swapping two numbers in a sorted
> list leaves one or two places where it goes **down** instead of up. The first bad
> number is the big one at the first drop; the second is the small one at the last
> drop. Swap their values and you're done."

## 📋 Problem, in your words
```
The values of exactly TWO nodes of a BST were swapped by mistake.
Fix the tree in place, without changing its structure.

  - return nothing; modify the tree
  - follow-up: O(1) extra space (Morris traversal)
```

## 🔢 The example
```
Input:  [4,6,2,1,3,5,7]              (2 and 6 were swapped)
Output: [4,2,6,1,3,5,7]

          4                      4
        /   \                  /   \
       6     2       ->       2     6
      / \   / \              / \   / \
     1   3 5   7            1   3 5   7

inorder:  1  6  3  4  5  2  7
             ^^^^        ^^^^
             drop 1      drop 2       swapped: 6 (first drop's LEFT)
                                               2 (last drop's RIGHT)

Input:  [3,1,4,null,null,2]  ->  [2,1,4,null,null,3]
inorder:  1  3  2  4      <- ONE drop: the swapped pair were neighbours
```

## 🧸 ELI5
> A row of kids is lined up by height, shortest to tallest. While you weren't looking,
> two of them swapped places. Walk down the line and watch for the moment someone is
> **shorter than the kid before them**.
>
> ```
> 1  6  3  4  5  2  7
>    6 > 3 : the 6 is too tall for this spot   <- culprit #1 is the one BEFORE the drop
>             5 > 2 : the 2 is too short        <- culprit #2 is the one AFTER the drop
> ```
>
> If the two swapped kids were standing **next to each other**, there's only one drop,
> and the two culprits are the two kids on either side of it.

## 🐌 Brute force (say it, don't type it)
Inorder into a list, sort a copy, walk the tree inorder again and overwrite each value
with the sorted one. **O(n log n)** time, **O(n)** space. Works, and it rewrites values
that were never wrong. The inorder already tells you *exactly* which two are out of
place; you only need to find them.

## 💡 The pattern reveal
**Signal:** "binary **search** tree" + two values **out of order**.
**Therefore:** Shape E, the inorder walk with a `prev` pointer. The pattern card's row:
*"find the two places where `prev > node`; those are the swapped nodes."*

**Key insight:** in a sorted sequence, swapping positions `i < j` creates a drop at
`i` (the big value is now early) and a drop just before `j` (the small value is now
late). If `j = i + 1` those are the same drop.

```python
if prev and prev.val > node.val:      # a drop
    if first is None:
        first = prev                  # first drop: the too-big value is prev
    second = node                     # every drop: the too-small value is node
```

Setting `second` on **every** drop handles both cases with no `if`: one drop, and
`second` is that drop's node; two drops, and the second drop overwrites it.

## 🔍 Dry run: `[4,6,2,1,3,5,7]`

Iterative inorder, same loop as EP137:

| visit | node | prev | `prev > node`? | first | second |
|---|---|---|---|---|---|
| 1 | 1 | - | - | - | - |
| 2 | 6 | 1 | no | - | - |
| 3 | 3 | 6 | **yes** (drop 1) | **6** | 3 |
| 4 | 4 | 3 | no | 6 | 3 |
| 5 | 5 | 4 | no | 6 | 3 |
| 6 | 2 | 5 | **yes** (drop 2) | 6 | **2** |
| 7 | 7 | 2 | no | 6 | 2 |

Swap `first.val` and `second.val`: 6 ↔ 2. Inorder is now `1 2 3 4 5 6 7` ✓.

On `[3,1,4,null,null,2]`: inorder `1 3 2 4`, one drop at (3, 2), so `first = 3`,
`second = 2`, swap → `[2,1,4,null,null,3]` ✓.

## ✅ Optimal solution
```python
class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        """Find the two swapped nodes via the drops in inorder; swap their values.

        Time:  O(n), one inorder pass.
        Space: O(h), the stack. (Morris traversal gets it to O(1).)
        """
        first = second = prev = None
        stack, node = [], root

        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()

            if prev and prev.val > node.val:    # inorder went DOWN: a drop
                if first is None:
                    first = prev                # the too-big one, at the first drop
                second = node                   # the too-small one, at the last drop

            prev = node
            node = node.right

        first.val, second.val = second.val, first.val
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **`first = prev`, `second = node`.** At the first drop the culprit is the **earlier**
  (too big) one; at the last drop it's the **later** (too small) one. Taking `node` at
  the first drop swaps 3 with 2 in the example, and the tree stays broken.
- **Adjacent swap = one drop.** If your code only sets `second` on a second drop,
  `[3,1,4,null,null,2]` crashes with `second = None`. Setting `second` on every drop
  handles it.
- **Swap values, not nodes.** "Without changing the structure." Re-linking nodes is
  harder and not asked for.
- **Keep `prev` as a node, not a value**, because you need to write to it later.
- **Don't stop at the first drop.** You don't yet know whether a second one is coming.

## 🎤 Interview talking points
- *"Inorder of a BST is sorted. Two swapped values leave one or two drops in that
  sequence. The first swapped node is the larger side of the first drop, the second is
  the smaller side of the last drop."*
- *"I record `second` on every drop, which covers the adjacent case where there's only
  one."*
- *"O(n) time, O(h) space with a stack. For O(1) space: Morris traversal, which
  temporarily threads each node's inorder predecessor back to it instead of using a
  stack."* ← the follow-up; name it even if you don't code it.

## 🔗 Transfer
EP137 used the inorder walk to **count**; EP143 used it (the alternate version) to
**check** `prev < node`. Today it **locates** the two violations. Same eight-line loop,
three jobs. That closes the Validation group. Tomorrow starts Path Sum, EP145, and the
direction of information flips: instead of children reporting **up**, the parent
passes a running total **down**.

## 📹 Metadata
- **Title:** `Recover BST, the two drops in a sorted line | Trees #24`
- **Thumbnail:** `1 6 3 4 5 2 7` with 6 and 2 circled (red)
- **Short:** the ELI5 line of kids, two drops flashing, 6 and 2 swapping back. 40s.
