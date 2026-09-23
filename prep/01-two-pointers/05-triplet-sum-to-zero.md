# EP005 · P01E05 · Triplet Sum to Zero (3Sum)   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/3sum/

---

## 🎬 Hook
> "3Sum is just Two Sum with a for-loop wrapped around it. That part takes ninety
> seconds. The reason it's rated Medium is the duplicates, and that's where I'm
> going to spend most of this video, because that's where everybody loses the offer."

## 📋 Problem, in your words
```
Given an array of integers, find every UNIQUE triplet [a, b, c] where a + b + c == 0.

Unique = the answer list must not contain the same triplet twice,
         even if different index combinations produce it.
The array is NOT sorted. It can contain duplicates.
```

## 🔢 The example
```
Input:  [-1, 0, 1, 2, -1, -4]
Sorted: [-4, -1, -1, 0, 1, 2]
Output: [[-1, -1, 2], [-1, 0, 1]]

Note: [-1, 0, 1] can be formed from index (1,3,4) AND index (2,3,4), two different
index sets, same triplet. We report it ONCE. That's the whole difficulty.
```

## 🧸 ELI5
> You want three numbers that cancel out to zero, like three people settling a debt
> so nobody owes anything.
>
> Sort everyone by how much they owe (most-owed to most-owing). Now **pick one person
> and freeze them**. Say they owe −4. That means the other two must add to exactly +4.
> And "find two numbers adding to a target in a sorted list" is *yesterday's problem*.
>
> So: freeze person 1, run the bookshelf two-finger trick on everyone to their right.
> Unfreeze, freeze the next person, repeat.
>
> The duplicate rule: if the next person you'd freeze owes *exactly the same* as the
> one you just did, skip them, you'd find the identical set of settlements again.

## 🐌 Brute force (say it, don't type it)
Three nested loops, **O(n³)**, plus a set to de-duplicate. For n = 3000 that's 27
billion operations. It times out. And the de-dup set is a patch over the real problem
rather than a fix.

## 💡 The pattern reveal
**Signal:** find a *triplet* summing to a target.
**Therefore:** sort, then **fix one + two pointers**: the standard kSum reduction.

**Key insight:** k-Sum reduces to (k−1)-Sum by fixing one element. 3Sum → fix `i`,
solve 2Sum on `nums[i+1:]` with target `-nums[i]`. 4Sum → fix two, solve 2Sum.
**Sorting is not optional here**: it's what makes both the two-pointer scan *and*
the duplicate-skipping possible.

## 🔍 Dry run: sorted `[-4, -1, -1, 0, 1, 2]`
| i | nums[i] | need | lo..hi scan | result |
|---|---|---|---|---|
| 0 | −4 | +4 | (−1,2)=1 ↑, (−1,... ) never reaches 4 | none |
| 1 | −1 | +1 | lo=2(−1), hi=5(2) → −1+2 = **1** ✓ | `[-1,-1,2]` |
| | | | then lo=3(0), hi=4(1) → 0+1 = **1** ✓ | `[-1,0,1]` |
| 2 | −1 | | `nums[2] == nums[1]` → **SKIP** | (would duplicate) |
| 3 | 0 | 0 | lo=4(1), hi=5(2) → 3 ↓, pointers cross | none |

Stop at `i = 3`: once `nums[i] > 0`, three sorted numbers starting there are all
positive and can never sum to zero. Free early exit.

## ✅ Optimal solution
```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()                                   # O(n log n), enables everything
        n, res = len(nums), []

        for i in range(n - 2):
            if nums[i] > 0:                           # sorted: rest are all positive
                break
            if i > 0 and nums[i] == nums[i - 1]:      # skip duplicate anchors
                continue

            lo, hi = i + 1, n - 1                     # <-- this is EP001, verbatim
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1
                elif total > 0:
                    hi -= 1
                else:
                    res.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    # skip duplicates AFTER recording a hit
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1
        return res
```
**Time:** O(n²), n anchors × O(n) scan; the O(n log n) sort is dominated.
**Space:** O(1) beyond the output (or O(log n) for the sort's stack).

## ⚠️ Gotchas: this is the video
There are **three separate** duplicate skips and they are not interchangeable:

1. **`i > 0 and nums[i] == nums[i-1]`**: skips duplicate *anchors*. The `i > 0`
   guard is essential; without it, `i=0` reads `nums[-1]` (the last element) and you
   silently skip a valid first anchor.
2. **`nums[lo] == nums[lo-1]`**: skips duplicate left values, **only after a hit**.
   Doing it before a hit is wrong: you'd skip values you never evaluated.
3. **`nums[hi] == nums[hi+1]`**: same, on the right.

Other traps:
- After recording a hit you must move **both** pointers. Moving one guarantees the
  next sum misses (you changed one addend against a fixed target), it terminates,
  but it's a wasted iteration and it signals you don't know why it works.
- `range(n - 2)`, not `range(n)`. You need two elements to the right of the anchor.
- Don't use a `set` of tuples to de-dup. It works, it's O(n) memory, and every
  interviewer reads it as "didn't understand the sorted structure."

## 🎤 Interview talking points
- *"kSum reduces to (k−1)Sum by fixing an element, so 3Sum is 2Sum in a loop."*
- *"Sorting buys me two things: the two-pointer convergence, and duplicate handling
  by adjacency instead of by hash set."*
- *"O(n²) is optimal for 3Sum, there's no known subquadratic algorithm."* (True, and
  a strong thing to know.)

## 🔗 Transfer
EP6 (3Sum Closest) and EP7 (Triplets with Smaller Sum) are this exact skeleton with
the `else` branch changed. EP10 (4Sum) adds one more nested anchor. Once today lands,
those three are ~20-minute problems.

## 📹 Metadata
- **Title:** `3Sum, it's just Two Sum in a loop (the hard part is duplicates) | Two Pointers #5`
- **Thumbnail:** `THE DUPLICATE TRAP` (blue block)
- **Short:** The three duplicate-skips, 60 seconds. This will do well on its own.
