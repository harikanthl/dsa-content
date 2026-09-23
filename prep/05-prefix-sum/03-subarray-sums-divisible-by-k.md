# EP041 · P05E03 · Subarray Sums Divisible by K   [Medium]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/subarray-sums-divisible-by-k/

---

## 🎬 Hook
> "Count the subarrays whose sum divides evenly by K. This looks like a number-theory
> problem and it is EP39 with one character changed. Two running totals that leave the
> **same remainder** when divided by K differ by a multiple of K, so key the dictionary
> on the remainder instead of the total, and the rest of the code is yesterday's."

## 📋 Problem, in your words
```
Given an integer array nums (negatives allowed) and an integer k,
return the NUMBER of contiguous non-empty subarrays whose sum is
divisible by k -- that is, sum % k == 0.

A sum of 0 counts: 0 is divisible by everything.
```

## 🔢 The example
```
Input:  nums = [4, 5, 0, -2, -3, 1], k = 5
Output: 7
Why:    [4,5,0,-2,-3,1], [5], [5,0], [5,0,-2,-3], [0], [0,-2,-3], [-2,-3]

Input:  nums = [-1, 2, 9], k = 2
Output: 2            <- [-1,2,9] = 10, and [2]. The negative prefix matters here.

Input:  nums = [5], k = 9
Output: 0
```

## 🧸 ELI5
> Imagine a clock face with `k` positions on it. Walk the array, and instead of tracking
> your running total, track **where the total lands on the clock**: `running % k`.
>
> ```
> k = 5, nums = [4, 5, 0, -2, -3, 1]
> running:   0    4    9    9    7    4    5
> clock:     0    4    4    4    2    4    0
>            ^ start of the walk, position 0
> ```
>
> Now: if you're standing on clock position `4` and you were **also** on position `4`
> earlier, then between those two moments you walked a whole number of laps, and one
> lap is exactly `k`. So the stretch between them sums to a multiple of `k`.
>
> The question stops being about division and becomes **"how many times have I stood on
> this clock position before?"**: and that is a dictionary lookup, exactly as in EP39.
> The only change is the key.

## 🐌 Brute force (say it, don't type it)
Every start, every end, running sum, `count += s % k == 0`. **O(n²)**. Worth saying,
because the leap to O(n) is *"I don't need the sum, I only need its remainder"* and that
sentence is the whole interview.

## 💡 The pattern reveal
**Signal:** count subarrays · **divisibility** condition · negatives present.
**Therefore:** prefix sums keyed on `running % k`, a hash map of counts.

**Key insight:** the algebra is two lines.

```
sum(a..b) = pre[b+1] - pre[a]

(pre[b+1] - pre[a]) % k == 0   <=>   pre[b+1] % k == pre[a] % k
```

Equal remainders ⇔ divisible difference. So this is EP39's *"how many earlier prefixes
equal `running − k`"* replaced by *"how many earlier prefixes share my remainder"*. Same
map, same `{0: 1}` seed, same query-then-insert order.

**🧨 The trap of the episode: negative remainders.** With a negative running total,
what `%` returns depends on the language:

| `running` | `k` | Python `running % k` | C++/Java `running % k` |
|---|---|---|---|
| −1 | 2 | **1** | **−1** |
| −3 | 5 | **2** | **−3** |

Python already floors toward negative infinity, so its remainder is always in
`[0, k)` and the code just works. In C++ or Java, `−1` and `1` would land in *different*
buckets and the match would be missed, a wrong answer, not a crash. The portable form
is:

```python
r = ((running % k) + k) % k
```

Say this on camera even in Python. Knowing *why* you don't need it is worth more than
not knowing you might.

## 🔍 Dry run: `nums = [4, 5, 0, -2, -3, 1]`, `k = 5`
Start: `seen = {0: 1}`, `running = 0`, `count = 0`.

| i | x | `running` | `r = running % 5` | seen `r` before | `count` | `seen` after |
|---|---|---|---|---|---|---|
| 0 | 4 | 4 | 4 | 0 | 0 | `{0:1, 4:1}` |
| 1 | 5 | 9 | **4** | **1** | **1** | `{0:1, 4:2}` |
| 2 | 0 | 9 | **4** | **2** | **3** | `{0:1, 4:3}` |
| 3 | −2 | 7 | 2 | 0 | 3 | `{0:1, 4:3, 2:1}` |
| 4 | −3 | 4 | **4** | **3** | **6** | `{0:1, 4:4, 2:1}` |
| 5 | 1 | 5 | **0** | **1** | **7** | `{0:2, 4:4, 2:1}` |

