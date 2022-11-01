set rtp+=/opt/homebrew/lib/python3.9/site-packages/powerline/bindings/vim
set rtp+=/usr/local/lib/python3.9/site-packages/powerline/bindings/vim
set fencs=ucs-bom,utf-8,cp949,euc-kr,shift_jis,euc-jp

set nocompatible
set autoread
set complete=.,w,b,u,t,i
filetype off

let g:NERDTreeWinSize=48
let g:NERDTreeIgore=['\.meta$']
let g:ycm_use_clangd = 0
let g:NERDSpaceDelims=1
let g:ycm_global_ycm_extra_conf='~/.vim/bundle/YouCompleteMe/third_party/ycmd/.ycm_extra_conf.py'
let g:ycm_confirm_extra_conf=0
let g:ycm_log_level='debug'
let g:ycm_key_list_selict_completion=['<C-j>', '<Down>']
let g:ycm_key_list_previous_completion=['<C-k>', '<Up>']
let g:ycm_autoclose_preview_window_after_completion=1
let g:neocomplcache#enable_at_startup = 1

let g:syntastic_python_python_exec='python3'
let g:syntastic_python_flake8_post_args='--ignore=E501,W505,E203,E305'

let g:airline#extension#tabline#enable=1
let g:airline#extension#tabline#formatter='unique_tail_improved'
let g:airline_powerline_fonts=1

set rtp+=~/.vim/bundle/Vundle.vim
set rtp+=/usr/local/opt/fzf

call vundle#begin()
Plugin 'VundleVim/Vundle.vim'

Plugin 'The-NERD-tree'
Plugin 'The-NERD-Commenter'
Plugin 'Auto-Pairs'
Plugin 'airblade/vim-gitgutter'
Plugin 'ycm-core/YouCompleteMe'
Plugin 'tpope/vim-fugitive'
Plugin 'scrooloose/syntastic'
Plugin 'snipMate'
Plugin 'terryma/vim-multiple-cursors'
Plugin 'Yggdroot/indentLine'
Plugin 'haya14busa/incsearch.vim'

call vundle#end()

filetype plugin indent on

let mapleader=','

syntax enable

noremap <F1> :set fileencoding=utf-8<CR> :w<CR> 
noremap <F7> :%!xxd<CR>

noremap <leader>y "*y
noremap <leader>yy "*Y

noremap <leader>p :set paste<CR>:put *<CR>:set nopaste<CR>
noremap <F3> :set hlsearch!<CR>

imap jj <ESC> :w<CR>
imap <F1> <ESC>

map <F8> :NERDTreeToggle<CR>
map <F5> :checktime<CR>

map / <Plug>(incsearch-forward)
map ? <Plug>(incsearch-backward)
map g/ <Plug>(incsearch-stay)

set cursorline
" set cursorcolumn
set si
set autoindent
set smartindent
set ruler
set number
set title
set expandtab
set hlsearch
set smartcase
set hidden
set splitbelow

set mouse=a
set tabstop=4
set softtabstop=4
set shiftwidth=4
set backspace=2
set laststatus=2
set cmdheight=1

set langmenu=en_US.UTF-8
language messages en_US.UTF-8
set term=screen-256color

if has('gui_running')
    set guifont=Cousine\ for\ Powerline:h12
endif

let @a='xjhxjhxjhxjhxjh'
