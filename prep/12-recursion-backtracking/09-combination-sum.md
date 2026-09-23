# EP119 · P12E09 · Combination Sum   [Medium]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/combination-sum/description/

---

## 🎬 Hook
> "Find every way to make 7 out of 2, 3, 6 and 7, using any number as often as you
> like. The search is easy. The hard part is that the naive version finds `[2,2,3]`,
> `[2,3,2]` and `[3,2,2]` as three answers, and **one integer called `start`** is the
> whole fix."

## 📋 Problem, in your words
```
Given an array of DISTINCT positive integers `candidates` and a `target`,
return every unique combination of candidates that sums to target.

  - the same number may be used any number of times
  - combinations are unique as multisets: [2,2,3] and [3,2,2] are the same one
  - any order of output is fine
```

## 🔢 The example
```
Input:  candidates = [2, 3, 6, 7], target = 7
Output: [[2, 2, 3], [7]]

Input:  candidates = [2, 3, 5], target = 8
Output: [[2, 2, 2, 2], [2, 3, 3], [3, 5]]

Input:  candidates = [2], target = 1
Output: []                     <- no way to make an odd number from 2s
```

## 🧸 ELI5
> You're paying exactly 7 rupees with coins of 2, 3, 6 and 7, and you have as many of
> each coin as you like. You want every different **handful**, not every different
> order of dropping coins on the counter.
>
> The trick: **you promise to put coins down in size order.** Once you've put down a 3,
> you're not allowed to go back and add a 2. That promise means every handful can only
> be built one way, so it can only be counted once.
>
> ```
> allowed:     2, 2, 3      (never goes back down)
> forbidden:   2, 3, 2      (went back to 2 after a 3)
> forbidden:   3, 2, 2
> ```
>
> "Never go back to a smaller coin" is the `start` index. "You may put the same coin
> down again" is recursing with `i` instead of `i + 1`.

## 🐌 Brute force (say it, don't type it)
Build every sequence of candidates whose sum doesn't exceed target, keep the ones that
hit it exactly, then deduplicate by sorting each answer and throwing them in a set.
It's correct, and it explores every **ordering** of every answer (`[2,2,3]` three
times, and far worse for longer ones) only to throw the repeats away at the end. Say
it to show you know where the duplicates come from, then kill them at the source.

## 💡 The pattern reveal
**Signal:** "return **all** combinations" · small inputs · choose-and-recurse.
**Therefore:** backtracking, flavour 3 from the pattern card: **combinations with a
`start` index.**

**Key insight:** order doesn't matter, so choose it for the algorithm. Only ever pick
candidates **at or after** the one you picked last. Two decisions follow, and they're
the entire problem:

| decision | code | effect |
|---|---|---|
| never look back | `for i in range(start, n)` | each multiset is built in exactly one order, no duplicates |
| reuse allowed | recurse with `i`, not `i + 1` | the same coin can go down again |
| prune early | sort, then `break` when `cands[i] > remaining` | every later candidate is bigger, so stop the whole loop |

```python
for i in range(start, len(candidates)):
    if candidates[i] > remaining:
        break                                 # sorted: the rest are bigger still
    path.append(candidates[i])                # choose
    combo(i, remaining - candidates[i])       # explore (i: reuse allowed)
    path.pop()                                # unchoose
```

## 🔍 Dry run: `candidates = [2, 3, 6, 7]`, `target = 7`

The decision tree. Each edge is a choice, the number is what's left to make:

```
                        (7)
         2 /       3 |       6 |      7 \
         (5)        (4)       (1)      (0) ✓ [7]
      2 /  3 \     3 |  6 x    6 x
     (3)   (2)     (1)         (6 > 1, break)
   2 / 3 \   3 x    3 x
  (1) (0) ✓ [2,2,3]
  2 x
```

`x` = pruned by the `break` before any recursive call. No branch ever goes **left**
of its parent's choice; that's `start` at work.

