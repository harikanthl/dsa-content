# Pattern 03: Sliding Window

**12 episodes · EP 21–32**

---

## The one-sentence version

When the answer is about a **contiguous run** of an array or string, don't rebuild each
run from scratch, **slide** a window across, adding what enters on the right and
removing what leaves on the left: **O(n²) → O(n)**.

## ELI5

You're looking through a cardboard tube at a row of houses, trying to find the best
stretch of five in a row.

The slow way is to walk back to the start for every possible stretch and count again.

The fast way: keep the tube at your eye and **shuffle sideways**. When house 6 comes
into view, house 1 leaves it. You don't recount the four in the middle, they didn't
change. One step, one addition, one subtraction.

Everything in this pattern is that idea. The only question that ever varies is **when
do I shuffle?**

## How to recognise it

| Signal | Example |
|---|---|
| "subarray" / "substring", i.e. **contiguous** | almost every problem here |
| "of size k" | Max Sum Subarray of Size K (EP21) |
| "longest ... such that <condition>" | K Distinct, No-repeat, Fruits (EP23–27) |
| "smallest / minimum ... such that <condition>" | Min Size Subarray Sum, Min Window (EP22, EP29) |
| "contains a permutation / anagram of" | EP30, EP31 |
| a **count** of qualifying subarrays | Subarray Product Less Than K (EP8) |

**The anti-signal:** if the problem says *subsequence* rather than *subarray*, elements
need not be adjacent and this pattern does not apply. That single word decides it; read
it carefully every time.

**Contrast with Two Pointers.** Two pointers usually converge from the ends of a
**sorted** array. A sliding window has both pointers moving **left to right** and does
not need sorted input. If the input is sorted and you're converging, that's Pattern 01;
if you're dragging a contiguous region forward, it's this one.

## The three shapes

### Shape A: Fixed window (size k is given)

```python
window_sum = sum(nums[:k])
best = window_sum
for hi in range(k, len(nums)):
    window_sum += nums[hi] - nums[hi - k]   # one in, one out
    best = max(best, window_sum)
return best
```

Both edges move together, every step, forever. There is no decision to make. Time O(n),
space O(1).

### Shape B: Variable window, **longest** valid

```python
lo = 0
for hi in range(len(nums)):
    add(nums[hi])                    # grow right, always
    while not valid():               # shrink left only while broken
        remove(nums[lo]); lo += 1
    best = max(best, hi - lo + 1)    # record AFTER restoring validity
```

The right edge advances unconditionally. The left edge only moves to repair a broken
window. **Record the answer after the while loop**, when the window is guaranteed valid.

### Shape C: Variable window, **shortest** valid

```python
lo = 0
for hi in range(len(nums)):
    add(nums[hi])
    while valid():                   # shrink while STILL valid
        best = min(best, hi - lo + 1)  # record BEFORE removing
        remove(nums[lo]); lo += 1
```

The mirror image, and the two differences are exactly the ones people get wrong:

| | Shape B (longest) | Shape C (shortest) |
|---|---|---|
| `while` condition | `while NOT valid` | `while valid` |
| record the answer | **after** the loop | **inside** the loop, before removing |

Write both on the board when you're stuck and pick the one whose question you're
answering. Half the bugs in this pattern are Shape B code answering a Shape C question.

## Why it's O(n) and not O(n²)

The inner `while` makes it *look* quadratic. It isn't: `lo` only ever moves **forward**,
and it can move at most `n` times across the entire run. So the two pointers together
take at most `2n` steps. This is **amortised analysis**: say the word out loud in an
interview; it's the single most common thing candidates get wrong about this pattern.

## The bookkeeping toolkit

What you keep about the window decides the problem's difficulty:

| Keep | Enables | Episodes |
|---|---|---|
| a running **sum** | sum thresholds | EP21, EP22, EP28 |
| a **count of zeros** | "flip at most k" | EP27 |
| a `dict` of **char → count** | distinct-character limits | EP23, EP24 |
| a dict + `len(dict)` | "at most k distinct" | EP23, EP24 |
| a dict + **last index seen** | jump `lo` instead of walking it | EP25 |
| `need` / `missing` counters | "contains all of ..." | EP29, EP30, EP31 |
| a dict of **word → count** | word-granular windows | EP32 |

**The `missing` counter is the trick worth learning cold** (EP29). Instead of comparing
two dictionaries on every step, O(k) per step, keep one integer: how many required
characters are still unmatched. Zero means the window is valid. It turns an O(nk)
solution into O(n).

## Complexity

| Shape | Time | Space |
|---|---|---|
| A, fixed | O(n) | O(1) |
| B, longest | O(n) amortised | O(k) for the counter |
| C, shortest | O(n) amortised | O(k) |
| brute force you're beating | O(n²) or O(n²k) | O(1) |

## The episodes

| EP | Problem | Shape | The thing it teaches |
|---|---|---|---|
| 21 | Maximum Sum Subarray of Size K | A | The base case. One in, one out. |
| 22 | Smallest Subarray with a given sum | C | First variable window. Shrink while valid. |
| 23 | Longest Substring with K Distinct | B | The counter dict, and `len(dict)` as the test. |
| 24 | Fruits into Baskets | B | The same problem in a costume. Recognise it. |
| 25 | No-repeat Substring | B | Jumping `lo` with last-seen indices. |
| 26 | Longest Substring, Same Letters after Replacement | B | `maxCount` never decreases, the famous "wrong but correct" window. |
| 27 | Longest Subarray with Ones after Replacement | B | EP26 reduced to two symbols. |
| 28 | Minimum Size Subarray Sum (revisited) | C | Same problem as EP22, solved the *other* way: prefix sums + binary search, and why O(n) still wins. |
| 29 | Minimum Window Substring | C | The `missing` counter. The hardest window problem there is. |
| 30 | Permutation in a String | A | Fixed window + frequency match. |
| 31 | String Anagrams | A | EP30 returning all matches. |
| 32 | Words Concatenation | A (word-granular) | Windows whose unit is a word, not a character. |

## What "knowing this in your sleep" means

1. Why is the two-pointer scan O(n) when there's a nested `while`? *(`lo` only moves
   forward, at most n times total, amortised.)*
2. Longest vs shortest: which way does the `while` test point, and where does the
   answer get recorded? *(B: `while not valid`, record after. C: `while valid`, record
   inside.)*
3. What do you keep about the window, and can you update it in O(1) per step?
4. Why does EP26 work even though `maxCount` is sometimes stale? *(The window never
   needs to shrink, only to stop growing. A stale max can only hold it back, never
   let it lie.)*
5. Subarray or subsequence? *(Subsequence kills this pattern dead.)*
