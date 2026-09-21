# EP026 · P03E06 · Longest Substring with Same Letters after Replacement   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/longest-repeating-character-replacement/

---

## 🎬 Hook
> "There's a variable in this solution that is sometimes *stale* — it holds a number
> that isn't true any more, and the standard solution never bothers to fix it. The
> answer still comes out right. Understanding why is the most interesting ten minutes
> in this entire pattern."

## 📋 Problem, in your words
```
Given a string of uppercase letters and a number k,
you may replace AT MOST k characters with any other letter.

Return the length of the longest substring that can be made
of all the SAME letter after those replacements.
```

## 🔢 The example
```
Input:  s = "AABABBA",  k = 1
Output: 4
Why:    take "AABA" and replace the B -> "AAAA". Length 4.
        (Or "ABBA" -> "BBBB". Also 4.)

Input:  s = "ABAB",  k = 2
Output: 4        (replace both Bs, or both As)
```

## 🧸 ELI5
> Look at any stretch of the word. Count the letter that appears **most** in it — those
> you keep. Everything else has to be painted over.
>
> So a stretch is affordable when **(its length) − (count of its most common letter)
> ≤ k**. That's how many paint jobs it needs.
>
> Walk right, growing the stretch. When it needs more paint than you have, slide the
> left edge up by one. Whatever the longest affordable stretch was, that's the answer.

## 🐌 Brute force (say it, don't type it)
Every substring; count its letter frequencies; check `length − maxFreq ≤ k`.
**O(n²) or O(n²·26).** The redundancy: neighbouring substrings have nearly identical
frequency tables.

## 💡 The pattern reveal
**Signal:** contiguous · longest · "change at most k things."
**Therefore:** Sliding Window, Shape B.

**Key insight #1 — the validity test.** You never need to know *which* letter you're
keeping. A window is affordable when:

```
(hi - lo + 1) - max_count  <=  k
 └─ window length ─┘   └ the most frequent letter in it ┘
```

**Key insight #2 — the famous one.** `max_count` is allowed to be **stale**. The usual
solution never recomputes it when the window shrinks, so it can hold a value larger
than any letter's actual count in the current window. And the answer is still correct.

**Why staleness is safe.** `best` is a running maximum, so it only ever records a
window when that window is *longer than anything seen so far*. A stale — that is,
too-large — `max_count` makes the window look **more** affordable than it is, so the
window can fail to shrink when it "should." But a window only grows by one per step,
and `best` only updates when the window strictly beats the record. To beat the record
with a too-large `max_count`, some letter would have to reach that count for real — at
which point `max_count` isn't stale any more.

Put plainly: **a stale `max_count` can hold the window steady, but it can never let it
grow past a genuine answer.** So the recorded maximum is always achievable.

This is why the window in the code below **never shrinks** — it slides. `if`, not
`while`. One element in, one element out, whenever it's unaffordable.

## 🔍 Dry run — `s = "AABABBA"`, k = 1
| hi | char | counts | max_count | len | len − max ≤ 1? | window | best |
|---|---|---|---|---|---|---|---|
| 0 | A | `{A:1}` | 1 | 1 | 0 ✓ | `A` | 1 |
| 1 | A | `{A:2}` | 2 | 2 | 0 ✓ | `AA` | 2 |
| 2 | B | `{A:2,B:1}` | 2 | 3 | 1 ✓ | `AAB` | 3 |
| 3 | A | `{A:3,B:1}` | 3 | 4 | 1 ✓ | `AABA` | **4** |
| 4 | B | `{A:3,B:2}` | 3 | 5 | 2 ✗ → slide | `ABAB` | 4 |
| 5 | B | `{A:2,B:3}` | 3 | 4 | 1 ✓ | `BABB` | 4 |
| 6 | A | `{A:2,B:3}` | 3 | 4 | 1 ✓ | `ABBA` | 4 |

Return **4**.

