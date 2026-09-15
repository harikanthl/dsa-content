#!/usr/bin/env bash
# One-shot install of the terminal toolchain this repo's workflow assumes.
# Safe to re-run: brew skips anything already present.
set -u
CORE=(fd entr lazygit git-delta zoxide eza tldr jq)      # workflow depends on these
NICE=(atuin btop yazi just watchexec starship television) # quality-of-life
echo "==> core"; brew install "${CORE[@]}"
echo "==> nice-to-have (optional, comment out if you want a lean box)"; brew install "${NICE[@]}"
echo "==> done. Run 'dsa doctor' to verify."
