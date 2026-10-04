# Day 37: ドキュメント作成

## 📅 実施日
- 予定: Week 8 - Day 37
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
プロジェクトの包括的なドキュメントを作成し、保守性と引き継ぎ性を高める

---

## 📋 午前の作業（9:00-13:00）

### 1. README作成（9:00-10:30）

**プロジェクトルートのREADME.md:**

\`\`\`markdown
# 天気予報アプリ

## 概要

47都道府県の天気情報を提供するWebアプリケーション。Open-Meteo APIを使用してリアルタイムの天気データを取得し、見やすいUIで表示します。

## 主な機能

- 🌤️ 47都道府県の天気情報表示
- 📊 7日間の天気予報
- 🔍 都道府県検索・地域フィルタ
- ⭐ お気に入り機能
- 📱 レスポンシブデザイン
- ♿ アクセシビリティ対応（WCAG 2.1準拠）

## 技術スタック

### バックエンド
- Java 17
- Spring Boot 3.5.x
- Spring Data JPA
- MySQL 8.0
- Gradle

### フロントエンド
- Thymeleaf
- HTML5/CSS3
- JavaScript (ES6+)
- レスポンシブデザイン

### テスト
- JUnit 5
- Mockito
- Spring Boot Test
- JaCoCo（カバレッジ82%）

### 外部API
- [Open-Meteo API](https://open-meteo.com/)

## セットアップ

### 前提条件

- Java 17以上
- MySQL 8.0以上
- Gradle 8.0以上

### インストール手順

1. リポジトリのクローン

\`\`\`bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
\`\`\`

2. データベース作成

\`\`\`sql
CREATE DATABASE weather_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
\`\`\`

3. 設定ファイル編集

\`application.properties\`を編集：

\`\`\`properties
spring.datasource.url=jdbc:mysql://localhost:3306/weather_app
spring.datasource.username=your_username
spring.datasource.password=your_password
\`\`\`

4. アプリケーション起動

\`\`\`bash
./gradlew bootRun
\`\`\`

5. ブラウザでアクセス

\`\`\`
http://localhost:8080
\`\`\`

## ディレクトリ構成

\`\`\`
weather-app/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/weatherapp/
│   │   │       ├── client/          # 外部API連携
│   │   │       ├── config/          # 設定
│   │   │       ├── controller/      # コントローラー
│   │   │       ├── dto/             # データ転送オブジェクト
│   │   │       ├── entity/          # エンティティ
│   │   │       ├── exception/       # 例外
│   │   │       ├── mapper/          # マッパー
│   │   │       ├── repository/      # リポジトリ
│   │   │       ├── service/         # サービス
│   │   │       └── util/            # ユーティリティ
│   │   └── resources/
│   │       ├── static/
│   │       │   ├── css/             # スタイルシート
│   │       │   ├── js/              # JavaScript
│   │       │   └── images/          # 画像
│   │       └── templates/           # Thymeleafテンプレート
│   └── test/                        # テストコード
├── docs/                            # ドキュメント
├── build.gradle                     # Gradle設定
└── README.md
\`\`\`

## API仕様

### エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | / | トップページ |
| GET | /weather/{id} | 都道府県別天気詳細 |
| GET | /?region={region} | 地域フィルタ |

## テスト

### テスト実行

\`\`\`bash
./gradlew test
\`\`\`

### カバレッジレポート

\`\`\`bash
./gradlew jacocoTestReport
\`\`\`

レポート: \`build/reports/jacoco/test/html/index.html\`

## デプロイ

### 本番ビルド

\`\`\`bash
./gradlew clean build
\`\`\`

### Jarファイル実行

\`\`\`bash
java -jar build/libs/weather-app-0.0.1-SNAPSHOT.jar
\`\`\`

## ライセンス

MIT License

## 作者

新入社員研修プロジェクト

## 謝辞

- Open-Meteo API
- Spring Boot
- Thymeleaf
\`\`\`

---

### 2. API仕様書作成（10:30-12:00）

**docs/API.md:**

\`\`\`markdown
# API仕様書

## 概要

天気予報アプリのAPI仕様を記載します。

## エンドポイント

### 1. トップページ

**エンドポイント:** \`GET /\`

**説明:** 47都道府県の一覧を地域別に表示

**クエリパラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| region | String | No | 地域フィルタ（北海道、東北、関東、中部、関西、中国、四国、九州、沖縄） |

**レスポンス:**

- ステータス: 200 OK
- Content-Type: text/html
- ビュー: index.html

**例:**

\`\`\`
GET /?region=関東
\`\`\`

### 2. 天気詳細ページ

**エンドポイント:** \`GET /weather/{id}\`

**説明:** 指定した都道府県の天気情報を表示

**パスパラメータ:**

| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| id | Long | Yes | 都道府県ID（1-47） |

**レスポンス:**

- ステータス: 200 OK
- Content-Type: text/html
- ビュー: weather-detail.html

**エラー:**

- 404 Not Found: 都道府県が見つからない
- 503 Service Unavailable: API接続エラー

**例:**

\`\`\`
GET /weather/13  # 東京都
\`\`\`

## データモデル

### Prefecture（都道府県）

\`\`\`json
{
  "id": 13,
  "name": "東京都",
  "nameEn": "Tokyo",
  "region": "関東",
  "latitude": 35.6895,
  "longitude": 139.6917
}
\`\`\`

### WeatherDetail（天気詳細）

\`\`\`json
{
  "prefecture": {
    "id": 13,
    "name": "東京都"
  },
  "current": {
    "time": "2024-01-05T15:00:00",
    "temperature": 15.5,
    "apparentTemperature": 14.2,
    "weatherCode": 1,
    "weatherDescription": "晴れ",
    "humidity": 65,
    "windSpeed": 3.2,
    "precipitation": 0.0,
    "cloudCover": 20
  },
  "dailyForecasts": [
    {
      "date": "2024-01-05",
      "dayOfWeek": "金",
      "temperatureMax": 18.0,
      "temperatureMin": 10.0,
      "weatherCode": 1,
      "weatherDescription": "晴れ",
      "precipitationSum": 0.0,
      "sunrise": "2024-01-05T06:50:00",
      "sunset": "2024-01-05T16:38:00"
    }
  ],
  "fetchedAt": "2024-01-05T15:30:00"
}
\`\`\`

## エラーコード

| コード | 説明 | 対処方法 |
|--------|------|----------|
| 400 | 不正なリクエスト | リクエストパラメータを確認 |
| 404 | リソースが見つからない | URLを確認 |
| 500 | サーバーエラー | 管理者に連絡 |
| 503 | サービス利用不可 | しばらく待ってリトライ |
\`\`\`

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. 開発ガイド作成（13:00-14:30）

**docs/DEVELOPMENT.md:**

\`\`\`markdown
# 開発ガイド

## 開発環境セットアップ

### IDE設定

#### IntelliJ IDEA推奨設定

1. Lombok Plugin インストール
2. Enable annotation processing
3. Code Style: Google Java Style

#### VS Code推奨設定

1. Extension Pack for Java
2. Spring Boot Extension Pack
3. Lombok Annotations Support

### コーディング規約

#### Java

- インデント: 4スペース
- 行の長さ: 120文字以内
- 命名規則: キャメルケース
- JavaDoc: public メソッドに必須

#### CSS

- インデント: 2スペース
- BEM命名規則
- CSS変数を活用

#### JavaScript

- インデント: 2スペース
- ES6+構文使用
- セミコロン必須

### Git運用

#### ブランチ戦略

\`\`\`
main          # 本番
  └─ develop  # 開発
      └─ feature/xxx  # 機能開発
\`\`\`

#### コミットメッセージ

\`\`\`
<type>(<scope>): <subject>

feat: 新機能
fix: バグ修正
docs: ドキュメント
style: フォーマット
refactor: リファクタリング
test: テスト追加
chore: ビルド・ツール
\`\`\`

例:
\`\`\`
feat(weather): 7日間予報機能追加
fix(ui): レスポンシブ表示の不具合修正
\`\`\`

## ビルド・デプロイ

### ローカルビルド

\`\`\`bash
./gradlew clean build
\`\`\`

### 開発サーバー起動

\`\`\`bash
./gradlew bootRun
\`\`\`

### 本番ビルド

\`\`\`bash
./gradlew clean build -Pprofile=prod
\`\`\`

## トラブルシューティング

### よくある問題

#### ポート8080が使用中

\`\`\`bash
# プロセス確認
lsof -i :8080

# プロセス停止
kill -9 <PID>
\`\`\`

#### MySQLに接続できない

1. MySQLが起動しているか確認
2. ユーザー名・パスワードを確認
3. データベースが作成されているか確認

#### テストが失敗する

\`\`\`bash
./gradlew clean test --info
\`\`\`
\`\`\`

---

### 4. 運用マニュアル作成（14:30-16:00）

**docs/OPERATION.md:**

\`\`\`markdown
# 運用マニュアル

## デプロイ手順

### 1. 事前準備

- [ ] コードレビュー完了
- [ ] テスト全パス確認
- [ ] ドキュメント更新
- [ ] リリースノート作成

### 2. デプロイ

\`\`\`bash
# 本番ビルド
./gradlew clean build -Pprofile=prod

# バックアップ
cp app.jar app.jar.backup

# デプロイ
cp build/libs/weather-app.jar app.jar

# 起動
java -jar app.jar
\`\`\`

### 3. 動作確認

- [ ] トップページ表示確認
- [ ] 天気情報取得確認
- [ ] エラーページ確認
- [ ] レスポンスタイム確認

## 監視

### ヘルスチェック

\`\`\`bash
curl http://localhost:8080/actuator/health
\`\`\`

### ログ確認

\`\`\`bash
tail -f logs/application.log
\`\`\`

## バックアップ

### データベースバックアップ

\`\`\`bash
mysqldump -u root -p weather_app > backup_\$(date +%Y%m%d).sql
\`\`\`

### リストア

\`\`\`bash
mysql -u root -p weather_app < backup_20240105.sql
\`\`\`

## 障害対応

### 障害レベル

| レベル | 説明 | 対応時間 |
|--------|------|----------|
| Critical | サービス停止 | 即時 |
| High | 主要機能停止 | 1時間以内 |
| Medium | 一部機能停止 | 4時間以内 |
| Low | 軽微な不具合 | 1営業日以内 |

### エスカレーション

1. 開発チーム
2. リードエンジニア
3. プロジェクトマネージャー
\`\`\`

---

### 5. リリースノート作成（16:00-17:00）

**docs/CHANGELOG.md:**

\`\`\`markdown
# リリースノート

## [1.0.0] - 2024-01-05

### 新機能
- ✨ 47都道府県の天気情報表示
- ✨ 7日間の天気予報
- ✨ 都道府県検索・地域フィルタ
- ✨ お気に入り機能
- ✨ レスポンシブデザイン
- ✨ アクセシビリティ対応（WCAG 2.1準拠）

### 技術スタック
- Java 17
- Spring Boot 3.5.x
- MySQL 8.0
- Thymeleaf
- Open-Meteo API

### テスト
- 単体テスト: 85件
- 統合テスト: 25件
- カバレッジ: 82%

### ドキュメント
- README
- API仕様書
- 開発ガイド
- 運用マニュアル

## [0.9.0] - 2024-01-04（ベータ版）

### 新機能
- 基本的な天気表示機能
- データベース連携

### 改善
- パフォーマンス最適化
- エラーハンドリング強化

### 既知の問題
- なし
\`\`\`

---

## ✅ チェックリスト

- [ ] README.mdを作成した
- [ ] API仕様書を作成した
- [ ] 開発ガイドを作成した
- [ ] 運用マニュアルを作成した
- [ ] リリースノートを作成した
- [ ] JavaDocを記載した
- [ ] コメントを記載した
- [ ] ドキュメントをレビューした
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "docs: プロジェクトドキュメント作成完了"
git push origin main
```

---

## 📚 参考リンク

### ドキュメント作成
- [Markdown Guide](https://www.markdownguide.org/)
- [JavaDoc（日本語）](https://www.oracle.com/jp/technical-resources/articles/java/javadoc-tool.html)

### ドキュメント管理
- [Read the Docs](https://readthedocs.org/)
- [GitHub Pages](https://pages.github.com/)

---

## 📝 本日のまとめ

1. **作成したドキュメント:**
   - README
   - API仕様書
   - 開発ガイド
   - 運用マニュアル
   - リリースノート

2. **学んだこと:**
   - ドキュメント作成の重要性
   - 保守性の向上
   - 引き継ぎ性の確保

3. **明日への引き継ぎ:**
   - Day 38でパフォーマンス最適化

---

## 🎉 完了後

次は [Day 38](day-38.md) へ

お疲れさまでした！
