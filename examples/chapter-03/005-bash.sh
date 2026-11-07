cd "$HOME/hermes-first-task" &&
pwd &&
python3 -c 'from pathlib import Path; print(Path("output/action-items.md").read_text(encoding="utf-8"))'