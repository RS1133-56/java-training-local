# Day 20: 外部API連携（OpenMeteoClient）

## 📅 実施日
- 予定: Week 4 - Day 20
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
RestTemplateを使ってOpen-Meteo APIと連携するClientクラスを実装する

> 📝 **このDayの位置づけ（Day 21への準備）**
> 次のDay 21で作る `WeatherServiceImpl` は、このDayで作る `OpenMeteoClient` を呼び出します。
> 先にClientを完成させておくことで、Day 21でServiceを実装したときにすぐ動作確認・テストができます。

---

## 📋 午前の作業（9:00-13:00）

### 1. RestTemplateの基礎理解（9:00-10:00）

**RestTemplateとは:**
- SpringのHTTPクライアント
- 外部APIを簡単に呼び出せる
- 同期的な通信（レスポンスを待つ）

**基本的な使い方:**

```java
RestTemplate restTemplate = new RestTemplate();

// GETリクエスト
String result = restTemplate.getForObject(
    "https://api.example.com/data", 
    String.class
);

// POSTリクエスト
MyResponse response = restTemplate.postForObject(
    "https://api.example.com/create",
    requestBody,
    MyResponse.class
);
```

---

### 2. RestTemplateの設定（10:00-11:00）

**設定クラス作成:** `src/main/java/com/example/weatherapp/config/RestTemplateConfig.java`

```java
package com.example.weatherapp.config;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.BufferingClientHttpRequestFactory;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
public class RestTemplateConfig {
    
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
            .connectTimeout(Duration.ofSeconds(5))
            .readTimeout(Duration.ofSeconds(10))
            .requestFactory(() -> new BufferingClientHttpRequestFactory(
                new SimpleClientHttpRequestFactory()
            ))
            .build();
    }
}
```

**ポイント:**
- **connectTimeout**: 接続確立の制限時間（5秒）
- **readTimeout**: レスポンス待機の制限時間（10秒）
- **BufferingClientHttpRequestFactory**: レスポンスの複数回読み取りを可能に

---

### 3. OpenMeteoClient実装（11:00-12:00）

**Clientクラス作成:** `src/main/java/com/example/weatherapp/client/OpenMeteoClient.java`

```java
package com.example.weatherapp.client;

import com.example.weatherapp.dto.api.OpenMeteoResponseDto;
import com.example.weatherapp.exception.ExternalApiException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

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
        
        log.info("Open-Meteo API呼び出し: lat={}, lon={}", latitude, longitude);
        log.debug("URL: {}", url);
        
        try {
            OpenMeteoResponseDto response = restTemplate.getForObject(
                url, 
                OpenMeteoResponseDto.class
            );
            
            if (response == null) {
                throw new ExternalApiException("APIレスポンスがnullです");
            }
            
            log.info("API呼び出し成功");
            return response;
            
        } catch (ResourceAccessException e) {
            log.error("APIタイムアウト: {}", e.getMessage());
            throw new ExternalApiException("天気APIへの接続がタイムアウトしました", e);
            
        } catch (HttpClientErrorException e) {
            log.error("APIクライアントエラー: status={}", e.getStatusCode());
            throw new ExternalApiException("天気APIエラー: " + e.getStatusCode(), e);
            
        } catch (HttpServerErrorException e) {
            log.error("APIサーバーエラー: status={}", e.getStatusCode());
            throw new ExternalApiException("天気APIサーバーエラー", e);
            
        } catch (Exception e) {
            log.error("API呼び出し失敗", e);
            throw new ExternalApiException("天気情報の取得に失敗しました", e);
        }
    }
    
    private String buildUrl(Double latitude, Double longitude) {
        return UriComponentsBuilder.fromUriString(API_BASE_URL)
            .queryParam("latitude", latitude)
            .queryParam("longitude", longitude)
            .queryParam("current", 
                "temperature_2m,weathercode,windspeed_10m,relativehumidity_2m," +
                "apparent_temperature,precipitation,cloud_cover"
            )
            .queryParam("daily",
                "temperature_2m_max,temperature_2m_min,weathercode," +
                "precipitation_sum,windspeed_10m_max,sunrise,sunset"
            )
            .queryParam("timezone", "UTC")
            .queryParam("forecast_days", 7)
            .toUriString();
    }
}
```

---

## 午後の作業（13:00-17:00）

### 4. テスト作成（13:00-16:00）

`src/test/java/com/example/weatherapp/client/OpenMeteoClientTest.java`:

```java
package com.example.weatherapp.client;

import com.example.weatherapp.dto.api.OpenMeteoResponseDto;
import com.example.weatherapp.exception.ExternalApiException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

import static org.assertj.core.api.Assertions.*;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.*;
import static org.springframework.test.web.client.response.MockRestResponseCreators.*;

class OpenMeteoClientTest {
    
    private OpenMeteoClient openMeteoClient;
    private MockRestServiceServer mockServer;
    
    @BeforeEach
    void setUp() {
        RestTemplate restTemplate = new RestTemplate();
        openMeteoClient = new OpenMeteoClient(restTemplate);
        mockServer = MockRestServiceServer.createServer(restTemplate);
    }
    
    @Test
    @DisplayName("API呼び出しが成功する")
    void testFetchWeather_Success() {
        String jsonResponse = "{\"latitude\":35.689,\"longitude\":139.692}";
        
        mockServer.expect(requestTo(containsString("api.open-meteo.com")))
            .andExpect(method(HttpMethod.GET))
            .andExpect(queryParam("latitude", "35.689"))
            .andExpect(queryParam("longitude", "139.692"))
            .andRespond(withSuccess(jsonResponse, MediaType.APPLICATION_JSON));
        
        OpenMeteoResponseDto result = openMeteoClient.fetchWeather(35.689, 139.692);
        
        assertThat(result).isNotNull();
        mockServer.verify();
    }
    
    @Test
    @DisplayName("タイムアウトエラー")
    void testFetchWeather_Timeout() {
        mockServer.expect(requestTo(containsString("api.open-meteo.com")))
            .andRespond(withServerError());
        
        assertThatThrownBy(() -> openMeteoClient.fetchWeather(35.689, 139.692))
            .isInstanceOf(ExternalApiException.class);
        
        mockServer.verify();
    }
}
```

---

## ✅ チェックリスト

- [ ] RestTemplateConfig作成
- [ ] OpenMeteoClient実装
- [ ] ExternalApiException作成
- [ ] テスト作成・実行
- [ ] GitHubプッシュ

**Gitコミット:**
```bash
git add .
git commit -m "feat(client): OpenMeteoClient実装"
git push origin main
```

---

## 📚 参考リンク

- [RestTemplate公式ドキュメント](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html)
- [RestTemplate使い方（日本語）](https://qiita.com/tag1216/items/437232338c0f7c4fcd57)
- [MockRestServiceServer（日本語）](https://qiita.com/rubytomato@github/items/5f0f7e70a0b63380f7db)
- [Open-Meteo API](https://open-meteo.com/en/docs)

---

## 🆘 トラブルシューティング

### `ResourceAccessException: I/O error ... Connect timed out`
**原因:** APIに接続できない（ネットワーク・プロキシ・タイムアウト）

**解決策:**
1. ブラウザやPostmanで同じURLが開けるか確認（開けない場合はネットワークの問題）
2. 社内ネットワークのプロキシ設定を確認
3. タイムアウト値（接続5秒・読み取り10秒）が短すぎないか確認

### `UnknownHostException: api.open-meteo.com`
**原因:** ホスト名の綴りの誤り、またはインターネットに接続できていない

**解決策:**
1. `API_BASE_URL` の定数を、公式ドキュメントのURLと1文字ずつ比較
2. PCがインターネットに接続されているか確認

### `HttpClientErrorException: 400 Bad Request`
**原因:** リクエストのパラメータが不正

**解決策:**
1. ログに出したURLをPostmanやブラウザにそのまま貼り、返ってくるエラーJSONの `reason` を読む
2. パラメータ名・値（緯度経度の範囲など）を確認

### レスポンスは取れているのに、DTOの値が `null` になる
**原因:** JSONの項目名とDTOのフィールド名が対応していない

**解決策:**
1. `@JsonProperty("...")` の名前が、実際のJSONの項目名と一致しているか確認
2. `log.debug` でレスポンスのJSON全文を出力して、実物を目で確認する
3. `UnrecognizedPropertyException` が出る場合は `@JsonIgnoreProperties(ignoreUnknown = true)` を付ける

### `429 Too Many Requests`
**原因:** 短時間にAPIを呼びすぎた（無料APIには利用制限がある）

**解決策:**
1. 数分待ってから再実行する
2. 開発中は、同じ地点を何度も連続で呼ばない。テストは `MockRestServiceServer` で行い、本物のAPIを呼ばない

### `MockRestServiceServer` のテストが「期待した呼び出しがない」で失敗する
**原因:** モックの期待（URL・回数）と、実際の呼び出しが一致していない

**解決策:**
1. `requestTo(...)` の条件が、実際のURLの一部と合っているか確認
2. テストの最後に `mockServer.verify()` を呼んでいるか確認
3. `RestTemplate` を、`MockRestServiceServer.createServer(restTemplate)` に渡したものと同じインスタンスで使っているか確認

---

## 🎉 完了後

次は [Day 21](day-21.md) で、このClientを使うWeatherServiceを実装します

お疲れさまでした！
