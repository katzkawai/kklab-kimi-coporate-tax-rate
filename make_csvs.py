# -*- coding: utf-8 -*-
"""Build data/*.csv for the corporate-tax-rate GitHub Pages site.

Inputs (already downloaded):
  /tmp/tf2025.html      Tax Foundation "Corporate Tax Rates Around the World, 2025"
  /tmp/oecd_etr.csv     OECD Data Explorer SDMX: DSD_ETR@DF_ETR_BASELINE (EATR/EMTR)
  /tmp/GRD_2025.xlsx    UNU-WIDER Government Revenue Dataset, Version 2025
  /tmp/cl_regional.csv  OECD CL_REGIONAL codelist (code -> English name)
Outputs: data/statutory.csv, data/effective.csv, data/revenue_gdp.csv,
         data/revenue_share.csv, data/SOURCES.md
"""
import csv
import datetime
import subprocess

import pandas as pd

OUT = '/home/katzkawai/kklab-kimi-coporate-tax-rate/data'

# ISO3 -> Japanese country/territory name (major ones; rest fall back to English)
NAME_JA = {
 'JPN':'日本','USA':'アメリカ合衆国','DEU':'ドイツ','FRA':'フランス','GBR':'イギリス','ITA':'イタリア',
 'ESP':'スペイン','NLD':'オランダ','BEL':'ベルギー','CHE':'スイス','AUT':'オーストリア','SWE':'スウェーデン',
 'NOR':'ノルウェー','DNK':'デンマーク','FIN':'フィンランド','IRL':'アイルランド','PRT':'ポルトガル',
 'GRC':'ギリシャ','POL':'ポーランド','CZE':'チェコ','SVK':'スロバキア','SVN':'スロベニア','HUN':'ハンガリー',
 'EST':'エストニア','LVA':'ラトビア','LTU':'リトアニア','LUX':'ルクセンブルク','ISL':'アイスランド',
 'TUR':'トルコ','ISR':'イスラエル','CAN':'カナダ','MEX':'メキシコ','AUS':'オーストラリア',
 'NZL':'ニュージーランド','KOR':'韓国','CHN':'中国','IND':'インド','IDN':'インドネシア','THA':'タイ',
 'VNM':'ベトナム','MYS':'マレーシア','SGP':'シンガポール','PHL':'フィリピン','HKG':'香港','TWN':'台湾',
 'MAC':'マカオ','BRA':'ブラジル','ARG':'アルゼンチン','CHL':'チリ','COL':'コロンビア','PER':'ペルー',
 'ZAF':'南アフリカ','EGY':'エジプト','NGA':'ナイジェリア','KEN':'ケニア','SAU':'サウジアラビア',
 'ARE':'アラブ首長国連邦','QAT':'カタール','KWT':'クウェート','BHR':'バーレーン','OMN':'オマーン',
 'RUS':'ロシア','UKR':'ウクライナ','KAZ':'カザフスタン','PAK':'パキスタン','BGD':'バングラデシュ',
 'LKA':'スリランカ','MMR':'ミャンマー','KHM':'カンボジア','LAO':'ラオス','MAR':'モロッコ','TUN':'チュニジア',
 'DZA':'アルジェリア','GHA':'ガーナ','CIV':'コートジボワール','ETH':'エチオピア','TZA':'タンザニア',
 'UGA':'ウガンダ','HRV':'クロアチア','ROU':'ルーマニア','BGR':'ブルガリア','SRB':'セルビア','CYP':'キプロス',
 'MLT':'マルタ','LIE':'リヒテンシュタイン','MCO':'モナコ','JOR':'ヨルダン','LBN':'レバノン','IRQ':'イラク',
 'IRN':'イラン','AFG':'アフガニスタン','NPL':'ネパール','MNG':'モンゴル','URY':'ウルグアイ','PRY':'パラグアイ',
 'BOL':'ボリビア','ECU':'エクアドル','VEN':'ベネズエラ','CRI':'コスタリカ','PAN':'パナマ',
 'DOM':'ドミニカ共和国','JAM':'ジャマイカ','TTO':'トリニダード・トバゴ','GTM':'グアテマラ',
 'HND':'ホンジュラス','SLV':'エルサルバドル','CUB':'キューバ','PNG':'パプアニューギニア','FJI':'フィジー',
 'BRN':'ブルネイ','ALB':'アルバニア','AND':'アンドラ','ARM':'アルメニア','AZE':'アゼルバイジャン',
 'BLR':'ベラルーシ','BIH':'ボスニア・ヘルツェゴビナ','MDA':'モルドバ','MNE':'モンテネグロ',
 'MKD':'北マケドニア','GEO':'ジョージア','LSO':'レソト','NAM':'ナミビア','BWA':'ボツワナ',
 'MUS':'モーリシャス','SYC':'セーシェル','ZMB':'ザンビア','ZWE':'ジンバブエ','AGO':'アンゴラ',
 'CMR':'カメルーン','SEN':'セネガル','MLI':'マリ','BFA':'ブルキナファソ','NER':'ニジェール','TCD':'チャド',
 'COG':'コンゴ共和国','COD':'コンゴ民主共和国','GAB':'ガボン','RWA':'ルワンダ','MDG':'マダガスカル',
 'MWI':'マラウイ','MOZ':'モザンビーク','GIN':'ギニア','BDI':'ブルンジ','SLE':'シエラレオネ','TGO':'トーゴ',
 'BEN':'ベナン','SDN':'スーダン','LBY':'リビア','SOM':'ソマリア','YEM':'イエメン','SYR':'シリア',
 'UZB':'ウズベキスタン','KGZ':'キルギス','TJK':'タジキスタン','TKM':'トルクメニスタン','NIC':'ニカラグア',
 'SWZ':'エスワティニ','LBR':'リベリア','GNB':'ギニアビサウ','BTN':'ブータン','MDV':'モルディブ',
 'FJI':'フィジー','SMR':'サンマリノ','VAT':'バチカン','GIB':'ジブラルタル','JEY':'ジャージー',
 'GGY':'ガーンジー','IMN':'マン島','BMU':'バミューダ','CYM':'ケイマン諸島','VGB':'英領バージン諸島',
 'BHS':'バハマ','BRB':'バルバドス','BLZ':'ベリーズ','GUY':'ガイアナ','SUR':'スリナム','ATG':'アンティグア・バーブーダ',
 'DMA':'ドミニカ国','GRD':'グレナダ','KNA':'セントクリストファー・ネービス','LCA':'セントルシア',
 'VCT':'セントビンセント・グレナディーン','ABW':'アルバ','CUW':'キュラソー','SXM':'シント・マールテン',
 'TCA':'タークス・カイコス諸島','AIA':'アンギラ','MSR':'モントセラト','WLF':'ウォリス・フツナ',
 'PYF':'フランス領ポリネシア','NCL':'ニューカレドニア','GUM':'グアム','PRI':'プエルトリコ','GRL':'グリーンランド',
 'FRO':'フェロー諸島','ALA':'オーランド諸島','XKX':'コソボ','MHL':'マーシャル諸島','PLW':'パラオ',
 'KIR':'キリバス','NRU':'ナウル','TUV':'ツバル','WSM':'サモア','TON':'トンガ','SLB':'ソロモン諸島',
 'VUT':'バヌアツ','TLS':'東ティモール','DJI':'ジブチ','COM':'コモロ','CPV':'カーボベルデ','STP':'サントメ・プリンシペ',
 'GNQ':'赤道ギニア','ERI':'エリトリア','DJI':'ジブチ','MRT':'モーリタニア','ESH':'西サハラ','PSE':'パレスチナ',
 'WBG':'パレスチナ(西岸・ガザ)','HTI':'ハイチ','MNE':'モンテネグロ','XKX':'コソボ','TWN':'台湾',
}

