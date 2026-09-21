# EP035 · P04E03 · Maximum Product Subarray   [Medium]

**Pattern:** Kadane · **Link:** https://leetcode.com/problems/maximum-product-subarray/

---

## 🎬 Hook
> "Swap addition for multiplication and Kadane breaks — because the *worst* running
> total you're carrying can become the best one the instant you meet a negative number.
> The fix is to stop tracking one state and start tracking two. This is the episode
> where Kadane grows up."

## 📋 Problem, in your words
```
Given an integer array, find the contiguous subarray with the largest PRODUCT,
and return that product.

Non-empty. The array may contain negatives and zeros.
```

## 🔢 The example
```
Input:  nums = [2, 3, -2, 4]
Output: 6        ([2,3] -- the -2 poisons anything that includes it here)

Input:  nums = [-2, 3, -4]
Output: 24       (the WHOLE array: -2 * 3 * -4 = 24)
                 Two negatives cancel. The best answer contains the worst prefix.

Input:  nums = [-2, 0, -1]
Output: 0        (the zero wins -- both neighbours are single negatives)
```

The middle example is the episode. `[-2, 3, -4]` is three elements long and it defeats
plain Kadane completely.

## 🧸 ELI5
> Running totals with **addition** only ever get worse when they're negative. Running
> totals with **multiplication** are different: a big negative is a *loaded spring*. The
> moment you multiply it by another negative, it becomes a big positive.
>
> So carrying "the worst product so far" is useful — it's not garbage, it's potential
> energy.
>
> That means at every step you track **two** things: the biggest product ending here
> and the smallest one. And when the next number is negative, they **swap roles** —
> your best becomes your worst and your worst becomes your best.

## 🐌 Brute force (say it, don't type it)
Every start, every end, running product. **O(n²).**

Worth naming the extra trap: you cannot fix this with division ("divide out the element
leaving the window"), because a single `0` anywhere makes that arithmetic impossible.
That's the natural first idea and it's wrong — say so.

## 💡 The pattern reveal
**Signal:** contiguous subarray · maximum **product** · negatives present.
**Therefore:** Kadane with **two running states**.

**Key insight:** maintain

- `hi` = the largest product of a subarray ending here
- `lo` = the smallest product of a subarray ending here

When the next element `x` is negative, multiplying flips the ordering: `hi * x` becomes
small and `lo * x` becomes large. So **swap them before updating**:

```python
if x < 0:
    hi, lo = lo, hi
hi = max(x, hi * x)
lo = min(x, lo * x)
```

The `max(x, ...)` and `min(x, ...)` handle zeros for free — after a `0`, both states
reset to `x` on the next element, because `0 * x = 0` loses to `x` whenever `x` beats
zero, and the `max` picks correctly either way.

## 🔍 Dry run — `[-2, 3, -4]`
Seed: `hi = lo = best = -2`.

| i | x | negative? | after swap (`hi`,`lo`) | `hi = max(x, hi·x)` | `lo = min(x, lo·x)` | `best` |
|---|---|---|---|---|---|---|
| 1 | 3 | no | (−2, −2) | max(3, −6) = **3** | min(3, −6) = **−6** | 3 |
| 2 | −4 | **yes** → swap | (−6, 3) | max(−4, **24**) = **24** | min(−4, −12) = **−12** | **24** |

Return **24**.

Row 2 is the whole point. At `i=1` the algorithm was carrying a *useless-looking* `−6`.
One negative number later, that `−6` became `24` — the answer. Plain Kadane, tracking
only `hi`, would have carried `3` into the last step and returned `max(−4, −12) = −4`.
**Show that failure on camera before showing the fix.**

## 🔍 Dry run — `[2, 3, -2, 4]`
| i | x | swap? | `hi` | `lo` | `best` |
|---|---|---|---|---|---|
| — | — | — | 2 | 2 | 2 |
| 1 | 3 | no | max(3, 6) = **6** | min(3, 6) = 3 | **6** |
| 2 | −2 | yes → (3, 6) | max(−2, −6) = **−2** | min(−2, −12) = −12 | 6 |
| 3 | 4 | no | max(4, −8) = **4** | min(4, −48) = −48 | 6 |

Return **6**. Here the negative genuinely did poison things, and the algorithm restarted
at row 2 — the `max(x, ...)` doing its job.

## ✅ Optimal solution
```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        """Largest product of any non-empty contiguous subarray.

        Time:  O(n) — one pass.
        Space: O(1) — three integers.
        """
        hi = lo = best = nums[0]

        for x in nums[1:]:
            if x < 0:
                hi, lo = lo, hi        # a negative swaps their roles
            hi = max(x, hi * x)        # largest product ending here
            lo = min(x, lo * x)        # smallest -- tomorrow's largest, maybe
            best = max(best, hi)

        return best
```
**Time:** O(n) · **Space:** O(1)

### The swap-free version, if you prefer
```python
for x in nums[1:]:
    candidates = (x, hi * x, lo * x)
    hi, lo = max(candidates), min(candidates)
    best = max(best, hi)
```
Identical behaviour, no sign reasoning to get wrong, one extra tuple per step. Under
interview pressure this is arguably the better thing to write — it's very hard to make
a mistake in. Show both and say which you'd pick.

## ⚠️ Gotchas
- **Swap *before* updating, and compute `hi` and `lo` from the same snapshot.** Writing
  `hi = max(x, hi*x)` and then `lo = min(x, lo*x)` where `lo` is already the *new* `hi`
  is the classic corruption. The tuple version above makes this impossible — that's why
  it's worth knowing.
- **Seed with `nums[0]`, not `1`.** A seed of `1` is multiplication's version of the
  zero-seed bug: on `[-2]` it returns `1`, a product of no elements.
- **Zeros reset both states**, and that's correct — a subarray spanning a zero has
  product zero. But `best` must still be allowed to *be* zero, which it is, since
  `best = max(best, hi)` and `hi` becomes 0 at that index. Test `[-2, 0, -1]` → `0`.
- **Division does not work here.** With a zero in the array you cannot undo a
  multiplication. Say it; it's the idea most people try first.
- **Overflow** is a non-issue in Python and a real one in C++/Java — mention `long
  long` if the interviewer's language demands it.

## 🎤 Interview talking points
- *"With multiplication, the minimum product is valuable — a negative times a negative
  is positive — so I track the largest and smallest product ending at each index."*
- *"A negative element swaps their roles, so I swap before updating."*
- *"`[-2, 3, -4]` is the case that breaks single-state Kadane: the answer is the whole
  array, and the winning prefix looked like the worst option one step earlier."* ←
  naming the concrete counterexample is what makes this convincing.
- *"Division would let me slide a window, but a single zero makes it impossible."*

## 🔗 Transfer
"Track two states because the future can invert their roles" is the idea, and it comes
back immediately: EP36 tracks a *with-deletion* and *without-deletion* state; EP37
tracks a maximum and a minimum for a different reason. In Pattern 15 (DP), carrying
several states per index is the normal situation rather than the exception — this
episode is the first taste of it.

## 📹 Metadata
- **Title:** `Maximum Product Subarray — why you must track the minimum too | Kadane #3`
- **Thumbnail:** `THE WORST BECOMES BEST` (green block)
- **Short:** `[-2,3,-4]` breaking single-state Kadane, then the two-state fix. 50s.
