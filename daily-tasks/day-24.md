# Day 24: 例外ハンドリング統一化

## 📅 実施日
- 予定: Week 5 - Day 24
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
@ControllerAdviceを使った統一的な例外ハンドリングを実装し、すべてのControllerで共通のエラー処理を行う

---

## 📋 午前の作業（9:00-13:00）

### 1. @ControllerAdviceの理解（9:00-9:30）

**@ControllerAdviceとは:**
- すべてのControllerに共通の処理を適用
- 例外ハンドリングを一箇所に集約
- コードの重複を削減

**使用する主なアノテーション:**

```java
@ControllerAdvice    // すべてのControllerに適用
@ExceptionHandler    // 特定の例外をハンドリング
@ResponseStatus      // HTTPステータスコードを指定
```

**例外ハンドリングの流れ:**

```
Controller: 例外発生
    ↓
Spring: @ControllerAdviceを探す
    ↓
GlobalExceptionHandler: @ExceptionHandlerでキャッチ
    ↓
エラーページ表示
```

**学習用ドキュメント作成:**

`exception-handling-guide.md`を作成：

```markdown
# Spring例外ハンドリングガイド

## @ControllerAdviceの基本

全Controllerで共通の例外処理を定義できる。

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public String handleNotFound(ResourceNotFoundException e, Model model) {
        model.addAttribute("error", e.getMessage());
        return "error/404";
    }
}
```

## @ExceptionHandlerの優先順位

1. Controller内の@ExceptionHandler（最優先）
2. @ControllerAdvice内の@ExceptionHandler
3. Spring Bootのデフォルトエラーハンドリング

## @ResponseStatusの使い方

```java
@ExceptionHandler(ResourceNotFoundException.class)
@ResponseStatus(HttpStatus.NOT_FOUND)  // 404ステータスを返す
public String handleNotFound(...) {
    return "error/404";
}
```

## ログ出力のベストプラクティス

- **warn**: ユーザーエラー（404など）
- **error**: システムエラー（500など）
- **debug**: 詳細なデバッグ情報

```java
@ExceptionHandler(Exception.class)
public String handleError(Exception e, Model model) {
    log.error("予期しないエラー", e);  // スタックトレース込み
    return "error/500";
}
```
```

---

### 2. GlobalExceptionHandler実装（9:30-12:00）

**ハンドラークラス作成:** `src/main/java/com/example/weatherapp/exception/GlobalExceptionHandler.java`

```java
package com.example.weatherapp.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.NoHandlerFoundException;

import javax.servlet.http.HttpServletRequest;

/**
 * グローバル例外ハンドラー
 * すべてのControllerで発生した例外を統一的に処理
 */
