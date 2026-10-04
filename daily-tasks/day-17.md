# Day 17: Repository層実装

## 📅 実施日
- 予定: Week 4 - Day 17
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Spring Data JPAのRepositoryインターフェースを実装し、データベースアクセス層を完成させる

---

## 📋 午前の作業（9:00-13:00）

### 1. Spring Data JPAの基礎理解（9:00-10:00）

**Spring Data JPAとは:**
- データベースアクセスを簡略化するフレームワーク
- インターフェースを定義するだけでCRUD操作が可能
- カスタムクエリもメソッド名規約で自動生成

**学習用ドキュメント作成:**

`repository-guide.md`を作成：

```markdown
# Spring Data JPA Repository実装ガイド

## Repositoryの階層

```
Repository (マーカーインターフェース)
    ↓
CrudRepository (基本的なCRUD)
    ↓
PagingAndSortingRepository (ページング・ソート)
    ↓
JpaRepository (JPA固有機能) ← 通常はこれを使う
```

## JpaRepositoryの基本

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // これだけで以下のメソッドが使える
    // - save(User)
    // - findById(Long)
    // - findAll()
    // - delete(User)
    // - count()
    // など
}
```

## メソッド名によるクエリ自動生成

### 基本パターン

| メソッド名 | 生成されるSQL |
|-----------|--------------|
| findByName(String name) | WHERE name = ? |
| findByNameAndAge(String name, int age) | WHERE name = ? AND age = ? |
| findByNameOrAge(String name, int age) | WHERE name = ? OR age = ? |
| findByAgeLessThan(int age) | WHERE age < ? |
| findByAgeGreaterThan(int age) | WHERE age > ? |
| findByNameLike(String name) | WHERE name LIKE ? |
| findByNameContaining(String name) | WHERE name LIKE %?% |
| findByNameStartingWith(String name) | WHERE name LIKE ?% |
| findByNameEndingWith(String name) | WHERE name LIKE %? |
| findByAgeIn(List<Integer> ages) | WHERE age IN (?) |
| findByNameOrderByAgeDesc(String name) | WHERE name = ? ORDER BY age DESC |

### 複雑なクエリ

```java
// ページング
Page<User> findByAge(int age, Pageable pageable);

// トップN件取得
List<User> findTop10ByOrderByCreatedAtDesc();

// カウント
long countByAge(int age);

// 存在確認
boolean existsByEmail(String email);

// 削除
void deleteByAge(int age);
```

## @Queryアノテーションの使用

### JPQLクエリ

```java
@Query("SELECT u FROM User u WHERE u.age >= :age")
List<User> findAdults(@Param("age") int age);

@Query("SELECT u FROM User u WHERE u.name LIKE %:keyword%")
List<User> searchByName(@Param("keyword") String keyword);
```

### ネイティブクエリ

```java
@Query(value = "SELECT * FROM users WHERE age >= ?1", nativeQuery = true)
List<User> findAdultsNative(int age);
```

### 更新クエリ

```java
@Modifying
@Transactional
@Query("UPDATE User u SET u.status = :status WHERE u.age >= :age")
int updateStatus(@Param("status") String status, @Param("age") int age);
```

## トランザクション

```java
@Transactional
public void updateUser(Long id, String name) {
    User user = userRepository.findById(id).orElseThrow();
    user.setName(name);
    // saveを呼ばなくても自動的に更新される（Dirty Checking）
}
```

## ベストプラクティス

1. **メソッド名は長くなりすぎないように**
   - 複雑な条件は@Queryを使う

2. **Optional<T>の活用**
   - findByIdはOptionalを返す
   - orElseThrow()でnullチェック不要

3. **ページングの活用**
   - 大量データはPageableを使う

4. **N+1問題の回避**
   - @EntityGraphや@Queryでfetch joinを使う
```

---

### 2. PrefectureRepository実装（10:00-11:00）

**ファイル作成:** `src/main/java/com/example/weatherapp/repository/PrefectureRepository.java`

```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.Prefecture;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Prefecture（都道府県）のRepositoryインターフェース
 */
@Repository
public interface PrefectureRepository extends JpaRepository<Prefecture, Long> {
    
    /**
     * 都道府県名で検索
     * 
     * @param name 都道府県名（例: "東京都"）
     * @return 該当する都道府県（Optional）
     */
    Optional<Prefecture> findByName(String name);
    
