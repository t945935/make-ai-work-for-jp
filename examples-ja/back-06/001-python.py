import csv
from pathlib import Path

root = Path(__file__).resolve().parent

def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)

source_fields, source_rows = read_csv(root / "input/tasks.csv")
assert source_fields == ["id", "task", "owner", "due", "status"]
assert source_rows == [
    dict(id="G01", task="完成封面", owner="小安", due="2026-10-05", status="done"),
    dict(id="G02", task="確認印量", owner="小文", due="2026-10-09", status="doing"),
    dict(id="G03", task="整理報名表", owner="", due="2026-10-10", status="todo"),
    dict(id="G04", task="檢查下載連結", owner="小安", due="", status="todo"),
], "source task fixture changed"
notes = (root / "input/notes.md").read_text(encoding="utf-8")
expected_notes = """# 慢光工作室會議摘記（虛構）
[N01] G02 的印量尚待確認，維持進行中。
[N02] G03 的負責人還沒決定，不要自行指派。
[N03] G04 有人建議十月十一日完成，但主持人尚未同意。
[N04] 本週只產生草稿，不寄出，也不公開上網。
"""
assert notes.strip() == expected_notes.strip(), "source notes changed"
fields, rows = read_csv(root / "output/actions.csv")
assert fields == ["id", "task", "owner", "due", "status", "sources"]
expected = [
    dict(id="G02", task="確認印量", owner="小文", due="2026-10-09",
         status="doing", sources="tasks.csv:G02;notes.md:N01"),
    dict(id="G03", task="整理報名表", owner="待確認", due="2026-10-10",
         status="todo", sources="tasks.csv:G03;notes.md:N02"),
    dict(id="G04", task="檢查下載連結", owner="小安", due="待確認",
         status="todo", sources="tasks.csv:G04;notes.md:N03"),
]
assert rows == expected, "action rows differ from approved contract"
for filename in ["report.md", "README.md"]:
    assert (root / "output" / filename).is_file(), filename
    assert (root / "output" / filename).read_text(encoding="utf-8").strip(), filename
report = (root / "output/report.md").read_text(encoding="utf-8")
for heading in ["## 本週待辦", "## 待確認", "## 來源"]:
    assert heading in report, heading
print("ACCEPTED: structured deliverables; human review still required")
