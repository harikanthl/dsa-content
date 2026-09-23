# EP042 · P05E04 · Contiguous Array   [Medium]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/contiguous-array/

---

## 🎬 Hook
> "Longest subarray with the same number of 0s and 1s. There is no sum in this question
> at all, until you rewrite every `0` as `−1`. Then 'equally many' becomes 'sums to
> zero', which becomes 'two running totals that are **equal**', and you're back in
> Pattern 05. One line of transformation turns a counting problem into yesterday's
> problem."

## 📋 Problem, in your words
```
Given a binary array nums (only 0s and 1s), return the LENGTH of the
longest contiguous subarray containing an equal number of 0s and 1s.

Length, not the subarray. Return 0 if there is none.
```

## 🔢 The example
```
Input:  nums = [0, 1]
Output: 2

Input:  nums = [0, 1, 0]
Output: 2            <- [0,1] or [1,0]; both length 2, the whole array is unbalanced

Input:  nums = [0, 1, 0, 0, 1, 1, 0]
Output: 6            <- indices 0..5: three 0s, three 1s. Index 6 is left out.
```
The third one is the dry run. Note the answer is *not* the whole array and *not*
anchored at index 0 by luck, it genuinely needs the map.

## 🧸 ELI5
> Score the walk like a tug-of-war: a `1` pulls you **up** one step, a `0` pulls you
> **down** one step.
>
> ```
> nums:      0    1    0    0    1    1    0
> step:     -1   +1   -1   -1   +1   +1   -1
> height: 0 -1    0   -1   -2   -1    0   -1
>         ^
>         before the walk starts
> ```
>
> A stretch is **balanced** exactly when it ends at the same height it started, the ups
> cancelled the downs. So:
>
> > *"Find the longest stretch between two moments at the **same height**."*
>
> Which means: the first time you reach a height, **write down where you were**. Every
> later visit to that height measures a balanced stretch, and because you wrote down the
> *first* visit, it's the longest one ending there.

## 🐌 Brute force (say it, don't type it)
Every start, every end, count 0s and 1s (or keep a running balance), take the longest
where they match. **O(n²)**. The O(n) version is the same running balance with the inner
loop replaced by a dictionary, identical move to EP39.

## 💡 The pattern reveal
**Signal:** longest subarray · a **balance** condition · binary values.
**Therefore:** map `0 → −1`, then find the longest span between equal prefix sums.

**Key insight:** two transformations stacked, and both are worth naming out loud.

```
1.  0 -> -1          "equal counts"  becomes  "sums to zero"
2.  prefix sums      "sums to zero"  becomes  "two prefixes are EQUAL"
```

After that it is a dictionary lookup, as always.

**🧨 The trap of the episode: store the FIRST index and never overwrite it.** EP39 and
EP41 counted subarrays, so the map value was a count. Here the question is *how long*,
so the map value is a **position**: and it must be the earliest one:

| question | map value | on seeing a key again |
|---|---|---|
| how **many** (EP39, EP41) | a count | `+= 1` |
| how **long** (EP42) | the **first** index | **leave it alone**, just measure |

Overwrite it and you measure from the most recent visit instead of the earliest: still a
balanced subarray, just not the longest. A wrong answer with no crash and no obvious
symptom. On `[0, 1, 0, 0, 1, 1, 0]` overwriting returns **4** instead of 6.

**And the seed is `{0: -1}`, not `{0: 0}`.** Height `0` happens *before* index 0, so its
position is `−1`. That makes the length arithmetic `i − first[h]` come out right for a
subarray starting at the beginning: on `[0, 1]`, `i = 1` gives `1 − (−1) = 2` ✓. Seed it
with `0` and every such answer is one short.

## 🔍 Dry run: `nums = [0, 1, 0, 0, 1, 1, 0]`
Start: `first = {0: -1}`, `running = 0`, `best = 0`.

