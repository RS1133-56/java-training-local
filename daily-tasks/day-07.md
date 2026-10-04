# Day 7: API調査の詳細と動作確認

## 📅 実施日
- 予定: Week 2 - Day 7
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Open-Meteo APIのレスポンスを詳細に解析し、実装に必要な情報を整理する

---

## 📋 午前の作業（9:00-13:00）

### 1. APIレスポンスの詳細解析（9:00-10:30）

**手順:**

PostmanでAPIを実行し、レスポンスを詳しく見る

**東京の現在+週間天気を取得:**
```
GET https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m,apparent_temperature,precipitation,cloudcover&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max,sunrise,sunset&timezone=Asia/Tokyo&forecast_days=7
```

**レスポンス例:**
```json
{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "generationtime_ms": 0.234,
  "utc_offset_seconds": 32400,
  "timezone": "Asia/Tokyo",
  "timezone_abbreviation": "JST",
  "elevation": 40.0,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C",
    "weathercode": "wmo code",
    "windspeed_10m": "m/s",
    "relativehumidity_2m": "%",
    "apparent_temperature": "°C",
    "precipitation": "mm",
    "cloudcover": "%"
  },
  "current": {
    "time": "2024-01-04T15:00",
    "interval": 900,
    "temperature_2m": 12.5,
    "weathercode": 1,
    "windspeed_10m": 3.2,
    "relativehumidity_2m": 65,
    "apparent_temperature": 10.8,
    "precipitation": 0.0,
    "cloudcover": 25
  },
  "daily_units": {
    "time": "iso8601",
    "temperature_2m_max": "°C",
    "temperature_2m_min": "°C",
    "weathercode": "wmo code",
    "precipitation_sum": "mm",
    "windspeed_10m_max": "m/s",
    "sunrise": "iso8601",
    "sunset": "iso8601"
  },
  "daily": {
    "time": [
      "2024-01-04",
      "2024-01-05",
      "2024-01-06",
      "2024-01-07",
      "2024-01-08",
      "2024-01-09",
      "2024-01-10"
    ],
    "temperature_2m_max": [15.2, 14.8, 13.5, 16.1, 14.9, 15.3, 14.6],
    "temperature_2m_min": [8.1, 7.5, 6.9, 8.3, 7.8, 8.0, 7.6],
    "weathercode": [1, 3, 61, 2, 1, 2, 3],
    "precipitation_sum": [0.0, 0.0, 5.2, 0.1, 0.0, 0.0, 0.3],
    "windspeed_10m_max": [4.5, 5.2, 8.1, 3.9, 4.2, 4.8, 5.0],
    "sunrise": [
      "2024-01-04T06:51",
      "2024-01-05T06:51",
      "2024-01-06T06:51",
      "2024-01-07T06:52",
      "2024-01-08T06:52",
      "2024-01-09T06:52",
      "2024-01-10T06:52"
    ],
    "sunset": [
      "2024-01-04T16:46",
      "2024-01-05T16:47",
      "2024-01-06T16:48",
      "2024-01-07T16:49",
      "2024-01-08T16:50",
      "2024-01-09T16:51",
      "2024-01-10T16:52"
    ]
  }
}
```

**`api-response-analysis.md`を作成:**

