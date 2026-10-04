# Day 15: 設計レビューと修正

## 📅 実施日
- 予定: Week 3 - Day 15
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
これまでの設計ドキュメントをレビューし、必要な修正を行う

---

## 午前の作業（9:00-13:00）

### 1. 設計ドキュメントの棚卸し（9:00-10:00）

**作成済みドキュメント一覧:**

```markdown
## Week 2: 設計基礎
- Day 6: requirements.md（要件定義書）
- Day 6: api-research.md（API調査レポート）
- Day 7: api-response-analysis.md（APIレスポンス解析）
- Day 7: dto-design.md（DTO設計書）
- Day 7: rest-template-design.md（RestTemplate設計）

## Week 2-3: 画面・DB・シーケンス設計
- Day 8: wireframe-top-page.png（トップページ）
- Day 8: wireframe-detail-page.png（詳細ページ）
- Day 8: screen-design-document.md（画面設計書）
- Day 9: screen-transition-diagram.png（画面遷移図）
- Day 9: user-flow.md（ユーザーフロー）
- Day 10: database-design.md（ER図）
- Day 11: table-definitions.md（テーブル定義書）
- Day 11: schema.sql（DDL）
- Day 12: data.sql（初期データ）
- Day 13: sequence-diagram-top-page.png（トップページシーケンス）
- Day 14: sequence-diagram-weather-detail.png（詳細ページシーケンス）
```

チェックリストを作成：
```markdown
# 設計ドキュメント チェックリスト

## 要件定義
- [ ] 機能要件が明確
- [ ] 非機能要件が定義されている
- [ ] 画面一覧が完全
- [ ] 制約事項が明記されている

## API調査
- [ ] エンドポイントが正しい
- [ ] パラメータが網羅されている
- [ ] レスポンス形式が理解できている
- [ ] エラーケースが考慮されている

## 画面設計
- [ ] ワイヤーフレームが完成
- [ ] 画面遷移が明確
- [ ] レスポンシブ対応が考慮されている
- [ ] エラー画面が設計されている

## データベース設計
- [ ] ER図が完成
- [ ] テーブル定義が完全
- [ ] インデックスが設計されている
- [ ] 外部キー制約が適切

## シーケンス図
- [ ] メインフローが図示されている
- [ ] エラーケースが考慮されている
- [ ] API連携が明確
- [ ] データベース保存が図示されている
```

---

### 2. 要件定義のレビュー（10:00-11:00）

**確認項目:**

1. **機能要件の漏れチェック**
   - トップページ: ✅ OK
   - 詳細ページ: ✅ OK
   - エラーページ: ✅ OK
   - お気に入り機能: ⚠️ 任意だが詳細化が必要

2. **非機能要件の追加**
   ```markdown
   ### セキュリティ（追加）
   - [ ] HTTPS通信（本番環境）
   - [ ] SQLインジェクション対策（Spring Data JPA使用）
   - [ ] XSS対策（Thymeleafのエスケープ機能）
   ```

---

### 3. データベース設計のレビュー（11:00-12:00）

**確認項目:**

1. **テーブル構造の妥当性**
   ```sql
   -- ✅ prefectures: OK
   -- ✅ weather_records: OK
   -- ✅ daily_forecasts: OK
   ```

2. **追加すべきカラムの検討**
   ```sql
   -- weather_records に追加を検討
   ALTER TABLE weather_records 
   ADD COLUMN api_response_json TEXT COMMENT 'APIレスポンス全体（デバッグ用）';
   
   -- インデックス追加
   CREATE INDEX idx_weather_records_prefecture_fetched 
   ON weather_records(prefecture_id, fetched_at DESC);
   ```

3. **制約の確認**
   - ON DELETE CASCADE: ✅ 適切
   - UNIQUE制約: 必要に応じて追加検討

---

## 午後の作業（13:00-17:00）

### 4. シーケンス図の修正（13:00-14:30）

**修正ポイント:**

1. **トップページのシーケンス図**
   - 地域フィルタ機能を明記
   - キャッシング処理を追加（任意機能）

2. **詳細ページのシーケンス図**
   - ローディング状態の表示を追加
   - リトライ処理を追加

**修正版シーケンス図を作成:**
```
ブラウザ → Controller: リクエスト送信
Controller → ブラウザ: ローディング画面返却
ブラウザ: ローディング表示（JavaScript）
ブラウザ → Controller: AJAXでAPI呼び出し
Controller → API: 天気情報取得
API → Controller: レスポンス
Controller → DB: データ保存
Controller → ブラウザ: JSON返却
ブラウザ: 画面更新
```

