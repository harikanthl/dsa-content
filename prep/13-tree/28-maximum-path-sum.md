# EP148 · P13E28 · Binary Tree Maximum Path Sum   [Hard]

**Pattern:** Tree · **Link:** https://leetcode.com/problems/binary-tree-maximum-path-sum/description/

---

## 🎬 Hook
> "This is a Hard, and it's EP141 Diameter with one new idea. Diameter's arms were
> lengths, always worth having. Here the arms are sums, and a sum can be **negative**. A
> negative arm makes any path worse, so you just... don't take it. `max(arm, 0)`. That's
> the entire gap between Easy and Hard."

## 📋 Problem, in your words
```
A path is any sequence of nodes connected by edges, each node used at most once.
It does NOT have to pass through the root, and does NOT have to end at a leaf.
It must contain at least ONE node.

Return the maximum sum of node values over all paths.

  - values can be negative
```

## 🔢 The example
```
Input:  [-10,9,20,null,null,15,7]
Output: 42

          -10
          /  \
         9    20
             /  \
            15   7

Why:    15 -> 20 -> 7 = 42. Adding -10 and 9 would give 41: the root hurts.

Input:  [1,2,3]       ->  6    (2 -> 1 -> 3)
Input:  [-3]          -> -3    (at least one node, so the answer can be negative)
Input:  [-2,-1]       -> -1    (the best path is the single node -1)
```

## 🧸 ELI5
> Every node is a town, and its number is how much money you gain (or lose, if it's
> negative) passing through. You want the most profitable road trip, starting and ending
> anywhere, never visiting a town twice.
>
> At every town, you ask each neighbourhood below: "what's the most profit I can get
> going **down** into you, one direction only?" If a neighbourhood answers with a loss,
> you say **"then I won't go there at all"**: that arm counts as 0.
>
> ```
> at town 20:  left arm (15) = +15, right arm (7) = +7
>              a trip that turns around at 20:  15 + 20 + 7 = 42   <- record it
>              what 20 offers its parent:       20 + max(15, 7) = 35   (one arm only)
>
> at town -10: left arm  9, right arm 35
>              a trip that turns around here:  9 + (-10) + 35 = 34   < 42, don't care
> ```

## 🐌 Brute force (say it, don't type it)
Every path is determined by its two endpoints. Try every pair of nodes, find the path
between them (through their LCA, EP132), sum it. **O(n²)** pairs, each path up to O(h)
long: **O(n² · h)**. It's what I used to *test* the real solution, and it's the thing to
say on camera before killing it.

## 💡 The pattern reveal
**Signal:** "path", "**any** node to **any** node", a number from both children.
**Therefore:** Shape D, bottom-up, with the **return / record split** from EP141:

| problem | returns to parent | records as the answer |
|---|---|---|
| Diameter (EP141) | `1 + max(L, R)` | `L + R` |
| **Max Path Sum (today)** | `node.val + max(L, R, 0)` | `node.val + max(L, 0) + max(R, 0)` |

**Key insight, part 1:** every path has one **highest** node, where it turns around. At
that node the best path is `val + best left arm + best right arm`. So compute that at
every node and keep the max. (Diameter's idea, verbatim.)

**Key insight, part 2:** an arm is **optional**. If the best you can get going down the
left is −5, a path that turns here is better off without it. So clamp every arm at 0:

```python
L = max(gain(node.left), 0)      # a losing arm is simply not taken
R = max(gain(node.right), 0)
best = max(best, node.val + L + R)       # turn around HERE: both arms
return node.val + max(L, R)              # offer the parent ONE arm
```

**The node itself is not optional.** `node.val` is always included, even when it's
negative: a path has at least one node, and the path through this node must contain
it. That's why `[-3]` returns −3 and not 0.

## 🔍 Dry run: `[-10,9,20,null,null,15,7]`

`gain(node)` returns the best **one-arm** sum starting at node and going down.

| step | node | L = max(gain, 0) | R = max(gain, 0) | `val + L + R` | best after | returns `val + max(L, R)` |
|---|---|---|---|---|---|---|
| 1 | 9 | 0 | 0 | 9 | 9 | 9 |
| 2 | 15 | 0 | 0 | 15 | 15 | 15 |
| 3 | 7 | 0 | 0 | 7 | 15 | 7 |
| 4 | 20 | 15 | 7 | **42** | **42** | 35 |
| 5 | −10 | 9 | 35 | 34 | 42 | 25 |

Answer **42** ✓. The root's return value (25) is never used. As in EP141, the answer
lives in `best`, and it was recorded two levels below the root.

On `[-2,-1]`: node −1 records −1 and returns −1; the root clamps that arm to 0 and
records −2 + 0 + 0 = −2. `best` stays **−1** ✓. That only works because `best` starts at
`-inf`, not 0.

## ✅ Optimal solution
```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        """Largest sum over all paths (any node to any node, at least one node).

        Time:  O(n), one postorder pass.
        Space: O(h), the recursion stack.
        """
        best = float('-inf')                # NOT 0: every value might be negative

        def gain(node: Optional[TreeNode]) -> int:
            """Best sum of a downward path starting at node; records the answer."""
            nonlocal best
            if not node:
                return 0
            L = max(gain(node.left), 0)     # a negative arm is left behind
            R = max(gain(node.right), 0)
            best = max(best, node.val + L + R)      # the path that turns here
            return node.val + max(L, R)             # the parent can extend one arm

        gain(root)
        return best
```
**Time:** O(n) · **Space:** O(h)

## ⚠️ Gotchas
- **`best = -inf`, not 0.** All-negative trees have a negative answer. Starting at 0
  returns 0 for `[-3]`, which is the empty path, and that's not allowed.
- **Clamp the arms, never the node.** `max(L, 0)` and `max(R, 0)` yes; `max(node.val, 0)`
  no. The node is on the path by definition.
- **Return one arm, record both.** Returning `node.val + L + R` lets the parent extend a
  path that already forks, which isn't a path. Same bug as EP141.
- **The clamp goes on the child's return, before adding.** Writing `return node.val +
  max(L, R, 0)` in the function but *not* clamping `L` and `R` in the `best` line lets a
  negative arm into the recorded answer.
- **The return value of `gain(root)` is not the answer.** It's the best path that starts
  at the root and goes down one side. 25, in the example.

## 🎤 Interview talking points
- *"Every path has a highest node where it turns. At each node I compute the best path
  turning there, value plus the best left arm plus the best right arm, and keep a running
  max."*
- *"What I return to the parent is different: value plus the better single arm, because
  the parent can only extend in one direction."*
- *"Arms are clamped at zero, because a negative arm only makes a path worse; the node
  itself is never clamped."*
- *"It's Diameter with sums instead of lengths. O(n) time, O(h) space."* ← name the
  family; it shows you've seen the shape, not memorised the problem.

## 🔗 Transfer
EP141 introduced "return one arm, record both" with lengths; today it handles values
that can hurt. The clamp at zero is Kadane's rule from Pattern 04, *drop a prefix that's
gone negative*, applied to a tree branch instead of an array prefix. That ends the Path
Sum group. Tomorrow, EP149, starts Construction: instead of reading a tree, you **build**
one from two of its traversals.

## 📹 Metadata
- **Title:** `Binary Tree Max Path Sum, the Hard that's really Diameter | Trees #28`
- **Thumbnail:** `max(arm, 0)` (red block)
- **Short:** the town road trip at node 20: 42 recorded, 35 handed up. 45s.