```markdown
# API レスポンス解析

## レスポンス構造

### 1. メタ情報
```json
{
  "latitude": 35.6895,        // リクエストした緯度
  "longitude": 139.6917,      // リクエストした経度
  "generationtime_ms": 0.234, // API処理時間
  "timezone": "Asia/Tokyo",   // タイムゾーン
  "elevation": 40.0           // 標高
}
```

### 2. current（現在の天気）

#### 単位情報
```json
"current_units": {
  "temperature_2m": "°C",
  "weathercode": "wmo code",
  "windspeed_10m": "m/s",
  "relativehumidity_2m": "%"
}
```

#### 実際のデータ
```json
"current": {
  "time": "2024-01-04T15:00",
  "temperature_2m": 12.5,
  "weathercode": 1,
  "windspeed_10m": 3.2,
  "relativehumidity_2m": 65,
  "apparent_temperature": 10.8,
  "precipitation": 0.0,
  "cloudcover": 25
}
```

**Javaでのマッピング:**
```java
public class CurrentWeather {
    private String time;              // LocalDateTime に変換
    private Double temperature2m;     // 気温
    private Integer weathercode;      // 天気コード
    private Double windspeed10m;      // 風速
    private Integer relativehumidity2m; // 湿度
    private Double apparentTemperature; // 体感温度
    private Double precipitation;     // 降水量
    private Integer cloudcover;       // 雲量
}
```

### 3. daily（日次予報）

#### データ構造の特徴
- 各項目が配列形式
- インデックスで対応（time[0]とtemperature_2m_max[0]は同じ日）

```json
"daily": {
  "time": ["2024-01-04", "2024-01-05", ...],
  "temperature_2m_max": [15.2, 14.8, ...],
  "temperature_2m_min": [8.1, 7.5, ...],
  "weathercode": [1, 3, ...]
}
```

**Javaでのマッピング:**
```java
public class DailyForecast {
    private String date;              // time配列から
    private Double temperatureMax;    // temperature_2m_max配列から
    private Double temperatureMin;    // temperature_2m_min配列から
    private Integer weathercode;      // weathercode配列から
    private Double precipitationSum;  // precipitation_sum配列から
    private String sunrise;           // sunrise配列から
    private String sunset;            // sunset配列から
}
```

## 天気コードの詳細

### 晴れ系（0-3）
- 0: 快晴（Clear sky）
- 1: ほぼ晴れ（Mainly clear）
- 2: 一部曇り（Partly cloudy）
- 3: 曇り（Overcast）

### 霧（45-48）
- 45: 霧（Fog）
- 48: 霧氷（Depositing rime fog）

### 霧雨（51-55）
- 51: 軽い霧雨（Light drizzle）
- 53: 霧雨（Moderate drizzle）
- 55: 激しい霧雨（Dense drizzle）

### 雨（61-67）
- 61: 小雨（Slight rain）
- 63: 雨（Moderate rain）
- 65: 大雨（Heavy rain）
- 66: 凍雨（Light freezing rain）
- 67: 凍雨（Heavy freezing rain）

### 雪（71-77）
- 71: 小雪（Slight snow fall）
- 73: 雪（Moderate snow fall）
- 75: 大雪（Heavy snow fall）
- 77: 雪粒（Snow grains）

### にわか雨・雪（80-86）
- 80: にわか雨（Slight rain showers）
- 81: にわか雨（Moderate rain showers）
- 82: 激しいにわか雨（Violent rain showers）
- 85: にわか雪（Slight snow showers）
- 86: にわか雪（Heavy snow showers）

### 雷雨（95-99）
- 95: 雷雨（Thunderstorm）
- 96: 雷雨と雹（Thunderstorm with slight hail）
- 99: 雷雨と大粒の雹（Thunderstorm with heavy hail）

## 実装時の注意点

### 1. 日時のパース
- `current.time`: ISO 8601形式（例: "2024-01-04T15:00"）
- Javaの`LocalDateTime.parse()`でパース可能

### 2. 配列の処理
- daily配列は全て同じ長さ
- ループ処理でDailyForecastオブジェクトのリストを作成

### 3. null値の可能性
- 一部のデータは null の可能性あり
- Javaでは`Double`や`Integer`（プリミティブ型ではなくラッパー型）を使用

### 4. 単位の扱い
- 気温: ℃
- 風速: m/s
- 湿度: %
- 降水量: mm
```

**成果物:**
- `api-response-analysis.md`

---

### 2. DTOクラスの設計（10:30-12:00）

**手順:**

APIレスポンスをJavaオブジェクトにマッピングするDTOを設計

> 📝 **この設計書は「考え方の整理」です。** 実装（Day 20）では、Day 18で作る画面用DTOと名前がぶつからないよう、
> API受信用のDTOは `OpenMeteoResponseDto` の内部クラス（`Current` / `Daily`）としてまとめて作ります。
> ここでは、「APIのレスポンスをどんな形のJavaオブジェクトで受け取るか」を考えるのが目的です。

