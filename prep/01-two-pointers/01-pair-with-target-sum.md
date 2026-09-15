# EP001 · P01E01 · Pair with Target Sum   [Easy]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

---

## 🎬 Hook
> "This array is sorted — and almost everybody ignores that. That one word is the
> entire problem. Ignore it and you write O(n²). Use it and you write O(n) with two
> variables and no extra memory."

## 📋 Problem, in your words
```
Given an array of numbers that is ALREADY SORTED in increasing order,
find the two numbers that add up to a given target.

Return their positions, 1-indexed (not 0-indexed — LeetCode is being annoying).
Exactly one answer exists. You may not use the same element twice.
```

## 🔢 The example
```
Input:  numbers = [2, 7, 11, 15],  target = 9
Output: [1, 2]
Why:    numbers[0] + numbers[1] = 2 + 7 = 9. In 1-indexed terms, positions 1 and 2.
```

## 🧸 ELI5
> A shelf of books sorted thinnest to thickest. You want two whose pages add to 500.
>
> Finger on the thinnest, finger on the thickest. Add them up.
> - **Too many pages?** The thick one is too thick. Slide the right finger left.
> - **Too few pages?** The thin one is too thin. Slide the left finger right.
>
> The magic: every slide throws away a book *forever*, and you're allowed to,
> because sorting guarantees everything past it is worse in the same direction.
> Two fingers, one walk down the shelf, done.

## 🐌 Brute force (say it, don't type it)
Two nested loops: try every pair, check if it hits the target — **O(n²)**.

Why it's wasteful: when `2 + 15 = 17` overshoots a target of 9, the brute force
goes on to test `7 + 15` and `11 + 15`. But those are *bigger*. The array is sorted,
so we already know they overshoot too. The brute force is re-learning something the
sorted order told us for free.

## 💡 The pattern reveal
**Signal:** the word *sorted* in the problem statement, plus "find a pair."
**Therefore:** Two Pointers, Shape A — converging from opposite ends.

**Key insight:** from the two ends, the sum can only move in one direction per
pointer. `lo` can only ever *increase* the sum; `hi` can only ever *decrease* it.
So the comparison against target tells you unambiguously which finger to move.
There's never a guess.

> Note for the video: this is **Two Sum II**, not Two Sum I. Two Sum I is unsorted →
> hash map. Mention this. It's the #1 confusion for beginners and a great 45-second
> Short on its own.

## 🔍 Dry run — `[2, 7, 11, 15]`, target 9
| step | lo | hi | numbers[lo] + numbers[hi] | vs 9 | action |
|---|---|---|---|---|---|
| 1 | 0 | 3 | 2 + 15 = 17 | too big | `hi -= 1` → kill 15 forever |
| 2 | 0 | 2 | 2 + 11 = 13 | too big | `hi -= 1` → kill 11 forever |
| 3 | 0 | 1 | 2 + 7 = **9** | hit | return `[1, 2]` |

Three steps on a 4-element array. Brute force would have tried 6 pairs.

## ✅ Optimal solution
```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        lo, hi = 0, len(numbers) - 1

        while lo < hi:
            total = numbers[lo] + numbers[hi]
            if total == target:
                return [lo + 1, hi + 1]      # problem wants 1-indexed
            if total < target:
                lo += 1                       # need bigger; only lo can grow it
            else:
                hi -= 1                       # need smaller; only hi can shrink it

        return []                             # unreachable: problem guarantees a solution
```
**Time:** O(n) — each pointer moves at most n times and never backwards, so ≤ 2n steps.
**Space:** O(1) — two integers, regardless of input size.

## ⚠️ Gotchas
- **1-indexed return.** `[lo + 1, hi + 1]`. This is the single most common wrong
  submission on this problem. Say it out loud when you type the `+ 1`.
- **`while lo < hi`, not `<=`.** With `<=` the pointers can land on the same element
  and you'd use one number twice, which the problem forbids.
- Do **not** reach for a hash map here. It works, but it's O(n) space for a problem
  that hands you sortedness for free. An interviewer will ask "can you do better on
  space?" and this is the answer they want.

## 🎤 Interview talking points
- *"Because it's sorted, I can eliminate a candidate with every comparison instead of
  testing every pair."*
- *"Each pointer is monotonic — `lo` only increases, `hi` only decreases — so the
  total work is bounded by n, not n²."*
- Proof of correctness, if pushed: *"If `numbers[lo] + numbers[hi] < target`, then
  `numbers[lo]` paired with any index ≤ `hi` is also < target, since everything at or
  below `hi` is ≤ `numbers[hi]`. So `lo` can't be in any solution and I can discard
  it safely."* ← **This is the sentence that separates a hire from a no-hire.**

## 🔗 Transfer
This exact converging loop is the inner engine of EP5 (3Sum), EP6 (3Sum Closest),
EP7 (Triplets with Smaller Sum) and EP10 (4Sum). Those problems are just *"fix one
number, then run today's code on the rest."* If today lands, the next week is easy.

## 📹 Metadata
- **Title:** `Two Sum II — the "sorted" trick almost nobody uses | Two Pointers #1`
- **Thumbnail:** `SORTED = FREE INFO` (blue block)
- **Short:** Beat 4 — the bookshelf analogy, 50 seconds vertical.
