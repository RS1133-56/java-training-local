# Day 12: 初期データ投入

## 📅 実施日
- 予定: Week 3 - Day 12
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
47都道府県の初期データをデータベースに投入する

---

## 午前の作業（9:00-13:00）

### 1. 初期データファイルの作成（9:00-11:00）

`src/main/resources/data.sql`を作成：

```sql
-- 47都道府県の初期データ

-- 北海道・東北
INSERT INTO prefectures (id, name, name_en, latitude, longitude, region) VALUES
(1, '北海道', 'Hokkaido', 43.064, 141.347, '北海道'),
(2, '青森県', 'Aomori', 40.824, 140.740, '東北'),
(3, '岩手県', 'Iwate', 39.704, 141.153, '東北'),
(4, '宮城県', 'Miyagi', 38.269, 140.872, '東北'),
(5, '秋田県', 'Akita', 39.719, 140.103, '東北'),
(6, '山形県', 'Yamagata', 38.241, 140.364, '東北'),
(7, '福島県', 'Fukushima', 37.750, 140.468, '東北'),

-- 関東
(8, '茨城県', 'Ibaraki', 36.341, 140.447, '関東'),
(9, '栃木県', 'Tochigi', 36.566, 139.883, '関東'),
(10, '群馬県', 'Gunma', 36.391, 139.061, '関東'),
(11, '埼玉県', 'Saitama', 35.857, 139.649, '関東'),
(12, '千葉県', 'Chiba', 35.605, 140.123, '関東'),
(13, '東京都', 'Tokyo', 35.689, 139.692, '関東'),
(14, '神奈川県', 'Kanagawa', 35.448, 139.643, '関東'),

-- 中部
(15, '新潟県', 'Niigata', 37.902, 139.023, '中部'),
(16, '富山県', 'Toyama', 36.695, 137.211, '中部'),
(17, '石川県', 'Ishikawa', 36.595, 136.626, '中部'),
(18, '福井県', 'Fukui', 36.065, 136.222, '中部'),
(19, '山梨県', 'Yamanashi', 35.664, 138.568, '中部'),
(20, '長野県', 'Nagano', 36.651, 138.181, '中部'),
(21, '岐阜県', 'Gifu', 35.391, 136.722, '中部'),
(22, '静岡県', 'Shizuoka', 34.977, 138.383, '中部'),
(23, '愛知県', 'Aichi', 35.180, 136.907, '中部'),

-- 関西
(24, '三重県', 'Mie', 34.730, 136.509, '関西'),
(25, '滋賀県', 'Shiga', 35.004, 135.869, '関西'),
(26, '京都府', 'Kyoto', 35.021, 135.756, '関西'),
(27, '大阪府', 'Osaka', 34.686, 135.520, '関西'),
(28, '兵庫県', 'Hyogo', 34.691, 135.183, '関西'),
(29, '奈良県', 'Nara', 34.685, 135.833, '関西'),
(30, '和歌山県', 'Wakayama', 34.226, 135.168, '関西'),

-- 中国
(31, '鳥取県', 'Tottori', 35.504, 134.238, '中国'),
(32, '島根県', 'Shimane', 35.472, 133.051, '中国'),
(33, '岡山県', 'Okayama', 34.662, 133.935, '中国'),
(34, '広島県', 'Hiroshima', 34.397, 132.460, '中国'),
(35, '山口県', 'Yamaguchi', 34.186, 131.471, '中国'),

-- 四国
(36, '徳島県', 'Tokushima', 34.066, 134.559, '四国'),
(37, '香川県', 'Kagawa', 34.340, 134.043, '四国'),
(38, '愛媛県', 'Ehime', 33.842, 132.766, '四国'),
(39, '高知県', 'Kochi', 33.560, 133.531, '四国'),

-- 九州・沖縄
(40, '福岡県', 'Fukuoka', 33.606, 130.418, '九州'),
(41, '佐賀県', 'Saga', 33.249, 130.299, '九州'),
(42, '長崎県', 'Nagasaki', 32.745, 129.874, '九州'),
(43, '熊本県', 'Kumamoto', 32.790, 130.742, '九州'),
(44, '大分県', 'Oita', 33.238, 131.613, '九州'),
(45, '宮崎県', 'Miyazaki', 31.911, 131.424, '九州'),
(46, '鹿児島県', 'Kagoshima', 31.560, 130.558, '九州'),
(47, '沖縄県', 'Okinawa', 26.212, 127.681, '沖縄');
```

