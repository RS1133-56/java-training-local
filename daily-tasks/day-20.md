# Day 20: Service層実装（Weather）

## 📅 実施日
- 予定: Week 4 - Day 20
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
WeatherServiceを実装し、外部API連携とデータベース保存のビジネスロジックを完成させる

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

## ✅ チェックリスト

- [ ] WeatherServiceインターフェース作成
- [ ] WeatherServiceImpl実装
- [ ] テスト作成
- [ ] GitHubにプッシュ

---

## 📚 参考リンク

- [Spring @Transactional（日本語）](https://qiita.com/NagaokaKenichi/items/c3371ce8dea0a1f8fa5b)

---

## 🎉 完了後

次は [Day 21](day-21.md) へ

お疲れさまでした！
