"""
EP009 · P01E09 · Dutch National Flag Problem   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/09-dutch-national-flag-problem.md
Link:    https://leetcode.com/problems/sort-colors/description/

Run:  dsa test 9          (or)  pytest problems/01-two-pointers/09_dutch_national_flag_problem.py -q
"""
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """Sort an array of 0s, 1s and 2s in place, in a single pass.

        Time:  O(n) — every iteration either advances mid or retreats high, and
               the unexamined region [mid, high] shrinks by one each time.
        Space: O(1) — three indices, swaps in place.

        The invariant: [0, low) is all 0s, [low, mid) is all 1s, (high, n) is all
        2s, and [mid, high] is the unexamined middle.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n) two-pass counting sort: count the 0s, 1s and 2s, then overwrite.
        # Correct, and genuinely fine — but it reads the array twice, and it only
        # works because the values are a tiny known set. The one-pass partition
        # below is the same move quicksort uses, which is why it's worth knowing.
        #
        # --- optimal ------------------------------------------------------
        low, mid, high = 0, 0, len(nums) - 1

        while mid <= high:                    # <=, not <: the last element still needs placing
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1                      # safe: everything in [low, mid) is a known 1,
                                              # so the value swapped in is already correct
            elif nums[mid] == 1:
                mid += 1                      # already in place
            else:                             # nums[mid] == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
                # mid does NOT advance: nums[high] came from the unexamined region,
                # so the value now at mid has never been looked at.


# ---------------------------------------------------------------- tests
# (input, expected-after) — the function mutates, so every case runs on a copy.
CASES = [
    ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
    ([2, 0, 1], [0, 1, 2]),
    ([2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2]),    # no 1s at all
    ([1, 1, 1], [1, 1, 1]),                      # all identical
    ([0, 1, 2], [0, 1, 2]),                      # already sorted
    ([2, 1, 0], [0, 1, 2]),                      # exactly reversed
    ([2, 0], [0, 2]),                            # the 2-swap, then mid == high
    ([0], [0]),
    ([2], [2]),                                  # single 2: high goes to -1
    ([], []),
]


def test_cases():
    for nums, want in CASES:
        got = list(nums)
        Solution().sortColors(got)
        assert got == want, f"{nums} -> {got}, want {want}"


def test_matches_sorted_on_every_short_arrangement():
    # Exhaustive over all 0/1/2 arrays up to length 5 — if `mid` ever advances
    # after the 2-swap, or the loop uses `<` instead of `<=`, something here fails.
    import itertools

    for length in range(1, 6):
        for nums in itertools.product((0, 1, 2), repeat=length):
            got = list(nums)
            Solution().sortColors(got)
            assert got == sorted(nums), f"{nums} -> {got}, want {sorted(nums)}"
