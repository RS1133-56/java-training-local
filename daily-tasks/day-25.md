# Day 25: バックエンド統合テスト

## 📅 実施日
- 予定: Week 5 - Day 25
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
@SpringBootTestを使った統合テストを作成し、バックエンド全体の動作を確認する

---

## 📋 午前の作業（9:00-13:00）

### 1. 統合テストの基礎理解（9:00-9:30）

**統合テストとは:**
- 複数のコンポーネントを組み合わせてテスト
- 実際のDBを使用（テスト用DB）
- 実際のアプリケーション起動

**単体テストとの違い:**

| 項目 | 単体テスト | 統合テスト |
|------|-----------|-----------|
| 対象 | 1つのクラス | 複数のコンポーネント |
| DB | モック | 実際のDB |
| 起動 | 一部のみ | アプリ全体 |
| 速度 | 速い | 遅い |
| アノテーション | @WebMvcTest, @DataJpaTest | @SpringBootTest |

**統合テストの種類:**

```
1. サービス統合テスト
   Service + Repository + Database

2. コントローラー統合テスト
   Controller + Service + Repository + Database

3. E2Eテスト（End-to-End）
   ブラウザ + アプリ全体
```

**学習用ドキュメント作成:**

`integration-test-guide.md`を作成：

```markdown
# Spring Boot 統合テストガイド

## @SpringBootTestの使い方

アプリケーション全体を起動してテスト。

```java
@SpringBootTest
@Transactional  // テスト後に自動ロールバック
class MyIntegrationTest {
    
    @Autowired
    private MyService service;
    
    @Test
    void testServiceMethod() {
        // 実際のDBを使用
        Result result = service.doSomething();
        assertThat(result).isNotNull();
    }
}
```

## テストデータの準備

### 1. @Sql アノテーション

```java
@SpringBootTest
@Sql("/test-data.sql")  // テスト前に実行
class MyTest {
    // テストメソッド
}
```

### 2. @BeforeEachでセットアップ

```java
@BeforeEach
void setUp() {
    Prefecture tokyo = Prefecture.builder()
        .name("東京都")
        .build();
    prefectureRepository.save(tokyo);
}
```

## @Transactionalの役割

テストメソッド終了後、自動的にロールバック。

```java
@SpringBootTest
@Transactional  // 重要！
class MyTest {
    
    @Test
    void testInsert() {
        // データを挿入
        repository.save(entity);
        
        // テスト終了後、自動ロールバック
        // DBは元の状態に戻る
    }
}
```

## テストの階層化

```java
// 1. Repository層
@DataJpaTest
class PrefectureRepositoryTest { }

// 2. Service層（Repositoryをモック）
@ExtendWith(MockitoExtension.class)
class PrefectureServiceTest { }

// 3. 統合テスト（全体）
@SpringBootTest
class PrefectureIntegrationTest { }
```

## MockMvcとRestAssured

### MockMvc（コントローラーテスト）

```java
@SpringBootTest
@AutoConfigureMockMvc
class ControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void test() throws Exception {
        mockMvc.perform(get("/api/data"))
            .andExpect(status().isOk());
    }
}
```

### RestAssured（REST API テスト）

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class ApiTest {
    
    @LocalServerPort
    private int port;
    
    @Test
    void test() {
        given()
            .port(port)
        .when()
            .get("/api/data")
        .then()
            .statusCode(200);
    }
}
```
```

---

### 2. サービス層統合テスト作成（9:30-12:00）

**PrefectureService統合テスト:** `src/test/java/com/example/weatherapp/integration/PrefectureServiceIntegrationTest.java`

```java
package com.example.weatherapp.integration;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.service.PrefectureService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.*;

/**
 * PrefectureServiceの統合テスト
 * 実際のDBを使用してService層をテスト
 */
@SpringBootTest
@Transactional
@Sql("/test-data.sql")  // テストデータ投入
class PrefectureServiceIntegrationTest {
    
    @Autowired
    private PrefectureService prefectureService;
    
    @Test
    @DisplayName("全都道府県を取得できる")
    void testFindAll() {
        // When
        List<PrefectureDto> prefectures = prefectureService.findAll();
        
        // Then
        assertThat(prefectures).isNotNull();
        assertThat(prefectures).hasSize(47);
        assertThat(prefectures).extracting("name")
            .contains("北海道", "東京都", "大阪府", "沖縄県");
    }
    
