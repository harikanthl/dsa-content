# Terminal Cheatsheet

Everything active on this machine, what it's for, and the keys. Run `dsa keys` for
the short version in the terminal.

**Learn in layers.** Ghostty holds windows → tmux holds sessions → nvim holds files.
Don't try to absorb all three at once; there's a practice ladder at the bottom.

---

## 1. Ghostty (the terminal app itself)

Your config: `~/.config/ghostty/config` — JetBrainsMono Nerd Font 16, Catppuccin Mocha.

| Key | Does |
|---|---|
| `Cmd +` / `Cmd -` | font bigger / smaller — **bump to 20+ before recording** |
| `Cmd T` / `Cmd W` | new tab / close |
| `Cmd N` | new window |
| `Cmd 1..9` | jump to tab |
| `Opt H/J/K/L` | move between splits *(your custom binding)* |
| `Opt Shift H/J/K/L` | create a split in that direction *(yours)* |
| `Cmd K` | clear scrollback |
| `Cmd Shift ,` | reload config |

**Ghostty splits vs tmux splits — use tmux.** Ghostty's splits die when you close the
window; tmux's survive. Keep Ghostty to one window and let tmux do the layout.

---

## 2. tmux (sessions that survive)

**Is it a server?** Yes, genuinely — `tmux` runs a background process that owns your
sessions, parented to the OS rather than your terminal. That's *why* work survives
closing the window. It talks over a local socket file (`/tmp/tmux-501/default`), and
opens **no network ports** — nothing is exposed to anyone.

**Prefix is `Ctrl-a`.** Press it, release, then the key.

### Panes (splits inside one screen)
| Key | Does |
|---|---|
| `Ctrl-a z` | **zoom** this pane fullscreen / back — *the most useful key here* |
| `Ctrl-a \|` | split left/right |
| `Ctrl-a -` | split top/bottom |
| `Ctrl-a h j k l` | move between panes (same letters as nvim) |
| `Ctrl-a H J K L` | resize (hold to repeat) |
| `Ctrl-a x` | kill this pane |
| `Ctrl-a !` | pop this pane out into its own window |

### Windows (tabs inside a session)
| Key | Does |
|---|---|
| `Ctrl-a c` | new window |
| `Ctrl-a 1` / `2` | jump to window 1 / 2 |
| `Ctrl-a n` / `p` | next / previous |
| `Ctrl-a ,` | rename |
| `Ctrl-a w` | pick from a list |

### Sessions (one per project)
| Key | Does |
|---|---|
| `Ctrl-a d` | **detach** — work keeps running in the background |
| `tmux a` | re-attach to the last session |
| `tmux a -t dsa1` | attach to a named one |
| `Ctrl-a S` | fzf session switcher |
| `Ctrl-a s` | visual session/window tree |

### Scrolling and copying
| Key | Does |
|---|---|
| `Ctrl-a [` | enter scroll mode, then `hjkl` / `Ctrl-u` / `Ctrl-d`, `q` to exit |
| `v` then `y` | (in scroll mode) select, then copy to the Mac clipboard |
| `/` | (in scroll mode) search backwards |

### Project popups (custom)
| Key | Does |
|---|---|
| `Ctrl-a g` | lazygit in a popup |
| `Ctrl-a N` | what to record next |
| `Ctrl-a D` | progress dashboard |
| `Ctrl-a r` | reload tmux config |

**Your `dsa start` layout:** session `dsa1` → window `1:solve` (nvim left, auto-test
right) and window `2:prep` (the prep sheet). So `Ctrl-a 1` and `Ctrl-a 2` flip between
code and notes; `Ctrl-a z` zooms the editor for recording.

---

## 3. Neovim

**Leader is `Space`.** `:w` save, `:q` quit, `:wq` both, `u` undo, `Ctrl-r` redo.