`dto-design.md`を作成：

```markdown
# DTO設計書

## 1. OpenMeteoResponseDto

APIレスポンス全体を表すDTO

```java
public class OpenMeteoResponseDto {
    private Double latitude;
    private Double longitude;
    private String timezone;
    private Double elevation;
    private CurrentWeatherDto current;
    private DailyWeatherDto daily;
}
```

## 2. CurrentWeatherDto

現在の天気情報

```java
public class CurrentWeatherDto {
    private String time;
    private Double temperature2m;
    private Integer weathercode;
    private Double windspeed10m;
    private Integer relativehumidity2m;
    private Double apparentTemperature;
    private Double precipitation;
    private Integer cloudcover;
}
```

## 3. DailyWeatherDto

日次予報（配列形式）

```java
public class DailyWeatherDto {
    private List<String> time;
    private List<Double> temperature2mMax;
    private List<Double> temperature2mMin;
    private List<Integer> weathercode;
    private List<Double> precipitationSum;
    private List<Double> windspeed10mMax;
    private List<String> sunrise;
    private List<String> sunset;
}
```

## 4. DailyForecastDto

1日分の予報（処理後）

```java
public class DailyForecastDto {
    private String date;
    private Double temperatureMax;
    private Double temperatureMin;
    private Integer weathercode;
    private Double precipitationSum;
    private Double windspeedMax;
    private String sunrise;
    private String sunset;
    
    // 天気コードから天気の説明を取得
    public String getWeatherDescription() {
        return WeatherCodeMapper.getDescription(weathercode);
    }
    
    // 天気コードからアイコンを取得
    public String getWeatherIcon() {
        return WeatherCodeMapper.getIcon(weathercode);
    }
}
```

## 5. WeatherDetailDto

画面表示用の統合DTO

```java
public class WeatherDetailDto {
    // 都道府県情報
    private Long prefectureId;
    private String prefectureName;
    
    // 現在の天気
    private CurrentWeatherDto currentWeather;
    
    // 週間予報
    private List<DailyForecastDto> dailyForecasts;
    
    // 取得日時
    private LocalDateTime fetchedAt;
}
```

## 6. WeatherCodeMapper

天気コードのマッピング

```java
public class WeatherCodeMapper {
    
    private static final Map<Integer, String> DESCRIPTIONS = new HashMap<>();
    private static final Map<Integer, String> ICONS = new HashMap<>();
    
    static {
        // 晴れ系
        DESCRIPTIONS.put(0, "快晴");
        DESCRIPTIONS.put(1, "晴れ");
        DESCRIPTIONS.put(2, "一部曇り");
        DESCRIPTIONS.put(3, "曇り");
        
        ICONS.put(0, "☀️");
        ICONS.put(1, "🌤️");
        ICONS.put(2, "⛅");
        ICONS.put(3, "☁️");
        
        // 雨系
        DESCRIPTIONS.put(61, "小雨");
        DESCRIPTIONS.put(63, "雨");
        DESCRIPTIONS.put(65, "大雨");
        
        ICONS.put(61, "🌧️");
        ICONS.put(63, "🌧️");
        ICONS.put(65, "🌧️");
        
        // 雪系
        DESCRIPTIONS.put(71, "小雪");
        DESCRIPTIONS.put(73, "雪");
        DESCRIPTIONS.put(75, "大雪");
        
        ICONS.put(71, "🌨️");
        ICONS.put(73, "❄️");
        ICONS.put(75, "❄️");
        
        // 雷雨
        DESCRIPTIONS.put(95, "雷雨");
        ICONS.put(95, "⛈️");
        
        // ... 他の天気コードも追加
    }
    
    public static String getDescription(Integer code) {
        return DESCRIPTIONS.getOrDefault(code, "不明");
    }
    
    public static String getIcon(Integer code) {
        return ICONS.getOrDefault(code, "❓");
    }
}
```

## JSON↔DTOのマッピング例

### Jackson使用時
```java
ObjectMapper mapper = new ObjectMapper();
OpenMeteoResponseDto response = mapper.readValue(jsonString, OpenMeteoResponseDto.class);
```

### フィールド名のマッピング
```java
@JsonProperty("temperature_2m")
private Double temperature2m;

