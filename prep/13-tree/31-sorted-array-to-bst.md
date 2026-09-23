# EP151 · P13E31 · Convert Sorted Array to Binary Search Tree   [Easy]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

---

## 🎬 Hook
> "The last two episodes had a traversal that **told** you the root. A sorted array
> tells you nothing: it's an inorder with the roots erased. So **you pick**. Pick the
> middle, and half the numbers go left, half go right, and the tree comes out balanced
> for free. It's binary search, building instead of searching."

## 📋 Problem, in your words
```
Given an integer array sorted in ascending order,
build a HEIGHT-BALANCED binary search tree from it.

  - height-balanced: at every node, subtree heights differ by at most 1
  - any valid answer is accepted (there can be several)
```

## 🔢 The example
```
Input:  [-10, -3, 0, 5, 9]
Output: [0,-10,5,null,-3,null,9]      (LeetCode also shows [0,-3,9,-10,null,5]:
                                        both are correct)

            0
           / \
        -10   5
           \    \
           -3    9

Input:  [1, 3]   ->  [1,null,3]   (or [3,1]: also balanced)
```

## 🧸 ELI5
> You're seating people in a tournament bracket by height, and you want it as even as
> possible. Who goes at the top? The person in the **middle** of the line: then exactly
> half are shorter (left side) and half are taller (right side).
>
> Then each half does the same thing: its middle person goes at the top of that half.
>
> ```
> [-10  -3  (0)  5   9]       0 is the middle: the root
>  [-10  -3]    [5   9]       each half picks its own middle
>   (-10) -3    (5)  9        -10 and 5 (the left-middle of each pair)
>          -3         9       what's left becomes their children
> ```
>
> Halving every time is why the tree's height ends up about log₂(n): the same halving
> that makes binary search fast.

## 🐌 Brute force (say it, don't type it)
Insert the values into an empty BST one by one, in the given order. It's a valid BST,
but inserting **sorted** values makes every new value the right child of the last one:
a straight line, height n, the least balanced tree possible. Then you'd need rotations
(AVL / red-black) to fix it. Say it to show *why* the order of choosing roots matters.

## 💡 The pattern reveal
**Signal:** "sorted array" + "**balanced** BST".
**Therefore:** Shape G, the degenerate case. The pattern card: *there's no preorder to
consult, so choose the root, `mid`, and recurse on the two halves.*

**Key insight:** a sorted array **is** the inorder of any BST built from it. Picking
index `mid` as the root automatically puts everything smaller on the left and
everything bigger on the right, so the BST rule holds. Picking the **middle**
specifically makes the two halves' sizes differ by at most 1, so the heights do too.

It's EP149's recursion with the hard part deleted:

| | EP149 | today |
|---|---|---|
| who is the root? | `preorder[pre_lo]`, given | `nums[mid]`, **chosen** |
| where's the split? | look it up: `idx[root.val]` | it's `mid`, you chose it |
| recurse on | two inorder ranges | two array ranges |

```python
mid = (lo + hi) // 2
root = TreeNode(nums[mid])
root.left  = rec(lo, mid - 1)
root.right = rec(mid + 1, hi)
```

## 🔍 Dry run: `[-10, -3, 0, 5, 9]`

| step | call `rec(lo, hi)` | range | `mid` | root | children |
|---|---|---|---|---|---|
| 1 | `rec(0, 4)` | `[-10,-3,0,5,9]` | 2 | **0** | `rec(0,1)`, `rec(3,4)` |
| 2 | `rec(0, 1)` | `[-10,-3]` | 0 | **−10** | `rec(0,-1)` → `None`, `rec(1,1)` |
| 3 | `rec(1, 1)` | `[-3]` | 1 | **−3** | both `None` |
| 4 | `rec(3, 4)` | `[5,9]` | 3 | **5** | `rec(3,2)` → `None`, `rec(4,4)` |
| 5 | `rec(4, 4)` | `[9]` | 4 | **9** | both `None` |

Tree: 0 → (−10 → (_, −3), 5 → (_, 9)) ✓. Height 3 for 5 nodes, and every node's
subtrees differ by at most 1.

With an even-length range, `(lo + hi) // 2` picks the **left** middle, so the extra
node goes right (step 2 and 4). `(lo + hi + 1) // 2` picks the right middle and gives
LeetCode's pictured answer. Both are balanced; both are accepted.

## ✅ Optimal solution
```python
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        """Height-balanced BST: the middle is the root, recurse on the halves.

        Time:  O(n), each value becomes a node once.
        Space: O(log n), the recursion depth of a balanced build (output excluded).
        """
        def rec(lo: int, hi: int) -> Optional[TreeNode]:
            if lo > hi:
                return None                 # empty range
            mid = (lo + hi) // 2            # the middle keeps both halves even
            root = TreeNode(nums[mid])
            root.left = rec(lo, mid - 1)    # everything smaller
            root.right = rec(mid + 1, hi)   # everything bigger
            return root

        return rec(0, len(nums) - 1)
```
**Time:** O(n) · **Space:** O(log n)

## ⚠️ Gotchas
- **Pass indices, not slices.** `nums[:mid]` and `nums[mid+1:]` copy the array at every
  level: O(n log n) time and more memory. It works, but say why you avoided it.
- **`mid - 1` and `mid + 1`.** Recursing on `(lo, mid)` puts the root in its own left
  subtree and, on a two-element range, loops forever.
- **Inclusive `hi = len(nums) - 1`**, so the empty check is `lo > hi`. With exclusive
  `hi = len(nums)`, it's `lo >= hi` and the recursion is `(lo, mid)` and `(mid + 1, hi)`.
  Pick one convention and don't mix, exactly as in Pattern 10.
- **There isn't one right answer.** Left-middle and right-middle both give valid,
  balanced trees. If your output doesn't match the picture, that's fine; say so.
- **Space is O(log n) only because the build is balanced.** That's a nice thing to point
  out: the same recursion on EP149 can be O(n) deep.

## 🎤 Interview talking points
- *"A sorted array is an inorder traversal. Choosing the middle as the root keeps the BST
  order and splits the rest evenly, so recursing on both halves gives a height-balanced
  tree."*
- *"I pass index ranges instead of slicing, so it's O(n) time and O(log n) stack."*
- *"Left-middle or right-middle both work; the answer isn't unique."*
- *"Follow-up, sorted **linked list** (LeetCode 109): no random access to the middle. Either
  find it with fast/slow pointers each time, O(n log n), or build inorder while walking
  the list once, O(n)."* ← ties back to Pattern 02.

## 🔗 Transfer
This closes Pattern 13. Thirty-one episodes, and every one was *what does this node need
from its children, and what does it hand back?* Today's answer: nothing from the
children, just a range from the parent. Tomorrow, EP152, starts Pattern 14, Graphs,
where a node can have any number of neighbours, there's no root, and cycles mean you
finally need a `visited` set. The DFS and BFS you've written thirty-one times carry
straight over; building the adjacency list is the new part.

## 📹 Metadata
- **Title:** `Sorted Array to BST, pick the middle, recurse | Trees #31`
- **Thumbnail:** `ROOT = MIDDLE` (green block)
- **Short:** the array splitting in half on screen while the tree grows below it. 30s.
