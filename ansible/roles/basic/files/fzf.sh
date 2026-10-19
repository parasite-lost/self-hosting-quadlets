# fzf initialization for bash
if [ -n "$BASH_VERSION" ] && [ -n "$PS1" ] && command -v fzf >/dev/null 2>&1; then
  eval "$(fzf --bash)"
fi
