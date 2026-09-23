# EP171 · P14E20 · Word Ladder   [Hard]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/word-ladder/

---

## 🎬 Hook
> "Turn `hit` into `cog`, one letter at a time, every step a real word. There's no graph
> in the input. There's a list of words. The moment you see that **words are nodes and
> one-letter changes are edges**, it's shortest path in an unweighted graph: EP163.
> The only hard part is finding the neighbours without comparing every pair, and one
> little `*` does that."

## 📋 Problem, in your words
```
Given beginWord, endWord and a wordList (all the same length, lowercase),
return the number of WORDS in the shortest sequence
    beginWord -> w1 -> w2 -> ... -> endWord
where each step changes exactly one letter and every wi is in wordList.

  - beginWord does not need to be in wordList; endWord does
  - return 0 if no such sequence exists
```

## 🔢 The example
```
beginWord = "hit", endWord = "cog"
wordList  = ["hot", "dot", "dog", "lot", "log", "cog"]

    hit -- hot -- dot -- dog -- cog
             \     |      |    /
              \    |      |   /
               - lot -- log -

Output: 5       <- hit -> hot -> dot -> dog -> cog   (5 words, 4 changes)

Same, but wordList without "cog"   ->   0     <- the end isn't a valid word
```

## 🧸 ELI5
> Every word is a stepping stone. You can hop between two stones if their words differ
> in exactly one letter. What's the fewest stones to walk from `hit` to `cog`?
>
> That's "fewest steps", so it's BFS: check everything 1 hop away, then 2 hops, and so
> on. The trouble is finding which stones are 1 hop away. Comparing a word to all 5,000
> others, letter by letter, is slow.
>
> The trick: give every word a few **nicknames** with one letter blanked out.
>
> ```
> hot  ->  *ot   h*t   ho*
> dot  ->  *ot   d*t   do*
> lot  ->  *ot   l*t   lo*
> ```
>
> Now put words in buckets by nickname. Everyone in the `*ot` bucket differs from each
> other by exactly the first letter, so they're all neighbours. To find `hot`'s
> neighbours, just look in its three buckets.

## 🐌 Brute force (say it, don't type it)
Build the graph explicitly: compare every pair of words, add an edge if they differ in
one letter. **O(N² · L)** to build, for N words of length L: with N = 5000 that's 25
million comparisons before the BFS starts. The other brute force, trying all 26 letters
at every position and checking the set, is **O(N · L · 26 · L)**, which is fine too and
worth mentioning. The bucket method is **O(N · L²)** and never touches a non-neighbour.

## 💡 The pattern reveal
**Signal:** "shortest transformation sequence", each step a small edit, nodes you have
to generate.
**Therefore:** Shape C: BFS on an **implicit graph**.

**Key insight:** two words are neighbours iff they share a **wildcard pattern** (the word
with one position replaced by `*`). So the buckets *are* the adjacency list, built in
O(N · L²) without ever comparing two words.

```python
buckets = defaultdict(list)
for w in wordList:
    for i in range(L):
        buckets[w[:i] + '*' + w[i+1:]].append(w)
# neighbours of w: every word in buckets[w[:i] + '*' + w[i+1:]] for each i
```

Then it's EP163 exactly: a queue of `(word, length)`, a `seen` set marked at push, and
return the length when `endWord` is popped.

## 🔍 Dry run: `hit → cog`
Buckets that matter: `h*t: [hot]`, `*ot: [hot, dot, lot]`, `do*: [dot, dog]`,
`lo*: [lot, log]`, `*og: [dog, log, cog]`, ...

| step | pop (length) | patterns checked → new words | queue after |
|---|---|---|---|
| 1 | `hit` (1) | `*it` -, **`h*t` → hot**, `hi*` - | `[hot 2]` |
| 2 | `hot` (2) | **`*ot` → dot, lot**, `h*t` (emptied), `ho*` - | `[dot 3, lot 3]` |
| 3 | `dot` (3) | `*ot` (emptied), `d*t` -, **`do*` → dog** | `[lot 3, dog 4]` |
| 4 | `lot` (3) | `*ot` (emptied), `l*t` -, **`lo*` → log** | `[dog 4, log 4]` |
| 5 | `dog` (4) | **`*og` → cog** (log already seen), `d*g` -, `do*` (emptied) | `[log 4, cog 5]` |
| 6 | `log` (4) | `*og` (emptied), `l*g` -, `lo*` (emptied) | `[cog 5]` |
| 7 | `cog` (5) | **it's the end word → return 5** | |

