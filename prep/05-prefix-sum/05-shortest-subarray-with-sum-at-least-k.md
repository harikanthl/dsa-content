# EP043 · P05E05 · Shortest Subarray with Sum at Least K   [Hard]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

---

## 🎬 Hook
> "This is EP22, smallest subarray with a given sum, with four words added:
> *the array may contain negatives*. Those four words delete the sliding window
> entirely, and this problem goes from Easy to Hard. Today is about what replaces it:
> a queue of prefix sums that you keep **increasing**, and two pop rules, each of which
> throws away something that can never be the answer."

## 📋 Problem, in your words
```
Given an integer array nums (negatives allowed) and an integer k,
return the LENGTH of the shortest non-empty contiguous subarray with
sum >= k.

Return -1 if no such subarray exists.
```

## 🔢 The example
```
Input:  nums = [1], k = 1          -> 1
Input:  nums = [1, 2], k = 4       -> -1        (total is 3)
Input:  nums = [2, -1, 2], k = 3   -> 3         <- the whole array. See below.
Input:  nums = [84, -37, 32, 40, 95], k = 167 -> 3    <- [32, 40, 95]
```

**Look hard at `[84, −37, 32, 40, 95], k = 167`.** Run EP22's sliding window on it and
it returns **5**, not 3. Here's why: the window only shrinks from the left while the sum
still reaches `k`. It arrives at the full array with sum 214, drops the leading `84`,
lands on 130, below `k`, and stops, having recorded length 5. It never discovers that
dropping the *pair* `84, −37` costs only 47 and leaves `[32, 40, 95] = 167`.

The `−37` is what breaks it: **removing an element can raise the remaining sum**, so
"the sum fell below k" no longer means "I have shrunk as far as I can." Run that on
camera before writing any deque code, a wrong answer from the previous pattern's tool
is the best motivation for this one.

`[2, −1, 2], k = 3` is the companion case: the answer is the **whole array**, negative
included, because there's no shorter way to reach 3. The window happens to get this one
right, which is precisely why you need the 84 example to prove it wrong.

## 🧸 ELI5
> Write down the running totals and forget the array entirely:
>
> ```
> nums:          2   -1    2
> prefix:   0    2    1    3
> index:    0    1    2    3
> ```
>
> You want two positions `i < j` with `pre[j] − pre[i] >= k`, and `j − i` as small as
> possible. So standing at `j`, you want the **closest** earlier position whose prefix
> is small enough.
>
> Now two observations, and they are the whole algorithm:
>
> 1. **If an earlier `i` already works, use it and throw it away forever.** You're at
>    the first `j` where it works, so any later `j` pairs with it more distantly. It can
>    never give a shorter answer again. *(pop from the front)*
> 2. **If an earlier `i` has a prefix `>= pre[j]`, throw it away too.** `j` is later
>    *and* smaller, better on both counts, for every future `j'`. It dominates. *(pop
>    from the back)*
>
> What survives is a queue of positions whose prefix values strictly **increase**. The
> front is the smallest prefix and the oldest position; the back is the newest.

## 🐌 Brute force (say it, don't type it)
All O(n²) pairs of prefix positions, keep the shortest gap reaching `k`. Correct,
trivially. Also worth naming the **wrong** O(n) attempt, the sliding window, because
the interviewer wants to hear you rule it out for a *reason*:

> *"With negatives, the sum isn't monotonic in the window's length. Extending can lower
> it, so shrinking from the left tells you nothing about what's ahead."*

## 💡 The pattern reveal
**Signal:** shortest subarray · a `>= k` **threshold** · negatives present.
**Therefore:** prefix sums + a **monotonic deque of indices**, O(n).

**Key insight:** a hash map is the wrong structure here and knowing *why* is the lesson
of this episode. EP39–EP42 all asked **equality** questions, "have I seen exactly this
key?", which is all a dict can answer in O(1). This asks a **range** question:

```
is there an earlier index i with  pre[i] <= pre[j] - k ?   and the LATEST such i
```

That needs order. The deque supplies it, and stays O(n) because each index is pushed
once and popped once.

**The two pops, spelled out** (this is the code, and it must be in this order):

```python
while dq and pre[j] - pre[dq[0]] >= k:      # (1) front: found an answer
    best = min(best, j - dq.popleft())      #     record it, then discard i forever

while dq and pre[dq[-1]] >= pre[j]:         # (2) back: dominated
    dq.pop()                                #     j is later AND no larger

dq.append(j)
```

Rule (1) before rule (2): a front element might complete an answer *with this very j*,
so you must harvest before you prune. And the loop runs over the prefix array
`0 .. n`, not the original array, `pre[0] = 0` is a legitimate left end.

## 🔍 Dry run: `nums = [2, -1, 2]`, `k = 3`
`pre = [0, 2, 1, 3]`, `dq = []`, `best = ∞`.

| j | `pre[j]` | front pops (record) | back pops (dominated) | `dq` after | `best` |
|---|---|---|---|---|---|
| 0 | 0 | - | - | `[0]` | ∞ |
| 1 | 2 | 2 − 0 = 2 < 3, no | `pre[0]=0 >= 2`? no | `[0, 1]` | ∞ |
| 2 | 1 | 1 − 0 = 1 < 3, no | **`pre[1]=2 >= 1` → pop 1** | `[0, 2]` | ∞ |
| 3 | 3 | **3 − pre[0] = 3 ≥ 3 → pop 0, best = 3 − 0 = 3**; then `3 − pre[2] = 2 < 3`, stop | `pre[2]=1 >= 3`? no | `[2, 3]` | **3** |

