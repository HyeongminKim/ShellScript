set rtp+=$HOME/.local/lib/python3.*/site-packages/powerline/bindings/vim
set fencs=ucs-bom,utf-8,cp949,euc-kr,shift_jis,euc-jp

set nocompatible
set autoread
set complete=.,w,b,u,t,i
filetype off

let g:airline#extension#tabline#enable=1
let g:airline#extension#tabline#formatter='unique_tail_improved'
let g:airline_powerline_fonts=1

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