Answer **5** ✓. "(emptied)" is the optimisation in the code: once a bucket has been
used, every word in it is already seen, so we clear it and never scan it again.

## ✅ Optimal solution
```python
from collections import defaultdict, deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        """Words in the shortest one-letter-at-a-time chain, or 0 if none exists.

        Time:  O(N * L^2), N*L patterns, each built in O(L); every bucket scanned once.
        Space: O(N * L^2), the buckets hold N*L patterns of length L.
        """
        if endWord not in wordList:
            return 0
        L = len(beginWord)

        buckets = defaultdict(list)                     # pattern -> words matching it
        for w in wordList:
            for i in range(L):
                buckets[w[:i] + '*' + w[i+1:]].append(w)

        seen = {beginWord}
        q = deque([(beginWord, 1)])                     # (word, words in chain so far)
        while q:
            word, length = q.popleft()
            if word == endWord:
                return length
            for i in range(L):
                pattern = word[:i] + '*' + word[i+1:]
                for nxt in buckets[pattern]:
                    if nxt not in seen:
                        seen.add(nxt)                   # mark at push
                        q.append((nxt, length + 1))
                buckets[pattern] = []                   # used up: never scan it again
        return 0
```
**Time:** O(N · L²) · **Space:** O(N · L²)

## ⚠️ Gotchas
- **Count words, not steps.** `hit → hot → dot → dog → cog` is 4 changes and **5**
  words. Start the length at 1, not 0.
- **`endWord` not in the list → 0**, checked up front. Without the check BFS still
  returns 0, but only after exploring every reachable word first.
- **`beginWord` may not be in `wordList`.** Don't rely on it having buckets; it only needs
  to generate patterns, which it does from its own letters.
- **`seen` at push time.** Same as every BFS: mark late and the queue fills with
  duplicates, which with thousands of words is a TLE.
- **Clear used buckets.** Without it, a big bucket like `*ot` is rescanned by every word
  in it: correct, but it can push the time towards O(N²).
- **`wordList` is a list.** `endWord not in wordList` is O(N) once, fine. Don't do
  `in wordList` inside the loop.
- **Bidirectional BFS** (grow from both ends, always expand the smaller frontier) is the
  standard speed-up. Mention it; don't lead with it.

## 🎤 Interview talking points
- *"Words are nodes, one-letter changes are edges, all edges cost 1: shortest path in an
  unweighted graph, so BFS."*
- *"I never build the edges. I bucket words by wildcard pattern, like `h*t`, and a word's
  neighbours are whatever shares one of its L patterns."* ← the insight.
- *"O(N · L²) to build buckets, and BFS touches each bucket once if I clear them after
  use."*
- *"Bidirectional BFS roughly square-roots the search space; that's the follow-up."*
- *"Word Ladder II wants all shortest paths: BFS to build parent links by level, then
  backtrack from the end."*

## 🔗 Transfer
The pattern ends where it started: BFS from EP154, `dist + 1` from EP163. What's new is
that the graph was never given, you **generated** it, and that's the step that separates
graph problems in the wild from graph problems in textbooks. Open Lock (LeetCode 752),
Minimum Genetic Mutation (433) and Sliding Puzzle (773) are this exact code with a
different neighbour generator. Next up is Pattern 15, DP, where EP169's "best using at
most `i` of something" becomes the whole idea.

## 📹 Metadata
- **Title:** `Word Ladder, the graph you never build | Graphs #20 (finale)`
- **Thumbnail:** `h*t` (purple block)
- **Short:** `hot`, `dot`, `lot` dropping into the `*ot` bucket, then BFS lighting up
  hit → hot → dot → dog → cog. 45s.