### Files and search
| Key | Does |
|---|---|
| `Space s f` | find file by name |
| `Space s g` | grep across the whole repo |
| `Space Space` | switch between open buffers |
| `Space s h` | search the help docs |
| `Space s k` | search keymaps — *use this when you forget one* |

### LeetCode (leetcode.nvim)
| Key | Does |
|---|---|
| `Space l l` | dashboard |
| `Space l q` | problem list |
| `Space l r` | **run** the sample tests |
| `Space l s` | **submit** |
| `Space l d` | toggle the problem description |
| `Space l c` | console |

### This project
| Key | Does |
|---|---|
| `Space d t` | pytest the current file |
| `Space d r` | **recording mode** — clean UI for camera |
| `Space d n` | what to record next |
| `Space d u` | drills due today |

### Motions — the grammar
Vim is `operator + motion`. Learn the grammar, not a list.

| Motion | Where |
|---|---|
| `w` `b` `e` | word forward / back / end |
| `0` `^` `$` | line start / first non-blank / end |
| `gg` `G` | top / bottom of file |
| `%` | jump to the matching bracket — *great for nested loops* |
| `f<char>` `;` | jump to next `<char>` on this line, repeat |
| `Ctrl-o` `Ctrl-i` | jump back / forward through your history |

| Operator | With a motion |
|---|---|
| `d` delete | `dw` word · `dd` line · `d$` to end of line |
| `c` change | `cw` word · `ci(` inside parens · `ci"` inside quotes |
| `y` yank | `yy` line · `yi{` inside braces |
| `v` visual | `vip` paragraph · `V` whole line |

**The three that pay off most in algorithm code:** `ci(` (rewrite function args),
`%` (bracket matching), `ciw` (rename a variable under the cursor).

### Macros — the party trick
`qa` record into register `a` · `q` stop · `@a` replay · `10@a` replay ten times.
Use it to reformat a list of test cases in one shot. Genuinely good on camera.

---

## 3b. Multiple files on one screen

Two different tools do this and picking the right one matters.

| You want | Use | Why |
|---|---|---|
| Several **files** side by side | **nvim splits** | one editor: yank between them, one LSP, `:wa` saves all |
| Several **programs** (editor + tests + git) | **tmux panes** | separate processes |

### nvim splits — for files

| Key | Does |
|---|---|
| `Ctrl-w v` | split **v**ertical (left/right) |
| `Ctrl-w s` | split horizontal (top/bottom) |
| `Ctrl-h j k l` | move between splits *(kickstart binds this)* |
| `Ctrl-w q` | close this split |
| `Ctrl-w o` | close all the **o**thers — the "zoom" of nvim |
| `Ctrl-w =` | make them all equal size |
| `Ctrl-w _` / `Ctrl-w \|` | maximise height / width |
| `Ctrl-w r` | rotate them |
| `Ctrl-w H J K L` | move this split to the far left/bottom/top/right |

**The fast way to build a layout** — from the file picker:

```
Space s f       find a file
  Ctrl-v          open it in a VERTICAL split
  Ctrl-x          open it in a HORIZONTAL split
  Enter           open it in the current split
```

So four files in about six keystrokes: `Space s f` → pick → `Ctrl-v`, repeat.
Same works from grep results (`Space s g`).

### Buffers — usually better than a 4-way split

Every file you open is a **buffer**, whether or not it's visible. Splits are just
*windows onto* buffers. Four splits on one screen gives you ~40 columns each, which
is too narrow for real code.

| Key | Does |
|---|---|
| `Space Space` | fuzzy-pick any open buffer |
| `Ctrl-^` | toggle between the last two files — *the one to build muscle memory on* |
| `:bd` | close the current buffer |

**Recommended:** keep **two** splits, and cycle buffers inside them with
`Space Space` and `Ctrl-^`. You get the side-by-side comparison where it helps,
without shrinking everything to unreadable columns. Most people over-split.

### tmux panes — for programs

To build a 4-pane grid in one window:

