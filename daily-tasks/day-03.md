# Day 3: 環境構築完了とHello World

## 📅 実施日
- 予定: Week 1 - Day 3
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Gradleのインストールと設定を完了し、初めてのHello Worldページを表示する

---

## 📋 午前の作業（9:00-13:00）

### 1. Gradleのインストール（9:00-10:00）

**手順:**
1. Gradle 8.xのインストール
   - Windows: https://gradle.org/releases/ からダウンロード
   - Mac: `brew install gradle`
   - Linux: `sdk install gradle`

2. 環境変数の設定
   - `GRADLE_HOME`を設定
   - `PATH`に追加

3. 動作確認
   ```bash
   gradle --version
   ```

**成果物:**
- `gradle --version`のスクリーンショット

---

### 2. Spring Initializrでプロジェクト作成（10:00-11:30）

**手順:**
1. Spring Initializrにアクセス
   - https://start.spring.io/

2. プロジェクト設定
   - **Project**: Gradle - Groovy
   - **Language**: Java
   - **Spring Boot**: **3.5.x の最新の安定版**（例: 3.5.9。画面に表示される 3.5.x のうち、`(SNAPSHOT)` が付いていない最新を選ぶ）
     - ⚠️ `4.x` や `(SNAPSHOT)` は選ばないでください。この研修の教材は Spring Boot 3.x 系を前提に書かれています
     - Spring Initializr の選択肢は時期によって変わります。`3.2.x` が表示されない場合も、上記の方針で選べば問題ありません
   - **Project Metadata**:
     - Group: `com.example`
     - Artifact: `weather-app`
     - Name: `weather-app`
     - Package name: `com.example.weatherapp`
     - Packaging: Jar
     - Java: 17

3. 依存関係の追加
   - Spring Web
   - Spring Data JPA
   - MySQL Driver
   - Thymeleaf
   - Lombok
   - Spring Boot DevTools

4. GENERATE でダウンロード

5. プロジェクトの展開
   ```bash
   cd ~/workspace
   unzip weather-app.zip
   cd weather-app
   ```

**成果物:**
- Spring Bootプロジェクト

---

### 3. IntelliJ IDEAでプロジェクトを開く（11:30-12:00）

**手順:**
1. IntelliJ IDEAを起動

2. "Open"をクリックし、`weather-app`フォルダを選択

3. Gradleの自動インポート待機
   - 右下に表示される"Load Gradle Project"をクリック
   - 依存関係のダウンロード完了を待つ（数分かかる）

4. プロジェクト構造の確認
   ```
   weather-app/
   ├── src/
   │   ├── main/
   │   │   ├── java/
   │   │   │   └── com/example/weatherapp/
   │   │   │       └── WeatherAppApplication.java
   │   │   └── resources/
   │   │       ├── application.properties
   │   │       ├── static/
   │   │       └── templates/
   │   └── test/
   ├── build.gradle
   └── settings.gradle
   ```

**成果物:**
- IntelliJ IDEAでプロジェクトが開かれている

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. application.propertiesの設定（13:00-13:30）

**手順:**
1. `src/main/resources/application.properties`を開く

2. データベース接続設定を追加
   ```properties
   # Server Configuration
   server.port=8080
   
   # Database Configuration
   spring.datasource.url=jdbc:mysql://localhost:3306/weather_app?useSSL=false&serverTimezone=Asia/Tokyo&allowPublicKeyRetrieval=true
   spring.datasource.username=root
   spring.datasource.password=your_password
   spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
   
   # JPA Configuration
   spring.jpa.hibernate.ddl-auto=update
   spring.jpa.show-sql=true
   spring.jpa.properties.hibernate.format_sql=true
   spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
   
   # Thymeleaf Configuration
   spring.thymeleaf.cache=false
   spring.thymeleaf.prefix=classpath:/templates/
   spring.thymeleaf.suffix=.html
   
   # Logging
   logging.level.org.springframework.web=DEBUG
   logging.level.com.example.weatherapp=DEBUG
   ```

3. パスワードを自分の環境に合わせて変更

**成果物:**
- 設定済みの`application.properties`

---

### 5. Hello World Controllerの作成（13:30-14:30）

**手順:**
1. `com.example.weatherapp.controller`パッケージを作成

2. `HelloController.java`を作成
   ```java
   package com.example.weatherapp.controller;
   
   import org.springframework.stereotype.Controller;
   import org.springframework.web.bind.annotation.GetMapping;
   import org.springframework.web.bind.annotation.ResponseBody;
   
   @Controller
   public class HelloController {
       
       @GetMapping("/")
       @ResponseBody
       public String hello() {
           return "Hello World!";
       }
   }
   ```

3. コードの説明
   - `@Controller`: このクラスがコントローラーであることを示す
   - `@GetMapping("/")`: ルートパス"/"へのGETリクエストを処理
   - `@ResponseBody`: レスポンスボディとして文字列を直接返す

**成果物:**
- `HelloController.java`

---

### 6. アプリケーションの起動と確認（14:30-15:30）

