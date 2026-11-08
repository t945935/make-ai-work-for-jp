if cd "$HOME/hermes-lab-17" && test ! -e .venv && test ! -L .venv &&
   python3 -m venv .venv &&
   .venv/bin/python -m pip install 'mcp==2.0.0' &&
   .venv/bin/python -m pip show mcp; then
  printf 'SDK READY: %s\n' "$PWD"
else
  printf 'STOP: SDK の準備に失敗しました。MCPを登録しないでください。\n' >&2
  false
fi
