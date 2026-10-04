# Day 34: エラーページの作成

## 📅 実施日
- 予定: Week 7 - Day 34
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
ユーザーフレンドリーなエラーページを作成し、エラー発生時の体験を向上させる

---

## 📋 午前の作業（9:00-13:00）

### 1. エラーページの設計（9:00-9:30）

**主要なエラーページ:**

| ステータス | エラー名 | 用途 |
|-----------|---------|------|
| 400 | Bad Request | 不正なリクエスト |
| 404 | Not Found | ページが見つからない |
| 500 | Internal Server Error | サーバーエラー |
| 503 | Service Unavailable | サービス利用不可（API） |

**エラーページの要素:**
1. エラーコード（大きく表示）
2. わかりやすいメッセージ
3. 原因の説明
4. 次のアクション提案
5. ナビゲーションリンク

---

### 2. 404エラーページ実装（9:30-11:00）

**404ページ完全版:** `src/main/resources/templates/error/404.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - ページが見つかりません</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        .error-code {
            font-size: 120px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 20px;
        }
        
        .error-title {
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .error-message {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .error-details {
            background: #f8f9fa;
            border-left: 4px solid #e74c3c;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
            border-radius: 8px;
        }
        
        .error-details h3 {
            color: #e74c3c;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .error-details p {
            color: #555;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .error-details code {
            background: #fff;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            color: #e74c3c;
        }
        
        .actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #ecf0f1;
            color: #2c3e50;
        }
        
        .btn-secondary:hover {
            background: #d5dbdb;
        }
        
        .search-box {
            margin: 30px 0;
        }
        
        .search-box input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .suggestions {
            margin-top: 30px;
            text-align: left;
        }
        
        .suggestions h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .suggestions ul {
            list-style: none;
            padding: 0;
        }
        
        .suggestions li {
            margin-bottom: 10px;
        }
        
        .suggestions a {
            color: #667eea;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 6px;
            transition: background 0.3s;
        }
        
        .suggestions a:hover {
            background: #f8f9fa;
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 40px 20px;
            }
            
            .error-code {
                font-size: 80px;
            }
            
            .error-title {
                font-size: 24px;
            }
            
            .actions {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">404</div>
        <h1 class="error-title">ページが見つかりません</h1>
        <p class="error-message" th:text="${errorMessage} ?: 'お探しのページは見つかりませんでした。'">
            お探しのページは見つかりませんでした。
        </p>
        
        <!-- エラー詳細（開発環境のみ） -->
        <div class="error-details" th:if="${requestUrl}">
            <h3>📍 リクエスト情報</h3>
            <p>
                アクセスしようとしたURL: <code th:text="${requestUrl}"></code>
            </p>
            <p style="margin-top: 10px; font-size: 13px; color: #888;">
                このページは削除されたか、URLが変更された可能性があります。
            </p>
        </div>
        
        <!-- 検索ボックス -->
        <div class="search-box">
            <input type="text" 
                   id="searchInput" 
                   placeholder="都道府県名で検索..."
                   onkeyup="searchPrefecture(event)">
        </div>
        
        <!-- おすすめリンク -->
        <div class="suggestions">
            <h3>よく見られているページ</h3>
            <ul>
                <li>
                    <a href="/">
                        🏠 トップページ
                    </a>
                </li>
                <li>
                    <a href="/weather/13">
                        🌤️ 東京都の天気
                    </a>
                </li>
                <li>
                    <a href="/weather/27">
                        🌤️ 大阪府の天気
                    </a>
                </li>
                <li>
                    <a href="/weather/1">
                        🌤️ 北海道の天気
                    </a>
                </li>
            </ul>
        </div>
        
        <!-- アクション -->
        <div class="actions">
            <a href="/" class="btn btn-primary">トップページに戻る</a>
            <button onclick="history.back()" class="btn btn-secondary">前のページに戻る</button>
        </div>
    </div>
    
    <script>
        function searchPrefecture(event) {
            if (event.key === 'Enter') {
                const query = event.target.value.trim();
                if (query) {
                    window.location.href = '/?search=' + encodeURIComponent(query);
                }
            }
        }
    </script>
</body>
</html>
```

