# Day 27: トップページ実装（index.html）

## 📅 実施日
- 予定: Week 6 - Day 27
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
47都道府県を表示するトップページ（index.html）を実装し、地域別グループ化と検索機能を追加する

---

## 📋 午前の作業（9:00-13:00）

### 1. トップページの設計（9:00-9:30）

**表示する内容:**
1. ヘッダー（タイトル、説明）
2. 検索・フィルタ機能
3. 47都道府県のカード表示（地域別グループ）
4. 各都道府県へのリンク

**レイアウト構成:**

```
+----------------------------------+
|         ヘッダー                  |
|  天気予報アプリ                   |
+----------------------------------+
|    検索バー | 地域フィルタ         |
+----------------------------------+
|                                  |
|  【北海道】                       |
|  [北海道]                        |
|                                  |
|  【東北】                         |
|  [青森] [岩手] [宮城] ...        |
|                                  |
|  【関東】                         |
|  [東京] [神奈川] [埼玉] ...      |
|                                  |
+----------------------------------+
|         フッター                  |
+----------------------------------+
```

---

### 2. index.html実装（9:30-12:00）

`src/main/resources/templates/index.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('全国天気予報')}"></head>
<body>
    <!-- ナビゲーション -->
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <!-- メインコンテンツ -->
    <div class="container">
        <!-- ヘッダーセクション -->
        <header class="page-header">
            <h1>🌤️ 全国天気予報</h1>
            <p class="subtitle">47都道府県の天気情報をチェック</p>
        </header>
        
        <!-- 検索・フィルタセクション -->
        <div class="search-filter-section">
            <!-- 検索ボックス -->
            <div class="search-box">
                <input type="text" 
                       id="searchInput" 
                       placeholder="都道府県名で検索..."
                       onkeyup="filterPrefectures()">
            </div>
            
            <!-- 地域フィルタ -->
            <div class="region-filter">
                <form method="get" action="/">
                    <label for="regionSelect">地域で絞り込み:</label>
                    <select name="region" 
                            id="regionSelect" 
                            onchange="this.form.submit()">
                        <option value="">すべての地域</option>
                        <option th:each="r : ${regions}" 
                                th:value="${r}" 
                                th:text="${r}"
                                th:selected="${r == selectedRegion}">
                        </option>
                    </select>
                </form>
            </div>
            
            <!-- フィルタリセット -->
            <div class="filter-reset" th:if="${selectedRegion}">
                <a th:href="@{/}" class="btn-reset">
                    フィルタをクリア
                </a>
            </div>
        </div>
        
        <!-- 地域別グループ表示 -->
        <div class="prefectures-container" th:if="${groupedPrefectures}">
            <div th:each="entry : ${groupedPrefectures}" 
                 class="region-group"
                 th:attr="data-region=${entry.key}">
                
                <!-- 地域名 -->
                <h2 class="region-title" th:text="${entry.key}"></h2>
                
                <!-- 都道府県カード -->
                <div class="prefecture-grid">
                    <div th:each="pref : ${entry.value}" 
                         class="prefecture-card"
                         th:attr="data-name=${pref.name}">
                        
                        <a th:href="@{/weather/{id}(id=${pref.id})}" 
                           class="card-link">
                            
                            <!-- 都道府県名 -->
                            <h3 class="prefecture-name" th:text="${pref.name}"></h3>
                            
                            <!-- 英語名 -->
                            <p class="prefecture-name-en" th:text="${pref.nameEn}"></p>
                            
                            <!-- 座標情報（デバッグ用・後で削除可） -->
                            <div class="prefecture-info">
                                <span class="info-item">
                                    緯度: <span th:text="${#numbers.formatDecimal(pref.latitude, 1, 3)}"></span>
                                </span>
                                <span class="info-item">
                                    経度: <span th:text="${#numbers.formatDecimal(pref.longitude, 1, 3)}"></span>
                                </span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- フィルタ結果表示（地域フィルタ適用時） -->
        <div class="prefectures-container" th:if="${prefectures}">
            <div class="region-group">
                <h2 class="region-title">
                    <span th:text="${selectedRegion}"></span>地方
                    (<span th:text="${#lists.size(prefectures)}"></span>件)
                </h2>
                
                <div class="prefecture-grid">
                    <div th:each="pref : ${prefectures}" 
                         class="prefecture-card"
                         th:attr="data-name=${pref.name}">
                        
                        <a th:href="@{/weather/{id}(id=${pref.id})}" 
                           class="card-link">
                            <h3 class="prefecture-name" th:text="${pref.name}"></h3>
                            <p class="prefecture-name-en" th:text="${pref.nameEn}"></p>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- データがない場合 -->
        <div class="no-data" 
             th:if="${groupedPrefectures == null and prefectures == null}">
            <p>データが見つかりませんでした。</p>
        </div>
    </div>
    
    <!-- フッター -->
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <!-- JavaScript -->
    <script>
        /**
         * 都道府県名でフィルタリング
         */
        function filterPrefectures() {
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const cards = document.querySelectorAll('.prefecture-card');
            
            cards.forEach(card => {
                const name = card.getAttribute('data-name').toLowerCase();
                if (name.includes(filter)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
            
            // 地域グループの表示制御
            updateRegionVisibility();
        }
        
        /**
         * 空の地域グループを非表示
         */
        function updateRegionVisibility() {
            const regionGroups = document.querySelectorAll('.region-group');
            
            regionGroups.forEach(group => {
                const visibleCards = group.querySelectorAll(
                    '.prefecture-card[style*="display: none"]'
                ).length;
                
                const totalCards = group.querySelectorAll('.prefecture-card').length;
                
                if (visibleCards === totalCards) {
                    group.style.display = 'none';
                } else {
                    group.style.display = '';
                }
            });
        }
    </script>
    
    <style>
        /* ページヘッダー */
        .page-header {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .page-header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 18px;
            opacity: 0.9;
        }
        
        /* 検索・フィルタセクション */
        .search-filter-section {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .search-box {
            flex: 1;
            min-width: 250px;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            transition: border-color 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .region-filter {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .region-filter select {
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
            cursor: pointer;
        }
        
        .btn-reset {
            padding: 12px 24px;
            background: #e74c3c;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s;
        }
        
        .btn-reset:hover {
            background: #c0392b;
        }
        
        /* 地域グループ */
        .region-group {
            margin-bottom: 40px;
        }
        
        .region-title {
            font-size: 24px;
            color: #2c3e50;
            padding: 10px 20px;
            background: #ecf0f1;
            border-left: 5px solid #3498db;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        /* 都道府県グリッド */
        .prefecture-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 15px;
        }
        
        /* 都道府県カード */
        .prefecture-card {
            background: white;
            border: 2px solid #e1e8ed;
            border-radius: 10px;
            transition: all 0.3s;
            overflow: hidden;
        }
        
        .prefecture-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            border-color: #3498db;
        }
        
        .card-link {
            display: block;
            padding: 20px;
            text-decoration: none;
            color: inherit;
        }
        
        .prefecture-name {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .prefecture-name-en {
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        
        .prefecture-info {
            font-size: 12px;
            color: #95a5a6;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        
        /* データなし */
        .no-data {
            text-align: center;
            padding: 60px 20px;
            color: #95a5a6;
            font-size: 18px;
        }
        
        /* レスポンシブ */
        @media (max-width: 768px) {
            .page-header h1 {
                font-size: 28px;
            }
            
            .prefecture-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
                gap: 10px;
            }
            
            .search-filter-section {
                flex-direction: column;
            }
            
            .search-box {
                width: 100%;
            }
        }
    </style>
</body>
</html>
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. HomeControllerの更新（13:00-14:00）

すでに実装済みのHomeControllerで対応済み。念のため確認：

```java
@GetMapping("/")
public String index(
    @RequestParam(required = false) String region,
    Model model
) {
    if (region != null && !region.isEmpty()) {
        List<PrefectureDto> prefectures = prefectureService.findByRegion(region);
        model.addAttribute("prefectures", prefectures);
        model.addAttribute("selectedRegion", region);
    } else {
        Map<String, List<PrefectureDto>> groupedPrefectures = 
            prefectureService.findAllGroupedByRegion();
        model.addAttribute("groupedPrefectures", groupedPrefectures);
    }
    
    List<String> regions = List.of(
        "北海道", "東北", "関東", "中部", 
        "関西", "中国", "四国", "九州", "沖縄"
    );
    model.addAttribute("regions", regions);
    
    return "index";
}
```

---

### 4. UI改善とインタラクション追加（14:00-16:00）

**ローディング表示追加:**

index.htmlに追加：

```html
<!-- ローディング表示 -->
<div id="loading" style="display: none;">
    <div class="loading-overlay">
        <div class="spinner"></div>
        <p>読み込み中...</p>
    </div>
