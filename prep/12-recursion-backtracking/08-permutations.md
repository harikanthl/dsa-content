# EP118 · P12E08 · Permutations   [Medium]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/permutations/description/

---

## 🎬 Hook
> "Every ordering of the array. The template is the one from the last two episodes, but
> now you mutate **two** things before the recursive call, the path and the set of
> used elements, and if you undo only one of them, you get the wrong answer with no
> error."

## 📋 Problem, in your words
```
Given an array of DISTINCT integers, return every possible ordering.

Any order of output.
1 <= len(nums) <= 6
```

## 🔢 The example
```
[1,2,3]  ->  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
[0,1]    ->  [[0,1],[1,0]]
[1]      ->  [[1]]
```
3! = 6 answers. At n = 6 it's 720. n! is the number of leaves, so it's also the floor on
the running time.

## 🧸 ELI5
> Three kids, three chairs, and you want every seating order.
>
> Pick who sits in chair 1. Then from whoever's **still standing**, pick chair 2. The
> last kid takes chair 3.
>
> ```
> chair 1: 1       standing: 2 3
> chair 2: 2       standing: 3
> chair 3: 3       -> [1,2,3]  write it down
>
> kid 3 stands up, kid 2 stands up   <- undo, in reverse order
> chair 2: 3       standing: 2
> chair 3: 2       -> [1,3,2]
> ```
>
> "Who's still standing" is the `used` set. When a kid stands up again, they have to
> leave the chair **and** go back into the standing group. Forget either half and the
> next arrangement is wrong.

## 🐌 Brute force (say it, don't type it)
Generate all nⁿ sequences of length n (each slot any element) and keep the ones with no
repeats. For n = 6: 46,656 sequences to find 720. **O(nⁿ · n)**. The optimal version
is this with "already used" pruned before the call instead of filtered at the leaf.
(`itertools.permutations` is the one-liner; say it, then write it.)

## 💡 The pattern reveal
**Signal:** "all orderings" / "all arrangements", order matters, tiny n.
**Therefore:** backtracking, permutations flavour. At each depth pick any element that
isn't used yet.

**Key insight:** in EP116 and EP117 the depth told you which choices were available.
Here it doesn't: the choices at depth 2 depend on what you picked at depths 0 and 1.
So you carry that history as state, a `used` array:

```python
for i in range(len(nums)):
    if used[i]: continue              # prune: already seated
    used[i] = True; path.append(nums[i])     # choose BOTH
    backtrack()                               # explore
    path.pop(); used[i] = False               # unchoose BOTH
```

## 🔍 Dry run: `[1,2,3]`, the first two leaves

| depth | path before | used before | choice | action |
|---|---|---|---|---|
| 0 | `[]` | `{}` | 1 | choose, recurse |
| 1 | `[1]` | `{1}` | 1 | ✗ used, skip |
| 1 | `[1]` | `{1}` | 2 | choose, recurse |
| 2 | `[1,2]` | `{1,2}` | 1, 2 | ✗ used, skip both |
| 2 | `[1,2]` | `{1,2}` | 3 | choose → `[1,2,3]` **record**, undo 3 |
| 1 | `[1,2]` | `{1,2}` | undo 2 | back to `[1]`, `{1}` |
| 1 | `[1]` | `{1}` | 3 | choose, recurse |
| 2 | `[1,3]` | `{1,3}` | 2 | choose → `[1,3,2]` **record**, undo 2 |

```
                        []
            /           |           \
          [1]          [2]          [3]
         /   \        /   \        /   \
     [1,2]  [1,3]  [2,1]  [2,3]  [3,1]  [3,2]
       |      |      |      |      |      |
   [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]
```

n choices, then n-1, then n-2: n! leaves.

## ✅ Optimal solution
```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """Every ordering of a list of distinct integers.

        Time:  O(n · n!), n! leaves, O(n) to copy each.
        Space: O(n) for recursion, path and used, excluding the output.
        """
        result, path = [], []
        used = [False] * len(nums)

        def backtrack() -> None:
            if len(path) == len(nums):             # every element placed
                result.append(path[:])             # COPY
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue                       # prune: already in the path
                used[i] = True                     # choose, both pieces of state
                path.append(x)
                backtrack()                        # explore
                path.pop()                         # unchoose, both pieces
                used[i] = False

        backtrack()
        return result
```
**Time:** O(n · n!) · **Space:** O(n) excluding the output

## ⚠️ Gotchas
- **`path[:]`, not `path`.** Without the copy you get six references to one list, which
  is empty when the search ends: `[[], [], [], [], [], []]`, and no error.
- **Undo both pieces of state.** Pop the path but forget `used[i] = False` and element
  `i` is marked used forever: after the first branch finishes, nothing is ever free again
  and you get one permutation. Reset `used` but forget the pop and the path grows past n.
- **Track used by index, not by value.** `if x in path` works for distinct inputs but is
  O(n) per check, and breaks the moment duplicates appear (Permutations II).
- **The swap approach is the alternative.** Swap `nums[start]` with each `nums[i]` for
  `i >= start`, recurse on `start + 1`, swap back. No `used` array, O(1) extra space,
  but the output order differs and the "swap back" is the undo you can't forget. Know
  both; say why you picked one.
- **No start index here.** That's EP119. Permutations reconsider every element at every
  depth, because `[2,1]` and `[1,2]` are different answers.

## 🎤 Interview talking points
- *"At each depth I can place any element that isn't already placed, so I carry a used
  array alongside the path."*
- *"I mutate two things before the recursive call, so I undo two things after it."*
  ← say this unprompted.
- *"n! permutations, O(n) to copy each, so O(n · n!), and that's optimal because the
  output is that size."*
- *"I could swap in place instead and drop the used array; same complexity, less space."*
- *"If the input had duplicates I'd sort it and skip `nums[i] == nums[i-1]` when
  `nums[i-1]` isn't used, that's Permutations II."*

## 🔗 Transfer
EP116 and EP117 had choices that depended only on the depth. Here they depend on the
history, so the history becomes state. EP119 flips the question: when order *doesn't*
matter, `[2,3]` and `[3,2]` are one answer, and a `start` index replaces the `used`
array. EP120 then makes the choice a cut point in a string.

## 📹 Metadata
- **Title:** `Permutations, undo both pieces of state | Backtracking #3`
- **Thumbnail:** `UNDO BOTH` (red block)
- **Short:** forget `used[i] = False` and watch it return one permutation. 45s.