```
Ctrl-a |        split left/right
Ctrl-a -        split the right one top/bottom
Ctrl-a h        move back to the left pane
Ctrl-a -        split that one too
```

| Key | Does |
|---|---|
| `Ctrl-a h j k l` | move between panes |
| `Ctrl-a z` | zoom one to fullscreen / back |
| `Ctrl-a x` | close this pane |
| `Ctrl-a !` | pop this pane out into its own window |
| `Ctrl-a space` | cycle through preset layouts |
| `Ctrl-a H J K L` | resize |

**No conflict with nvim:** tmux needs the `Ctrl-a` prefix first; nvim's `Ctrl-h/j/k/l`
is pressed directly. Different keys, they coexist.

## 4. Shell tools

| Command | Does |
|---|---|
| `z <partial>` | jump to any directory you've visited — `z dsa` from anywhere |
| `Ctrl-r` | fuzzy-search your entire shell history (atuin) |
| `rg <text>` | search file *contents* recursively, respects `.gitignore` |
| `fd <name>` | find files by *name* |
| `bat <file>` | cat with syntax highlighting |
| `eza --tree` | directory tree (`ls` and `ll` are aliased to eza) |
| `lg` | lazygit |
| `btop` | system monitor — watch CPU while recording |
| `glow <file.md>` | render markdown in the terminal |
| `tldr <cmd>` | practical examples instead of a man page |

### lazygit (`lg` or `Ctrl-a g`)
| Key | Does |
|---|---|
| `Space` | stage / unstage the selected file |
| `a` | stage everything |
| `c` | commit |
| `P` / `p` | push / pull |
| `Tab` | move between panels |
| `Enter` on a file | stage **individual lines** — this is the killer feature |
| `x` | menu of everything available here |
| `q` | quit |

### Project commands
```bash
dsa next | start | test | prep | done | rep | due | stats | keys | doctor
archive status | push [--purge] | pull <file>
```

---

## 5. The practice ladder

Don't learn this list. Learn **one thing per day**, using it until it's automatic.

**Week 1 — survive without arrows.** `hjkl`, `w`/`b`, `0`/`$`, `gg`/`G`, `i`/`a`/`o`,
`Esc`. Disable the arrow keys so you can't cheat:
```lua
-- add to ~/.config/nvim/lua/custom/plugins/dsa.lua
for _, k in ipairs { '<Up>', '<Down>', '<Left>', '<Right>' } do
  vim.keymap.set({ 'n', 'i', 'v' }, k, '<Nop>')
end
```

**Week 2 — operators.** `dw`, `dd`, `cw`, `ci(`, `yy`, `p`. This is the week vim
starts being faster than a normal editor.

**Week 3 — tmux panes.** `Ctrl-a z`, `Ctrl-a |`, `Ctrl-a hjkl`. Stop opening new
terminal windows.

**Week 4 — search and jump.** `/`, `n`, `*`, `%`, `Ctrl-o`, `Space s g`.

**Week 5 — sessions.** `Ctrl-a d`, `tmux a`, `Ctrl-a S`. Never lose work to a closed
window again.

**Week 6 — macros and text objects.** `qa...q`, `@a`, `ci{`, `vip`.

**Graduation test:** rewrite the body of a `while` loop without touching the arrow
keys, the mouse, or backspace more than twice. When that's comfortable, you're faster
than a VS Code user — and on camera, it shows.

---

## 6. If something looks broken

| Symptom | Cause | Fix |
|---|---|---|
| Empty boxes (□) in the prompt | terminal font isn't a Nerd Font | Ghostty is set to JetBrainsMono Nerd Font; in Apple Terminal set it manually |
| `Ctrl-a` does nothing | not inside tmux | `tmux a`, or `dsa start` |
| tmux colours look flat | `TERM` wrong | use Ghostty, not Apple Terminal |
| Prompt shows versions you don't want | starship | write `~/.config/starship.toml` to disable modules |
| `dsa: command not found` | alias not loaded | `source ~/.zshrc` |
