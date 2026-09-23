# Pattern 09 — Hash Maps

**4 episodes · EP 67–70**

---

## The one-sentence version

When the question is about **how many of each thing** there are — and not about where
they sit — count everything once into a dictionary and then **interrogate the counts**
instead of the input: the nested "for every x, scan for x" loop becomes one pass and one
lookup, **O(n²) → O(n)**.

## ELI5

You're sorting a bag of coloured beads. Someone asks: is there a colour that appears
exactly once? How many complete rainbows can you make? Can you build this necklace from
what's in the bag?

The slow way is to answer each question by picking up a bead and rummaging through the
whole bag looking for its twins, for every bead.

The fast way: tip the bag onto the table and **sort into piles by colour**. Now every
question is a question about the piles, not the beads.

```
"balloon" from "loonbalxballpoon"

pile:   a b l o n x
count:  2 2 4 4 2 1

one "balloon" needs:  a=1 b=1 l=2 o=2 n=1
how many can I make?  a:2/1=2  b:2/1=2  l:4/2=2  o:4/2=2  n:2/1=2  -> 2
```

Every episode in this pattern is: **build the piles in one pass, then ask the piles
something.** The only things that vary are *what you ask* and whether the *original
order* still matters afterwards.

## How to recognise it

| Signal | Example |
|---|---|
| "first / any character that appears **exactly once**" | First Non-repeating Character (EP67) |
| "how many times can you **form / spell** X from Y" | Maximum Number of Balloons (EP68) |
| "longest palindrome you can **build** from these letters" | Longest Palindrome (EP69) |
| "can A be **constructed from** B" — a multiset covers another | Ransom Note (EP70) |
| the words **count**, **frequency**, **occurrences**, **anagram** | all four |
| the alphabet is small and fixed (26 letters) | all four — an array of 26 works too |

**The anti-signal:** if the answer depends on a *contiguous* run, counting alone loses
that — you're in Sliding Window (Pattern 03) with a counter as the bookkeeping. And
"pair that sums to target" on unsorted input is a hash map keyed **value → index**, not
a count; this card is the frequency half of the family.

**Contrast with Two Pointers.** Two pointers needs sorted input to eliminate candidates.
A hash map doesn't care about order — it trades O(n) memory for never sorting. If you're
about to sort just to count runs of equal things, stop: a `Counter` does it in O(n).

## The shape

### Shape A — Count, then interrogate the counts

```python
from collections import Counter

counts = Counter(s)                 # one pass over the input
# ...every question after this is about `counts`, never about `s`
return min(counts[ch] // need[ch] for ch in need)     # EP68
```

`Counter` is a `dict` whose missing keys read as `0` instead of raising. That single
property is why the rest of the code has no `if ch in counts` guards.

### Shape B — Count, then walk the ORIGINAL again in order

```python
counts = Counter(s)                 # pass 1: how many of each
for i, ch in enumerate(s):          # pass 2: in the input's order
    if counts[ch] == 1:
        return i                    # the FIRST one, because we walk s not counts
return -1
```

Two passes, both O(n). The second one is over `s`, not over `counts`, because a
dictionary remembers *how many* but the question asked *which comes first*. The
input is the only thing that knows the order.

**Why not one pass?** You can't know a character is non-repeating until you've seen
the whole string. The counting pass has to finish first.

## The three questions these four episodes ask the piles

| EP | the question to the counts | the one line |
|---|---|---|
| 67 | which key has count 1, **earliest in s**? | `next(i for i,c in enumerate(s) if counts[c]==1)` |
| 68 | how many full copies of `need` fit? | `min(counts[c] // need[c] for c in need)` |
| 69 | how many letters pair up, plus one odd in the middle? | `sum(v//2*2 for v in counts.values()) + any(v%2 for v in counts.values())` |
| 70 | does every key in `note` have enough in `magazine`? | `not (Counter(note) - Counter(magazine))` |

**EP68 is a budget with a ratio.** The bottleneck letter decides. `l` and `o` are
needed twice per word, so their counts get halved before the `min`. Forget the `// 2`
and "balloon" from `"loonbalxballpoon"` gives 4 instead of 2.

**EP69 is pairs plus at most one singleton.** Every even count contributes all of
itself; every odd count contributes all but one. If *any* count was odd, one leftover
letter can sit in the centre — but only **one**, no matter how many odd counts there
were. That `any` is the bug people ship as `sum`.

**EP70 is multiset containment.** `Counter(a) - Counter(b)` drops non-positive
entries, so the subtraction is empty exactly when `b` has enough of everything.
Written longhand: `all(mag[c] >= need for c, need in note.items())`.

## The three things that go wrong

### 1. `counts[ch]` on a plain `dict`

A plain `dict` raises `KeyError` for a missing key. `Counter` returns 0.
`defaultdict(int)` returns 0 *and inserts the key*. Pick one and know which you're
holding: `d.get(ch, 0)` is the plain-dict spelling, and forgetting it is the most
common crash in this pattern. In EP70, the letter you need that's *absent* from the
magazine is exactly the case that matters — it must read as 0, not blow up.

### 2. Iterating the dict when the answer wants the input's order

`for ch, n in counts.items()` walks in **insertion** order (Python ≥ 3.7), which
happens to match first-appearance order for a string — so EP67 written that way
*works by accident*. Don't rely on it in an interview; walk `s` and say why: *"the
dictionary knows how many, the string knows where."*

### 3. Integer division and the letter that appears twice in the target

In EP68 the divisor is `need[ch]`, not 1. Building `need = Counter("balloon")` gets
this for free; hard-coding `{'b':1,'a':1,'l':1,'o':1,'n':1}` from memory does not.
Same family of slip in EP69: `v // 2 * 2` (floor to even) is not `v // 2` (number of
pairs) — one is letters, the other is pairs, and the answer is in letters.

## Complexity

| Problem | Time | Space |
|---|---|---|
| all four episodes | O(n) — one or two passes | O(k), k = alphabet size, so **O(1)** for 26 letters |
| EP70 | O(n + m) over note and magazine | O(k) |
| brute force you're beating | O(n²) — rescan for every element | O(1) |

When the interviewer asks "is that O(n) space?", the answer is: the map has at most one
entry per **distinct** key, and the alphabet is fixed at 26 — so it's O(1). Say it
before they ask.

## The episodes

| EP | Problem | The thing it teaches |
|---|---|---|
| 67 | First Non-repeating Character | Two passes: count, then **walk the string** for order. |
| 68 | Maximum Number of Balloons | Frequency **budget**: `min` over `have // need`. |
| 69 | Longest Palindrome | Pairs from every pile, plus **at most one** odd centre. |
| 70 | Ransom Note | Multiset containment: `Counter(a) - Counter(b)` is empty. |

## What "knowing this in your sleep" means

1. What does the map's key mean, and what does the value mean? *(Key: the thing being
   counted. Value: how many so far. Say it before typing.)*
2. Does order matter after counting? *(If yes, the second pass walks the input, never
   the dict — EP67.)*
3. What happens on a missing key? *(`Counter` → 0, `dict` → `KeyError`. Know which one
   you're holding, and use `.get(k, 0)` on a plain dict.)*
4. Why is the space O(1) here? *(One entry per distinct key; the alphabet is fixed at
   26.)*
5. When is a hash map the wrong tool? *(When adjacency or contiguity matters — that's
   a window; when the input is sorted and you're converging — that's two pointers.)*