---

### 5. クラス設計の詳細化（14:30-16:00）

**Entityクラス設計:**

```java
// Prefecture.java
@Entity
@Table(name = "prefectures")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Prefecture {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 10)
    private String name;
    
    @Column(name = "name_en", nullable = false, length = 50)
    private String nameEn;
    
    @Column(nullable = false, precision = 9, scale = 6)
    private Double latitude;
    
    @Column(nullable = false, precision = 9, scale = 6)
    private Double longitude;
    
    @Column(nullable = false, length = 20)
    private String region;
    
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

**DTOクラス設計:**

```java
// WeatherDetailDto.java
@Data
@Builder
public class WeatherDetailDto {
    // 都道府県情報
    private Long prefectureId;
    private String prefectureName;
    
    // 現在の天気
    private CurrentWeatherDto current;
    
    // 週間予報
    private List<DailyForecastDto> dailyForecasts;
    
    // メタ情報
    private LocalDateTime fetchedAt;
}

// CurrentWeatherDto.java
@Data
@Builder
public class CurrentWeatherDto {
    private LocalDateTime time;
    private Double temperature;
    private Integer weatherCode;
    private String weatherDescription;  // 天気コードから生成
    private String weatherIcon;         // 天気コードから生成
    private Double windSpeed;
    private Integer humidity;
    private Double apparentTemperature;
}

// DailyForecastDto.java
@Data
@Builder
public class DailyForecastDto {
    private LocalDate date;
    private Double temperatureMax;
    private Double temperatureMin;
    private Integer weatherCode;
    private String weatherDescription;
    private String weatherIcon;
    private Double precipitationSum;
}
```

---

### 6. 設計書の最終更新（16:00-17:00）

**`design-summary.md`を作成:**

```markdown
# 設計書サマリー

## プロジェクト概要
47都道府県の天気情報を表示するWebアプリケーション

---

## アーキテクチャ

### レイヤー構成
```
Presentation Layer (View)
    ↓
Controller Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database Layer

External API Client
    ↓
Open-Meteo API
```

---

## 主要コンポーネント

### Controller
- HomeController: トップページ
- WeatherController: 天気詳細ページ
- ErrorController: エラーページ

### Service
- PrefectureService: 都道府県マスタ管理
- WeatherService: 天気情報取得・保存

### Repository
- PrefectureRepository: JpaRepository<Prefecture, Long>
- WeatherRecordRepository: JpaRepository<WeatherRecord, Long>
- DailyForecastRepository: JpaRepository<DailyForecast, Long>

### External Client
- OpenMeteoClient: Open-Meteo API連携

---

## データフロー

### 1. トップページ表示
```
User → Browser → HomeController 
    → PrefectureService 
    → PrefectureRepository 
    → Database
```

### 2. 天気詳細表示
```
User → Browser → WeatherController
    → WeatherService
        → OpenMeteoClient → Open-Meteo API
        → WeatherRecordRepository → Database
    → View
```

---

## セキュリティ

### 実装済み
- SQLインジェクション対策（JPA）
- XSS対策（Thymeleaf自動エスケープ）
- CSRF対策（Spring Security、今回は無効化）

### 今後の検討
- HTTPS化（本番環境）
- レート制限
- ユーザー認証

---

## パフォーマンス

### 目標値
- トップページ: 300ms以内
- 詳細ページ: 1000ms以内（API含む）

### 最適化
- データベースインデックス
- 都道府県マスタのキャッシング（任意）

---

## エラーハンドリング

### エラー種類
1. 404 Not Found: 存在しないページ
2. 500 Internal Server Error: サーバーエラー
3. API Error: 外部API障害

### 対応
- GlobalExceptionHandlerで一元管理
- ユーザーフレンドリーなエラーページ
```

---

## ✅ チェックリスト

- [ ] 設計ドキュメントの棚卸し完了
- [ ] 要件定義のレビュー完了
- [ ] データベース設計のレビュー完了
- [ ] シーケンス図の修正完了
- [ ] クラス設計の詳細化完了
- [ ] 設計書サマリー作成完了
- [ ] GitHubにコミット・プッシュ

---

## 📝 本日のまとめ

設計フェーズが完了し、実装に移る準備が整った

---

## 🎉 完了後

次は [Day 16](day-16.md) から実装開始！

お疲れさまでした！