| i | x | step | `running` | in map? | length `i − first[r]` | `best` | `first` after |
|---|---|---|---|---|---|---|---|
| 0 | 0 | −1 | −1 | no | - | 0 | `{0:−1, −1:0}` |
| 1 | 1 | +1 | 0 | **yes, at −1** | 1 − (−1) = **2** | **2** | unchanged |
| 2 | 0 | −1 | −1 | **yes, at 0** | 2 − 0 = **2** | 2 | unchanged |
| 3 | 0 | −1 | −2 | no | - | 2 | `+ −2:3` |
| 4 | 1 | +1 | −1 | **yes, at 0** | 4 − 0 = **4** | **4** | unchanged |
| 5 | 1 | +1 | 0 | **yes, at −1** | 5 − (−1) = **6** | **6** | unchanged |
| 6 | 0 | −1 | −1 | **yes, at 0** | 6 − 0 = **6** | 6 | unchanged |

Answer **6** ✓, indices 0..5, which is `[0,1,0,0,1,1]`: three of each.

The row that proves the rule is **`i = 4`**. Height `−1` was first reached at index 0
and reached again at index 2. If index 2 had overwritten the stored index, this row
would measure `4 − 2 = 2`, and row 6 would measure `6 − 4 = 2`, the final answer would
be 4. Keeping the *earliest* index is what makes it 6.

And **`i = 5`** is the one that needs the `−1` seed: it pairs with the empty prefix to
give the subarray starting at index 0.

## ✅ Optimal solution
```python
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        """Longest subarray with equally many 0s and 1s.

        Time:  O(n), one pass.
        Space: O(n), at most n+1 distinct running balances.
        """
        first = {0: -1}                # balance 0 occurs BEFORE index 0
        running = best = 0

        for i, x in enumerate(nums):
            running += 1 if x == 1 else -1     # 0 counts as -1

            if running in first:
                best = max(best, i - first[running])   # measure, don't store
            else:
                first[running] = i                     # first sighting only

            # note: no `else` branch that updates an existing key. That is the point.

        return best
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **Never overwrite an existing key.** The `if/else` above is load-bearing. A plain
  `first[running] = i` at the end of every iteration silently shortens the answer.
- **Seed `{0: -1}`.** Position `−1` for the empty prefix, so `i − (−1)` counts the
  element at index 0. `[0, 1]` → 2 is the test; seeding `{0: 0}` gives 1.
- **`best` is a length, not an index.** Return the max span, and return `0`, not −1,
  when nothing balances. `[0, 0, 0]` → **0**.
- **The answer's length is always even.** Useful sanity check on camera: an odd answer
  means the arithmetic is off by one somewhere.
- **`1 if x == 1 else -1`, not `x if x else -1`** if the array might ever hold other
  values. It won't here, but read the constraints rather than assume binary.
- **This does not need the sum to be zero at the end.** The whole array being unbalanced
  is normal; you're looking for the longest *interior* balanced stretch.

## 🎤 Interview talking points
- *"Rewrite 0 as −1 and 'equal counts' becomes 'sum zero', which is 'two prefix sums
  that are equal', then it's a hash map."* ← the whole answer in one breath.
- *"Because I want the longest, the map stores the first index each balance was seen at,
  and I never overwrite it."* ← say this before they ask; it's the follow-up question.
- *"I seed with balance 0 at index −1, so subarrays starting at the beginning measure
  correctly."*
- *"Same three lines as Subarray Sum Equals K, what changed is the transform on the
  way in and what the map stores on the way out."*

## 🔗 Transfer
This closes the "hash map" half of Pattern 05. Every episode so far asked an **equality**
question, equal to `running − k`, equal remainder, equal balance, because that's all a
dictionary can answer. Tomorrow (EP43) asks a **range** question instead: *is there an
earlier prefix at most `running − k`?* A dict cannot do that, and the structure that
replaces it is a monotonic deque.

## 📹 Metadata
- **Title:** `Contiguous Array, rewrite 0 as −1 and it's a prefix sum | Prefix Sum #4`
- **Thumbnail:** `0 → −1` (green block)
- **Short:** the tug-of-war height graph, then overwriting the index and watching 6 become 4. 50s.
