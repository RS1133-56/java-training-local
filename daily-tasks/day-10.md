# Day 10: データベース設計（ER図）

## 📅 実施日
- 予定: Week 2 - Day 10
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
天気アプリのデータベース構造を設計し、ER図を作成する

---

## 午前の作業

### 1. テーブル設計（9:00-12:00）

#### prefectures（都道府県マスタ）
```sql
CREATE TABLE prefectures (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    name_en VARCHAR(50) NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    region VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### weather_records（天気記録）
```sql
CREATE TABLE weather_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    prefecture_id BIGINT NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    temperature DOUBLE,
    weather_code INT,
    wind_speed DOUBLE,
    humidity INT,
    apparent_temperature DOUBLE,
    precipitation DOUBLE,
    cloud_cover INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prefecture_id) REFERENCES prefectures(id)
);
```

#### daily_forecasts（日次予報）
```sql
CREATE TABLE daily_forecasts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    weather_record_id BIGINT NOT NULL,
    forecast_date DATE NOT NULL,
    temperature_max DOUBLE,
    temperature_min DOUBLE,
    weather_code INT,
    precipitation_sum DOUBLE,
    wind_speed_max DOUBLE,
    sunrise TIME,
    sunset TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (weather_record_id) REFERENCES weather_records(id) ON DELETE CASCADE
);
```

**ER図を作成（draw.io）:**
```
prefectures     weather_records     daily_forecasts
┌──────────┐    ┌──────────────┐    ┌───────────────┐
│id (PK)   │───<│id (PK)       │───<│id (PK)        │
│name      │    │prefecture_id │    │weather_rec_id │
│latitude  │    │fetched_at    │    │forecast_date  │
│longitude │    │temperature   │    │temperature_max│
│region    │    │weather_code  │    │temperature_min│
└──────────┘    │...           │    │weather_code   │
                └──────────────┘    │...            │
                                    └───────────────┘
```

---

## 午後の作業

### 2. インデックス設計（13:00-15:00）

```sql
-- weather_recordsの検索を高速化
CREATE INDEX idx_weather_records_prefecture 
ON weather_records(prefecture_id);

CREATE INDEX idx_weather_records_fetched 
ON weather_records(fetched_at);

-- daily_forecastsの検索を高速化
CREATE INDEX idx_daily_forecasts_record 
ON daily_forecasts(weather_record_id);

CREATE INDEX idx_daily_forecasts_date 
ON daily_forecasts(forecast_date);
```

### 3. ドキュメント作成（15:00-17:00）

`database-design.md`を作成

---

## ✅ チェックリスト

- [ ] テーブル設計完了
- [ ] ER図作成
- [ ] インデックス設計完了
- [ ] ドキュメント作成
- [ ] GitHubにプッシュ

---

## 🎉 完了後

次は [Day 11](day-11.md) へ

お疲れさまでした！
