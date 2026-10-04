# Day 28: 天気詳細ページ実装（weather-detail.html）

## 📅 実施日
- 予定: Week 6 - Day 28
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
都道府県ごとの天気詳細ページを実装し、現在の天気と7日間の予報を表示する

---

## 📋 午前の作業（9:00-13:00）

### 1. 詳細ページの設計（9:00-9:30）

**表示する内容:**
1. 都道府県情報（名前、地域）
2. 現在の天気
   - 気温、体感温度
   - 天気コード・説明
   - 風速、湿度
   - 降水量、雲量
3. 7日間の天気予報
   - 日付、曜日
   - 最高気温・最低気温
   - 天気
   - 降水量
   - 日の出・日の入り

**レイアウト構成:**

```
+----------------------------------+
|         ヘッダー                  |
|  東京都の天気                     |
|  更新: 2024/01/05 15:30          |
+----------------------------------+
|                                  |
|  【現在の天気】                   |
|  🌤️ 晴れ  15.5℃                |
|  体感 14.2℃ | 湿度 65%           |
|  風速 3.2m/s | 降水 0mm          |
|                                  |
+----------------------------------+
|                                  |
|  【週間天気予報】                 |
|  +------+------+------+-----+    |
|  | 1/5  | 1/6  | 1/7  | ... |    |
|  | 金   | 土   | 日   | ... |    |
|  | 🌤️  | ☀️  | 🌧️  | ... |    |
|  | 18°  | 20°  | 15°  | ... |    |
|  | 10°  | 12°  | 12°  | ... |    |
|  +------+------+------+-----+    |
|                                  |
+----------------------------------+
```

---

### 2. weather-detail.html実装（9:30-12:00）

