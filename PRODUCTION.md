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

### The DJI Pocket 2 — it CAN work. Here's how.

**Correction to my first take:** I said skip it. That was wrong. There's no UVC
webcam mode, but there *is* a working path, and it's already installed and tested on
this machine.

**What's actually true.** DJI never shipped UVC webcam mode for the Pocket 2 —
verified here: plugged into USB-C it mounts as storage (`/Volumes/Untitled`, 256 GB,
`DCIM/` + `MISC/`) and macOS still lists only the Brio 300 as a camera. So no cable
will make it a webcam.

**But** DJI's own docs list the Pocket 2 as supporting **livestream via the DJI Mimo
app** (v1.2.20+), to a **custom RTMP server**, at 1080p30 / 3–6 Mbps. So we run that
server locally:

```
Pocket 2 ──USB──> your phone (DJI Mimo) ──wifi──> this Mac (MediaMTX)
                                                       │
                                            Meld Studio "Browser" layer
```

No Do-It-All Handle needed — the phone provides the network.

**Already set up and tested:**

```bash
pocketcam start     # starts the local RTMP server, prints both URLs
pocketcam status    # is the phone publishing yet?
pocketcam stop
```

It prints exactly what to type into Mimo (`rtmp://192.168.31.69:1935/pocket`, empty
stream key) and what to paste into Meld's Browser layer
(`http://localhost:8889/pocket/?controls=false&muted=true`).

I verified the full chain with a synthetic 1080p30 stream: RTMP ingest accepted,
readable back over WebRTC, RTSP and HLS. Meld's layer list confirms a **Browser**
layer exists, so no extra software and nothing to buy.

**The one real cost: latency.** Wi-Fi adds 1–2 seconds of video delay. Your USB mic
has none, so your voice arrives ahead of your face. Fix it once in Meld by adding a
matching **delay to the mic channel** — clap on camera, line up the waveform, note
the offset. It stays put for every recording afterwards. This is fine for *recording*;
it would be miserable for live interaction, which you aren't doing.

**The paid alternative.** [Webcam Tool](https://www.webcam-tool.com/) explicitly
supports the Pocket 2 on macOS 13+ and produces a real **virtual camera**, which Meld
takes directly as a Video Device layer (cleaner than a Browser layer). Same 1–2s
Wi-Fi latency. It connects over Wi-Fi in AP mode — which for a Pocket 2 means you
need the **Do-It-All Handle**, since the bare camera has no Wi-Fi of its own. Worth
it only if you own the handle and the Browser layer annoys you.

**My recommendation, unchanged in substance:** shoot the daily 186 on the Brio 300.
In a 320px corner circle the Pocket 2's sensor advantage is invisible, and a Wi-Fi
hop is one more thing that can fail at the start of a session. Use the RTMP path for
the pieces where image quality actually shows — the channel trailer, a "why I'm doing
this" video, pattern-recap intros. Now you have the option, which you didn't before.

### Checking the stream without Meld

```bash
pocketcam preview          # opens the WebRTC player — exactly what Meld will show
pocketcam preview ff       # ffplay instead; lowest latency, q to quit
pocketcam status           # is the phone publishing yet?
```

If you see colour bars / an RGB test pattern, that's a synthetic test stream, not
your camera — it means the pipeline is working end to end and is waiting for Mimo.

### The face cam: circle/square crop and background

**The crop is built into Meld.** Select the camera layer; a quick-actions toolbar
appears above its bounding box. Hit **Crop**, then pick the **Circle** preset (or the
rounded-square). For a custom radius, drag any of the four corner handles inward.
**Reset Crop** puts it back. No mask PNG, no plugin.

**The background — three options, in the order to try them.**

**1. macOS built-in (free, no green screen) — test this first.**
macOS 26 Tahoe can replace your background with a gradient, an Apple image, or *your
own photo* (a woods shot, a clean colour), using on-device ML. AVFoundation reports
your Brio 300 as supporting it at the full 1920×1080@30:

```
1920x1080 @30fps  portrait=true  bgReplace=true  studioLight=true
```

The catch: Apple has historically gated these effects to built-in FaceTime cameras
and the Studio Display, and community reports say third-party USB webcams often
don't get the toggle even when the format advertises support. So test it rather than
trust it:

```bash
./scripts/camcheck
```

That opens the Brio, prints which effects are currently active, and pops the macOS
**Video Effects** panel. Look for a **Background** control. Leave it running while
you click around — it live-prints each flag as you toggle it, so you get an
unambiguous yes/no. `Ctrl-C` to quit.

If Background is there: turn it on, point it at your image, and you're done — the
effect is applied at the OS level, so Meld just sees a camera that already has the
background replaced. Zero cost inside Meld.

**2. Camo Studio (paid, no green screen) — the reliable Mac fallback.**
[Camo](https://reincubate.com/camo/) does background **Replace** and privacy blur on
*any* USB webcam and publishes a virtual camera. Meld takes that directly as a
**Video Device** layer, which is cleaner than a Browser layer. This is the answer if
`camcheck` shows no Background control.

**3. Physical green screen + Meld's Chroma Key (cheapest reliable).**
Meld has a built-in **Green Screen / Chroma Key** effect with an eyedropper for the
key colour: select the layer → Effects → **＋** → Chroma Key → pick the colour. A
collapsible green screen is about $20 and it is the only option here that never
depends on a vendor's ML being in a good mood. It also keys far better, which matters
if you ever want a *transparent* background so your code shows through behind you.

**Worth saying plainly:** at 320px in the corner, background replacement is mostly
invisible — viewers are reading your editor. Where it genuinely pays off is the
full-frame `TALK` scene in beats 1, 4, 9 and 10. Consider enabling it per-scene
rather than globally.

### Storage — record local, archive to hkt460s

This Mac has **19 GB free**. At ~800 MB per 14-minute 1080p recording that's about
20 videos before you're stuck. `hkt460s` (ThinkPad T460s, reachable over Tailscale at
`100.126.137.0`) has **377 GB free**.

**Never record straight to the network share.** A Tailscale hiccup mid-take corrupts
the file and you reshoot. Record to `~/Movies/dsa`, archive after.

```bash
archive              # dry run — what would transfer
archive push         # copy to hkt460s, keep local copies
archive push --purge # copy, SHA-256 verify BOTH ends, then free local space
archive status       # disk + counts, both machines
archive pull <file>  # bring one back for re-editing
```

The `--purge` path checksums every file on both ends and refuses to delete anything
that doesn't match. Tested end to end.

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
