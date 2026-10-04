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

## 🎉 完了後

次は [Day 21](day-21.md) で、このClientを使うWeatherServiceを実装します

お疲れさまでした！