</div>

<style>
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    color: white;
}

.spinner {
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid white;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<script>
// リンククリック時にローディング表示
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.card-link');
    const loading = document.getElementById('loading');
    
    links.forEach(link => {
        link.addEventListener('click', function() {
            loading.style.display = 'block';
        });
    });
});
</script>
```

**カードホバーエフェクト強化:**

```css
.prefecture-card {
    position: relative;
    background: white;
    border: 2px solid #e1e8ed;
    border-radius: 10px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}

.prefecture-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    opacity: 0;
    transition: opacity 0.3s;
    z-index: -1;
}

.prefecture-card:hover::before {
    opacity: 0.1;
}

.prefecture-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    border-color: #667eea;
}
```

---

### 5. 動作確認とテスト（16:00-17:00）

**ブラウザで確認:**

1. http://localhost:8080/ にアクセス
2. 47都道府県が地域別に表示されることを確認
3. 検索ボックスで「東京」と入力 → 東京都のみ表示
4. 地域フィルタで「関東」を選択 → 関東7県のみ表示
5. 都道府県カードをクリック → 天気詳細ページに遷移
6. レスポンシブ対応確認（ブラウザ幅を変更）

**テストケース:**

`src/test/java/com/example/weatherapp/controller/HomeControllerE2ETest.java`:

```java
package com.example.weatherapp.controller;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

