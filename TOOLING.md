# Tooling — what's installed, and the order to learn it

You asked to get proficient enough that people recognise the work. Tooling is a real
part of that, but only in one specific way: **speed removes friction between having
an idea and seeing it run.** That's it. Nobody hires you for your dotfiles. They hire
you because you move through a problem without fighting your editor.

So: learn a small set, deeply. Do not collect plugins.

---

## What's on this machine now

| Tool | Replaces | Why it earns its place |
|---|---|---|
| **nvim 0.12** (kickstart) | VS Code | Your editor. `vim.pack` is the new built-in plugin manager — no lazy.nvim needed. |
| **leetcode.nvim** | the browser | Browse, solve, run and submit LeetCode *inside nvim*. This is what makes your videos look different from everyone else's. |
| **tmux** | multiple terminal windows | Persistent sessions. Close the terminal, the work survives. |
| **ripgrep** (`rg`) | `grep` | ~10× faster, respects `.gitignore` by default |
| **fd** | `find` | Sane syntax. `fd sliding` instead of `find . -name "*sliding*"` |
| **bat** | `cat` | Syntax highlighting + line numbers |
| **eza** | `ls` | Colours, git status, `--tree` |
| **zoxide** (`z`) | `cd` | Learns your habits. `z dsa` from anywhere. |
| **fzf** | — | Fuzzy-find anything. The highest-leverage tool in this list. |
| **lazygit** | `git` CLI | A TUI for git. Staging individual lines is trivial. |
| **delta** | `git diff` | Side-by-side, syntax-highlighted diffs |
| **entr** | — | Re-run a command on file save. Powers the auto-test pane. |
| **glow** | — | Renders your prep sheets as formatted markdown in the terminal |
| **atuin** | shell history | Searchable, synced history. `Ctrl-R` becomes useful. |
| **just** | `make` | A command runner without Make's tab-vs-space misery |
| **btop** | `top` | Watch CPU while recording, to catch encoder overload |
| **uv** | pip/venv | Rust-fast Python packaging |
| **starship** | your prompt | 5–15ms prompt. Shows git branch + python version. |

Re-run `./scripts/setup-tooling.sh` any time; `dsa doctor` verifies.

### Two you should turn on manually

Add to `~/.zshrc`:
```bash
eval "$(zoxide init zsh)"      # then use `z` instead of `cd`
eval "$(atuin init zsh)"       # Ctrl-R becomes a real search
eval "$(starship init zsh)"    # fast prompt
alias ls='eza --icons --git'
alias cat='bat --style=plain'
alias lg='lazygit'
alias dsa='~/Documents/dsa-content/scripts/dsa'
```

---

## The nvim ladder — 6 weeks, ~10 min/day

The mistake is trying to learn everything at once. Learn **one motion per day** and
force yourself to use it until it's automatic. Muscle memory is built by repetition
under mild pressure, which is exactly what recording a video provides.

### Week 1 — stop using arrow keys
`h j k l` · `w` `b` `e` (word) · `0` `^` `$` (line) · `gg` `G` (file) · `i a o O` `Esc`

**Drill:** disable the arrow keys for one week. Put this in your config and suffer:
```lua
for _, k in ipairs { '<Up>', '<Down>', '<Left>', '<Right>' } do
  vim.keymap.set({ 'n', 'i', 'v' }, k, '<Nop>')
end
```

### Week 2 — operators, and the grammar
This is the week vim starts paying off. Vim is a **language**: `operator + motion`.

`d` delete · `c` change · `y` yank · `v` visual
→ `dw` delete word · `ci(` change inside parens · `yy` copy line · `dd` delete line ·
`ct,` change up to the next comma

**The insight:** you're not memorising commands, you're composing sentences. `ci"`
= "change inside quotes." Once you see the grammar, new combinations come free.

Best DSA use: `ci(` to rewrite a function's arguments, `ct:` to change a dict key.

### Week 3 — search and jump
`/` search · `n` `N` · `*` search word under cursor · `f` `t` `;` `,` (in-line jump) ·
`%` jump to matching bracket ·  `Ctrl-o` / `Ctrl-i` (jump back / forward)

`%` is quietly the best one for algorithm code — jumping between a bracket pair in
nested loops.

### Week 4 — multi-file
`<leader>sf` find file · `<leader>sg` live grep · `<leader><leader>` buffers
(all from kickstart's telescope config) · `:b <partial>` · `Ctrl-^` last buffer

### Week 5 — macros
`qa` start recording into register `a` · `q` stop · `@a` replay · `10@a` replay 10×

The classic use: you have ten test cases to reformat. Record the edit once, replay it
nine times. Doing this on camera makes viewers audibly gasp; it's great content.

### Week 6 — text objects at speed
`ci{` `di[` `ya(` `vip` (inside paragraph) · `dap` · `ct<char>`

**Test for graduation:** rewrite the body of a `while` loop without touching the
arrow keys, the mouse, or backspace more than twice. When that's comfortable, you're
faster than a VS Code user, and it will show on camera.

---

## The tmux ladder — 2 weeks

Config is at `~/.tmux.conf`. Prefix is **`Ctrl-a`** (not the default `Ctrl-b`).

### Week 1 — panes
| Keys | Does |
|---|---|
| `Ctrl-a` `\|` | split vertical |
| `Ctrl-a` `-` | split horizontal |
| `Ctrl-a` `h/j/k/l` | move between panes |
| `Ctrl-a` `z` | **zoom** a pane fullscreen (toggle) |
| `Ctrl-a` `x` | kill pane |

`Ctrl-a z` is the one to internalise for recording: code in a split, then zoom to
fullscreen the moment you want the viewer to focus on the editor only.

### Week 2 — sessions
| Keys | Does |
|---|---|
| `Ctrl-a` `d` | detach (work keeps running) |
| `tmux a` | re-attach |
| `Ctrl-a` `S` | fzf session switcher |
| `Ctrl-a` `g` | lazygit in a popup |
| `Ctrl-a` `D` | `dsa stats` in a popup |
| `Ctrl-a` `N` | what to record next |

**The mental model:** a *session* is a project. A *window* is a task in that project.
A *pane* is a view within a task. `dsa start` builds all three for you.

---

## The LeetCode-in-nvim loop

```
<leader>ll   dashboard
<leader>lq   pick a problem
<leader>lr   run the sample tests
<leader>ls   submit
<leader>ld   toggle the problem description
<leader>dr   toggle recording mode (clean UI)
```

First run: `:Leet` will ask you to sign in. It opens a browser once for the cookie,
then never again.

**Why this matters for the channel:** every other LeetCode video is a browser tab with
a cramped editor. Yours is a terminal, with the problem on the left and the solution
on the right, running tests without the mouse. That visual difference *is* a brand.

---

## What NOT to install

You will be tempted. Resist:

- **More colorschemes.** Pick one (kickstart ships tokyonight). Done.
- **A file-tree plugin you leave open.** Use `<leader>sf`. Trees are a VS Code habit.
- **Copilot / AI completion, while practising.** It will autocomplete the two-pointer
  loop before you've thought about it, and you'll learn nothing. Turn it on for real
  work; leave it off for the 186.
- **zellij**, for now. It's genuinely nicer than tmux out of the box, but tmux is what
  you'll find on every server you ever SSH into. Learn tmux first; it transfers.
