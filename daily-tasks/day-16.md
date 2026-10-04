# Day 16: Entityクラス実装

## 📅 実施日
- 予定: Week 4 - Day 16
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Prefecture、WeatherRecord、DailyForecastの3つのEntityクラスを実装し、JPAでデータベースとマッピングする

---

## 📋 午前の作業（9:00-13:00）

### 1. JPAとEntityの基礎理解（9:00-10:00）

**Entityとは:**
- データベースのテーブルと1対1で対応するJavaクラス
- `@Entity`アノテーションを付与
- フィールドがテーブルのカラムに対応

**主要なアノテーション:**

```java
@Entity              // このクラスがEntityであることを示す
@Table               // テーブル名を指定（省略可）
@Id                  // 主キーを示す
@GeneratedValue      // 主キーの自動生成戦略
@Column              // カラム名や制約を指定
@OneToMany           // 1対多のリレーション
@ManyToOne           // 多対1のリレーション
@JoinColumn          // 外部キーのカラム名
@Temporal            // 日時型の精度指定
@PrePersist          // INSERT前に実行
@PreUpdate           // UPDATE前に実行
```

**学習用ドキュメント作成:**

`jpa-entity-guide.md`を作成：

```markdown
# JPA Entity 実装ガイド

## 基本的なEntityの構造

```java
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 50)
    private String name;
    
    @Column(unique = true)
    private String email;
    
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
```

## アノテーション詳細

### @GeneratedValue の戦略

- **IDENTITY**: データベースのAUTO_INCREMENT使用（MySQL推奨）
- **SEQUENCE**: シーケンスを使用（PostgreSQL等）
- **TABLE**: 専用テーブルで管理
- **AUTO**: データベースに応じて自動選択

### @Column の主要属性

- `name`: カラム名（Javaのフィールド名と異なる場合）
- `nullable`: NULL許可（デフォルトtrue）
- `unique`: ユニーク制約
- `length`: 文字列の最大長
- `precision`, `scale`: 数値の精度（`BigDecimal` / `DECIMAL` のカラム用。`Double` には指定しない）

### リレーションシップ

#### @OneToMany（1対多）
```java
@Entity
public class Parent {
    @Id
    private Long id;
    
    @OneToMany(mappedBy = "parent", cascade = CascadeType.ALL)
    private List<Child> children;
}
```

#### @ManyToOne（多対1）
```java
@Entity
public class Child {
    @Id
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "parent_id")
    private Parent parent;
}
```

## Lombokとの組み合わせ

```java
@Entity
@Data                    // getter/setter/toString/equals/hashCode
@NoArgsConstructor      // 引数なしコンストラクタ
@AllArgsConstructor     // 全フィールドコンストラクタ
@Builder                // ビルダーパターン
public class Sample {
    @Id
    private Long id;
    private String name;
}
```

**使い方:**
```java
Sample sample = Sample.builder()
    .id(1L)
    .name("Test")
    .build();
```
```

---

### 2. Prefecture Entity実装（10:00-11:00）

**ファイル作成:** `src/main/java/com/example/weatherapp/entity/Prefecture.java`

```java
package com.example.weatherapp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

/**
 * 都道府県マスタEntity
 * prefectures テーブルとマッピング
 */
@Entity
@Table(name = "prefectures")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Prefecture {
    
    /**
     * 都道府県ID（主キー）
     * AUTO_INCREMENTで自動採番
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 都道府県名（例: 東京都）
     * NOT NULL制約、最大10文字
     */
    @Column(nullable = false, length = 10)
    private String name;
    
    /**
     * 英語名（例: Tokyo）
     * NOT NULL制約、最大50文字
     */
    @Column(name = "name_en", nullable = false, length = 50)
    private String nameEn;
    
    /**
     * 緯度（例: 35.689487）
     * DOUBLE型
     */
    @Column(nullable = false)
    private Double latitude;
    
    /**
     * 経度（例: 139.691706）
     * DOUBLE型
     */
    @Column(nullable = false)
    private Double longitude;
    
    /**
     * 地域区分（例: 関東）
     * NOT NULL制約、最大20文字
     */
    @Column(nullable = false, length = 20)
    private String region;
    
    /**
     * 作成日時
     * INSERT時に自動設定
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * 更新日時
     * INSERT/UPDATE時に自動設定
     */
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    /**
     * INSERT前に実行されるメソッド
     * 作成日時・更新日時を現在時刻で初期化
     */
    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        createdAt = now;
        updatedAt = now;
    }
    
    /**
     * UPDATE前に実行されるメソッド
     * 更新日時を現在時刻で更新
     */
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

**ポイント解説:**

1. **@Column(name = "name_en")**
   - JavaではキャメルケースだがDBではスネークケース
   - `name`属性でカラム名を明示的に指定

2. **数値カラムの型の対応（重要）**
   - DBの `DOUBLE` 型 ⇔ Javaの `Double` 型 で揃えます
   - `ddl-auto=validate` では、DBの型とEntityの型が一致しているかチェックされます
   - DBが `DECIMAL`、Entityが `Double`（または逆）だと、起動やテストで
     `wrong column type encountered` というエラーになります
   - 緯度・経度・気温のように「多少の誤差が許される値」は `DOUBLE` / `Double` で十分です
   - 金額のように1円もずれてはいけない値は `DECIMAL` ⇔ `BigDecimal` を使います

3. **updatable = false**
   - `createdAt`は一度設定したら変更不可

4. **@PrePersist と @PreUpdate**
   - データベース操作前に自動実行
   - タイムスタンプの自動設定に便利

---

### 3. WeatherRecord Entity実装（11:00-12:00）

**ファイル作成:** `src/main/java/com/example/weatherapp/entity/WeatherRecord.java`

```java
package com.example.weatherapp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 天気記録Entity
 * weather_records テーブルとマッピング
 */
