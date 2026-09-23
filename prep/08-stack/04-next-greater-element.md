# EP061 · P08E04 · Next Greater Element II   [Medium]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/next-greater-element-ii/

---

## 🎬 Hook
> "For every number, find the next bigger one to its right, and the array is
> **circular**, so 'right' wraps around to the front. This is the template episode for
> the whole second half of the pattern: the stack stops being the answer and becomes a
> queue of elements **still waiting for something bigger**. When one arrives, the pop is
> the answer being written down."

## 📋 Problem, in your words
```
Given a CIRCULAR integer array nums, return an array where position i
holds the first number greater than nums[i], searching to the right
and wrapping around past the end.

If no such number exists anywhere in the circle, the answer is -1.
"Greater" is STRICT: equal values don't count.
```

## 🔢 The example
```
Input:  [1, 2, 1]
Output: [2, -1, 2]
Why:    nums[0]=1 -> 2 is next.  nums[1]=2 -> nothing bigger anywhere -> -1.
        nums[2]=1 -> wrap around to the 2 at index 1.   <- the circular part

Input:  [1, 2, 3, 4, 3]     -> [2, 3, 4, -1, 4]
Input:  [5, 4, 3, 2, 1]     -> [-1, 5, 5, 5, 5]     <- everyone wraps to the 5
```
That last one is the shape to keep in your head: a strictly decreasing array is the
worst case, where every element sits on the stack until the very end.

## 🧸 ELI5
> Think of the numbers as people in a queue, each holding up a sign with their height,
> each waiting for someone **taller** to walk past.
>
> ```
> [1, 2, 1]
>
> 1 arrives -> nobody taller yet -> he WAITS       waiting: [1]
> 2 arrives -> taller than the 1 waiting!          -> answer for that 1 is 2
>              the 2 then waits himself             waiting: [2]
> 1 arrives -> shorter than the waiting 2          -> he waits too   waiting: [2, 1]
>
> end of array -- but it's a CIRCLE, so walk it again:
>
> 1 (again) -> not taller than either waiter       waiting: [2, 1]
> 2 (again) -> taller than the waiting 1!          -> answer for that 1 is 2
>              (we don't add anyone on lap two)     waiting: [2]
>
> the 2 is still waiting when the music stops      -> answer -1
> ```
>
> The people still waiting are always in **decreasing** height order, because anyone
> shorter arriving just joins the back, and anyone taller **clears out** everyone they
> beat. That's the invariant, and it's what makes the stack work.

## 🐌 Brute force (say it, don't type it)
For each `i`, scan forward `n − 1` positions with `(i + step) % n` and take the first
bigger value. **O(n²)**, trivially correct, and the right thing to say, the stack's job
is to delete that inner scan.

## 💡 The pattern reveal
**Signal:** "next greater/smaller/warmer" · for **every** element · O(n) wanted.
**Therefore:** a **monotonic stack**. Plus, here, one extra twist for the circle.

**The four decisions** (make them out loud, before typing):

| decision | here |
|---|---|
| increasing or decreasing? | "next **greater**" → pop while the top is smaller → the stack stays **decreasing** |
| index or value? | **index**: you need to write into `res[j]`, and the value is recoverable as `nums[j]` |
| what happens at the pop? | `res[popped] = current` ← **the answer is discovered here** |
| what's left at the end? | elements that never found anything bigger → keep the default `-1` |

```python
while stack and nums[stack[-1]] < cur:
    res[stack.pop()] = cur          # `cur` is the answer for everything it beats
```

One arriving element can resolve **many** waiting ones, that inner `while` sometimes
pops four in a row (see the `[5,4,3,2,1]` trace). Each pop writes one final answer.

**🧨 The circular trick: walk the array twice, push only on the first lap.**

```python
for i in range(2 * n):
    cur = nums[i % n]
    while stack and nums[stack[-1]] < cur:
        res[stack.pop()] = cur
    if i < n:                        # second lap RESOLVES but never ADDS
        stack.append(i)
```

Two laps is enough because after a full extra lap, anything still unresolved has been
compared against every element in the array. And `if i < n` is essential: pushing on the
second lap would leave indices on the stack that get a third chance they shouldn't have,
and (worse) it stops being clear which occurrence an index refers to.

**Still O(n)**: `2n` iterations, each index pushed once and popped at most once.

## 🔍 Dry run: `[1, 2, 1]`
`res = [-1, -1, -1]`, `stack = []` (holding **indices**).

