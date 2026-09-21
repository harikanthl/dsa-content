"""
EP012 · P01E12 · Minimum Window Sort   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/12-minimum-window-sort.md
Link:    https://leetcode.com/problems/shortest-unsorted-continuous-subarray/
         https://www.ideserve.co.in/learn/minimum-length-subarray-sorting-which-results-in-sorted-array

Run:  dsa test 12         (or)  pytest problems/01-two-pointers/12_minimum_window_sort.py -q
"""
from typing import List


class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        """Length of the shortest subarray that, once sorted, sorts the whole array.

        Time:  O(n) — five linear passes, no nesting.
        Space: O(1) if you track min/max in a loop; the slices below are O(k) in
               Python, which is worth naming out loud rather than glossing over.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n log n): sort a copy, then compare element by element to find the
        # first and last index that differ. Correct, easy, and a fine answer to
        # give first — but it pays for a full sort to learn two indices, and the
        # array already tells you where it stops ascending.
        #
        # --- optimal ------------------------------------------------------
        n = len(nums)
        lo, hi = 0, n - 1

        # 1. first index from the left that breaks ascending order
        while lo < n - 1 and nums[lo] <= nums[lo + 1]:   # <=, not <: equal neighbours are sorted
            lo += 1
        if lo >= n - 1:
            return 0                                     # already sorted (also the empty/single guard)

        # 2. first index from the right that breaks it
        while hi > 0 and nums[hi] >= nums[hi - 1]:
            hi -= 1

        # 3. the extremes inside that rough window
        window_min = min(nums[lo:hi + 1])
        window_max = max(nums[lo:hi + 1])

        # 4. extend left: anything bigger than the window's min belongs inside it
        while lo > 0 and nums[lo - 1] > window_min:
            lo -= 1

        # 5. extend right: anything smaller than the window's max belongs inside it
        while hi < n - 1 and nums[hi + 1] < window_max:
            hi += 1

        return hi - lo + 1


# ---------------------------------------------------------------- tests
CASES = [
    (([2, 6, 4, 8, 10, 9, 15],), 5),          # the classic: [6, 4, 8, 10, 9]
    (([1, 3, 2, 0, -1, 7, 10],), 5),          # steps 4 and 5 both fire
    (([1, 3, 2, 0, 5],), 4),                  # fails without the extend-left pass
    (([1, 2, 5, 3, 7, 10, 9, 12],), 5),
    (([1, 2, 3],), 0),                        # already sorted
    (([1, 1, 1],), 0),                        # all identical — needs <= / >=, not < / >
    (([3, 2, 1],), 3),                        # fully reversed
    (([2, 1],), 2),
    (([1],), 0),                              # single element
    (([],), 0),                               # empty
    (([1, 2, 4, 5, 3],), 3),                  # tail element belongs further left
    (([5, 1, 2, 3, 4],), 5),                  # head element belongs at the end
]


def test_cases():
    for args, want in CASES:
        got = Solution().findUnsortedSubarray(list(args[0]))
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_the_sort_oracle():
    # Oracle: sort a copy and diff. Exhaustive over every short array drawn from
    # {0,1,2,3} — this is what catches a missing extend pass.
    import itertools

    def oracle(nums: List[int]) -> int:
        target = sorted(nums)
        diff = [i for i, (a, b) in enumerate(zip(nums, target)) if a != b]
        return diff[-1] - diff[0] + 1 if diff else 0

    for length in range(0, 6):
        for nums in itertools.product(range(4), repeat=length):
            got = Solution().findUnsortedSubarray(list(nums))
            assert got == oracle(list(nums)), f"{nums} -> {got}, want {oracle(list(nums))}"
