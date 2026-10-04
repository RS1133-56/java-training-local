# Day 38: パフォーマンス最適化

## 📅 実施日
- 予定: Week 8 - Day 38
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
アプリケーションのパフォーマンスを測定し、最適化を実施してユーザー体験を向上させる

---

## 📋 午前の作業（9:00-13:00）

### 1. パフォーマンス測定（9:00-10:00）

**測定ツール:**

| ツール | 用途 |
|--------|------|
| Chrome DevTools | フロントエンド計測 |
| Lighthouse | 総合評価 |
| Spring Boot Actuator | バックエンド監視 |
| JMeter | 負荷テスト |

**パフォーマンス目標:**

| 指標 | 目標値 |
|------|--------|
| First Contentful Paint | < 1.8s |
| Time to Interactive | < 3.8s |
| Largest Contentful Paint | < 2.5s |
| API Response Time | < 200ms |
| Lighthouse Score | > 90 |

---

### 2. データベース最適化（10:00-11:30）

**インデックス追加:**

```sql
-- 都道府県検索用
CREATE INDEX idx_prefecture_name ON prefectures(name);
CREATE INDEX idx_prefecture_region ON prefectures(region);

-- 天気記録検索用
CREATE INDEX idx_weather_prefecture_id ON weather_records(prefecture_id);
CREATE INDEX idx_weather_fetched_at ON weather_records(fetched_at DESC);

-- 複合インデックス
CREATE INDEX idx_weather_pref_fetched 
ON weather_records(prefecture_id, fetched_at DESC);
```

**N+1問題対策:**

```java
@Service
public class PrefectureService {
    
    // Before: N+1問題
    public List<PrefectureDto> findAll() {
        List<Prefecture> prefectures = prefectureRepository.findAll();
        return prefectures.stream()
            .map(prefectureMapper::toDto)
            .collect(Collectors.toList());
    }
    
    // After: 最適化
    @Transactional(readOnly = true)
    public List<PrefectureDto> findAll() {
        // 一括取得でクエリ数削減
        List<Prefecture> prefectures = prefectureRepository.findAll();
        return prefectures.stream()
            .map(prefectureMapper::toDto)
            .collect(Collectors.toList());
    }
}
```

**クエリ最適化:**

```java
@Repository
public interface WeatherRecordRepository extends JpaRepository<WeatherRecord, Long> {
    
    // ページネーション対応
    @Query("SELECT w FROM WeatherRecord w " +
           "WHERE w.prefecture.id = :prefectureId " +
           "ORDER BY w.fetchedAt DESC")
    Page<WeatherRecord> findByPrefectureIdOrderByFetchedAtDesc(
        @Param("prefectureId") Long prefectureId,
        Pageable pageable
    );
    
    // 必要なカラムのみ取得
    @Query("SELECT new com.example.weatherapp.dto.WeatherSummaryDto(" +
           "w.id, w.prefecture.name, w.currentTemperature, w.fetchedAt) " +
           "FROM WeatherRecord w " +
           "WHERE w.prefecture.region = :region")
    List<WeatherSummaryDto> findSummaryByRegion(@Param("region") String region);
}
```

---

### 3. キャッシュ実装（11:30-12:30）

**Spring Cache設定:**

```java
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager(
            "prefectures", "weather", "regions"
        );
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .recordStats());
        return cacheManager;
    }
}
```

**キャッシュ適用:**

```java
@Service
public class PrefectureService {
    
    @Cacheable(value = "prefectures", key = "#id")
    public PrefectureDto findById(Long id) {
        Prefecture prefecture = prefectureRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("都道府県が見つかりません"));
        return prefectureMapper.toDto(prefecture);
    }
    
    @Cacheable(value = "prefectures")
    public List<PrefectureDto> findAll() {
        return prefectureRepository.findAll().stream()
            .map(prefectureMapper::toDto)
            .collect(Collectors.toList());
    }
    
    @CacheEvict(value = "prefectures", allEntries = true)
    public void clearCache() {
        // キャッシュクリア
    }
}
```

**天気データキャッシュ:**

```java
@Service
public class WeatherService {
    
    @Cacheable(
        value = "weather",
        key = "#prefectureId",
        unless = "#result == null"
    )
    public WeatherDetailDto getWeatherByPrefectureId(Long prefectureId) {
        // API呼び出しをキャッシュ
        // 10分間は同じデータを返す
    }
}
```

---

### 昼休憩（12:30-13:30）

---

## 📋 午後の作業（13:30-17:00）

### 4. フロントエンド最適化（13:30-15:00）

**CSS最適化:**

```css
/* Before: 複数回定義 */
.card { background: white; }
.prefecture-card { background: white; }
.weather-card { background: white; }

/* After: 共通化 */
.card,
.prefecture-card,
.weather-card {
    background: white;
}

/* CSSスプライト */
.icon {
    background-image: url('/images/sprites.png');
    background-repeat: no-repeat;
}

.icon-sun { background-position: 0 0; }
.icon-cloud { background-position: -32px 0; }
```

**JavaScript最適化:**

```javascript
// Before: 毎回DOM検索
function updateCards() {
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('active');
    });
}

// After: DOM検索を1回に
const cards = document.querySelectorAll('.card');
function updateCards() {
    cards.forEach(card => {
        card.classList.add('active');
    });
}

// デバウンス実装
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 検索にデバウンス適用
const debouncedSearch = debounce(filterPrefectures, 300);
searchInput.addEventListener('input', debouncedSearch);
```

**画像最適化:**