@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    /**
     * ResourceNotFoundExceptionのハンドリング
     * 都道府県が見つからない場合など
     * 
     * @param e 例外
     * @param model モデル
     * @param request HTTPリクエスト
     * @return エラーページ
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String handleResourceNotFound(
        ResourceNotFoundException e,
        Model model,
        HttpServletRequest request
    ) {
        log.warn("リソースが見つかりません: path={}, message={}", 
            request.getRequestURI(), 
            e.getMessage()
        );
        
        model.addAttribute("errorMessage", e.getMessage());
        model.addAttribute("requestUrl", request.getRequestURI());
        model.addAttribute("statusCode", 404);
        
        return "error/404";
    }
    
    /**
     * ExternalApiExceptionのハンドリング
     * 外部API（Open-Meteo）呼び出し失敗時
     * 
     * @param e 例外
     * @param model モデル
     * @param request HTTPリクエスト
     * @return エラーページ
     */
    @ExceptionHandler(ExternalApiException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    public String handleExternalApiError(
        ExternalApiException e,
        Model model,
        HttpServletRequest request
    ) {
        log.error("外部API呼び出しエラー: path={}, message={}", 
            request.getRequestURI(),
            e.getMessage(),
            e
        );
        
        model.addAttribute("errorMessage", "天気情報の取得に失敗しました");
        model.addAttribute("errorDetail", e.getMessage());
        model.addAttribute("requestUrl", request.getRequestURI());
        model.addAttribute("statusCode", 503);
        
        // リトライ用のパラメータを抽出
        String prefectureId = extractPrefectureId(request.getRequestURI());
        if (prefectureId != null) {
            model.addAttribute("prefectureId", prefectureId);
            model.addAttribute("retryUrl", "/weather/" + prefectureId);
        }
        
        return "error/api-error";
    }
    
    /**
     * BusinessExceptionのハンドリング
     * ビジネスロジックエラー
     * 
     * @param e 例外
     * @param model モデル
     * @return エラーページ
     */
    @ExceptionHandler(BusinessException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String handleBusinessError(
        BusinessException e,
        Model model,
        HttpServletRequest request
    ) {
        log.warn("ビジネスエラー: path={}, message={}", 
            request.getRequestURI(),
            e.getMessage()
        );
        
        model.addAttribute("errorMessage", e.getMessage());
        model.addAttribute("statusCode", 400);
        
        return "error/business-error";
    }
    
    /**
     * NoHandlerFoundExceptionのハンドリング
     * 存在しないURLにアクセスした場合
     * 
     * @param e 例外
     * @param model モデル
     * @return エラーページ
     */
    @ExceptionHandler(NoHandlerFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String handleNoHandlerFound(
        NoHandlerFoundException e,
        Model model
    ) {
        log.warn("ページが見つかりません: {}", e.getRequestURL());
        
        model.addAttribute("errorMessage", "お探しのページは見つかりませんでした");
        model.addAttribute("requestUrl", e.getRequestURL());
        model.addAttribute("statusCode", 404);
        
        return "error/404";
    }
    
    /**
     * すべての予期しない例外のハンドリング
     * 最終的なセーフティネット
     * 
     * @param e 例外
     * @param model モデル
     * @param request HTTPリクエスト
     * @return エラーページ
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public String handleGeneralError(
        Exception e,
        Model model,
        HttpServletRequest request
    ) {
        log.error("予期しないエラーが発生しました: path={}", 
            request.getRequestURI(),
            e  // スタックトレースも出力
        );
        
        model.addAttribute("errorMessage", "システムエラーが発生しました");
        model.addAttribute("requestUrl", request.getRequestURI());
        model.addAttribute("statusCode", 500);
        
        // 開発環境のみエラー詳細を表示
        if (isDevelopmentMode()) {
            model.addAttribute("errorDetail", e.getMessage());
            model.addAttribute("stackTrace", getStackTraceAsString(e));
        }
        
        return "error/500";
    }
    
    /**
     * URLから都道府県IDを抽出
     * /weather/13 → "13"
     */
    private String extractPrefectureId(String uri) {
        if (uri == null || !uri.startsWith("/weather/")) {
            return null;
        }
        
        String[] parts = uri.split("/");
        if (parts.length >= 3) {
            return parts[2].split("\\?")[0];  // クエリパラメータを除去
        }
        
        return null;
    }
    
    /**
     * 開発モードかどうか判定
     */
    private boolean isDevelopmentMode() {
        String profile = System.getProperty("spring.profiles.active", "");
        return profile.contains("dev") || profile.isEmpty();
    }
    
    /**
     * スタックトレースを文字列化
     */
    private String getStackTraceAsString(Exception e) {
        StringBuilder sb = new StringBuilder();
        for (StackTraceElement element : e.getStackTrace()) {
            sb.append(element.toString()).append("\n");
            if (sb.length() > 2000) {  // 長すぎる場合は切り詰め
                sb.append("...(省略)");
                break;
            }
        }
        return sb.toString();
    }
}
```

**実装のポイント:**

1. **@ControllerAdvice**
   - すべてのControllerに適用
   - 例外ハンドリングを一箇所に集約

2. **@ExceptionHandler**
   - 特定の例外型を指定
   - より具体的な例外から順に定義

3. **@ResponseStatus**
   - HTTPステータスコードを指定
   - 404, 503, 500など

4. **ログレベルの使い分け**
   - warn: ユーザーエラー
   - error: システムエラー

5. **開発/本番の切り替え**
   - 開発環境でのみ詳細表示

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. エラーページ作成（13:00-15:00）

**404エラーページ:** `src/main/resources/templates/error/404.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>404 - ページが見つかりません</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            color: #e74c3c;
            margin: 20px 0;
        }
        .error-title {
            font-size: 32px;
            margin: 20px 0;
        }
        .error-message {
            font-size: 18px;
            color: #666;
            margin: 20px 0;
        }
        .error-details {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-family: monospace;
            text-align: left;
        }
        .actions {
            margin: 30px 0;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            margin: 0 10px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background: #2980b9;
        }
        .btn-secondary {
            background: #95a5a6;
        }
        .btn-secondary:hover {
            background: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="error-code">404</div>
    <div class="error-title">ページが見つかりません</div>
    
    <div class="error-message" th:text="${errorMessage}">
        お探しのページは見つかりませんでした
    </div>
    
    <div class="error-details" th:if="${requestUrl}">
        <strong>リクエストURL:</strong> <span th:text="${requestUrl}"></span>
    </div>
    
    <div class="actions">
        <a href="/" class="btn">トップページに戻る</a>
        <a href="javascript:history.back()" class="btn btn-secondary">前のページに戻る</a>
    </div>
</body>
</html>
```

**APIエラーページ:** `src/main/resources/templates/error/api-error.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>503 - サービス利用不可</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            color: #f39c12;
            margin: 20px 0;
        }
        .error-icon {
            font-size: 80px;
            margin: 20px 0;
        }
        .error-title {
            font-size: 32px;
            margin: 20px 0;
        }
        .error-message {
            font-size: 18px;
            color: #666;
            margin: 20px 0;
        }
        .error-details {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
        }
        .actions {
            margin: 30px 0;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            margin: 0 10px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background: #2980b9;
        }
        .btn-retry {
            background: #27ae60;
        }
        .btn-retry:hover {
            background: #229954;
        }
    </style>
</head>
<body>
    <div class="error-code">503</div>
    <div class="error-icon">⚠️</div>
    <div class="error-title">天気情報の取得に失敗しました</div>
    
    <div class="error-message" th:text="${errorMessage}">
        外部サービスに接続できませんでした
    </div>
    
    <div class="error-details" th:if="${errorDetail}">
        <strong>エラー詳細:</strong><br>
        <span th:text="${errorDetail}"></span>
    </div>
    
    <div class="actions">
        <a th:href="${retryUrl}" th:if="${retryUrl}" class="btn btn-retry">再試行</a>
        <a href="/" class="btn">トップページに戻る</a>
    </div>
    
    <p style="color: #999; font-size: 14px; margin-top: 40px;">
        問題が続く場合は、しばらく時間をおいてから再度お試しください。
    </p>
</body>
</html>
```

**500エラーページ:** `src/main/resources/templates/error/500.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>500 - サーバーエラー</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            color: #c0392b;
            margin: 20px 0;
        }
        .error-title {
            font-size: 32px;
            margin: 20px 0;
        }
        .error-message {
            font-size: 18px;
            color: #666;
            margin: 20px 0;
        }
        .error-details {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
            max-height: 300px;
            overflow-y: auto;
        }
        .stack-trace {
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .actions {
            margin: 30px 0;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            margin: 0 10px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="error-code">500</div>
    <div class="error-title">システムエラーが発生しました</div>
    
    <div class="error-message" th:text="${errorMessage}">
        申し訳ございません。サーバーでエラーが発生しました。
    </div>
    
    <!-- 開発環境のみ表示 -->
    <div class="error-details" th:if="${errorDetail}">
        <strong>エラー詳細:</strong><br>
        <span th:text="${errorDetail}"></span>
    </div>
    
    <div class="error-details" th:if="${stackTrace}">
        <strong>スタックトレース:</strong><br>
        <div class="stack-trace" th:text="${stackTrace}"></div>
    </div>
    
    <div class="actions">
        <a href="/" class="btn">トップページに戻る</a>
    </div>
    
    <p style="color: #999; font-size: 14px; margin-top: 40px;">
        問題が解決しない場合は、管理者にお問い合わせください。
    </p>
</body>
</html>
```

---

### 4. テスト作成（15:00-17:00）

`src/test/java/com/example/weatherapp/exception/GlobalExceptionHandlerTest.java`:

```java
package com.example.weatherapp.exception;

import com.example.weatherapp.controller.WeatherController;
import com.example.weatherapp.service.WeatherService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * GlobalExceptionHandlerのテスト
 */
@WebMvcTest(WeatherController.class)
class GlobalExceptionHandlerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private WeatherService weatherService;
    
    @Test
    @DisplayName("ResourceNotFoundExceptionが404エラーページを表示する")
    void testResourceNotFoundException() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(999L))
            .thenThrow(new ResourceNotFoundException("都道府県が見つかりません: id=999"));
        
        // When & Then
        mockMvc.perform(get("/weather/999"))
            .andExpect(status().isNotFound())
            .andExpect(view().name("error/404"))
            .andExpect(model().attributeExists("errorMessage"))
            .andExpect(model().attribute("statusCode", 404));
    }
    
    @Test
    @DisplayName("ExternalApiExceptionがAPIエラーページを表示する")
    void testExternalApiException() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(13L))
            .thenThrow(new ExternalApiException("API呼び出し失敗"));
        
        // When & Then
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isServiceUnavailable())
            .andExpect(view().name("error/api-error"))
            .andExpect(model().attributeExists("errorMessage"))
            .andExpect(model().attribute("statusCode", 503))
            .andExpect(model().attribute("prefectureId", "13"))
            .andExpect(model().attribute("retryUrl", "/weather/13"));
    }
    
    @Test
    @DisplayName("予期しない例外が500エラーページを表示する")
    void testUnexpectedException() throws Exception {
        // Given
        when(weatherService.getWeatherByPrefectureId(13L))
            .thenThrow(new RuntimeException("予期しないエラー"));
        
        // When & Then
        mockMvc.perform(get("/weather/13"))
            .andExpect(status().isInternalServerError())
            .andExpect(view().name("error/500"))
            .andExpect(model().attributeExists("errorMessage"))
            .andExpect(model().attribute("statusCode", 500));
    }
}
```

---

## ✅ チェックリスト

- [ ] @ControllerAdviceの仕組みを理解した
- [ ] GlobalExceptionHandlerを実装した
- [ ] 各種例外のハンドリングを実装した
- [ ] エラーページ（404, 503, 500）を作成した
- [ ] テストを作成し、すべてパスした
- [ ] exception-handling-guide.mdを作成した
- [ ] ブラウザで各エラーページを確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(exception): GlobalExceptionHandlerとエラーページを実装"
git push origin feature/day-24
```

