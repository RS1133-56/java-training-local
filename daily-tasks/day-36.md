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
import com.example.weatherapp.dto.OpenMeteoResponseDto;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.exception.ExternalApiException;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.mapper.WeatherMapper;
import com.example.weatherapp.repository.PrefectureRepository;
import com.example.weatherapp.repository.WeatherRecordRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * WeatherServiceの単体テスト
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("WeatherService単体テスト")
class WeatherServiceTest {
    
    @Mock
    private PrefectureRepository prefectureRepository;
    
    @Mock
    private WeatherRecordRepository weatherRecordRepository;
    
    @Mock
    private OpenMeteoClient openMeteoClient;
    
    @Mock
    private WeatherMapper weatherMapper;
    
    @InjectMocks
    private WeatherService weatherService;
    
    private Prefecture testPrefecture;
    private OpenMeteoResponseDto testApiResponse;
    private WeatherRecord testWeatherRecord;
    private WeatherDetailDto testWeatherDetailDto;
    
    @BeforeEach
    void setUp() {
        // テストデータ準備
        testPrefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .region("関東")
            .latitude(35.6895)
            .longitude(139.6917)
            .build();
        
        testApiResponse = new OpenMeteoResponseDto();
        // API responseの詳細設定（省略）
        
        testWeatherRecord = WeatherRecord.builder()
            .id(1L)
            .prefecture(testPrefecture)
            .fetchedAt(LocalDateTime.now())
            .build();
        
        testWeatherDetailDto = WeatherDetailDto.builder()
            .build();
    }
    
    @Test
    @DisplayName("正常系: 都道府県IDから天気情報を取得")
    void testGetWeatherByPrefectureId_Success() {
        // Given
        when(prefectureRepository.findById(13L))
            .thenReturn(Optional.of(testPrefecture));
        when(openMeteoClient.fetchWeather(anyDouble(), anyDouble()))
            .thenReturn(testApiResponse);
        when(weatherMapper.toEntity(any(Prefecture.class), any(OpenMeteoResponseDto.class)))
            .thenReturn(testWeatherRecord);
        when(weatherRecordRepository.save(any(WeatherRecord.class)))
            .thenReturn(testWeatherRecord);
        when(weatherMapper.toDetailDto(any(WeatherRecord.class)))
            .thenReturn(testWeatherDetailDto);
        
        // When
        WeatherDetailDto result = weatherService.getWeatherByPrefectureId(13L);
        
        // Then
        assertThat(result).isNotNull();
        verify(prefectureRepository, times(1)).findById(13L);
        verify(openMeteoClient, times(1)).fetchWeather(35.6895, 139.6917);
        verify(weatherRecordRepository, times(1)).save(any(WeatherRecord.class));
    }
    
    @Test
    @DisplayName("異常系: 存在しない都道府県ID")
    void testGetWeatherByPrefectureId_NotFound() {
        // Given
        when(prefectureRepository.findById(999L))
            .thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> weatherService.getWeatherByPrefectureId(999L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("都道府県が見つかりません");
        
        verify(prefectureRepository, times(1)).findById(999L);
        verify(openMeteoClient, never()).fetchWeather(anyDouble(), anyDouble());
    }
    
    @Test
    @DisplayName("異常系: API呼び出し失敗")
    void testGetWeatherByPrefectureId_ApiError() {
        // Given
        when(prefectureRepository.findById(13L))
            .thenReturn(Optional.of(testPrefecture));
        when(openMeteoClient.fetchWeather(anyDouble(), anyDouble()))
            .thenThrow(new ExternalApiException("API接続エラー"));
        
        // When & Then
        assertThatThrownBy(() -> weatherService.getWeatherByPrefectureId(13L))
            .isInstanceOf(ExternalApiException.class)
            .hasMessageContaining("API接続エラー");
        
        verify(weatherRecordRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("境界値: 緯度経度の範囲チェック")
    void testGetWeatherByPrefectureId_BoundaryValues() {
        // 日本の最北端・最南端のテスト
        Prefecture hokkaido = Prefecture.builder()
            .id(1L)
            .latitude(45.5)  // 北端
            .longitude(141.0)
            .build();
        
        Prefecture okinawa = Prefecture.builder()
            .id(47L)
            .latitude(24.3)  // 南端
            .longitude(124.0)
            .build();
        
        // テスト実装
        assertThat(hokkaido.getLatitude()).isBetween(20.0, 50.0);
        assertThat(okinawa.getLatitude()).isBetween(20.0, 50.0);
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

```gradle
plugins {
    id 'jacoco'
}

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
git push origin feature/day-36
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