| step | call | path before | i tries | action | path after |
|---|---|---|---|---|---|
| 1 | `combo(0, 7)` | `[]` | 2 | choose 2 | `[2]` |
| 2 | `combo(0, 5)` | `[2]` | 2 | choose 2 | `[2,2]` |
| 3 | `combo(0, 3)` | `[2,2]` | 2 | choose 2 | `[2,2,2]` |
| 4 | `combo(0, 1)` | `[2,2,2]` | 2 | 2 > 1, **break** | pop → `[2,2]` |
| 5 | `combo(0, 3)` | `[2,2]` | 3 | choose 3 | `[2,2,3]` |
| 6 | `combo(1, 0)` | `[2,2,3]` | - | remaining 0, **record `[2,2,3]`** | pop → `[2,2]` |
| 7 | `combo(0, 3)` | `[2,2]` | 6 | 6 > 3, **break** | pop → `[2]` |
| 8 | `combo(0, 5)` | `[2]` | 3 | choose 3 | `[2,3]` |
| 9 | `combo(1, 2)` | `[2,3]` | 3 | 3 > 2, **break** | pop → `[2]` |
| 10 | `combo(0, 5)` | `[2]` | 6 | 6 > 5, **break** | pop → `[]` |
| 11 | `combo(0, 7)` | `[]` | 3 | choose 3 | `[3]` |
| 12 | `combo(1, 4)` | `[3]` | 3 | choose 3, then `combo(1, 1)` breaks at once | pop → `[3]` |
| 13 | `combo(1, 4)` | `[3]` | 6 | 6 > 4, **break** | pop → `[]` |
| 14 | `combo(0, 7)` | `[]` | 6 | choose 6, then `combo(2, 1)` breaks at once | pop → `[]` |
| 15 | `combo(0, 7)` | `[]` | 7 | choose 7, `combo(3, 0)` **records `[7]`** | pop → `[]` |

Answer **`[[2, 2, 3], [7]]`** ✓. Notice step 9: from `[2,3]` the loop starts at 3,
not 2, so `[2,3,2]` is never even considered.

## ✅ Optimal solution
```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """Every multiset of candidates (reuse allowed) that sums to target.

        Time:  O(n^(T/m)), T = target, m = smallest candidate: the tree is at most
               T/m deep and branches up to n ways. Pruning cuts it hard in practice.
        Space: O(T/m) for the recursion stack and path, excluding the output.
        """
        candidates = sorted(candidates)     # sorted so the break prune is valid
        results, path = [], []

        def combo(start: int, remaining: int) -> None:
            if remaining == 0:
                results.append(path[:])     # COPY: path keeps changing after this
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break                   # every later candidate is bigger too
                path.append(candidates[i])              # choose
                combo(i, remaining - candidates[i])     # explore; i, so reuse is allowed
                path.pop()                              # unchoose

        combo(0, target)
        return results
```
**Time:** O(n^(T/m)) · **Space:** O(T/m) excluding the output

## ⚠️ Gotchas
- **`start` is what kills duplicates.** Loop from `0` every time and you'll get
  `[2,2,3]`, `[2,3,2]` and `[3,2,2]`. Don't fix it with a set of sorted tuples at the
  end; fix it by never looking back.
- **`i` vs `i + 1`.** Recurse with `i` and the same candidate can be used again (this
  problem). Recurse with `i + 1` and each is used once (Combination Sum II, LeetCode
  40). One character, two different problems. Say which one you're solving.
- **`break` needs sorted input.** Without the sort, a big candidate early in the list
  would `break` before a small one later got its turn, and you'd silently lose answers.
  Unsorted? Use `continue`, and lose most of the pruning.
- **`path[:]`, not `path`.** Append `path` itself and every answer aliases one list
  that ends empty: `[[], []]`. The pattern card's gotcha #1.
- **`remaining == 0` is the only success.** There's no `remaining < 0` case to handle,
  because the `break` stops you from ever overshooting. If you find yourself writing a
  negative check, the prune is in the wrong place.
- **An unreachable target returns `[]`, not `[[]]`.** `[2]` with target 1: the loop
  breaks immediately and nothing is recorded. Correct for free.

## 🎤 Interview talking points
- *"Order doesn't matter, so I impose one: I only pick candidates at or after the last
  one I picked. Every combination then has exactly one way to be built."*
- *"Recursing with `i` allows reuse; `i + 1` would be Combination Sum II."* ← say this
  unprompted, it's the follow-up every time.
- *"I sort first so I can `break` instead of `continue`: once a candidate is too big,
  everything after it is too."*
- *"Time is exponential in target over the smallest candidate; the output itself can be
  that large, so there's no polynomial answer."*
- *"If they only wanted the **number** of combinations, I'd stop listing and do the
  coin-change DP from Pattern 15."*

## 🔗 Transfer
EP118 used a `used` set because order mattered. Here order doesn't, so a single integer
replaces the whole set. Tomorrow, EP120 Palindrome Partitioning, keeps the `start`
index but changes what a choice *is*: not which number to add, but **where to cut the
string next**. Much later, EP178 Subset Sum asks "is it *possible* to hit the target",
and that yes/no question is where this exponential search collapses into a DP table.

## 📹 Metadata
- **Title:** `Combination Sum, one integer kills every duplicate | Backtracking #4`
- **Thumbnail:** `i  vs  i + 1` (red block)
- **Short:** the three orderings of `[2,2,3]` appearing, then vanishing when `start` is
  added. 45s.
