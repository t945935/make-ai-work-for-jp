if mkdir "$HOME/hermes-lab-16" && cd "$HOME/hermes-lab-16"; then
  printf 'READY: %s\n' "$PWD"
else
  printf 'STOP: 初始化失敗；不要執行本章後續步驟。\n' >&2
  false
fi