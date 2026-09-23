# EP097 · P11E04 · Top K Frequent Words   [Medium]

**Pattern:** Heap (top-k) · **Link:** https://leetcode.com/problems/top-k-frequent-words/description/

---

## 🎬 Hook
> "Yesterday's problem with two new rules: ties go **alphabetically**, and the output has
> to be **in order**. One tuple, `(-freq, word)`, handles both at once, and the reason it
> works is the reason you can't always do this trick."

## 📋 Problem, in your words
```
Given a list of words and k, return the k most frequent words.

  - sorted by frequency, highest first
  - equal frequency -> alphabetical (lexicographical) order
  - the ORDER of the output matters this time
```

## 🔢 The example
```
Input:  words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2
Output: ["i", "love"]
Why:    "i" and "love" both appear twice; "i" < "love" alphabetically

Input:  words = ["b", "a", "c", "b", "a", "d"], k = 3
Output: ["a", "b", "c"]
Why:    a:2, b:2 tie -> a first. c:1, d:1 tie for 3rd -> c wins.
```

## 🧸 ELI5
> A spelling bee leaderboard. Most points on top. When two kids have the same points,
> the one whose name comes first in the **dictionary** goes higher.
>
> You write each kid on a card as **(minus points, name)**. Why minus? Because the pile
> always gives you the **smallest** card first, and "-2" is smaller than "-1", so the
> kid with **more** points comes out first. The name you leave alone, because "a" is
> already smaller than "b", which is exactly the tie order you want.
>
> ```
> cards:   (-2, a)  (-2, b)  (-1, c)  (-1, d)
> pile hands them out:  (-2, a)  (-2, b)  (-1, c)  | stop at k = 3
> ```
>
> One card design, both rules obeyed, no extra sorting.

## 🐌 Brute force (say it, don't type it)
Count, then `sorted(count, key=lambda w: (-count[w], w))[:k]`. **O(n + u log u)**. It's
short and correct, and interviewers accept it as a first answer. The heap version is
the one that doesn't order all u words to get k of them.

## 💡 The pattern reveal
**Signal:** "k most frequent" + "**ties** by alphabetical order" + "**sorted** output".
**Therefore:** count (Pattern 9), then top-k with the tie-break **inside the tuple**.

**Key insight:** make one key where "smaller" means "better", and both rules are the
same comparison:

| rule | wanted order | key part | why |
|---|---|---|---|
| frequency | high first | `-freq` | negate so high freq is small |
| tie | a before b | `word` | strings already sort ascending |

`(-freq, word)` in a **min-heap**: pop k times and the words come out in exactly the
required output order. No reverse, no second sort.

**🧨 The trap.** The EP95 bounded-heap shape (size k, evict the weakest) needs the
*weakest* on top: lowest freq, then **alphabetically last**. That's `(freq, reversed
word)`, and **you can't negate a string**. The pattern card's gotcha #2. So either
heapify everything and pop k (below), or write a wrapper class with `__lt__` (in the
talking points).

## 🔍 Dry run: `words = ["b", "a", "c", "b", "a", "d"]`, `k = 3`

Count: `{b: 2, a: 2, c: 1, d: 1}`. Keys: `(-2,'b') (-2,'a') (-1,'c') (-1,'d')`.
`heapify` → top is `(-2, 'a')`.

| pop # | popped | why it's the smallest key | output so far |
|---|---|---|---|
| 1 | (-2, 'a') | -2 is the lowest; among the two -2s, 'a' < 'b' | `[a]` |
| 2 | (-2, 'b') | the other -2 | `[a, b]` |
| 3 | (-1, 'c') | -1 ties with d; 'c' < 'd' | `[a, b, c]` |

Stop at k = 3. Answer **`["a", "b", "c"]`** ✓. `(-1, 'd')` is never popped.

## ✅ Optimal solution
```python
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        """k most frequent words, by frequency desc then alphabetically.

        Time:  O(n + u + k log u), count, heapify all u keys in O(u), pop k.
        Space: O(u).
        """
        count = Counter(words)

        # smaller key = better word: high freq first (negated), then a before b
        heap = [(-freq, word) for word, freq in count.items()]
        heapq.heapify(heap)                 # O(u), not O(u log u)

        return [heapq.heappop(heap)[1] for _ in range(k)]
```
**Time:** O(n + u + k log u) · **Space:** O(u)

## ⚠️ Gotchas
- **Negate the count, not the word.** `(freq, word)` gives the *least* frequent first.
  `(-freq, -word)` is a `TypeError`.
- **`heapify` is O(u).** Say it. Building by u pushes would be O(u log u), which is no
  better than sorting.
- **Output order matters.** Yesterday's "any order" answer read the heap's array
  directly. Here you must **pop**, because the heap array itself isn't sorted.
- **Tie at the k-th place is real.** `c` and `d` both have 1. The second example is
  there to test it; use it on camera.
- **Uppercase sorts before lowercase** in Python string order. LeetCode guarantees
  lowercase; mention it if asked about general input.

## 🎤 Interview talking points
- *"Count, then a min-heap keyed on `(-freq, word)`: one key where smaller means better,
  so popping gives the output order directly."*
- *"O(n + u + k log u) using `heapify`, which is linear."*
- *"The follow-up is O(n log k) with a size-k heap. That needs the weakest on top:
  lowest freq, then alphabetically **last**. I can't negate a string, so I'd wrap it:"*
  ```python
  class WordFreq:
      def __init__(self, freq, word): self.freq, self.word = freq, word
      def __lt__(self, other):          # "less" = weaker = evicted first
          if self.freq != other.freq:
              return self.freq < other.freq
          return self.word > other.word  # later in the alphabet is weaker
  ```
  *"then push, trim at k, pop everything, and reverse."*
- *"Tuples compare element by element, so the tie-break is free as long as every element
  is comparable."*

## 🔗 Transfer
That's the top-k family done: EP94/95 raw values, EP96/97 counted values with tie-breaks.
Tomorrow (EP98, K Closest Points) the key isn't a count any more, it's a **distance**
you compute per item, and the heap flips back to a max-heap because you evict the
farthest.

## 📹 Metadata
- **Title:** `Top K Frequent Words, one tuple, two rules | Heap #4`
- **Thumbnail:** `(-freq, word)` (green block)
- **Short:** the spelling-bee cards coming off the pile in order, then `-word` crashing.
  45s.
