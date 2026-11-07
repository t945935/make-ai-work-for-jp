cd "$HOME/hermes-rules-practice" &&
pwd &&
python3 -c 'from pathlib import Path; import hashlib; print(hashlib.sha256(Path("rule-result.md").read_bytes()).hexdigest())'