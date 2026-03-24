# Neovim/LazyVim Cheatsheet

Leader key: `<Space>`

## General Commands

| Command | Action |
|---------|--------|
| `:Lazy` | Plugin manager UI |
| `:Mason` | LSP/linter/formatter manager |
| `:checkhealth` | Diagnose issues |
| `:LspInfo` | Show attached LSP servers |
| `:LazyExtras` | Enable/disable LazyVim extras |

## File Navigation

| Key | Action |
|-----|--------|
| `<leader>e` | Toggle file explorer (neo-tree) |
| `<leader><space>` | Find files |
| `<leader>ff` | Find files |
| `<leader>fr` | Recent files |
| `<leader>fb` | Find buffers |
| `<leader>/` | Live grep (search in files) |
| `<leader>sg` | Grep (search string) |
| `<leader>sw` | Search word under cursor |

## Buffers & Windows

| Key | Action |
|-----|--------|
| `<S-h>` | Previous buffer |
| `<S-l>` | Next buffer |
| `<leader>bd` | Delete buffer |
| `<leader>bo` | Delete other buffers |
| `<C-h/j/k/l>` | Navigate windows |
| `<leader>-` | Split horizontal |
| `<leader>\|` | Split vertical |

## Git (lazygit)

| Key | Action |
|-----|--------|
| `<leader>gg` | Open lazygit |
| `<leader>gf` | Lazygit file history |
| `<leader>gl` | Lazygit log |
| `]h` | Next hunk |
| `[h` | Previous hunk |
| `<leader>ghs` | Stage hunk |
| `<leader>ghr` | Reset hunk |
| `<leader>ghp` | Preview hunk |
| `<leader>ghb` | Blame line |

## LSP (Code Intelligence)

| Key | Action |
|-----|--------|
| `gd` | Go to definition |
| `gr` | Go to references |
| `gD` | Go to declaration |
| `gI` | Go to implementation |
| `gy` | Go to type definition |
| `K` | Hover documentation |
| `gK` | Signature help |
| `<leader>ca` | Code actions |
| `<leader>cr` | Rename symbol |
| `<leader>cf` | Format file |
| `<leader>cd` | Line diagnostics |
| `]d` | Next diagnostic |
| `[d` | Previous diagnostic |
| `]e` | Next error |
| `[e` | Previous error |

## Search & Replace

| Key | Action |
|-----|--------|
| `<leader>sr` | Replace in files (grug-far) |
| `n` / `N` | Next/previous search result |
| `*` | Search word under cursor |
| `#` | Search word (backward) |

## Terminal

| Key | Action |
|-----|--------|
| `<C-/>` | Toggle terminal |
| `<leader>ft` | Terminal (root dir) |
| `<leader>fT` | Terminal (cwd) |

## Editing

| Key | Action |
|-----|--------|
| `gcc` | Toggle line comment |
| `gc` | Toggle comment (visual) |
| `<leader>cf` | Format |
| `<` / `>` | Indent left/right (visual) |
| `.` | Repeat last change |
| `u` | Undo |
| `<C-r>` | Redo |

## Motions (Essential)

| Key | Action |
|-----|--------|
| `w` / `b` | Next/previous word |
| `e` | End of word |
| `0` / `$` | Start/end of line |
| `^` | First non-blank |
| `gg` / `G` | Start/end of file |
| `{` / `}` | Previous/next paragraph |
| `%` | Matching bracket |
| `f{char}` | Find char forward |
| `t{char}` | Till char forward |
| `s` | Flash jump (2-char) |

## Text Objects

| Key | Action |
|-----|--------|
| `iw` / `aw` | Inner/around word |
| `i"` / `a"` | Inner/around quotes |
| `i(` / `a(` | Inner/around parens |
| `i{` / `a{` | Inner/around braces |
| `if` / `af` | Inner/around function |
| `ic` / `ac` | Inner/around class |

## which-key

Press `<leader>` and wait 300ms to see all available keybindings.
Each submenu shows what's available under that prefix.

## Tips

1. Use `<leader>sk` to search keymaps
2. Use `:Telescope keymaps` for full list
3. `hardtime.nvim` will gently remind you of better motions
4. Press `?` in neo-tree for help
5. Press `?` in lazygit for help
