"""
EP007 · P01E07 · Triplets with Smaller Sum   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/07-triplets-with-smaller-sum.md
Link:    https://www.geeksforgeeks.org/problems/count-triplets-with-sum-smaller-than-x5549/1

Run:  dsa test 7          (or)  pytest problems/01-two-pointers/07_triplets_with_smaller_sum.py -q
"""
from typing import List


class Solution:
    def countTriplets(self, nums: List[int], target: int) -> int:
        """Count index triplets i < j < k with nums[i] + nums[j] + nums[k] < target.

        Time:  O(n^2) — n anchors, each with an O(n) two-pointer scan.
        Space: O(1) beyond the sort.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^3): three nested loops, incrementing a counter. The waste is that
        # it re-checks triplets sortedness has already settled — once a pair is
        # under the limit, so is every smaller pair between the two pointers.
        #
        # --- optimal ------------------------------------------------------
        nums.sort()
        n, count = len(nums), 0

        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                if nums[i] + nums[lo] + nums[hi] < target:
                    # Every index strictly between lo and hi holds a value <= nums[hi],
                    # so it works as the third element too. That's hi - lo triplets,
                    # counted in one operation — this is what makes it O(n^2).
                    count += hi - lo
                    lo += 1                  # advance AFTER counting
                else:
                    hi -= 1                  # too big: only shrinking hi can help

        return count
        # No duplicate-skipping, unlike EP005: these are index triplets, so equal
        # values at different indices are genuinely different triplets.


# ---------------------------------------------------------------- tests
CASES = [
    (([-1, 1, 2, 3, 4], 5), 4),         # (-1,1,2) (-1,1,3) (-1,1,4) (-1,2,3)
    (([-1, 0, 2, 3], 3), 2),            # (-1,0,2) (-1,0,3)
    (([5, 1, 3, 4, 7], 12), 4),
    (([1, 1, 1, 1], 4), 4),             # all identical: every C(4,3) triplet counts
    (([1, 1, 1, 1], 3), 0),             # strict <, so sum == target does not count
    (([10, 20, 30], 5), 0),             # target below every triplet
    (([1, 2], 100), 0),                 # too short for a triplet
    (([], 5), 0),
]


def test_cases():
    for args, want in CASES:
        nums, target = args
        got = Solution().countTriplets(list(nums), target)
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_brute_force():
    # Oracle for the off-by-one: hi - lo, not hi - lo + 1. Get it wrong and this
    # fails on the very first random-ish input.
    import itertools

    for nums in ([-1, 1, 2, 3, 4], [5, 1, 3, 4, 7], [0, 0, 1, 2, 2, -3]):
        for target in range(-5, 12):
            want = sum(1 for t in itertools.combinations(nums, 3) if sum(t) < target)
            got = Solution().countTriplets(list(nums), target)
            assert got == want, f"{nums},{target} -> {got}, want {want}"
