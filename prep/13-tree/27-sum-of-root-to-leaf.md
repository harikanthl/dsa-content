# EP147 · P13E27 · Sum Root to Leaf Numbers   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/sum-root-to-leaf-numbers/description/

---

## 🎬 Hook
> "Every root-to-leaf path in this tree spells a number: 4, 9, 5 is four hundred and
> ninety-five. Add them all up. You don't need strings, and you don't need to store any
> path. You need the line every calculator uses when you press a digit: **`acc = acc *
> 10 + digit`**. Carry that down, and each leaf hands back its finished number."

## 📋 Problem, in your words
```
Every node holds a digit 0-9. Each root-to-leaf path forms a number,
reading the digits from the root down.

Return the SUM of all those numbers.

  - a leaf is a node with NO children
  - the answer fits in a 32-bit int
```

## 🔢 The example
```
Input:  [4,9,0,5,1]
Output: 1026

          4
         / \
        9   0
       / \
      5   1

Why:    4 -> 9 -> 5  =  495
        4 -> 9 -> 1  =  491
        4 -> 0       =   40
                       -----
                        1026

Input:  [1,2,3]   ->  12 + 13 = 25
```

## 🧸 ELI5
> Typing a number on a calculator: you press 4, the screen says 4. You press 9, the
> screen doesn't say 13, it says 49: everything already there **shifts one place left**
> (× 10) and the new digit drops into the ones place (+ 9).
>
> ```
> screen = 0
> press 4:  0 * 10 + 4 =   4
> press 9:  4 * 10 + 9 =  49
> press 5: 49 * 10 + 5 = 495
> ```
>
> Walking down the tree is pressing digits. When you reach a dead end (a leaf), read the
> screen and add it to the total. When you back up to try the other branch, the screen
> goes back to what it was at that junction, for free, because each branch got its own
> copy of the screen.

## 🐌 Brute force (say it, don't type it)
Collect every root-to-leaf path as a string of digits, `int()` each one, sum them.
Correct, **O(n · h)** for building strings, and it stores every path. The running number
already *is* the path, compressed into one integer.

## 💡 The pattern reveal
**Signal:** "**root to leaf**" + building something along the way.
**Therefore:** top-down DFS, the same carry as EP145, but the carried value is a number
being **built**, not a sum being **paid off**.

| episode | carried down | at a leaf |
|---|---|---|
| EP145 Path Sum | `remaining = remaining - val` | `remaining == 0`? |
| EP146 Path Sum II | `remaining` and the `path` list | copy the path if it matches |
| **EP147 today** | `acc = acc * 10 + val` | return `acc` |

**Key insight:** it's top-down **and** bottom-up at once. The number flows **down** as an
argument; the finished numbers flow **up** as return values and get added at every
junction. `dfs(node, acc)` returns *the sum of all numbers in this subtree, given the
digits above it.*

Because `acc` is an int passed by value, the left branch can't corrupt the right
branch's copy. No `pop`, no undo.

## 🔍 Dry run: `[4,9,0,5,1]`

| step | call | `acc * 10 + val` | leaf? | returns |
|---|---|---|---|---|
| 1 | `dfs(4, 0)` | 0·10 + 4 = 4 | no | waits on children |
| 2 | `dfs(9, 4)` | 4·10 + 9 = 49 | no | waits |
| 3 | `dfs(5, 49)` | 49·10 + 5 = **495** | yes | **495** |
| 4 | `dfs(1, 49)` | 49·10 + 1 = **491** | yes | **491** |
| 5 | back in `dfs(9, 4)` | - | - | 495 + 491 = **986** |
| 6 | `dfs(0, 4)` | 4·10 + 0 = **40** | yes | **40** |
| 7 | back in `dfs(4, 0)` | - | - | 986 + 40 = **1026** |

Answer **1026** ✓. Step 4 is the one to point at: node 1 receives `acc = 49`, not 495.
The left sibling's digit never leaked, because nothing was shared.

## ✅ Optimal solution
```python
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        """Sum of the numbers spelled by every root-to-leaf path.

        Time:  O(n), each node once.
        Space: O(h), the recursion stack.
        """
        def dfs(node: Optional[TreeNode], acc: int) -> int:
            """Sum of all root-to-leaf numbers below node, given the digits above."""
            if not node:
                return 0                        # no path through here: adds nothing
            acc = acc * 10 + node.val           # shift left, drop the new digit in
            if not node.left and not node.right:
                return acc                      # a leaf: the number is finished
            return dfs(node.left, acc) + dfs(node.right, acc)

        return dfs(root, 0)
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **Return `acc` at a leaf, 0 at `None`.** If `None` returned `acc`, a node with one
  child would count its partial number as a path: `[1,2]` would give 12 + 1 = 13
  instead of 12. The same one-child trap as EP138 and EP145, third time.
- **`acc * 10 + val`, not `acc + val * 10`.** The existing digits shift, not the new one.
- **Zeros are real digits.** `4 -> 0` is 40, not 4. The formula handles it; a
  string-building version that strips leading zeros or uses `if node.val` does not.
- **Start with `acc = 0`.** Starting at `root.val` and then applying the formula again at
  the root double-counts it: 44, not 4.
- **Don't use a shared global for the current number.** If you do, you'd need to undo it
  (`acc //= 10`) on the way back up. Passing it as an argument makes that automatic.

## 🎤 Interview talking points
- *"Top-down DFS carrying the number built so far: times ten plus the digit. At a leaf,
  return it; everywhere else, return left plus right."*
- *"The number's an int passed by value, so each branch gets its own copy; no
  backtracking needed, unlike Path Sum II's list."*
- *"O(n) time, O(h) space. Iteratively, a stack of (node, acc) pairs works the same way."*

## 🔗 Transfer
Three Path Sum episodes, three things carried down: a remainder, a list, a number. Only
the list needed undoing. Tomorrow, EP148 Binary Tree Maximum Path Sum, drops the
"root-to-leaf" rule: a path can start and end **anywhere**. That kills the top-down
carry, and brings back EP141 Diameter's bottom-up split, *return one arm, record both*,
now with negative values in the mix.

## 📹 Metadata
- **Title:** `Sum Root to Leaf Numbers, the calculator trick | Trees #27`
- **Thumbnail:** `acc * 10 + d` (green block)
- **Short:** the calculator screen going 4 → 49 → 495, then the tree lighting up the
  same way. 30s.