---

### 3. 500エラーページ実装（11:00-12:00）

`src/main/resources/templates/error/500.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - サーバーエラー</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            max-width: 700px;
            width: 100%;
            text-align: center;
        }
        
        .error-icon {
            font-size: 80px;
            margin-bottom: 20px;
        }
        
        .error-code {
            font-size: 100px;
            font-weight: bold;
            color: #e74c3c;
            line-height: 1;
            margin-bottom: 20px;
        }
        
        .error-title {
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .error-message {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .technical-details {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            text-align: left;
            font-family: monospace;
            font-size: 14px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .technical-details h3 {
            color: #e74c3c;
            margin-bottom: 10px;
        }
        
        .actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #e74c3c;
            color: white;
        }
        
        .btn-primary:hover {
            background: #c0392b;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: #ecf0f1;
            color: #2c3e50;
        }
        
        .help-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #ecf0f1;
        }
        
        .help-section h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .help-list {
            list-style: none;
            text-align: left;
            max-width: 500px;
            margin: 0 auto;
        }
        
        .help-list li {
            padding: 10px 0;
            color: #555;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 40px 20px;
            }
            
            .error-code {
                font-size: 80px;
            }
            
            .actions {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-code">500</div>
        <h1 class="error-title">サーバーエラーが発生しました</h1>
        <p class="error-message">
            申し訳ございません。サーバー側で問題が発生しました。<br>
            しばらく待ってから再度お試しください。
        </p>
        
        <!-- 技術的詳細（開発環境のみ） -->
        <div class="technical-details" th:if="${errorDetail}">
            <h3>🔧 エラー詳細（開発環境）</h3>
            <p th:text="${errorDetail}"></p>
            
            <div th:if="${stackTrace}" style="margin-top: 15px;">
                <h4 style="color: #e74c3c; font-size: 12px;">Stack Trace:</h4>
                <pre th:text="${stackTrace}" style="white-space: pre-wrap; word-break: break-all; font-size: 11px;"></pre>
            </div>
        </div>
        
        <div class="help-section">
            <h3>この問題を解決するには</h3>
            <ul class="help-list">
                <li>
                    <span>1️⃣</span>
                    <span>ページを再読み込みしてみてください</span>
                </li>
                <li>
                    <span>2️⃣</span>
                    <span>しばらく時間をおいてから再度アクセスしてください</span>
                </li>
                <li>
                    <span>3️⃣</span>
                    <span>問題が続く場合は、管理者にお問い合わせください</span>
                </li>
            </ul>
        </div>
        
        <div class="actions">
            <button onclick="location.reload()" class="btn btn-primary">ページを再読み込み</button>
            <a href="/" class="btn btn-secondary">トップページに戻る</a>
        </div>
    </div>
</body>
</html>
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. APIエラーページ実装（13:00-14:00）

`src/main/resources/templates/error/api-error.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>503 - サービス利用不可</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        .error-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
        }
        
        .error-code {
            font-size: 100px;
            font-weight: bold;
            color: #f39c12;
            line-height: 1;
            margin-bottom: 20px;
        }
        
        .error-title {
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .error-message {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .status-info {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }
        
        .status-info h3 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .status-info p {
            color: #856404;
            line-height: 1.6;
        }
        
        .retry-section {
            margin: 30px 0;
        }
        
        .countdown {
            font-size: 48px;
            font-weight: bold;
            color: #f39c12;
            margin: 20px 0;
        }
        
        .actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        
        .btn-primary {
            background: #27ae60;
            color: white;
        }
        
        .btn-primary:hover {
            background: #229954;
        }
        
        .btn-secondary {
            background: #ecf0f1;
            color: #2c3e50;
        }
        
        @media (max-width: 768px) {
            .error-container {
                padding: 40px 20px;
            }
            
            .error-code {
                font-size: 80px;
            }
            
            .actions {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">🌐</div>
        <div class="error-code">503</div>
        <h1 class="error-title">天気情報を取得できません</h1>
        <p class="error-message" th:text="${errorMessage} ?: '外部APIに接続できませんでした'">
            外部APIに接続できませんでした
        </p>
        
        <div class="status-info">
            <h3>💡 考えられる原因</h3>
            <p>
                • 天気情報提供サービスが一時的に利用できない<br>
                • ネットワーク接続に問題がある<br>
                • サーバーのメンテナンス中
            </p>
        </div>
        
        <div class="retry-section" th:if="${retryUrl}">
            <p>自動的に再試行します...</p>
            <div class="countdown" id="countdown">10</div>
        </div>
        
        <div class="actions">
            <a th:href="${retryUrl}" th:if="${retryUrl}" class="btn btn-primary">今すぐ再試行</a>
            <a href="/" class="btn btn-secondary">トップページに戻る</a>
        </div>
    </div>
    
    <script th:if="${retryUrl}">
        let countdown = 10;
        const countdownEl = document.getElementById('countdown');
        const retryUrl = /*[[${retryUrl}]]*/ '/';
        
        const timer = setInterval(() => {
            countdown--;
            if (countdownEl) {
                countdownEl.textContent = countdown;
            }
            
            if (countdown <= 0) {
                clearInterval(timer);
                window.location.href = retryUrl;
            }
        }, 1000);
    </script>
</body>
</html>
```

---

### 5. 400エラーページ実装（14:00-15:00）

`src/main/resources/templates/error/400.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>400 - 不正なリクエスト</title>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        .error-code {
            font-size: 100px;
            font-weight: bold;
            color: #3498db;
            line-height: 1;
            margin-bottom: 20px;
        }
        
        .error-title {
            font-size: 32px;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .error-message {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .actions {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-block;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            background: #3498db;
            color: white;
        }
        
        .btn:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">400</div>
        <h1 class="error-title">不正なリクエストです</h1>
        <p class="error-message">
            リクエストの形式が正しくありません。<br>
            正しいURLでアクセスしてください。
        </p>
        
        <div class="actions">
            <a href="/" class="btn">トップページに戻る</a>
        </div>
    </div>
</body>
</html>
```

---

### 6. エラーハンドリングテスト（15:00-17:00）

**テストコントローラー:** `src/main/java/com/example/weatherapp/controller/ErrorTestController.java`

```java
package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/test/error")
public class ErrorTestController {
    
    @GetMapping("/404")
    public String test404() {
        throw new ResourceNotFoundException("テスト用404エラー");
    }
    
    @GetMapping("/500")
    public String test500() {
        throw new RuntimeException("テスト用500エラー");
    }
    
    @GetMapping("/api")
    public String testApi() {
        throw new ExternalApiException("テスト用APIエラー");
    }
}
```

---

## ✅ チェックリスト

- [ ] 404エラーページを実装した
- [ ] 500エラーページを実装した
- [ ] 503（API）エラーページを実装した
- [ ] 400エラーページを実装した
- [ ] レスポンシブデザイン対応した
- [ ] 自動リトライ機能を実装した
- [ ] エラーテストを作成した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): エラーページ実装"
git push origin feature/day-34
```

---

## 📚 参考リンク

### エラーページデザイン
- [404ページデザイン集](https://www.awwwards.com/404-error-page-designs.html)
- [エラーページUX（日本語）](https://qiita.com/baby-degu/items/c6d0cf2e4b2e0b1c0d4d)

### Spring Boot エラーハンドリング
- [エラーページカスタマイズ（日本語）](https://qiita.com/NagaokaKenichi/items/5d8bc0ae5d36889b8972)

---

## 📝 本日のまとめ

1. **実装した機能:**
   - 404, 500, 503, 400エラーページ
   - 自動リトライ機能
   - エラーテスト

2. **学んだこと:**
   - エラーページのUX
   - ユーザーフレンドリーなエラー表示

3. **明日への引き継ぎ:**
   - Day 35でアクセシビリティ対応

---

## 🎉 完了後

次は [Day 35](day-35.md) へ

お疲れさまでした！
