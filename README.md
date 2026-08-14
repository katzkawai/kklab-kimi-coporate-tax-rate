# 世界の法人税の重み — 国際比較ダッシュボード

世界各国の法人税の「重み」を4つの指標で可視化したGitHub Pagesサイトです。

- **法定税率** — 企業利益に課される表定の税率(地方税込み複合税率)
- **実効税率** — OECDのフォワードルッキングEATR/EMTR(控除等を考慮した実質負担率)
- **法人税収の対GDP比** — 経済規模に対する法人税収の大きさ
- **総税収に占める法人税の割合** — 財政の法人税依存度

## 公開URL

https://katzkawai.org/kklab-kimi-coporate-tax-rate/ (GitHub Pages、カスタムドメイン)

## ファイル構成

- `index.html` — サイト本体 (Chart.js をCDNから読み込む静的ページ)
- `make_csvs.py` — 公開データ (Tax Foundation / OECD SDMX / UNU-WIDER GRD) から `data/*.csv` を生成するスクリプト
- `build_data.py` — `data/*.csv` を `data/data.json` に変換するビルドスクリプト
- `data/` — 加工済みデータ (CSV + 生成JSON)。出典は `data/SOURCES.md` を参照

## データ更新手順

1. `data/` のCSVを最新データで差し替える (スキーマは `build_data.py` 冒頭のコメント参照)
2. `python3 build_data.py` で `data/data.json` を再生成
3. commit & push で GitHub Pages に反映

## ローカルでの確認

```sh
python3 -m http.server 8000
# http://localhost:8000 を開く
```

## このサイトについて

このページは **Kimi K3** (Moonshot AIのAIエージェント) によって作成されました。データ収集・加工、サイト実装、GitHub Pagesへの公開までの一連の作業をAIが行っています。

## ライセンス

コードはMITライセンス。データの利用条件は各出典のライセンスに従ってください (`data/SOURCES.md` 参照)。
