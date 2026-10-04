# Day 6: 要件定義とAPI調査

## 📅 実施日
- 予定: Week 2 - Day 6
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
天気アプリの要件を定義し、Open-Meteo APIの仕様を詳しく調査する

---

## 📋 午前の作業（9:00-13:00）

### 1. 要件定義書の作成（9:00-11:00）

**学習内容:**

要件定義とは、「何を作るか」を明確にする作業

**要件定義書のテンプレート作成:**

`requirements.md`を作成：

```markdown
# 天気アプリケーション 要件定義書

## 1. プロジェクト概要

### 1.1 目的
47都道府県の天気情報を取得・表示し、取得履歴をデータベースに保存するWebアプリケーション

### 1.2 対象ユーザー
- 一般ユーザー（日本国内の天気を知りたい人）

### 1.3 開発期間
- 40営業日（約2ヶ月）

## 2. 機能要件

### 2.1 トップページ（都道府県一覧）
- **機能**: 47都道府県の一覧を表示
- **表示項目**:
  - 都道府県名
  - 都道府県コード
  - 代表地点の緯度・経度
- **操作**:
  - 都道府県をクリックすると詳細ページへ遷移

### 2.2 天気詳細ページ
- **機能**: 選択した都道府県の天気情報を表示
- **表示項目**:
  - 現在の天気
    - 気温（℃）
    - 天気コード（晴れ、曇り、雨など）
    - 風速（m/s）
    - 湿度（%）
  - 週間天気予報（7日間）
    - 日付
    - 最高気温
    - 最低気温
    - 天気コード
- **データ取得**:
  - Open-Meteo APIから取得
  - 取得した情報はデータベースに保存

### 2.3 データ保存機能
- **機能**: API取得データの履歴保存
- **保存項目**:
  - 都道府県ID
  - 取得日時
  - 気温
  - 天気コード
  - その他の気象データ

### 2.4 UI/UX機能
- **ローディング表示**: API呼び出し中の待機画面
- **エラーハンドリング**: わかりやすいエラーメッセージ
- **レスポンシブデザイン**: スマホ・タブレット対応
- **天気アイコン**: 天気コードに応じたビジュアル表示
- **お気に入り機能**: よく見る都道府県の保存（LocalStorage）

## 3. 非機能要件

### 3.1 パフォーマンス
- ページ読み込み時間: 3秒以内
- API レスポンス時間: 5秒以内

### 3.2 可用性
- 稼働率: 開発環境では制限なし
- エラー時の適切なメッセージ表示

### 3.3 セキュリティ
- SQLインジェクション対策
- XSS対策
- CSRF対策（Spring Securityで対応）

### 3.4 互換性
- ブラウザ対応: Chrome, Firefox, Edge（最新版）
- モバイル対応: iOS Safari, Android Chrome

### 3.5 保守性
- コードの可読性
- 適切なコメント
- ドキュメント整備

## 4. 技術スタック

### 4.1 バックエンド
- Java 17
- Spring Boot 3.x
- Spring Data JPA
- Gradle

### 4.2 フロントエンド
- Thymeleaf
- HTML5/CSS3
- JavaScript（バニラ）

### 4.3 データベース
- MySQL 8.0

### 4.4 外部API
- Open-Meteo API (https://open-meteo.com/)

## 5. 画面一覧

| 画面ID | 画面名 | URL | 説明 |
|--------|--------|-----|------|
| HOME | トップページ | / | 47都道府県一覧 |
| DETAIL | 天気詳細 | /weather/{prefectureId} | 選択都道府県の天気 |
| ERROR_404 | 404エラー | /error/404 | ページが見つからない |
| ERROR_500 | 500エラー | /error/500 | サーバーエラー |

## 6. データベース構成（概要）

### 6.1 テーブル一覧
1. prefectures（都道府県マスタ）
2. weather_records（天気記録）
3. daily_forecasts（日次予報）

詳細は別途ER図で定義

## 7. 外部連携

### 7.1 Open-Meteo API
- **エンドポイント**: https://api.open-meteo.com/v1/forecast
- **認証**: 不要（無料プラン）
- **レート制限**: 10,000リクエスト/日

## 8. 制約事項・前提条件

### 8.1 制約事項
- インターネット接続が必要
- Open-Meteo APIの利用制限に従う

### 8.2 前提条件
- JDK 17以上
- MySQL 8.0以上
- モダンブラウザ

## 9. 今後の拡張性

### 9.1 将来的な機能追加候補
- ユーザー認証機能
- お気に入り地点の永続化
- 天気アラート機能
- 過去の天気データ分析

## 10. 成功基準

- [ ] 47都道府県の天気が正しく表示される
- [ ] 週間天気予報が表示される
- [ ] データベースに履歴が保存される
- [ ] スマホでも快適に閲覧できる
- [ ] エラーが適切に処理される
```

