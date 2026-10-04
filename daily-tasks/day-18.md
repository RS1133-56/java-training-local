# Day 18: DTO設計と実装

## 📅 実施日
- 予定: Week 4 - Day 18
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
データ転送用のDTOクラスを設計・実装し、EntityとDTOの変換ロジックを作成する

---

## 📋 午前の作業（9:00-13:00）

### 1. DTOの基礎理解（9:00-9:30）

**DTOとは:**
- Data Transfer Object（データ転送オブジェクト）
- レイヤー間でデータを運ぶための専用クラス
- Entityをそのまま公開せず、必要な情報だけを選択

**Entity vs DTO:**

```java
// Entity（データベースと1対1）
@Entity
public class User {
    private Long id;
    private String password;  // ← これは外部に出したくない
    private LocalDateTime createdAt;
}

// DTO（外部公開用）
public class UserDto {
    private Long id;
    private String name;
    // passwordは含めない！
}
```

**DTOを使う理由:**
1. セキュリティ: パスワードなど機密情報を除外
2. パフォーマンス: 必要なデータのみ転送
3. 柔軟性: Entity変更の影響を最小化
4. API設計: クライアントに最適な形式で提供

---

### 2. DTOクラス設計（9:30-12:00）

#### PrefectureDto

`src/main/java/com/example/weatherapp/dto/PrefectureDto.java`:

```java
package com.example.weatherapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 都道府県情報DTO
 * 画面表示・API応答用
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PrefectureDto {
    
    /** 都道府県ID */
    private Long id;
    
    /** 都道府県名 */
    private String name;
    
    /** 英語名 */
    private String nameEn;
    
    /** 緯度 */
    private Double latitude;
    
    /** 経度 */
    private Double longitude;
    
    /** 地域 */
    private String region;
    
    // createdAt, updatedAtは含めない（不要なため）
}
```

#### CurrentWeatherDto

`src/main/java/com/example/weatherapp/dto/CurrentWeatherDto.java`:

```java
package com.example.weatherapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 現在の天気DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CurrentWeatherDto {
    
    /** 観測時刻 */
    private LocalDateTime time;
    
    /** 気温（℃） */
    private Double temperature;
    
    /** 天気コード */
    private Integer weatherCode;
    
    /** 天気の説明（日本語） */
    private String weatherDescription;
    
    /** 天気アイコン */
    private String weatherIcon;
    
    /** 風速（m/s） */
    private Double windSpeed;
    
    /** 湿度（%） */
    private Integer humidity;
    
    /** 体感温度（℃） */
    private Double apparentTemperature;
    
    /** 降水量（mm） */
    private Double precipitation;
    
    /** 雲量（%） */
    private Integer cloudCover;
}
```

#### DailyForecastDto

`src/main/java/com/example/weatherapp/dto/DailyForecastDto.java`:

```java
package com.example.weatherapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalTime;

/**
 * 日次予報DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DailyForecastDto {
    
    /** 予報日 */
    private LocalDate date;
    
    /** 曜日（月、火、...） */
    private String dayOfWeek;
    
    /** 最高気温（℃） */
    private Double temperatureMax;
    
    /** 最低気温（℃） */
    private Double temperatureMin;
    
    /** 天気コード */
    private Integer weatherCode;
    
    /** 天気の説明 */
    private String weatherDescription;
    
    /** 天気アイコン */
    private String weatherIcon;
    
    /** 降水量合計（mm） */
    private Double precipitationSum;
    
    /** 降水確率（%） ※計算で算出 */
    private Integer precipitationProbability;
    
    /** 最大風速（m/s） */
    private Double windSpeedMax;
    
    /** 日の出時刻 */
    private LocalTime sunrise;
    
    /** 日の入り時刻 */
    private LocalTime sunset;
}
```

#### WeatherDetailDto

`src/main/java/com/example/weatherapp/dto/WeatherDetailDto.java`:

```java
package com.example.weatherapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 天気詳細画面用DTO
 * 都道府県情報 + 現在の天気 + 週間予報をまとめたもの
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class WeatherDetailDto {
    
    /** 都道府県情報 */
    private PrefectureDto prefecture;
    
    /** 現在の天気 */
    private CurrentWeatherDto current;
    
    /** 週間予報（7日分） */
    private List<DailyForecastDto> dailyForecasts;
    
    /** データ取得日時 */
    private LocalDateTime fetchedAt;
}
```

