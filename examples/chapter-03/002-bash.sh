pwd
python3 -c 'from pathlib import Path; p=Path("examples/first-task/notes.md"); print("來源存在：", p.is_file()); print("輸出已存在：", Path("output/action-items.md").exists())'