**成果物:**
- `requirements.md`

---

### 2. Open-Meteo APIの調査（11:00-12:00）

**手順:**

1. Open-Meteo公式サイトにアクセス
   - https://open-meteo.com/

2. APIドキュメントを読む
   - https://open-meteo.com/en/docs

3. 重要なポイントを`api-research.md`にまとめる：

```markdown
# Open-Meteo API 調査レポート

## APIの概要

Open-Meteoは無料で使える天気予報API

### 特徴
- **無料**: 商用利用も可能
- **認証不要**: API キーやトークン不要
- **高速**: レスポンスが速い
- **豊富なデータ**: 様々な気象データを提供

## エンドポイント

### Weather Forecast API
```
GET https://api.open-meteo.com/v1/forecast
```

## 必須パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|---|------|-----|
| latitude | float | 緯度 | 35.6895 |
| longitude | float | 経度 | 139.6917 |

## オプションパラメータ

### current（現在の天気）
```
current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m
```

利用可能な値：
- `temperature_2m`: 地上2mの気温（℃）
- `weathercode`: 天気コード
- `windspeed_10m`: 風速（m/s）
- `relativehumidity_2m`: 相対湿度（%）
- `apparent_temperature`: 体感温度
- `precipitation`: 降水量
- `cloudcover`: 雲量

### daily（日次予報）
```
daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum
```

利用可能な値：
- `temperature_2m_max`: 最高気温
- `temperature_2m_min`: 最低気温
- `weathercode`: 天気コード
- `precipitation_sum`: 降水量合計
- `sunrise`: 日の出時刻
- `sunset`: 日の入り時刻

### その他のパラメータ
- `timezone`: タイムゾーン（例: Asia/Tokyo）
- `forecast_days`: 予報日数（1-16日、デフォルト7日）

## 天気コード（WMO Weather Code）

| コード | 説明 | アイコン候補 |
|--------|------|------------|
| 0 | 快晴 | ☀️ |
| 1, 2, 3 | 晴れ、一部曇り、曇り | 🌤️ ⛅ ☁️ |
| 45, 48 | 霧 | 🌫️ |
| 51, 53, 55 | 霧雨 | 🌦️ |
| 61, 63, 65 | 雨 | 🌧️ |
| 71, 73, 75 | 雪 | ❄️ |
| 77 | 雪の粒 | 🌨️ |
| 80, 81, 82 | にわか雨 | 🌦️ |
| 85, 86 | にわか雪 | 🌨️ |
| 95 | 雷雨 | ⛈️ |
| 96, 99 | 雷雨（雹） | ⛈️ |

## リクエスト例

### 東京の現在の天気
```
GET https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m&timezone=Asia/Tokyo
```

### 東京の週間天気予報
```
GET https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum&timezone=Asia/Tokyo&forecast_days=7
```

### 現在 + 週間予報
```
GET https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum&timezone=Asia/Tokyo&forecast_days=7
```

## レスポンス例

```json
{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "generationtime_ms": 0.123,
  "utc_offset_seconds": 32400,
  "timezone": "Asia/Tokyo",
  "timezone_abbreviation": "JST",
  "elevation": 40.0,
  "current": {
    "time": "2024-01-04T15:00",
    "temperature_2m": 12.5,
    "weathercode": 1,
    "windspeed_10m": 3.2,
    "relativehumidity_2m": 65
  },
  "daily": {
    "time": ["2024-01-04", "2024-01-05", ...],
    "temperature_2m_max": [15.2, 14.8, ...],
    "temperature_2m_min": [8.1, 7.5, ...],
    "weathercode": [1, 3, ...],
    "precipitation_sum": [0.0, 2.5, ...]
  }
}
```

## レート制限

- **無料プラン**: 10,000リクエスト/日
- **商用利用**: 可能

## エラーレスポンス

### パラメータエラー
```json
{
  "error": true,
  "reason": "Latitude must be in range of -90 to 90°. Given: 200."
}
```

## 47都道府県の緯度・経度

| 都道府県 | 緯度 | 経度 |
|---------|------|------|
| 北海道 | 43.064 | 141.347 |
| 青森県 | 40.824 | 140.740 |
| 岩手県 | 39.704 | 141.153 |
| ... | ... | ... |

（完全なリストは別途CSVで管理）

## 実装方針

1. **47都道府県マスタ作成**
   - prefecturesテーブルに緯度・経度を保存

2. **API呼び出し**
   - RestTemplateまたはWebClientを使用
   - タイムアウト設定: 5秒

3. **データ保存**
   - API取得後、weather_recordsテーブルに保存

4. **キャッシュ戦略**
   - 同じ都道府県は1時間以内は再取得しない（任意）
```