@JsonProperty("weathercode")
private Integer weathercode;
```
```

**成果物:**
- `dto-design.md`

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. 様々なシナリオでのAPIテスト（13:00-15:00）

**テストシナリオ:**

**1. 北海道（寒冷地）**
```
latitude=43.064&longitude=141.347
```
期待: 気温が低い、雪の可能性

**2. 沖縄（温暖地）**
```
latitude=26.212&longitude=127.681
```
期待: 気温が高い

**3. 山間部（長野）**
```
latitude=36.651&longitude=138.181
```
期待: 気温差が大きい

**4. 複数の都道府県を連続取得**
- 東京 → 大阪 → 福岡 を順番に取得
- レスポンスタイムを計測

**5. エラーケース**
```
latitude=200&longitude=139.6917  // 無効な緯度
latitude=35.6895&longitude=200   // 無効な経度
（パラメータなし）                // 必須パラメータ欠落
```

`api-test-scenarios.md`を作成：

```markdown
# APIテストシナリオと結果

## テスト実施日
2024-01-XX

## シナリオ1: 北海道（寒冷地）

### リクエスト
```
GET https://api.open-meteo.com/v1/forecast?latitude=43.064&longitude=141.347&current=temperature_2m,weathercode&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Tokyo&forecast_days=7
```

### 結果
- Status: 200 OK
- Response Time: 234ms
- 現在気温: -2.3℃
- 天気コード: 71（小雪）
- 週間最高気温: 1.2℃ ~ 3.5℃
- 週間最低気温: -5.1℃ ~ -2.8℃

### 学び
- 寒冷地では天気コード71-77（雪系）が多い
- マイナス気温も正しく取得できる

---

## シナリオ2: 沖縄（温暖地）

### リクエスト
```
GET https://api.open-meteo.com/v1/forecast?latitude=26.212&longitude=127.681&current=temperature_2m,weathercode&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Asia/Tokyo&forecast_days=7
```

### 結果
- Status: 200 OK
- Response Time: 198ms
- 現在気温: 18.5℃
- 天気コード: 2（一部曇り）
- 週間最高気温: 20.1℃ ~ 22.3℃
- 週間最低気温: 15.2℃ ~ 17.8℃

### 学び
- 温暖地では気温が高い
- 雪のコードは出現しない

---

## シナリオ3: 連続取得パフォーマンステスト

### テスト内容
東京 → 大阪 → 福岡 を連続で3回取得（計9リクエスト）

### 結果
| 都道府県 | 試行1 | 試行2 | 試行3 | 平均 |
|---------|------|------|------|------|
| 東京 | 245ms | 198ms | 210ms | 217ms |
| 大阪 | 234ms | 205ms | 198ms | 212ms |
| 福岡 | 256ms | 201ms | 215ms | 224ms |

### 学び
- 平均レスポンスタイム: 約220ms
- 安定したパフォーマンス
- レート制限には引っかからなかった

---

## シナリオ4: エラーケース

### 4-1. 無効な緯度
```
GET .../forecast?latitude=200&longitude=139.6917
```
- Status: 400 Bad Request
- Error Message: "Latitude must be in range of -90 to 90°. Given: 200."

### 4-2. 無効な経度
```
GET .../forecast?latitude=35.6895&longitude=200
```
- Status: 400 Bad Request
- Error Message: "Longitude must be in range of -180 to 180°. Given: 200."

### 4-3. パラメータなし
```
GET .../forecast
```
- Status: 400 Bad Request
- Error Message: "Required parameter latitude is missing."

### 学び
- エラーメッセージが明確
- 400エラーで適切に返却される
- Javaでの例外ハンドリングが必要

---

## 結論

### APIの信頼性
✅ 高速（200-250ms）
✅ 安定している
✅ エラーハンドリングが適切

### 実装時の考慮事項
1. タイムアウト設定: 5秒
2. リトライ: 3回まで
3. エラーハンドリング: 400/500エラーの処理
4. ローディング表示: 必須
```

