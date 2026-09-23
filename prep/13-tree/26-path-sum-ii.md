# EP146 · P13E26 · Path Sum II   [Medium]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/path-sum-ii/

---

## 🎬 Hook
> "Yesterday: *is there* a path that sums to 22? Today: give me *every* one. That one
> word turns a tree problem into a backtracking problem. You carry the path down in a
> list, and the bug everyone hits is appending that list to the answer and getting back
> `[[], []]`. Two characters fix it: `[:]`."

## 📋 Problem, in your words
```
Given the root of a binary tree and an integer targetSum,
return ALL root-to-leaf paths whose values sum to targetSum.

  - each path is a list of node values, root first
  - a leaf is a node with NO children
  - values can be negative
```

## 🔢 The example
```
Input:  root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2], [5,8,4,5]]

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1

Why:    5+4+11+2 = 22   and   5+8+4+5 = 22

Input:  root = [1,2,3], targetSum = 5   ->  []
Input:  root = [1,2],   targetSum = 0   ->  []
```

## 🧸 ELI5
> You're exploring a cave system with a ball of string. As you walk down a tunnel, the
> string unrolls behind you: that's your `path`. When you hit a dead end, you check if
> the numbers on the string add to 22. If they do, you **take a photo** of the string.
>
> Then you **wind the string back** to the last junction and try the other tunnel.
>
> ```
> photo, not the string itself:  you only have ONE ball of string, and it keeps
>                                 changing. Save the string and by the end it's
>                                 wound all the way back in: empty.
> ```

## 🐌 Brute force (say it, don't type it)
Pass a **new** list down at every call, `path + [node.val]`, so nothing needs undoing.
It's correct and many people ship it. Cost: every call copies a list of length up to h,
so **O(n · h)** time spent copying paths that mostly *won't* match. The backtracking
version copies only when a path actually matches.

## 💡 The pattern reveal
**Signal:** "return **all** paths", root to leaf.
**Therefore:** EP145's top-down DFS **plus** Pattern 12's choose / explore / unchoose.
The pattern card's gotcha #3 is this episode.

| | EP145 Path Sum | today |
|---|---|---|
| carried down | `remaining` | `remaining` **and** `path` |
| at a matching leaf | return True | `results.append(path[:])` |
| stop at the first? | yes, `or` short-circuits | no, visit everything |
| on the way back up | nothing | `path.pop()` |

**Key insight:** one shared list, mutated in place. Every `append` on the way down is
paired with exactly one `pop` on the way up, so when a call returns, `path` is exactly
what it was when the call started.

```python
path.append(node.val)                 # choose
... recurse into both children ...    # explore
path.pop()                            # unchoose
```

## 🔍 Dry run: target 22

| step | node | path after append | remaining | leaf? | action |
|---|---|---|---|---|---|
| 1 | 5 | `[5]` | 17 | no | go left |
| 2 | 4 | `[5,4]` | 13 | no | go left |
| 3 | 11 | `[5,4,11]` | 2 | no | go left |
| 4 | 7 | `[5,4,11,7]` | −5 | yes | no match; pop → `[5,4,11]` |
| 5 | 2 | `[5,4,11,2]` | 0 | yes | **record `[5,4,11,2]`**; pop → `[5,4,11]` |
| 6 | 11 done | - | - | - | pop → `[5,4]` |
| 7 | 4 done | - | - | - | (right is `None`) pop → `[5]` |
| 8 | 8 | `[5,8]` | 9 | no | go left |
| 9 | 13 | `[5,8,13]` | −4 | yes | no match; pop → `[5,8]` |
| 10 | 4 | `[5,8,4]` | 5 | no | go left |
| 11 | 5 | `[5,8,4,5]` | 0 | yes | **record `[5,8,4,5]`**; pop → `[5,8,4]` |
| 12 | 1 | `[5,8,4,1]` | 4 | yes | no match; pop → `[5,8,4]` |
| 13 | unwind | - | - | - | pops back to `[]` |

Answer **`[[5,4,11,2], [5,8,4,5]]`** ✓. After the last call returns, `path` is `[]`.
If you had appended `path` itself, both results would be that same empty list.

## ✅ Optimal solution
```python
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        """Every root-to-leaf path summing to targetSum, by backtracking.

        Time:  O(n · h) worst case: O(n) visits, plus an O(h) copy per matching leaf
               (up to ~n/2 leaves).
        Space: O(h) for the recursion and the path, excluding the output.
        """
        results, path = [], []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if not node:
                return
            path.append(node.val)                       # choose
            remaining -= node.val

            if not node.left and not node.right and remaining == 0:
                results.append(path[:])                 # COPY: path keeps changing
            else:
                dfs(node.left, remaining)               # explore
                dfs(node.right, remaining)

            path.pop()                                  # unchoose

        dfs(root, targetSum)
        return results
```
**Time:** O(n · h) · **Space:** O(h) excluding the output

## ⚠️ Gotchas
- **`path[:]`, not `path`.** The pattern card's gotcha #3. Append the live list and
  every result aliases it; by the end it's empty, and you return `[[], []]`.
- **Exactly one `pop` per `append`.** Put the `pop` after both branches, at the very end.
  An early `return` after recording (without popping) leaves the leaf's value stuck in
  `path` for every later path.
- **Leaf check, not `None` check.** Same as EP145: recording at `None` records the path
  twice for every leaf (once per `None` child) and wrongly accepts one-child nodes.
- **No pruning on `remaining < 0`.** Negative values can bring it back.
- **`remaining` is an int, so it doesn't need undoing.** It's passed by value; each call
  has its own copy. Only the shared list needs a `pop`. Say that, it shows you know why
  one needs backtracking and the other doesn't.

## 🎤 Interview talking points
- *"Same DFS as Path Sum, but I carry the path in one shared list: append on the way
  down, pop on the way up, and copy it only when a leaf matches."*
- *"I copy with `path[:]` because the list keeps changing after I record it."*
- *"The remaining sum is an integer passed by value, so only the list needs undoing."*
- *"O(n · h) worst case, because each match costs a copy of up to h values."*

## 🔗 Transfer
This is EP119 Combination Sum's choose / explore / unchoose, with the tree deciding the
choices instead of a `for` loop. Tomorrow, EP147 Sum Root to Leaf Numbers, keeps the
top-down carry but the thing being carried is a **number being built digit by digit**,
`acc * 10 + val`, and like `remaining` it's passed by value, so no `pop` needed.

## 📹 Metadata
- **Title:** `Path Sum II, why you get [[], []] and the two-character fix | Trees #26`
- **Thumbnail:** `path[:]` (red block)
- **Short:** the result list showing `[[], []]`, then `[:]` added and the real paths
  appearing. 30s.
