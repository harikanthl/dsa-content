"""
EP001 · P01E01 · Pair with Target Sum   [Easy]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/01-pair-with-target-sum.md
Link:    https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/

Run:  dsa test 1          (or)  pytest problems/01-two-pointers/01_pair_with_target_sum.py -q
"""
from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """Return the 1-indexed positions of the pair summing to target.

        Time:  O(n) — each pointer moves at most n times and never backwards,
               so the loop runs at most 2n iterations.
        Space: O(1) — two integers, regardless of input size.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^2) time / O(1) space: test every pair with two nested loops.
        # Wasteful because it re-learns what sortedness already told us — once
        # 2 + 15 overshoots, 7 + 15 and 11 + 15 must overshoot too.
        #
        # --- optimal ------------------------------------------------------
        lo, hi = 0, len(numbers) - 1

        while lo < hi:
            total = numbers[lo] + numbers[hi]
            if total == target:
                return [lo + 1, hi + 1]   # the problem wants 1-indexed positions
            if total < target:
                lo += 1                   # need a bigger sum; only lo can grow it
            else:
                hi -= 1                   # need a smaller sum; only hi can shrink it

        return []                         # unreachable: the problem guarantees a solution


# ---------------------------------------------------------------- tests
CASES = [
    (([2, 7, 11, 15], 9), [1, 2]),
    (([2, 3, 4], 6), [1, 3]),
    (([-1, 0], -1), [1, 2]),
    (([1, 2, 3, 4, 4, 9, 56, 90], 8), [4, 5]),   # answer sits adjacent in the middle
    (([5, 25, 75], 100), [2, 3]),                # answer is the last two
]


def test_cases():
    for args, want in CASES:
        got = Solution().twoSum(*args)
        assert got == want, f"{args} -> {got}, want {want}"


def test_no_pair_returns_empty():
    # Not a LeetCode input, but the guard has to hold: lo and hi must cross.
    assert Solution().twoSum([1, 2, 3], 100) == []
