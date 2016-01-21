set nocompatible 
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Bundle 'gmarik/vundle'
Bundle 'L9'
Bundle 'FuzzyFinder'
Bundle 'git://git.wincent.com/command-t.git'
Bundle 'git://github.com/Lokaltog/vim-powerline.git'
Bundle 'https://github.com/sukima/xmledit.git'
"Bundle 'https://github.com/Rip-Rip/clang_complete.git'
"Bundle 'https://github.com/scrooloose/syntastic.git'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'gmarik/vim-markdown'
Plugin 'gmarik/ingretu'
Plugin 'timcharper/textile.vim'
Plugin 'bogado/file-line'
Plugin 'junegunn/vim-easy-align'
Plugin 'tomasr/molokai'
Plugin 'vim-scripts/taglist.vim'
Plugin 'scrooloose/syntastic'
Plugin 'Valloric/YouCompleteMe'
call vundle#end()
filetype plugin indent on


let Tlist_Auto_Open=0
let Tlist_Auto_Update=1
let Tlist_WinWidth=30
let Tlist_Show_One_File=1
let Tlist_Use_SingleClick=1
let Tlist_Compact_Format=1
let Tlist_Exit_OnlyWindow=1
let Tlist_File_Fold_Auto_Close=1
let Tlist_GainFocus_On_ToggleOpen=1


let g:syntastic_check_on_open = 0
let g:syntastic_auto_loc_list = 1
let g:syntastic_enable_perl_checker = 1
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_error_symbol = '✗'
let g:syntastic_warning_symbol = '⚠'
let g:syntastic_cpp_include_dirs = ['/usr/include/qt']
let g:syntastic_cpp_compiler_options = '-std=gnu++11 -Wall'
let g:syntastic_php_checkers = ['php', 'phpcs', 'phpmd']
let g:syntastic_python_checkers = ['flake8']
let g:syntastic_quiet_messages = { "type": "style" }
let g:syntastic_phpcs_conf = "--tab-width=4 --standard=CodeIgniter"

let g:ycm_global_ycm_extra_conf = '.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm/.ycm_extra_conf.py'
let g:ycm_confirm_extra_conf = 0
let g:ycm_always_populate_location_list = 1
let g:ycm_complete_in_comments = 1
"let g:ycm_key_invoke_completion = 'mm'
set completeopt=longest,menu
let g:ycm_cache_omnifunc=0
let g:ycm_seed_identifiers_with_syntax = 1
let g:ycm_complete_in_strings = 1
let g:ycm_collect_identifiers_from_comments_and_strings = 0

let g:molokai_original = 1
let g:rehash256 = 1