    /**
     * 地域で検索
     * 
     * @param region 地域名（例: "関東"）
     * @return 該当する都道府県のリスト
     * 
     * 例: findByRegion("関東") 
     * → SELECT * FROM prefectures WHERE region = '関東' ORDER BY id
     */
    List<Prefecture> findByRegionOrderById(String region);
    
    /**
     * 英語名で検索
     * 
     * @param nameEn 英語名（例: "Tokyo"）
     * @return 該当する都道府県（Optional）
     */
    Optional<Prefecture> findByNameEn(String nameEn);
    
    /**
     * 都道府県名の部分一致検索
     * 
     * @param keyword キーワード（例: "京"）
     * @return 該当する都道府県のリスト
     * 
     * 例: findByNameContaining("京")
     * → 東京都、京都府
     */
    List<Prefecture> findByNameContaining(String keyword);
    
    /**
     * 地域リストで検索
     * 
     * @param regions 地域のリスト（例: ["関東", "関西"]）
     * @return 該当する都道府県のリスト
     */
    List<Prefecture> findByRegionIn(List<String> regions);
    
    /**
     * 緯度・経度の範囲で検索
     * カスタムクエリ使用（メソッド名だと複雑になりすぎるため）
     * 
     * @param minLat 最小緯度
     * @param maxLat 最大緯度
     * @param minLon 最小経度
     * @param maxLon 最大経度
     * @return 該当する都道府県のリスト
     */
    @Query("SELECT p FROM Prefecture p " +
           "WHERE p.latitude BETWEEN :minLat AND :maxLat " +
           "AND p.longitude BETWEEN :minLon AND :maxLon " +
           "ORDER BY p.id")
    List<Prefecture> findByCoordinateRange(
        @Param("minLat") Double minLat,
        @Param("maxLat") Double maxLat,
        @Param("minLon") Double minLon,
        @Param("maxLon") Double maxLon
    );
    
    /**
     * すべての地域を重複なしで取得
     * 
     * @return 地域のリスト（例: ["北海道", "東北", "関東", ...]）
     */
    // ※ DISTINCT と ORDER BY p.id を組み合わせると、MySQL 8 でもエラーになる
    //    （並び替えに使う列は、SELECTする列に含まれている必要がある）。
    //    GROUP BY で地域をまとめ、各地域の最小IDで並び替える
    @Query("SELECT p.region FROM Prefecture p GROUP BY p.region ORDER BY MIN(p.id)")
    List<String> findAllRegions();
    
    /**
     * 地域ごとの都道府県数をカウント
     * ネイティブクエリ使用（GROUP BYのため）
     * 
     * @return 地域名と件数のマップ
     */
    @Query(value = "SELECT region, COUNT(*) as count " +
                   "FROM prefectures " +
                   "GROUP BY region " +
                   "ORDER BY MIN(id)",
           nativeQuery = true)
    List<Object[]> countByRegion();
}
```

**ポイント解説:**

1. **@Repository**
   - Spring管理のBeanとして登録
   - 例外の変換（SQLExceptionをDataAccessExceptionに）

2. **JpaRepository<Prefecture, Long>**
   - Prefecture: エンティティ型
   - Long: 主キーの型

3. **Optional<T>**
   - 単一結果はOptionalで返す
   - nullチェック不要

4. **メソッド名規約**
   - `findBy` + フィールド名 + 条件
   - 自動的にクエリ生成

5. **@Query**
   - 複雑なクエリは明示的に記述
   - JPQL（エンティティベース）とネイティブSQL両方可能

---

### 3. WeatherRecordRepository実装（11:00-12:00）

**ファイル作成:** `src/main/java/com/example/weatherapp/repository/WeatherRecordRepository.java`

```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.entity.WeatherRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * WeatherRecord（天気記録）のRepositoryインターフェース
 */
@Repository
public interface WeatherRecordRepository extends JpaRepository<WeatherRecord, Long> {
    
    /**
     * 都道府県IDで検索（最新順）
     * 
     * @param prefectureId 都道府県ID
     * @return 該当する天気記録のリスト
     */
    List<WeatherRecord> findByPrefectureIdOrderByFetchedAtDesc(Long prefectureId);
    
    /**
     * 都道府県で検索（最新順、上位N件）
     * 
     * @param prefecture 都道府県エンティティ
     * @param limit 取得件数
     * @return 該当する天気記録のリスト
     */
    List<WeatherRecord> findTop10ByPrefectureOrderByFetchedAtDesc(Prefecture prefecture);
    
