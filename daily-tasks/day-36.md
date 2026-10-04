# Day 36: テスト・品質保証

## 📅 実施日
- 予定: Week 8 - Day 36
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
包括的なテスト戦略を実装し、アプリケーションの品質を保証する

---

## 📋 午前の作業（9:00-13:00）

### 1. テスト戦略の策定（9:00-9:30）

**テストピラミッド:**

```
        /       /  \     E2E (少)
      /----     / 統合  \   Integration (中)
    /--------   /  単体    \  Unit (多)
  /----------```

**テストレベル:**

| レベル | 範囲 | ツール | 割合 |
|--------|------|--------|------|
| 単体テスト | メソッド単位 | JUnit | 70% |
| 統合テスト | 複数クラス | Spring Test | 20% |
| E2Eテスト | 画面操作 | MockMvc | 10% |

**カバレッジ目標:**
- ライン: 80%以上
- ブランチ: 70%以上
- 重要ロジック: 100%

---

### 2. 単体テスト強化（9:30-11:00）

**WeatherServiceの完全テスト:**

`src/test/java/com/example/weatherapp/service/WeatherServiceTest.java`:

```java
package com.example.weatherapp.service;

import com.example.weatherapp.client.OpenMeteoClient;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.dto.api.OpenMeteoResponseDto;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.exception.ExternalApiException;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.mapper.WeatherMapper;
import com.example.weatherapp.repository.WeatherRecordRepository;
import com.example.weatherapp.service.impl.WeatherServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * WeatherServiceImplの単体テスト（Day 21のテストを強化したもの）
 *
 * 外部API・DBはモックにして、Serviceのロジック
 * （APIレスポンス → Entity変換 → 保存 → DTO変換）を検証する
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("WeatherServiceImpl単体テスト")
class WeatherServiceTest {
    
    @Mock
    private PrefectureService prefectureService;
    
    @Mock
    private WeatherRecordRepository weatherRecordRepository;
    
    @Mock
    private OpenMeteoClient openMeteoClient;
    
    @Mock
    private WeatherMapper weatherMapper;
    
    @InjectMocks
    private WeatherServiceImpl weatherService;
    
    private Prefecture testPrefecture;
    private OpenMeteoResponseDto testApiResponse;
    
    @BeforeEach
    void setUp() {
        testPrefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .region("関東")
            .latitude(35.6895)
            .longitude(139.6917)
            .build();
        
        testApiResponse = createApiResponse();
    }
    
    /** 現在の天気 + 7日分の日次予報を持つ、テスト用のAPIレスポンスを作る */
    private OpenMeteoResponseDto createApiResponse() {
        OpenMeteoResponseDto.Current current = new OpenMeteoResponseDto.Current();
        current.setTemperature2m(15.5);
        current.setWeathercode(1);
        current.setWindspeed10m(3.2);
        current.setRelativehumidity2m(60);
        current.setApparentTemperature(14.0);
        current.setPrecipitation(0.0);
        current.setCloudCover(20);
        
        OpenMeteoResponseDto.Daily daily = new OpenMeteoResponseDto.Daily();
        daily.setTime(List.of("2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08",
            "2024-01-09", "2024-01-10", "2024-01-11"));
        daily.setTemperature2mMax(List.of(15.2, 14.0, 13.5, 12.0, 11.0, 13.0, 14.5));
        daily.setTemperature2mMin(List.of(8.1, 7.0, 6.5, 5.0, 4.0, 6.0, 7.5));
        daily.setWeathercode(List.of(61, 1, 2, 3, 0, 1, 2));
        daily.setPrecipitationSum(List.of(5.2, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0));
        daily.setWindspeed10mMax(List.of(8.1, 6.0, 5.5, 7.0, 4.0, 5.0, 6.5));
        daily.setSunrise(List.of("2024-01-05T06:51", "2024-01-06T06:51", "2024-01-07T06:51",
            "2024-01-08T06:51", "2024-01-09T06:51", "2024-01-10T06:50", "2024-01-11T06:50"));
        daily.setSunset(List.of("2024-01-05T16:46", "2024-01-06T16:47", "2024-01-07T16:48",
            "2024-01-08T16:49", "2024-01-09T16:50", "2024-01-10T16:51", "2024-01-11T16:52"));
        
        OpenMeteoResponseDto response = new OpenMeteoResponseDto();
        response.setCurrent(current);
        response.setDaily(daily);
        return response;
    }
    
    @Test
    @DisplayName("正常系: 都道府県IDから天気情報を取得し、現在+7日分をDBに保存する")
    void testGetWeatherByPrefectureId_Success() {
        // Given
        WeatherDetailDto dto = WeatherDetailDto.builder().build();
        when(prefectureService.findEntityById(13L)).thenReturn(testPrefecture);
        when(openMeteoClient.fetchWeather(35.6895, 139.6917)).thenReturn(testApiResponse);
        when(weatherRecordRepository.save(any(WeatherRecord.class)))
            .thenAnswer(invocation -> invocation.getArgument(0));  // 渡されたEntityをそのまま返す
        when(weatherMapper.toDetailDto(any(WeatherRecord.class))).thenReturn(dto);
        
        // When
        WeatherDetailDto result = weatherService.getWeatherByPrefectureId(13L);
        
        // Then
        assertThat(result).isSameAs(dto);
        
        // 保存されたEntityの中身を検証する
        ArgumentCaptor<WeatherRecord> captor = ArgumentCaptor.forClass(WeatherRecord.class);
        verify(weatherRecordRepository, times(1)).save(captor.capture());
        WeatherRecord saved = captor.getValue();
        assertThat(saved.getPrefecture()).isSameAs(testPrefecture);
        assertThat(saved.getTemperature()).isEqualTo(15.5);
        assertThat(saved.getWeatherCode()).isEqualTo(1);
        assertThat(saved.getDailyForecasts()).hasSize(7);
        assertThat(saved.getDailyForecasts().get(0).getTemperatureMax()).isEqualTo(15.2);
    }
    
    @Test
    @DisplayName("異常系: 存在しない都道府県ID")
    void testGetWeatherByPrefectureId_NotFound() {
        // Given
        when(prefectureService.findEntityById(999L))
            .thenThrow(new ResourceNotFoundException("都道府県が見つかりません: id=999"));
        
        // When & Then
        assertThatThrownBy(() -> weatherService.getWeatherByPrefectureId(999L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("都道府県が見つかりません");
        
        // 都道府県がなければ、外部APIは呼ばれない
        verify(openMeteoClient, never()).fetchWeather(anyDouble(), anyDouble());
    }
    
    @Test
    @DisplayName("異常系: API呼び出し失敗")
    void testGetWeatherByPrefectureId_ApiError() {
        // Given
        when(prefectureService.findEntityById(13L)).thenReturn(testPrefecture);
        when(openMeteoClient.fetchWeather(anyDouble(), anyDouble()))
            .thenThrow(new ExternalApiException("API接続エラー"));
        
        // When & Then
        assertThatThrownBy(() -> weatherService.getWeatherByPrefectureId(13L))
            .isInstanceOf(ExternalApiException.class)
            .hasMessageContaining("API接続エラー");
        
        // APIが失敗したら、DBには保存されない
        verify(weatherRecordRepository, never()).save(any());
    }
}
```

