# Pattern 12 — Recursion and Backtracking

**10 episodes · EP 111–120**

---

## The one-sentence version

Recursion is a function that **trusts a smaller call of itself** and does one step of
work on top; backtracking is recursion that **makes a choice, recurses, then undoes the
choice** — one `path` list walks every branch of a decision tree, and the leaves are
the answers.

## ELI5

You're exploring a hedge maze with a piece of chalk.

At every fork you pick a corridor and **draw a chalk line** into it. Dead end? Walk back
to the fork, **rub out the line**, try the next corridor. Reach an exit? The chalk trail
behind you *is* the route — copy it into your notebook, rub it out, keep looking.

```
                 start
               /   |   \
             L     M     R
            / \    |    / \
          LL  LR  ML  RL  RR
          x   ✓   x   ✓   x        ✓ = a leaf that is an answer
```

The trail is `path`. Drawing a line is *choose*. Walking the corridor is *explore* (the
recursive call). Rubbing it out is *unchoose*. You own one piece of chalk and one
trail — the maze is explored by **reusing** it, not by copying it down every branch.

Plain recursion is the same maze with **one corridor** at every fork: nothing to undo,
you just walk (EP111–115). Backtracking is when the forks appear (EP116–120).

## How to recognise it

| Signal | Example |
|---|---|
| **"all"** combinations / permutations / subsets / partitions | Permutations (EP118), Palindrome Partitioning (EP120) |
| "generate every **valid** …" | Generate Parentheses (EP116) |
| digits / letters that each **map to choices** | Letter Combinations (EP117) |
| "all ways to reach a target", and they want the ways | Combination Sum (EP119) |
| **small n** in the constraints — n ≤ 8, ≤ 16, ≤ 20 | every backtracking episode |
| the problem is defined by a **smaller version of itself** | Fibonacci (EP111), Sum of Digits (EP114) |

**The small-n tell.** `1 <= n <= 8` means the answer set is exponential and enumerating
it is *expected*. `n <= 10^5` means it isn't, and this is the wrong tool.

**The anti-signal:** if the question asks **how many** ways, or for the **best** way,
rather than for the list, that's Dynamic Programming (Pattern 15). Same decision tree,
but you never need the leaves — you need a number about them, and numbers can be cached.
Combination Sum (EP119) wants the combinations; Combination Sum IV wants the count and
is DP. Read which one you've been handed.

## Shape A — plain recursion (one smaller call)

```python
def sum_of_digits(n):
    if n < 10:                              # base case: answer it by looking
        return n
    return n % 10 + sum_of_digits(n // 10)  # one step of work + trust the smaller call
```

| line | question it answers |
|---|---|
| **base case** | what is the smallest input, and its answer *without recursing*? |
| **the smaller call** | how does the answer for `n` follow from a smaller answer? |

**The leap of faith.** Do not trace into `sum_of_digits(n // 10)`. Assume it returns
the right digit sum of the smaller number — if the function is correct, it does. Your
only job: given that, is `n % 10 + that` right? Yes. Done. People who follow the
recursion all the way down in their head get lost at depth three.

The trace exists so you believe the leap once and never need it again:

```
sum_of_digits(345)
  = 5 + sum_of_digits(34)
  = 5 + (4 + sum_of_digits(3))
  = 5 + (4 + 3)              <- base case; the stack starts unwinding
  = 12
```

Each indented line is a **stack frame** — which is why a recursion n deep costs O(n)
space even when it allocates nothing. EP111–115 are this shape with different base
cases: `fib` has *two* smaller calls (that's what makes it 2ⁿ without memoisation),
palindrome (EP112) shrinks from both ends, remove-char (EP115) builds the result on the
way back up.

## Shape B — backtracking

```python
def backtrack(path, state):
    if is_complete(path):
        results.append(path[:])          # COPY — see "what goes wrong" #1
        return
    for choice in available(state):
        if not allowed(choice):          # prune BEFORE descending
            continue
        path.append(choice)              # choose
        backtrack(path, next_state)      # explore
        path.pop()                       # unchoose — restore for the next sibling
```

Say the three verbs as you type them: **choose, explore, unchoose.** The `append` and
the `pop` bracket the recursive call like `(` and `)`.

Generate Parentheses, n = 2 — each level adds one character:

```
                 ""
                 |
                "("            <- ")" is never tried: close would exceed open
              /      \
           "(("      "()"      <- "(((" is never tried: open would exceed n
            |          |
          "(()"      "()("
            |          |
         "(())"     "()()"     <- leaves: both are answers
```

The branches that **don't exist** are the pruning conditions (`open < n`,
`close < open`), and they're why this runs in Catalan time rather than 4ⁿ. A
backtracker without pruning is brute force written recursively.

### The four flavours

Every one of EP116–120 is the template with a different `available()` and
`is_complete()`.

**1. Build by position (EP116, EP117).** Fixed target length; at depth `i` choose the
character for position `i`. `available()` is a lookup: `keypad[digits[i]]`.

**2. Permutations (EP118).** Every element once, order matters. Track what's used:

```python
for i, x in enumerate(nums):
    if i in used: continue
    used.add(i); path.append(x)
    permute(path, used)
    path.pop(); used.discard(i)          # undo BOTH pieces of state
```

**3. Combinations with a `start` index (EP119).** Order doesn't matter, so `[2,3]` and
`[3,2]` are one answer. Only consider candidates at or after `start`:

```python
for i in range(start, len(cands)):
    if cands[i] > remaining: break       # sorted input -> prune the rest
    path.append(cands[i])
    combo(path, i, remaining - cands[i]) # i: reuse allowed.  i + 1: each used once
    path.pop()
```

That `i` vs `i + 1` is the entire difference between Combination Sum and Combination
Sum II.

**4. Partitioning a string (EP120).** The choice is *where to cut next*. Try every
prefix of what's left; if it qualifies, commit it and recurse on the suffix:

```python
for end in range(start + 1, len(s) + 1):
    if is_pal(s[start:end]):             # the check IS the prune
        path.append(s[start:end]); partition(path, end); path.pop()
```

## The three things that go wrong

### 1. `results.append(path)` instead of `results.append(path[:])`

`path` is one list, mutated for the whole run. Append it without copying and every
result is a reference to **the same list**, which by the end is empty. You get
`[[], [], [], []]` and no error. Use `path[:]`, or `''.join(path)` for strings. This
bites people who *know about it*.

### 2. Forgetting to undo — or undoing only half

If you mutated two things before the call (`path` and `used`, or a visited cell and a
budget), you restore two things after. Miss one and sibling branches see a polluted
world: skipped answers or duplicates. The alternative that can't forget is passing new
state instead of mutating (`build(path + [ch], i + 1)`) — an O(n) copy per node, usually
fine at these sizes. Know both; say why you picked one.

### 3. No pruning, or pruning at the leaf

`open < n` and `close < open` (EP116), `cands[i] > remaining: break` (EP119) — these
belong **before** the recursive call. Checking validity at the leaf still visits every
dead branch all the way down. Put the check where the corridor starts, not at its end.

## Complexity

The honest answer is "number of leaves × cost of copying one", and the leaf count is a
property of the problem, not the code.

| Problem | Time | what `n` is |
|---|---|---|
| Sum of Digits (EP114) | O(d) | d = digits; O(d) stack |
| Fibonacci, naive (EP111) | O(2ⁿ) | the input; Pattern 15 fixes this |
| Generate Parentheses (EP116) | O(4ⁿ / √n) — Catalan | pairs of brackets |
| Letter Combinations (EP117) | O(n · 4ⁿ) | number of digits |
| Permutations (EP118) | O(n · n!) | length of the array |
| Combination Sum (EP119) | O(n^(T/m)) | T = target, m = smallest candidate |
| Palindrome Partitioning (EP120) | O(n · 2ⁿ) | length of the string |

Space is O(depth) for the stack plus `path`, **excluding the output**. Say "excluding
the output" out loud; the output alone is exponential and the interviewer knows it.

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 111 | Fibonacci | plain recursion | Two base cases, two smaller calls, and why that's 2ⁿ. |
| 112 | Check if String is Palindrome | plain recursion | Shrink from both ends; base case is length ≤ 1. |
| 113 | Check if Array is Sorted | plain recursion | Compare one pair, trust the rest. |
| 114 | Sum of Digits | plain recursion | The stack-frame trace, done once. |
| 115 | Remove Occurrences of a Character | plain recursion | Building the result on the way **back up**. |
| 116 | Generate Parentheses | build-by-position | The template, the tree, and pruning with `open < n`, `close < open`. |
| 117 | Letter Combinations of a Phone Number | build-by-position | Same template; a lookup table supplies the choices. |
| 118 | Permutations | permutations | A `used` set and undoing **two** pieces of state. |
| 119 | Combination Sum | combinations | `start` kills duplicates; `i` vs `i + 1` decides reuse. |
| 120 | Palindrome Partitioning | partitioning | The choice is a cut point; the validity check *is* the prune. |

## What "knowing this in your sleep" means

1. What is the base case, and what is the one smaller call? *(Answer both before
   writing anything. If you can't state the base case you don't understand the problem.)*
2. What does `path` hold at depth d, and when is it complete? *(A partial answer of
   length d; complete at the target length, target sum, or end of input.)*
3. Where are the three verbs? *(Choose, explore, unchoose — the `append` and `pop`
   bracketing the call, plus every other piece of state you touched.)*
4. Why `path[:]` and not `path`? *(One list is reused for the whole search; without a
   copy every result aliases the same soon-to-be-empty list.)*
5. What prunes the tree, and is it **before** the recursive call? *(Name the condition.
   Without it you've written brute force with extra stack frames.)*
6. Permutation, combination, or partition — so `used`, `start`, or a cut index?
   *(Order matters → `used`. Order doesn't → `start`. Choosing where to split → cut.)*
7. Why is this recursion and not DP? *(They want the list, not a count or an optimum.
   The moment they want a number, go to Pattern 15.)*
