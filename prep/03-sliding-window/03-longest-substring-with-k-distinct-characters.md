# EP023 · P03E03 · Longest Substring with K Distinct Characters   [Medium]

**Pattern:** Sliding Window · **Link:** https://www.geeksforgeeks.org/problems/longest-k-unique-characters-substring0853/1

---

## 🎬 Hook
> "Yesterday we wanted the *smallest* window. Today we want the *largest* — and
> flipping that one word flips two lines of the algorithm. Get them the wrong way
> round and you'll write code that runs, returns a number, and is quietly wrong."

## 📋 Problem, in your words
```
Given a string and a number k,
find the length of the LONGEST substring containing at most k DISTINCT characters.

"at most k distinct" counts unique letters, not total letters:
"aaab" has 2 distinct characters and length 4.
```

## 🔢 The example
```
Input:  s = "araaci",  k = 2
Output: 4
Why:    "araa" uses only {a, r} -- 2 distinct, length 4.

Input:  s = "araaci",  k = 1
Output: 2        ("aa")

Input:  s = "cbbebi",  k = 3
Output: 5        ("cbbeb" uses {c,b,e}; so does "bbebi")
```

## 🧸 ELI5
> You're collecting letters into a bag as you walk along the word, and the bag can
> only hold **k different kinds** — any number of each kind, but only k kinds.
>
> Keep walking right, dropping letters in. The moment you'd have a (k+1)th kind, start
> throwing away letters from the **left end** — one at a time — until one whole kind is
> gone from the bag. Now you're legal again, so measure how far you've walked.
>
> The subtle bit: throwing away one `a` doesn't remove the *kind* `a` if there are
> more `a`s still in the bag. You only lose a kind when its count hits zero.

## 🐌 Brute force (say it, don't type it)
Every start, extend right, track distinct characters with a set, stop when it exceeds
k.

**O(n²) time** (O(n²·k) if you rebuild the set each time). Same waste as always: each
new start throws away a window that was one element away from the last one.

## 💡 The pattern reveal
**Signal:** contiguous · **longest** · "at most k <something>".
**Therefore:** Sliding Window, Shape B — the growing window.

**Key insight:** keep a `char → count` dictionary for the window. Then
**`len(counts)` is the number of distinct characters** — an O(1) read, no scanning.
That one observation converts a set-rebuilding O(n²·k) solution into O(n).

**The Shape B rules — the exact mirror of yesterday:**

| | EP22 (shortest) | Today (longest) |
|---|---|---|
| shrink `while` | `while valid` | **`while NOT valid`** |
| record the answer | inside the loop | **after the loop** |

Why: for a *longest* answer, a window that's still valid might get even better — so
you never measure it early. You only shrink to repair a break, and once repaired, the
window is the best one ending at `hi`. **Measure after repair.**

## 🔍 Dry run — `s = "araaci"`, k = 2
| hi | char | counts | distinct | action | window | best |
|---|---|---|---|---|---|---|
| 0 | a | `{a:1}` | 1 | ok | `a` | 1 |
| 1 | r | `{a:1,r:1}` | 2 | ok | `ar` | 2 |
| 2 | a | `{a:2,r:1}` | 2 | ok | `ara` | 3 |
| 3 | a | `{a:3,r:1}` | 2 | ok | `araa` | **4** |
| 4 | c | `{a:3,r:1,c:1}` | 3 ✗ | drop `a`→`{a:2,r:1,c:1}` still 3 ✗; drop `r`→`{a:2,c:1}` ✓ | `aac` | 4 |
| 5 | i | `{a:2,c:1,i:1}` | 3 ✗ | drop `a`→ still 3 ✗; drop `a`→`{c:1,i:1}` ✓ | `ci` | 4 |

Return **4**. Look at `hi=4`: dropping the first `a` did **not** reduce the distinct
count, because two more `a`s remained. The kind only disappears when its count reaches
zero — that's the `del` in the code, and it's the bug people ship.

## ✅ Optimal solution
```python
class Solution:
    def longestKSubstr(self, s: str, k: int) -> int:
        """Longest substring with at most k distinct characters.

        Time:  O(n) amortised — lo only moves forward.
        Space: O(k) — the counter holds at most k+1 keys at any moment.
        """
        if k == 0:
            return 0

        counts: Dict[str, int] = defaultdict(int)
        lo = 0
        best = 0

        for hi, char in enumerate(s):
            counts[char] += 1                   # grow right, always

            while len(counts) > k:              # shrink only while BROKEN
                left = s[lo]
                counts[left] -= 1
                if counts[left] == 0:
                    del counts[left]            # the kind is gone only at zero
                lo += 1

            best = max(best, hi - lo + 1)       # measure AFTER repair

        return best
```
**Time:** O(n) · **Space:** O(k)

### Why `del` and not just leaving a zero
`len(counts)` is the distinct-character test. A key sitting at count `0` still counts
toward `len`, so leaving it makes the window look invalid forever and `lo` marches to
the end — you'd return 1 or 0 on everything. Either `del` the key, or track
`distinct` as a separate integer you decrement. **Do not** write
`len([c for c in counts if counts[c] > 0])`; that's O(k) per step and throws away the
whole reason for the dictionary.

## ⚠️ Gotchas
- **`del` the key at zero** (above). The single most common bug on this problem.
- **`while`, not `if`.** One removal may not drop a kind — `hi=4` in the trace needed
  two. An `if` leaves an invalid window and inflates the answer.
- **Measure after the while loop, not inside it.** Inside, you'd be measuring windows
  that are still broken.
- **`k = 0`** should return 0. Without the guard, the while loop can't ever be
  satisfied — `len(counts) > 0` is true as soon as anything is added — and `lo` runs
  past `hi`, giving a negative length. Trace it on camera.
- **"at most k", not "exactly k".** If a variant says *exactly*, the answer is
  `atMost(k) - atMost(k-1)` — a genuinely useful trick, worth mentioning here because
  it comes back in counting problems.
- `defaultdict(int)` avoids a `KeyError` on first touch; plain `dict` needs
  `counts.get(char, 0) + 1`.

## 🎤 Interview talking points
- *"I keep a frequency map of the window, so the distinct count is just `len(map)` —
  O(1) per step instead of rescanning."*
- *"For a longest-window problem I shrink only while the window is invalid and record
  after; for a shortest one I shrink while it's valid and record before. Same skeleton,
  mirrored."*
- *"Space is O(k), not O(n), because the map never holds more than k+1 keys."*
- *"If it asked for exactly k, I'd compute at-most-k minus at-most-(k−1)."*

## 🔗 Transfer
EP24 (Fruits into Baskets) is **this exact problem with k hard-coded to 2** and a story
about fruit wrapped round it — the episode is about recognising that. EP25 (No-repeat
Substring) is the same shape where the condition is "no duplicates at all." EP26 and
EP27 keep the shape and make the validity test cleverer. Five episodes, one skeleton.

## 📹 Metadata
- **Title:** `Longest Substring with K Distinct — the len(dict) trick | Sliding Window #3`
- **Thumbnail:** `COUNT KINDS, NOT LETTERS` (amber block)
- **Short:** The `hi=4` step where dropping an `a` doesn't drop the kind `a`, 45s.