**Utilityクラスのテスト:**

```java
package com.example.weatherapp.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.assertj.core.api.Assertions.*;

/**
 * WeatherCodeUtilの単体テスト
 */
@DisplayName("WeatherCodeUtil単体テスト")
class WeatherCodeUtilTest {
    
    @ParameterizedTest
    @CsvSource({
        "0, 快晴",
        "1, 晴れ",
        "2, 一部曇り",
        "3, 曇り",
        "45, 霧",
        "61, 小雨",
        "71, 小雪",
        "95, 雷雨"
    })
    @DisplayName("天気コードから説明文を取得")
    void testGetDescription(int code, String expected) {
        assertThat(WeatherCodeUtil.getDescription(code))
            .isEqualTo(expected);
    }
    
    @Test
    @DisplayName("不明なコードの場合")
    void testGetDescription_Unknown() {
        assertThat(WeatherCodeUtil.getDescription(999))
            .isEqualTo("不明");
    }
    
    @ParameterizedTest
    @CsvSource({
        "0, ☀️",
        "1, 🌤️",
        "61, 🌧️",
        "95, ⛈️"
    })
    @DisplayName("天気コードから絵文字を取得")
    void testGetEmoji(int code, String expected) {
        assertThat(WeatherCodeUtil.getEmoji(code))
            .isEqualTo(expected);
    }
}
```

---

### 3. 統合テスト作成（11:00-12:00）

