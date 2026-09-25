# csmap-qgis

全国の **CS立体図** の XYZ タイル（46 レイヤー）を QGIS に一括で読み込むためのプロジェクトファイルと PyQGIS スクリプトです。

レイヤー定義は Web 地図 [csmap-on-maplibre](https://github.com/shiwaku/csmap-on-maplibre)（[デモ](https://shiwaku.github.io/csmap-on-maplibre/)）と共通で、そのスタイル定義から生成しています。

## 使い方

### プロジェクトを開く

[`csmap.qgz`](csmap.qgz) をダウンロードして QGIS で開きます。「CS立体図」グループに全レイヤーが入り、下に地理院タイル（淡色地図）が敷かれます。

### 既存のプロジェクトに追加する

QGIS の Python コンソールを開き（プラグイン > Python コンソール）、エディタで [`load_csmap.py`](load_csmap.py) を開いて実行します。

QGIS 3.34 と 4.0 で動作を確認しています。

## 注意

- タイルはズームレベル 8 前後から表示されるものが多く、日本全体を表示した状態では一部の地域しか見えません。
- 各レイヤーの出典はレイヤープロパティの「メタデータ > 権利」に入れてあります。利用条件は各提供元に従ってください（一覧は [csmap-on-maplibre の README](https://github.com/shiwaku/csmap-on-maplibre#データソース) を参照）。

## レイヤー一覧の更新

csmap-on-maplibre 側でレイヤーを追加・変更したら、次の手順で作り直します。

```bash
# 1. load_csmap.py の CS_LAYERS を GitHub の main から作り直す
python build_layers.py
#    ローカルのチェックアウトを使う場合
python build_layers.py ../csmap-on-maplibre

# 2. csmap.qgz を書き出す
"C:/Program Files/QGIS 3.34.12/bin/python-qgis-ltr.bat" load_csmap.py csmap.qgz
```

`build_layers.py` は、レイヤーの順序と表示名を `src/layers.ts`、タイル URL と出典を `public/style/pale.json` から取ります。最大ズームは、ソースの `maxzoom`、[csmap-tiles](https://github.com/shiwaku/csmap-tiles) の `datasets.json`、スクリプト内の `ZMAX_FALLBACK` の順に決まります。どれにも無いレイヤーがあるとエラーで止まるので、実際のタイルで最大ズームを確かめて `ZMAX_FALLBACK` に追加してください。

## ライセンス

このリポジトリのスクリプトとプロジェクトファイルは [MIT License](LICENSE) です。タイルは各提供元の利用条件に従います。