**手順:**
1. アプリケーションの起動
   - IntelliJ IDEAの`WeatherAppApplication.java`を開く
   - 緑の再生ボタン（Run）をクリック
   - または、ターミナルで`./gradlew bootRun`

2. 起動ログの確認
   ```
   Started WeatherAppApplication in X.XXX seconds
   ```

3. ブラウザで確認
   - http://localhost:8080/ にアクセス
   - "Hello World!"が表示されることを確認

4. ターミナルでcurlテスト
   ```bash
   curl http://localhost:8080/
   ```

**トラブルシューティング:**
- ポート8080が使用中の場合: `application.properties`で`server.port=8081`に変更
- データベース接続エラー: MySQL Serverが起動しているか確認

**成果物:**
- 起動成功のスクリーンショット
- ブラウザで"Hello World!"が表示されているスクリーンショット

---

### 7. Thymeleafテンプレートで表示（15:30-16:30）

**手順:**
1. `src/main/resources/templates/hello.html`を作成
   ```html
   <!DOCTYPE html>
   <html xmlns:th="http://www.thymeleaf.org">
   <head>
       <meta charset="UTF-8">
       <title>Hello World</title>
       <style>
           body {
               font-family: Arial, sans-serif;
               display: flex;
               justify-content: center;
               align-items: center;
               height: 100vh;
               margin: 0;
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               color: white;
           }
           .container {
               text-align: center;
           }
           h1 {
               font-size: 4rem;
               margin: 0;
           }
           p {
               font-size: 1.5rem;
           }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>Hello World!</h1>
           <p>Spring Bootアプリケーションが動作しています</p>
           <p th:text="'現在時刻: ' + ${currentTime}"></p>
       </div>
   </body>
   </html>
   ```

2. `HelloController.java`を修正
   ```java
   package com.example.weatherapp.controller;
   
   import org.springframework.stereotype.Controller;
   import org.springframework.ui.Model;
   import org.springframework.web.bind.annotation.GetMapping;
   
   import java.time.LocalDateTime;
   import java.time.format.DateTimeFormatter;
   
   @Controller
   public class HelloController {
       
       @GetMapping("/")
       public String hello(Model model) {
           String currentTime = LocalDateTime.now()
               .format(DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss"));
           model.addAttribute("currentTime", currentTime);
           return "hello";
       }
   }
   ```

3. アプリケーションを再起動

4. ブラウザで確認
   - http://localhost:8080/
   - Thymeleafテンプレートが表示される
   - 現在時刻が表示される

**成果物:**
- `hello.html`
- 更新された`HelloController.java`
- Thymeleaf表示のスクリーンショット

---

### 8. Gitコミットとプッシュ（16:30-17:00）

**手順:**
1. .gitignoreの確認
   ```gitignore
   .gradle
   build/
   !gradle/wrapper/gradle-wrapper.jar
   !**/src/main/**/build/
   !**/src/test/**/build/
   
   ### IntelliJ IDEA ###
   .idea
   *.iws
   *.iml
   *.ipr
   out/
   
   ### Application Properties ###
   application-local.properties
   ```

2. ステージングとコミット
   ```bash
   git add .
   git commit -m "feat: Hello Worldページを作成"
   ```

3. リモートにプッシュ
   ```bash
   git push origin main
   ```

**成果物:**
- GitHubにプッシュされたコード

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] Gradleがインストールされている
- [ ] Spring Bootプロジェクトが作成されている
- [ ] IntelliJ IDEAでプロジェクトが開かれている
- [ ] `application.properties`が設定されている
- [ ] HelloControllerが作成されている
- [ ] アプリケーションが起動する
- [ ] http://localhost:8080/ で"Hello World!"が表示される
- [ ] Thymeleafテンプレートが動作する
- [ ] 現在時刻が表示される
- [ ] GitHubにコードがプッシュされている

---

## 📚 参考リンク

- [Spring Boot公式ドキュメント](https://spring.io/projects/spring-boot)
- [Spring Initializr](https://start.spring.io/)
- [Thymeleaf公式ドキュメント](https://www.thymeleaf.org/documentation.html)
- [Gradle公式ドキュメント](https://docs.gradle.org/)

---

## 🆘 トラブルシューティング

### アプリケーションが起動しない
```bash
# Gradleキャッシュをクリア
./gradlew clean build
```

### ポート8080が使用中
```bash
# 使用中のプロセスを確認（Windows）
netstat -ano | findstr :8080

# 使用中のプロセスを確認（Mac/Linux）
lsof -i :8080
```

### Thymeleafテンプレートが見つからない
- ファイル名が正しいか確認（`hello.html`）
- `src/main/resources/templates/`に配置されているか確認

---

## 📝 本日のまとめ

`day-03-summary.md`を作成し、以下の質問に答えてください：

1. Spring Bootの起動で最も印象的だったことは？
2. Thymeleafテンプレートの仕組みが理解できましたか？
3. application.propertiesの役割を説明してください
4. 明日からの開発で期待することは？

---

## 🎉 完了後

すべてのチェックリストが完了したら：
1. [Day 4](day-04.md)の準備をする
2. Spring Bootの公式チュートリアルを読む（任意）
3. 明日の学習内容を確認

お疲れさまでした！
