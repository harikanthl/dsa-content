-- ════════════════════════════════════════════════════════════════════════════
--  dsa.lua — LeetCode inside Neovim + practice ergonomics
--  Loaded by lua/custom/plugins/init.lua (vim.pack, Neovim 0.12+)
-- ════════════════════════════════════════════════════════════════════════════

local gh = function(name) return { src = 'https://github.com/' .. name } end

-- ── leetcode.nvim ───────────────────────────────────────────────────────────
-- Browse, solve, TEST and SUBMIT LeetCode problems without leaving the editor.
-- This is the whole reason the recording setup looks good: no browser tab.
vim.pack.add {
  gh 'nvim-lua/plenary.nvim',
  gh 'MunifTanjim/nui.nvim',
  gh 'kawre/leetcode.nvim',
}

require('leetcode').setup {
  lang = 'python3',
  cn = { enabled = false },
  storage = {
    home = vim.fn.expand '~/Documents/dsa-content/leetcode',
    cache = vim.fn.stdpath 'cache' .. '/leetcode',
  },
  console = {
    open_on_runcode = true,
    dir = 'row',
    size = { width = '90%', height = '75%' },
    result = { size = '60%' },
    testcase = { virt_text = true, size = '40%' },
  },
  description = {
    position = 'left',
    width = '40%',
    show_stats = true,
  },
  hooks = {
    -- Bigger, calmer text the moment a problem opens — matters on camera.
    ['question_enter'] = {
      function()
        vim.opt_local.wrap = true
        vim.opt_local.linebreak = true
      end,
    },
  },
  image_support = false, -- terminal images fight with screen recorders
}

-- ── keymaps ─────────────────────────────────────────────────────────────────
local map = function(lhs, rhs, desc) vim.keymap.set('n', lhs, rhs, { desc = desc }) end

-- <leader>l… = LeetCode
map('<leader>ll', '<cmd>Leet<cr>',          'LeetCode: dashboard')
map('<leader>lq', '<cmd>Leet list<cr>',     'LeetCode: problem list')
map('<leader>lr', '<cmd>Leet run<cr>',      'LeetCode: run testcases')
map('<leader>ls', '<cmd>Leet submit<cr>',   'LeetCode: submit')
map('<leader>ld', '<cmd>Leet desc<cr>',     'LeetCode: toggle description')
map('<leader>li', '<cmd>Leet info<cr>',     'LeetCode: problem info')
map('<leader>lc', '<cmd>Leet console<cr>',  'LeetCode: console')
map('<leader>lt', '<cmd>Leet lang<cr>',     'LeetCode: change language')

-- <leader>d… = the local dsa project
local dsa = vim.fn.expand '~/Documents/dsa-content/scripts/dsa'
map('<leader>dt', '<cmd>!pytest % -q<cr>',            'DSA: test this file')
map('<leader>dn', '<cmd>!' .. dsa .. ' next<cr>',     'DSA: what to record next')
map('<leader>dS', '<cmd>!' .. dsa .. ' stats<cr>',    'DSA: progress')
map('<leader>du', '<cmd>!' .. dsa .. ' due<cr>',      'DSA: drills due today')

-- ── recording mode ──────────────────────────────────────────────────────────
-- One toggle to make the editor legible at 1080p: bigger gaps, no clutter.
local recording = false
vim.api.nvim_create_user_command('RecordMode', function()
  recording = not recording
  if recording then
    vim.opt.number = true
    vim.opt.relativenumber = false -- absolute numbers: viewers can follow along
    vim.opt.signcolumn = 'no'
    vim.opt.laststatus = 0
    vim.opt.cmdheight = 0
    vim.opt.scrolloff = 8
    vim.opt.colorcolumn = ''
    vim.notify 'Recording mode ON'
  else
    vim.opt.relativenumber = true
    vim.opt.signcolumn = 'yes'
    vim.opt.laststatus = 3
    vim.opt.cmdheight = 1
    vim.notify 'Recording mode OFF'
  end
end, { desc = 'Toggle a clean, camera-friendly UI' })
map('<leader>dr', '<cmd>RecordMode<cr>', 'DSA: toggle recording mode')

-- ── python practice ergonomics ──────────────────────────────────────────────
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'python',
  callback = function()
    vim.opt_local.expandtab = true
    vim.opt_local.shiftwidth = 4
    vim.opt_local.tabstop = 4
    vim.opt_local.textwidth = 88
  end,
})