Answer **7** ✓

Two rows do the teaching:

- **`i = 2` adds 2 at once.** Remainder `4` had been seen twice already (after index 0
  and after index 1), so *two* subarrays end here: `[5, 0]` and `[0]`. This is why the
  count is added rather than incremented, the same reason as EP39, made unmissable.
- **`i = 5` matches the seeded `0`.** The prefix is `5`, remainder `0`, and it pairs
  with the **empty** prefix, giving the whole array `[4, 5, 0, −2, −3, 1] = 5`, the one answer that
  starts at index 0. Delete the `{0: 1}` seed and that answer disappears.

## 🔍 Dry run: `nums = [-1, 2, 9]`, `k = 2` (the negative-remainder case)
`seen = {0: 1}`.

| i | x | `running` | `r` (Python) | `r` (C++) | found | `count` |
|---|---|---|---|---|---|---|
| 0 | −1 | −1 | **1** | **−1** | 0 | 0 |
| 1 | 2 | 1 | **1** | 1 | **1** | **1** |
| 2 | 9 | 10 | 0 | 0 | **1** (the seed) | **2** |

Answer **2** ✓, the subarrays are `[2]` and `[−1, 2, 9] = 10`.

Look at `i = 1` in the C++ column: its remainder is `1`, but index 0 stored `−1`, so the
buckets don't match and `[2]` is never counted. The C++ answer without normalisation is
**1**. Same algorithm, different language, wrong answer.

## ✅ Optimal solution
```python
class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        """Count contiguous subarrays whose sum is divisible by k.

        Time:  O(n), one pass.
        Space: O(k), at most k distinct remainders, not n.
        """
        seen = {0: 1}                  # the EMPTY prefix: remainder 0, seen once
        running = count = 0

        for x in nums:
            running += x
            r = running % k            # Python's % is already in [0, k)
            count += seen.get(r, 0)    # every earlier prefix with this remainder
            seen[r] = seen.get(r, 0) + 1

        return count
```
**Time:** O(n) · **Space:** O(k)

## ⚠️ Gotchas
- **Negative remainders.** Python is safe; C++/Java/Go/Rust are not. The portable line
  is `r = ((running % k) + k) % k`, and knowing which languages need it is the point.
- **`seen = {0: 1}`.** Same seed as EP39, same failure without it, every subarray
  starting at index 0 vanishes. Test `[5], k = 5` → must be **1**.
- **Space is O(k), not O(n).** There are only `k` possible remainders. Saying this
  unprompted shows you understand what the key *is*. For large `k` an array of size `k`
  beats a dict.
- **Add the count, don't increment.** Row `i = 2` above adds 2 in one step.
- **Don't reduce `running` itself** with `running %= k` and then also key on it, it
  works, but mixing the reduced and unreduced totals in the same function is how the
  bug gets in. Keep `running` true and derive `r`.
- **`k` is guaranteed non-zero** by the constraints, so no division guard is needed,
  but check the constraints rather than assuming.

## 🎤 Interview talking points
- *"Two prefixes with the same remainder mod k differ by a multiple of k, so I count
  pairs sharing a remainder."* ← the whole solution in one sentence.
- *"It's the same code as Subarray Sum Equals K with the key changed from the prefix to
  the prefix mod k."* ← naming the reuse is what a senior answer sounds like.
- *"Space is O(k) rather than O(n), because remainders are the keys."*
- *"In Python the modulo of a negative is already non-negative; in C++ I'd normalise
  with `((r % k) + k) % k`."* ← the detail that separates memorised from understood.

## 🔗 Transfer
This is the first of the two *transform-then-ask-for-equality* episodes. Tomorrow
(EP42) does the same move with a different transform, rewrite every `0` as `−1` and
"equal numbers of 0s and 1s" becomes "two prefixes that are equal", but flips what the
map stores, because the question changes from **how many** to **how long**.

## 📹 Metadata
- **Title:** `Subarray Sums Divisible by K, same remainder, same lap | Prefix Sum #3`
- **Thumbnail:** `SAME REMAINDER` (green block)
- **Short:** the clock-face picture, then `[-1,2,9]` returning 1 in C++ and 2 in Python. 50s.
