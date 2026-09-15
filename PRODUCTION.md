# The Production Playbook

Everything about *how* a video gets made. The prep sheets handle *what* you say.

---

## 1. The format (locked — do not redesign it per video)

A consistent format is what turns 186 uploads into a *series* instead of 186 orphans.
Viewers subscribe to a format, not to a topic.

**Target length: 8–14 minutes.** Under 6 feels thin for a Medium; over 18 loses retention.

| # | Beat | Time | What's on screen |
|---|------|------|------------------|
| 1 | **Hook** | 0:00–0:15 | Your face, full screen. One sentence: the *insight*, not the problem. |
| 2 | **Type the problem** | 0:15–1:30 | Editor. You type the statement out and read it aloud. |
| 3 | **The example** | 1:30–3:00 | You hand-write a tiny input and trace what the answer should be. |
| 4 | **ELI5 / the analogy** | 3:00–4:30 | Face cam bigger. The real-world metaphor. No code yet. |
| 5 | **Brute force, out loud** | 4:30–5:30 | Say the O(n²) idea. Say why it's wasteful. *Do not type it.* |
| 6 | **The pattern reveal** | 5:30–6:30 | Name the pattern. Name the signal in the problem that gave it away. |
| 7 | **Code it** | 6:30–10:30 | Type the optimal solution. Narrate every line as you write it. |
| 8 | **Run it** | 10:30–11:30 | `<leader>lr` → run → `<leader>ls` → submit. Show the green. |
| 9 | **Complexity + the takeaway** | 11:30–13:00 | Time/space. Then one sentence: "when you see X, reach for Y." |
| 10 | **Outro** | last 15s | "Tomorrow: \<next problem\>." Nothing else. |

### The one rule that matters

**Never edit out a mistake in beats 7–8.** If you get an index wrong and the test
fails, fix it on camera and say what you got wrong. That is the single most
valuable thing on the whole channel — it is the thing no polished tutorial has, and
it is exactly what a viewer preparing for an interview needs to see. Polished
perfection reads as "this person memorised it." Recovery reads as "this person
*understands* it."

---

## 2. Recording setup — your actual kit

Detected on this Mac mini M4: **Logitech Brio 300** (UVC camera) and a **USB PnP
Audio Device** (your mic, mono input — which is correct for one voice).

### Meld Studio — build these two scenes once, then never touch them

Meld is Metal-accelerated and Mac-native, so it will cost you far less CPU than OBS
on an M4. You want exactly two scenes and a hotkey between them.

| Scene | Layers (top → bottom) | Used for |
|---|---|---|
| `TALK` | Brio 300, full frame 1920×1080 | Beats 1, 4, 9, 10 |
| `CODE` | Brio 300 cropped to a circle, bottom-right ~320px · Screen Capture (display) | Beats 2, 3, 5–8 |

Build `TALK` first, then duplicate the scene and add the screen capture underneath —
that keeps the camera crop identical across both, so your face doesn't jump size when
you switch.

Bind a keyboard shortcut for each scene (Meld → Settings → Shortcuts). You will press
it about four times per video. That is the entire "edit."

**Settings:** 1920×1080 · 30 fps · hardware (VideoToolbox) H.264 · ~8000 Kbps ·
48 kHz audio. Record locally to disk; do not stream.

### Audio — the one thing to fix before recording anything

Your mic is already the right kind of device. Two things to do in Meld:

1. **Mute the Mac mini's built-in input entirely.** If both your USB mic and any
   other input are live, you get phasing that sounds like a cheap headset.
2. Add a **Noise Suppression** and a **Limiter** filter on the mic channel. The
   limiter is the important one — it stops the clip that happens when you get excited
   and lean in, which is the #1 audio defect in solo coding videos.

Record in a room with soft things in it. Hard rooms echo, and no filter fixes echo.

### Terminal appearance — the part people underestimate

Small text is the #1 reason coding videos fail. On a phone, 14pt is unreadable.

```bash
brew install --cask font-jetbrains-mono   # then set your terminal to 18-20pt
```

Then inside nvim, before every take:

```vim
:RecordMode
```

That toggle (installed at `~/.config/nvim/lua/custom/plugins/dsa.lua`) switches to
absolute line numbers so viewers can follow along when you say "line 14", kills the
sign column and status line, and sets `scrolloff=8` so your cursor never sits at the
screen edge.

### The DJI Pocket 2 — the honest answer

**It will not work as a webcam on this Mac, and I'd skip it for this project.**

DJI never shipped UVC webcam mode for the Pocket 2. Their own support page lists
webcam mode only for Osmo Pocket 3/4 and the Action 2–6 line — the Pocket 2 is
absent. Plugging it into the Mac mini's USB-C gives you a *storage* device (you'll
see the SD card), not a camera. macOS currently reports exactly one camera on this
machine: the Brio 300. So there is no on-device menu step I can give you, because the
mode doesn't exist in its firmware.

Your three real options, ranked:

1. **Just use the Brio 300.** For a 320px face circle in the corner of a code video,
   the Pocket 2's better sensor is invisible. The viewer is reading your editor. This
   costs you nothing and is what I'd do for all 186.