nmap cqd di"
nmap cqs di'
nmap zj \\w
nmap zk \\b
nmap tl :TlistToggle<CR>
nmap gd :YcmCompleter GoToDefinitionElseDeclaration<CR>
nmap <F8> :YcmForceCompileAndDiagnostics<CR>
" 错误列表窗口
nmap lop :lopen<CR>
nmap lcl :lclose<CR>
" Ctrl+T 新建标签
nmap <C-T> <C-W>n
vmap <C-T> v<C-T>
imap <C-T> <ESC><C-T>
" <F5> 一键保存
nmap <F5> :w<CR>
imap <F5> <ESC><F5>a
vmap <F5> v<F5>
" <F9> 一键编译(需要makefile)
nmap <F9> <F5>:make %<CR>lop
vmap <F9> v<F9>
imap <F9> <Esc><F9>a
" <F6>        <F7>
" 十六进制化  逆十六进制化
nmap <F6> :%!xxd<CR>
vmap <F6> v<F6>
imap <F6> <ESC><F6>
nmap <F7> :%!xxd -r<CR>
vmap <F7> v<F7>
imap <F7> <ESC><F7>
" Ctrl+Z  Ctrl+Y
" 撤销    重做
nmap <C-Z> u
vmap <C-Z> v<C-Z>
imap <C-Z> <ESC><C-Z>i
nmap <C-Y> <C-R>
vmap <C-Y> v<C-Y>
imap <C-Y> <ESC><C-Y>i
" Ctrl+F  Ctrl+H
" 查找    替换
nmap <C-F> :/
vmap <C-F> v<C-F>
imap <C-F> <Esc><C-F>
nmap <C-H> :%s///g<Left><Left><Left>
vmap <C-H> v<C-H>
imap <C-H> <Esc><C-H>
" Ctrl+B 快速选定鼠标所在括号所关联另一端括号之间的文本块
nmap <C-B> v%
vmap <C-B> %
imap <C-B> <ESC><C-B>
" Ctrl+A 全选
nmap <C-A> ggVG
vmap <C-A> v<C-A>
imap <C-A> <ESC><C-A>
" Ctrl+X    Ctrl+C    Ctrl+V
" X11 剪贴  X11 复制  X11 粘贴
vmap <C-X> "+d
imap <C-X> <ESC><C-X>i
vmap <C-C> "+y
imap <C-C> <ESC><C-C>i
nmap <C-V> <F10>"+gP<F10>
vmap <C-V> v<C-V>v
imap <C-V> <Esc>1w<C-V>a
" <F2>    <F3>    <F4>
" 下一个  上一个  取消高亮
nmap <F2> n
imap <F2> <ESC><F2>a
nmap <F3> N
imap <F3> <ESC><F3>i
nmap <F4> :nohlsearch<CR>
imap <F4> <ESC><F4>a
" 分屏控制 <C-W>
" j/k/h/l       J/K/H/L       u/d                 q/o               s/v
" 分屏切换      分屏放置      上/下轮转           关闭当前/其他     水平/垂直分割
" v=/v-         h=/h-         a=/a-/e             =/-               ./,
" 垂直最大/最小 水平最大/最小 分屏最大/最小/相等  水平增大/减小三行 垂直增大/减小三行
imap <C-W> <ESC><C-W>
vmap <C-W> v<C-W>
nmap <C-W>u :wincmd R<CR>
nmap <C-W>d :wincmd r<CR>
nmap <C-W>q :q<CR>
nmap <C-W>o :only<CR>
nmap <C-W>v= :wincmd _<CR>
nmap <C-W>v- :wincmd 1_<CR>
nmap <C-W>h= :wincmd \|<CR>
nmap <C-W>h- :wincmd 1\|<CR>
nmap <C-W>a= <C-W>v=<C-W>h=
nmap <C-W>a- <C-W>v-<C-W>h-
nmap <C-W>e :wincmd =<CR>
nmap <C-W>s :split<CR>
nmap <C-W>v :vertical split<CR>
nmap <C-W>= :resize +3<CR>
nmap <C-W>- :resize -3<CR>
nmap <C-W>. :vertical resize +3<CR>
nmap <C-W>, :vertical resize -3<CR>

" ==========================
" Autocmd
" ==========================
if has("autocmd")
" Save the cursor localtion
  autocmd BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") |
    \ exe "normal! g`\"" |
    \ endif
endif

" ==========================
" asm 文件使用nasm 语法
" ==========================
au FileType asm set filetype=nasm

" ==========================
" GNU 缩进风格
" ==========================
" 如果不喜欢GNU 缩进风格
" 请注释掉函数后的au 一行
" ==========================
function! GnuIndent ()
  let b:did_ftplugin = 1
  setlocal cindent
  setlocal shiftwidth=4 tabstop=8 textwidth=78 softtabstop=2
  setlocal cinoptions=>2s,e-s,n-s,{1s,^-s,Ls,:s,=s,g0,+.5s,p2s,t0,(0
  setlocal formatoptions-=t formatoptions+=croql
  setlocal comments=sO:*\ -,mO:\ \ \ ,exO:*/,s1:/*,mb:\ ,ex:*/
  set cpoptions-=C
  set expandtab smarttab autoindent smartindent
endfunction
au FileType c,h,cpp,cc,hpp call GnuIndent ()

"vim-powerline
set laststatus=2
set t_Co=256
let g:Powerline_symbols = 'unicode'
set encoding=utf8

let g:vundle_lazy_load = 1

