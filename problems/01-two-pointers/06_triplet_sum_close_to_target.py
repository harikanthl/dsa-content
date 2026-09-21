"""
EP006 · P01E06 · Triplet Sum Close to Target   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/06-triplet-sum-close-to-target.md
Link:    https://leetcode.com/problems/3sum-closest/

Run:  dsa test 6          (or)  pytest problems/01-two-pointers/06_triplet_sum_close_to_target.py -q
"""
from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """Return the triplet sum closest to target.

        Time:  O(n^2) — n anchors, each with an O(n) two-pointer scan.
        Space: O(1) beyond the sort.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^3): every triplet, tracking the smallest |sum - target|. Same
        # structure as 3Sum's brute force, and sorting fixes it the same way —
        # once sorted, the sign of (total - target) tells you which pointer to move.
        #
        # --- optimal ------------------------------------------------------
        nums.sort()
        n = len(nums)
        best = nums[0] + nums[1] + nums[2]            # seed with a REAL triplet

        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]

                if abs(total - target) < abs(best - target):
                    best = total

                if total == target:                   # distance 0 is unbeatable
                    return total
                if total < target:
                    lo += 1
                else:
                    hi -= 1

        return best
        # No duplicate-skipping here, unlike EP005: the answer is a number, not a
        # list, so re-seeing a triplet just recomputes the same distance. Dropping
        # yesterday's de-dup on purpose is the point.


# ---------------------------------------------------------------- tests
CASES = [
    (([-1, 2, 1, -4], 1), 2),
    (([0, 0, 0], 1), 0),                              # all identical
    (([1, 1, 1, 0], -100), 2),                        # target far below every sum
    (([1, 1, 1, 0], 100), 3),                         # target far above every sum
    (([0, 2, 1, -3], 1), 0),                          # exact hit — the early return
    (([4, 0, 5, -5, 3, 3, 0, -4, -5], -2), -2),       # exact hit among duplicates
    (([-3, -2, -5, 3, -4], -1), -2),                  # all-negative answer
]


def test_cases():
    for args, want in CASES:
        nums, target = args
        got = Solution().threeSumClosest(list(nums), target)
        assert got == want, f"{args} -> {got}, want {want}"


def test_seed_must_be_a_reachable_sum():
    # Seeding `best` with 0 or inf is the classic bug. Here every triplet sum is
    # far from 0, so a 0-seed would return a sum that doesn't exist in the array.
    assert Solution().threeSumClosest([10, 20, 30, 40], 0) == 60


def test_matches_brute_force():
    import itertools

    for nums, target in ([-1, 2, 1, -4], 1), ([1, 1, -1, -1, 3], 3), ([0, 3, 97, 102, 200], 300):
        want = min((sum(t) for t in itertools.combinations(nums, 3)),
                   key=lambda s: abs(s - target))
        got = Solution().threeSumClosest(list(nums), target)
        assert abs(got - target) == abs(want - target), f"{nums},{target} -> {got}, want {want}"
