# EP036 · P04E04 · Maximum Subarray Sum with One Deletion   [Medium]

**Pattern:** Kadane · **Link:** https://leetcode.com/problems/maximum-subarray-sum-with-one-deletion/

---

## 🎬 Hook
> "You get one free deletion, you may remove a single element from your subarray. That
> sounds like it needs a rethink, and it doesn't: it needs a **second Kadane running
> alongside the first**, one that has already spent the budget. 'One allowed change' is
> a state, not a new algorithm."

## 📋 Problem, in your words
```
Given an integer array, find the maximum sum of a non-empty contiguous subarray
after OPTIONALLY deleting exactly one element from it.

You may delete nothing. If you delete, the remaining elements must still be
non-empty -- you can't delete the only element.
```

## 🔢 The example
```
Input:  nums = [1, -2, 0, 3]
Output: 4
Why:    take [1, -2, 0, 3] and delete the -2 -> 1 + 0 + 3 = 4.

Input:  nums = [1, -2, -2, 3]
Output: 3
Why:    one deletion can't rescue two adjacent negatives, so just take [3].

Input:  nums = [-1, -1, -1, -1]
Output: -1
Why:    everything is negative and the result must be non-empty.
```

That third one is the trap: you may not delete your way down to nothing.

## 🧸 ELI5
> You're walking the array collecting a score, same as Kadane, but you also carry
> **one eraser**, good for exactly one number.
>
> At every step you're in one of two situations:
>
> - **eraser unused:** your best run ending here, having deleted nothing.
> - **eraser used:** your best run ending here, having deleted exactly one element.
>
> And the second situation can be reached two ways: you were already in it and just
> extended the run, **or** you were in the first situation and you're spending the
> eraser on *this* element right now.
>
> Track both numbers. The answer is the best either one ever reached.

## 🐌 Brute force (say it, don't type it)
For every element, delete it and run Kadane on what's left. **O(n²).** Correct and easy
to describe, say it, then note you're going to do it in one pass by carrying the
deletion as a state.

## 💡 The pattern reveal
**Signal:** a Kadane problem · "with at most one <modification>".
**Therefore:** Kadane with **two parallel states**, one that has spent the budget.

**Key insight, the two recurrences:**

```python
keep   = max(keep + x, x)          # ordinary Kadane: extend, or start fresh here
delete = max(delete + x, keep)     # (a) already deleted, extend with x
                                   # (b) delete x RIGHT NOW, so take keep as it was
```

Line two is the whole episode, so read it slowly on camera:

| option | meaning | expression |
|---|---|---|
| (a) | I deleted something earlier; `x` joins the run | `delete + x` |
| (b) | I delete `x` itself; the run is whatever I had before `x` | `keep` (the *old* one) |

**`keep` must be the value from before this iteration** when you use it in (b), which
is why the `delete` line comes *first* in the code below. Update `keep` first and
option (b) silently becomes "delete `x`, but also include `x`," which is nonsense.

**Why no explicit "non-empty after deletion" check is needed:** option (b) uses the old
`keep`, which is the best run *ending at the previous index*, a run that already
contains at least one element. So the deleted-state run is never empty by construction.
That's why `[-1,-1,-1,-1]` returns `-1` and not `0`.

## 🔍 Dry run: `[1, -2, 0, 3]`
Seed: `keep = delete = best = 1`.

| i | x | `delete = max(delete+x, keep_old)` | `keep = max(keep+x, x)` | `best` |
|---|---|---|---|---|
| 1 | −2 | max(1 + (−2), **1**) = **1** ← deleted the −2 | max(1−2, −2) = −1 | 1 |
| 2 | 0 | max(1 + 0, −1) = **1** | max(−1+0, 0) = **0** | 1 |
| 3 | 3 | max(1 + 3, 0) = **4** | max(0+3, 3) = **3** | **4** |

Return **4**: the run `[1, −2, 0, 3]` with the `−2` erased.

Follow the `delete` column: at `i=1` it spends the eraser on the `−2` (taking the old
`keep` of 1), and from there it just extends, ending at `1 + 0 + 3 = 4`. Meanwhile
`keep` never recovers past 3. Two runners, and the one who used the eraser wins.

## ✅ Optimal solution
```python
class Solution:
    def maximumSum(self, arr: List[int]) -> int:
        """Max subarray sum with at most one element deleted.

        Time:  O(n), one pass, two states.
        Space: O(1).
        """
        keep = delete = best = arr[0]

        for x in arr[1:]:
            # `delete` FIRST -- option (b) needs `keep` from the previous index.
            delete = max(delete + x, keep)   # (a) extend a deleted run | (b) delete x now
            keep   = max(keep + x, x)        # ordinary Kadane
            best   = max(best, keep, delete)

        return best
```
**Time:** O(n) · **Space:** O(1)

### The alternative framing worth showing
Compute two arrays, `left[i]` = best subarray ending at `i`, `right[i]` = best
subarray starting at `i`, then for each `i`, deleting `arr[i]` gives
`left[i-1] + right[i+1]`:

```python
best = max(max(left), max(left[i-1] + right[i+1] for i in range(1, n-1)))
```
**O(n) time, O(n) space.** Less elegant, but noticeably easier to explain and to get
right, and the "prefix best / suffix best" idea is worth having in your hands, it
solves a whole family of "remove one element" problems. Show both.

## ⚠️ Gotchas
- **Update `delete` before `keep`.** Option (b) must see the *previous* `keep`. This is
  the bug of the episode and it produces answers that are too large. If the ordering
  makes you nervous, save `keep_old = keep` at the top of the loop and use it
  explicitly, clearer, and free.
- **Seed all three with `arr[0]`**, not 0. Same lesson as EP33, and here it is what
  makes the all-negative case come out as `-1` instead of `0`.
- **`delete` starting at `arr[0]`** is technically "deleted nothing yet", that's fine,
  because it can only ever be improved, and the non-empty guarantee comes from option
  (b) using `keep`.
- **You may delete nothing**, so `best` must consider `keep` too. Taking only `delete`
  fails on `[1, 2, 3]`.
- **Single-element array** returns that element. Check it, a wrong loop seed shows up
  here immediately.
- The result must be non-empty *after* deletion, which is why you can't "delete the only
  element." Read the constraint out loud; interviewers add it deliberately.

## 🎤 Interview talking points
- *"'At most one deletion' is a second state, not a second algorithm. I run two
  Kadanes: one that hasn't used the deletion and one that has."*
- *"The deleted state has two ways to arrive: extend an already-deleted run, or delete
  the current element and inherit the undeleted run from one index back."*
- *"Order matters, I update the deleted state first, because it reads the undeleted
  state from the previous index."*
- *"If I wanted something easier to defend, prefix-best and suffix-best arrays give the
  same answer in O(n) time and O(n) space."*

## 🔗 Transfer
"**A budget becomes a state**" is one of the highest-leverage ideas in the whole sheet.
It's the bridge from Kadane to Pattern 15 (DP), where problems like *Best Time to Buy
and Sell Stock with Cooldown* and *with at most k transactions* are exactly this,
scaled up: one state per amount of budget consumed.

## 📹 Metadata
- **Title:** `Max Subarray Sum with One Deletion, a budget is just a state | Kadane #4`
- **Thumbnail:** `ONE ERASER` (green block)
- **Short:** The two-line recurrence, with the "use the OLD keep" arrow drawn on. 50s.
