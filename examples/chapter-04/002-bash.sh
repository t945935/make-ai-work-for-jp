cd "$HOME/hermes-support-lab" &&
pwd &&
python3 -c 'from pathlib import Path; import hashlib; print(hashlib.sha256(Path("support-notes.md").read_bytes()).hexdigest())'