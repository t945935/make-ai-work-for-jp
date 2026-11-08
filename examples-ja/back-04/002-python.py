from pathlib import Path
import csv
import io
import subprocess
import sys
import tempfile

# 人手で作成した受け入れテスト用データであり、モデルが生成したクリーニング結果ではない。
SOURCE = """row_id,name,email,seats
R1,林青, LIN@example.com ,2
R2,林青,lin@example.com,2
R3,周舟,zhou@example.com,1
R4,阿晴,,1
R5,杜明,du@example.com,兩位
R6,許禾,xu@example.com,0
R7,陳小溪,chen@example.com,3
R8,林青,lin@example.com,4
"""
BASE = "row_id,name,email,seats,raw_name,raw_email,raw_seats".split(",")
FIELDS = {"clean.csv": BASE,
          "duplicates.csv": BASE + ["retained_row_id", "reason"],
          "exceptions.csv": BASE + ["reason"]}
CHECKER = Path(__file__).with_name("verify.py").read_text(encoding="utf-8")


def fixture(root, r9=False):
    raw_text = SOURCE + ("R9,林青,lin@example.com,3\n" if r9 else "")
    (root / "registrations.csv").write_text(raw_text, encoding="utf-8")
    (root / "verify.py").write_text(CHECKER, encoding="utf-8")
    # 振り分けと正規化値は固定の正解であり、クリーナーや検証器で生成しない。
    groups = {"clean.csv": ["R3", "R7"] if r9 else ["R1", "R3", "R7"],
              "duplicates.csv": [] if r9 else ["R2"],
              "exceptions.csv": (["R1", "R2", "R4", "R5", "R6", "R8", "R9"]
                                 if r9 else ["R4", "R5", "R6", "R8"])}
    values = [("林青", "lin@example.com", "2"), ("林青", "lin@example.com", "2"),
              ("周舟", "zhou@example.com", "1"), ("阿晴", "", "1"),
              ("杜明", "du@example.com", "兩位"), ("許禾", "xu@example.com", "0"),
              ("陳小溪", "chen@example.com", "3"), ("林青", "lin@example.com", "4"),
              ("林青", "lin@example.com", "3")]
    reasons = {"R4": "缺少信箱", "R5": "席次非 ASCII 整數",
               "R6": "席次低於 1", "R8": "席次高於 3"}
    rows = {}
    for index, raw in enumerate(csv.DictReader(io.StringIO(raw_text))):
        rows[raw["row_id"]] = dict(zip(BASE, [raw["row_id"], *values[index],
                                             raw["name"], raw["email"], raw["seats"]]))
    for filename, ids in groups.items():
        output = []
        for rid in ids:
            row = rows[rid].copy()
            if filename == "duplicates.csv":
                row.update(retained_row_id="R1", reason="完全重複")
            if filename == "exceptions.csv":
                row["reason"] = reasons.get(rid, "同信箱資料衝突")
            output.append(row)
        save(root / filename, FIELDS[filename], output)
    counts = (9, 2, 0, 7) if r9 else (8, 3, 1, 4)
    summary = ("# 報名清理摘要\n- 來源：registrations.csv\n"
               "- 規則版本：registrations-v1\n"
               f"- 輸入列數：{counts[0]}\n- clean：{counts[1]}\n"
               f"- duplicates：{counts[2]}\n- exceptions：{counts[3]}\n"
               f"- 未處理例外：{'、'.join(groups['exceptions.csv'])}；待人工確認，未自動修正\n"
               "- 原檔：未覆寫；固定全文比對通過\n")
    (root / "summary.md").write_text(summary, encoding="utf-8")


def save(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def change(root, filename, rid, field, value):
    path = root / filename
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    for row in rows:
        if row["row_id"] == rid:
            row[field] = value
    save(path, fields, rows)


def run_case(label, mutate=None, r9=False):
    with tempfile.TemporaryDirectory(prefix="registration-check-") as directory:
        root = Path(directory)
        fixture(root, r9)
        if mutate:
            mutate(root)
        command = [sys.executable, "-B", str(root / "verify.py")]
        result = subprocess.run(command + (["--r9"] if r9 else []),
                                capture_output=True, text=True)
        expected_success = mutate is None
        if (result.returncode == 0) != expected_success:
            raise RuntimeError(label + "\n" + result.stdout + result.stderr)
        print(f"確認済み {label}: 終了コード={result.returncode}")


run_case("正しい8行")
run_case("正しいR9の競合優先", r9=True)
for rid in ("R1", "R3", "R7"):
    for field, value in (("name", "錯誤姓名"), ("email", "WRONG@example.com"),
                         ("seats", "99")):
        run_case(f"誤り {rid} {field}",
                 lambda p, r=rid, f=field, v=value: change(p, "clean.csv", r, f, v))
for filename, rid in (("clean.csv", "R1"), ("duplicates.csv", "R2"),
                      ("exceptions.csv", "R5")):
    for field in ("raw_name", "raw_email", "raw_seats"):
        run_case(f"誤り {filename} {field}",
                 lambda p, n=filename, r=rid, f=field: change(p, n, r, f, "被改掉"))
run_case("保持行の誤り", lambda p: change(p, "duplicates.csv", "R2", "retained_row_id", "R3"))
run_case("任意の例外理由", lambda p: change(p, "exceptions.csv", "R4", "reason", "任意文字"))
run_case("R1の原値の空白がトリミングされた", lambda p: change(p, "clean.csv", "R1", "raw_email", "LIN@example.com"))
run_case("ソースが変更された", lambda p: (p / "registrations.csv").write_text(SOURCE.replace("周舟", "錯名"), encoding="utf-8"))
run_case("summaryがない", lambda p: (p / "summary.md").unlink())
run_case("summaryが誤り", lambda p: (p / "summary.md").write_text("全部完成", encoding="utf-8"))
run_case("schemaがない", lambda p: (p / "exceptions.csv").write_text("row_id,reason\nR4,任意文字\n", encoding="utf-8"))
run_case("IDの重複", lambda p: change(p, "clean.csv", "R3", "row_id", "R1"))
run_case("R9の競合が重複と誤認された", lambda p: change(p, "exceptions.csv", "R2", "reason", "完全重複"), r9=True)


def dedup_before_conflict(root):
    path = root / "exceptions.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    duplicate = next(row.copy() for row in rows if row["row_id"] == "R2")
    duplicate.update(reason="完全重複", retained_row_id="R1")
    save(root / "duplicates.csv", FIELDS["duplicates.csv"], [duplicate])
    save(path, FIELDS["exceptions.csv"], [row for row in rows if row["row_id"] != "R2"])


run_case("R9を誤って先に重複として振り分け", dedup_before_conflict, r9=True)