def ja(code, en):
    return NAME_JA.get(code, en)

oecd_names = dict(csv.reader(open('/tmp/cl_regional.csv'))).__class__(
    (r['code'], r['name']) for r in csv.DictReader(open('/tmp/cl_regional.csv')))

# ---------------------------------------------------------------- statutory
tables = pd.read_html('/tmp/tf2025.html')
tf = tables[5]
tf = tf.rename(columns={'ISO 3': 'code', 'Country': 'name', 'Corporate Tax Rate': 'rate'})
tf = tf[['code', 'name', 'rate']].dropna(subset=['code', 'rate'])
tf['rate'] = tf['rate'].astype(str).str.rstrip('%').astype(float)
tf['name_ja'] = [ja(c, n) for c, n in zip(tf.code, tf.name)]
tf['year'] = 2025
statutory = tf[['code', 'name', 'name_ja', 'rate', 'year']].sort_values('code')
statutory.to_csv(f'{OUT}/statutory.csv', index=False)
print('statutory:', len(statutory))
print(statutory[statutory.code.isin(['JPN', 'USA', 'DEU'])].to_string(index=False))

# ---------------------------------------------------------------- effective
etr = pd.read_csv('/tmp/oecd_etr.csv')
etr = etr[(etr.ETR_SCENARIO == 'FIXED') & (etr.MEASURE.isin(['EATR', 'EMTR']))]
# latest year per country+measure
etr = etr.sort_values('TIME_PERIOD').groupby(['REF_AREA', 'MEASURE'], as_index=False).tail(1)
eff = pd.DataFrame({
    'code': etr.REF_AREA,
    'name': etr.REF_AREA.map(oecd_names).fillna(etr.REF_AREA),
    'measure': etr.MEASURE,
    'value': etr.OBS_VALUE.round(2),
    'year': etr.TIME_PERIOD.astype(int),
})
eff['name_ja'] = [ja(c, n) for c, n in zip(eff.code, eff.name)]
eff = eff[['code', 'name', 'name_ja', 'measure', 'value', 'year']].sort_values(['code', 'measure'])
eff.to_csv(f'{OUT}/effective.csv', index=False)
print('effective:', len(eff), 'countries:', eff.code.nunique())
print(eff[eff.code.isin(['JPN', 'USA', 'DEU'])].to_string(index=False))

