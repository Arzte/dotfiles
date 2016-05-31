export TERM="xterm-256color"
# Path to your oh-my-zsh installation.
  export ZSH=/home/benjamin/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="powerlevel9k/powerlevel9k"

# Theme settings
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(time context dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status rbenv nvm rvm virtualenv rbenv)
POWERLEVEL9K_STATUS_VERBOSE=true
POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_RPROMPT_ON_NEWLINE=true
POWERLEVEL9K_CONTEXT_DEFAULT_FOREGROUND=green
POWERLEVEL9K_DIR_DEFAULT_BACKGROUND=green
POWERLEVEL9K_DIR_HOME_BACKGROUND=green
POWERLEVEL9K_DIR_HOME_SUBFOLDER_BACKGROUND=green
POWERLEVEL9K_TIME_BACKGROUND=green
POWERLEVEL9K_BATTERY_LOW=red
POWERLEVEL9K_BATTERY_CHARGING=orange
POWERLEVEL9K_BATTERY_CHARGED=green
POWERLEVEL9K_BATTER_DISCONNECTED=blue

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git adb pip ssh-agent thefuck sprunge web-search fasd)

# User configuration

  export PATH="$PATH:$HOME/bin"
  export GPG_TTY=$(tty)
  export JAVA_HOME=/usr/lib/jvm/oracle-jdk
# export MANPATH="/usr/local/man:$MANPATH"
  fpath=(/home/benjamin/zsh-completions/src $fpath)

source $ZSH/oh-my-zsh.sh

# You may need to manually set your language environment
export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='nano'
else
  export EDITOR='vi'
fi

# Compilation flags
export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/dsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias xbps-i="sudo xbps-install -S"
alias xbps-r="sudo xbps-remove"
alias xbps-s="sudo xbps-query -Rs"
alias xbps-clean="sudo xbps-remove -ROo"
eval $(thefuck --alias)
eval "$(hub alias -s)"

# Stuff that appears when a new session opens
screenfetch
fortune | cowsay
