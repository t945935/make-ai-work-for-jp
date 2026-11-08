pwd
python3 -c 'from pathlib import Path; p=Path("examples/first-task/notes.md"); print("ソースが存在：", p.is_file()); print("出力がすでに存在：", Path("output/action-items.md").exists())'
