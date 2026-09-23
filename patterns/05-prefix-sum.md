# Pattern 05: Prefix Sum

**6 episodes · EP 39–44**

---

## The one-sentence version

Every range sum is the **difference of two prefix sums**, so "find a subarray whose sum
does X" becomes "find a **pair of prefix values** whose difference does X", and a hash
map answers pair questions in O(1): **O(n²) → O(n)**.

## ELI5

Walk the array keeping a running total. At index `i` you're holding `pre[i]`, the sum of
everything behind you.

```
nums:         3   4   7   2  -3   1
prefix:   0   3   7  14  16  13  14
          ^                       ^
          pre[0] = 0, the EMPTY prefix
```

The sum of `nums[a..b]` is `pre[b+1] − pre[a]`. That's the entire pattern. Once you
believe it, the question changes shape:

| the subarray question | becomes the prefix question |
|---|---|
| a subarray summing to `k` | two prefixes **differing by `k`** |
| a subarray divisible by `k` | two prefixes with the **same remainder** mod `k` |
| equal 0s and 1s | two prefixes that are **equal** (after mapping 0 → −1) |
| a sum in `[lo, hi]` | two prefixes differing by something in `[lo, hi]` |

And "have I seen a prefix like that?" is a dictionary lookup.

## How to recognise it

| Signal | Example |
|---|---|
| "**how many** subarrays sum to …" | Subarray Sum Equals K (EP39) |
| "longest subarray such that …" | Contiguous Array (EP42) |
| a **range sum** queried repeatedly | Find Pivot Index (EP40) |
| divisibility / remainders | Subarray Sums Divisible by K (EP41) |
| the array contains **negatives** and you wanted a window | Shortest Subarray ≥ K (EP43) |

**The negatives test.** This is the same fork as Pattern 04, one step further on:

| | Sliding Window (P03) | Kadane (P04) | Prefix Sum (P05) |
|---|---|---|---|
| handles negatives | no | yes | yes |
| answers | one best window | one best sum | **counts, lengths, ranges** |
| keeps | `[lo, hi]` | a running total | a running total **plus a map of the past** |

Kadane keeps one number about the past. Prefix Sum keeps *all* of it, in a dictionary,
which is exactly what buys you counting.

## The shape

```python
def count_subarrays_summing_to(nums, k):
    seen = {0: 1}                       # the EMPTY prefix, seen once
    running = count = 0
    for x in nums:
        running += x
        count += seen.get(running - k, 0)     # every earlier prefix that completes a k
        seen[running] = seen.get(running, 0) + 1
    return count
```

**Why `seen = {0: 1}` and not `{}`:** a subarray that starts at index 0 has no earlier
element in front of it, its "left prefix" is the empty one, worth 0. Leave `0` out of
the map and every answer beginning at the first element is silently dropped. This is the
Pattern 05 equivalent of Kadane's *"seed with `nums[0]`, never `0`"*, and it is the
single most common bug in these six problems.

Note also **`count +=`, not `count = max(...)`**: there may be several earlier prefixes
with the same value and each one is a different valid subarray. Add the count, don't
flag a boolean.

## The three variations you need

### 1. Transform the values first, then ask for *equality* (EP41, EP42)

The map only ever answers "have I seen this exact key?" So change the values until the
question **is** about equality:

```python
running = (running + x) % k      # EP41: equal remainders  <=> difference divisible by k
running += 1 if x == 1 else -1   # EP42: equal running sums <=> equal counts of 0 and 1
```

Both problems look nothing like EP39 and are the same three lines underneath.

### 2. Store a count, or store the first index: never both (EP39/41 vs EP42)

| the question is | the map value is | on a repeat key |
|---|---|---|
| **how many** subarrays | a **count** | increment it |
| the **longest** subarray | the **first index** the key appeared at | **leave it alone** |

Overwriting the stored index in a "longest" problem is a wrong answer, not a crash: you
keep measuring from the most recent occurrence instead of the earliest, and report a
window that is too short.

### 3. When the question isn't equality, you need order, not a map (EP43, EP44)

A hash map cannot answer "is there an earlier prefix **at most** `p − k`?", that's a
range query. Two tools:

```python
# EP43: keep prefix indices in a deque with INCREASING prefix values
while dq and p - pre[dq[0]] >= k:  best = min(best, j - dq.popleft())   # found; never needed again
while dq and pre[dq[-1]] >= p:     dq.pop()   # p is smaller AND later -- strictly better
```

```python
# EP44: count earlier prefixes inside [running - upper, running - lower]
# -> an ordered structure: merge sort, a BIT, or a sorted list
```

This is the honest boundary of the pattern: the prefix insight still holds, but the
lookup structure gets upgraded from a dict to something that keeps order.

## Complexity

| Problem | Time | Space |
|---|---|---|
| EP39, EP41, EP42 | O(n) | O(n), the map |
| EP40 | O(n) | **O(1)**: no map at all |
| EP43 | O(n) | O(n), the deque |
| EP44 | O(n log n) | O(n) |
| brute force you're beating | O(n²) | O(1) |

The space is the honest cost of the pattern: you're trading memory for the ability to
ask about *any* earlier position in O(1).

## The episodes

| EP | Problem | Variation | The thing it teaches |
|---|---|---|---|
| 39 | Subarray Sum Equals K | count pairs | `{0: 1}`, and why you add rather than flag. |
| 40 | Find Pivot Index | no map | Prefix sums without a dictionary: `total − left − x`. |
| 41 | Subarray Sums Divisible by K | transform | Same remainder ⇒ divisible difference. Negative mod. |
| 42 | Contiguous Array | transform + first index | 0 → −1 turns "balanced" into "equal". Store the earliest index. |
| 43 | Shortest Subarray with Sum ≥ K | monotonic deque | Why negatives break the window, and what replaces it. |
| 44 | Count Range Sum | ordered structure | Counting pairs in a *range* needs sorting, not hashing. |

## What "knowing this in your sleep" means

1. What is `pre[0]` and why does it exist? *(The empty prefix, 0. Without it, every
   answer that starts at index 0 is lost.)*
2. When does the map store a count, and when a first index? *(Counting → count.
   Longest → earliest index, never overwritten.)*
3. How do you turn "divisible by k" into an equality question? *(Key on
   `running % k`. Equal remainders mean the difference is a multiple of k.)*
4. Why can't you slide a window over an array with negatives? *(Growing the window can
   shrink the sum, so neither pointer is monotonic and shrinking proves nothing.)*
5. What do you reach for when the question is a range rather than an exact value?
   *(An ordered structure, monotonic deque, BIT, or merge sort, because a hash map
   only answers exact keys.)*