---

### 2. データ投入の実行（11:00-12:00）

#### MySQL Workbenchで実行
1. `data.sql`を開く
2. 実行（⚡ボタン）
3. 確認
```sql
SELECT COUNT(*) FROM prefectures;
-- 結果: 47

SELECT * FROM prefectures ORDER BY id LIMIT 10;
```

---

## 午後の作業（13:00-17:00）

### 3. Spring Bootでの起動確認（13:00-14:00）

アプリケーションを起動して、自動的にデータが投入されることを確認

```bash
./gradlew bootRun
```

ログで確認：
```
Executing SQL script from URL [classpath:schema.sql]
Executing SQL script from URL [classpath:data.sql]
```

---

### 4. Repositoryでのデータ取得確認（14:00-16:00）

`PrefectureRepository.java`を作成：

```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.Prefecture;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PrefectureRepository extends JpaRepository<Prefecture, Long> {
    
    // 地域で検索
    List<Prefecture> findByRegion(String region);
    
    // 名前で検索
    Prefecture findByName(String name);
}
```

テスト用Controllerで確認：

```java
@RestController
@RequestMapping("/api/test")
public class TestController {
    
    @Autowired
    private PrefectureRepository prefectureRepository;
    
    @GetMapping("/prefectures")
    public List<Prefecture> getAllPrefectures() {
        return prefectureRepository.findAll();
    }
    
    @GetMapping("/prefectures/region/{region}")
    public List<Prefecture> getByRegion(@PathVariable String region) {
        return prefectureRepository.findByRegion(region);
    }
}
```

動作確認：
- http://localhost:8080/api/test/prefectures
- http://localhost:8080/api/test/prefectures/region/関東

---

### 5. ドキュメント作成（16:00-17:00）

`data-initialization-guide.md`を作成

---

## ✅ チェックリスト

- [ ] data.sql作成
- [ ] MySQLでデータ投入確認
- [ ] Spring Boot起動確認
- [ ] Repositoryでデータ取得確認
- [ ] ドキュメント作成
- [ ] GitHubにプッシュ

---

## 🆘 トラブルシューティング

### `Duplicate entry '1' for key 'PRIMARY'`
**原因:** 同じデータを2回投入しようとしている（再実行した）

**解決策:**
1. 先に `DELETE FROM テーブル名;` で空にしてから投入する（子テーブル → 親テーブルの順）
2. または `TRUNCATE` を使う場合は、外部キーのチェックを一時的に外す必要がある（慣れるまで `DELETE` が安全）

### 日本語が `????` になる／文字化けする
**原因:** DB・接続・ファイルのどこかで文字コードが `UTF-8` になっていない

**解決策:**
1. DBとテーブルが `utf8mb4` か確認（`SHOW CREATE TABLE prefectures;`）
2. JDBCのURLに `characterEncoding=UTF-8` を付ける
3. SQLファイルをUTF-8で保存し直す（Windowsのメモ帳は要注意。VS CodeやIntelliJで保存）

### `Cannot add or update a child row: a foreign key constraint fails`
**原因:** 親テーブルにまだ存在しないIDを、子テーブルで参照している

**解決策:**
1. 投入順を「親（prefectures）→ 子」にする
2. 子テーブルの `prefecture_id` が、親に実在するIDか確認

### `SELECT COUNT(*)` が47件にならない
**原因:** INSERT文の一部が実行されていない（区切りの誤り）

**解決策:**
1. 行の区切りは `,`、最後の行だけ `;` になっているか確認
2. 一部の文だけ選択して実行していないか確認（全体を選択して実行）
3. エラーが出た行は、出力パネルのメッセージで特定する

---

## 🎉 完了後

次は [Day 13](day-13.md) へ

お疲れさまでした！
