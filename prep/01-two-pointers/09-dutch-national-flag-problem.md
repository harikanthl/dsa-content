# EP009 · P01E09 · Dutch National Flag Problem (Sort Colors)   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/sort-colors/

---

## 🎬 Hook
> "There is exactly one line in this algorithm that everyone gets wrong, and it's a
> line that *isn't there*. After one of the two swaps you must NOT advance the middle
> pointer — and if you can explain why, you understand this problem completely."

## 📋 Problem, in your words
```
An array containing only 0s, 1s and 2s (red, white, blue).
Sort it in place, in ONE pass, using O(1) extra space.

No sorting library. No counting pass. One traversal.
```

## 🔢 The example
```
Input:  [2, 0, 2, 1, 1, 0]
Output: [0, 0, 1, 1, 2, 2]
```

## 🧸 ELI5
> You're sorting a pile of red, white and blue socks into three regions of a table:
> reds on the left, blues on the right, whites in the middle.
>
> You have three markers:
> - **`low`** — the line where the red region ends
> - **`high`** — the line where the blue region begins
> - **`mid`** — the sock you're currently looking at
>
> Pick up the sock at `mid`:
> - **Red?** Throw it left across the `low` line. Advance both `low` and `mid`.
> - **White?** It's already in the right region. Just move `mid` along.
> - **Blue?** Throw it right across the `high` line. Pull `high` in. **But do not
>   move `mid`** — because whatever came back from the right side is a sock you have
>   never looked at. You have to inspect it.
>
> That last bullet is the whole problem.

## 🐌 Brute force (say it, don't type it)
1. `nums.sort()` — O(n log n), and the problem bans it.
2. **Counting sort**: count the 0s, 1s, 2s, then overwrite. O(n) time, O(1) space —
   genuinely correct! But it's **two passes**, and the problem explicitly asks for
   one. Show it on camera, then say: "this passes, but the follow-up is always
   'can you do it in one pass?', and that's the real question."

## 💡 The pattern reveal
**Signal:** exactly three distinct values + in place + one pass + O(1) space.
**Therefore:** Two Pointers, Shape C — **three-way partition** (Dijkstra's Dutch
National Flag).

**Key insight — the invariant.** At every moment:
```
[0 .. low-1]      all 0s      (finished)
[low .. mid-1]    all 1s      (finished)
[mid .. high]     UNKNOWN     (still to inspect)
[high+1 .. n-1]   all 2s      (finished)
```
The unknown region shrinks by one every iteration, so the loop terminates in ≤ n
steps. Draw this on screen. **Every decision in the code falls out of maintaining it.**

## 🔍 Dry run — `[2, 0, 2, 1, 1, 0]`
| low | mid | high | array | nums[mid] | action |
|---|---|---|---|---|---|
| 0 | 0 | 5 | `[2,0,2,1,1,0]` | 2 | swap mid↔high, `high=4`, **mid stays** |
| 0 | 0 | 4 | `[0,0,2,1,1,2]` | 0 | swap mid↔low, `low=1`, `mid=1` |
| 1 | 1 | 4 | `[0,0,2,1,1,2]` | 0 | swap mid↔low, `low=2`, `mid=2` |
| 2 | 2 | 4 | `[0,0,2,1,1,2]` | 2 | swap mid↔high, `high=3`, **mid stays** |
| 2 | 2 | 3 | `[0,0,1,1,2,2]` | 1 | `mid=3` |
| 2 | 3 | 3 | `[0,0,1,1,2,2]` | 1 | `mid=4` |
| | 4 | 3 | | | `mid > high` → done |

Result `[0,0,1,1,2,2]` ✓

**Look at row 1.** We swapped a `2` out and a `0` in. If `mid` had advanced, that `0`
would be stranded in the middle region forever and the output would be wrong. That is
the bug. Pause the video here.

## ✅ Optimal solution
```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1                      # safe: swapped-in value is a known 1
            elif nums[mid] == 1:
                mid += 1                      # already in place
            else:                             # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
                # mid does NOT advance — nums[mid] is now unexamined
```
**Time:** O(n), one pass · **Space:** O(1)

### Why `mid += 1` is safe in the 0-branch but not the 2-branch
In the 0-branch, you swap with `nums[low]`. But `low ≤ mid`, and everything in
`[low, mid)` is already known to be a **1**. So the value swapped into `mid` is a 1 —
already correct, nothing to inspect. In the 2-branch you swap with `nums[high]`, which
is in the **unknown** region. You've learned nothing about it. You must look again.

This asymmetry is the single best thing in the episode. It's a 60-second Short by itself.

## ⚠️ Gotchas
- **`while mid <= high`, not `<`.** At `mid == high` there's one unclassified element
  left, and it still needs placing.
- Don't advance `mid` after the 2-swap. (Said three times because it's that common.)
- Don't advance `high` past a value you've placed — `high -= 1` happens once per swap.
- Python's tuple swap `a, b = b, a` is safe here; in C/Java you'd need a temp. Worth a
  passing mention if you ever re-record in another language.

## 🎤 Interview talking points
- *"I'm maintaining a four-region invariant; the unknown region shrinks every step,
  so it's one pass."*
- *"This is Dijkstra's Dutch National Flag problem, and it's the same three-way
  partition used in quicksort to handle arrays with many duplicate keys."*
  ← Naming the connection to quicksort is a genuine senior signal.
- *"Counting sort also works in O(n)/O(1), but takes two passes. This is the one-pass
  version."*

## 🔗 Transfer
Three-way partitioning is the core of **quickselect** (Kth Largest, EP 95) and of
quicksort on duplicate-heavy data. EP2 was the two-bucket version of this. If someone
asks you to partition into *k* buckets in one pass, this is the shape you generalise.

## 📹 Metadata
- **Title:** `Sort Colors — the ONE line everybody gets wrong | Dutch National Flag`
- **Thumbnail:** `DON'T MOVE MID` (blue block)
- **Short:** Why `mid` advances after one swap and not the other. High replay value.