    @Test
    @DisplayName("IDで都道府県を取得できる")
    void testFindById() {
        // When
        PrefectureDto tokyo = prefectureService.findById(13L);
        
        // Then
        assertThat(tokyo).isNotNull();
        assertThat(tokyo.getName()).isEqualTo("東京都");
        assertThat(tokyo.getNameEn()).isEqualTo("Tokyo");
        assertThat(tokyo.getRegion()).isEqualTo("関東");
        assertThat(tokyo.getLatitude()).isCloseTo(35.689, within(0.001));
        assertThat(tokyo.getLongitude()).isCloseTo(139.692, within(0.001));
    }
    
    @Test
    @DisplayName("存在しないIDで例外が発生する")
    void testFindById_NotFound() {
        // When & Then
        assertThatThrownBy(() -> prefectureService.findById(999L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("都道府県が見つかりません");
    }
    
    @Test
    @DisplayName("地域別に都道府県を取得できる")
    void testFindByRegion() {
        // When
        List<PrefectureDto> kanto = prefectureService.findByRegion("関東");
        
        // Then
        assertThat(kanto).isNotNull();
        assertThat(kanto).hasSize(7);  // 東京、神奈川、埼玉、千葉、茨城、栃木、群馬
        assertThat(kanto).extracting("name")
            .contains("東京都", "神奈川県", "埼玉県");
    }
    
    @Test
    @DisplayName("地域別グループ化が正しく動作する")
    void testFindAllGroupedByRegion() {
        // When
        Map<String, List<PrefectureDto>> grouped = 
            prefectureService.findAllGroupedByRegion();
        
        // Then
        assertThat(grouped).isNotNull();
        assertThat(grouped).hasSize(9);  // 9地域
        
        assertThat(grouped).containsKeys(
            "北海道", "東北", "関東", "中部", 
            "関西", "中国", "四国", "九州", "沖縄"
        );
        
        // 関東地方の検証
        List<PrefectureDto> kanto = grouped.get("関東");
        assertThat(kanto).hasSize(7);
        assertThat(kanto).extracting("region")
            .containsOnly("関東");
    }
    
    @Test
    @DisplayName("名前で都道府県を検索できる")
    void testFindByName() {
        // When
        PrefectureDto result = prefectureService.findByName("大阪府");
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(27L);
        assertThat(result.getNameEn()).isEqualTo("Osaka");
        assertThat(result.getRegion()).isEqualTo("関西");
    }
}
```

**WeatherService統合テスト:** `src/test/java/com/example/weatherapp/integration/WeatherServiceIntegrationTest.java`

```java
package com.example.weatherapp.integration;

import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.repository.WeatherRecordRepository;
import com.example.weatherapp.service.WeatherService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

/**
 * WeatherServiceの統合テスト
 * 実際のAPIを呼び出すため、テストに時間がかかる
 */
@SpringBootTest
@Transactional
@Sql("/test-data.sql")
class WeatherServiceIntegrationTest {
    
    @Autowired
    private WeatherService weatherService;
    
    @Autowired
    private WeatherRecordRepository weatherRecordRepository;
    
    @Test
    @DisplayName("天気情報を取得してDBに保存できる")
    void testGetWeatherByPrefectureId() {
        // Given
        Long tokyoId = 13L;
        
        // When
        WeatherDetailDto result = weatherService.getWeatherByPrefectureId(tokyoId);
        
        // Then
        // DTOの検証
        assertThat(result).isNotNull();
        assertThat(result.getPrefecture()).isNotNull();
        assertThat(result.getPrefecture().getName()).isEqualTo("東京都");
        
        // 現在の天気
        assertThat(result.getCurrent()).isNotNull();
        assertThat(result.getCurrent().getTemperature()).isNotNull();
        assertThat(result.getCurrent().getWeatherCode()).isNotNull();
        
        // 日次予報（7日分）
        assertThat(result.getDailyForecasts()).isNotNull();
        assertThat(result.getDailyForecasts()).hasSize(7);
        
        // DBに保存されているか確認
        List<WeatherRecord> saved = weatherRecordRepository
            .findByPrefectureIdOrderByFetchedAtDesc(tokyoId);
        
        assertThat(saved).isNotEmpty();
        assertThat(saved.get(0).getPrefecture().getId()).isEqualTo(tokyoId);
        assertThat(saved.get(0).getDailyForecasts()).hasSize(7);
    }
    
    @Test
    @DisplayName("DB保存済みの最新天気を取得できる")
    void testGetLatestWeatherFromDb() {
        // Given: 事前に天気データを保存
        weatherService.getWeatherByPrefectureId(13L);
        
        // When: DB から取得（API呼び出しなし）
        WeatherDetailDto result = weatherService.getLatestWeatherFromDb(13L);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getPrefecture().getName()).isEqualTo("東京都");
        assertThat(result.getCurrent()).isNotNull();
        assertThat(result.getDailyForecasts()).hasSize(7);
    }
    
    @Test
    @DisplayName("天気データがない場合はnullを返す")
    void testGetLatestWeatherFromDb_NoData() {
        // When: データが存在しない都道府県
        WeatherDetailDto result = weatherService.getLatestWeatherFromDb(1L);
        
        // Then
        assertThat(result).isNull();
    }
}
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. コントローラー統合テスト（13:00-15:00）

`src/test/java/com/example/weatherapp/integration/HomeControllerIntegrationTest.java`:

```java
package com.example.weatherapp.integration;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

/**
 * HomeControllerの統合テスト
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@Sql("/test-data.sql")
class HomeControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("トップページが表示される")
    void testIndexPage() throws Exception {
        mockMvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(view().name("index"))
            .andExpect(model().attributeExists("groupedPrefectures"))
            .andExpect(model().attributeExists("regions"));
    }
    
    @Test
    @DisplayName("地域フィルタが動作する")
    void testIndexWithRegionFilter() throws Exception {
        mockMvc.perform(get("/").param("region", "関東"))
            .andExpect(status().isOk())
            .andExpect(model().attributeExists("prefectures"))
            .andExpect(model().attribute("selectedRegion", "関東"))
            .andExpect(model().attribute("prefectures", hasSize(7)));
    }
}
```

`src/test/java/com/example/weatherapp/integration/WeatherControllerIntegrationTest.java`:

```java
package com.example.weatherapp.integration;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * WeatherControllerの統合テスト
 * 実際のAPIを呼び出すため時間がかかる
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@Sql("/test-data.sql")
class WeatherControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("天気詳細ページが表示される")
    void testWeatherDetailPage() throws Exception {
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("weather-detail"))
            .andExpect(model().attributeExists("weather"))
            .andExpect(model().attribute("weather", 
                hasProperty("prefecture", 
                    hasProperty("name", is("東京都"))
                )
            ));
    }
    
    @Test
    @DisplayName("存在しない都道府県で404エラー")
    void testWeatherDetail_NotFound() throws Exception {
        mockMvc.perform(get("/weather/999"))
            .andExpect(status().isNotFound())
            .andExpect(view().name("error/404"));
    }
}
```

---

### 4. テストデータ準備（15:00-16:00）

`src/test/resources/test-data.sql` は、**Day 17で作成したものをそのまま使います**（47都道府県が入っています）。

次の内容になっているか確認しましょう。

| 確認項目 | 期待値 |
|---|---|
| `prefectures` テーブルの件数 | 47件 |
| 地域ごとの件数 | 北海道1 / 東北6 / 関東7 / 中部9 / 関西7 / 中国5 / 四国4 / 九州7 / 沖縄1 |
| 東京都 | id=13 |
| `created_at` / `updated_at` | すべての行に値が入っている（NOT NULLのため） |

> ⚠️ INSERT文のテーブル名は `prefectures`（複数形）です。`prefecture`（単数形）だと
> `Table "PREFECTURE" not found` のエラーになります。

---

### 5. テスト実行とカバレッジ確認（16:00-17:00）

**全テスト実行:**

```bash
./gradlew test
```

**カバレッジレポート生成:**

`build.gradle`にJaCoCo追加:

> ⚠️ `build.gradle` の `plugins { }` ブロックは**ファイルに1つだけ**しか書けません。
> 新しく `plugins { }` を書き足すのではなく、**すでにある `plugins { }` の中に `id 'jacoco'` の1行を追加**してください。
> それ以外（`jacoco { }` など）は、ファイルの末尾に追加します。

```gradle
// ① 既存の plugins { } ブロックの中に1行追加する
plugins {
    id 'java'
    id 'org.springframework.boot' version '...'   // 既存の行はそのまま
    id 'io.spring.dependency-management' version '...'
    id 'jacoco'                                    // ← これを追加
}

// ② 以降は、ファイルの末尾に追加する
jacoco {
    toolVersion = "0.8.10"
}

test {
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }
}
```

**カバレッジ確認:**

```bash
./gradlew jacocoTestReport

# レポート表示
open build/reports/jacoco/test/html/index.html
```

**テストサマリー作成:**

`test-summary.md`を作成：

```markdown
# テストサマリー

## テスト実行結果

- 総テスト数: XX件
- 成功: XX件
- 失敗: 0件
- スキップ: 0件

## カバレッジ

- Line Coverage: XX%
- Branch Coverage: XX%

## テスト階層

### Repository層
- PrefectureRepositoryTest
- WeatherRecordRepositoryTest
- DailyForecastRepositoryTest

### Service層
- PrefectureServiceTest
- WeatherServiceTest

### Controller層
- HomeControllerTest
- WeatherControllerTest

### 統合テスト
- PrefectureServiceIntegrationTest
- WeatherServiceIntegrationTest
- HomeControllerIntegrationTest
- WeatherControllerIntegrationTest
```

---

## ✅ チェックリスト

- [ ] 統合テストの概念を理解した
- [ ] PrefectureService統合テストを作成した
- [ ] WeatherService統合テストを作成した
- [ ] Controller統合テストを作成した
- [ ] テストデータ（test-data.sql）を作成した
- [ ] すべてのテストがパスした
- [ ] カバレッジレポートを確認した
- [ ] integration-test-guide.mdを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "test(integration): バックエンド統合テストを実装"
git push origin main
```

---

## 📚 参考リンク

### Spring Boot テスト
- [@SpringBootTest公式ドキュメント](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
- [統合テストの書き方（日本語）](https://qiita.com/disc99/items/31fa7abb724f63602dc9)
- [@Transactionalとテスト（日本語）](https://qiita.com/NagaokaKenichi/items/c3371ce8dea0a1f8fa5b)

### テストデータ準備
- [@Sqlの使い方（日本語）](https://qiita.com/rubytomato@github/items/f5c5c3e5c8c8d6c4e9c3)
- [テストデータ管理（日本語）](https://qiita.com/disc99/items/b613b9b3bc5d796c840c)

### JaCoCo（カバレッジ）
- [JaCoCo公式サイト](https://www.jacoco.org/)
- [JaCoCo + Gradle（日本語）](https://qiita.com/tag1216/items/3680b92cf96eb5a170f0)

---

## 🆘 トラブルシューティング

### テストがタイムアウトする
**症状:** 外部API呼び出しでテストが遅い

**原因:** 実際のAPIを呼び出している

**解決策:**
```java
// 統合テストは時間がかかることを許容
@Test
@Timeout(30)  // 30秒まで許容
void testApiCall() {
    // ...
}
```

### トランザクションがロールバックされない
**症状:** テストデータがDBに残る

**原因:** @Transactionalがない

**解決策:**
```java
@SpringBootTest
@Transactional  // これを追加
class MyTest {
    // ...
}
```

### テストデータが見つからない
**症状:** test-data.sqlが実行されない

**原因:** ファイルパスが間違っている

**解決策:**
```
src/test/resources/
  └── test-data.sql  // ここに配置

@Sql("/test-data.sql")  // スラッシュから始める
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - サービス層統合テスト
   - コントローラー統合テスト
   - テストデータ準備

2. **学んだこと:**
   - @SpringBootTestの使い方
   - 統合テストと単体テストの違い
   - カバレッジの確認方法

3. **明日への引き継ぎ:**
   - Day 26でThymeleafテンプレート実装開始

---

## 🎉 完了後

次は [Day 26](day-26.md) へ

お疲れさまでした！
