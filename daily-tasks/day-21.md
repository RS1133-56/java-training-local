# Day 21: Service層実装（Weather）

## 📅 実施日
- 予定: Week 5 - Day 21
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
WeatherServiceを実装し、外部API連携（Day 20で作成したOpenMeteoClient）とデータベース保存のビジネスロジックを完成させる

> 📝 **前提**: Day 20で `OpenMeteoClient` と `ExternalApiException` を作成済みであること。

---

## 📋 午前の作業（9:00-13:00）

### 1. WeatherServiceの設計（9:00-9:30）

**WeatherServiceの責務:**
1. Open-Meteo APIから天気データ取得
2. APIレスポンスをEntityに変換
3. データベースに保存（WeatherRecord + DailyForecast）
4. EntityをDTOに変換して返却

**処理フロー:**
```
Controller → WeatherService
                ↓
            OpenMeteoClient (API呼び出し)
                ↓
            APIレスポンス受信
                ↓
            Entity変換
                ↓
            Repository保存
                ↓
            DTO変換
                ↓
            Controller ← DTO返却
```

---

### 2. WeatherService実装（9:30-12:00）

**インターフェース:** `src/main/java/com/example/weatherapp/service/WeatherService.java`

```java
package com.example.weatherapp.service;

import com.example.weatherapp.dto.WeatherDetailDto;

public interface WeatherService {
    
    WeatherDetailDto getWeatherByPrefectureId(Long prefectureId);
    
    WeatherDetailDto getLatestWeatherFromDb(Long prefectureId);
}
```

**実装クラス:** `src/main/java/com/example/weatherapp/service/impl/WeatherServiceImpl.java`

