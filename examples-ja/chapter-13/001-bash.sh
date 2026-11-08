if mkdir "$HOME/hermes-lab-13" && cd "$HOME/hermes-lab-13" && python3 --version; then
  printf 'READY: %s\n' "$PWD"
else
  printf 'STOP: 初期化に失敗しました。この章の以降の手順を実行しないでください。\n' >&2
  false
fi