    /**
     * 都道府県の最新の天気記録を1件取得
     * 
     * @param prefecture 都道府県エンティティ
     * @return 最新の天気記録（Optional）
     */
    Optional<WeatherRecord> findFirstByPrefectureOrderByFetchedAtDesc(Prefecture prefecture);
    
    /**
     * 日時範囲で検索
     * 
     * @param start 開始日時
     * @param end 終了日時
     * @return 該当する天気記録のリスト
     */
    List<WeatherRecord> findByFetchedAtBetweenOrderByFetchedAtDesc(
        LocalDateTime start, 
        LocalDateTime end
    );
    
    /**
     * 都道府県と日時範囲で検索
     * 
     * @param prefecture 都道府県
     * @param start 開始日時
     * @param end 終了日時
     * @return 該当する天気記録のリスト
     */
    List<WeatherRecord> findByPrefectureAndFetchedAtBetween(
        Prefecture prefecture,
        LocalDateTime start,
        LocalDateTime end
    );
    
    /**
     * 天気コードで検索
     * 
     * @param weatherCode 天気コード
     * @param pageable ページング情報
     * @return 該当する天気記録のページ
     */
    Page<WeatherRecord> findByWeatherCode(Integer weatherCode, Pageable pageable);
    
    /**
     * 気温範囲で検索
     * 
     * @param minTemp 最低気温
     * @param maxTemp 最高気温
     * @return 該当する天気記録のリスト
     */
    List<WeatherRecord> findByTemperatureBetween(Double minTemp, Double maxTemp);
    
    /**
     * DailyForecastsをEAGER fetchで取得
     * N+1問題を回避
     * 
     * @param id 天気記録ID
     * @return 天気記録（DailyForecasts込み）
     */
    @Query("SELECT w FROM WeatherRecord w " +
           "LEFT JOIN FETCH w.dailyForecasts " +
           "WHERE w.id = :id")
    Optional<WeatherRecord> findByIdWithForecasts(@Param("id") Long id);
    
    /**
     * 都道府県の最新記録をDailyForecasts込みで取得
     * 
     * @param prefectureId 都道府県ID
     * @return 最新の天気記録（DailyForecasts込み）
     */
    @Query("SELECT w FROM WeatherRecord w " +
           "LEFT JOIN FETCH w.dailyForecasts " +
           "WHERE w.prefecture.id = :prefectureId " +
           "ORDER BY w.fetchedAt DESC " +
           "LIMIT 1")
    Optional<WeatherRecord> findLatestWithForecasts(@Param("prefectureId") Long prefectureId);
    
    /**
     * 古い記録を削除（データ保持期間管理用）
     * 
     * @param before この日時より前の記録を削除
     */
    void deleteByFetchedAtBefore(LocalDateTime before);
    
    /**
     * 都道府県の記録件数をカウント
     * 
     * @param prefecture 都道府県
     * @return 記録件数
     */
    long countByPrefecture(Prefecture prefecture);
}
```

**ポイント解説:**

1. **Top/First**
   - `findTopNBy...`: 上位N件取得
   - `findFirstBy...`: 1件のみ取得

2. **Between**
   - 範囲検索に便利
   - 日時、数値両方で使用可能

3. **LEFT JOIN FETCH**
   - 関連エンティティを同時に取得
   - N+1問題（後述）の回避

4. **Page<T>**
   - ページング対応
   - 総件数も自動取得

5. **void delete系**
   - 削除メソッド
   - `@Modifying`や`@Transactional`は不要（自動付与）

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. DailyForecastRepository実装（13:00-13:30）

**ファイル作成:** `src/main/java/com/example/weatherapp/repository/DailyForecastRepository.java`

```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.DailyForecast;
import com.example.weatherapp.entity.WeatherRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * DailyForecast（日次予報）のRepositoryインターフェース
 */
@Repository
public interface DailyForecastRepository extends JpaRepository<DailyForecast, Long> {
    
    /**
     * 天気記録IDで検索（日付順）
     * 
     * @param weatherRecordId 天気記録ID
     * @return 該当する日次予報のリスト（7日分）
     */
    List<DailyForecast> findByWeatherRecordIdOrderByForecastDateAsc(Long weatherRecordId);
    