```html
<!-- WebP形式使用 -->
<picture>
    <source srcset="/images/weather.webp" type="image/webp">
    <source srcset="/images/weather.jpg" type="image/jpeg">
    <img src="/images/weather.jpg" alt="天気">
</picture>

<!-- 遅延読み込み -->
<img src="/images/placeholder.jpg" 
     data-src="/images/weather.jpg"
     class="lazy-load"
     loading="lazy"
     alt="天気">

<!-- レスポンシブ画像 -->
<img srcset="/images/weather-320w.jpg 320w,
             /images/weather-640w.jpg 640w,
             /images/weather-1280w.jpg 1280w"
     sizes="(max-width: 640px) 100vw, 640px"
     src="/images/weather-640w.jpg"
     alt="天気">
```

---

### 5. 静的リソース最適化（15:00-16:00）

**圧縮設定:**

`application.properties`:

```properties
# Gzip圧縮有効化
server.compression.enabled=true
server.compression.mime-types=text/html,text/xml,text/plain,text/css,text/javascript,application/javascript,application/json
server.compression.min-response-size=1024

# 静的リソースキャッシュ
spring.web.resources.cache.cachecontrol.max-age=31536000
spring.web.resources.cache.cachecontrol.cache-public=true
```

**ファイル結合・圧縮:**

```gradle
// build.gradle
plugins {
    id 'com.github.node-gradle.node' version '3.5.0'
}

task compressCss(type: NpmTask) {
    args = ['run', 'css:minify']
}

task compressJs(type: NpmTask) {
    args = ['run', 'js:minify']
}
```

**package.json:**

```json
{
  "scripts": {
    "css:minify": "cleancss -o static/css/all.min.css static/css/*.css",
    "js:minify": "uglifyjs static/js/*.js -o static/js/all.min.js"
  }
}
```

---

### 6. パフォーマンス計測（16:00-17:00）

**Lighthouseレポート取得:**

```bash
# Chrome DevTools > Lighthouse > Generate report
```

**パフォーマンステスト:**

```java
@Test
@DisplayName("API応答時間計測")
void testApiResponseTime() throws Exception {
    long startTime = System.currentTimeMillis();
    
    mockMvc.perform(get("/weather/13"))
        .andExpect(status().isOk());
    
    long endTime = System.currentTimeMillis();
    long responseTime = endTime - startTime;
    
    System.out.println("応答時間: " + responseTime + "ms");
    assertThat(responseTime).isLessThan(200);
}
```

**最適化前後の比較:**

`performance-report.md`:

```markdown
# パフォーマンス最適化レポート

## 測定結果

### Lighthouseスコア

| 項目 | 最適化前 | 最適化後 | 改善 |
|------|---------|---------|------|
| Performance | 75 | 92 | +17 |
| Accessibility | 85 | 95 | +10 |
| Best Practices | 80 | 95 | +15 |
| SEO | 90 | 100 | +10 |

### ページロード時間

| 指標 | 最適化前 | 最適化後 | 改善率 |
|------|---------|---------|--------|
| FCP | 2.5s | 1.2s | 52% |
| LCP | 4.2s | 2.1s | 50% |
| TTI | 5.8s | 3.2s | 45% |
| TBT | 450ms | 180ms | 60% |

### API応答時間

| エンドポイント | 最適化前 | 最適化後 |
|---------------|---------|---------|
| GET / | 320ms | 85ms |
| GET /weather/{id} | 580ms | 150ms |

## 実施した最適化

### バックエンド
- ✅ データベースインデックス追加
- ✅ N+1問題解消
- ✅ クエリ最適化
- ✅ キャッシュ導入

### フロントエンド
- ✅ CSS/JS圧縮
- ✅ 画像最適化
- ✅ 遅延読み込み
- ✅ デバウンス実装

### インフラ
- ✅ Gzip圧縮有効化
- ✅ 静的リソースキャッシュ
- ✅ HTTP/2有効化

## 結論

全項目で目標値を達成し、ユーザー体験が大幅に向上しました。
```

---

## ✅ チェックリスト

- [ ] パフォーマンス測定を実施した
- [ ] データベースを最適化した
- [ ] キャッシュを実装した
- [ ] フロントエンドを最適化した
- [ ] 静的リソースを最適化した
- [ ] Lighthouse 90点以上を達成した
- [ ] API応答時間200ms以下を達成した
- [ ] パフォーマンスレポートを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "perf: パフォーマンス最適化完了"
git push origin feature/day-38
```

---

## 📚 参考リンク

### パフォーマンス測定
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [WebPageTest](https://www.webpagetest.org/)

### 最適化
- [Web.dev（パフォーマンス）](https://web.dev/performance/)
- [Spring Boot Performance](https://spring.io/guides/gs/performance/)

### キャッシュ
- [Caffeine Cache](https://github.com/ben-manes/caffeine)
- [Spring Cache](https://spring.pleiades.io/spring-boot/docs/current/reference/html/io.html#io.caching)

---

## 🆘 トラブルシューティング

### キャッシュが効かない
**原因:** @Cacheableの条件が合わない

**解決策:** unless条件を確認

### 画像が表示されない
**原因:** WebP非対応ブラウザ

**解決策:** pictureタグでフォールバック

---

## 📝 本日のまとめ

1. **実施した最適化:**
   - データベース最適化
   - キャッシュ導入
   - フロントエンド最適化
   - 静的リソース最適化

2. **達成した成果:**
   - Lighthouse 92点
   - ページロード50%改善
   - API応答時間60%改善

3. **明日への引き継ぎ:**
   - Day 39で最終レビュー

---

## 🎉 完了後

次は [Day 39](day-39.md) へ

お疲れさまでした！
