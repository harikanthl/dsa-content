"""
EP003 · P01E03 · Remove Duplicates   [Easy]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/03-remove-duplicates.md
Link:    https://leetcode.com/problems/remove-duplicates-from-sorted-list/
         https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
         https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/

Three LeetCode problems, one idea: you never delete, you overwrite.

Run:  dsa test 3          (or)  pytest problems/01-two-pointers/03_remove_duplicates.py -q
"""
from typing import List, Optional


class ListNode:
    """LeetCode supplies this; defined here so the file runs standalone."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    # --- brute force (say it out loud, then discard) -----------------------
    # Build a fresh array and append whenever the value differs from the last
    # appended one: O(n) time but O(n) extra space, which the problem forbids.
    # Or delete in place by shifting every later element left one slot: O(n^2).
    # Both miss the point — sortedness puts duplicates next to each other, so a
    # one-element memory of the past is enough.

    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Variant A — sorted linked list, keep one node per value.

        Time:  O(n) — every node is visited once; unlinking is O(1).
        Space: O(1) — one cursor, no new nodes.
        """
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next   # unlink, and STAY PUT: 1->1->1 needs a re-check
            else:
                cur = cur.next
        return head

    def removeDuplicates(self, nums: List[int]) -> int:
        """Variant B — sorted array, keep one copy. Returns the new length."""
        return self._compact(nums, keep=1)

    def removeDuplicatesII(self, nums: List[int]) -> int:
        """Variant C — sorted array, keep at most two copies. Returns the new length."""
        return self._compact(nums, keep=2)

    def _compact(self, nums: List[int], keep: int) -> int:
        """Keep at most `keep` copies of each value, in place. Returns the count.

        Time:  O(n) — one read pass; the write pointer never overtakes the read
               pointer, so nothing unread is ever clobbered.
        Space: O(1) — one index.

        Setting keep=1 recovers variant B, keep=2 gives variant C. That the same
        four lines answer both is the payoff of the episode.
        """
        slow = 0                           # how many elements we've decided to keep
        for value in nums:
            # Keep it if we haven't filled the quota yet, or if the element `keep`
            # positions back in the KEPT region is a different value.
            if slow < keep or value != nums[slow - keep]:
                nums[slow] = value
                slow += 1
        return slow


# ---------------------------------------------------------------- helpers
def build(values: List[int]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def flatten(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# ---------------------------------------------------------------- tests
LIST_CASES = [
    ([1, 1, 2], [1, 2]),
    ([1, 1, 2, 3, 3], [1, 2, 3]),
    ([1, 1, 1], [1]),                      # three in a row — breaks if you advance after unlinking
    ([1, 2, 3], [1, 2, 3]),                # no duplicates at all
    ([1], [1]),
    ([], []),
]

# (input, expected k, expected prefix) — the grader ignores whatever sits past k.
KEEP_ONE_CASES = [
    ([1, 1, 2, 2, 2, 3], 3, [1, 2, 3]),
    ([1, 1, 2], 2, [1, 2]),
    ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 5, [0, 1, 2, 3, 4]),
    ([1, 2, 3], 3, [1, 2, 3]),             # already unique
    ([7, 7, 7, 7], 1, [7]),                # all identical
    ([5], 1, [5]),
    ([], 0, []),
]

KEEP_TWO_CASES = [
    ([1, 1, 2, 2, 2, 3], 5, [1, 1, 2, 2, 3]),
    ([1, 1, 1, 2, 2, 3], 5, [1, 1, 2, 2, 3]),
    ([0, 0, 1, 1, 1, 1, 2, 3, 3], 7, [0, 0, 1, 1, 2, 3, 3]),
    ([1, 2, 3], 3, [1, 2, 3]),
    ([7, 7], 2, [7, 7]),                   # exactly at the quota
    ([], 0, []),
]


def test_linked_list():
    for values, want in LIST_CASES:
        got = flatten(Solution().deleteDuplicates(build(values)))
        assert got == want, f"{values} -> {got}, want {want}"


def test_array_keep_one():
    for values, want_k, want_prefix in KEEP_ONE_CASES:
        nums = list(values)
        k = Solution().removeDuplicates(nums)
        assert k == want_k, f"{values} -> k={k}, want {want_k}"
        assert nums[:k] == want_prefix, f"{values} -> {nums[:k]}, want {want_prefix}"


def test_array_keep_two():
    for values, want_k, want_prefix in KEEP_TWO_CASES:
        nums = list(values)
        k = Solution().removeDuplicatesII(nums)
        assert k == want_k, f"{values} -> k={k}, want {want_k}"
        assert nums[:k] == want_prefix, f"{values} -> {nums[:k]}, want {want_prefix}"
