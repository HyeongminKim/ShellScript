OMZ_INSTALLED="false"

# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
if [ -d $HOME/.oh-my-zsh ]; then
    export ZSH="$HOME/.oh-my-zsh"
    OMZ_INSTALLED="true"
else
    echo -e "\033[33mWarning: oh-my-zsh is currently not installed or executable."
    echo -e "         Therefore some plugins doesn't work probably."
    echo -e "         Please check $HOME/.oh-my-zsh directory can accessable.\033[m"
    autoload -U colors && colors
fi

if [ ! -d /mnt/c ]; then
    echo -e "\033[31mAttention: Windows volume \"Local Disk (C:)\" is currently not mounted."
    echo -e "           Therefore most functions doesn't work probably."
    echo -e "           Please check /mnt/c directory can accessable.\033[m"
fi

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
if [[ "$OMZ_INSTALLED" == "true" ]]; then
    ZSH_THEME="mh"
else
    # https://github.com/ohmyzsh/ohmyzsh/blob/master/themes/mh.zsh-theme
    if [ $UID -eq 0 ]; then
        NCOLOR="green"
    else
        NCOLOR="white"
    fi
    PROMPT="[%{$fg[$NCOLOR]%}%B%n%b%{$reset_color%}:%{$fg[red]%}%30<...<%~%<<%{$reset_color%}]%(!.#.$) "
fi

# ZSH_THEME="powerlevel9k/powerlevel9k"

# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
if [[ "$OMZ_INSTALLED" == "true" ]]; then
    DISABLE_AUTO_UPDATE="true"
    ZSH_DISABLE_COMPFIX="true"
fi

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
  zsh-syntax-highlighting
  zsh-autosuggestions
  fasd
)

if [[ "$OMZ_INSTALLED" == "true" ]]; then
    source $ZSH/oh-my-zsh.sh
fi

aptall() {
    if [ -x ~/.local/bin/updater ]; then
        ~/.local/bin/updater $@
    fi
}

open() {
    if [ -x ~/.local/bin/open ]; then
        ~/.local/bin/open $@
    fi
}

powermgr() {
    if [ -x ~/.local/bin/powermgr ]; then
        ~/.local/bin/powermgr $@
    fi
}

wudo() {
    if [ -r ~/.shellscript/wsl-sudo/wsl-sudo.py ]; then
        python3 ~/.shellscript/wsl-sudo/wsl-sudo.py $@
    fi
}

function diff() {
    git diff --no-index $2 $3
}

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
alias "ls"="ls -lhF"
alias "dir"="ls -alhF"
alias "diff"="diff -s"
alias "ps"="ps -l"
alias "ㄷ턋"="exit"
alias zshconfig="vi ~/.zshrc"
alias vimconfig="vi ~/.vimrc"
alias tmuxconfig="vi ~/.tmux.conf"
alias brewall="echo \"$(uname -s) doesn't support this command.\""
alias taskmgr="open /mnt/c/Windows/System32/Taskmgr.exe"
alias reboot="echo \"WSL doesn't support this command. Did you mean 'halt' or 'powermgr reboot'?\""
alias halt="wsl.exe --shutdown"
alias yt-multi="~/.local/bin/YTMultiDown"
alias check="~/.local/bin/gitFileSize"
# alias ohmyzsh="mate ~/.oh-my-zsh"

set -o vi

# bindkey -v