# ---------------------------------------------------------------- GRD revenue
def grd_sheet(sheet):
    raw = pd.read_excel('/tmp/GRD_2025.xlsx', sheet_name=sheet, header=None, skiprows=3)
    df = raw.iloc[:, [2, 6, 7, 23, 35]].copy()  # country, iso, year, Taxes exSC, o/w CIT
    df.columns = ['country', 'iso', 'year', 'taxes', 'cit']
    df = df.dropna(subset=['iso'])
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['taxes'] = pd.to_numeric(df['taxes'], errors='coerce')
    df['cit'] = pd.to_numeric(df['cit'], errors='coerce')
    return df.dropna(subset=['year'])

gen = grd_sheet('General')
gen['gov'] = 'General'
cen = grd_sheet('Central')
cen['gov'] = 'Central'
grd = pd.concat([gen, cen])
# Per country prefer General government; fall back to Central when no General data
def make_rev(df, value_fn, need):
    d = df.dropna(subset=need).copy()
    d = d.sort_values(['gov', 'year'], ascending=[False, False]).groupby('iso').head(1)
    d['value'] = value_fn(d).round(2)
    out = pd.DataFrame({
        'code': d.iso,
        'name': d.country,
        'name_ja': [ja(c, n) for c, n in zip(d.iso, d.country)],
        'value': d.value,
        'year': d.year.astype(int),
    })
    return out.sort_values('code')

rev_gdp = make_rev(grd, lambda d: d.cit * 100, ['cit'])
rev_share = make_rev(grd, lambda d: d.cit / d.taxes * 100, ['cit', 'taxes'])
rev_gdp.to_csv(f'{OUT}/revenue_gdp.csv', index=False)
rev_share.to_csv(f'{OUT}/revenue_share.csv', index=False)
print('revenue_gdp:', len(rev_gdp), 'years:', rev_gdp.year.min(), '-', rev_gdp.year.max())
print(rev_gdp[rev_gdp.code.isin(['JPN', 'USA', 'DEU'])].to_string(index=False))
print('revenue_share:', len(rev_share))
print(rev_share[rev_share.code.isin(['JPN', 'USA', 'DEU'])].to_string(index=False))

today = subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()
print('TODAY=' + today)
