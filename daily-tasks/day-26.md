# Day 26: Thymeleafテンプレート基礎

## 📅 実施日
- 予定: Week 6 - Day 26
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Thymeleafテンプレートエンジンの基本文法を習得し、動的なHTMLページを作成できるようになる

---

## 📋 午前の作業（9:00-13:00）

### 1. Thymeleafの基礎理解（9:00-10:00）

**Thymeleafとは:**
- Springが推奨するテンプレートエンジン
- HTMLにサーバーサイドの動的データを埋め込む
- 自然なHTMLテンプレート（Natural Templates）

**テンプレートエンジンの仕組み:**

```
Controller
    ↓ Model（データ）
Thymeleaf
    ↓ HTMLにデータを埋め込み
Browser
```

**主要な属性:**

| 属性 | 用途 | 例 |
|------|------|-----|
| th:text | テキスト表示 | `<p th:text="${message}"></p>` |
| th:each | 繰り返し | `<li th:each="item : ${items}"></li>` |
| th:if | 条件分岐 | `<div th:if="${user != null}"></div>` |
| th:href | リンク | `<a th:href="@{/path}"></a>` |
| th:src | 画像 | `<img th:src="@{/img/logo.png}">` |
| th:object | フォームオブジェクト | `<form th:object="${user}"></form>` |
| th:field | フォームフィールド | `<input th:field="*{name}">` |

**学習用ドキュメント作成:**

`thymeleaf-guide.md`を作成：

```markdown
# Thymeleaf 基本ガイド

## 1. テキスト表示（th:text）

```html
<!-- Controller -->
model.addAttribute("username", "太郎");

<!-- HTML -->
<p th:text="${username}">ダミーテキスト</p>

<!-- 結果 -->
<p>太郎</p>
```

**HTMLエスケープ:**
- `th:text`: エスケープする（安全）
- `th:utext`: エスケープしない（XSS注意）

## 2. 繰り返し（th:each）

```html
<!-- Controller -->
List<String> fruits = List.of("りんご", "バナナ", "みかん");
model.addAttribute("fruits", fruits);

<!-- HTML -->
<ul>
    <li th:each="fruit : ${fruits}" th:text="${fruit}"></li>
</ul>

<!-- 結果 -->
<ul>
    <li>りんご</li>
    <li>バナナ</li>
    <li>みかん</li>
</ul>
```

**繰り返しステータス:**

```html
<li th:each="item, stat : ${items}">
    インデックス: <span th:text="${stat.index}"></span>
    カウント: <span th:text="${stat.count}"></span>
    最初?: <span th:text="${stat.first}"></span>
    最後?: <span th:text="${stat.last}"></span>
</li>
```

## 3. 条件分岐（th:if / th:unless）

```html
<!-- Controller -->
model.addAttribute("isLoggedIn", true);

<!-- HTML -->
<div th:if="${isLoggedIn}">
    ようこそ、ログイン中です
</div>

<div th:unless="${isLoggedIn}">
    ログインしてください
</div>
```

**th:switchによる複数分岐:**

```html
<div th:switch="${user.role}">
    <p th:case="'admin'">管理者</p>
    <p th:case="'user'">一般ユーザー</p>
    <p th:case="*">ゲスト</p>
</div>
```

## 4. URL式（@{...}）

```html
<!-- 絶対パス -->
<a th:href="@{/weather/13}">東京の天気</a>

<!-- パラメータ付き -->
<a th:href="@{/search(keyword='天気')}">検索</a>
<!-- 結果: /search?keyword=天気 -->

<!-- パスパラメータ -->
<a th:href="@{/weather/{id}(id=${prefecture.id})}">詳細</a>
<!-- 結果: /weather/13 -->
```

## 5. オブジェクトのプロパティアクセス

```html
<!-- Controller -->
Prefecture prefecture = new Prefecture();
prefecture.setName("東京都");
model.addAttribute("pref", prefecture);

<!-- HTML -->
<p th:text="${pref.name}">都道府県名</p>
<!-- または -->
<p th:text="${pref.getName()}">都道府県名</p>
```

## 6. 日付フォーマット（#temporals）

```html
<!-- Controller -->
model.addAttribute("now", LocalDateTime.now());

<!-- HTML -->
<p th:text="${#temporals.format(now, 'yyyy/MM/dd HH:mm')}"></p>
<!-- 結果: 2024/01/05 15:30 -->
```

## 7. 数値フォーマット（#numbers）

```html
<!-- Controller -->
model.addAttribute("temperature", 15.678);

