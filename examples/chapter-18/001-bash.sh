if mkdir "$HOME/hermes-graduation" && cd "$HOME/hermes-graduation" && mkdir input output; then
  printf 'READY: %s\n' "$PWD"
else
  printf 'STOP: 初始化失敗；不要執行本章後續步驟。\n' >&2
  false
fi