| i | `i%n` | `cur` | pops (answers written) | stack after | `res` |
|---|---|---|---|---|---|
| 0 | 0 | 1 | - | `[0]` | `[-1, -1, -1]` |
| 1 | 1 | 2 | pop 0 → `res[0] = 2` | `[1]` | `[2, -1, -1]` |
| 2 | 2 | 1 |, (1 < 2) | `[1, 2]` | `[2, -1, -1]` |
| 3 | 0 | 1 | - | `[1, 2]` | *(lap 2: no push)* |
| 4 | 1 | 2 | **pop 2 → `res[2] = 2`** | `[1]` | `[2, -1, 2]` |
| 5 | 2 | 1 | - | `[1]` | `[2, -1, 2]` |

Index `1` is still on the stack → `res[1]` keeps its default. Answer **`[2, -1, 2]`** ✓

Row `i = 4` is the circular payoff: index 2's answer is found on the **second lap**, by
an element that sits to its *left* in the original array.

## 🔍 Dry run: `[5, 4, 3, 2, 1]` (the worst case)
Lap one pushes everything, each element is smaller than the last, so nothing pops:

```
stack (indices): [0, 1, 2, 3, 4]        values 5 4 3 2 1 -- decreasing, as promised
```

Then `i = 5` (`nums[0] = 5`) arrives and clears four of them in a single `while`:

| pop | writes |
|---|---|
| 4 | `res[4] = 5` |
| 3 | `res[3] = 5` |
| 2 | `res[2] = 5` |
| 1 | `res[1] = 5` |

Index 0 remains (nothing beats 5) → `res[0] = -1`. Answer **`[-1, 5, 5, 5, 5]`** ✓

Four pops in one iteration, and that's exactly why the complexity argument has to be
amortised: this single step is O(n), but it can only happen because n pushes paid for it
earlier.

## ✅ Optimal solution
```python
class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        """Next strictly greater element to the right, wrapping around.

        Time:  O(n), 2n iterations; each index is pushed once, popped at most once.
        Space: O(n), the stack.
        """
        n = len(nums)
        res = [-1] * n              # the default: nothing bigger exists
        stack = []                  # INDICES, values strictly decreasing

        for i in range(2 * n):      # two laps around the circle
            cur = nums[i % n]

            # `cur` is the next greater element for everything smaller still waiting
            while stack and nums[stack[-1]] < cur:
                res[stack.pop()] = cur

            if i < n:               # only the FIRST lap adds new waiters
                stack.append(i)

        return res
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`if i < n` before pushing.** Without it the second lap adds duplicate waiters and
  the answers drift.
- **`<` not `<=`.** "Strictly greater" means equal values stay on the stack.
  `[2, 2]` → `[-1, -1]`, not `[2, 2]`. Test duplicates on purpose.
- **Store indices, not values.** You're writing into `res[j]`; a stack of values can't
  tell you where to write.
- **`res` starts as `-1`**, and the leftovers keep it. There's no "handle the remaining
  stack" step, that's the default doing the work.
- **`nums[stack[-1]]`, not `stack[-1]`.** Comparing an index against a value is a silent
  wrong answer, and the types are both `int` so nothing complains.
- **Two laps, not three.** One full extra pass compares every waiter against every
  element; more is wasted work.

## 🎤 Interview talking points
- *"I keep a stack of indices whose next-greater element hasn't been found yet. It stays
  decreasing, because anything bigger clears out everyone it beats, and each of those
  pops is one final answer."* ← the template, stated.
- *"For the circular part I walk `2n` positions with `i % n`, but only push on the first
  lap, so nobody gets two turns."*
- *"O(n) amortised, one iteration can pop four elements, but only because four pushes
  happened earlier."* ← the follow-up, pre-answered.
- *"Strictly greater, so `<`. With `<=` I'd be answering 'next greater or equal'."*

## 🔗 Transfer
This is the monotonic template and the next three episodes are all variations on it:
EP62 stores indices so the pop can compute a **distance**, EP63 runs the same invariant
over a **linked list** and keeps the survivors, and EP66 adds a **budget** to the pops.
Tomorrow (EP62) is the gentlest of them, same code, minus the circular lap, with the
answer being `i − j` instead of `nums[i]`.

## 📹 Metadata
- **Title:** `Next Greater Element II, the pop IS the answer | Stack #4`
- **Thumbnail:** `WAITING FOR TALLER` (green block)
- **Short:** `[5,4,3,2,1]`, four pops in a single step on the wrap-around. 50s.
