#!/usr/bin/env python3
"""data/*.csv を data/data.json に変換するビルドスクリプト。

入力スキーマ:
  statutory.csv    : code,name,name_ja,rate,year
  effective.csv    : code,name,name_ja,measure,value,year  (measure = EATR/EMTR)
  revenue_gdp.csv  : code,name,name_ja,value,year
  revenue_share.csv: code,name,name_ja,value,year
"""
import csv
import json
import os
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def read_rows(filename, value_col, measure=None):
    path = os.path.join(DATA_DIR, filename)
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if measure and r.get("measure") != measure:
                continue
            if r.get(value_col) in (None, ""):
                continue
            rows.append({
                "code": r["code"].strip(),
                "name": r["name"].strip(),
                "name_ja": (r.get("name_ja") or "").strip(),
                "value": round(float(r[value_col]), 2),
                "year": int(float(r["year"])),
            })
    return rows


SPEC = [
    # key, csvファイル, 値の列, 単位, measure絞り込み, 出典表示名
    ("statutory", "statutory.csv", "rate", "%", None,
     "Tax Foundation, Corporate Tax Rates around the World"),
    ("effective_eatr", "effective.csv", "value", "%", "EATR",
     "OECD, Corporate Tax Statistics (forward-looking ETR)"),
    ("effective_emtr", "effective.csv", "value", "%", "EMTR",
     "OECD, Corporate Tax Statistics (forward-looking ETR)"),
    ("revenue_gdp", "revenue_gdp.csv", "value", "%", None,
     "UNU-WIDER, Government Revenue Dataset"),
    ("revenue_share", "revenue_share.csv", "value", "%", None,
     "UNU-WIDER, Government Revenue Dataset"),
]


def main():
    out = {"generated": str(date.today()), "sources": []}
    for key, filename, value_col, unit, measure, source in SPEC:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"SKIP {key}: {filename} がありません")
            continue
        rows = read_rows(filename, value_col, measure)
        out[key] = {"unit": unit, "source": source, "rows": rows}
        if source not in out["sources"]:
            out["sources"].append(source)
        print(f"OK {key}: {len(rows)} rows")

    out_path = os.path.join(DATA_DIR, "data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
