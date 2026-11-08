python3 -c 'from pathlib import Path; import hashlib; print(hashlib.sha256(Path("examples/first-task/notes.md").read_bytes()).hexdigest())'
