"""
EP002 · P01E02 · Rearrange 0 and 1   [Easy]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/02-rearrange-0-and-1.md
Link:    https://www.geeksforgeeks.org/problems/segregate-0s-and-1s5106/1

Run:  dsa test 2          (or)  pytest problems/01-two-pointers/02_rearrange_0_and_1.py -q
"""
from typing import List


class Solution:
    def segregate0and1(self, arr: List[int]) -> None:
        """Rearrange arr in place so every 0 precedes every 1.

        Time:  O(n) — each iteration advances lo or hi (or both), and they only
               ever move toward each other, so the loop runs at most n times.
        Space: O(1) — two indices; the swap is in place.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n log n): arr.sort(). One line, correct, and enormous overkill —
        # a comparison sort to order a set with exactly two distinct values.
        #
        # --- optimal ------------------------------------------------------
        lo, hi = 0, len(arr) - 1

        while lo < hi:
            if arr[lo] == 0:            # already on the correct side
                lo += 1
            elif arr[hi] == 1:          # already on the correct side
                hi -= 1
            else:                       # arr[lo]==1 and arr[hi]==0 — both misplaced
                arr[lo], arr[hi] = arr[hi], arr[lo]
                lo += 1                 # one swap fixes two elements, so move both
                hi -= 1

    def segregate0and1_by_counting(self, arr: List[int]) -> None:
        """The counting alternative: also O(n)/O(1), but it reads the array twice.

        Kept for the video — the point is that it only works for exactly two
        values, whereas the two-pointer version generalises to EP009's three.
        """
        zeros = arr.count(0)
        arr[:zeros] = [0] * zeros
        arr[zeros:] = [1] * (len(arr) - zeros)


# ---------------------------------------------------------------- tests
# (input, expected-after) — the function mutates, so every case runs on a copy.
CASES = [
    ([0, 1, 0, 1, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]),
    ([1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]),     # fully reversed: n/2 swaps
    ([0, 0, 0], [0, 0, 0]),                       # all identical
    ([1, 1, 1], [1, 1, 1]),                       # all identical, other value
    ([0, 1], [0, 1]),                             # already correct, two elements
    ([1, 0], [0, 1]),                             # single swap
    ([1], [1]),                                   # single element — loop never runs
    ([], []),                                     # empty — hi is -1, loop never runs
]


def test_cases():
    for arr, want in CASES:
        got = list(arr)
        Solution().segregate0and1(got)
        assert got == want, f"{arr} -> {got}, want {want}"


def test_counting_agrees_with_two_pointers():
    # Both are correct answers; the episode is about why we prefer one.
    for arr, want in CASES:
        got = list(arr)
        Solution().segregate0and1_by_counting(got)
        assert got == want, f"{arr} -> {got}, want {want}"
