# Day 22: Controller層実装（Home）

## 📅 実施日
- 予定: Week 5 - Day 22
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
HomeControllerを実装し、トップページで47都道府県の一覧を表示する

---

## 📋 午前の作業（9:00-13:00）

### 1. Spring MVC Controllerの基礎理解（9:00-10:00）

**Controllerとは:**
- ユーザーのリクエストを受け取る入口
- ビジネスロジック（Service）を呼び出す
- 結果をViewに渡す

**MVCパターン:**

```
Browser（ユーザー）
    ↓ HTTPリクエスト
Controller（今日実装）
    ↓ ビジネスロジック呼び出し
Service
    ↓ データアクセス
Repository
    ↓ SQL
Database
    ↑ データ取得
Repository
    ↑ Entityを返却
Service
    ↑ DTOに変換
Controller
    ↓ ModelにDTOをセット
View（Thymeleaf）
    ↓ HTMLレンダリング
Browser（ユーザー）
```

**主要なアノテーション:**

```java
@Controller        // このクラスがControllerであることを示す
@GetMapping        // GETリクエストをマッピング
@PostMapping       // POSTリクエストをマッピング
@RequestParam      // クエリパラメータを受け取る
@PathVariable      // URLパスの一部を変数として受け取る
@ModelAttribute    // フォームデータをオブジェクトで受け取る
```

**学習用ドキュメント作成:**

`controller-guide.md`を作成：

```markdown
# Spring MVC Controller 実装ガイド

## 基本的なController

```java
@Controller
public class HomeController {
    
    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("message", "Hello World");
        return "index";  // templates/index.html を表示
    }
}
```

## Modelの使い方

Modelはビューにデータを渡すための入れ物。

```java
@GetMapping("/users")
public String listUsers(Model model) {
    List<User> users = userService.findAll();
    model.addAttribute("users", users);
    model.addAttribute("count", users.size());
    return "users/list";
}
```

Thymeleafで受け取る:

```html
<p>ユーザー数: <span th:text="${count}"></span></p>
<ul>
    <li th:each="user : ${users}" th:text="${user.name}"></li>
</ul>
```

## RequestParamの使い方

```java
@GetMapping("/search")
public String search(
    @RequestParam String keyword,           // 必須パラメータ
    @RequestParam(required = false) String category,  // 任意
    @RequestParam(defaultValue = "0") int page,       // デフォルト値
    Model model
) {
    // ?keyword=Java&category=tech&page=1
    return "search";
}
```

## PathVariableの使い方

```java
@GetMapping("/users/{id}")
public String showUser(
    @PathVariable Long id,
    Model model
) {
    User user = userService.findById(id);
    model.addAttribute("user", user);
    return "users/detail";
}
```

## リダイレクト

```java
@PostMapping("/users/create")
public String createUser(@ModelAttribute User user) {
    userService.save(user);
    return "redirect:/users";  // リダイレクト
}
```
```

---

### 2. HomeController実装（10:00-12:00）

**Controllerクラス作成:** `src/main/java/com/example/weatherapp/controller/HomeController.java`

