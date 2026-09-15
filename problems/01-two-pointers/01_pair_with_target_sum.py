"""
EP001 · P01E01 · Pair with Target Sum   [Easy]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/01-pair-with-target-sum.md
Link:    https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/

Run:  dsa test 1          (or)  pytest problems/01-two-pointers/01_pair_with_target_sum.py -q
"""
from typing import List, Optional


class Solution:
    def pair_with_target_sum(self):
        # --- brute force (say it out loud, then discard) -------------------
        # O(?) time / O(?) space
        #
        # --- optimal ------------------------------------------------------
        # O(?) time / O(?) space
        pass


# ---------------------------------------------------------------- tests
# Add the LeetCode samples here FIRST, before you write the solution.
CASES = [
    # (args_tuple, expected),
]


def test_cases():
    for args, want in CASES:
        got = Solution().pair_with_target_sum(*args)
        assert got == want, f"{args} -> {got}, want {want}"
