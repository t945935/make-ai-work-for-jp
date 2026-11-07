if cd "$HOME/hermes-lab-17" && test ! -e .venv && test ! -L .venv &&
   python3 -m venv .venv &&
   .venv/bin/python -m pip install 'mcp==2.0.0' &&
   .venv/bin/python -m pip show mcp; then
  printf 'SDK READY: %s\n' "$PWD"
else
  printf 'STOP: SDK 準備失敗，不註冊 MCP。\n' >&2
  false
fi