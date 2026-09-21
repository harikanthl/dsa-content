"""
EP005 · P01E05 · Triplet Sum to Zero   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/05-triplet-sum-to-zero.md
Link:    https://leetcode.com/problems/3sum/

Run:  dsa test 5          (or)  pytest problems/01-two-pointers/05_triplet_sum_to_zero.py -q
"""
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Find every unique triplet summing to zero.

        Time:  O(n^2) — n anchors, each with an O(n) two-pointer scan. The
               O(n log n) sort is dominated by that.
        Space: O(1) beyond the output (O(log n) for the sort's stack).
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^3): three nested loops, plus a set of tuples to de-duplicate.
        # The de-dup set is the tell that you're fighting the problem — sorting
        # first makes duplicates adjacent, so they can be skipped for free.
        #
        # --- optimal ------------------------------------------------------
        nums.sort()                                   # O(n log n) — enables everything
        n, res = len(nums), []

        for i in range(n - 2):                        # need two elements right of the anchor
            if nums[i] > 0:                           # sorted: the rest are positive too
                break
            if i > 0 and nums[i] == nums[i - 1]:      # skip duplicate anchors
                continue                              # the i > 0 guard stops nums[-1] wrapping

            lo, hi = i + 1, n - 1                     # this inner loop is EP001, verbatim
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1                           # need a bigger sum
                elif total > 0:
                    hi -= 1                           # need a smaller sum
                else:
                    res.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1                           # move both: one addend alone must miss
                    # Skip duplicates only AFTER a hit — before one, they're values
                    # we haven't evaluated yet.
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1

        return res


# ---------------------------------------------------------------- tests
# The algorithm emits triplets in sorted order, so the expected lists are exact.
CASES = [
    (([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]),
    (([0, 1, 1],), []),                                  # no triplet sums to zero
    (([0, 0, 0],), [[0, 0, 0]]),                         # all identical
    (([0, 0, 0, 0],), [[0, 0, 0]]),                      # duplicate anchors must not repeat it
    (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]]),
    (([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],),
     [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2],
      [-2, -2, 4], [-2, 0, 2]]),                         # heavy duplicates on every index
    (([1, 2, 3],), []),                                  # all positive — the break fires
    (([-1, 0],), []),                                    # too short for a triplet
    (([],), []),
]


def test_cases():
    for args, want in CASES:
        got = Solution().threeSum(*[list(a) for a in args])
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_brute_force_on_duplicate_heavy_input():
    # Oracle: the O(n^3) version, de-duplicated with a set. Slow but obviously
    # correct — exactly the trade the optimal solution is buying its way out of.
    import itertools

    for nums in ([-2, -2, 0, 0, 2, 2], [-1, -1, -1, 2, 2], [3, -1, -2, 0, 1, -1, 2]):
        want = sorted({tuple(sorted(t)) for t in itertools.combinations(nums, 3) if sum(t) == 0})
        got = [tuple(t) for t in Solution().threeSum(list(nums))]
        assert sorted(got) == want, f"{nums} -> {got}, want {want}"