    /**
     * 天気記録で検索
     * 
     * @param weatherRecord 天気記録エンティティ
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByWeatherRecordOrderByForecastDateAsc(WeatherRecord weatherRecord);
    
    /**
     * 予報日で検索
     * 
     * @param forecastDate 予報日
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByForecastDate(LocalDate forecastDate);
    
    /**
     * 予報日範囲で検索
     * 
     * @param startDate 開始日
     * @param endDate 終了日
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByForecastDateBetweenOrderByForecastDateAsc(
        LocalDate startDate,
        LocalDate endDate
    );
    
    /**
     * 天気記録と予報日で検索
     * 
     * @param weatherRecord 天気記録
     * @param forecastDate 予報日
     * @return 該当する日次予報（Optional）
     */
    Optional<DailyForecast> findByWeatherRecordAndForecastDate(
        WeatherRecord weatherRecord,
        LocalDate forecastDate
    );
    
    /**
     * 天気コードで検索
     * 
     * @param weatherCode 天気コード
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByWeatherCode(Integer weatherCode);
    
    /**
     * 最高気温が閾値以上の予報を検索
     * 
     * @param temperature 気温閾値
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByTemperatureMaxGreaterThanEqual(Double temperature);
    
    /**
     * 最低気温が閾値以下の予報を検索
     * 
     * @param temperature 気温閾値
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByTemperatureMinLessThanEqual(Double temperature);
    
    /**
     * 降水量が閾値以上の予報を検索（雨の日）
     * 
     * @param amount 降水量閾値（mm）
     * @return 該当する日次予報のリスト
     */
    List<DailyForecast> findByPrecipitationSumGreaterThan(Double amount);
    
    /**
     * 都道府県IDと予報日範囲で予報を取得
     * WeatherRecordを経由して検索
     * 
     * @param prefectureId 都道府県ID
     * @param startDate 開始日
     * @param endDate 終了日
     * @return 該当する日次予報のリスト
     */
    @Query("SELECT df FROM DailyForecast df " +
           "JOIN df.weatherRecord wr " +
           "WHERE wr.prefecture.id = :prefectureId " +
           "AND df.forecastDate BETWEEN :startDate AND :endDate " +
           "ORDER BY df.forecastDate ASC")
    List<DailyForecast> findByPrefectureAndDateRange(
        @Param("prefectureId") Long prefectureId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
}
```

---

### 5. Repositoryの動作確認テスト（13:30-15:30）

#### 5-0. テスト用データベース（H2）の準備

> ⚠️ **ここを飛ばすと `./gradlew test` が失敗します。** 先に必ず設定してください。

`@DataJpaTest` は、**本物のMySQLではなく、メモリ上のテスト用DB（H2）** に自動で差し替えて動きます。
そのため、次の3つが必要です。

**① `build.gradle` にH2を追加**（`dependencies { ... }` の中）:

```groovy
testRuntimeOnly 'com.h2database:h2'
```

追加したらGradleを再読み込み（IntelliJ右側のGradleタブの🔄ボタン）します。

**② テスト専用の設定ファイルを作成**: `src/test/resources/application.properties`

```properties
# テスト用DB（メモリ上のH2。MySQL互換モード）
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# テーブルはEntityの定義から自動作成し、テスト終了後に破棄する
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect

# 本番用のschema.sql / data.sql はテストでは実行しない
spring.sql.init.mode=never
```

**③ このファイルが `src/main/resources/application.properties`（本番用・MySQL・`ddl-auto=validate`）より優先される** ことを理解しておきます。
テストでは `src/test/resources` 側の設定が使われます。

**よくあるエラーと原因:**

| エラーメッセージ | 原因 | 対処 |
|---|---|---|
| `Failed to replace DataSource with an embedded database` | H2が依存関係にない | ① を実施 |
| `wrong column type encountered in column [latitude]` | DBの型とEntityの型が不一致（DECIMAL ⇔ Double など） | Day 11のDDLとDay 16のEntityで `DOUBLE` ⇔ `Double` に揃える |
| `Schema-validation: missing table` | テストでも `ddl-auto=validate` になっている | ② の `create-drop` を確認 |
| MySQLに接続しようとして失敗する | `src/test/resources/application.properties` がない・場所が違う | ② のパスとファイル名を確認 |

#### 5-1. テストクラスの作成

**統合テスト作成:** `src/test/java/com/example/weatherapp/repository/PrefectureRepositoryTest.java`

```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.Prefecture;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.jdbc.Sql;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * PrefectureRepositoryの統合テスト
 * 
 * @DataJpaTest: JPA関連のみをロードする軽量テスト
 */
@DataJpaTest
@Sql("/test-data.sql")  // テストデータ投入
class PrefectureRepositoryTest {
    