<!-- HTML -->
<p th:text="${#numbers.formatDecimal(temperature, 1, 1)}"></p>
<!-- 結果: 15.7 -->
```

## 8. フラグメント（共通部品）

**header.html:**
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <title th:text="${title}">タイトル</title>
</head>
</html>
```

**使用側:**
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{header :: head('トップページ')}"></head>
<body>
    コンテンツ
</body>
</html>
```
```

---

### 2. 基本構文の実践（10:00-12:00）

**練習用ページ作成:** `src/main/resources/templates/practice/thymeleaf-basic.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Thymeleaf基礎練習</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
        }
        .section {
            border: 1px solid #ddd;
            padding: 20px;
            margin: 20px 0;
            background: #f9f9f9;
        }
        .section h2 {
            margin-top: 0;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background: #3498db;
            color: white;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
        }
        .badge-first {
            background: #e74c3c;
            color: white;
        }
        .badge-last {
            background: #3498db;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Thymeleaf基礎練習ページ</h1>
    
    <!-- 1. テキスト表示 -->
    <div class="section">
        <h2>1. テキスト表示（th:text）</h2>
        <p>メッセージ: <span th:text="${message}">ここにメッセージが表示されます</span></p>
        <p>ユーザー名: <span th:text="${username}">ゲスト</span></p>
    </div>
    
    <!-- 2. 繰り返し -->
    <div class="section">
        <h2>2. 繰り返し（th:each）</h2>
        <h3>都道府県リスト</h3>
        <ul>
            <li th:each="pref : ${prefectures}" th:text="${pref.name}"></li>
        </ul>
        
        <h3>繰り返しステータス</h3>
        <table>
            <thead>
                <tr>
                    <th>インデックス</th>
                    <th>カウント</th>
                    <th>都道府県名</th>
                    <th>ステータス</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="pref, stat : ${prefectures}">
                    <td th:text="${stat.index}"></td>
                    <td th:text="${stat.count}"></td>
                    <td th:text="${pref.name}"></td>
                    <td>
                        <span th:if="${stat.first}" class="badge badge-first">最初</span>
                        <span th:if="${stat.last}" class="badge badge-last">最後</span>
                        <span th:unless="${stat.first or stat.last}">-</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <!-- 3. 条件分岐 -->
    <div class="section">
        <h2>3. 条件分岐（th:if / th:unless）</h2>
        
        <div th:if="${isLoggedIn}">
            <p style="color: green;">✓ ログイン中です</p>
        </div>
        
        <div th:unless="${isLoggedIn}">
            <p style="color: red;">✗ ログインしていません</p>
        </div>
        
        <h3>th:switch による分岐</h3>
        <div th:switch="${userRole}">
            <p th:case="'admin'" style="color: red;">管理者権限</p>
            <p th:case="'moderator'" style="color: orange;">モデレーター権限</p>
            <p th:case="'user'" style="color: blue;">一般ユーザー</p>
            <p th:case="*" style="color: gray;">ゲスト</p>
        </div>
    </div>
    
    <!-- 4. URL生成 -->
    <div class="section">
        <h2>4. URL生成（@{...}）</h2>
        
        <h3>リンク集</h3>
        <ul>
            <li><a th:href="@{/}">トップページ</a></li>
            <li><a th:href="@{/weather/13}">東京の天気</a></li>
            <li>
                <a th:href="@{/weather/{id}(id=${samplePrefectureId})}">
                    パスパラメータの例
                </a>
            </li>
            <li>
                <a th:href="@{/(region='関東')}">
                    クエリパラメータの例
                </a>
            </li>
        </ul>
    </div>
    
    <!-- 5. 日付・時刻フォーマット -->
    <div class="section">
        <h2>5. 日付・時刻フォーマット（#temporals）</h2>
        <p>現在日時: <span th:text="${#temporals.format(now, 'yyyy年MM月dd日 HH:mm:ss')}"></span></p>
        <p>日付のみ: <span th:text="${#temporals.format(now, 'yyyy/MM/dd')}"></span></p>
        <p>時刻のみ: <span th:text="${#temporals.format(now, 'HH:mm')}"></span></p>
    </div>
    
    <!-- 6. 数値フォーマット -->
    <div class="section">
        <h2>6. 数値フォーマット（#numbers）</h2>
        <p>気温: <span th:text="${temperature}"></span>℃</p>
        <p>気温（小数点1桁）: <span th:text="${#numbers.formatDecimal(temperature, 1, 1)}"></span>℃</p>
        <p>湿度: <span th:text="${humidity}"></span>%</p>
    </div>
    
    <!-- 7. Elvis演算子（デフォルト値） -->
    <div class="section">
        <h2>7. Elvis演算子（?:）</h2>
        <p>ニックネーム: <span th:text="${nickname} ?: '未設定'"></span></p>
        <p>説明: <span th:text="${description} ?: 'データがありません'"></span></p>
    </div>
    
    <!-- 8. セーフナビゲーション -->
    <div class="section">
        <h2>8. セーフナビゲーション（?.）</h2>
        <p>都道府県名: <span th:text="${prefecture?.name} ?: '未選択'"></span></p>
        <p>地域: <span th:text="${prefecture?.region} ?: '未選択'"></span></p>
    </div>
    
    <div style="margin-top: 40px; text-align: center;">
        <a th:href="@{/}">トップページに戻る</a>
    </div>
</body>
</html>
```