---

## 午後の作業（13:00-17:00）

### 3. 天気コードマッピング実装（13:00-14:00）

`src/main/java/com/example/weatherapp/util/WeatherCodeMapper.java`:

```java
package com.example.weatherapp.util;

import java.util.HashMap;
import java.util.Map;

/**
 * WMO天気コードと説明文・アイコンのマッピング
 */
public class WeatherCodeMapper {
    
    private static final Map<Integer, String> DESCRIPTIONS = new HashMap<>();
    private static final Map<Integer, String> ICONS = new HashMap<>();
    
    static {
        // 晴れ系（0-3）
        DESCRIPTIONS.put(0, "快晴");
        DESCRIPTIONS.put(1, "晴れ");
        DESCRIPTIONS.put(2, "一部曇り");
        DESCRIPTIONS.put(3, "曇り");
        
        ICONS.put(0, "☀️");
        ICONS.put(1, "🌤️");
        ICONS.put(2, "⛅");
        ICONS.put(3, "☁️");
        
        // 霧（45-48）
        DESCRIPTIONS.put(45, "霧");
        DESCRIPTIONS.put(48, "霧氷");
        
        ICONS.put(45, "🌫️");
        ICONS.put(48, "🌫️");
        
        // 霧雨（51-55）
        DESCRIPTIONS.put(51, "軽い霧雨");
        DESCRIPTIONS.put(53, "霧雨");
        DESCRIPTIONS.put(55, "激しい霧雨");
        
        ICONS.put(51, "🌦️");
        ICONS.put(53, "🌦️");
        ICONS.put(55, "🌦️");
        
        // 雨（61-67）
        DESCRIPTIONS.put(61, "小雨");
        DESCRIPTIONS.put(63, "雨");
        DESCRIPTIONS.put(65, "大雨");
        DESCRIPTIONS.put(66, "凍雨");
        DESCRIPTIONS.put(67, "激しい凍雨");
        
        ICONS.put(61, "🌧️");
        ICONS.put(63, "🌧️");
        ICONS.put(65, "🌧️");
        ICONS.put(66, "🌧️");
        ICONS.put(67, "🌧️");
        
        // 雪（71-77）
        DESCRIPTIONS.put(71, "小雪");
        DESCRIPTIONS.put(73, "雪");
        DESCRIPTIONS.put(75, "大雪");
        DESCRIPTIONS.put(77, "雪粒");
        
        ICONS.put(71, "🌨️");
        ICONS.put(73, "❄️");
        ICONS.put(75, "❄️");
        ICONS.put(77, "🌨️");
        
        // にわか雨・雪（80-86）
        DESCRIPTIONS.put(80, "にわか雨");
        DESCRIPTIONS.put(81, "強いにわか雨");
        DESCRIPTIONS.put(82, "激しいにわか雨");
        DESCRIPTIONS.put(85, "にわか雪");
        DESCRIPTIONS.put(86, "強いにわか雪");
        
        ICONS.put(80, "🌦️");
        ICONS.put(81, "🌦️");
        ICONS.put(82, "🌦️");
        ICONS.put(85, "🌨️");
        ICONS.put(86, "🌨️");
        
        // 雷雨（95-99）
        DESCRIPTIONS.put(95, "雷雨");
        DESCRIPTIONS.put(96, "雷雨（雹）");
        DESCRIPTIONS.put(99, "激しい雷雨（雹）");
        
        ICONS.put(95, "⛈️");
        ICONS.put(96, "⛈️");
        ICONS.put(99, "⛈️");
    }
    
    /**
     * 天気コードから説明文を取得
     */
    public static String getDescription(Integer code) {
        if (code == null) {
            return "不明";
        }
        return DESCRIPTIONS.getOrDefault(code, "不明");
    }
    
    /**
     * 天気コードからアイコンを取得
     */
    public static String getIcon(Integer code) {
        if (code == null) {
            return "❓";
        }
        return ICONS.getOrDefault(code, "❓");
    }
}
```

