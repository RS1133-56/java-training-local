# Day 23: Controller層実装（Weather）

## 📅 実施日
- 予定: Week 5 - Day 23
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
WeatherControllerを実装し、都道府県ごとの天気詳細ページを表示する

---

## 📋 午前の作業（9:00-13:00）

### 1. WeatherControllerの設計（9:00-9:30）

**WeatherControllerの責務:**
- 都道府県IDをパラメータで受け取る
- WeatherServiceから天気情報を取得
- 取得した情報をModelに設定
- 詳細ページ（weather-detail.html）を表示

**URL設計:**
```
/weather/{id}
例: /weather/13 → 東京都の天気詳細
```

**処理フロー:**
```
Browser: GET /weather/13
    ↓
WeatherController
    ↓ prefectureId = 13
WeatherService.getWeatherByPrefectureId(13)
    ↓
WeatherDetailDto取得
    ↓
Model.addAttribute("weather", dto)
    ↓
return "weather-detail"
    ↓
templates/weather-detail.html
    ↓
Browser: HTML表示
```

---

### 2. WeatherController実装（9:30-12:00）

**Controllerクラス作成:** `src/main/java/com/example/weatherapp/controller/WeatherController.java`

```java
package com.example.weatherapp.controller;

import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.exception.ExternalApiException;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.service.WeatherService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * 天気詳細画面のController
 */
@Controller
@RequestMapping("/weather")
@Slf4j
public class WeatherController {
    
    private final WeatherService weatherService;
    
    public WeatherController(WeatherService weatherService) {
        this.weatherService = weatherService;
    }
    
    /**
     * 天気詳細ページ表示
     * 
     * URL: /weather/{id}
     * 例: /weather/13 → 東京都の天気
     * 
     * @param id 都道府県ID
     * @param model ビューに渡すデータ
     * @return テンプレート名
     */
    @GetMapping("/{id}")
    public String showWeather(
        @PathVariable Long id,
        Model model
    ) {
        log.info("天気詳細ページ表示: prefectureId={}", id);
        
        try {
            // 天気情報を取得（API呼び出し → DB保存 → DTO返却）
            WeatherDetailDto weather = weatherService.getWeatherByPrefectureId(id);
            
            // Modelに設定
            model.addAttribute("weather", weather);
            
            log.debug("天気情報取得成功: {}", weather.getPrefecture().getName());
            
            return "weather-detail";
            
        } catch (ResourceNotFoundException e) {
            // 都道府県が存在しない
            log.warn("都道府県が見つかりません: id={}", id);
            model.addAttribute("errorMessage", "指定された都道府県が見つかりません");
            return "error/404";
            
        } catch (ExternalApiException e) {
            // API呼び出し失敗
            log.error("天気API呼び出し失敗: id={}", id, e);
            model.addAttribute("errorMessage", "天気情報の取得に失敗しました");
            model.addAttribute("prefectureId", id);
            return "error/api-error";
            
        } catch (Exception e) {
            // その他の予期しないエラー
            log.error("予期しないエラー: id={}", id, e);
            model.addAttribute("errorMessage", "システムエラーが発生しました");
            return "error/500";
        }
    }
    
    /**
     * DB保存済みの最新天気を表示（API呼び出しなし）
     * 
     * URL: /weather/{id}/latest
     * 
     * @param id 都道府県ID
     * @param model ビューに渡すデータ
     * @return テンプレート名
     */
    @GetMapping("/{id}/latest")
    public String showLatestWeather(
        @PathVariable Long id,
        Model model
    ) {
        log.info("最新天気表示（DB）: prefectureId={}", id);
        
        try {
            WeatherDetailDto weather = weatherService.getLatestWeatherFromDb(id);
            
            if (weather == null) {
                log.warn("天気データが存在しません: id={}", id);
                model.addAttribute("errorMessage", "天気データがまだ取得されていません");
                return "error/404";
            }
            
            model.addAttribute("weather", weather);
            return "weather-detail";
            
        } catch (Exception e) {
            log.error("エラー: id={}", id, e);
            model.addAttribute("errorMessage", "エラーが発生しました");
            return "error/500";
        }
    }
}
```

**実装のポイント:**

1. **@RequestMapping("/weather")**
   - クラスレベルで共通のパスを定義
   - すべてのメソッドで `/weather` がプレフィックスになる

2. **@PathVariable Long id**
   - URLパスの `{id}` を変数として受け取る
   - `/weather/13` → id = 13

3. **try-catch による例外ハンドリング**
   - `ResourceNotFoundException`: 404エラー
   - `ExternalApiException`: APIエラー
   - その他: 500エラー

4. **ログ出力**
   - info: 正常な処理の記録
   - warn: 異常だが処理継続可能
   - error: エラー発生時の詳細記録

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. WeatherControllerのテスト作成（13:00-15:30）

