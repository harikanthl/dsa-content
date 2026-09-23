# EP136 · P13E16 · Two Sum IV, Input is a BST   [Easy]

**Pattern:** Tree (Search) · **Link:** https://leetcode.com/problems/two-sum-iv-input-is-a-bst/description/

---

## 🎬 Hook
> "Episode one of this whole series was Two Sum on a **sorted array**, two pointers from
> the ends. Here's the same problem on a BST. You don't need a new idea. One inorder
> walk turns the tree **into** that sorted array, and then it's EP1."

## 📋 Problem, in your words
```
Given the root of a BST and an integer k, return True if there are two
DIFFERENT nodes whose values add up to k.

The same node can't be used twice.
```

## 🔢 The example
```
          5
         / \          Input:  root = [5, 3, 6, 2, 4, null, 7], k = 9
        3   6         Output: True     (2 + 7, or 3 + 6, or 4 + 5)
       / \   \
      2   4   7       Input:  k = 28   Output: False  (largest pair is 6 + 7 = 13)

Input:  [1], k = 2    Output: False  (1 + 1 would reuse the same node)
```

## 🧸 ELI5
> The BST is a messy bookshelf, except it isn't really messy: if you read it in the
> right order (left, me, right), the books come out **sorted**.
>
> So read them out in that order and line them up on a table: `2 3 4 5 6 7`. Now it's
> the game from the very first episode. One finger on the smallest, one on the
> biggest. Too small? Move the left finger right. Too big? Move the right finger left.

## 🐌 Brute force (say it, don't type it)
For every node, search the BST for `k - node.val` with EP133's walk: **O(n · h)**, so
O(n log n) balanced and O(n²) skewed. The hash-set version (DFS, check if
`k - val` was seen, then add `val`) is a legitimate **O(n)** answer and works on any
tree, BST or not. The inorder + two pointers version is also O(n), and it's the one
that **uses** the BST, which is why this episode is in the Search family.

## 💡 The pattern reveal
**Signal:** "BST" + "two values that sum to k".
**Therefore:** Shape E (inorder is sorted) → Pattern 01 opposite-ends two pointers.

```python
vals = inorder(root)                  # sorted, because it's a BST
lo, hi = 0, len(vals) - 1
while lo < hi:
    s = vals[lo] + vals[hi]
    if s == k:  return True
    if s < k:   lo += 1               # need bigger: move the small end up
    else:       hi -= 1               # need smaller: move the big end down
return False
```

**Key insight:** `lo < hi` (strictly) is what enforces "two **different** nodes". The
pointers can never land on the same index, so `[1], k = 2` can't pair 1 with itself.

## 🔍 Dry run: `root = [5, 3, 6, 2, 4, null, 7]`, `k = 11`

Inorder: `vals = [2, 3, 4, 5, 6, 7]`.

| step | lo | hi | `vals[lo] + vals[hi]` | vs 11 | move |
|---|---|---|---|---|---|
| 1 | 0 (2) | 5 (7) | 9 | too small | lo → 1 |
| 2 | 1 (3) | 5 (7) | 10 | too small | lo → 2 |
| 3 | 2 (4) | 5 (7) | 11 | **equal** | **return True** ✓ |

For `k = 28`: the sum starts at 9 and only ever increases by moving `lo` right, until
`lo` meets `hi` at 5. Never reaches 28 → False.

## ✅ Optimal solution
```python
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        """Inorder gives a sorted list; opposite-ends two pointers finds the pair.

        Time:  O(n), one traversal plus one two-pointer sweep.
        Space: O(n) for the sorted list.
        """
        vals, stack, node = [], [], root
        while stack or node:                # iterative inorder, EP121
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            vals.append(node.val)
            node = node.right

        lo, hi = 0, len(vals) - 1
        while lo < hi:                      # strict: two DIFFERENT nodes
            total = vals[lo] + vals[hi]
            if total == k:
                return True
            if total < k:
                lo += 1
            else:
                hi -= 1
        return False
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`lo < hi`, not `lo <= hi`.** With `<=`, a single node of value `k/2` pairs with
  itself. `[1], k = 2` must be False.
- **Inorder, specifically.** Preorder of a BST is not sorted, and two pointers on
  unsorted data silently gives wrong answers.
- **The hash-set answer is also O(n)**; don't argue against it if the interviewer
  proposes it. Say why you chose this one: it uses the BST and it's the same code as
  EP1.
- **O(h) space follow-up:** instead of materialising the list, run two iterative inorder
  stacks, one forward (smallest first) and one backward (largest first), and advance
  whichever the sum says. That's LeetCode's BST Iterator (173) twice.

## 🎤 Interview talking points
- *"A BST's inorder is sorted, so I flatten it and run the sorted-array two-sum: two
  pointers from the ends."*
- *"`lo < hi` guarantees two distinct nodes."*
- *"O(n) time and space. A hash set also works in O(n) and doesn't need the BST. If
  they want O(h) space, I'd use two BST iterators, one from each end."* ← covers all
  three follow-ups.

## 🔗 Transfer
This is the first time a tree problem has been solved by turning it into a **different
pattern's** problem, and it won't be the last. Tomorrow, EP137 Kth Smallest in a BST,
uses the same inorder walk but **stops early**, which is why the iterative version from
EP121 matters. EP143 Validate BST checks the same "inorder is sorted" fact from the
other direction.

## 📹 Metadata
- **Title:** `Two Sum on a BST, it's Episode 1 again | Trees #16`
- **Thumbnail:** `BST → [2 3 4 5 6 7]`
- **Short:** the tree flattening into a sorted row, then two fingers closing in. 40s.