---

### 4. Mapperクラス実装（14:00-16:00）

`src/main/java/com/example/weatherapp/mapper/PrefectureMapper.java`:

```java
package com.example.weatherapp.mapper;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.entity.Prefecture;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Prefecture ↔ PrefectureDto 変換
 */
@Component
public class PrefectureMapper {
    
    /**
     * Entity → DTO
     */
    public PrefectureDto toDto(Prefecture entity) {
        if (entity == null) {
            return null;
        }
        
        return PrefectureDto.builder()
            .id(entity.getId())
            .name(entity.getName())
            .nameEn(entity.getNameEn())
            .latitude(entity.getLatitude())
            .longitude(entity.getLongitude())
            .region(entity.getRegion())
            .build();
    }
    
    /**
     * Entity List → DTO List
     */
    public List<PrefectureDto> toDtoList(List<Prefecture> entities) {
        return entities.stream()
            .map(this::toDto)
            .collect(Collectors.toList());
    }
    
    /**
     * DTO → Entity（新規作成時）
     */
    public Prefecture toEntity(PrefectureDto dto) {
        if (dto == null) {
            return null;
        }
        
        return Prefecture.builder()
            .id(dto.getId())
            .name(dto.getName())
            .nameEn(dto.getNameEn())
            .latitude(dto.getLatitude())
            .longitude(dto.getLongitude())
            .region(dto.getRegion())
            .build();
    }
}
```

`src/main/java/com/example/weatherapp/mapper/WeatherMapper.java`:

```java
package com.example.weatherapp.mapper;

import com.example.weatherapp.dto.CurrentWeatherDto;
import com.example.weatherapp.dto.DailyForecastDto;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.entity.DailyForecast;
import com.example.weatherapp.entity.WeatherRecord;
import com.example.weatherapp.util.WeatherCodeMapper;
import org.springframework.stereotype.Component;

import java.time.format.DateTimeFormatter;
import java.time.format.TextStyle;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

/**
 * WeatherRecord/DailyForecast ↔ DTO 変換
 */
@Component
public class WeatherMapper {
    
    private final PrefectureMapper prefectureMapper;
    
    public WeatherMapper(PrefectureMapper prefectureMapper) {
        this.prefectureMapper = prefectureMapper;
    }
    
    /**
     * WeatherRecord → CurrentWeatherDto
     */
    public CurrentWeatherDto toCurrentDto(WeatherRecord record) {
        if (record == null) {
            return null;
        }
        
        return CurrentWeatherDto.builder()
            .time(record.getFetchedAt())
            .temperature(record.getTemperature())
            .weatherCode(record.getWeatherCode())
            .weatherDescription(WeatherCodeMapper.getDescription(record.getWeatherCode()))
            .weatherIcon(WeatherCodeMapper.getIcon(record.getWeatherCode()))
            .windSpeed(record.getWindSpeed())
            .humidity(record.getHumidity())
            .apparentTemperature(record.getApparentTemperature())
            .precipitation(record.getPrecipitation())
            .cloudCover(record.getCloudCover())
            .build();
    }
    
    /**
     * DailyForecast → DailyForecastDto
     */
    public DailyForecastDto toDailyDto(DailyForecast forecast) {
        if (forecast == null) {
            return null;
        }
        
        // 曜日を日本語で取得
        String[] weekNames = {"月", "火", "水", "木", "金", "土", "日"};
        String dayOfWeek = weekNames[forecast.getForecastDate().getDayOfWeek().getValue()];
        
        // 降水確率を計算（降水量から推定）
        Integer precipProb = calculatePrecipitationProbability(
            forecast.getPrecipitationSum()
        );
        
        return DailyForecastDto.builder()
            .date(forecast.getForecastDate())
            .dayOfWeek(dayOfWeek)
            .temperatureMax(forecast.getTemperatureMax())
            .temperatureMin(forecast.getTemperatureMin())
            .weatherCode(forecast.getWeatherCode())
            .weatherDescription(WeatherCodeMapper.getDescription(forecast.getWeatherCode()))
            .weatherIcon(WeatherCodeMapper.getIcon(forecast.getWeatherCode()))
            .precipitationSum(forecast.getPrecipitationSum())
            .precipitationProbability(precipProb)
            .windSpeedMax(forecast.getWindSpeedMax())
            .sunrise(forecast.getSunrise())
            .sunset(forecast.getSunset())
            .build();
    }
    
    /**
     * DailyForecast List → DailyForecastDto List
     */
    public List<DailyForecastDto> toDailyDtoList(List<DailyForecast> forecasts) {
        return forecasts.stream()
            .map(this::toDailyDto)
            .collect(Collectors.toList());
    }
    
    /**
     * WeatherRecord → WeatherDetailDto（完全版）
     */
    public WeatherDetailDto toDetailDto(WeatherRecord record) {
        if (record == null) {
            return null;
        }
        
        return WeatherDetailDto.builder()
            .prefecture(prefectureMapper.toDto(record.getPrefecture()))
            .current(toCurrentDto(record))
            .dailyForecasts(toDailyDtoList(record.getDailyForecasts()))
            .fetchedAt(record.getFetchedAt())
            .build();
    }
    
    /**
     * 降水量から降水確率を推定（簡易計算）
     */
    private Integer calculatePrecipitationProbability(Double precipSum) {
        if (precipSum == null || precipSum <= 0) {
            return 0;
        } else if (precipSum < 1.0) {
            return 20;
        } else if (precipSum < 5.0) {
            return 50;
        } else if (precipSum < 10.0) {
            return 70;
        } else {
            return 90;
        }
    }
}
```

