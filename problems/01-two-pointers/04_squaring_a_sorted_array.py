"""
EP004 · P01E04 · Squaring a Sorted Array   [Easy]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/04-squaring-a-sorted-array.md
Link:    https://leetcode.com/problems/squares-of-a-sorted-array/

Run:  dsa test 4          (or)  pytest problems/01-two-pointers/04_squaring_a_sorted_array.py -q
"""
from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """Return the squares of a sorted array, sorted ascending.

        Time:  O(n) — one pass; each step consumes exactly one input element.
        Space: O(n) for the output, which the problem requires. O(1) is not
               possible: you must return a new array, and overwriting the input
               would clobber a value you still need.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n log n): sorted(x * x for x in nums). Correct, one line — but it
        # throws away the fact that the input is already sorted. The squares are
        # only *unsorted* because of the negatives, and the largest square is
        # always at one end or the other. That's a two-pointer signal.
        #
        # --- optimal ------------------------------------------------------
        n = len(nums)
        result = [0] * n
        lo, hi = 0, n - 1

        for write in range(n - 1, -1, -1):     # fill BACKWARDS: biggest square first
            left, right = nums[lo] * nums[lo], nums[hi] * nums[hi]
            if left > right:                   # compare the SQUARES, not the values
                result[write] = left
                lo += 1
            else:
                result[write] = right
                hi -= 1

        return result


# ---------------------------------------------------------------- tests
CASES = [
    (([-4, -1, 0, 3, 10],), [0, 1, 9, 16, 100]),
    (([-7, -3, 2, 3, 11],), [4, 9, 9, 49, 121]),
    (([-5, -4, -3, -2, -1],), [1, 4, 9, 16, 25]),   # all negative — order reverses
    (([1, 2, 3, 4],), [1, 4, 9, 16]),               # all positive — order is kept
    (([-3, 3],), [9, 9]),                           # ties: left > right is False, hi wins
    (([0],), [0]),                                  # single element — the <= / range end
    (([-2, 0, 2],), [0, 4, 4]),
    (([],), []),                                    # empty — the loop never runs
]


def test_cases():
    for args, want in CASES:
        got = Solution().sortedSquares(*args)
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_the_brute_force():
    # The O(n log n) version is the oracle: same answer, different route.
    for args, _ in CASES:
        nums = args[0]
        assert Solution().sortedSquares(nums) == sorted(x * x for x in nums)
