# EP073 · P10E03 · Find First and Last Position of Element in Sorted Array   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

---

## 🎬 Hook
> "The popular answer: binary search until you find the target, then walk left and
> right to find the edges. It looks like O(log n). Now run it on an array of a million
> 8s. You just wrote a linear scan with extra steps. The real answer is **two binary
> searches**, and the second one searches for a number that might not even be in the
> array."

## 📋 Problem, in your words
```
Given a sorted array (duplicates allowed) and a target,
return [first index of target, last index of target].

  - if target isn't present, return [-1, -1]
  - must be O(log n)
```

## 🔢 The example
```
Input:  nums = [5, 7, 7, 8, 8, 10], target = 8
Output: [3, 4]

Input:  nums = [5, 7, 7, 8, 8, 10], target = 6
Output: [-1, -1]

Input:  nums = [], target = 0
Output: [-1, -1]
```

## 🧸 ELI5
> Kids are lined up by age. You want the block of 8-year-olds. Ask two questions:
>
> 1. "Where does the first kid who is **at least 8** stand?" → the start of the block.
> 2. "Where does the first kid who is **at least 9** stand?" → one past the end of it.
>
> ```
> nums:     5   7   7   8   8   10
> index:    0   1   2   3   4   5
>                       ^           first >= 8  -> 3
>                               ^   first >= 9  -> 5
> block of 8s: [3, 5 - 1] = [3, 4]
> ```
>
> Nobody is 9. Doesn't matter. The question "where would a 9 stand?" still has an answer.

## 🐌 Brute force (say it, don't type it)
Scan once, record the first and last time you see the target: **O(n)**. The tempting
"improvement", binary search once and then expand outwards, is still **O(n)** in the
worst case: if all n elements equal the target, the expansion walks all of them. Say
this unprompted. It's the trap the problem is built around.

## 💡 The pattern reveal
**Signal:** "sorted" · "first and last" · "O(log n)".
**Therefore:** Shape A, two calls.

**Key insight:** first = `lower_bound(target)`. last = `lower_bound(target + 1) - 1`.
The second search looks for where `target + 1` **would** go, and it doesn't care
whether `target + 1` exists. That's why a template that returns an insertion position,
not a found/not-found boolean, is the one to learn.

| call | question | on the example |
|---|---|---|
| `lower_bound(8)` | first index with value `>= 8` | 3 |
| `lower_bound(9)` | first index with value `>= 9` (i.e. `> 8`) | 5 |
| last = `5 - 1` | the element just before | 4 |

One check decides "not present": the first call lands on something that isn't the
target (or on `n`). If the first call finds it, the second call is guaranteed to find a
valid last position, so it needs no check of its own.

## 🔍 Dry run: `nums = [5, 7, 7, 8, 8, 10]`, `target = 8`

**Call 1: `lower_bound(8)`**

| step | lo | hi | mid | nums[mid] | compare | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | 8 >= 8 | `hi = 3` |
| 2 | 0 | 3 | 1 | 7 | 7 < 8 | `lo = 2` |
| 3 | 2 | 3 | 2 | 7 | 7 < 8 | `lo = 3` |
| 4 | 3 | 3 | - | - | stop | first = **3**, `nums[3] == 8` ✓ |

Step 1 hit an 8 at index 3 and **kept going left**. It happened to be the first 8
already, but the search doesn't know that; it has to prove nothing to the left is 8.

**Call 2: `lower_bound(9)`**

| step | lo | hi | mid | nums[mid] | compare | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | 8 < 9 | `lo = 4` |
| 2 | 4 | 6 | 5 | 10 | 10 >= 9 | `hi = 5` |
| 3 | 4 | 5 | 4 | 8 | 8 < 9 | `lo = 5` |
| 4 | 5 | 5 | - | - | stop | 5 → last = 5 - 1 = **4** |

Answer **`[3, 4]`** ✓. Six comparisons total, no matter how many 8s there are.

## ✅ Optimal solution
```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """[first, last] index of target in a sorted array, or [-1, -1].

        Time:  O(log n), two independent lower_bound calls.
        Space: O(1).
        """
        def lower_bound(x: int) -> int:
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo                   # first index with nums[i] >= x

        first = lower_bound(target)
        if first == len(nums) or nums[first] != target:
            return [-1, -1]             # target absent: nothing to bracket

        last = lower_bound(target + 1) - 1   # one before the first value > target
        return [first, last]
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **Find-then-expand is O(n).** An array of all 8s makes the expansion linear. It's the
  most common wrong answer to this problem and interviewers wait for it.
- **Check `first == len(nums)` before `nums[first]`.** Target bigger than everything
  (`target = 11`) or an empty array makes `first = n`.
- **`target + 1` does not need to exist.** The template returns where it *would* go.
  If you wrote a boolean "found" binary search, you can't do this, and that's why the
  template returns positions.
- **No second presence check.** If `first` is valid, `lower_bound(target + 1) - 1` is
  at least `first`. Adding a check there is harmless but shows you haven't reasoned
  about it.
- **The alternative, one function with a `bias` flag** (search left vs right) is also
  accepted. It's more code and more ways to be off by one. Two calls to one template
  is cleaner.

## 🎤 Interview talking points
- *"First is lower bound of the target. Last is lower bound of target plus one, minus
  one. Two searches, O(log n) regardless of duplicates."*
- *"I'm avoiding find-then-expand because it degrades to O(n) when everything equals
  the target."* ← say this before they ask.
- *"The second search looks for a value that may not exist; lower bound still returns
  where it would be inserted."*
- *"If the first search doesn't land on the target, it's absent and I return early."*

## 🔗 Transfer
The gap between those two searches is a count: `last - first + 1`, or directly
`lower_bound(x + 1) - lower_bound(x)`. That subtraction is all of tomorrow's EP74. The
"search for a value that may not exist" idea comes back hard in EP91 and EP92, where
you binary search over **values** and the answer must be proven to be one that exists.

## 📹 Metadata
- **Title:** `First and Last Position, why find-then-expand is O(n) | Binary Search #3`
- **Thumbnail:** `search for 9` (blue block)
- **Short:** a row of eight 8s, the expand version walking all of them vs two searches. 45s.
