# EP007 · P01E07 · Triplets with Smaller Sum   [Medium]

**Pattern:** Two Pointers · **Link:** https://www.geeksforgeeks.org/problems/count-triplets-with-sum-smaller-than-x5549/1

---

## 🎬 Hook
> "This one looks like 3Sum, but there's a trick that makes it *faster to think about*:
> when you find one valid triplet, you've actually found a whole batch of them at once.
> One subtraction counts them all."

## 📋 Problem, in your words
```
Given an array and a target, COUNT how many triplets (i, j, k) with i < j < k
have nums[i] + nums[j] + nums[k] < target.

Count them. Don't list them.
```

## 🔢 The example
```
Input:  nums = [-1, 1, 2, 3, 4],  target = 5
Sorted: [-1, 1, 2, 3, 4]
Output: 4
Triplets: (-1,1,2)=2  (-1,1,3)=3  (-1,1,4)=4  (-1,2,3)=4    all < 5
```

## 🧸 ELI5
> You've frozen one person and you're two-finger walking the rest, like 3Sum.
>
> Now suppose left finger is on `1`, right finger is on `4`, and the total is under
> the limit. Here's the leap: **everything between those two fingers is smaller than
> `4`**, because the list is sorted. So pairing `1` with *any* of them is also under
> the limit.
>
> You don't need to check them one at a time. There are `hi − lo` of them. Add that
> number to your count and slide the left finger right.
>
> It's like a shop where you find the most expensive thing you can afford, you
> instantly know you can afford everything cheaper, without checking price tags.

## 🐌 Brute force (say it, don't type it)
Three nested loops counting, **O(n³)**.

## 💡 The pattern reveal
**Signal:** *count* triplets satisfying an **inequality** (not an equality).
**Therefore:** sort + fix one + two pointers, with **batch counting**.

**Key insight, this is the whole video:** when `nums[i] + nums[lo] + nums[hi] < target`,
every index strictly between `lo` and `hi` also works as the third element, because
all of them are ≤ `nums[hi]`. That's `hi - lo` triplets, counted in one operation
instead of `hi - lo` operations. This is what turns O(n³) into O(n²).

## 🔍 Dry run: `[-1, 1, 2, 3, 4]`, target 5
| i | anchor | lo | hi | sum | < 5? | action |
|---|---|---|---|---|---|---|
| 0 | −1 | 1 | 4 | −1+1+4 = 4 | yes | count += (4−1) = **3**, `lo=2` |
| 0 | −1 | 2 | 4 | −1+2+4 = 5 | no | `hi=3` |
| 0 | −1 | 2 | 3 | −1+2+3 = 4 | yes | count += (3−2) = **1**, `lo=3` |
| 0 | | 3 | 3 | - | | `lo == hi`, stop |
| 1 | 1 | 2 | 4 | 1+2+4 = 7 | no | `hi=3` |
| 1 | 1 | 2 | 3 | 1+2+3 = 6 | no | `hi=2`, stop |
| 2 | 2 | 3 | 4 | 2+3+4 = 9 | no | stop |

Total = **4** ✓

Note step 1: `count += 3` captured `(-1,1,2)`, `(-1,1,3)`, `(-1,1,4)` in one line.
Point at that on camera.

## ✅ Optimal solution
```python
class Solution:
    def countTriplets(self, nums: List[int], target: int) -> int:
        nums.sort()
        n, count = len(nums), 0

        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                if nums[i] + nums[lo] + nums[hi] < target:
                    count += hi - lo        # <-- the whole trick: a BATCH, not one
                    lo += 1
                else:
                    hi -= 1                 # too big: only shrinking hi can help

        return count
```
**Time:** O(n²) · **Space:** O(1) beyond the sort

## ⚠️ Gotchas
- **`hi - lo`, not `hi - lo + 1`.** The `+1` would count the pair `(lo, hi)` twice,
  once as itself and once as "an element between." Draw the indices on screen and
  count them by hand; this off-by-one is the entire difficulty of the problem.
- Advance `lo` **after** counting, not before.
- No duplicate-skipping. You're counting index triplets, so repeated *values* at
  different indices are genuinely different triplets and must all be counted. This is
  the opposite of 3Sum, call out the contrast explicitly, it makes both stick.
- If the problem asked you to *list* the triplets instead of count them, the batch
  trick evaporates and you're back to O(n³) output-bound. Worth saying: the batching
  is only available because the output is a single number.

## 🎤 Interview talking points
- *"Sortedness lets me count a range of solutions in O(1) instead of enumerating it.
  That's the difference between O(n³) and O(n²) here."*
- *"Because the output is a count, not a list, I'm not bound by the size of the
  answer set, so I can batch."*

## 🔗 Transfer
"Counting a batch instead of enumerating it" is the same move as EP8 (Subarray
Product Less Than K), where `hi - lo + 1` counts all subarrays ending at `hi`. Note
the `+1` differs between the two, and know *why*. That pair of problems, side by
side, is one of the best off-by-one lessons in the whole sheet.

## 📹 Metadata
- **Title:** `Count Triplets with Smaller Sum, count a batch, not one at a time | Two Pointers #7`
- **Thumbnail:** `COUNT, DON'T LIST` (blue block)
- **Short:** The `hi - lo` vs `hi - lo + 1` question. Ask it, pause, answer it.