**成果物:**
- `api-test-scenarios.md`
- Postmanのテスト結果スクリーンショット

---

### 4. RestTemplateの設定方針（15:00-16:30）

**学習内容:**

JavaでHTTP APIを呼び出す方法を学ぶ

`rest-template-design.md`を作成：

```markdown
# RestTemplate 設定方針

## RestTemplateとは

Spring Frameworkが提供するHTTPクライアント
- RESTful APIの呼び出し
- JSON↔Javaオブジェクトの変換
- エラーハンドリング

## 設定クラスの作成

### RestTemplateConfig.java
```java
@Configuration
public class RestTemplateConfig {
    
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
            .connectTimeout(Duration.ofSeconds(5))  // 接続タイムアウト
            .readTimeout(Duration.ofSeconds(5))     // 読み取りタイムアウト
            .build();
    }
}
```

## OpenMeteoClientの設計

### 責務
- Open-Meteo APIとの通信
- レスポンスのDTOへの変換
- エラーハンドリング

### 実装イメージ
```java
@Component
@Slf4j
public class OpenMeteoClient {
    
    private static final String API_BASE_URL = "https://api.open-meteo.com/v1/forecast";
    
    private final RestTemplate restTemplate;
    
    public OpenMeteoClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    public OpenMeteoResponseDto fetchWeather(Double latitude, Double longitude) {
        String url = buildUrl(latitude, longitude);
        
        log.info("Fetching weather from Open-Meteo API: lat={}, lon={}", latitude, longitude);
        
        try {
            OpenMeteoResponseDto response = restTemplate.getForObject(url, OpenMeteoResponseDto.class);
            log.info("Successfully fetched weather data");
            return response;
            
        } catch (HttpClientErrorException e) {
            log.error("Client error when calling API: {}", e.getMessage());
            throw new ExternalApiException("Failed to fetch weather data", e);
            
        } catch (HttpServerErrorException e) {
            log.error("Server error when calling API: {}", e.getMessage());
            throw new ExternalApiException("Weather API server error", e);
            
        } catch (Exception e) {
            log.error("Unexpected error when calling API: {}", e.getMessage());
            throw new ExternalApiException("Unexpected error", e);
        }
    }
    
    private String buildUrl(Double latitude, Double longitude) {
        return UriComponentsBuilder.fromUriString(API_BASE_URL)
            .queryParam("latitude", latitude)
            .queryParam("longitude", longitude)
            .queryParam("current", "temperature_2m,weathercode,windspeed_10m,relativehumidity_2m")
            .queryParam("daily", "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum")
            .queryParam("timezone", "Asia/Tokyo")
            .queryParam("forecast_days", 7)
            .toUriString();
    }
}
```

## エラーハンドリング

### カスタム例外
```java
public class ExternalApiException extends RuntimeException {
    public ExternalApiException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### GlobalExceptionHandlerでの処理
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ExternalApiException.class)
    public String handleExternalApiException(ExternalApiException e, Model model) {
        model.addAttribute("error", "天気情報の取得に失敗しました");
        return "error/api-error";
    }
}
```

## テスト方針

### ユニットテスト
- MockRestTemplateを使用
- 正常系・異常系のテスト

```java
@ExtendWith(MockitoExtension.class)
class OpenMeteoClientTest {
    
    @Mock
    private RestTemplate restTemplate;
    
    @InjectMocks
    private OpenMeteoClient openMeteoClient;
    
    @Test
    void fetchWeather_Success() {
        // Given
        OpenMeteoResponseDto mockResponse = new OpenMeteoResponseDto();
        when(restTemplate.getForObject(anyString(), eq(OpenMeteoResponseDto.class)))
            .thenReturn(mockResponse);
        
        // When
        OpenMeteoResponseDto result = openMeteoClient.fetchWeather(35.6895, 139.6917);
        
        // Then
        assertNotNull(result);
    }
    