---

### 5. Mapperのテスト（16:00-17:00）

`src/test/java/com/example/weatherapp/mapper/WeatherMapperTest.java`:

```java
package com.example.weatherapp.mapper;

import com.example.weatherapp.dto.CurrentWeatherDto;
import com.example.weatherapp.dto.DailyForecastDto;
import com.example.weatherapp.dto.WeatherDetailDto;
import com.example.weatherapp.entity.DailyForecast;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.entity.WeatherRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class WeatherMapperTest {
    
    private WeatherMapper weatherMapper;
    private PrefectureMapper prefectureMapper;
    
    @BeforeEach
    void setUp() {
        prefectureMapper = new PrefectureMapper();
        weatherMapper = new WeatherMapper(prefectureMapper);
    }
    
    @Test
    @DisplayName("WeatherRecordをCurrentWeatherDtoに変換できる")
    void testToCurrentDto() {
        // Given
        WeatherRecord record = WeatherRecord.builder()
            .fetchedAt(LocalDateTime.now())
            .temperature(15.5)
            .weatherCode(1)
            .windSpeed(3.2)
            .humidity(65)
            .apparentTemperature(13.8)
            .precipitation(0.0)
            .cloudCover(25)
            .build();
        
        // When
        CurrentWeatherDto dto = weatherMapper.toCurrentDto(record);
        
        // Then
        assertThat(dto).isNotNull();
        assertThat(dto.getTemperature()).isEqualTo(15.5);
        assertThat(dto.getWeatherCode()).isEqualTo(1);
        assertThat(dto.getWeatherDescription()).isEqualTo("晴れ");
        assertThat(dto.getWeatherIcon()).isEqualTo("🌤️");
    }
    
    @Test
    @DisplayName("DailyForecastをDailyForecastDtoに変換できる")
    void testToDailyDto() {
        // Given
        DailyForecast forecast = DailyForecast.builder()
            .forecastDate(LocalDate.of(2024, 1, 5))
            .temperatureMax(15.2)
            .temperatureMin(8.1)
            .weatherCode(61)
            .precipitationSum(5.2)
            .windSpeedMax(8.1)
            .sunrise(LocalTime.of(6, 51))
            .sunset(LocalTime.of(16, 46))
            .build();
        
        // When
        DailyForecastDto dto = weatherMapper.toDailyDto(forecast);
        
        // Then
        assertThat(dto).isNotNull();
        assertThat(dto.getDate()).isEqualTo(LocalDate.of(2024, 1, 5));
        assertThat(dto.getDayOfWeek()).isEqualTo("金");
        assertThat(dto.getWeatherDescription()).isEqualTo("小雨");
        assertThat(dto.getWeatherIcon()).isEqualTo("🌧️");
        assertThat(dto.getPrecipitationProbability()).isEqualTo(70);
    }
    
    @Test
    @DisplayName("WeatherRecordを完全なWeatherDetailDtoに変換できる")
    void testToDetailDto() {
        // Given
        Prefecture prefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .build();
        
        WeatherRecord record = WeatherRecord.builder()
            .prefecture(prefecture)
            .fetchedAt(LocalDateTime.now())
            .temperature(15.5)
            .weatherCode(1)
            .build();
        
        List<DailyForecast> forecasts = new ArrayList<>();
        for (int i = 0; i < 7; i++) {
            forecasts.add(DailyForecast.builder()
                .weatherRecord(record)
                .forecastDate(LocalDate.now().plusDays(i))
                .temperatureMax(15.0 + i)
                .temperatureMin(8.0 + i)
                .weatherCode(1)
                .build());
        }
        record.getDailyForecasts().addAll(forecasts);
        
        // When
        WeatherDetailDto dto = weatherMapper.toDetailDto(record);
        
        // Then
        assertThat(dto).isNotNull();
        assertThat(dto.getPrefecture()).isNotNull();
        assertThat(dto.getPrefecture().getName()).isEqualTo("東京都");
        assertThat(dto.getCurrent()).isNotNull();
        assertThat(dto.getDailyForecasts()).hasSize(7);
    }
}
```

