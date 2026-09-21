"""
EP010 · P01E10 · Quadruple Sum to Target   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/10-quadruple-sum-to-target.md
Link:    https://leetcode.com/problems/4sum/

Run:  dsa test 10         (or)  pytest problems/01-two-pointers/10_quadruple_sum_to_target.py -q
"""
from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        """Find every unique quadruplet summing to target.

        Time:  O(n^3) — two nested anchors, each pair with an O(n) scan.
        Space: O(1) beyond the output and the sort.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n^4): four nested loops plus a set to de-duplicate. Sorting first
        # collapses the innermost two loops into one two-pointer scan, exactly
        # as it did in EP005 — 4Sum is 3Sum with one more anchor peeled off.
        #
        # --- optimal ------------------------------------------------------
        nums.sort()
        n, res = len(nums), []

        for i in range(n - 3):                          # need three elements right of i
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            # Pruning. Getting break/continue backwards is a silent wrong answer.
            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break                                   # smallest from here already overshoots
            if nums[i] + nums[n - 3] + nums[n - 2] + nums[n - 1] < target:
                continue                                # largest from here still falls short

            for j in range(i + 1, n - 2):               # need two elements right of j
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue                            # j > i + 1, NOT j > 0

                lo, hi = j + 1, n - 1                   # EP001 again, one level deeper
                need = target - nums[i] - nums[j]
                while lo < hi:
                    pair = nums[lo] + nums[hi]
                    if pair < need:
                        lo += 1
                    elif pair > need:
                        hi -= 1
                    else:
                        res.append([nums[i], nums[j], nums[lo], nums[hi]])
                        lo += 1
                        hi -= 1
                        while lo < hi and nums[lo] == nums[lo - 1]:
                            lo += 1
                        while lo < hi and nums[hi] == nums[hi + 1]:
                            hi -= 1

        return res


def kSum(nums: List[int], target: int, k: int) -> List[List[int]]:
    """The generalisation: one function for 2Sum, 3Sum, 4Sum and any kSum.

    Expects `nums` already sorted. Peels one anchor off per level of recursion
    until k == 2, where the two-pointer scan is the base case.

    Time:  O(n^(k-1)) · Space: O(k) recursion depth, beyond the output.
    """
    res: List[List[int]] = []
    if not nums:
        return res

    if k == 2:                                          # base case: two pointers
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            pair = nums[lo] + nums[hi]
            if pair < target:
                lo += 1
            elif pair > target:
                hi -= 1
            else:
                res.append([nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
        return res

    for i in range(len(nums) - k + 1):                  # recursive case: peel one off
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for rest in kSum(nums[i + 1:], target - nums[i], k - 1):
            res.append([nums[i]] + rest)
    return res


# ---------------------------------------------------------------- tests
# The algorithm emits quadruplets in sorted order, so the expected lists are exact.
CASES = [
    (([1, 0, -1, 0, -2, 2], 0), [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
    (([2, 2, 2, 2, 2], 8), [[2, 2, 2, 2]]),             # all identical
    (([0, 0, 0, 0], 0), [[0, 0, 0, 0]]),
    (([1, 2, 3, 4], 100), []),                          # target unreachable — the continue prunes
    (([1, 2, 3, 4], 0), []),                            # target below every sum — the break prunes
    (([-3, -1, 0, 2, 4, 5], 2), [[-3, -1, 2, 4]]),      # unique answer, no duplicates
    (([1, 2, 3], 6), []),                               # too short for a quadruplet
    (([], 0), []),
]


def test_cases():
    for args, want in CASES:
        nums, target = args
        got = Solution().fourSum(list(nums), target)
        assert got == want, f"{args} -> {got}, want {want}"


def test_ksum_agrees_with_foursum():
    for args, _ in CASES:
        nums, target = args
        want = Solution().fourSum(list(nums), target)
        got = kSum(sorted(nums), target, 4)
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_brute_force():
    import itertools

    for nums, target in ([1, 0, -1, 0, -2, 2], 0), ([2, 2, 2, 2, 2], 8), ([-3, -1, 0, 2, 4, 5], 2):
        want = sorted({tuple(sorted(q))
                       for q in itertools.combinations(nums, 4) if sum(q) == target})
        got = sorted(tuple(q) for q in Solution().fourSum(list(nums), target))
        assert got == want, f"{nums},{target} -> {got}, want {want}"
