# EP010 · P01E10 · Quadruple Sum to Target (4Sum)   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/4sum/

---

## 🎬 Hook
> "By now you should be bored of this, and that's the point. 2Sum, 3Sum, 4Sum, it's
> one recursive idea: fix a number, solve the smaller problem. Today I'll write 4Sum,
> and then I'll write the version that solves *k*Sum for any k."

## 📋 Problem, in your words
```
Given an array and a target, find all UNIQUE quadruplets [a, b, c, d]
where a + b + c + d == target.

Unique means: no duplicate quadruplets in the output.
The target can be any integer (not just 0, unlike 3Sum).
```

## 🔢 The example
```
Input:  nums = [1, 0, -1, 0, -2, 2],  target = 0
Sorted: [-2, -1, 0, 0, 1, 2]
Output: [[-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]]
```

## 🧸 ELI5
> Splitting a restaurant bill four ways with exact change.
>
> Freeze one person's contribution. Now it's a three-way split of what remains,
> which is 3Sum, which you did on day 5. Freeze a second person, and it's a two-way
> split, the bookshelf trick from day 1.
>
> Two frozen people, two walking fingers. Every layer you freeze is one more `for`
> loop, and the fingers at the bottom are always the same code.

## 🐌 Brute force (say it, don't type it)
Four nested loops, **O(n⁴)**. At n = 200 that's 1.6 billion operations.

## 💡 The pattern reveal
**Signal:** find a k-tuple summing to a target.
**Therefore:** the **kSum reduction**: sort once, fix (k−2) elements with nested
loops, converge two pointers at the bottom.

**Key insight:** kSum is not k separate problems. It's one recursive definition:
```
kSum(k, target) = for each anchor a:  (k-1)Sum(target - a)
base case: 2Sum on a sorted array = two pointers
```
Complexity is **O(n^(k−1))**. 2Sum → O(n), 3Sum → O(n²), 4Sum → O(n³).

## 🔍 Dry run: sorted `[-2, -1, 0, 0, 1, 2]`, target 0
| i | j | anchors | need | lo..hi | found |
|---|---|---|---|---|---|
| 0 | 1 | −2, −1 | +3 | lo=2(0), hi=5(2) → 2 ↑ … lo=4(1), hi=5(2) → **3** ✓ | `[-2,-1,1,2]` |
| 0 | 2 | −2, 0 | +2 | lo=3(0), hi=5(2) → **2** ✓ | `[-2,0,0,2]` |
| 0 | 3 | −2, 0 | | `nums[3]==nums[2]` → **SKIP j** | duplicate |
| 1 | 2 | −1, 0 | +1 | lo=3(0), hi=5(2) → 2 ↓; lo=3, hi=4(1) → **1** ✓ | `[-1,0,0,1]` |

## ✅ Optimal solution
```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n, res = len(nums), []

        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            # pruning: smallest possible / largest possible sum from here
            if nums[i] + nums[i+1] + nums[i+2] + nums[i+3] > target:
                break                                   # only grows from here
            if nums[i] + nums[n-3] + nums[n-2] + nums[n-1] < target:
                continue                                # this anchor can't reach

            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                lo, hi = j + 1, n - 1                   # <-- EP001 again
                need = target - nums[i] - nums[j]
                while lo < hi:
                    s = nums[lo] + nums[hi]
                    if s < need:
                        lo += 1
                    elif s > need:
                        hi -= 1
                    else:
                        res.append([nums[i], nums[j], nums[lo], nums[hi]])
                        lo += 1
                        hi -= 1
                        while lo < hi and nums[lo] == nums[lo - 1]:
                            lo += 1
                        while lo < hi and nums[hi] == nums[hi + 1]:
                            hi -= 1
        return res
```
**Time:** O(n³) · **Space:** O(1) beyond output and sort

### The generalisation: show this at the end, it's the payoff
```python
def kSum(nums: List[int], target: int, k: int) -> List[List[int]]:
    res = []
    if not nums:
        return res
    if k == 2:                                  # base case: two pointers
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            s = nums[lo] + nums[hi]
            if s < target:   lo += 1
            elif s > target: hi -= 1
            else:
                res.append([nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
        return res
    for i in range(len(nums) - k + 1):          # recursive case: peel one off
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for sub in kSum(nums[i+1:], target - nums[i], k - 1):
            res.append([nums[i]] + sub)
    return res

# usage:  nums.sort();  kSum(nums, target, 4)
```
Say on camera: *"This one function answers 2Sum, 3Sum, 4Sum and any kSum an
interviewer invents on the spot."* That's the moment the viewer subscribes.

## ⚠️ Gotchas
- **Duplicate guards at every level.** `i > 0` for the outer, `j > i + 1` for the
  inner. Writing `j > 0` is a real bug: it skips the legitimate first `j` whenever
  `nums[i] == nums[i+1]`.
- **`break` vs `continue` in the pruning.** If the *smallest* four numbers from `i`
  already exceed target, nothing later can work → `break`. If the *largest* possible
  from `i` still falls short, only this anchor fails → `continue`. Getting these
  backwards is a silent wrong answer, not a crash.
- Python ints are arbitrary precision, so no overflow. In Java/C++ you'd need `long`.
  Mention it, interviewers in those languages will ask.
- `range(n - 3)` and `range(i+1, n-2)`: you need three elements after `i` and two after `j`.

## 🎤 Interview talking points
- *"kSum reduces to (k−1)Sum; the base case is 2Sum with two pointers. That gives
  O(n^(k−1))."*
- *"The pruning steps aren't required for correctness but cut real runtime, and they
  fall straight out of the array being sorted."*

## 🔗 Transfer
This closes the kSum family (EP1, 5, 6, 7, 10). The recursive peel-one-off shape is
also how you'll think about **backtracking** in Pattern 12 (EP 111–120), Combination
Sum is structurally this same recursion without the sorted two-pointer base case.

## 📹 Metadata
- **Title:** `4Sum → kSum, one function for every "find k numbers" problem | Two Pointers #10`
- **Thumbnail:** `2SUM → 3SUM → kSUM` (blue block)
- **Short:** The recursive kSum function, 60s. Strong standalone.