---

## 📚 参考リンク

### Spring例外ハンドリング
- [@ControllerAdvice公式ドキュメント](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-advice.html)
- [@ControllerAdviceの使い方（日本語）](https://qiita.com/tag1216/items/3680b92cf96eb5a170f0)
- [Spring Boot エラーハンドリング（日本語）](https://qiita.com/NagaokaKenichi/items/5d8bc0ae5d36889b8972)

### エラーページデザイン
- [エラーページのベストプラクティス](https://uxdesign.cc/how-to-design-a-404-error-page-that-actually-helps-users-69b067b25b56)
- [HTTPステータスコード一覧](https://developer.mozilla.org/ja/docs/Web/HTTP/Status)

---

## 🆘 トラブルシューティング

### @ControllerAdviceが動作しない
**症状:** 例外が補足されない

**原因:**
- @ControllerAdviceがコンポーネントスキャン対象外
- 例外の型が一致していない

**解決策:**
```java
@ControllerAdvice  // 必須
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)  // 正確な型
    public String handle(...) { ... }
}
```

### エラーページが表示されない
**症状:** Whitelabel Error Page が表示される

**原因:**
- テンプレートファイルが見つからない
- return文のパスが間違っている

**解決策:**
```
templates/
  └── error/
      ├── 404.html
      ├── api-error.html
      └── 500.html

return "error/404";  // templates/error/404.html
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - GlobalExceptionHandler
   - 統一的な例外ハンドリング
   - カスタムエラーページ

2. **学んだこと:**
   - @ControllerAdviceの使い方
   - @ExceptionHandlerの優先順位
   - エラーページのデザイン

3. **明日への引き継ぎ:**
   - Day 25でバックエンドの統合テスト

---

## 🎉 完了後

次は [Day 25](day-25.md) へ

お疲れさまでした！