    @Autowired
    private PrefectureRepository prefectureRepository;
    
    @Test
    @DisplayName("全件取得できる")
    void testFindAll() {
        // When
        List<Prefecture> prefectures = prefectureRepository.findAll();
        
        // Then
        assertThat(prefectures).hasSize(47);
    }
    
    @Test
    @DisplayName("IDで検索できる")
    void testFindById() {
        // When
        Optional<Prefecture> result = prefectureRepository.findById(13L);
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("東京都");
        assertThat(result.get().getNameEn()).isEqualTo("Tokyo");
    }
    
    @Test
    @DisplayName("存在しないIDで検索するとOptional.emptyが返る")
    void testFindById_NotFound() {
        // When
        Optional<Prefecture> result = prefectureRepository.findById(999L);
        
        // Then
        assertThat(result).isEmpty();
    }
    
    @Test
    @DisplayName("都道府県名で検索できる")
    void testFindByName() {
        // When
        Optional<Prefecture> result = prefectureRepository.findByName("東京都");
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getId()).isEqualTo(13L);
    }
    
    @Test
    @DisplayName("地域で検索できる")
    void testFindByRegion() {
        // When
        List<Prefecture> kanto = prefectureRepository.findByRegionOrderById("関東");
        
        // Then
        assertThat(kanto).hasSize(7);  // 茨城、栃木、群馬、埼玉、千葉、東京、神奈川
        assertThat(kanto.get(0).getName()).isEqualTo("茨城県");
        assertThat(kanto.get(6).getName()).isEqualTo("神奈川県");
    }
    
    @Test
    @DisplayName("部分一致で検索できる")
    void testFindByNameContaining() {
        // When
        List<Prefecture> result = prefectureRepository.findByNameContaining("京");
        
        // Then
        assertThat(result).hasSize(2);  // 東京都、京都府
        assertThat(result)
            .extracting(Prefecture::getName)
            .containsExactlyInAnyOrder("東京都", "京都府");
    }
    
    @Test
    @DisplayName("複数地域で検索できる")
    void testFindByRegionIn() {
        // When
        List<Prefecture> result = prefectureRepository.findByRegionIn(
            List.of("関東", "関西")
        );
        
        // Then
        assertThat(result).hasSize(14);  // 関東7 + 関西7
    }
    
    @Test
    @DisplayName("すべての地域を取得できる")
    void testFindAllRegions() {
        // When
        List<String> regions = prefectureRepository.findAllRegions();
        
        // Then
        assertThat(regions).containsExactly(
            "北海道", "東北", "関東", "中部", "関西", "中国", "四国", "九州", "沖縄"
        );
    }
    
    @Test
    @DisplayName("新しい都道府県を保存できる")
    void testSave() {
        // Given
        Prefecture newPref = Prefecture.builder()
            .name("テスト県")
            .nameEn("Test")
            .latitude(35.0)
            .longitude(135.0)
            .region("テスト")
            .build();
        
        // When
        Prefecture saved = prefectureRepository.save(newPref);
        
        // Then
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getName()).isEqualTo("テスト県");
        
        // 保存されたか確認
        Optional<Prefecture> found = prefectureRepository.findById(saved.getId());
        assertThat(found).isPresent();
    }
    
    @Test
    @DisplayName("都道府県を更新できる")
    void testUpdate() {
        // Given
        Prefecture tokyo = prefectureRepository.findById(13L).orElseThrow();
        String originalName = tokyo.getName();
        
        // When
        tokyo.setName("東京特別区");
        Prefecture updated = prefectureRepository.save(tokyo);
        
        // Then
        assertThat(updated.getName()).isEqualTo("東京特別区");
        
        // 元に戻す
        tokyo.setName(originalName);
        prefectureRepository.save(tokyo);
    }
    
    @Test
    @DisplayName("都道府県を削除できる")
    void testDelete() {
        // Given
        Prefecture testPref = Prefecture.builder()
            .name("削除テスト県")
            .nameEn("Delete Test")
            .latitude(35.0)
            .longitude(135.0)
            .region("テスト")
            .build();
        Prefecture saved = prefectureRepository.save(testPref);
        Long savedId = saved.getId();
        
        // When
        prefectureRepository.delete(saved);
        
        // Then
        Optional<Prefecture> found = prefectureRepository.findById(savedId);
        assertThat(found).isEmpty();
    }
}
```

**テストデータ（47都道府県）:** `src/test/resources/test-data.sql`

> 💡 このファイルは、Day 19・Day 25のテストでも使い回します。ここで正しく作っておきましょう。

```sql
-- テスト用データ(47都道府県)
DELETE FROM daily_forecasts;
DELETE FROM weather_records;
DELETE FROM prefectures;