Answer **3** ✓

Row `j = 2` is rule (2) earning its keep: position 1 holds prefix `2`, position 2 holds
prefix `1`. Position 2 is later *and* smaller, so position 1 can never be part of a
better answer and leaves. That pop is what keeps the deque increasing, and the deque
being increasing is what makes the front pop in row 3 safe to stop at the first failure.

## 🔍 Dry run: `nums = [84, -37, 32, 40, 95]`, `k = 167`
`pre = [0, 84, 47, 79, 119, 214]`.

| j | `pre[j]` | front pops | back pops | `dq` after | `best` |
|---|---|---|---|---|---|
| 0 | 0 | - | - | `[0]` | ∞ |
| 1 | 84 | 84 < 167 | no | `[0, 1]` | ∞ |
| 2 | 47 | 47 < 167 | **`pre[1]=84 >= 47` → pop 1** | `[0, 2]` | ∞ |
| 3 | 79 | 79 < 167 | `pre[2]=47 >= 79`? no | `[0, 2, 3]` | ∞ |
| 4 | 119 | 119 < 167 | no | `[0, 2, 3, 4]` | ∞ |
| 5 | 214 | **214 − 0 = 214 ≥ 167 → pop 0, best = 5**; **214 − 47 = 167 ≥ 167 → pop 2, best = 5 − 2 = 3**; 214 − 79 = 135 < 167, stop | `pre[4]=119 >= 214`? no | `[3, 4, 5]` | **3** |

Answer **3** ✓, the subarray `[32, 40, 95]`, indices 2..4.

Row `j = 5` pops the front **twice**, improving the answer from 5 to 3 in a single
iteration. That is the rule-(1) loop doing its job: keep harvesting while the front
still reaches `k`, because each pop is a *shorter* candidate than the last. And note
`214 − 47 = 167`, the `>=` is inclusive, so an exact hit must count.

## ✅ Optimal solution
```python
from collections import deque

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        """Length of the shortest subarray with sum >= k. Negatives allowed.

        Time:  O(n), every index enters and leaves the deque at most once.
        Space: O(n), the prefix array and the deque.
        """
        n = len(nums)
        pre = [0] * (n + 1)
        for i, x in enumerate(nums):
            pre[i + 1] = pre[i] + x

        dq = deque()            # indices into `pre`, with pre[...] INCREASING
        best = n + 1            # sentinel: longer than any real answer

        for j, p in enumerate(pre):
            # (1) harvest: this front index already reaches k, and never will more cheaply
            while dq and p - pre[dq[0]] >= k:
                best = min(best, j - dq.popleft())

            # (2) prune: j is later and no larger, so dq[-1] is dominated
            while dq and pre[dq[-1]] >= p:
                dq.pop()

            dq.append(j)

        return best if best <= n else -1
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **Harvest before you prune.** Swap the two `while` loops and a front index that would
  have completed an answer with this `j` can be popped as "dominated" first. Order is
  correctness here, not style.
- **Loop over `pre`, all `n + 1` of it.** `pre[0] = 0` must enter the deque or every
  answer starting at index 0 is lost, the same empty-prefix idea as EP39, wearing a
  deque instead of a map.
- **The deque holds indices, not values.** You need `j − i` at the end. Storing values
  and losing the positions is the classic first-draft bug.
- **`>= k`, not `> k`.** The `214 − 47 = 167` row above is exactly the case that a
  strict `>` gets wrong.
- **Pop from the front *only* after recording.** `best = min(best, j - dq.popleft())` in
  one expression keeps that honest; splitting it across lines invites popping without
  measuring.
- **The sentinel `best = n + 1`** and the final `if best <= n`, returning `-1` for
  "impossible" is part of the spec, and `float('inf')` works too as long as the return
  converts it.
- **This is not EP22.** If every value is positive, the two-pointer window from EP22 is
  simpler and also O(n), say so. The deque is the price of negatives.

## 🎤 Interview talking points
- *"Sliding window is out: with negatives the sum isn't monotonic in the window length,
  so shrinking from the left proves nothing."* ← rule out the wrong answer first, with
  a reason.
- *"I want, for each right end, the latest earlier prefix that's at most `pre[j] − k`.
  That's a range query, not an equality lookup, so a hash map can't do it."* ← this
  sentence is why the episode exists.
- *"Two discard rules: an index that already produced an answer is done, and an index
  whose prefix is at least the current one is dominated. What's left increases, so the
  front is always the best candidate."*
- *"Each index is pushed and popped at most once, so it's O(n) despite the nested
  loops."* ← the amortised argument; expect to be asked for it.

## 🔗 Transfer
This episode swapped the hash map for a structure that respects **order**, and tomorrow
(EP44) pushes that one step further: counting how many earlier prefixes fall inside a
*range* `[running − upper, running − lower]`, which needs sorting, a BIT or a merge
sort. The monotonic deque itself comes back in Pattern 08 (Stack) for Sliding Window
Maximum, where the same two-pop reasoning appears with the inequality flipped.

## 📹 Metadata
- **Title:** `Shortest Subarray with Sum at Least K, when the window dies | Prefix Sum #5`
- **Thumbnail:** `NEGATIVES KILL THE WINDOW` (red block)
- **Short:** `[84,-37,32,40,95], k=167`, the window saying 5, the deque saying 3. 55s.
