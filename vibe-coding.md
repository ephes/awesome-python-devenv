# Vibe Coding Cheatsheet

Both tmux and zellij are available. Use whichever you prefer.

## Getting In

| Command | Action |
|---------|--------|
| `ta vibe@macmini.tailde2ec.ts.net` | tmux session picker + agent forwarding |
| `za vibe@macmini.tailde2ec.ts.net` | zellij session picker + agent forwarding |
| `ssh vibe@macmini.tailde2ec.ts.net` | SSH in, then `t` (tmux) or `zz` (zellij) |
| `t` | Attach to tmux session or create "work" |
| `zz` | Attach to zellij session or create "work" |

---

## tmux

Prefix key: `Ctrl+Space`

### Prefix-Free Navigation (no prefix needed)

| Key | Action |
|-----|--------|
| `Ctrl+Shift+h/j/k/l` | Navigate between panes |
| `Ctrl+Alt+Left/Right/Up/Down` | Navigate between panes (fallback) |
| `Shift+Left/Right/Up/Down` | Resize panes |
| `Ctrl+Shift+Left/Right` | Previous / next window |
| `Ctrl+Alt+PageDown` (`Ctrl+Alt+Fn+Down`) | Split pane below (vertical) |
| `End` (`Fn+Right`) | Kill pane (with confirmation prompt) |
| Left click pane | Focus pane only (no click-through into app) |
| `Shift+Left click` pane | Focus pane and forward click to app |

### Prefix Commands (Ctrl+Space, then...)

| Key | Action |
|-----|--------|
| `\|` | Split pane side-by-side (horizontal) |
| `-` | Split pane stacked (vertical) |
| `%` | Split pane side-by-side (tmux default) |
| `"` | Split pane stacked (tmux default) |
| `c` | New window |
| `s` | Session picker (choose-tree) |
| `a` | Toggle sync panes (type in all) |
| `X` | Kill session |
| `d` | Detach (disconnect, session persists) |
| `[` | Enter copy mode (vi keys) |
| `]` | Paste buffer |
| `z` | Toggle pane zoom (fullscreen) |
| `n` / `p` | Next / previous window |
| `)` / `(` | Next / previous session |
| `,` | Rename current window |
| `$` | Rename current session |
| `w` | Window picker |

### Window Reordering

| Command | Action |
|---------|--------|
| `tmux swap-window -s 1 -t 3` | Swap window 1 with window 3 |

### Copy Mode (vi keys)

Enter copy mode: `Ctrl+Space`, `[`

| Key | Action |
|-----|--------|
| `Space` | Start selection |
| `y` | Copy selection (OSC 52 → local clipboard) |
| `Escape` | Clear selection (stays in copy mode!) |
| `q` | Exit copy mode (back to terminal) |
| `/` | Search forward |
| `?` | Search backward |
| `n` / `N` | Next/previous match |
| `Ctrl+u` / `Ctrl+d` | Page up / page down |
| `gg` / `G` | Jump to top / bottom |
| `h/j/k/l` | Move cursor (vim-style) |

### Copying Long Passages

**Tip: zoom the pane first** with `Ctrl+Space`, `z` to avoid accidentally scrolling adjacent panes when mouse-dragging near the pane border. `Ctrl+Space`, `z` again to unzoom.

For really long selections, keyboard is more reliable than mouse:

1. `Ctrl+Space`, `z` — zoom pane (optional, avoids pane-border issues)
2. `Ctrl+Space`, `[` — enter copy mode
3. Navigate to start (`/` to search, `gg` for top, `Ctrl+u`/`Ctrl+d` for pages)
4. `Space` — start selection
5. Navigate to end (same keys)
6. `y` — copy and exit copy mode
7. `Ctrl+Space`, `z` — unzoom (if you zoomed)

---

## zellij

Modes: Normal → `Ctrl+g` Locked | `Ctrl+p` Pane | `Ctrl+t` Tab | `Ctrl+n` Resize | `Ctrl+s` Scroll | `Ctrl+o` Session

### Normal Mode (no prefix needed)