**成果物:**
- `api-research.md`

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. PostmanでAPIテスト（13:00-15:00）

**手順:**

1. Postmanを起動

2. 新しいリクエストを作成

3. 東京の現在の天気を取得
   - **Method**: GET
   - **URL**: 
   ```
   https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m&timezone=Asia/Tokyo
   ```
   - **Send**をクリック

4. レスポンスを確認
   - Statusが200 OKであることを確認
   - JSONレスポンスを確認

5. 週間天気予報を取得
   - **URL**:
   ```
   https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum&timezone=Asia/Tokyo&forecast_days=7
   ```

6. 複数の都道府県でテスト
   - 北海道: `latitude=43.064&longitude=141.347`
   - 大阪: `latitude=34.686&longitude=135.520`
   - 福岡: `latitude=33.590&longitude=130.402`
   - 沖縄: `latitude=26.212&longitude=127.681`

7. エラーケースもテスト
   - 緯度が範囲外: `latitude=200&longitude=139.6917`
   - 必須パラメータなし: パラメータを削除

8. Postmanコレクションとして保存
   - コレクション名: "Weather App API Tests"
   - リクエストを整理

**演習:**

`postman-test-results.md`を作成：

```markdown
# Postman APIテスト結果

## テスト日時
2024-01-XX XX:XX

## テストケース

### 1. 東京の現在天気取得
- **URL**: https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode&timezone=Asia/Tokyo
- **Result**: ✅ 成功
- **Status**: 200 OK
- **Response Time**: 245ms
- **Temperature**: 12.5℃
- **Weather Code**: 1

### 2. 東京の週間予報取得
- **URL**: https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Tokyo&forecast_days=7
- **Result**: ✅ 成功
- **Status**: 200 OK
- **Response Time**: 198ms
- **Days**: 7日分のデータ取得確認

### 3. 北海道の天気取得
- **URL**: https://api.open-meteo.com/v1/forecast?latitude=43.064&longitude=141.347&current=temperature_2m,weathercode&timezone=Asia/Tokyo
- **Result**: ✅ 成功
- **Temperature**: -2.3℃

### 4. エラーケース: 無効な緯度
- **URL**: https://api.open-meteo.com/v1/forecast?latitude=200&longitude=139.6917&current=temperature_2m
- **Result**: ✅ エラーハンドリング確認
- **Status**: 400 Bad Request
- **Error Message**: "Latitude must be in range of -90 to 90°"

## 学んだこと

1. APIレスポンスは非常に高速（200-300ms）
2. 天気コードは数値で返却される
3. タイムゾーン指定が重要
4. エラーメッセージが明確

## 次のステップ

- Javaでの実装準備
- DTOクラスの設計
- RestTemplateの設定
```

**成果物:**
- Postmanコレクション（エクスポートしてJSONファイル保存）
- `postman-test-results.md`
- 各テストのスクリーンショット

---

### 4. 47都道府県データの準備（15:00-16:30）

**手順:**

47都道府県の緯度・経度データをCSVで準備

`prefectures.csv`を作成：

