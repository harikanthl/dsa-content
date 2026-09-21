# Pattern 04 — Kadane's Algorithm

**6 episodes · EP 33–38**

---

## The one-sentence version

For "best contiguous subarray" questions, walk the array once asking a single question
at each element — **extend the run, or start a new one here?** — and keep the best
answer you've ever seen: **O(n²) → O(n)**.

## ELI5

You're walking along the array collecting a score, and at every step you ask **one**
question:

> *Is what I'm carrying actually helping me?*

If your running total is positive, carry it forward and add the new element. If it's
negative, **drop it** — a negative prefix can only drag down everything that follows,
so you're better off starting fresh from where you stand.

That's it. One comparison per element.

```python
current = max(x, current + x)     # start fresh, or extend
best    = max(best, current)      # remember the best run ever seen
```

The subtlety people miss: `current` is *"the best run that ENDS exactly here"*, while
`best` is *"the best run anywhere so far."* Two different quantities, and you need both.
Confusing them is the source of nearly every Kadane bug.

## How to recognise it

| Signal | Example |
|---|---|
| "maximum/minimum **contiguous** subarray" | Maximum Subarray (EP33) |
| the array contains **negative numbers** | the whole reason this exists |
| "maximum product" / "maximum absolute" | EP35, EP37 |
| a variant with one allowed modification | Subarray Sum with One Deletion (EP36) |
| a **circular** array | Circular Subarray (EP38) |

**Kadane vs Sliding Window** — this is the distinction to have ready:

| | Sliding Window (P03) | Kadane (P04) |
|---|---|---|
| needs | all **positive** values | works **with negatives** |
| keeps | an explicit `[lo, hi]` window | one running total, no window |
| question | "should I shrink from the left?" | "should I abandon what I'm carrying?" |
| breaks when | values go negative | — |

If the array has negatives and you reach for a sliding window, you will get a wrong
answer. Notice the sign of the input before you choose.

## The shape

```python
def kadane(nums):
    best = current = nums[0]        # seed with a REAL element, never 0
    for x in nums[1:]:
        current = max(x, current + x)   # abandon, or extend
        best = max(best, current)
    return best
```

**Why seed with `nums[0]` and not `0`:** an all-negative array like `[-3, -1, -2]` has
answer `-1`, but seeding with `0` returns `0` — a subarray that doesn't exist. Empty
subarrays are not allowed unless the problem says so. This is the single most common
Kadane mistake and it appears in every episode of this pattern.

## The three variations you need

### 1. Track two states when negatives can flip things (EP35, EP37)

For **products**, a large negative multiplied by a negative becomes a large positive —
so the minimum is as valuable as the maximum. Carry both:

```python
hi = lo = best = nums[0]
for x in nums[1:]:
    if x < 0: hi, lo = lo, hi      # a negative swaps their roles
    hi = max(x, hi * x)
    lo = min(x, lo * x)
    best = max(best, hi)
```

### 2. Track a second "budget spent" state (EP36)

When one modification is allowed, run two Kadanes side by side — one that hasn't used
the modification, one that has:

```python
keep   = max(keep + x, x)          # no deletion used
delete = max(delete + x, keep)     # either continue a deleted run, or delete x now
```

### 3. Total minus the minimum (EP38)

For a **circular** array, the answer either doesn't wrap (ordinary Kadane) or it does —
and a wrapping subarray is exactly `total − (some non-wrapping subarray)`. So maximise
by *minimising* the part you throw away:

```python
answer = max(max_kadane, total - min_kadane)
```
…with one guard: if every number is negative, `total − min` is the **empty** subarray,
which isn't allowed. Return `max_kadane` in that case.

## Complexity

| Problem | Time | Space |
|---|---|---|
| all six episodes | O(n) | O(1) |
| brute force you're beating | O(n²) | O(1) |

Every problem in this pattern is one pass and a handful of variables. If your solution
needs an array, you've over-thought it.

## The episodes

| EP | Problem | Variation | The thing it teaches |
|---|---|---|---|
| 33 | Maximum Subarray Sum | base | `current` vs `best`, and never seeding with 0. |
| 34 | Minimum Subarray Sum | base, mirrored | Flip every max to a min. Proves you understood the shape. |
| 35 | Maximum Product Subarray | two states | A negative swaps the roles of max and min. |
| 36 | Maximum Subarray Sum with One Deletion | two states | "One allowed modification" = a second parallel state. |
| 37 | Maximum Absolute Sum | two states | `max(max_sum, |min_sum|)` — run both Kadanes. |
| 38 | Maximum Sum Circular Subarray | total − min | The wrap case, and the all-negative trap. |

## What "knowing this in your sleep" means

1. What exactly does `current` mean? *(The best subarray ENDING at this index — not the
   best so far.)*
2. Why seed with `nums[0]` rather than `0`? *(All-negative arrays; an empty subarray is
   not a legal answer.)*
3. Why does the product version track a minimum too? *(A negative times a large
   negative is a large positive, so today's worst can be tomorrow's best.)*
4. How do you handle "one allowed change"? *(A second running state that has spent the
   budget, updated from the first.)*
5. Why does the circular answer equal `total − min_subarray`? *(Whatever wraps is the
   complement of something that doesn't. And if everything is negative, that complement
   is empty — which is why that case needs its own guard.)*