    @Test
    void fetchWeather_ThrowsException() {
        // Given
        when(restTemplate.getForObject(anyString(), eq(OpenMeteoResponseDto.class)))
            .thenThrow(new HttpClientErrorException(HttpStatus.BAD_REQUEST));
        
        // When & Then
        assertThrows(ExternalApiException.class, () -> {
            openMeteoClient.fetchWeather(200.0, 139.6917);
        });
    }
}
```
```

**成果物:**
- `rest-template-design.md`

---

### 5. 明日以降の準備とまとめ（16:30-17:00）

**手順:**

1. これまでの成果物を整理

2. `day-07-summary.md`を作成：

```markdown
# Day 7 学習まとめ

## 本日の成果

### 1. APIレスポンスの詳細理解
- current（現在天気）の構造
- daily（日次予報）の配列構造
- 天気コードの完全なマッピング

### 2. DTO設計完了
- OpenMeteoResponseDto
- CurrentWeatherDto
- DailyWeatherDto
- DailyForecastDto
- WeatherDetailDto
- WeatherCodeMapper

### 3. APIテスト
- 様々な地域でのテスト
- パフォーマンステスト
- エラーケーステスト

### 4. 実装方針の確立
- RestTemplateの設定
- OpenMeteoClientの設計
- エラーハンドリング

## 技術的な学び

### APIレスポンスの特徴
- 配列形式のデータ処理が必要
- 天気コードと表示の変換が必要
- タイムゾーン処理が重要

### Javaでの実装ポイント
- DTO設計の重要性
- Jackson でのJSONマッピング
- RestTemplate によるHTTP通信
- エラーハンドリング

## 明日への準備

### Day 8: 画面設計
- ワイヤーフレームツールの準備（Figma, draw.io等）
- UI/UXの参考サイト調査
- 天気アプリの画面構成を考える
```

3. Gitコミット
```bash
git add .
git commit -m "docs: APIレスポンス解析とDTO設計を完了"
git push origin main
```

**成果物:**
- `day-07-summary.md`
- GitHubへのpush

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] APIレスポンスの詳細解析が完了した
- [ ] DTO設計が完了した
- [ ] 様々なシナリオでAPIテストを実施した
- [ ] RestTemplateの設定方針が決まった
- [ ] すべてのドキュメントが作成された
- [ ] GitHubにコミット・プッシュした

---

## 📚 参考リンク

- [Spring RestTemplate公式ドキュメント](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html)
- [Jackson公式ドキュメント](https://github.com/FasterXML/jackson-docs)
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)

---

## 🆘 トラブルシューティング

### JSONの項目名（`temperature_2m`）とJavaのフィールド名（`temperature2m`）が合わず、値が `null` になる
**原因:** JSONはsnake_case、JavaはcamelCaseで、自動では対応づかない

**解決策:**
1. DTOのフィールドに `@JsonProperty("temperature_2m")` を付けて、JSON側の名前を明示する
2. 項目名の綴り（`windspeed_10m` など）をレスポンスの実物と1文字ずつ比較する

### `UnrecognizedPropertyException: Unrecognized field ...`
**原因:** JSONにあるのにDTOに存在しない項目があり、変換でエラーになっている

**解決策:**
1. DTOクラスに `@JsonIgnoreProperties(ignoreUnknown = true)` を付ける
2. 必要な項目だけDTOに定義すればよい（全項目を網羅しなくてよい）

### `Cannot deserialize value of type ...` で変換できない
**原因:** DTOの型がJSONの型と合っていない（配列なのに単一値で受けている、など）

**解決策:**
1. `daily.time` のような配列は `List<String>`、`List<Double>` で受ける
2. 数値は `Double` / `Integer`、日時文字列は一旦 `String` で受けてから変換する
3. レスポンスのJSONを見て、`[ ]`（配列）か `{ }`（オブジェクト）かを確認

### 天気コードが想定外の値で、説明が引けない
**原因:** 定義していないコードが返ってきた

**解決策:**
1. WMO天気コード表（このDayの表）を再確認
2. 表にないコードは「不明」を返すデフォルト処理を用意しておく

---

## 🎉 完了後

次は [Day 8](day-08.md) へ進む

お疲れさまでした！