```java
package com.example.weatherapp.controller;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.service.PrefectureService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Map;

/**
 * ホーム画面のController
 * トップページで47都道府県の一覧を表示
 */
@Controller
@Slf4j
public class HomeController {
    
    private final PrefectureService prefectureService;
    
    /**
     * コンストラクタインジェクション
     */
    public HomeController(PrefectureService prefectureService) {
        this.prefectureService = prefectureService;
    }
    
    /**
     * トップページ表示
     * 
     * URL: http://localhost:8080/
     * 
     * @param region 地域フィルタ（任意）
     * @param model ビューに渡すデータ
     * @return テンプレート名（index.html）
     */
    @GetMapping("/")
    public String index(
        @RequestParam(required = false) String region,
        Model model
    ) {
        log.info("トップページ表示: region={}", region);
        
        if (region != null && !region.isEmpty()) {
            // 地域フィルタが指定されている場合
            log.debug("地域フィルタ適用: {}", region);
            
            List<PrefectureDto> prefectures = prefectureService.findByRegion(region);
            model.addAttribute("prefectures", prefectures);
            model.addAttribute("selectedRegion", region);
            
        } else {
            // すべての都道府県を地域別にグループ化
            Map<String, List<PrefectureDto>> groupedPrefectures = 
                prefectureService.findAllGroupedByRegion();
            
            model.addAttribute("groupedPrefectures", groupedPrefectures);
        }
        
        // 地域リストをドロップダウン用に追加
        List<String> regions = List.of(
            "北海道", "東北", "関東", "中部", 
            "関西", "中国", "四国", "九州", "沖縄"
        );
        model.addAttribute("regions", regions);
        
        log.debug("モデルにデータを設定完了");
        
        return "index";  // templates/index.html
    }
    
    /**
     * ヘルスチェック用エンドポイント
     * 
     * URL: http://localhost:8080/health
     * 
     * @return ステータスメッセージ
     */
    @GetMapping("/health")
    public String health(Model model) {
        model.addAttribute("status", "OK");
        model.addAttribute("message", "Application is running");
        return "health";
    }
}
```

**実装のポイント:**

1. **@Controller**
   - Spring MVCのControllerとして登録
   - リクエストを受け取る窓口

2. **@GetMapping("/")**
   - ルートパス（`/`）へのGETリクエストをマッピング
   - `http://localhost:8080/` でアクセス可能

3. **@RequestParam(required = false)**
   - クエリパラメータを任意で受け取る
   - `?region=関東` のような指定に対応

4. **Model**
   - ビュー（HTML）にデータを渡すための入れ物
   - `model.addAttribute("key", value)` でデータを追加

5. **return "index"**
   - `templates/index.html` を表示
   - Thymeleafがレンダリング

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. HomeControllerのテスト作成（13:00-15:00）

`src/test/java/com/example/weatherapp/controller/HomeControllerTest.java`:

```java
package com.example.weatherapp.controller;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.service.PrefectureService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.*;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

/**
 * HomeControllerのテスト
 * 
 * @WebMvcTest: Controller層のみをテスト
 * MockMvcを使ってHTTPリクエストをシミュレート
 */
@WebMvcTest(HomeController.class)
class HomeControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private PrefectureService prefectureService;
    
    private PrefectureDto tokyo;
    private PrefectureDto osaka;
    private Map<String, List<PrefectureDto>> groupedPrefectures;
    
    @BeforeEach
    void setUp() {
        // テストデータ準備
        tokyo = PrefectureDto.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .region("関東")
            .build();
        
        osaka = PrefectureDto.builder()
            .id(27L)
            .name("大阪府")
            .nameEn("Osaka")
            .region("関西")
            .build();
        
        // 地域別グループ化データ
        groupedPrefectures = new LinkedHashMap<>();
        groupedPrefectures.put("関東", List.of(tokyo));
        groupedPrefectures.put("関西", List.of(osaka));
    }
    
    @Test
    @DisplayName("トップページが正しく表示される")
    void testIndex_NoFilter() throws Exception {
        // Given
        when(prefectureService.findAllGroupedByRegion())
            .thenReturn(groupedPrefectures);
        
        // When & Then
        mockMvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(view().name("index"))
            .andExpect(model().attributeExists("groupedPrefectures"))
            .andExpect(model().attributeExists("regions"))
            .andExpect(model().attribute("groupedPrefectures", groupedPrefectures));
        
        verify(prefectureService, times(1)).findAllGroupedByRegion();
    }
    
    @Test
    @DisplayName("地域フィルタが正しく動作する")
    void testIndex_WithRegionFilter() throws Exception {
        // Given
        List<PrefectureDto> kantoPrefectures = List.of(tokyo);
        when(prefectureService.findByRegion("関東"))
            .thenReturn(kantoPrefectures);
        
        // When & Then
        mockMvc.perform(get("/")
                .param("region", "関東"))
            .andExpect(status().isOk())
            .andExpect(view().name("index"))
            .andExpect(model().attributeExists("prefectures"))
            .andExpect(model().attribute("selectedRegion", "関東"))
            .andExpect(model().attribute("prefectures", hasSize(1)))
            .andExpect(model().attribute("prefectures", hasItem(
                hasProperty("name", is("東京都"))
            )));
        
        verify(prefectureService, times(1)).findByRegion("関東");
        verify(prefectureService, never()).findAllGroupedByRegion();
    }
    
    @Test
    @DisplayName("空文字列の地域フィルタは無視される")
    void testIndex_WithEmptyRegion() throws Exception {
        // Given
        when(prefectureService.findAllGroupedByRegion())
            .thenReturn(groupedPrefectures);
        
        // When & Then
        mockMvc.perform(get("/")
                .param("region", ""))
            .andExpect(status().isOk())
            .andExpect(model().attributeExists("groupedPrefectures"))
            .andExpect(model().attributeDoesNotExist("selectedRegion"));
        
        verify(prefectureService, times(1)).findAllGroupedByRegion();
    }
    
    @Test
    @DisplayName("ヘルスチェックエンドポイントが正しく動作する")
    void testHealth() throws Exception {
        mockMvc.perform(get("/health"))
            .andExpect(status().isOk())
            .andExpect(view().name("health"))
            .andExpect(model().attribute("status", "OK"))
            .andExpect(model().attribute("message", "Application is running"));
    }
}
```