| Key | Action |
|-----|--------|
| `Alt+Left/Right/Up/Down` | Navigate between panes (if terminal sends Alt keys to zellij) |
| `Alt+h/j/k/l` | Navigate between panes (vim-style, if terminal sends Alt keys) |
| `Alt+n` | New pane (split down) |
| `Alt+=` / `Alt+-` | Increase / decrease pane size |
| `Ctrl+p`, then `h/j/k/l` or arrows, then `Ctrl+p` | Reliable pane-switch fallback (works when Alt is intercepted by terminal) |

### Pane Mode (`Ctrl+p`, then...)

| Key | Action |
|-----|--------|
| `h/j/k/l` or arrows | Move focus between panes |
| `d` | Split pane down |
| `r` | Split pane right |
| `x` | Close pane |
| `f` | Toggle fullscreen (zoom) |
| `w` | Toggle floating pane |
| `c` | Rename pane |

### Tab Mode (`Ctrl+t`, then...)

| Key | Action |
|-----|--------|
| `n` | New tab |
| `x` | Close tab |
| `r` | Rename tab |
| `1`–`9` | Switch to tab N |
| `h` / `l` or `Left` / `Right` | Previous / next tab |
| `s` | Toggle sync (type in all panes) |

### Session Mode (`Ctrl+o`, then...)

| Key | Action |
|-----|--------|
| `d` | Detach (disconnect, session persists) |
| `w` | Session manager (sessions + tabs + panes) |

### Session Rename

| Command | Action |
|---------|--------|
| `zellij action rename-session <new-name>` | Rename current session |
| `zellij list-sessions --short --no-formatting` | Verify session names |

### Resize Mode (`Ctrl+n`, then...)

| Key | Action |
|-----|--------|
| `h/j/k/l` | Resize in direction |
| `H/J/K/L` | Resize in larger steps |
| `+` / `-` | Increase / decrease size |

### Scroll Mode (`Ctrl+s`)

| Key | Action |
|-----|--------|
| `j` / `k` or `Up` / `Down` | Scroll |
| `s` | Enter search mode |
| `n` / `N` | Next / previous match |
| `Escape` or `q` | Exit scroll mode |

### Locked Mode (`Ctrl+g`)

All keys pass through to the inner application. Use when apps need `Alt+<key>` bindings (e.g., fish word navigation with `Alt+Left/Right`). Press `Ctrl+g` again to return to normal mode.

### Copy/Paste

- **`copy_on_select true`** — selecting text copies to clipboard via OSC 52
- In scroll mode: select with mouse, auto-copied

---

## Project Sync (vsync) — works with both

| Command | Action |
|---------|--------|
| `vsync push <project>` | Sync local → macmini (incl. .git) |
| `vsync pull <project>` | Sync macmini → local (never deletes local files) |
| `vsync push <project> --force` | Push with `--delete` (mirror) |
| `vsync push <project> --dry-run` | Preview what would change |
| `vsync pull <project> --dry-run` | Preview what would change |

## Typical Workflow

1. `vsync push myproject` — push code to macmini
2. `ta vibe@macmini.tailde2ec.ts.net` (tmux) or `za ...` (zellij) — attach
3. Code, run tests, use Claude Code
4. Detach: `Ctrl+Space, d` (tmux) or `Ctrl+o, d` (zellij)
5. `vsync pull myproject` — pull changes back

## Tips

1. Sessions survive SSH disconnects — just reconnect and `t`/`zz`
2. `git push/pull` only works when connected via `ta`/`za` (agent forwarding)
3. After `vsync push`, run `npm install` / `uv sync` on macmini (node_modules/.venv excluded)
4. State files live in `~/.local/state/vsync/` (not in the repo)
5. Mouse behavior: tmux mouse is on (plain click focuses pane; `Shift+click` forwards click). zellij `mouse_mode` is set to `false`
6. zellij + Ghostty: if `Alt+Left/Right` switches tabs or `Alt+h/j/k/l` types symbols, use `Ctrl+p` + `h/j/k/l` (or arrows) for pane switching
7. Optional Ghostty fix for Alt navigation: set `macos-option-as-alt = true` and remove `alt+left/right` tab keybinds in `~/.config/ghostty/config`
8. `zellij list-sessions` / `tmux list-sessions` to see sessions (zellij may also show exited/resurrectable ones)
9. `z` remains available for zoxide; zellij local attach uses `zz`