`src/test/java/com/example/weatherapp/controller/WeatherControllerTest.java`:

```java
package com.example.weatherapp.controller;

import com.example.weatherapp.dto.CurrentWeatherDto;
import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.exception.ExternalApiException;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.service.WeatherService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.ArrayList;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

/**
 * WeatherControllerのテスト
 */
@WebMvcTest(WeatherController.class)
class WeatherControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private WeatherService weatherService;
    
    private WeatherDetailDto weatherDetail;
    
    @BeforeEach
    void setUp() {
        // テストデータ準備
        PrefectureDto prefecture = PrefectureDto.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .region("関東")
            .build();
        
        CurrentWeatherDto current = CurrentWeatherDto.builder()
            .time(LocalDateTime.now())
            .temperature(15.5)
            .weatherCode(1)
            .weatherDescription("晴れ")
            .build();
        
        weatherDetail = WeatherDetailDto.builder()
            .prefecture(prefecture)
            .current(current)
            .dailyForecasts(new ArrayList<>())
            .fetchedAt(LocalDateTime.now())
            .build();
    }
    
    @Test
    @DisplayName("天気詳細ページが正しく表示される")
    void testShowWeather_Success() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(13L))
            .thenReturn(weatherDetail);
        
        // When & Then
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("weather-detail"))
            .andExpect(model().attributeExists("weather"))
            .andExpect(model().attribute("weather", weatherDetail))
            .andExpect(model().attribute("weather", 
                hasProperty("prefecture", 
                    hasProperty("name", is("東京都"))
                )
            ));
        
        verify(weatherService, times(1)).getWeatherByPrefectureId(13L);
    }
    
    @Test
    @DisplayName("存在しない都道府県で404エラーが表示される")
    void testShowWeather_NotFound() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(999L))
            .thenThrow(new ResourceNotFoundException("都道府県が見つかりません"));
        
        // When & Then
        mockMvc.perform(get("/weather/999"))
            .andExpect(status().isOk())
            .andExpect(view().name("error/404"))
            .andExpect(model().attributeExists("errorMessage"))
            .andExpect(model().attribute("errorMessage", 
                containsString("見つかりません")));
        
        verify(weatherService, times(1)).getWeatherByPrefectureId(999L);
    }
    
    @Test
    @DisplayName("API呼び出し失敗時にエラーページが表示される")
    void testShowWeather_ApiError() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(13L))
            .thenThrow(new ExternalApiException("API呼び出し失敗"));
        
        // When & Then
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("error/api-error"))
            .andExpect(model().attributeExists("errorMessage"))
            .andExpect(model().attribute("prefectureId", 13L));
        
        verify(weatherService, times(1)).getWeatherByPrefectureId(13L);
    }
    
    @Test
    @DisplayName("予期しないエラーで500エラーが表示される")
    void testShowWeather_UnexpectedError() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(13L))
            .thenThrow(new RuntimeException("予期しないエラー"));
        
        // When & Then
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("error/500"))
            .andExpect(model().attributeExists("errorMessage"));
        
        verify(weatherService, times(1)).getWeatherByPrefectureId(13L);
    }
    
    @Test
    @DisplayName("DB保存済みの最新天気を表示できる")
    void testShowLatestWeather_Success() throws Exception {
        // Given
        when(weatherService.getLatestWeatherFromDb(13L))
            .thenReturn(weatherDetail);
        
        // When & Then
        mockMvc.perform(get("/weather/13/latest"))
            .andExpect(status().isOk())
            .andExpect(view().name("weather-detail"))
            .andExpect(model().attributeExists("weather"));
        
        verify(weatherService, times(1)).getLatestWeatherFromDb(13L);
    }
    
    @Test
    @DisplayName("DBに天気データがない場合404エラー")
    void testShowLatestWeather_NoData() throws Exception {
        // Given
        when(weatherService.getLatestWeatherFromDb(13L))
            .thenReturn(null);
        
        // When & Then
        mockMvc.perform(get("/weather/13/latest"))
            .andExpect(status().isOk())
            .andExpect(view().name("error/404"))
            .andExpect(model().attribute("errorMessage", 
                containsString("まだ取得されていません")));
        
        verify(weatherService, times(1)).getLatestWeatherFromDb(13L);
    }
}
```

**テストのポイント:**

1. **正常系テスト**
   - 天気情報が正しく表示される
   - Modelに正しいデータが設定される

2. **異常系テスト**
   - 404エラー: 都道府県が存在しない
   - APIエラー: 外部API呼び出し失敗
   - 500エラー: 予期しないエラー

3. **Hamcrest Matchers**
   - `hasProperty()`: ネストしたオブジェクトの検証
   - `containsString()`: 文字列の部分一致

---

### 4. 簡易的なエラーページ作成（15:30-17:00）