@Entity
@Table(name = "weather_records")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class WeatherRecord {
    
    /**
     * 天気記録ID（主キー）
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 都道府県（多対1）
     * 外部キー: prefecture_id
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "prefecture_id", nullable = false)
    private Prefecture prefecture;
    
    /**
     * API取得日時
     * この時点での天気情報
     */
    @Column(name = "fetched_at", nullable = false)
    private LocalDateTime fetchedAt;
    
    /**
     * 気温（℃）
     * 例: 15.5
     */
    @Column
    private Double temperature;
    
    /**
     * 天気コード（WMO Weather Code）
     * 例: 0=快晴, 1=晴れ, 61=雨
     */
    @Column(name = "weather_code")
    private Integer weatherCode;
    
    /**
     * 風速（m/s）
     * 例: 3.2
     */
    @Column(name = "wind_speed")
    private Double windSpeed;
    
    /**
     * 湿度（%）
     * 例: 65
     */
    private Integer humidity;
    
    /**
     * 体感温度（℃）
     * 例: 13.8
     */
    @Column(name = "apparent_temperature")
    private Double apparentTemperature;
    
    /**
     * 降水量（mm）
     * 例: 0.0
     */
    @Column
    private Double precipitation;
    
    /**
     * 雲量（%）
     * 例: 25
     */
    @Column(name = "cloud_cover")
    private Integer cloudCover;
    
    /**
     * 作成日時
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * 日次予報リスト（1対多）
     * このWeatherRecordに紐づく7日分の予報
     */
    @OneToMany(
        mappedBy = "weatherRecord", 
        cascade = CascadeType.ALL, 
        orphanRemoval = true
    )
    @Builder.Default
    private List<DailyForecast> dailyForecasts = new ArrayList<>();
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
    
    /**
     * 日次予報を追加するヘルパーメソッド
     * 双方向の関連を正しく設定
     */
    public void addDailyForecast(DailyForecast forecast) {
        dailyForecasts.add(forecast);
        forecast.setWeatherRecord(this);
    }
}
```

**ポイント解説:**

1. **@ManyToOne(fetch = FetchType.LAZY)**
   - 遅延読み込み: 必要になるまでPrefectureを取得しない
   - パフォーマンス向上

2. **@JoinColumn(name = "prefecture_id")**
   - 外部キーのカラム名を明示的に指定

3. **@OneToMany(cascade = CascadeType.ALL)**
   - `CascadeType.ALL`: 親の操作（保存・削除）が子に伝播
   - `orphanRemoval = true`: 親から切り離された子を自動削除

4. **@Builder.Default**
   - Builderパターン使用時にリストを空で初期化

5. **addDailyForecast() メソッド**
   - 双方向関連を正しく設定するヘルパー
   - 手動で両側をセットするのを防ぐ

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. DailyForecast Entity実装（13:00-14:00）

**ファイル作成:** `src/main/java/com/example/weatherapp/entity/DailyForecast.java`

```java
package com.example.weatherapp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

/**
 * 日次予報Entity
 * daily_forecasts テーブルとマッピング
 */
