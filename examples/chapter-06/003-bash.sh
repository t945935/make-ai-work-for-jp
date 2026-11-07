cd "$HOME/hermes-rules-practice" &&
pwd &&
python3 -c 'from pathlib import Path; import hashlib; print(hashlib.sha256(Path("rule-notes.md").read_bytes()).hexdigest())'