2. **Third-party Wi-Fi bridge** ([webcam-tool.com](https://www.webcam-tool.com/))
   supports the Pocket 2 over Wi-Fi as a virtual camera. It's paid, it adds latency,
   and it adds a thing that can fail at the start of every recording session. For a
   186-video run, a daily failure point is a real cost.
3. **Record the Pocket 2 separately to its microSD and sync in post.** Genuinely the
   best image, and genuinely not worth it — it adds a sync-and-export step to every
   single episode, and that is exactly the kind of friction that kills a daily series
   at week three.

**Where the Pocket 2 *is* worth using:** a channel trailer, a "who I am / why I'm
doing 186 videos" intro film, or B-roll. Shoot those as one-off projects where an
extra hour of editing is fine. Keep it out of the daily loop.

## 3. The recording loop

```bash
dsa next            # tells you the episode
dsa start           # scaffolds the file, opens the tmux workspace
#   → window "solve": nvim on the left, auto-running pytest on the right
#   → window "prep":  the prep sheet rendered with glow
```

Read the prep sheet **the night before**, not while recording. Sleep on it.
In the morning you re-derive it cold on camera — that is what makes the learning
stick, and it makes the video honest.

After the take:

```bash
dsa done 1 https://youtu.be/xxxx    # mark recorded + uploaded
dsa rep 1                           # log a repetition → schedules the re-drill
```

---

## 4. Retention: the four places people leave

1. **0:00–0:15.** Fix: open with the *insight*, never with "Hey guys, welcome back."
   Compare: ~~"Hi everyone, today we're doing Two Sum II"~~ vs. **"This array is
   sorted, and almost nobody uses that. It's the whole problem."**
2. **~1:00, when you start reading the statement.** Fix: you are *typing* it, which
   keeps motion on screen. Keep it under 75 seconds.
3. **The silent gap while you think.** Fix: think out loud, always. Silence is the
   retention killer in coding videos. If you're stuck, say "okay, I'm stuck, here's
   what I'm considering."
4. **The moment the code works.** Fix: the takeaway line in beat 9 must promise
   transfer — "this same two-pointer shape solves 3Sum tomorrow." Give them a
   reason to come back.

---

## 5. Titles, thumbnails, descriptions

### Titles

The format is a promise plus a specific. Search traffic comes from the problem name,
so it must be present and spelled the way LeetCode spells it.

```
Two Sum II — the sorted array trick nobody uses | DSA Pattern #1
3Sum, explained like you're five | Two Pointers
Why your Sliding Window is O(n) and not O(n²)
```

Avoid: all-caps, "EASY!!!", clickbait you don't pay off. This audience is technical
and punishes it.

### Thumbnails

Three elements, nothing more. Build **one** template in Canva and swap the text:

- **3–5 huge words.** `SORTED = FREE INFO`. Readable at 120px wide.
- **Your face**, one clear expression, right third.
- **A colour block per pattern** (Two Pointers = blue, Sliding Window = orange, …).
  After 20 videos a returning viewer recognises the pattern from the colour alone.
  That is a channel, not a pile of videos.

### Description template

```
{one-line insight}

Problem: {leetcode url}
Pattern: {pattern} — video {n} of {total} in this playlist
Full pattern playlist: {playlist url}

⏱ Chapters
0:00 The idea
0:15 Reading the problem
1:30 Working an example
3:00 The intuition
4:30 Brute force and why it's slow
5:30 The pattern
6:30 Writing the code
10:30 Running it
11:30 Complexity + takeaway

Solving in Neovim with leetcode.nvim. Full setup + my notes for all 186 problems:
{github repo url}

#leetcode #datastructures #algorithms #{pattern-tag} #codinginterview
```

Chapters are not optional — they generate the timeline segments that YouTube uses
for suggested-video placement, and they let a returning viewer skip to beat 7.

---

## 6. Playlists

One playlist per pattern, 15 total. Each playlist is ordered by the `CODE` column
(`P01E01`, `P01E02`, …) in `curriculum/CURRICULUM.md` — **not** upload date.

Name them for search:

```
Two Pointers — every pattern, 12 problems
Binary Search — from basics to Aggressive Cows (23 problems)
Dynamic Programming — from Fibonacci to Min Cost to Cut a Stick
```

Put the playlist link in every description in that playlist. A viewer who finishes
#3 and finds #4 one click away is the entire growth mechanism on YouTube.

---

## 7. Cadence — the honest version

One video a day for 186 days is roughly 6 months with zero missed days, and the
failure mode is burnout at week 3, not lack of skill.

**Record in batches. Publish daily.** Batch 3–4 videos in one sitting on a good day
(the setup cost is paid once — lights, mic, mental state), then schedule them out.
YouTube does not care when you recorded; it cares that a video appears on schedule.

A sustainable target: **5 videos a week, batched into two sessions.** That is
~37 weeks. Slower than daily, and you will actually finish, which daily-or-nothing
people do not.

### Shorts, for free

Beat 4 (the ELI5 analogy) is a 45–60 second vertical Short with no extra work:
crop to 9:16, add the problem name as a caption, done. Shorts are how a channel
with 0 subscribers gets discovered; long-form is how it retains them. One Short per
long-form video doubles your surface area for about four minutes of effort.

---

## 8. The first ten videos

Do not publish videos 1–5 the day you record them. Record all five, watch them back,
and notice your own tics (filler words, looking away, typing in silence). Publish
video 1 on the day you record video 6. You will be measurably better by then, and
the first impression a new viewer gets from your top-of-playlist video will be a
version of you that has already practised.