**練習用Controller:** `src/main/java/com/example/weatherapp/controller/PracticeController.java`

```java
package com.example.weatherapp.controller;

import com.example.weatherapp.dto.PrefectureDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

/**
 * Thymeleaf練習用Controller
 */
@Controller
@RequestMapping("/practice")
@Slf4j
public class PracticeController {
    
    @GetMapping("/thymeleaf-basic")
    public String thymeleafBasic(Model model) {
        log.info("Thymeleaf基礎練習ページ表示");
        
        // 1. テキスト表示用
        model.addAttribute("message", "Thymeleafへようこそ！");
        model.addAttribute("username", "山田太郎");
        
        // 2. 繰り返し用
        List<PrefectureDto> prefectures = Arrays.asList(
            PrefectureDto.builder().id(13L).name("東京都").region("関東").build(),
            PrefectureDto.builder().id(27L).name("大阪府").region("関西").build(),
            PrefectureDto.builder().id(1L).name("北海道").region("北海道").build()
        );
        model.addAttribute("prefectures", prefectures);
        
        // 3. 条件分岐用
        model.addAttribute("isLoggedIn", true);
        model.addAttribute("userRole", "admin");
        
        // 4. URL生成用
        model.addAttribute("samplePrefectureId", 13L);
        
        // 5. 日付フォーマット用
        model.addAttribute("now", LocalDateTime.now());
        
        // 6. 数値フォーマット用
        model.addAttribute("temperature", 15.678);
        model.addAttribute("humidity", 65);
        
        // 7. Elvis演算子用
        model.addAttribute("nickname", null);  // nullの場合のテスト
        
        // 8. セーフナビゲーション用
        model.addAttribute("prefecture", null);  // nullの場合のテスト
        
        return "practice/thymeleaf-basic";
    }
}
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. レイアウト・フラグメント実践（13:00-15:00）

**共通ヘッダー:** `src/main/resources/templates/fragments/header.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title th:text="${title}">天気予報アプリ</title>
    
    <!-- 共通CSS -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
                         Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
    </style>
</head>
</html>
```

**共通ナビゲーション:** `src/main/resources/templates/fragments/navbar.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<body>
    <nav th:fragment="navbar" class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a th:href="@{/}">🌤️ 天気予報アプリ</a>
            </div>
            <ul class="nav-menu">
                <li><a th:href="@{/}">ホーム</a></li>
                <li><a th:href="@{/practice/thymeleaf-basic}">練習</a></li>
            </ul>
        </div>
    </nav>
    
    <style>
        .navbar {
            background: #3498db;
            color: white;
            padding: 15px 0;
            margin-bottom: 20px;
        }
        
        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .nav-brand a {
            color: white;
            text-decoration: none;
            font-size: 24px;
            font-weight: bold;
        }
        
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 20px;
        }
        
        .nav-menu a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        
        .nav-menu a:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</body>
</html>
```

**共通フッター:** `src/main/resources/templates/fragments/footer.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<body>
    <footer th:fragment="footer" class="footer">
        <div class="container">
            <p>&copy; 2024 天気予報アプリ. All rights reserved.</p>
            <p>Powered by <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a></p>
        </div>
    </footer>
    
    <style>
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-top: 40px;
        }
        
        .footer a {
            color: #3498db;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</body>
</html>
```

**レイアウト適用例:** `src/main/resources/templates/practice/layout-example.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('レイアウト例')}"></head>
<body>
    <!-- ナビゲーション -->
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <!-- メインコンテンツ -->
    <div class="container">
        <h1>レイアウト・フラグメント例</h1>
        
        <div class="content">
            <h2>共通部品の使い方</h2>
            <p>ヘッダー、ナビゲーション、フッターを共通化しています。</p>
            
            <h3>使用しているフラグメント</h3>
            <ul>
                <li>fragments/header.html - ヘッダー（title, meta, CSS）</li>
                <li>fragments/navbar.html - ナビゲーションバー</li>
                <li>fragments/footer.html - フッター</li>
            </ul>
        </div>
    </div>
    
    <!-- フッター -->
    <div th:replace="~{fragments/footer :: footer}"></div>