`src/main/resources/templates/weather-detail.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head(${weather.prefecture.name} + 'の天気')}"></head>
<body>
    <!-- ナビゲーション -->
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <!-- メインコンテンツ -->
    <div class="container">
        <!-- ページヘッダー -->
        <header class="weather-header">
            <div class="header-content">
                <h1 class="prefecture-title">
                    <span th:text="${weather.prefecture.name}"></span>の天気
                </h1>
                <p class="prefecture-info">
                    <span class="badge badge-region" th:text="${weather.prefecture.region}"></span>
                    <span class="update-time">
                        更新: <time th:text="${#temporals.format(weather.fetchedAt, 'yyyy/MM/dd HH:mm')}"></time>
                    </span>
                </p>
            </div>
            
            <!-- パンくずリスト -->
            <nav class="breadcrumb">
                <a th:href="@{/}">トップ</a>
                <span class="separator">›</span>
                <span th:text="${weather.prefecture.name}"></span>
            </nav>
        </header>
        
        <!-- 現在の天気セクション -->
        <section class="current-weather-section">
            <h2 class="section-title">現在の天気</h2>
            
            <div class="current-weather-card">
                <!-- 天気アイコン（後日実装） -->
                <div class="weather-icon">
                    <span class="icon-placeholder" th:text="${weather.current.weatherCode}">1</span>
                </div>
                
                <!-- メイン情報 -->
                <div class="weather-main">
                    <div class="temperature-display">
                        <span class="temperature" th:text="${#numbers.formatDecimal(weather.current.temperature, 1, 1)}">15.5</span>
                        <span class="unit">℃</span>
                    </div>
                    <div class="weather-description" th:text="${weather.current.weatherDescription}">晴れ</div>
                </div>
                
                <!-- 詳細情報 -->
                <div class="weather-details">
                    <div class="detail-item">
                        <span class="detail-icon">🌡️</span>
                        <span class="detail-label">体感温度</span>
                        <span class="detail-value">
                            <span th:text="${#numbers.formatDecimal(weather.current.apparentTemperature, 1, 1)}">14.2</span>℃
                        </span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-icon">💧</span>
                        <span class="detail-label">湿度</span>
                        <span class="detail-value">
                            <span th:text="${weather.current.humidity}">65</span>%
                        </span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-icon">💨</span>
                        <span class="detail-label">風速</span>
                        <span class="detail-value">
                            <span th:text="${#numbers.formatDecimal(weather.current.windSpeed, 1, 1)}">3.2</span>m/s
                        </span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-icon">🌧️</span>
                        <span class="detail-label">降水量</span>
                        <span class="detail-value">
                            <span th:text="${#numbers.formatDecimal(weather.current.precipitation, 1, 1)}">0.0</span>mm
                        </span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-icon">☁️</span>
                        <span class="detail-label">雲量</span>
                        <span class="detail-value">
                            <span th:text="${weather.current.cloudCover}">20</span>%
                        </span>
                    </div>
                    
                    <div class="detail-item">
                        <span class="detail-icon">🕐</span>
                        <span class="detail-label">観測時刻</span>
                        <span class="detail-value">
                            <time th:text="${#temporals.format(weather.current.time, 'HH:mm')}">15:00</time>
                        </span>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- 週間予報セクション -->
        <section class="forecast-section">
            <h2 class="section-title">7日間の天気予報</h2>
            
            <div class="forecast-container">
                <div th:each="day, stat : ${weather.dailyForecasts}" 
                     class="forecast-card"
                     th:classappend="${stat.first} ? 'today' : ''">
                    
                    <!-- 日付 -->
                    <div class="forecast-date">
                        <div class="date-month-day" 
                             th:text="${#temporals.format(day.date, 'M/d')}">1/5</div>
                        <div class="date-day-of-week" 
                             th:text="${day.dayOfWeek}">金</div>
                    </div>
                    
                    <!-- 天気アイコン（後日実装） -->
                    <div class="forecast-weather">
                        <span class="forecast-icon" th:text="${day.weatherCode}">1</span>
                        <div class="forecast-description" 
                             th:text="${day.weatherDescription}">晴れ</div>
                    </div>
                    
                    <!-- 気温 -->
                    <div class="forecast-temperature">
                        <div class="temp-max">
                            <span class="temp-value" 
                                  th:text="${#numbers.formatDecimal(day.temperatureMax, 1, 0)}">18</span>°
                        </div>
                        <div class="temp-min">
                            <span class="temp-value" 
                                  th:text="${#numbers.formatDecimal(day.temperatureMin, 1, 0)}">10</span>°
                        </div>
                    </div>
                    
                    <!-- 降水量 -->
                    <div class="forecast-precipitation" th:if="${day.precipitationSum > 0}">
                        <span class="precip-icon">🌧️</span>
                        <span th:text="${#numbers.formatDecimal(day.precipitationSum, 1, 1)}">5.2</span>mm
                    </div>
                    
                    <!-- 日の出・日の入り -->
                    <div class="forecast-sun-times">
                        <div class="sun-time">
                            <span class="sun-icon">🌅</span>
                            <time th:text="${#temporals.format(day.sunrise, 'HH:mm')}">06:30</time>
                        </div>
                        <div class="sun-time">
                            <span class="sun-icon">🌇</span>
                            <time th:text="${#temporals.format(day.sunset, 'HH:mm')}">17:30</time>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- アクションボタン -->
        <div class="action-buttons">
            <a th:href="@{/}" class="btn btn-secondary">トップページに戻る</a>
            <button onclick="window.location.reload()" class="btn btn-primary">最新情報に更新</button>
        </div>
    </div>
    
    <!-- フッター -->
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <style>
        /* ページヘッダー */
        .weather-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .header-content {
            margin-bottom: 15px;
        }
        
        .prefecture-title {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .prefecture-info {
            display: flex;
            gap: 15px;
            align-items: center;
            font-size: 14px;
        }
        
        .badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .badge-region {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .update-time {
            opacity: 0.9;
        }
        
        /* パンくずリスト */
        .breadcrumb {
            display: flex;
            gap: 10px;
            align-items: center;
            font-size: 14px;
        }
        
        .breadcrumb a {
            color: white;
            text-decoration: none;
            opacity: 0.8;
        }
        
        .breadcrumb a:hover {
            opacity: 1;
            text-decoration: underline;
        }
        
        .separator {
            opacity: 0.6;
        }
        
        /* セクションタイトル */
        .section-title {
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }
        
        /* 現在の天気カード */
        .current-weather-section {
            margin-bottom: 40px;
        }
        
        .current-weather-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            display: grid;
            grid-template-columns: auto 1fr;
            grid-template-rows: auto auto;
            gap: 30px;
        }
        
        .weather-icon {
            grid-row: 1 / 3;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .icon-placeholder {
            font-size: 80px;
            width: 120px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #ecf0f1;
            border-radius: 50%;
            color: #3498db;
        }
        
        .weather-main {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .temperature-display {
            display: flex;
            align-items: flex-start;
            gap: 5px;
        }
        
        .temperature {
            font-size: 64px;
            font-weight: bold;
            color: #2c3e50;
            line-height: 1;
        }
        
        .unit {
            font-size: 32px;
            color: #7f8c8d;
            margin-top: 10px;
        }
        
        .weather-description {
            font-size: 24px;
            color: #3498db;
            margin-top: 10px;
        }
        
        /* 詳細情報グリッド */
        .weather-details {
            grid-column: 1 / 3;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }
        
        .detail-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .detail-icon {
            font-size: 24px;
        }
        
        .detail-label {
            font-size: 12px;
            color: #7f8c8d;
        }
        
        .detail-value {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        /* 週間予報 */
        .forecast-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
        }
        
        .forecast-card {
            background: white;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
        }
        
        .forecast-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            border-color: #3498db;
        }
        
        .forecast-card.today {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .forecast-date {
            margin-bottom: 15px;
        }
        
        .date-month-day {
            font-size: 18px;
            font-weight: bold;
        }
        
        .date-day-of-week {
            font-size: 14px;
            opacity: 0.8;
        }
        
        .forecast-weather {
            margin-bottom: 15px;
        }
        
        .forecast-icon {
            font-size: 48px;
            display: block;
            margin-bottom: 5px;
        }
        
        .forecast-description {
            font-size: 14px;
        }
        
        .forecast-temperature {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 18px;
        }
        
        .temp-max {
            color: #e74c3c;
        }
        
        .temp-min {
            color: #3498db;
        }
        
        .forecast-card.today .temp-max,
        .forecast-card.today .temp-min {
            color: white;
        }
        
        .forecast-precipitation {
            font-size: 12px;
            margin-bottom: 10px;
        }
        
        .forecast-sun-times {
            font-size: 11px;
            opacity: 0.8;
        }
        
        .sun-time {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 5px;
            margin: 3px 0;
        }
        
        .sun-icon {
            font-size: 14px;
        }
        
        /* アクションボタン */
        .action-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 40px 0;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2980b9;
        }
        
        .btn-secondary {
            background: #95a5a6;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #7f8c8d;
        }
        
        /* レスポンシブ */
        @media (max-width: 768px) {
            .prefecture-title {
                font-size: 24px;
            }
            
            .current-weather-card {
                grid-template-columns: 1fr;
                grid-template-rows: auto auto auto;
            }
            
            .weather-icon {
                grid-row: 1;
                grid-column: 1;
            }
            
            .weather-details {
                grid-column: 1;
                grid-template-columns: repeat(2, 1fr);
            }
            
            .temperature {
                font-size: 48px;
            }
            
            .forecast-container {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }
    </style>
</body>
</html>
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. WeatherServiceの確認（13:00-13:30）

既存のWeatherServiceで対応済み。念のため確認：

```java
public WeatherDetailDto getWeatherByPrefectureId(Long prefectureId) {
    // 1. 都道府県取得
    Prefecture prefecture = prefectureRepository.findById(prefectureId)
        .orElseThrow(() -> new ResourceNotFoundException("都道府県が見つかりません"));
    
    // 2. API呼び出し
    OpenMeteoResponseDto apiResponse = openMeteoClient.fetchWeather(
        prefecture.getLatitude(), 
        prefecture.getLongitude()
    );
    
    // 3. DB保存
    WeatherRecord record = weatherMapper.toEntity(prefecture, apiResponse);
    weatherRecordRepository.save(record);
    
    // 4. DTO変換
    return weatherMapper.toDetailDto(record);
}
```

---

### 4. 天気コード変換ユーティリティ作成（13:30-15:00）

**天気コード変換:** `src/main/java/com/example/weatherapp/util/WeatherCodeUtil.java`

```java
package com.example.weatherapp.util;

