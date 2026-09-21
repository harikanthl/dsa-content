# Pattern 08 — Stack

**9 episodes · EP 58–66**

---

## The one-sentence version

A stack holds **the things that are still unresolved, most recent first** — so any
question whose answer depends on the *nearest previous* item that hasn't been settled
yet is a stack problem, and because each element is pushed and popped at most once, the
whole thing is **O(n)** even when the code has a loop inside a loop.

## ELI5

A stack is a pile of plates: you can only see the top one, and that restriction is the
*feature*. It means the thing you can see is always the **most recent unfinished
business**.

```
text:   ( [ { } ]
stack:  (        <- still open
        ( [      <- still open, [ is more recent
        ( [ {    <- the { is the only thing } can possibly close
```

Two things happen at a stack, and every episode in this pattern is one of them:

| | what a push means | what a **pop** means | the answer is |
|---|---|---|---|
| **cancelling** | "unresolved so far" | the new item **annihilates** the top | what's **left on the stack** |
| **monotonic** | "still waiting for something bigger" | the new item **is** what the top was waiting for | recorded **at the moment of the pop** |

Cancelling stacks *build* the answer. Monotonic stacks are scaffolding — the answer is
written down during the pops and the stack itself is thrown away.

## How to recognise it

| Signal | Example |
|---|---|
| brackets, nesting, "valid" / "balanced" | Balanced Parentheses (EP59) |
| "remove adjacent …", "collapse", "cancel out" | Remove Adjacent Duplicates (EP58, EP64) |
| **"next greater / warmer / smaller"** | Next Greater Element (EP61), Daily Temperatures (EP62) |
| "how many days/steps until …" | Daily Temperatures (EP62) |
| a path, an expression, an undo history | Simplify Path (EP65) |
| "remove k things to make it smallest/largest" | Remove K Digits (EP66) |
| the word **most recent** appears in your own restatement | all nine |

**The tell for a monotonic stack specifically:** the problem asks, for every element, a
question about the first element to its right (or left) that beats it. The brute force
is a nested loop; the stack deletes the inner one.

## The shape — the cancelling stack

```python
stack = []
for item in sequence:
    if stack and cancels(stack[-1], item):
        stack.pop()             # the pair annihilates
    else:
        stack.append(item)      # unresolved: keep it
return stack                    # what survived IS the answer
```

## The shape — the monotonic stack

```python
stack = []                              # holds INDICES, usually
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:      # x beats what's on top
        j = stack.pop()
        answer[j] = ...                        # <- the pop is where the answer happens
    stack.append(i)
# anything still on the stack never found its answer -> the default
```

Four decisions, and writing them down before coding is the difference between fluency
and flailing:

| decision | ask |
|---|---|
| **increasing or decreasing?** | "next **greater**" → pop while the top is **smaller** → the stack stays decreasing |
| **index or value?** | need a **distance** → store the index (EP62). Only need the value → either (EP61) |
| **what happens at the pop?** | this is the answer being discovered: `answer[j] = x` or `i - j` |
| **what's left over?** | elements that never got popped → the default answer (`-1`, `0`, or they're the output) |

**Why it's O(n) despite the nested `while`:** every index is pushed exactly once and
popped at most once, so the total work in the inner loop across the whole run is at most
n. Say "amortised" out loud in the interview — it's the follow-up question, every time.

## The three things that go wrong

### 1. `<` vs `<=` — ties

`while stack and nums[stack[-1]] < x` leaves **equal** elements on the stack;
`<=` pops them. For "next strictly greater" you want `<`. For "next greater **or
equal**" you want `<=`. Nothing else in the code changes, and the two produce different
answers on any input with duplicates — so test with duplicates deliberately.

### 2. Popping an empty stack

`stack[-1]` on an empty stack raises. Every condition in this pattern starts with
`if stack and …` or `while stack and …`. In the bracket problems an empty stack at a
closing bracket isn't an error to guard against — it **is** the answer (`False`).

### 3. Confusing "what's left" with "what was popped"

At the end of a cancelling stack, the survivors are the answer. At the end of a
monotonic stack, the survivors are the *failures* — the elements that never found what
they were waiting for. EP66 is the episode where both matter at once: leftovers get
trimmed, and the pops were the greedy work.

## Complexity

| Problem | Time | Space |
|---|---|---|
| all nine episodes | O(n) | O(n) — the stack |
| EP61 (circular, two laps) | O(2n) = O(n) | O(n) |
| EP60 with two pointers | O(n) | **O(1)** — the episode about *not* using a stack |
| brute force you're beating | O(n²) | O(1) |

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 58 | Remove Adjacent Duplicates | cancelling | The stack IS the answer. One `if`. |
| 59 | Balanced Parentheses | cancelling | Match the top, and the three ways to be invalid. |
| 60 | Reverse a String | — | A stack works and is the wrong tool. O(n) vs O(1) space. |
| 61 | Next Greater Element II | monotonic | The template, plus a **circular** array: two laps. |
| 62 | Daily Temperatures | monotonic | Store **indices**, because the answer is a distance. |
| 63 | Remove Nodes From Linked List | monotonic | The stack's survivors are the output list. |
| 64 | Remove Adjacent Duplicates II | cancelling | Stack of `[char, count]` — compress the state. |
| 65 | Simplify Path | cancelling | Tokenise first; `..` pops, `.` and `''` are noise. |
| 66 | Remove K Digits | monotonic + greedy | A pop budget, leftover k, and leading zeros. |

## What "knowing this in your sleep" means

1. What does the top of the stack mean in this problem? *(Always answer this before
   writing code. "The most recent X that hasn't been resolved yet.")*
2. Increasing or decreasing, and why? *("Next greater" pops smaller elements, so what
   remains is decreasing.)*
3. Index or value? *(Index whenever the answer involves a distance or you need to write
   into an answer array.)*
4. Why is it O(n) with a `while` inside a `for`? *(Each element is pushed once and
   popped at most once — amortised O(1) per element.)*
5. What do the leftovers mean? *(Cancelling: they're the answer. Monotonic: they never
   found their match, so they take the default.)*