@Entity
@Table(name = "daily_forecasts")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DailyForecast {
    
    /**
     * 日次予報ID（主キー）
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 天気記録（多対1）
     * 外部キー: weather_record_id
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "weather_record_id", nullable = false)
    @ToString.Exclude  // toString()で無限ループを防ぐ
    private WeatherRecord weatherRecord;
    
    /**
     * 予報日
     * 例: 2024-01-05
     */
    @Column(name = "forecast_date", nullable = false)
    private LocalDate forecastDate;
    
    /**
     * 最高気温（℃）
     * 例: 15.2
     */
    @Column(name = "temperature_max")
    private Double temperatureMax;
    
    /**
     * 最低気温（℃）
     * 例: 8.1
     */
    @Column(name = "temperature_min")
    private Double temperatureMin;
    
    /**
     * 天気コード
     */
    @Column(name = "weather_code")
    private Integer weatherCode;
    
    /**
     * 降水量合計（mm）
     * 例: 5.2
     */
    @Column(name = "precipitation_sum")
    private Double precipitationSum;
    
    /**
     * 最大風速（m/s）
     * 例: 8.1
     */
    @Column(name = "wind_speed_max")
    private Double windSpeedMax;
    
    /**
     * 日の出時刻
     * 例: 06:51
     */
    private LocalTime sunrise;
    
    /**
     * 日の入り時刻
     * 例: 16:46
     */
    private LocalTime sunset;
    
    /**
     * 作成日時
     */
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
```

**ポイント解説:**

1. **@ToString.Exclude**
   - 循環参照による無限ループを防ぐ
   - WeatherRecord ↔ DailyForecast の双方向関連で必須

2. **LocalDate vs LocalDateTime vs LocalTime**
   - `LocalDate`: 日付のみ（2024-01-05）
   - `LocalDateTime`: 日付+時刻（2024-01-05 15:30:00）
   - `LocalTime`: 時刻のみ（15:30:00）

---

### 5. Entityの動作確認（14:00-15:30）

**テストコード作成:** `src/test/java/com/example/weatherapp/entity/PrefectureTest.java`

```java
package com.example.weatherapp.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Prefecture Entityのテスト
 */
class PrefectureTest {
    
    @Test
    @DisplayName("Prefectureオブジェクトが正しく生成される")
    void testPrefectureCreation() {
        // Given
        Prefecture prefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .latitude(35.689487)
            .longitude(139.691706)
            .region("関東")
            .build();
        
        // When
        prefecture.onCreate();  // @PrePersistを手動実行
        
        // Then
        assertThat(prefecture.getId()).isEqualTo(13L);
        assertThat(prefecture.getName()).isEqualTo("東京都");
        assertThat(prefecture.getNameEn()).isEqualTo("Tokyo");
        assertThat(prefecture.getLatitude()).isEqualTo(35.689487);
        assertThat(prefecture.getLongitude()).isEqualTo(139.691706);
        assertThat(prefecture.getRegion()).isEqualTo("関東");
        assertThat(prefecture.getCreatedAt()).isNotNull();
        assertThat(prefecture.getUpdatedAt()).isNotNull();
    }
    
    @Test
    @DisplayName("@PreUpdateで更新日時が更新される")
    void testPreUpdate() throws InterruptedException {
        // Given
        Prefecture prefecture = Prefecture.builder()
            .name("東京都")
            .nameEn("Tokyo")
            .latitude(35.689487)
            .longitude(139.691706)
            .region("関東")
            .build();
        prefecture.onCreate();
        
        LocalDateTime originalUpdatedAt = prefecture.getUpdatedAt();
        
        // When
        Thread.sleep(10);  // 時刻の違いを作るため少し待つ
        prefecture.onUpdate();  // @PreUpdateを手動実行
        
        // Then
        assertThat(prefecture.getUpdatedAt()).isAfter(originalUpdatedAt);
        assertThat(prefecture.getCreatedAt()).isEqualTo(prefecture.getCreatedAt()); // 変わらない
    }
}
```

**WeatherRecord のテスト:** `src/test/java/com/example/weatherapp/entity/WeatherRecordTest.java`

```java
package com.example.weatherapp.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

import static org.assertj.core.api.Assertions.assertThat;

class WeatherRecordTest {
    
    @Test
    @DisplayName("WeatherRecordにDailyForecastを追加できる")
    void testAddDailyForecast() {
        // Given
        Prefecture prefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .build();
        
        WeatherRecord weatherRecord = WeatherRecord.builder()
            .prefecture(prefecture)
            .fetchedAt(LocalDateTime.now())
            .temperature(15.5)
            .weatherCode(1)
            .build();
        
        DailyForecast forecast = DailyForecast.builder()
            .forecastDate(LocalDate.now().plusDays(1))
            .temperatureMax(18.0)
            .temperatureMin(10.0)
            .weatherCode(2)
            .build();
        
        // When
        weatherRecord.addDailyForecast(forecast);
        
        // Then
        assertThat(weatherRecord.getDailyForecasts()).hasSize(1);
        assertThat(weatherRecord.getDailyForecasts().get(0)).isEqualTo(forecast);
        assertThat(forecast.getWeatherRecord()).isEqualTo(weatherRecord);  // 双方向関連が設定されている
    }
    
    @Test
    @DisplayName("複数のDailyForecastを追加できる")
    void testAddMultipleDailyForecasts() {
        // Given
        WeatherRecord weatherRecord = WeatherRecord.builder()
            .fetchedAt(LocalDateTime.now())
            .build();
        
        // When
        for (int i = 0; i < 7; i++) {
            DailyForecast forecast = DailyForecast.builder()
                .forecastDate(LocalDate.now().plusDays(i))
                .temperatureMax(15.0 + i)
                .temperatureMin(8.0 + i)
                .weatherCode(1)
                .sunrise(LocalTime.of(6, 30))
                .sunset(LocalTime.of(17, 30))
                .build();
            
            weatherRecord.addDailyForecast(forecast);
        }
        
        // Then
        assertThat(weatherRecord.getDailyForecasts()).hasSize(7);
        assertThat(weatherRecord.getDailyForecasts().get(0).getTemperatureMax()).isEqualTo(15.0);
        assertThat(weatherRecord.getDailyForecasts().get(6).getTemperatureMax()).isEqualTo(21.0);
    }
}
```

**テストの実行:**

```bash
# すべてのテストを実行
./gradlew test

# 特定のテストクラスのみ実行
./gradlew test --tests PrefectureTest

# テスト結果の確認
# build/reports/tests/test/index.html をブラウザで開く
```

---

### 6. application.propertiesの設定確認（15:30-16:00）

**`src/main/resources/application.properties`を確認:**

```properties
# JPA設定
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

# ネーミング戦略
spring.jpa.hibernate.naming.physical-strategy=org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
spring.jpa.hibernate.naming.implicit-strategy=org.hibernate.boot.model.naming.ImplicitNamingStrategyLegacyJpaImpl
```

**ddl-autoの設定値:**
- `none`: 何もしない
- `validate`: Entityとテーブル定義の整合性チェックのみ ← **本番推奨**
- `update`: 差分を自動適用（カラム追加のみ、削除はしない）
- `create`: 起動時にテーブル再作成（既存データ削除）
- `create-drop`: 終了時にテーブル削除

---

### 7. ドキュメント作成（16:00-17:00）

**`entity-implementation-summary.md`を作成:**

```markdown
# Entity実装サマリー

## 実装したEntity

### 1. Prefecture（都道府県マスタ）

#### フィールド
- id: 主キー（AUTO_INCREMENT）
- name: 都道府県名
- nameEn: 英語名
- latitude: 緯度
- longitude: 経度
- region: 地域区分
- createdAt: 作成日時
- updatedAt: 更新日時

#### リレーション
- なし（マスタテーブル）

---

### 2. WeatherRecord（天気記録）

#### フィールド
- id: 主キー
- prefecture: 都道府県（外部キー）
- fetchedAt: 取得日時
- temperature: 気温
- weatherCode: 天気コード
- windSpeed: 風速
- humidity: 湿度
- apparentTemperature: 体感温度
- precipitation: 降水量
- cloudCover: 雲量
- createdAt: 作成日時
- dailyForecasts: 日次予報リスト

#### リレーション
- @ManyToOne: Prefecture（多対1）
- @OneToMany: DailyForecast（1対多）

---

### 3. DailyForecast（日次予報）

#### フィールド
- id: 主キー
- weatherRecord: 天気記録（外部キー）
- forecastDate: 予報日
- temperatureMax: 最高気温
- temperatureMin: 最低気温
- weatherCode: 天気コード
- precipitationSum: 降水量合計
- windSpeedMax: 最大風速
- sunrise: 日の出時刻
- sunset: 日の入り時刻
- createdAt: 作成日時

#### リレーション
- @ManyToOne: WeatherRecord（多対1）

---

## ER図

```
Prefecture (1) ←──── (*) WeatherRecord (1) ←──── (*) DailyForecast
```

---

## 実装のポイント

### Lombokアノテーション
- @Data: getter/setter/toString/equals/hashCode
- @Builder: ビルダーパターン
- @NoArgsConstructor / @AllArgsConstructor: コンストラクタ
- @ToString.Exclude: toString()から除外（循環参照防止）

### JPAアノテーション
- @Entity: Entityクラス
- @Table: テーブル名指定
- @Id: 主キー
- @GeneratedValue: 主キー生成戦略
- @Column: カラム属性
- @ManyToOne / @OneToMany: リレーション
- @JoinColumn: 外部キー
- @PrePersist / @PreUpdate: ライフサイクルコールバック

### パフォーマンス考慮
- FetchType.LAZY: 遅延読み込み
- CascadeType.ALL: カスケード設定
- orphanRemoval: 孤児削除

---

## テスト観点

### 単体テスト
- [ ] オブジェクトが正しく生成される
- [ ] Builderパターンが動作する
- [ ] @PrePersistで日時が設定される
- [ ] @PreUpdateで更新日時が更新される
- [ ] リレーションが正しく設定される

### 統合テスト（Day 25で実施）
- [ ] データベースに保存できる
- [ ] データベースから取得できる
- [ ] リレーションが正しく動作する
- [ ] カスケードが動作する
```

---

## ✅ チェックリスト

- [ ] JPAとEntityの基礎を理解した
- [ ] Prefecture Entityを実装した
- [ ] WeatherRecord Entityを実装した
- [ ] DailyForecast Entityを実装した
- [ ] リレーションシップを正しく設定した
- [ ] 単体テストを作成し、すべてパスした
- [ ] application.propertiesを確認した
- [ ] entity-implementation-summary.mdを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(entity): Prefecture, WeatherRecord, DailyForecast Entityを実装"
git push origin feature/day-16
```

---

## 📚 参考リンク

### JPA基礎
- [Spring Data JPA公式ドキュメント](https://spring.io/projects/spring-data-jpa)
- [JPAアノテーション一覧（日本語）](https://qiita.com/KevinFQ/items/a6d92ec7b32911e50ffe)
- [JPA Entity設計のベストプラクティス（日本語）](https://qiita.com/disc99/items/5c2c6f8b511e6c8d7b4e)

### Lombok
- [Lombok公式ガイド](https://projectlombok.org/features/)
- [Lombokを使ったEntityの書き方（日本語）](https://qiita.com/opengl-8080/items/671ffd4bf0e01c1fbf6c)

### リレーションシップ
- [@OneToManyと@ManyToOneの使い方（日本語）](https://qiita.com/KevinFQ/items/83b3f4f8f4f4f2a0c2b7)
- [双方向関連の落とし穴（日本語）](https://qiita.com/rubytomato@github/items/cfb1e3d5c3b6f46c09b7)

### テスト
- [JUnit 5使い方（日本語）](https://qiita.com/opengl-8080/items/e57c76f291885bac8ab7)
- [AssertJの使い方（日本語）](https://qiita.com/disc99/items/31fa7abb724f63602dc9)

---

## 🆘 トラブルシューティング

### Lombokが動作しない
1. IntelliJ IDEAのLombokプラグインをインストール
2. Settings → Build, Execution, Deployment → Compiler → Annotation Processors
3. "Enable annotation processing" をチェック
4. IntelliJ IDEAを再起動

### テーブルとEntityの不一致エラー
```
org.hibernate.tool.schema.spi.SchemaManagementException: Schema-validation: missing column
```
**原因:** DDLとEntityの定義が一致していない

**解決策:**
1. schema.sqlを確認
2. Entityのフィールド名、型を確認
3. `@Column(name = "...")`でカラム名を明示

### 循環参照エラー（StackOverflowError）
```
java.lang.StackOverflowError at toString()
```
**原因:** 双方向関連でtoString()が無限ループ

**解決策:**
```java
@ToString.Exclude  // ← これを追加
@ManyToOne
private WeatherRecord weatherRecord;
```

---

## 📝 本日のまとめ

`day-16-summary.md`を作成し、以下を記録：

1. **実装したEntity:**
   - Prefecture
   - WeatherRecord
   - DailyForecast

2. **学んだJPAアノテーション:**
   - @Entity, @Table, @Id, @GeneratedValue
   - @Column, @ManyToOne, @OneToMany
   - @PrePersist, @PreUpdate

3. **困難だった点:**
   
4. **明日への引き継ぎ:**
   - Repository層の実装準備

---

## 🎉 完了後

次は [Day 17](day-17.md) でRepository層を実装する

お疲れさまでした！