**テストのポイント:**

1. **@WebMvcTest(HomeController.class)**
   - Controller層のみをテスト対象に
   - Service層はモック化
   - 軽量で高速なテスト

2. **MockMvc**
   - HTTPリクエストをシミュレート
   - `perform(get("/"))` でGETリクエスト送信
   - 実際のサーバー起動不要

3. **@MockBean**
   - PrefectureServiceをモック化
   - `when().thenReturn()` で振る舞いを定義

4. **andExpect()**
   - レスポンスの検証
   - status: HTTPステータスコード
   - view: 表示されるビュー名
   - model: モデルに設定された属性

5. **Hamcrest Matchers**
   - `hasSize()`: リストのサイズ検証
   - `hasItem()`: リストの要素検証
   - `hasProperty()`: オブジェクトのプロパティ検証

---

### 4. 簡易的なテンプレート作成（15:00-16:00）

動作確認用に簡易的なHTMLを作成：

`src/main/resources/templates/index.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>天気予報アプリ - トップページ</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: #4CAF50;
            color: white;
            padding: 20px;
            margin-bottom: 20px;
        }
        .filter {
            margin-bottom: 20px;
        }
        .region-group {
            margin-bottom: 30px;
        }
        .region-title {
            background: #f0f0f0;
            padding: 10px;
            font-weight: bold;
        }
        .prefecture-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            padding: 10px;
        }
        .prefecture-card {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
            cursor: pointer;
        }
        .prefecture-card:hover {
            background: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>全国天気予報</h1>
        <p>47都道府県の天気をチェック</p>
    </div>
    
    <!-- 地域フィルタ（任意機能） -->
    <div class="filter" th:if="${regions}">
        <form method="get">
            <label>地域で絞り込み:</label>
            <select name="region" onchange="this.form.submit()">
                <option value="">すべて</option>
                <option th:each="r : ${regions}" 
                        th:value="${r}" 
                        th:text="${r}"
                        th:selected="${r == selectedRegion}"></option>
            </select>
        </form>
    </div>
    
    <!-- 地域別グループ表示 -->
    <div th:if="${groupedPrefectures}">
        <div th:each="entry : ${groupedPrefectures}" class="region-group">
            <div class="region-title" th:text="${entry.key}"></div>
            <div class="prefecture-list">
                <div th:each="pref : ${entry.value}" class="prefecture-card">
                    <a th:href="@{/weather/{id}(id=${pref.id})}" th:text="${pref.name}"></a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- フィルタ適用時の表示 -->
    <div th:if="${prefectures}">
        <h2 th:text="${selectedRegion} + '地方'"></h2>
        <div class="prefecture-list">
            <div th:each="pref : ${prefectures}" class="prefecture-card">
                <a th:href="@{/weather/{id}(id=${pref.id})}" th:text="${pref.name}"></a>
            </div>
        </div>
    </div>
</body>
</html>
```