```csv
id,name,name_en,latitude,longitude,region
1,北海道,Hokkaido,43.064,141.347,北海道
2,青森県,Aomori,40.824,140.740,東北
3,岩手県,Iwate,39.704,141.153,東北
4,宮城県,Miyagi,38.269,140.872,東北
5,秋田県,Akita,39.719,140.103,東北
6,山形県,Yamagata,38.241,140.364,東北
7,福島県,Fukushima,37.750,140.468,東北
8,茨城県,Ibaraki,36.341,140.447,関東
9,栃木県,Tochigi,36.566,139.883,関東
10,群馬県,Gunma,36.391,139.061,関東
11,埼玉県,Saitama,35.857,139.649,関東
12,千葉県,Chiba,35.605,140.123,関東
13,東京都,Tokyo,35.689,139.692,関東
14,神奈川県,Kanagawa,35.448,139.643,関東
15,新潟県,Niigata,37.902,139.023,中部
16,富山県,Toyama,36.695,137.211,中部
17,石川県,Ishikawa,36.595,136.626,中部
18,福井県,Fukui,36.065,136.222,中部
19,山梨県,Yamanashi,35.664,138.568,中部
20,長野県,Nagano,36.651,138.181,中部
21,岐阜県,Gifu,35.391,136.722,中部
22,静岡県,Shizuoka,34.977,138.383,中部
23,愛知県,Aichi,35.180,136.907,中部
24,三重県,Mie,34.730,136.509,関西
25,滋賀県,Shiga,35.004,135.869,関西
26,京都府,Kyoto,35.021,135.756,関西
27,大阪府,Osaka,34.686,135.520,関西
28,兵庫県,Hyogo,34.691,135.183,関西
29,奈良県,Nara,34.685,135.833,関西
30,和歌山県,Wakayama,34.226,135.168,関西
31,鳥取県,Tottori,35.504,134.238,中国
32,島根県,Shimane,35.472,133.051,中国
33,岡山県,Okayama,34.662,133.935,中国
34,広島県,Hiroshima,34.397,132.460,中国
35,山口県,Yamaguchi,34.186,131.471,中国
36,徳島県,Tokushima,34.066,134.559,四国
37,香川県,Kagawa,34.340,134.043,四国
38,愛媛県,Ehime,33.842,132.766,四国
39,高知県,Kochi,33.560,133.531,四国
40,福岡県,Fukuoka,33.606,130.418,九州
41,佐賀県,Saga,33.249,130.299,九州
42,長崎県,Nagasaki,32.745,129.874,九州
43,熊本県,Kumamoto,32.790,130.742,九州
44,大分県,Oita,33.238,131.613,九州
45,宮崎県,Miyazaki,31.911,131.424,九州
46,鹿児島県,Kagoshima,31.560,130.558,九州
47,沖縄県,Okinawa,26.212,127.681,沖縄
```

**このデータの活用方法:**
- データベースの初期データとして投入
- APIリクエスト時の緯度・経度として使用

**成果物:**
- `prefectures.csv`

---

### 5. 要件とAPIの統合確認（16:30-17:00）

**手順:**

`integration-check.md`を作成：

```markdown
# 要件とAPI仕様の統合確認

## 1. トップページ

### 要件
- 47都道府県の一覧表示

### 実装方針
- `prefectures.csv`をデータベースに投入
- `PrefectureRepository.findAll()`で全件取得
- Thymeleafで一覧表示

### 必要なAPI呼び出し
- なし（マスタデータのみ）

---

## 2. 天気詳細ページ

### 要件
- 現在の天気表示
- 週間天気予報（7日間）

### 実装方針
1. URLから都道府県IDを取得
2. データベースから緯度・経度を取得
3. Open-Meteo APIを呼び出し
4. レスポンスをDTOに変換
5. データベースに保存
6. Thymeleafで表示

### 必要なAPI呼び出し
```
GET https://api.open-meteo.com/v1/forecast
  ?latitude={lat}
  &longitude={lon}
  &current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m
  &daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum
  &timezone=Asia/Tokyo
  &forecast_days=7
```

---

## 3. データ保存

### 要件
- API取得データの履歴保存

### 実装方針
- `WeatherRecord`エンティティ作成
- API取得後、`WeatherRecordRepository.save()`

---

## 4. UI/UX

### ローディング表示
- JavaScript + CSSで実装

### エラーハンドリング
- Spring MVCの@ControllerAdvice
- カスタムエラーページ

### レスポンシブデザイン
- CSSメディアクエリ

### 天気アイコン
- 天気コードとアイコンのマッピング

### お気に入り機能
- LocalStorageで実装

---

## 5. 技術的課題と解決策

### 課題1: APIレスポンスの遅延
**解決策**: ローディング表示 + タイムアウト設定

### 課題2: 同時アクセス時のAPI制限
**解決策**: キャッシュ機能（任意）

### 課題3: エラー時のユーザー体験
**解決策**: わかりやすいエラーメッセージ

---

## 6. 次週からの開発フロー

- Day 7: API動作確認とレスポンス解析
- Day 8-9: 画面設計
- Day 10-12: データベース設計
- Day 13-15: シーケンス図と設計レビュー
- Day 16以降: 実装開始
```

**成果物:**
- `integration-check.md`

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] 要件定義書が完成した
- [ ] Open-Meteo APIの仕様を理解した
- [ ] Postmanでのテストが成功した
- [ ] 47都道府県データを準備した
- [ ] 要件とAPIの統合確認が完了した
- [ ] すべてのドキュメントが作成された
- [ ] GitHubにコミット・プッシュした

---

## 📚 参考リンク

- [Open-Meteo公式ドキュメント](https://open-meteo.com/en/docs)
- [WMO Weather Code](https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM)

---

## 🎉 完了後

次は [Day 7](day-07.md) へ進む

お疲れさまでした！
