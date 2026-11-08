import csv
from pathlib import Path

with Path("sessions.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
expected = [
    ("W01", "筆記整理", "12", "10", "小岑", "confirmed"),
    ("W02", "簡報演練", "8", "10", "小岳", "confirmed"),
    ("W03", "資料清理", "10", "6", "", "confirmed"),
    ("W04", "寫作暖身", "6", "2", "", "draft"),
]
actual = [(r["id"], r["title"], r["capacity"], r["registered"],
           r["owner"], r["status"]) for r in rows]
assert actual == expected, "承認済みの固定データと一致しません"
assert len({r["id"] for r in rows}) == len(rows)
assert all(r["status"] in {"confirmed", "draft"} for r in rows)
over = {r["id"]: int(r["registered"]) - int(r["capacity"])
        for r in rows if int(r["registered"]) > int(r["capacity"])}
missing = {r["id"] for r in rows
           if r["status"] == "confirmed" and not r["owner"].strip()}
assert over == {"W02": 2}
assert missing == {"W03"}
print("定員超過", over)
print("確認済み・担当者不足", sorted(missing))
