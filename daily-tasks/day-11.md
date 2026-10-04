# Day 11: テーブル定義書とDDL作成

## 📅 実施日
- 予定: Week 3 - Day 11
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
テーブル定義書を作成し、DDLスクリプトを完成させる

---

## 午前の作業（9:00-13:00）

### 1. テーブル定義書の作成

`table-definitions.md`を作成：

#### prefectures（都道府県マスタ）

| 列名 | データ型 | NULL | デフォルト | 説明 |
|------|---------|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | 主キー |
| name | VARCHAR(10) | NO | - | 都道府県名 |
| name_en | VARCHAR(50) | NO | - | 英語名 |
| latitude | DECIMAL(9,6) | NO | - | 緯度 |
| longitude | DECIMAL(9,6) | NO | - | 経度 |
| region | VARCHAR(20) | NO | - | 地域区分 |
| created_at | TIMESTAMP | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | NO | ON UPDATE | 更新日時 |

---

### 2. DDLスクリプト作成（10:00-12:00）

`src/main/resources/schema.sql`を作成：

```sql
-- データベース作成
CREATE DATABASE IF NOT EXISTS weather_app 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE weather_app;

-- 既存テーブルを削除（開発環境のみ）
DROP TABLE IF EXISTS daily_forecasts;
DROP TABLE IF EXISTS weather_records;
DROP TABLE IF EXISTS prefectures;

-- prefectures（都道府県マスタ）
CREATE TABLE prefectures (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL COMMENT '都道府県名',
    name_en VARCHAR(50) NOT NULL COMMENT '英語名',
    latitude DECIMAL(9, 6) NOT NULL COMMENT '緯度',
    longitude DECIMAL(9, 6) NOT NULL COMMENT '経度',
    region VARCHAR(20) NOT NULL COMMENT '地域区分',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='都道府県マスタ';

-- weather_records（天気記録）
CREATE TABLE weather_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    prefecture_id BIGINT NOT NULL COMMENT '都道府県ID',
    fetched_at TIMESTAMP NOT NULL COMMENT '取得日時',
    temperature DECIMAL(5, 2) COMMENT '気温（℃）',
    weather_code INT COMMENT '天気コード',
    wind_speed DECIMAL(5, 2) COMMENT '風速（m/s）',
    humidity INT COMMENT '湿度（%）',
    apparent_temperature DECIMAL(5, 2) COMMENT '体感温度（℃）',
    precipitation DECIMAL(5, 2) COMMENT '降水量（mm）',
    cloud_cover INT COMMENT '雲量（%）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY fk_prefecture (prefecture_id) 
        REFERENCES prefectures(id) ON DELETE CASCADE,
    INDEX idx_prefecture (prefecture_id),
    INDEX idx_fetched (fetched_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='天気記録';

-- daily_forecasts（日次予報）
CREATE TABLE daily_forecasts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    weather_record_id BIGINT NOT NULL COMMENT '天気記録ID',
    forecast_date DATE NOT NULL COMMENT '予報日',
    temperature_max DECIMAL(5, 2) COMMENT '最高気温（℃）',
    temperature_min DECIMAL(5, 2) COMMENT '最低気温（℃）',
    weather_code INT COMMENT '天気コード',
    precipitation_sum DECIMAL(5, 2) COMMENT '降水量合計（mm）',
    wind_speed_max DECIMAL(5, 2) COMMENT '最大風速（m/s）',
    sunrise TIME COMMENT '日の出時刻',
    sunset TIME COMMENT '日の入り時刻',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY fk_weather_record (weather_record_id) 
        REFERENCES weather_records(id) ON DELETE CASCADE,
    INDEX idx_record (weather_record_id),
    INDEX idx_date (forecast_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='日次予報';
```

---

## 午後の作業（13:00-17:00）

### 3. MySQL Workbenchでの実行（13:00-14:00）

1. MySQL Workbenchを開く
2. `schema.sql`を開く
3. 実行（⚡ボタン）
4. テーブルが作成されたことを確認

```sql
SHOW TABLES;
DESCRIBE prefectures;
DESCRIBE weather_records;
DESCRIBE daily_forecasts;
```

---

### 4. Spring Bootでの自動実行設定（14:00-15:00）

`application.properties`に追加：

```properties
# Schema initialization
spring.sql.init.mode=always
spring.sql.init.schema-locations=classpath:schema.sql
spring.sql.init.data-locations=classpath:data.sql
spring.sql.init.continue-on-error=false

# JPA設定
spring.jpa.hibernate.ddl-auto=none
```

---

### 5. ドキュメント整備（15:00-17:00）

`database-setup-guide.md`を作成

---

## ✅ チェックリスト

- [ ] テーブル定義書作成
- [ ] DDLスクリプト作成
- [ ] MySQLでテーブル作成確認
- [ ] Spring Boot設定完了
- [ ] GitHubにプッシュ

---

## 🎉 完了後

次は [Day 12](day-12.md) へ

お疲れさまでした！