import java.util.Map;

/**
 * 天気コード変換ユーティリティ
 * WMO天気コードを日本語と絵文字に変換
 */
public class WeatherCodeUtil {
    
    private static final Map<Integer, String> WEATHER_DESCRIPTIONS = Map.ofEntries(
        Map.entry(0, "快晴"),
        Map.entry(1, "晴れ"),
        Map.entry(2, "一部曇り"),
        Map.entry(3, "曇り"),
        Map.entry(45, "霧"),
        Map.entry(48, "霧氷"),
        Map.entry(51, "小雨"),
        Map.entry(53, "雨"),
        Map.entry(55, "大雨"),
        Map.entry(61, "小雨"),
        Map.entry(63, "雨"),
        Map.entry(65, "大雨"),
        Map.entry(71, "小雪"),
        Map.entry(73, "雪"),
        Map.entry(75, "大雪"),
        Map.entry(80, "にわか雨"),
        Map.entry(81, "にわか雨"),
        Map.entry(82, "激しいにわか雨"),
        Map.entry(85, "にわか雪"),
        Map.entry(86, "にわか雪"),
        Map.entry(95, "雷雨"),
        Map.entry(96, "雷雨（雹）"),
        Map.entry(99, "激しい雷雨（雹）")
    );
    
    private static final Map<Integer, String> WEATHER_EMOJIS = Map.ofEntries(
        Map.entry(0, "☀️"),
        Map.entry(1, "🌤️"),
        Map.entry(2, "⛅"),
        Map.entry(3, "☁️"),
        Map.entry(45, "🌫️"),
        Map.entry(48, "🌫️"),
        Map.entry(51, "🌦️"),
        Map.entry(53, "🌧️"),
        Map.entry(55, "🌧️"),
        Map.entry(61, "🌦️"),
        Map.entry(63, "🌧️"),
        Map.entry(65, "🌧️"),
        Map.entry(71, "🌨️"),
        Map.entry(73, "❄️"),
        Map.entry(75, "❄️"),
        Map.entry(80, "🌦️"),
        Map.entry(81, "🌦️"),
        Map.entry(82, "⛈️"),
        Map.entry(85, "🌨️"),
        Map.entry(86, "🌨️"),
        Map.entry(95, "⛈️"),
        Map.entry(96, "⛈️"),
        Map.entry(99, "⛈️")
    );
    