`src/main/resources/templates/health.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Health Check</title>
</head>
<body>
    <h1>Health Check</h1>
    <p>Status: <span th:text="${status}"></span></p>
    <p>Message: <span th:text="${message}"></span></p>
</body>
</html>
```

---

### 5. 動作確認（16:00-17:00）

**アプリケーション起動:**

```bash
./gradlew bootRun
```

**動作確認URL:**

1. **トップページ:** http://localhost:8080/
   - 全都道府県が地域別に表示される

2. **地域フィルタ:** http://localhost:8080/?region=関東
   - 関東地方のみ表示される

3. **ヘルスチェック:** http://localhost:8080/health
   - ステータス確認

**確認項目:**

- [ ] トップページが表示される
- [ ] 47都道府県がすべて表示される
- [ ] 地域別にグループ化されている
- [ ] 地域フィルタが動作する
- [ ] 各都道府県のリンクが正しい（`/weather/13` など）

**ログ確認:**

```
INFO  HomeController - トップページ表示: region=null
DEBUG HomeController - モデルにデータを設定完了
```

---

## ✅ チェックリスト

- [ ] Controllerの基礎を理解した
- [ ] HomeControllerを実装した
- [ ] 地域フィルタ機能を実装した
- [ ] MockMvcでテストを作成した
- [ ] すべてのテストがパスした
- [ ] 簡易的なHTMLで動作確認した
- [ ] ブラウザで表示確認した
- [ ] controller-guide.mdを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(controller): HomeControllerとテストを実装"
git push origin feature/day-22
```

---

## 📚 参考リンク

### Spring MVC
- [Spring MVC公式ドキュメント](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- [Controllerの書き方（日本語）](https://qiita.com/tag1216/items/3680b92cf96eb5a170f0)
- [@RequestParamの使い方（日本語）](https://qiita.com/NagaokaKenichi/items/c7556b93b9b4c53346e4)

### テスト
- [MockMvcの使い方（日本語）](https://qiita.com/rubytomato@github/items/f5c5c3e5c8c8d6c4e9c3)
- [@WebMvcTestの使い方（日本語）](https://qiita.com/disc99/items/31fa7abb724f63602dc9)
- [Hamcrest Matchersリファレンス](http://hamcrest.org/JavaHamcrest/javadoc/2.2/)

### Thymeleaf
- [Thymeleaf公式チュートリアル](https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html)
- [Thymeleaf基本文法（日本語）](https://qiita.com/NagaokaKenichi/items/c6d1b76090ef5ef39482)

---

## 🆘 トラブルシューティング

### テンプレートが見つからない
**症状:** `TemplateNotFoundException`

**原因:** テンプレートファイルが正しい場所にない

**解決策:**
1. `src/main/resources/templates/index.html` にファイルがあるか確認
2. ファイル名が正しいか確認（`return "index"` → `index.html`）

### モデルの属性が表示されない
**症状:** Thymeleafで `${groupedPrefectures}` が空

**原因:**
- Controllerで `model.addAttribute()` していない
- 属性名が一致していない

**解決策:**
```java
// Controller
model.addAttribute("groupedPrefectures", data);

// HTML
<div th:each="entry : ${groupedPrefectures}">
```

### テストが失敗する
**症状:** `NullPointerException` in test

**原因:** Serviceがモック化されていない

**解決策:**
```java
@MockBean
private PrefectureService prefectureService;

@BeforeEach
void setUp() {
    when(prefectureService.findAll()).thenReturn(...);
}
```

---

## 📝 本日のまとめ

`day-22-summary.md`を作成し、以下を記録：

1. **実装した機能:**
   - HomeController
   - 地域フィルタ機能
   - MockMvcテスト

2. **学んだこと:**
   - Spring MVCの基礎
   - Modelの使い方
   - @RequestParamの使い方
   - MockMvcでのテスト方法

3. **困難だった点:**

4. **明日への引き継ぎ:**
   - Day 23でWeatherController実装

---

## 🎉 完了後

次は [Day 23](day-23.md) でWeatherControllerを実装する

お疲れさまでした！