**完全な統合テスト:**

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
 * アプリケーション全体の統合テスト
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@Sql("/test-data.sql")
@DisplayName("アプリケーション統合テスト")
class ApplicationIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("トップページからデータ取得までの一連の流れ")
    void testCompleteUserFlow() throws Exception {
        // 1. トップページアクセス
        mockMvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(view().name("index"))
            .andExpect(model().attributeExists("groupedPrefectures"));
        
        // 2. 東京都の天気ページアクセス
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("weather-detail"))
            .andExpect(model().attributeExists("weather"));
        
        // 3. 地域フィルタ
        mockMvc.perform(get("/").param("region", "関東"))
            .andExpect(status().isOk())
            .andExpect(model().attribute("selectedRegion", "関東"));
    }
    
    @Test
    @DisplayName("エラーハンドリングの動作確認")
    void testErrorHandling() throws Exception {
        // 存在しない都道府県
        mockMvc.perform(get("/weather/999"))
            .andExpect(status().isNotFound());
        
        // 存在しないページ
        mockMvc.perform(get("/nonexistent"))
            .andExpect(status().isNotFound());
    }
}
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. パフォーマンステスト（13:00-14:30）

**負荷テスト用スクリプト:**

`src/test/java/com/example/weatherapp/performance/PerformanceTest.java`:

```java
package com.example.weatherapp.performance;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.assertj.core.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

/**
 * パフォーマンステスト
 */
@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("パフォーマンステスト")
class PerformanceTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("並行リクエスト処理性能")
    void testConcurrentRequests() throws Exception {
        int threadCount = 100;
        int requestsPerThread = 10;
        
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch latch = new CountDownLatch(threadCount * requestsPerThread);
        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger errorCount = new AtomicInteger(0);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < requestsPerThread; j++) {
                    try {
                        mockMvc.perform(get("/"));
                        successCount.incrementAndGet();
                    } catch (Exception e) {
                        errorCount.incrementAndGet();
                    } finally {
                        latch.countDown();
                    }
                }
            });
        }
        
        latch.await(30, TimeUnit.SECONDS);
        executor.shutdown();
        
        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        
        System.out.println("総リクエスト数: " + (threadCount * requestsPerThread));
        System.out.println("成功: " + successCount.get());
        System.out.println("失敗: " + errorCount.get());
        System.out.println("所要時間: " + duration + "ms");
        System.out.println("平均応答時間: " + (duration / (threadCount * requestsPerThread)) + "ms");
        
        // 成功率95%以上を期待
        double successRate = (double) successCount.get() / (threadCount * requestsPerThread);
        assertThat(successRate).isGreaterThan(0.95);
    }
}
```

---

### 5. セキュリティテスト（14:30-16:00）

**セキュリティチェックリスト:**

`security-checklist.md`:

```markdown
# セキュリティチェックリスト

## ✅ XSS対策
- [ ] すべてのユーザー入力をエスケープ
- [ ] Thymeleafのth:text使用
- [ ] Content-Security-Policy設定

## ✅ CSRF対策
- [ ] Spring SecurityのCSRF有効化
- [ ] フォームにCSRFトークン

## ✅ SQLインジェクション対策
- [ ] JPAのパラメータバインディング使用
- [ ] 生SQLを使用しない

## ✅ 認証・認可
- [ ] パスワードのハッシュ化
- [ ] セッション管理の適切な実装

## ✅ HTTPヘッダー
- [ ] X-Frame-Options設定
- [ ] X-Content-Type-Options設定
- [ ] Strict-Transport-Security設定

## ✅ 依存関係
- [ ] 脆弱性のある依存関係なし
- [ ] 定期的なアップデート
```

**セキュリティテスト:**

```java
@Test
@DisplayName("XSS対策確認")
void testXssPrevention() throws Exception {
    String maliciousScript = "<script>alert('XSS')</script>";
    
    mockMvc.perform(get("/")
            .param("search", maliciousScript))
        .andExpect(status().isOk())
        .andExpect(content().string(not(containsString("<script>"))));
}
```

---

### 6. テストレポート作成（16:00-17:00）

**JaCoCoカバレッジレポート設定:**

`build.gradle`に追加：

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
    toolVersion = "0.8.11"
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }
    
    afterEvaluate {
        classDirectories.setFrom(files(classDirectories.files.collect {
            fileTree(dir: it, exclude: [
                '**/dto/**',
                '**/entity/**',
                '**/config/**'
            ])
        }))
    }
}

