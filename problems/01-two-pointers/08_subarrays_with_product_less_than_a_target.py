"""
EP008 · P01E08 · Subarrays with Product Less than a Target   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/08-subarrays-with-product-less-than-a-target.md
Link:    https://leetcode.com/problems/subarray-product-less-than-k/

Run:  dsa test 8          (or)  pytest problems/01-two-pointers/08_subarrays_with_product_less_than_a_target.py -q
"""
from typing import List


class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        """Count contiguous subarrays whose product is strictly less than k.

        Time:  O(n) amortised — hi advances n times, and lo only ever moves
               forward, so it also moves at most n times across the whole run.
               The inner while does not make this quadratic.
        Space: O(1) — a running product and two indices.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^2): for every start, extend the end and multiply until you pass k.
        # Wasteful because a window that's already too big stays too big when you
        # extend it — all inputs are >= 1, so growing the window never shrinks
        # the product. That monotonicity is what lets the left edge never rewind.
        #
        # --- optimal ------------------------------------------------------
        if k <= 1:                        # every product is >= 1, so none is < 1
            return 0                      # also the guard that stops lo running past hi

        product, lo, count = 1, 0, 0

        for hi in range(len(nums)):
            product *= nums[hi]           # grow on the right

            while product >= k:           # shrink from the left until valid again
                product //= nums[lo]      # integer division exactly undoes the *=
                lo += 1

            # Every window ending at hi and starting anywhere in [lo, hi] is valid.
            # That's hi - lo + 1 of them — the +1 is the single-element [hi] itself.
            # Contrast EP007's `hi - lo`, which counted indices strictly between.
            count += hi - lo + 1

        return count


# ---------------------------------------------------------------- tests
CASES = [
    (([10, 5, 2, 6], 100), 8),
    (([1, 2, 3], 0), 0),                  # k <= 1 guard
    (([1, 2, 3], 1), 0),                  # k == 1: no product is < 1
    (([1, 1, 1], 2), 6),                  # all identical, all valid: C(3,2) + 3
    (([10, 9, 10, 4, 3, 8, 3, 3, 6, 2, 10, 2, 9, 3], 19), 19),
    (([100], 100), 0),                    # strict <, so equal does not count
    (([100], 101), 1),
    (([], 100), 0),
]


def test_cases():
    for args, want in CASES:
        nums, k = args
        got = Solution().numSubarrayProductLessThanK(list(nums), k)
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_brute_force():
    # Oracle for the other off-by-one: hi - lo + 1 here, hi - lo in EP007.
    import math

    def brute(nums: List[int], k: int) -> int:
        return sum(1
                   for start in range(len(nums))
                   for end in range(start, len(nums))
                   if math.prod(nums[start:end + 1]) < k)

    for nums in ([10, 5, 2, 6], [1, 2, 3, 4], [1, 1, 5, 1, 2]):
        for k in range(0, 40):
            got = Solution().numSubarrayProductLessThanK(list(nums), k)
            assert got == brute(nums, k), f"{nums},{k} -> {got}, want {brute(nums, k)}"
