"""
EP011 · P01E11 · Comparing Strings containing Backspaces   [Medium]
Pattern: Two Pointers
Prep:    prep/01-two-pointers/11-comparing-strings-containing-backspaces.md
Link:    https://leetcode.com/problems/backspace-string-compare/

Run:  dsa test 11         (or)  pytest problems/01-two-pointers/11_comparing_strings_containing_backspaces.py -q
"""


class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        """Compare two strings once '#' is applied as a backspace.

        Time:  O(n + m) — each index in each string is visited once.
        Space: O(1) — two cursors and two skip counters. No rebuilt strings.
        """
        # --- brute force (say it out loud, then discard) -------------------
        # O(n + m) time but O(n + m) space: push characters onto a stack, pop on
        # '#', compare the stacks. Perfectly correct, and the answer most people
        # give. The follow-up is always "now do it in O(1) space", and the fix is
        # to walk BACKWARDS — from the right, a '#' tells you what to delete next,
        # whereas from the left you can't know if a character survives until later.
        #
        # --- optimal ------------------------------------------------------
        i, j = len(s) - 1, len(t) - 1
        skip_s = skip_t = 0

        while i >= 0 or j >= 0:                  # OR, not AND: one string may be longer
            # Walk each cursor back to the next character that actually survives.
            while i >= 0:
                if s[i] == '#':                  # bank a deletion
                    skip_s += 1
                    i -= 1
                elif skip_s > 0:                 # spend a banked deletion
                    skip_s -= 1
                    i -= 1
                else:
                    break                        # s[i] survives
            while j >= 0:
                if t[j] == '#':
                    skip_t += 1
                    j -= 1
                elif skip_t > 0:
                    skip_t -= 1
                    j -= 1
                else:
                    break

            if i >= 0 and j >= 0:                # both have a survivor: compare them
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:               # one ran out and the other didn't
                return False                     # this is the length check — easy to forget

            i -= 1
            j -= 1

        return True


# ---------------------------------------------------------------- tests
CASES = [
    (("ab#c", "ad#c"), True),          # both reduce to "ac"
    (("ab##", "c#d#"), True),          # both reduce to ""
    (("a#c", "b"), False),
    (("a##c", "#a#c"), True),
    (("bxj##tw", "bxo#j##tw"), True),
    (("bxj##tw", "bxj###tw"), False),
    (("nzp#o#g", "b#nzp#g"), True),
    (("", ""), True),                  # both empty
    (("#", ""), True),                 # backspace on empty does nothing
    (("a", "ab"), False),              # the OR guard: AND would wrongly say True
    (("ab", "a"), False),              # same, other way round
    (("a#", "b#"), True),              # both delete their only character
    (("xywrrmp", "xywrrmu#p"), True),
]


def test_cases():
    for args, want in CASES:
        got = Solution().backspaceCompare(*args)
        assert got == want, f"{args} -> {got}, want {want}"


def test_matches_the_stack_oracle():
    # The O(n) space version, used as the oracle — and exhaustively, over every
    # short string of {a, b, #}, which is where the length-check bug hides.
    import itertools

    def apply(text: str) -> str:
        out = []
        for ch in text:
            if ch == '#':
                if out:
                    out.pop()
            else:
                out.append(ch)
        return "".join(out)

    alphabet = "ab#"
    strings = [""] + ["".join(p)
                      for length in range(1, 4)
                      for p in itertools.product(alphabet, repeat=length)]
    for s in strings:
        for t in strings:
            got = Solution().backspaceCompare(s, t)
            assert got == (apply(s) == apply(t)), f"({s!r}, {t!r}) -> {got}"