test {
    finalizedBy jacocoTestReport
}
```

**カバレッジ確認:**

```bash
./gradlew clean test jacocoTestReport
```

レポート場所: `build/reports/jacoco/test/html/index.html`

**テストレポートサマリー:**

`test-report-summary.md`:

```markdown
# テストレポートサマリー

## テスト実行結果

### 単体テスト
- 実行: 85件
- 成功: 85件
- 失敗: 0件
- スキップ: 0件

### 統合テスト
- 実行: 25件
- 成功: 25件
- 失敗: 0件

### E2Eテスト
- 実行: 10件
- 成功: 10件
- 失敗: 0件

## カバレッジ

### 全体
- ライン: 82%
- ブランチ: 75%
- クラス: 90%

### コンポーネント別
- Controller: 85%
- Service: 90%
- Repository: 100%
- Mapper: 80%

## パフォーマンス
- 平均応答時間: 45ms
- 並行100リクエスト: 成功率98%

## セキュリティ
- XSS対策: ✅
- CSRF対策: ✅
- SQLインジェクション: ✅

## 品質評価
総合評価: **A**（85点以上）
```

---

## ✅ チェックリスト

- [ ] 単体テストを強化した
- [ ] 統合テストを作成した
- [ ] E2Eテストを作成した
- [ ] パフォーマンステストを実施した
- [ ] セキュリティテストを実施した
- [ ] カバレッジ80%以上を達成した
- [ ] テストレポートを作成した
- [ ] すべてのテストが成功した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "test: テスト・品質保証完了"
git push origin main
```

---

## 📚 参考リンク

### テスト
- [JUnit 5（日本語）](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito（日本語）](https://site.mockito.org/)
- [AssertJ（日本語）](https://assertj.github.io/doc/)

### カバレッジ
- [JaCoCo](https://www.jacoco.org/jacoco/)

### Spring Test
- [Spring Boot Testing（日本語）](https://spring.pleiades.io/spring-boot/docs/current/reference/html/features.html#features.testing)

---

## 🆘 トラブルシューティング

### JaCoCoのレポートが生成されない
**原因:** テストだけを実行していて、レポート生成のタスクを実行していない

**解決策:**
1. `./gradlew test jacocoTestReport` を実行する
2. レポートは `build/reports/jacoco/test/html/index.html` をブラウザで開く
3. `build.gradle` に `jacoco` プラグインが入っているか確認

### カバレッジがなかなか上がらない
**原因:** どこが未テストか把握できていない

**解決策:**
1. JaCoCoのレポートで、**赤・黄色の行**（未実行・一部のみ）を確認する
2. 全体を均等に上げようとせず、Serviceなどロジックの多い部分から優先する
3. 目標の数字そのものより、「重要な分岐がテストされているか」を重視する

### `Failed to load ApplicationContext`
**原因:** アプリの起動に失敗している（原因は別にある）

**解決策:**
1. エラーメッセージの**一番下の `Caused by:`** を読む（そこに本当の原因がある）
2. Beanの不足、設定ファイルの値、DBの接続設定が主な原因

### テストを単独だと通るのに、全体で実行すると失敗する
**原因:** テスト同士がデータや状態を共有してしまっている

**解決策:**
1. 各テストの `@BeforeEach` でデータを準備し直す
2. DBを使うテストには `@Transactional` を付けて、テスト後にロールバックする
3. テストが実行順に依存しないようにする

### テストが遅い／ネットワークの状態で不安定になる
**原因:** `@SpringBootTest` の使いすぎ、または本物の外部APIを呼んでいる

**解決策:**
1. Controllerは `@WebMvcTest`、Repositoryは `@DataJpaTest`、Serviceはモックのみで、軽いテストにする
2. 外部APIは必ずモックにする（本物のAPIを呼ばない）

### 特定のテストだけ実行したい
**原因:** 実行方法を知らない

**解決策:**
1. `./gradlew test --tests クラス名` でクラス単位、`--tests クラス名.メソッド名` でメソッド単位に実行できる

---

## 📝 本日のまとめ

1. **実装した機能:**
   - 包括的なテストスイート
   - パフォーマンステスト
   - セキュリティテスト
   - カバレッジレポート

2. **学んだこと:**
   - テストピラミッド
   - テスト駆動開発
   - 品質保証プロセス

3. **明日への引き継ぎ:**
   - Day 37でドキュメント作成

---

## 🎉 完了後

次は [Day 37](day-37.md) へ

お疲れさまでした！
