# EP024 · P03E04 · Fruits into Baskets   [Medium]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/fruit-into-baskets/

---

## 🎬 Hook
> "This problem is about fruit trees and baskets and a farmer. It is also, word for
> word, yesterday's problem with k set to 2. The skill today isn't solving it — it's
> *seeing* it. Interviewers dress problems in stories precisely to find out whether
> you recognise the shape underneath."

## 📋 Problem, in your words
```
A row of fruit trees; fruits[i] is the type of fruit on tree i.

You have two baskets, and each basket holds only ONE type of fruit.
You must pick from every tree you pass, starting anywhere, and you stop
the moment you reach a tree whose fruit fits in neither basket.

Return the maximum number of fruits you can pick.
```

**Translated:** find the longest contiguous subarray containing at most **2 distinct**
values. That's the whole problem. Say the translation out loud on camera before you
write a line — that act *is* the episode.

## 🔢 The example
```
Input:  fruits = [1, 2, 1]
Output: 3        (two types, so the whole row works)

Input:  fruits = [0, 1, 2, 2]
Output: 3        ([1,2,2] -- types {1,2}. Starting at 0 would need three baskets.)

Input:  fruits = [1, 2, 3, 2, 2]
Output: 4        ([2,3,2,2] -- types {2,3})
```

## 🧸 ELI5
> Walk down a row of trees with two baskets. Each basket can only ever hold one kind
> of fruit.
>
> You keep picking as you walk. The moment you meet a **third** kind, you're stuck — so
> you pretend you'd started further along: drop trees from the back of your walk until
> only two kinds remain.
>
> "How many fruits did I carry?" is "how long was my walk?"

## 🐌 Brute force (say it, don't type it)
Try every starting tree; walk forward with a set of types; stop at the third type.
**O(n²).** Exactly the waste from EP23 — every restart rebuilds a window that was
nearly identical to the last one.

## 💡 The pattern reveal
**Signal:** contiguous run · longest · "at most 2 kinds" wearing a costume.
**Therefore:** Sliding Window, Shape B — literally EP23 with `k = 2`.

**Key insight — the transferable one:** *"two baskets, one type each"* is a paraphrase
of *"at most 2 distinct values."* The moment you translate the story into that
sentence, you already have the code from yesterday.

**How to spot a costume,** as a habit worth naming on camera:

| Story says | It means |
|---|---|
| "two baskets, one fruit type each" | at most 2 distinct |
| "you must pick from every tree you pass" | the subarray is **contiguous** |
| "you stop at a tree you can't pick" | the window's validity condition |
| "maximum fruits" | longest window |

Every phrase in the story maps to a piece of machinery. Doing this translation out
loud, line by line, is the most useful interview habit in this whole pattern.

## 🔍 Dry run — `fruits = [1, 2, 3, 2, 2]`
| hi | fruit | counts | kinds | action | window | best |
|---|---|---|---|---|---|---|
| 0 | 1 | `{1:1}` | 1 | ok | `[1]` | 1 |
| 1 | 2 | `{1:1,2:1}` | 2 | ok | `[1,2]` | 2 |
| 2 | 3 | `{1:1,2:1,3:1}` | 3 ✗ | drop `1` → `{2:1,3:1}` ✓ | `[2,3]` | 2 |
| 3 | 2 | `{2:2,3:1}` | 2 | ok | `[2,3,2]` | 3 |
| 4 | 2 | `{2:3,3:1}` | 2 | ok | `[2,3,2,2]` | **4** |

Return **4**.

## ✅ Optimal solution
```python
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        """Longest contiguous run containing at most 2 distinct values.

        Time:  O(n) amortised — lo only moves forward.
        Space: O(1) — the counter holds at most 3 keys, a constant.
        """
        counts: Dict[int, int] = defaultdict(int)
        lo = 0
        best = 0

        for hi, fruit in enumerate(fruits):
            counts[fruit] += 1                  # pick from this tree

            while len(counts) > 2:              # a third type -- start later
                left = fruits[lo]
                counts[left] -= 1
                if counts[left] == 0:
                    del counts[left]            # that type is fully out of the window
                lo += 1

            best = max(best, hi - lo + 1)

        return best
```
**Time:** O(n) · **Space:** O(1) — note it's O(1) here, not O(k): the map never exceeds
3 keys because k is a literal 2. Saying that precisely is a small, real signal.

### Write it generically, then call it
```python
def longest_at_most_k_distinct(values, k): ...   # EP23, unchanged
def totalFruit(self, fruits): return longest_at_most_k_distinct(fruits, 2)
```
Doing this on camera is the whole point of the episode: **one function, two problems.**
In an interview, saying *"this is the at-most-k-distinct problem with k=2, here's the
general version"* is stronger than solving it in isolation, because it tells the
interviewer you'd recognise the third costume too.

## ⚠️ Gotchas
- **`del` at zero**, exactly as in EP23. Leaving zero-count keys makes `len(counts)`
  permanently wrong.
- **Don't hand-roll two variables for the two basket types.** `basket1`, `basket2`,
  `count1`, `count2` plus "which one do I evict" is genuinely fiddly and breaks on
  `[1,1,2,2,1]`-style inputs. The dictionary is shorter *and* correct.
- **You pick from every tree you pass** — the run is contiguous. If it were "choose any
  trees," this would be a counting problem, not a window one.
- A single tree, or all trees the same type, returns `len(fruits)` with no special
  casing.
- The values are arbitrary integers, not characters — nothing changes, but don't
  assume a 26-slot array.

## 🎤 Interview talking points
- *"This is 'longest subarray with at most k distinct values' with k = 2. I'd write the
  general version and call it with 2."*
- *"Space is O(1) rather than O(k) because k is fixed at 2 — the map holds at most
  three keys."*
- *"If they later asked for three baskets, I'd change one argument."* ← that sentence
  is the payoff of writing it generically.

## 🔗 Transfer
The habit is the transfer: **translate the story into the constraint before you code.**
It comes back immediately — EP27 (Longest Subarray with Ones after Replacement) is
"flip at most k zeros," which is a costume for a window condition too, and EP29's
"contains all characters of t" is the hardest costume in the pattern.

## 📹 Metadata
- **Title:** `Fruit Into Baskets — it's the k-distinct problem in a costume | Sliding Window #4`
- **Thumbnail:** `SAME PROBLEM, NEW STORY` (amber block)
- **Short:** The story-to-constraint translation table, read aloud line by line, 40s.
