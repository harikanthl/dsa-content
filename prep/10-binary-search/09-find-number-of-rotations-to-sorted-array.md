# EP079 · P10E09 · Find the Number of Rotations (Kth Rotation)   [Easy]

**Pattern:** Binary Search · **Link:** https://www.geeksforgeeks.org/problems/rotation4723/1

---

## 🎬 Hook
> "How many times was this sorted array rotated? You already solved it yesterday, you
> just returned the wrong thing. The minimum's **index** is the rotation count. This
> episode is thirty seconds of code and five minutes on why that's true, because
> recognising a problem you've already solved is a skill interviewers test on purpose."

## 📋 Problem, in your words
```
A sorted array of DISTINCT numbers was rotated to the RIGHT k times:
[2, 3, 6, 12, 15, 18] rotated 2 times -> [15, 18, 2, 3, 6, 12].

Given the rotated array, return k.
Expected O(log n).
```

## 🔢 The example
```
Input:  arr = [15, 18, 2, 3, 6, 12]
Output: 2

Input:  arr = [5, 1, 2, 3, 4]
Output: 1

Input:  arr = [1, 2, 3, 4, 5]
Output: 0              <- never rotated
```

## 🧸 ELI5
> A line of kids sorted by height. Each "rotation" takes the kid at the **back** and
> moves them to the **front**. After k rotations, k tall kids are standing at the
> front, and the shortest kid has been pushed back by exactly k places.
>
> ```
> original:        2   3   6   12   15   18     shortest at index 0
> rotate once:    18   2   3    6   12   15     shortest at index 1
> rotate twice:   15  18   2    3    6   12     shortest at index 2
> ```
>
> So: **where is the shortest kid standing?** That number is k.

## 🐌 Brute force (say it, don't type it)
`arr.index(min(arr))`: **O(n)**. Correct, and it's the right idea already. The only
upgrade is finding that index in O(log n), which is EP78.

## 💡 The pattern reveal
**Signal:** "rotated sorted array" · "how many rotations".
**Therefore:** Shape B, EP78 returning `lo` instead of `nums[lo]`.

**Key insight:** each right rotation moves the smallest element one step right. It
started at index 0, so after k rotations it's at index k. The rotation count **is** the
minimum's index. One-line proof, zero new code.

| | EP78 | EP79 |
|---|---|---|
| predicate | `arr[mid] > arr[hi]` | same |
| branches | `lo = mid + 1` / `hi = mid` | same |
| return | `arr[lo]` (the value) | **`lo`** (the index) |

**Left rotations?** If the problem rotated left instead, the minimum ends up at
`(n - k) % n`, so `k = (n - lo) % n`. Ask which direction before you answer.

## 🔍 Dry run: `arr = [15, 18, 2, 3, 6, 12]`

| step | lo | hi | mid | arr[mid] | arr[hi] | mid > hi? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 2 | 12 | no | `hi = 2` |
| 2 | 0 | 2 | 1 | 18 | 2 | yes | `lo = 2` |
| 3 | 2 | 2 | - | | | | return **2** ✓ |

Step 1 landed on the minimum immediately and still didn't stop. Step 2 checked the one
thing left of it that could've been smaller, found it was in the high part, and closed
the range.

## ✅ Optimal solution
```python
def find_k_rotation(arr: list[int]) -> int:
    """How many times a sorted array of distinct values was rotated right.

    The minimum started at index 0 and moves one step right per rotation,
    so its current index is the rotation count.

    Time:  O(log n), EP78's search.
    Space: O(1).
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] > arr[hi]:
            lo = mid + 1            # mid is in the rotated-up part; the minimum is right of it
        else:
            hi = mid                # mid is in the low part; the minimum is mid or left of it
    return lo                       # index of the minimum == rotation count
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **Return the index.** Returning `arr[lo]` is EP78's answer and gives 2 for the
  example by coincidence, since the minimum happens to be 2 and so does k. Try
  `[5, 1, 2, 3, 4]`: value 1, count 1. Coincidence again! Try `[30, 40, 10, 20]`:
  value 10, count 2. Always test with values that aren't small integers.
- **Rotations are modulo n.** Rotating 6 times a 6-element array gives 0. The index
  can only be `0..n-1`, so the answer is naturally `k % n`.
- **Right vs left rotation** changes the formula. Confirm the direction.
- **Duplicates** make it O(n) worst case, same as EP78. The GfG version guarantees
  distinct values.

## 🎤 Interview talking points
- *"Each right rotation shifts the minimum one place right, so the rotation count is
  the minimum's index."*
- *"That makes it Find Minimum in Rotated Sorted Array, returning the index instead of
  the value."* ← naming the reuse is the point of the episode.
- *"If they meant left rotations, it's `(n - index) % n`."*

## 🔗 Transfer
EP78 and EP79 find the break point. Tomorrow's EP80, Search in Rotated Sorted Array,
doesn't care where the break is. It searches for a target directly, by asking at each
step "which half of me is sorted?" and range-checking the target against that half.
(You *could* find the break with EP79 and then binary search the correct side: two
searches, also O(log n), and a perfectly good answer to mention.)

## 📹 Metadata
- **Title:** `Number of rotations, you solved this yesterday | Binary Search #9`
- **Thumbnail:** `index = k` (blue block)
- **Short:** the kids-in-a-line rotation, shortest kid shifting right each time. 30s.
