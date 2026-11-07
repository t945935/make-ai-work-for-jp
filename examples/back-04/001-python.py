from pathlib import Path
import csv
import io
import sys

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
SCHEMAS = {
    "clean.csv": BASE,
    "duplicates.csv": BASE + ["retained_row_id", "reason"],
    "exceptions.csv": BASE + ["reason"],
}
REASONS = {"R4": "缺少信箱", "R5": "席次非 ASCII 整數",
           "R6": "席次低於 1", "R8": "席次高於 3"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def text(path):
    # 只容許 BOM、換行風格及最後一個換行的差異，不 strip 欄位。
    return path.read_text(encoding="utf-8-sig").removesuffix("\n")


def verify(root, r9=False):
    expected_source = SOURCE + ("R9,林青,lin@example.com,3\n" if r9 else "")
    require(text(root / "registrations.csv") == expected_source.removesuffix("\n"),
            "來源全文不同：先核對章內固定素材")
    source = list(csv.DictReader(io.StringIO(expected_source)))
    clean_ids = ["R3", "R7"] if r9 else ["R1", "R3", "R7"]
    dup_ids = [] if r9 else ["R2"]
    exc_ids = ["R1", "R2", "R4", "R5", "R6", "R8", "R9"] if r9 else list(REASONS)
    groups = dict(zip(SCHEMAS, [clean_ids, dup_ids, exc_ids]))
    by_id = {row["row_id"]: row for row in source}
    for filename, fields in SCHEMAS.items():
        with (root / filename).open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == fields, filename + ": 表頭不符")
            actual = list(reader)
        expected = []
        for row_id in groups[filename]:
            raw = by_id[row_id]
            row = {"row_id": row_id, "name": raw["name"].strip(),
                   "email": raw["email"].strip().lower(), "seats": raw["seats"],
                   "raw_name": raw["name"], "raw_email": raw["email"],
                   "raw_seats": raw["seats"]}
            # 此固定素材有效席次已是無前導零字串。
            if filename == "duplicates.csv":
                row.update(retained_row_id="R1", reason="完全重複")
            if filename == "exceptions.csv":
                row["reason"] = REASONS.get(row_id, "同信箱資料衝突")
            expected.append(row)
        require(actual == expected, filename + ": 分流、順序或欄位內容不符")
    summary = (
        "# 報名清理摘要\n"
        "- 來源：registrations.csv\n"
        "- 規則版本：registrations-v1\n"
        f"- 輸入列數：{len(source)}\n"
        f"- clean：{len(clean_ids)}\n"
        f"- duplicates：{len(dup_ids)}\n"
        f"- exceptions：{len(exc_ids)}\n"
        f"- 未處理例外：{'、'.join(exc_ids)}；待人工確認，未自動修正\n"
        "- 原檔：未覆寫；固定全文比對通過"
    )
    require(text(root / "summary.md") == summary, "summary.md 內容不符")
    print(f"PASS: 固定{'R9 擴充' if r9 else '八列'}契約；來源/schema/全欄位/分流/summary")


if __name__ == "__main__":
    require(sys.argv[1:] in ([], ["--r9"]), "用法：python3 verify.py [--r9]")
    verify(Path(__file__).resolve().parent, r9=sys.argv[1:] == ["--r9"])