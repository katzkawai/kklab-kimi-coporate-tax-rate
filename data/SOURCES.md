# データ出典 (SOURCES)

取得日: 2026-08-14 (いずれも公開データを加工。数値の捏造はない)

## 1. statutory.csv — 法人税 法定税率 (複合: 中央+地方、2025年)

- 正式名称: **Tax Foundation, "Corporate Tax Rates Around the World, 2025"**
- 出典URL: https://taxfoundation.org/data/all/global/corporate-tax-rates-by-country-2025/
- 取得方法: ページHTML中の統合表 (226法域、ISO3コード付き、"Corporate Tax Rate" 列) をパース
- ライセンス/引用: Tax Foundation (著作権あり、引用は出典明記のうえ) / 引用例: Daniel Bunn and Isabela Calle, “Corporate Tax Rates Around the World, 2025,” Tax Foundation.
- 備考: "rate" は中央・地方税を合成した法定税率 (adjusted combined statutory rate)。フランス 36.13% は2025年の大企業向け一時付加税を含むソース値

## 2. effective.csv — フォワードルッキング実効税率 (EATR / EMTR)

- 正式名称: **OECD Corporate Tax Statistics database — "Effective tax rates" (dataflow: OECD.CTP.TPS:DSD_ETR@DF_ETR_BASELINE)**
- データセットページ: https://www.oecd.org/en/data/datasets/corporate-income-tax-rates-database.html
- 取得URL (OECD Data Explorer SDMX API):
  https://sdmx.oecd.org/public/rest/v1/data/OECD.CTP.TPS,DSD_ETR@DF_ETR_BASELINE/..EATR+EMTR..BASELINE..COMPOSITE.?dimensionAtObservation=AllDimensions
- ライセンス/引用: © OECD / 引用例: OECD (2025), Corporate Tax Statistics 2025, OECD Publishing, Paris, https://www.oecd.org/en/publications/corporate-tax-statistics-2025_6a915941-en.html
- 備考:
  - 仮想的投資プロジェクトに各国の税制パラメータを適用した合成指標 (実際の納税額ベースではない)
  - ETR_SCENARIO=FIXED (実質金利3%・インフレ率1%の共通マクロシナリオ、報告書ヘッドラインと同じ前提)
  - ETR_TAX_TYPE=COMPOSITE (資産・調達源泉の加重平均)、ETR_TAX_BASIS=BASELINE、単位は課税所得に対する%
  - 2025年値 (税制は当年7月1日時点)。EMTRが100%を超える国があるのはOECD原データ通り (投資インセンティブ等による)

## 3. revenue_gdp.csv / revenue_share.csv — 法人税収 (対GDP比 / 総税収比)

- 正式名称: **UNU-WIDER Government Revenue Dataset (GRD), Version 2025** (2025年11月更新)
- DOI: https://doi.org/10.35188/UNU-WIDER/GRD-2025
- 出典ページ: https://www.wider.unu.edu/project/grd-government-revenue-dataset
- 取得ファイル: https://www.wider.unu.edu/sites/default/files/Data/UNUWIDERGRD_2025.xlsx
- ライセンス/引用: オープンかつ無償利用可 / 引用: 'UNU-WIDER Government Revenue Dataset', Version 2025, https://doi.org/10.35188/UNU-WIDER/GRD-2025
- 備考:
  - 'General' (一般政府) シートを優先し、データがない国は 'Central' (中央政府) シートで補完
  - 法人税収 = "Taxes on Income, Profits & Capital Gains — o/w CIT" (GDP比、割合→×100で%化)
  - revenue_share = 法人税収 ÷ "Taxes (Excluding SC: 社会保険料を除く総税収)" × 100
  - 各国「その指標が存在する最新年」の値を採用 (1994–2023年の幅あり)