/**
 * トップページのE2Eテスト
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@Sql("/test-data.sql")
class HomeControllerE2ETest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    @DisplayName("トップページが正しく表示される")
    void testIndexPage() throws Exception {
        mockMvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(view().name("index"))
            .andExpect(content().string(containsString("全国天気予報")))
            .andExpect(content().string(containsString("北海道")))
            .andExpect(content().string(containsString("東京都")))
            .andExpect(content().string(containsString("沖縄県")));
    }
    
    @Test
    @DisplayName("地域フィルタが動作する")
    void testRegionFilter() throws Exception {
        mockMvc.perform(get("/").param("region", "関東"))
            .andExpect(status().isOk())
            .andExpect(model().attribute("selectedRegion", "関東"))
            .andExpect(content().string(containsString("東京都")))
            .andExpect(content().string(containsString("神奈川県")));
    }
}
```

---

## ✅ チェックリスト

- [ ] index.htmlを実装した
- [ ] 47都道府県が地域別に表示される
- [ ] 検索機能が動作する
- [ ] 地域フィルタが動作する
- [ ] レスポンシブデザイン対応
- [ ] ローディング表示を実装した
- [ ] ホバーエフェクトを実装した
- [ ] E2Eテストを作成した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): トップページ（index.html）実装"
git push origin main
```

---

## 📚 参考リンク

### CSS Grid
- [CSS Grid完全ガイド（日本語）](https://coliss.com/articles/build-websites/operation/css/css-grid-layout-guide.html)
- [Grid Layout公式](https://developer.mozilla.org/ja/docs/Web/CSS/CSS_Grid_Layout)

### JavaScript
- [JavaScript基礎（日本語）](https://developer.mozilla.org/ja/docs/Web/JavaScript/Guide)
- [DOM操作（日本語）](https://qiita.com/kouh/items/dfc14d25ccb4e50afe89)

### レスポンシブデザイン
- [レスポンシブデザイン基礎（日本語）](https://qiita.com/mrd-takahashi/items/b82a5c452fa5e41e33f4)

---

## 🆘 トラブルシューティング

### 都道府県が表示されない
**症状:** カードが1つも表示されない

**原因:**
- DBにデータがない
- Controllerでモデルに追加していない

**解決策:**
```sql
-- test-data.sqlを実行
./gradlew bootRun --args='--spring.jpa.hibernate.ddl-auto=none'
```

### 検索が動作しない
**症状:** 検索ボックスに入力しても何も起きない

**原因:** JavaScriptが読み込まれていない

**解決策:**
```html
<!-- </body>の直前に配置 -->
<script>
function filterPrefectures() { ... }
</script>
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - トップページ（index.html）
   - 地域別グループ表示
   - 検索・フィルタ機能
   - レスポンシブデザイン

2. **学んだこと:**
   - CSS Gridレイアウト
   - JavaScript DOM操作
   - Thymeleaf実践

3. **明日への引き継ぎ:**
   - Day 28で天気詳細ページ実装

---

## 🎉 完了後

次は [Day 28](day-28.md) へ

お疲れさまでした！