-- created_at / updated_at はNOT NULLのため必ず値を入れる

-- 北海道
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(1, '北海道', 'Hokkaido', 43.064167, 141.346944, '北海道', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 東北
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(2, '青森県', 'Aomori', 40.824444, 140.74, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, '岩手県', 'Iwate', 39.703611, 141.1525, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, '宮城県', 'Miyagi', 38.268889, 140.872222, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, '秋田県', 'Akita', 39.718611, 140.1025, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, '山形県', 'Yamagata', 38.240556, 140.363333, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, '福島県', 'Fukushima', 37.75, 140.467778, '東北', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 関東
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(8, '茨城県', 'Ibaraki', 36.341389, 140.446667, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(9, '栃木県', 'Tochigi', 36.565556, 139.883611, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(10, '群馬県', 'Gunma', 36.390833, 139.060556, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(11, '埼玉県', 'Saitama', 35.856944, 139.648889, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(12, '千葉県', 'Chiba', 35.605, 140.123333, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(13, '東京都', 'Tokyo', 35.689487, 139.691706, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(14, '神奈川県', 'Kanagawa', 35.447778, 139.6425, '関東', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 中部
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(15, '新潟県', 'Niigata', 37.902222, 139.023611, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(16, '富山県', 'Toyama', 36.695278, 137.211389, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(17, '石川県', 'Ishikawa', 36.594444, 136.625556, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(18, '福井県', 'Fukui', 36.065278, 136.221667, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(19, '山梨県', 'Yamanashi', 35.664167, 138.568333, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(20, '長野県', 'Nagano', 36.651389, 138.181111, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(21, '岐阜県', 'Gifu', 35.391111, 136.722222, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(22, '静岡県', 'Shizuoka', 34.976944, 138.383056, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(23, '愛知県', 'Aichi', 35.180278, 136.906389, '中部', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 関西
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(24, '三重県', 'Mie', 34.730278, 136.508611, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(25, '滋賀県', 'Shiga', 35.004444, 135.868333, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(26, '京都府', 'Kyoto', 35.021389, 135.755556, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(27, '大阪府', 'Osaka', 34.686389, 135.52, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(28, '兵庫県', 'Hyogo', 34.691389, 135.183056, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(29, '奈良県', 'Nara', 34.685278, 135.832778, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(30, '和歌山県', 'Wakayama', 34.225833, 135.1675, '関西', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 中国
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(31, '鳥取県', 'Tottori', 35.503889, 134.238056, '中国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(32, '島根県', 'Shimane', 35.472222, 133.050556, '中国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(33, '岡山県', 'Okayama', 34.661667, 133.934722, '中国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(34, '広島県', 'Hiroshima', 34.396389, 132.459444, '中国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(35, '山口県', 'Yamaguchi', 34.186111, 131.470556, '中国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 四国
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(36, '徳島県', 'Tokushima', 34.065833, 134.559444, '四国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(37, '香川県', 'Kagawa', 34.340278, 134.043333, '四国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(38, '愛媛県', 'Ehime', 33.841667, 132.765556, '四国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(39, '高知県', 'Kochi', 33.559722, 133.531111, '四国', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 九州
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(40, '福岡県', 'Fukuoka', 33.606389, 130.418056, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(41, '佐賀県', 'Saga', 33.249444, 130.299167, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(42, '長崎県', 'Nagasaki', 32.744722, 129.873611, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(43, '熊本県', 'Kumamoto', 32.789722, 130.741667, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(44, '大分県', 'Oita', 33.238056, 131.6125, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(45, '宮崎県', 'Miyazaki', 31.911111, 131.423889, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(46, '鹿児島県', 'Kagoshima', 31.560278, 130.558056, '九州', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 沖縄
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region, created_at, updated_at) VALUES
(47, '沖縄県', 'Okinawa', 26.2125, 127.680833, '沖縄', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 新規保存（testSave）で採番されるIDが、上で入れたIDとぶつからないようにする
ALTER TABLE prefectures ALTER COLUMN id RESTART WITH 100;
```

**テスト実行:**

```bash
# 全テスト実行
./gradlew test

# 特定のテストクラスのみ
./gradlew test --tests PrefectureRepositoryTest

# テスト結果の確認
open build/reports/tests/test/index.html
```

---

### 6. N+1問題の理解と対策（15:30-16:30）

**N+1問題とは:**

`n+1-problem-guide.md`を作成：

```markdown
# N+1問題の理解と対策

## N+1問題とは

### 問題の例

```java
// 1. 都道府県を全件取得（1回のクエリ）
List<Prefecture> prefectures = prefectureRepository.findAll();

// 2. 各都道府県の天気記録を取得（N回のクエリ）
for (Prefecture pref : prefectures) {
    List<WeatherRecord> records = weatherRecordRepository
        .findByPrefecture(pref);  // ← 47回実行される！
}

// 合計: 1 + 47 = 48回のクエリ
```

### 発行されるSQL

```sql
-- 1回目
SELECT * FROM prefectures;

-- 2回目以降（47回）
SELECT * FROM weather_records WHERE prefecture_id = 1;
SELECT * FROM weather_records WHERE prefecture_id = 2;
SELECT * FROM weather_records WHERE prefecture_id = 3;
...
SELECT * FROM weather_records WHERE prefecture_id = 47;
```

**パフォーマンスへの影響:**
- データベースへのアクセス回数が激増
- レスポンスタイムが遅くなる
- データベースサーバーの負荷が上がる

---

## 対策1: JOIN FETCH

### @Queryでの実装

```java
@Query("SELECT w FROM WeatherRecord w " +
       "LEFT JOIN FETCH w.dailyForecasts " +
       "WHERE w.prefecture.id = :prefectureId")
Optional<WeatherRecord> findByPrefectureWithForecasts(
    @Param("prefectureId") Long prefectureId
);
```

### 発行されるSQL

```sql
SELECT w.*, df.* 
FROM weather_records w
LEFT JOIN daily_forecasts df ON w.id = df.weather_record_id
WHERE w.prefecture_id = 13;
```

**メリット:**
- 1回のクエリで関連データも取得
- N+1問題が発生しない

---

## 対策2: @EntityGraph

```java
public interface WeatherRecordRepository extends JpaRepository<WeatherRecord, Long> {
    
    @EntityGraph(attributePaths = {"dailyForecasts", "prefecture"})
    Optional<WeatherRecord> findById(Long id);
}
```

**メリット:**
- アノテーションで簡単に指定
- メソッド名規約で使える

---

## 対策3: Batch Fetch Size

`application.properties`に追加：

```properties
spring.jpa.properties.hibernate.default_batch_fetch_size=10
```

**効果:**
- N+1問題は解決しないが、クエリ数を減らせる
- 47回 → 5回程度に削減

---

## 実装例: 正しいデータ取得

### ❌ 悪い例（N+1発生）

```java
@GetMapping("/prefectures-with-weather")
public List<PrefectureWeatherDto> getAllWithWeather() {
    List<Prefecture> prefectures = prefectureRepository.findAll();
    
    return prefectures.stream()
        .map(pref -> {
            // ← ここでN+1発生！
            Optional<WeatherRecord> record = weatherRecordRepository
                .findFirstByPrefectureOrderByFetchedAtDesc(pref);
            
            return new PrefectureWeatherDto(pref, record.orElse(null));
        })
        .collect(Collectors.toList());
}
```

### ✅ 良い例（1回のクエリ）

```java
@Query("SELECT p, w FROM Prefecture p " +
       "LEFT JOIN WeatherRecord w ON w.prefecture.id = p.id " +
       "WHERE w.id IN (" +
       "  SELECT MAX(w2.id) FROM WeatherRecord w2 " +
       "  GROUP BY w2.prefecture.id" +
       ") OR w.id IS NULL")
List<Object[]> findAllPrefecturesWithLatestWeather();
```

---

## ベストプラクティス

1. **関連データが必要な場合は JOIN FETCH**
2. **不要な場合は LAZY fetch（デフォルト）**
3. **Hibernateのクエリログを確認**
   ```properties
   spring.jpa.show-sql=true
   logging.level.org.hibernate.SQL=DEBUG
   ```
4. **テスト時にクエリ数を確認**
```

---

### 7. ドキュメント作成（16:30-17:00）

**`repository-implementation-summary.md`を作成**

---

## ✅ チェックリスト

- [ ] Spring Data JPAの基礎を理解した
- [ ] PrefectureRepositoryを実装した
- [ ] WeatherRecordRepositoryを実装した
- [ ] DailyForecastRepositoryを実装した
- [ ] 統合テストを作成し、すべてパスした
- [ ] N+1問題を理解し対策を学んだ
- [ ] GitHubにコミット・プッシュした

---

## 📚 参考リンク

### Spring Data JPA
- [Spring Data JPA公式ドキュメント](https://spring.io/projects/spring-data-jpa)
- [クエリメソッドの命名規則（日本語）](https://qiita.com/shindo_ryo/items/0e2cc88b6277a4e17895)
- [Spring Data JPAの使い方まとめ（日本語）](https://qiita.com/tag1216/items/89d908f61eb621622786)

### テスト
- [@DataJpaTestの使い方（日本語）](https://qiita.com/rubytomato@github/items/5f0f7e70a0b63380f7db)
- [Repository層のテスト書き方（日本語）](https://qiita.com/disc99/items/ea443af9a4a8d15fcfd1)

### N+1問題
- [N+1問題とは（日本語）](https://qiita.com/muroya2355/items/d2a9b3b768f8e0e368bf)
- [Hibernateでの対策（日本語）](https://qiita.com/KevinFQ/items/a11af02741c47b89cbba)

---

## 🆘 トラブルシューティング

### `./gradlew test` で `Failed to replace DataSource with an embedded database`
**原因:** テスト用DB（H2）が依存関係に入っていない

**解決策:**
1. `build.gradle` に `testRuntimeOnly 'com.h2database:h2'` を追加し、Gradleを再読み込み
2. このDayの「5-0. テスト用データベース（H2）の準備」を、①〜②の順に実施

### `wrong column type encountered in column [...]`
**原因:** DBの列の型とEntityのフィールドの型が一致していない（DECIMALとDoubleなど）

**解決策:**
1. Day 11のDDLとEntityの型を見比べる（`DOUBLE` ⇔ `Double`、`BIGINT` ⇔ `Long`）
2. テスト用DBでは `ddl-auto=create-drop` のため、Entityから自動作成される。本番のMySQL側（DDL）がずれていないかも確認

### `Schema-validation: missing table` / MySQLに接続しようとして失敗する
**原因:** テストが本番用の設定（MySQL・`validate`）で動いている

**解決策:**
1. `src/test/resources/application.properties` を作成したか、場所・ファイル名が合っているか確認
2. テスト用設定で `ddl-auto=create-drop` と `spring.sql.init.mode=never` になっているか確認

### `PropertyReferenceException: No property 'xxx' found for type 'Prefecture'`
**原因:** メソッド名のプロパティ名がEntityのフィールド名と一致していない

**解決策:**
1. `findByRegion` の `Region` が、Entityのフィールド `region` と一致しているか確認（綴り・大文字小文字）
2. Entityのフィールド名を変えた場合は、Repositoryのメソッド名も合わせて直す

### `QuerySyntaxException: Prefecture is not mapped`
**原因:** JPQLの書き方の誤り（テーブル名で書いている、クラス名の綴りが違う）

**解決策:**
1. JPQLでは**テーブル名ではなくEntityのクラス名**を書く（`FROM Prefecture p`）
2. 列名ではなくフィールド名（`p.nameEn`）で書く

### `LazyInitializationException`
**原因:** トランザクションの外で、遅延読み込み（LAZY）の関連データにアクセスしている

**解決策:**
1. Service層のメソッドに `@Transactional` を付ける
2. 必要なデータを `JOIN FETCH` や `@EntityGraph` で最初にまとめて取得する

### `Duplicate entry` / 保存テストで主キーが重複する
**原因:** テストデータで固定IDを入れたため、自動採番のIDとぶつかっている

**解決策:**
1. `test-data.sql` の末尾の `ALTER TABLE ... RESTART WITH 100;` があるか確認
2. テストメソッドに `@Transactional`（`@DataJpaTest` は標準で付く）が効いているか確認

---

## 🎉 完了後

次は [Day 18](day-18.md) でDTO設計と実装を行う

お疲れさまでした！