</body>
</html>
```

---

### 4. 練習問題（15:00-17:00）

**練習問題ページ:** `thymeleaf-exercises.md`を作成

```markdown
# Thymeleaf練習問題

## 問題1: テキスト表示

以下のデータをHTMLに表示してください。

**Controller:**
```java
model.addAttribute("productName", "Spring Boot入門");
model.addAttribute("price", 3000);
```

**期待される表示:**
```
商品名: Spring Boot入門
価格: 3,000円
```

## 問題2: リスト表示

以下のリストをテーブルで表示してください。

**Controller:**
```java
List<Book> books = Arrays.asList(
    new Book("Java入門", 2500),
    new Book("Spring実践", 3500),
    new Book("Thymeleaf基礎", 2000)
);
model.addAttribute("books", books);
```

**期待されるHTML:**
```
| 書籍名 | 価格 |
|--------|------|
| Java入門 | 2,500円 |
| Spring実践 | 3,500円 |
| Thymeleaf基礎 | 2,000円 |
```

## 問題3: 条件分岐

在庫数に応じてメッセージを表示してください。

**条件:**
- 在庫 > 10: 在庫あり（緑）
- 在庫 1-10: 残りわずか（オレンジ）
- 在庫 = 0: 売り切れ（赤）

## 問題4: 日付フォーマット

現在日時を以下の形式で表示してください。

- 形式1: 2024年1月5日 15時30分
- 形式2: 2024/01/05
- 形式3: 15:30

## 問題5: URLリンク

以下のリンクを作成してください。

1. トップページへのリンク
2. 都道府県ID=13の天気ページへのリンク
3. 地域=関東でフィルタするリンク

## 解答例

解答例は `src/main/resources/templates/practice/exercises-answer.html` を参照
```

---

## ✅ チェックリスト

- [ ] Thymeleafの基本概念を理解した
- [ ] th:text, th:each, th:ifの使い方を習得した
- [ ] URL式（@{...}）の使い方を習得した
- [ ] 日付・数値フォーマットの使い方を習得した
- [ ] フラグメント（共通部品）の作り方を習得した
- [ ] thymeleaf-guide.mdを作成した
- [ ] 練習用ページを作成した
- [ ] 共通レイアウトを作成した
- [ ] 練習問題を解いた
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): Thymeleaf基礎実装と練習ページ作成"
git push origin feature/day-26
```

---

## 📚 参考リンク

### Thymeleaf公式
- [Thymeleaf公式ドキュメント](https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html)
- [Standard Expression Syntax](https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html#standard-expression-syntax)

### 日本語リソース
- [Thymeleaf基本文法（日本語）](https://qiita.com/NagaokaKenichi/items/c6d1b76090ef5ef39482)
- [Thymeleafレイアウト（日本語）](https://qiita.com/tag1216/items/3680b92cf96eb5a170f0)
- [Spring Boot + Thymeleaf（日本語）](https://spring.pleiades.io/guides/gs/serving-web-content/)

---

## 🆘 トラブルシューティング

### テンプレートが見つからない
**症状:** `TemplateNotFoundException`

**原因:** ファイルパスが間違っている

**解決策:**
```
src/main/resources/templates/
  └── practice/
      └── thymeleaf-basic.html

return "practice/thymeleaf-basic";  // 正しい
return "thymeleaf-basic";           // 間違い
```

### 変数が表示されない
**症状:** `${variable}` がそのまま表示される

**原因:**
- Controllerでモデルに追加していない
- xmlns宣言がない

**解決策:**
```html
<!-- xmlns宣言が必要 -->
<html xmlns:th="http://www.thymeleaf.org">

<!-- Controllerで追加 -->
model.addAttribute("variable", value);
```

### 日本語が文字化けする
**症状:** 日本語が「???」になる

**原因:** 文字コードがUTF-8でない

**解決策:**
```html
<meta charset="UTF-8">  <!-- 必須 -->
```

---

## 📝 本日のまとめ

1. **学んだこと:**
   - Thymeleafの基本文法
   - th:text, th:each, th:if, th:href
   - フラグメント（共通部品化）
   - 日付・数値フォーマット

2. **実装した機能:**
   - 練習用ページ
   - 共通レイアウト（ヘッダー、ナビ、フッター）

3. **明日への引き継ぎ:**
   - Day 27でトップページ（index.html）実装

---

## 🎉 完了後

次は [Day 27](day-27.md) へ

お疲れさまでした！