```java
package com.example.weatherapp.service.impl;

import com.example.weatherapp.client.OpenMeteoClient;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.dto.api.OpenMeteoResponseDto;
import com.example.weatherapp.entity.DailyForecast;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.mapper.WeatherMapper;
import com.example.weatherapp.repository.WeatherRecordRepository;
import com.example.weatherapp.service.PrefectureService;
import com.example.weatherapp.service.WeatherService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
@Transactional
@Slf4j
public class WeatherServiceImpl implements WeatherService {
    
    private final OpenMeteoClient openMeteoClient;
    private final WeatherRecordRepository weatherRecordRepository;
    private final PrefectureService prefectureService;
    private final WeatherMapper weatherMapper;
    
    public WeatherServiceImpl(
        OpenMeteoClient openMeteoClient,
        WeatherRecordRepository weatherRecordRepository,
        PrefectureService prefectureService,
        WeatherMapper weatherMapper
    ) {
        this.openMeteoClient = openMeteoClient;
        this.weatherRecordRepository = weatherRecordRepository;
        this.prefectureService = prefectureService;
        this.weatherMapper = weatherMapper;
    }
    
    @Override
    public WeatherDetailDto getWeatherByPrefectureId(Long prefectureId) {
        log.info("天気情報取得開始: prefectureId={}", prefectureId);
        
        Prefecture prefecture = prefectureService.findEntityById(prefectureId);
        log.debug("都道府県: {}", prefecture.getName());
        
        OpenMeteoResponseDto apiResponse = openMeteoClient.fetchWeather(
            prefecture.getLatitude(),
            prefecture.getLongitude()
        );
        
        WeatherRecord weatherRecord = buildWeatherRecord(apiResponse, prefecture);
        List<DailyForecast> dailyForecasts = buildDailyForecasts(apiResponse, weatherRecord);
        dailyForecasts.forEach(weatherRecord::addDailyForecast);
        
        WeatherRecord savedRecord = weatherRecordRepository.save(weatherRecord);
        log.info("天気情報保存完了: recordId={}", savedRecord.getId());
        
        return weatherMapper.toDetailDto(savedRecord);
    }
    
    @Override
    @Transactional(readOnly = true)
    public WeatherDetailDto getLatestWeatherFromDb(Long prefectureId) {
        return weatherRecordRepository
            .findLatestWithForecasts(prefectureId)
            .map(weatherMapper::toDetailDto)
            .orElse(null);
    }
    
    private WeatherRecord buildWeatherRecord(
        OpenMeteoResponseDto apiResponse, 
        Prefecture prefecture
    ) {
        var current = apiResponse.getCurrent();
        
        return WeatherRecord.builder()
            .prefecture(prefecture)
            .fetchedAt(LocalDateTime.now())
            .temperature(current.getTemperature2m())
            .weatherCode(current.getWeathercode())
            .windSpeed(current.getWindspeed10m())
            .humidity(current.getRelativehumidity2m())
            .apparentTemperature(current.getApparentTemperature())
            .precipitation(current.getPrecipitation())
            .cloudCover(current.getCloudCover())
            .build();
    }
    
    private List<DailyForecast> buildDailyForecasts(
        OpenMeteoResponseDto apiResponse,
        WeatherRecord weatherRecord
    ) {
        List<DailyForecast> forecasts = new ArrayList<>();
        var daily = apiResponse.getDaily();
        
        for (int i = 0; i < daily.getTime().size(); i++) {
            DailyForecast forecast = DailyForecast.builder()
                .weatherRecord(weatherRecord)
                .forecastDate(LocalDate.parse(daily.getTime().get(i)))
                .temperatureMax(daily.getTemperature2mMax().get(i))
                .temperatureMin(daily.getTemperature2mMin().get(i))
                .weatherCode(daily.getWeathercode().get(i))
                .precipitationSum(daily.getPrecipitationSum().get(i))
                .windSpeedMax(getOrNull(daily.getWindspeed10mMax(), i))
                .sunrise(parseTime(daily.getSunrise(), i))
                .sunset(parseTime(daily.getSunset(), i))
                .build();
            
            forecasts.add(forecast);
        }
        
        return forecasts;
    }
    
    private <T> T getOrNull(List<T> list, int index) {
        if (list == null || index >= list.size()) {
            return null;
        }
        return list.get(index);
    }
    
    private LocalTime parseTime(List<String> timeList, int index) {
        String timeStr = getOrNull(timeList, index);
        if (timeStr == null) {
            return null;
        }
        
        try {
            LocalDateTime dateTime = LocalDateTime.parse(timeStr);
            return dateTime.toLocalTime();
        } catch (Exception e) {
            log.warn("時刻パース失敗: {}", timeStr, e);
            return null;
        }
    }
}
```

---

## 午後の作業（13:00-17:00）

### 3. WeatherServiceImplのテスト作成（13:00-16:00）

Day 20で `OpenMeteoClient` が完成しているので、`WeatherServiceImpl` もテストできます。
外部API・DBには実際にアクセスせず、**Mockito** で依存クラスをモックにして、Serviceのロジックだけを確認します。

`src/test/java/com/example/weatherapp/service/WeatherServiceImplTest.java`:

```java
package com.example.weatherapp.service;

import com.example.weatherapp.client.OpenMeteoClient;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.exception.ExternalApiException;
import com.example.weatherapp.mapper.WeatherMapper;
import com.example.weatherapp.repository.WeatherRecordRepository;
import com.example.weatherapp.service.impl.WeatherServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class WeatherServiceImplTest {

    @Mock
    private OpenMeteoClient openMeteoClient;
    @Mock
    private WeatherRecordRepository weatherRecordRepository;
    @Mock
    private PrefectureService prefectureService;
    @Mock
    private WeatherMapper weatherMapper;

    @InjectMocks
    private WeatherServiceImpl weatherService;

    @Test
    @DisplayName("DBに保存済みの最新データがあればDTOに変換して返す")
    void getLatestWeatherFromDb_found() {
        // Given
        WeatherRecord record = new WeatherRecord();
        WeatherDetailDto dto = WeatherDetailDto.builder().build();
        when(weatherRecordRepository.findLatestWithForecasts(13L))
            .thenReturn(Optional.of(record));
        when(weatherMapper.toDetailDto(record)).thenReturn(dto);

        // When
        WeatherDetailDto result = weatherService.getLatestWeatherFromDb(13L);

        // Then
        assertThat(result).isSameAs(dto);
    }

    @Test
    @DisplayName("DBにデータがなければnullを返す")
    void getLatestWeatherFromDb_notFound() {
        // Given
        when(weatherRecordRepository.findLatestWithForecasts(13L))
            .thenReturn(Optional.empty());

        // When & Then
        assertThat(weatherService.getLatestWeatherFromDb(13L)).isNull();
    }

    @Test
    @DisplayName("外部APIが失敗したら例外が伝わり、DBには保存されない")
    void getWeatherByPrefectureId_apiError() {
        // Given: 都道府県の取得は成功し、API呼び出しだけ失敗する
        com.example.weatherapp.entity.Prefecture tokyo = new com.example.weatherapp.entity.Prefecture();
        tokyo.setLatitude(35.689);
        tokyo.setLongitude(139.692);
        when(prefectureService.findEntityById(13L)).thenReturn(tokyo);
        when(openMeteoClient.fetchWeather(35.689, 139.692))
            .thenThrow(new ExternalApiException("天気情報の取得に失敗しました"));

        // When & Then
        assertThatThrownBy(() -> weatherService.getWeatherByPrefectureId(13L))
            .isInstanceOf(ExternalApiException.class);
        verify(weatherRecordRepository, never()).save(any());
    }
}
```

> 💡 **ポイント**: `@Mock` で本物の代わりになるニセモノを作り、`@InjectMocks` で `WeatherServiceImpl` のコンストラクタに自動で渡します。
> API正常系（レスポンスを組み立てて保存まで確認するテスト）は、余力があれば挑戦してみましょう。

**実行:**

```bash
./gradlew test --tests WeatherServiceImplTest
```

---

## ✅ チェックリスト

- [ ] WeatherServiceインターフェース作成
- [ ] WeatherServiceImpl実装
- [ ] WeatherServiceImplのテスト作成・実行
- [ ] GitHubにプッシュ

---

## 📚 参考リンク

- [Spring @Transactional（日本語）](https://qiita.com/NagaokaKenichi/items/c3371ce8dea0a1f8fa5b)

---

## 🆘 トラブルシューティング

### `NoSuchBeanDefinitionException: ... OpenMeteoClient`
**原因:** Day 20で作ったClientがSpringに登録されていない、または未実装

**解決策:**
1. `OpenMeteoClient` に `@Component` が付いているか確認
2. Day 20のClient・設定クラス（`RestTemplateConfig`）が完成しているか確認

### `TransientPropertyValueException` / `object references an unsaved transient instance`
**原因:** 親（WeatherRecord）を保存する前に、子（DailyForecast）を参照している

**解決策:**
1. `cascade = CascadeType.ALL` が親側の関連に付いているか確認
2. 子の追加は、Entityのヘルパーメソッド（`addDailyForecast`）を使い、**親に子を追加してから親を保存**する

### `DataIntegrityViolationException`（NOT NULL違反など）
**原因:** 必須の列（取得日時、都道府県など）に値が入っていない

**解決策:**
1. エラーメッセージの `Column 'xxx' cannot be null` で、列名を特定する
2. Entityの組み立て（`buildWeatherRecord`）で、その列に値を設定しているか確認

### `LazyInitializationException`
**原因:** トランザクションの外で、遅延読み込みの関連データにアクセスしている

**解決策:**
1. Serviceのメソッドに `@Transactional` があるか確認
2. DTOに変換する処理も、トランザクションの範囲内で行う

### Mockitoテストで `NullPointerException`／`Wanted but not invoked`
**原因:** 必要なモックの設定（`when`）が足りない、または呼び出しの引数が違う

**解決策:**
1. Serviceが呼ぶ全ての依存先（Client・Repository・Mapperなど）について、`when(...).thenReturn(...)` を設定したか確認
2. `verify(...)` に渡す引数が、実際に渡された値と同じか確認

---

## 🎉 完了後

次は [Day 22](day-22.md) へ

お疲れさまでした！
