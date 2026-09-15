# EP002 · P01E02 · Rearrange 0 and 1   [Easy]

**Pattern:** Two Pointers · **Link:** https://www.geeksforgeeks.org/problems/segregate-0s-and-1s5106/1

---

## 🎬 Hook
> "There's a cheat for this one — count the zeros, overwrite the array. It's O(n) and
> it passes. I'll show it, and then I'll show you why the interviewer asked for the
> *other* answer, the one that only reads each element once."

## 📋 Problem, in your words
```
You have an array containing only 0s and 1s, in any order.
Rearrange it in place so every 0 comes before every 1.

In place = O(1) extra space. You may not build a new array.
```

## 🔢 The example
```
Input:  [0, 1, 0, 1, 1, 1, 0]
Output: [0, 0, 0, 1, 1, 1, 1]
Why:    three 0s, four 1s — all zeros pushed to the front.
```

## 🧸 ELI5
> A line of people wearing black shirts and white shirts, all jumbled. You want all
> black at the front.
>
> One person starts at the front, one at the back. The front person walks right until
> they find a white shirt. The back person walks left until they find a black shirt.
> Those two swap places. Repeat until they meet in the middle.
>
> Nobody walks the line twice. Every step, one of the two fingers moves forward and
> never comes back.

## 🐌 Brute force (say it, don't type it)
Sort the array — **O(n log n)**. It works and it's one line, but sorting is
*enormous* overkill: you're paying a comparison sort to order a set with exactly two
distinct values. Say this on camera. "Using a sort here is like using a forklift to
pick up a pencil."

## 💡 The pattern reveal
**Signal:** "rearrange **in place**", only two distinct values, O(1) space required.
**Therefore:** Two Pointers, Shape A (swap from ends) — or Shape B (write pointer).

**Key insight:** a 0 on the right side and a 1 on the left side are *both* in the
wrong place. One swap fixes two problems at once. That's why a single pass is enough.

## 🔍 Dry run — `[0, 1, 0, 1, 1, 1, 0]`
| step | lo | hi | array | action |
|---|---|---|---|---|
| 1 | 0 | 6 | `[0,1,0,1,1,1,0]` | `arr[0]==0` → already fine, `lo += 1` |
| 2 | 1 | 6 | `[0,1,0,1,1,1,0]` | `arr[1]==1`, `arr[6]==0` → **swap** |
| 3 | 2 | 5 | `[0,0,0,1,1,1,1]` | `arr[2]==0` → fine, `lo += 1` |
| 4 | 3 | 5 | `[0,0,0,1,1,1,1]` | `arr[5]==1` → fine, `hi -= 1` |
| … | | | | pointers cross → done |

## ✅ Optimal solution
```python
class Solution:
    def segregate0and1(self, arr: List[int]) -> None:
        lo, hi = 0, len(arr) - 1

        while lo < hi:
            if arr[lo] == 0:            # already on the correct side
                lo += 1
            elif arr[hi] == 1:          # already on the correct side
                hi -= 1
            else:                       # arr[lo]==1 and arr[hi]==0 — both misplaced
                arr[lo], arr[hi] = arr[hi], arr[lo]
                lo += 1
                hi -= 1
```
**Time:** O(n), single pass · **Space:** O(1), true in-place

### The counting alternative — show it, then reject it
```python
zeros = arr.count(0)                    # pass 1
arr[:zeros] = [0] * zeros               # pass 2
arr[zeros:] = [1] * (len(arr) - zeros)
```
Also O(n) time, O(1) extra space. Perfectly valid! But it reads the array **twice**,
and it only works because there are exactly two values. The two-pointer version
generalises to EP9 (Dutch National Flag, three values) — the counting trick doesn't.
Saying *why* you prefer one correct answer over another correct answer is a senior
signal in an interview.

## ⚠️ Gotchas
- Move **both** pointers after a swap. Moving only one still terminates but wastes a
  comparison re-checking a slot you just fixed.
- `while lo < hi`, not `<=`. At `lo == hi` there's one element and nothing to swap.
- The `elif` matters: check `arr[lo] == 0` **first**. If you write two independent
  `if`s you can advance past an element you haven't placed.

## 🎤 Interview talking points
- *"Both misplaced elements get fixed by one swap, so the work is n/2 swaps at worst."*
- *"I'm choosing two pointers over counting because it extends to three or more
  buckets — that's the Dutch National Flag partition, which is also the core of
  quicksort's 3-way partition."*

## 🔗 Transfer
This is the **two-bucket** version of EP9 (Sort Colors / Dutch National Flag), which
is the three-bucket version. It's also literally the partition step inside quicksort —
worth naming on camera, because that connection is what makes it feel like real CS
rather than a puzzle.

## 📹 Metadata
- **Title:** `Segregate 0s and 1s — one pass, zero extra memory | Two Pointers #2`
- **Thumbnail:** `ONE SWAP, TWO FIXES` (blue block)
- **Short:** Beat 4 — the black/white shirt line.
