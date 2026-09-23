# EP088 · P10E18 · Split Array Largest Sum   [Hard]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/split-array-largest-sum/description/

---

## 🎬 Hook
> "LeetCode marks this one **Hard**. You solved it yesterday. Split an array into k
> pieces so the biggest piece is as small as possible: that's Book Allocation with the
> story stripped off. Today's episode is about **recognising a duplicate**, and then
> proving the greedy check is right, because that's what makes it Hard."

## 📋 Problem, in your words
```
Split nums into k NON-EMPTY, CONTIGUOUS subarrays.
Among those k pieces, one has the largest sum.

Minimise that largest sum and return it.
(1 <= k <= min(50, len(nums)), so a valid split always exists.)
```

## 🔢 The example
```
Input:  nums = [7, 2, 5, 10, 8], k = 2
Output: 18
Why:    [7, 2, 5] | [10, 8]  -> sums 14 and 18, the largest is 18.
        [7, 2, 5, 10] | [8]  -> 24 and 8, worse.

Input:  nums = [1, 2, 3, 4, 5], k = 2  -> 9   ([1,2,3] [4,5])
Input:  nums = [1, 4, 4],       k = 3  -> 4   (every number alone)
```

## 🧸 ELI5
> Same shelf, same teacher, no story. She picks a **cap** and walks left to right,
> closing a piece whenever the next number would push it over the cap.
>
> ```
> nums: 7  2  5  10  8          k = 2
>
> cap 21:  [7 2 5] [10 8]        2 pieces  ✓
> cap 18:  [7 2 5] [10 8]        2 pieces  ✓
> cap 17:  [7 2 5] [10] [8]      3 pieces  ✗
> ```
>
> Loose cap, few pieces. Tight cap, many. The tightest cap that still needs `<= k`
> pieces is the answer.

## 🐌 Brute force (say it, don't type it)
Try every placement of `k - 1` cuts: **C(n−1, k−1)** splits. The textbook DP,
`dp[i][j]` = best largest-sum splitting the first `i` numbers into `j` pieces, is
**O(k · n²)** and correct. Mention it: it's the answer an interviewer expects you to
beat. Binary search on the answer is **O(n log S)**.

## 💡 The pattern reveal
**Signal:** "**minimise the largest** sum" · contiguous pieces · a fixed number of them.
**Therefore:** Shape C, minimise flavour. EP87 verbatim.

| decision | here |
|---|---|
| what is `x`? | the cap on any one piece's sum |
| what is `feasible(x)`? | greedy: `pieces_needed(x) <= k` |
| why monotonic? | a higher cap never needs more pieces |
| what is the range? | `[max(nums), sum(nums)]` |

**Why the greedy check is correct (the Hard part):** for a fixed cap, packing each
piece as full as possible uses the **fewest** pieces. Take any valid split; slide its
first cut right as far as the cap allows. That never adds a piece and never breaks the
cap, and repeating it for each cut gives exactly the greedy split. And if the greedy
needs **fewer** than `k` pieces, you can split any piece further (sums only shrink),
so `<= k` is the right test.

## 🔍 Dry run: `[7, 2, 5, 10, 8]`, `k = 2`
Range `[10, 32]`.

| step | lo | hi | mid | pieces | count | ≤ 2? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 10 | 32 | 21 | [7,2,5] [10,8] | 2 | ✓ | `hi = 21` |
| 2 | 10 | 21 | 15 | [7,2,5] [10] [8] | 3 | ✗ | `lo = 16` |
| 3 | 16 | 21 | 18 | [7,2,5] [10,8] | 2 | ✓ | `hi = 18` |
| 4 | 16 | 18 | 17 | [7,2,5] [10] [8] | 3 | ✗ | `lo = 18` |
| - | 18 | 18 | stop | | | | answer **18** ✓ |

The answer is `10 + 8`, a real piece sum. It always is: if cap `x` works but no piece
sums to exactly `x`, then `x - 1` works too, so `x` wasn't the smallest.

## ✅ Optimal solution
```python
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        """Minimise the largest sum among k contiguous non-empty pieces.

        Time:  O(n log S), S = sum(nums): log S greedy passes.
        Space: O(1).
        """
        def pieces_needed(cap: int) -> int:
            pieces, total = 1, 0
            for x in nums:
                if total + x > cap:         # x opens a new piece
                    pieces += 1
                    total = 0
                total += x
            return pieces

        lo, hi = max(nums), sum(nums)       # biggest single number; the whole array
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:
                hi = mid                    # cap works; try tighter
            else:
                lo = mid + 1
        return lo
```
**Time:** O(n log S) · **Space:** O(1)

## ⚠️ Gotchas
- **`<= k`.** The greedy may use fewer pieces than `k`; that's still a yes, since
  pieces can always be split further. `== k` breaks monotonicity.
- **`lo = max(nums)`.** Below it, the biggest element fits in no piece.
- **Non-negative numbers only.** With negatives, "higher cap, fewer pieces" is false and
  the greedy fails. The constraints say `0 <= nums[i]`; say why that matters.
- **Don't memorise three problems.** EP86, EP87 and EP88 are one algorithm. If you have
  three different versions in your head, one of them will have a bug.

## 🎤 Interview talking points
- *"Binary search on the maximum piece sum, with a greedy check that packs each piece as
  full as possible."*
- *"The greedy gives the minimum number of pieces for a cap, by sliding each cut right;
  and fewer than k is fine because pieces can be split further."* ← this is the Hard.
- *"The DP is O(k·n²); this is O(n log S), which wins whenever the sum isn't
  astronomically larger than n."*
- *"It's the same algorithm as Book Allocation and Ship Packages."*

## 🔗 Transfer
That closes the minimise run (EP86 to EP88). Next, the pattern moves into two
dimensions: EP89 Search a 2-D Matrix is Shape A after one line of `divmod`, and by EP91
Shape C comes back, searching **values** in a matrix instead of capacities.

## 📹 Metadata
- **Title:** `Split Array Largest Sum, a Hard you already solved | Binary Search #18`
- **Thumbnail:** `HARD = EP87` (red block)
- **Short:** the "slide the cut right" proof, one cut moving across the array. 50s.