`src/main/resources/templates/error/404.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>404 - ページが見つかりません</title>
    <style>
        body {
            font-family: sans-serif;
            text-align: center;
            padding: 50px;
        }
        .error-code {
            font-size: 72px;
            color: #e74c3c;
        }
        .error-message {
            font-size: 24px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="error-code">404</div>
    <div class="error-message" th:text="${errorMessage}">ページが見つかりません</div>
    <a href="/">トップページに戻る</a>
</body>
</html>
```

`src/main/resources/templates/error/api-error.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>API Error</title>
</head>
<body>
    <h1>天気情報の取得に失敗しました</h1>
    <p th:text="${errorMessage}"></p>
    <p>
        <a th:href="@{/weather/{id}(id=${prefectureId})}">再試行</a> |
        <a href="/">トップページに戻る</a>
    </p>
</body>
</html>
```

`src/main/resources/templates/error/500.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>500 - サーバーエラー</title>
</head>
<body>
    <h1>システムエラーが発生しました</h1>
    <p th:text="${errorMessage}"></p>
    <a href="/">トップページに戻る</a>
</body>
</html>
```

`src/main/resources/templates/weather-detail.html`（簡易版）:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title th:text="${weather.prefecture.name} + 'の天気'">天気詳細</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: #4CAF50;
            color: white;
            padding: 20px;
        }
        .current-weather {
            border: 2px solid #ddd;
            padding: 20px;
            margin: 20px 0;
        }
        .forecast {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
        .forecast-day {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 th:text="${weather.prefecture.name} + 'の天気'"></h1>
        <p th:text="'更新: ' + ${#temporals.format(weather.fetchedAt, 'yyyy/MM/dd HH:mm')}"></p>
    </div>
    
    <div class="current-weather">
        <h2>現在の天気</h2>
        <p>気温: <span th:text="${weather.current.temperature} + '℃'"></span></p>
        <p>天気: <span th:text="${weather.current.weatherDescription}"></span></p>
        <p>風速: <span th:text="${weather.current.windSpeed} + 'm/s'"></span></p>
        <p>湿度: <span th:text="${weather.current.humidity} + '%'"></span></p>
    </div>
    
    <h2>週間天気予報</h2>
    <div class="forecast">
        <div th:each="day : ${weather.dailyForecasts}" class="forecast-day">
            <div th:text="${#temporals.format(day.date, 'M/d')}"></div>
            <div th:text="${day.dayOfWeek}"></div>
            <div th:text="${day.weatherDescription}"></div>
            <div th:text="${day.temperatureMax} + '℃ / ' + ${day.temperatureMin} + '℃'"></div>
        </div>
    </div>
    
    <a href="/">トップページに戻る</a>
</body>
</html>
```

---

## ✅ チェックリスト

- [ ] WeatherControllerを実装した
- [ ] @PathVariableを使用した
- [ ] 例外ハンドリングを実装した
- [ ] MockMvcでテストを作成した
- [ ] すべてのテストがパスした
- [ ] エラーページを作成した
- [ ] weather-detail.htmlを作成した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(controller): WeatherControllerとエラーハンドリングを実装"
git push origin feature/day-23
```

---

## 📚 参考リンク

### Spring MVC
- [@PathVariableの使い方（日本語）](https://qiita.com/NagaokaKenichi/items/7d1285e70b6a9c9e5b9d)
- [例外ハンドリング（日本語）](https://qiita.com/tag1216/items/3680b92cf96eb5a170f0)
- [エラーページのカスタマイズ（日本語）](https://qiita.com/NagaokaKenichi/items/5d8bc0ae5d36889b8972)

### テスト
- [Controller層のテスト（日本語）](https://qiita.com/disc99/items/31fa7abb724f63602dc9)
- [MockMvc詳解（日本語）](https://qiita.com/rubytomato@github/items/f5c5c3e5c8c8d6c4e9c3)

---

## 🆘 トラブルシューティング

### PathVariableが受け取れない
**症状:** `id` がnullになる

**原因:** パス定義が間違っている

**解決策:**
```java
@GetMapping("/{id}")  // ← {id} の形式で指定
public String show(@PathVariable Long id) { ... }
```

### 例外が捕捉されない
**症状:** try-catchで例外が捕捉されない

**原因:** 例外の型が一致していない

**解決策:**
```java
catch (ResourceNotFoundException e) {  // 正確な型を指定
    ...
}
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - WeatherController
   - エラーハンドリング
   - エラーページ

2. **学んだこと:**
   - @PathVariableの使い方
   - try-catchによる例外ハンドリング
   - エラーページの作成

3. **明日への引き継ぎ:**
   - Day 24でGlobalExceptionHandler実装

---

## 🎉 完了後

次は [Day 24](day-24.md) へ

お疲れさまでした！