---

## ✅ チェックリスト

- [ ] DTOの概念を理解した
- [ ] PrefectureDto実装
- [ ] CurrentWeatherDto実装
- [ ] DailyForecastDto実装
- [ ] WeatherDetailDto実装
- [ ] WeatherCodeMapper実装
- [ ] Mapperクラス実装
- [ ] Mapperのテスト作成・パス
- [ ] GitHubにプッシュ

---

## 📚 参考リンク

- [DTOパターンとは（日本語）](https://qiita.com/yuki153/items/a350419e20876b3ca4dd)
- [MapperとModelMapperの使い分け（日本語）](https://qiita.com/disc99/items/a6ab6e5e3f1698e35a0e)
- [Lombokの@Builder使い方（日本語）](https://qiita.com/opengl-8080/items/671ffd4bf0e01c1fbf6c)

---

## 🆘 トラブルシューティング

### `@Builder` を付けたら `no suitable constructor` / デフォルトコンストラクタがないエラー
**原因:** `@Builder` と `@NoArgsConstructor` を併用すると、全引数のコンストラクタが必要になる

**解決策:**
1. `@Builder` / `@NoArgsConstructor` / `@AllArgsConstructor` の3つをセットで付ける

### MapperでNullPointerException
**原因:** Entityの項目や関連が `null` のまま、メソッドを呼んでいる

**解決策:**
1. 変換の入口で `if (entity == null) return null;` を入れる
2. `null` になりうる項目（任意の列）は、呼び出す前に `null` チェックをする

### `StackOverflowError`（`toString` やJSON変換で無限ループ）
**原因:** EntityとEntityが双方向に参照し合っている

**解決策:**
1. DTOには、Entityそのものではなく**必要な値だけ**を持たせる
2. Entityの `@ToString` / `@EqualsAndHashCode` では、相手側の関連項目を除外する（`@ToString.Exclude`）

### 天気の説明やアイコンが「不明」になる
**原因:** 天気コードのMapのキーの型や、未定義のコードが原因

**解決策:**
1. Mapのキーが `Integer` か確認（`Long` や `String` と混ざっていないか）
2. 対象のコードがMapに登録されているか確認（Day 7の天気コード表と照合）

### テストが失敗した（`expected` と `actual` が違う）
**原因:** 実装かテスト（期待値）のどちらかが間違っている

**解決策:**
1. エラーメッセージの `Expecting ... to be equal to ...` の**2つの値**を読む
2. 仕様として正しいのは実装の値か期待値か、根拠（仕様・計算式・API仕様）で確認する
3. どの入力でどの値になるかを、`System.out.println` かデバッガで1つずつ確認する

---

## 🎉 完了後

次は [Day 19](day-19.md) でPrefectureServiceを実装する

お疲れさまでした！