Now look at the last two rows. At `hi=6` the window is `ABBA`, where the true maximum
count is 2 (`A:2`, `B:2`) — but `max_count` is still **3**, left over from earlier. The
window looks affordable when honestly it isn't. It doesn't matter: the window length is
4, which merely ties the record and never exceeds it. The stale value bought nothing.
**Point at this row on camera — it's the proof, live.**

## ✅ Optimal solution
```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """Longest run that becomes uniform after at most k replacements.

        Time:  O(n) — one pass, no inner loop at all.
        Space: O(26) = O(1) — counts for uppercase letters.
        """
        counts: Dict[str, int] = defaultdict(int)
        lo = 0
        max_count = 0                       # deliberately never decreased

        for hi, char in enumerate(s):
            counts[char] += 1
            max_count = max(max_count, counts[char])

            # Unaffordable: slide the window right by one. Note `if`, not `while` --
            # the window never shrinks, it only ever stops growing.
            if (hi - lo + 1) - max_count > k:
                counts[s[lo]] -= 1
                lo += 1

        return len(s) - lo                  # the window's final (maximal) size
```
**Time:** O(n) · **Space:** O(1)

### Two things about that code
**`return len(s) - lo`, not a tracked `best`.** Because the window never shrinks, its
size is monotonically non-decreasing — so its *final* size is its maximum. Tracking
`best = max(best, hi - lo + 1)` inside the loop is equally correct and easier to read;
use it if the trick makes you uneasy. Say both on camera.

**The honest version, if staleness bothers you:**
```python
while (hi - lo + 1) - max(counts.values()) > k:    # recompute properly
    counts[s[lo]] -= 1; lo += 1
best = max(best, hi - lo + 1)
```
This is **O(26n)** — still linear, since the alphabet is fixed — and obviously correct
with no cleverness to defend. An interviewer who asks "are you sure that's right?"
will be happier with this plus an explanation than with the stale version plus a
shrug.

## ⚠️ Gotchas
- **`if`, not `while`.** This is Shape B's one exception, and it works only because we
  never need the window to shrink — only to stop growing. Writing `while` here isn't
  wrong (it still returns the right answer with a tracked `best`), but it obscures the
  invariant.
- **Don't "fix" `max_count` on shrink.** Recomputing it is correct but costs O(26) per
  step; *decrementing* it is plain wrong, because the departing character may not be
  the maximal one.
- **`(hi - lo + 1) - max_count`** is the replacement count. Getting this expression
  backwards (`max_count - length`) is a silent sign error.
- Uppercase only per the constraints, so O(26) space. If the alphabet were unbounded,
  the honest `max(counts.values())` version becomes O(n·k) and you'd want a different
  structure.
- `k = 0` reduces to "longest run of a single repeated character," and the same code
  handles it.
- `k >= len(s)` returns `len(s)`. Check it.

## 🎤 Interview talking points
- *"A window is valid when its length minus its most-frequent-letter count is at most
  k — I never need to know which letter wins."*
- *"`max_count` is never decreased. That's safe because the answer is a running
  maximum: a stale max can only keep the window from shrinking, and the window can't
  exceed a real answer without some letter actually reaching that count."* ← if you can
  say this cleanly you are, on this problem, ahead of most candidates.
- *"If I wanted no cleverness to defend, recomputing `max(counts.values())` is O(26)
  per step — still linear overall."*

## 🔗 Transfer
EP27 (Longest Subarray with Ones after Replacement) is **this problem with a
two-letter alphabet**: `max_count` becomes "count of ones," and the whole staleness
discussion evaporates because you can just count zeros directly. Do today's hard
version first and tomorrow is a relief — that ordering is deliberate.

## 📹 Metadata
- **Title:** `Longest Repeating Character Replacement — the stale variable that still works | Sliding Window #6`
- **Thumbnail:** `WRONG, BUT NOT WRONG` (amber block)
- **Short:** The `hi=6` row where max_count is 3 and the truth is 2 — and why it doesn't matter. 60s.