    public static String getDescription(Integer weatherCode) {
        return WEATHER_DESCRIPTIONS.getOrDefault(weatherCode, "不明");
    }
    
    public static String getEmoji(Integer weatherCode) {
        return WEATHER_EMOJIS.getOrDefault(weatherCode, "❓");
    }
}
```

**Mapperで使用:**

```java
// WeatherMapperImpl内
import com.example.weatherapp.util.WeatherCodeUtil;

@Override
public CurrentWeatherDto toCurrentWeatherDto(WeatherRecord record) {
    return CurrentWeatherDto.builder()
        .time(record.getCurrentTime())
        .temperature(record.getCurrentTemperature())
        .weatherCode(record.getCurrentWeatherCode())
        .weatherDescription(WeatherCodeUtil.getDescription(record.getCurrentWeatherCode()))
        // ... 他のフィールド
        .build();
}
```

---

### 5. 動作確認とテスト（15:00-17:00）

**ブラウザで確認:**

1. http://localhost:8080/ にアクセス
2. 東京都をクリック
3. http://localhost:8080/weather/13 に遷移
4. 現在の天気が表示される
5. 7日間の予報が表示される
6. レスポンシブ確認（モバイル表示）

**テスト作成:**

`src/test/java/com/example/weatherapp/controller/WeatherDetailPageTest.java`:

```java
package com.example.weatherapp.controller;

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
 * 天気詳細ページのE2Eテスト
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@Sql("/test-data.sql")
class WeatherDetailPageTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("天気詳細ページが表示される")
    void testWeatherDetailPage() throws Exception {
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isOk())
            .andExpect(view().name("weather-detail"))
            .andExpect(content().string(containsString("東京都の天気")))
            .andExpect(content().string(containsString("現在の天気")))
            .andExpect(content().string(containsString("7日間の天気予報")));
    }
    
    @Test
    @DisplayName("現在の天気情報が表示される")
    void testCurrentWeatherDisplay() throws Exception {
        mockMvc.perform(get("/weather/13"))
            .andExpect(content().string(containsString("体感温度")))
            .andExpect(content().string(containsString("湿度")))
            .andExpect(content().string(containsString("風速")));
    }
}
```

---

## ✅ チェックリスト

- [ ] weather-detail.htmlを実装した
- [ ] 現在の天気が表示される
- [ ] 7日間の予報が表示される
- [ ] WeatherCodeUtilを実装した
- [ ] レスポンシブデザイン対応
- [ ] ブラウザで動作確認した
- [ ] E2Eテストを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): 天気詳細ページ実装"
git push origin main
```

---

## 📚 参考リンク

### CSS Grid & Flexbox
- [CSS Grid完全ガイド](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexboxガイド](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

### レスポンシブデザイン
- [メディアクエリ（日本語）](https://developer.mozilla.org/ja/docs/Web/CSS/Media_Queries/Using_media_queries)

### 天気コード
- [WMO Weather Code](https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM)

---

## 🆘 トラブルシューティング

### 天気データが表示されない
**症状:** "データがありません"と表示される

**原因:** API呼び出しが失敗している

**解決策:**
- ログを確認
- Open-Meteo APIが稼働しているか確認
- 座標（緯度・経度）が正しいか確認

### レイアウトが崩れる
**症状:** モバイルで表示が崩れる

**原因:** viewportタグがない

**解決策:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - 天気詳細ページ
   - 現在の天気表示
   - 7日間の予報表示
   - WeatherCodeUtil

2. **学んだこと:**
   - 複雑なグリッドレイアウト
   - レスポンシブデザイン
   - ユーティリティクラスの作成

3. **明日への引き継ぎ:**
   - Day 29でCSS改善・スタイリング

---

## 🎉 完了後

次は [Day 29](day-29.md) へ

お疲れさまでした！
