# Day 5: Spring Boot Hello Worldの理解

## 📅 実施日
- 予定: Week 1 - Day 5
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Spring Bootの動作原理を深く理解し、アノテーションの役割を学ぶ

---

## 📋 午前の作業（9:00-13:00）

### 1. Spring Bootの自動設定の仕組み（9:00-10:30）

**学習内容:**

Spring Bootの3大特徴を理解する：

1. **自動設定（Auto Configuration）**
   - `@SpringBootApplication`の中身
   - `@EnableAutoConfiguration`の役割
   - 条件付きBean登録の仕組み

2. **スターター依存関係**
   - `spring-boot-starter-web`に含まれるもの
   - `spring-boot-starter-data-jpa`の役割
   - `spring-boot-starter-thymeleaf`の機能

3. **組み込みサーバー**
   - Tomcatが組み込まれている理由
   - ポート番号の変更方法
   - サーバー設定のカスタマイズ

**演習:**

`WeatherAppApplication.java`を詳しく見てみる：

```java
package com.example.weatherapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class WeatherAppApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(WeatherAppApplication.class, args);
    }
}
```

**`@SpringBootApplication`の内訳を理解:**
```java
// @SpringBootApplicationは以下3つのアノテーションの組み合わせ

@SpringBootConfiguration  // 設定クラスであることを示す
@EnableAutoConfiguration  // 自動設定を有効にする
@ComponentScan           // コンポーネントスキャンを有効にする
```

**ドキュメント作成:**
`spring-boot-architecture.md`を作成：

```markdown
# Spring Boot アーキテクチャの理解

## @SpringBootApplicationの役割

### @SpringBootConfiguration
- このクラスが設定クラスであることをSpringに伝える
- @Configurationと同じ役割

### @EnableAutoConfiguration
- クラスパスに基づいて自動的にBeanを設定
- 例：MySQLドライバがあれば自動的にDataSourceを設定

### @ComponentScan
- 同じパッケージ以下の@Component、@Service、@Repository、@Controllerを自動検出
- DIコンテナに登録

## DIコンテナとは

Dependency Injection（依存性注入）を管理するコンテナ
- Beanのライフサイクル管理
- 依存関係の自動解決
- シングルトンパターンの実装

## 起動プロセス

1. main()メソッド実行
2. SpringApplication.run()呼び出し
3. コンポーネントスキャン
4. Bean登録
5. 自動設定実行
6. 組み込みTomcat起動
7. アプリケーション起動完了
```

**成果物:**
- `spring-boot-architecture.md`

---

### 2. アノテーションの詳細理解（10:30-12:00）

**学習内容:**

主要なアノテーションの役割を理解する：

**1. ステレオタイプアノテーション**
```java
@Controller     // Webリクエストを処理するクラス
@Service        // ビジネスロジックを持つクラス
@Repository     // データアクセス層のクラス
@Component      // 汎用的なSpring管理Bean
```

**2. マッピングアノテーション**
```java
@GetMapping     // GETリクエストを処理
@PostMapping    // POSTリクエストを処理
@PutMapping     // PUTリクエストを処理
@DeleteMapping  // DELETEリクエストを処理
@RequestMapping // 汎用的なマッピング
```

**3. パラメータアノテーション**
```java
@RequestParam   // クエリパラメータを取得
@PathVariable   // URLパスから変数を取得
@RequestBody    // リクエストボディをオブジェクトに変換
@ModelAttribute // フォームデータをオブジェクトにバインド
```

**演習:**

様々なアノテーションを試すControllerを作成：

```java
package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/practice")
public class PracticeController {
    
    // 1. 基本的なGETマッピング
    @GetMapping
    public String index(Model model) {
        model.addAttribute("message", "練習ページ");
        return "practice/index";
    }
    
    // 2. @RequestParamの使用
    @GetMapping("/param")
    public String withParam(
        @RequestParam String name,
        @RequestParam(defaultValue = "0") int age,
        Model model
    ) {
        model.addAttribute("name", name);
        model.addAttribute("age", age);
        return "practice/param";
    }
    
    // 3. @PathVariableの使用
    @GetMapping("/user/{userId}")
    public String userDetail(
        @PathVariable Long userId,
        Model model
    ) {
        model.addAttribute("userId", userId);
        return "practice/user";
    }
    
    // 4. 複数のパスパラメータ
    @GetMapping("/article/{category}/{id}")
    public String articleDetail(
        @PathVariable String category,
        @PathVariable Long id,
        Model model
    ) {
        model.addAttribute("category", category);
        model.addAttribute("id", id);
        return "practice/article";
    }
    
    // 5. @ResponseBodyでJSON返却
    @GetMapping("/json")
    @ResponseBody
    public String returnJson() {
        return "{"message": "Hello JSON"}";
    }
}
```

対応するテンプレートを作成：

`src/main/resources/templates/practice/index.html`:
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>練習ページ</title>
</head>
<body>
    <h1 th:text="${message}"></h1>
    
    <h2>アノテーション練習リンク</h2>
    <ul>
        <li><a href="/practice/param?name=Taro&age=25">@RequestParam練習</a></li>
        <li><a href="/practice/user/123">@PathVariable練習</a></li>
        <li><a href="/practice/article/tech/456">複数PathVariable練習</a></li>
        <li><a href="/practice/json">JSON返却練習</a></li>
    </ul>
</body>
</html>
```

`src/main/resources/templates/practice/param.html`:
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>パラメータ練習</title>
</head>
<body>
    <h1>@RequestParam練習</h1>
    <p>名前: <span th:text="${name}"></span></p>
    <p>年齢: <span th:text="${age}"></span></p>
    <a href="/practice">戻る</a>
</body>
</html>
```

**成果物:**
- `PracticeController.java`
- `practice/index.html`
- `practice/param.html`
- `practice/user.html`
- `practice/article.html`

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. Modelの使い方を深く理解（13:00-14:30）

**学習内容:**

Modelは、ControllerからViewにデータを渡すための仕組み

**基本的な使い方:**
```java
@GetMapping("/example")
public String example(Model model) {
    // 単一の値を追加
    model.addAttribute("message", "Hello");
    
    // オブジェクトを追加
    User user = new User("Taro", 25);
    model.addAttribute("user", user);
    
    // リストを追加
    List<String> items = Arrays.asList("Apple", "Banana", "Orange");
    model.addAttribute("items", items);
    
    return "example";
}
```

**演習:**

複雑なデータをModelで渡す練習：

```java
package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/model-practice")
public class ModelPracticeController {
    
    @GetMapping
    public String practice(Model model) {
        // 1. 基本データ型
        model.addAttribute("title", "Modelの練習");
        model.addAttribute("count", 100);
        model.addAttribute("isActive", true);
        model.addAttribute("currentTime", LocalDateTime.now());
        
        // 2. リスト
        List<String> fruits = Arrays.asList("Apple", "Banana", "Orange", "Grape");
        model.addAttribute("fruits", fruits);
        
        // 3. Map
        Map<String, Integer> scores = new HashMap<>();
        scores.put("Math", 85);
        scores.put("English", 92);
        scores.put("Science", 78);
        model.addAttribute("scores", scores);
        
        // 4. オブジェクト
        Person person = new Person("Yamada Taro", 30, "Tokyo");
        model.addAttribute("person", person);
        
        // 5. オブジェクトのリスト
        List<Person> people = Arrays.asList(
            new Person("Sato Hanako", 25, "Osaka"),
            new Person("Tanaka Jiro", 35, "Nagoya"),
            new Person("Suzuki Yuki", 28, "Fukuoka")
        );
        model.addAttribute("people", people);
        
        return "model-practice";
    }
    
    // 内部クラスとしてPersonを定義
    public static class Person {
        private String name;
        private int age;
        private String city;
        
        public Person(String name, int age, String city) {
            this.name = name;
            this.age = age;
            this.city = city;
        }
        
        // Getter
        public String getName() { return name; }
        public int getAge() { return age; }
        public String getCity() { return city; }
    }
}
```

対応するテンプレート `src/main/resources/templates/model-practice.html`:
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Model練習</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1 th:text="${title}"></h1>
    
    <!-- 1. 基本データ型 -->
    <section>
        <h2>基本データ型</h2>
        <p>カウント: <span th:text="${count}"></span></p>
        <p>アクティブ: <span th:text="${isActive}"></span></p>
        <p>現在時刻: <span th:text="${currentTime}"></span></p>
    </section>
    
    <!-- 2. リスト -->
    <section>
        <h2>リストの表示</h2>
        <ul>
            <li th:each="fruit : ${fruits}" th:text="${fruit}"></li>
        </ul>
    </section>
    
    <!-- 3. Map -->
    <section>
        <h2>Mapの表示</h2>
        <table>
            <tr>
                <th>科目</th>
                <th>点数</th>
            </tr>
            <tr th:each="entry : ${scores}">
                <td th:text="${entry.key}"></td>
                <td th:text="${entry.value}"></td>
            </tr>
        </table>
    </section>
    
    <!-- 4. オブジェクト -->
    <section>
        <h2>オブジェクトの表示</h2>
        <p>名前: <span th:text="${person.name}"></span></p>
        <p>年齢: <span th:text="${person.age}"></span></p>
        <p>都市: <span th:text="${person.city}"></span></p>
    </section>
    
    <!-- 5. オブジェクトのリスト -->
    <section>
        <h2>オブジェクトリストの表示</h2>
        <table>
            <tr>
                <th>名前</th>
                <th>年齢</th>
                <th>都市</th>
            </tr>
            <tr th:each="p : ${people}">
                <td th:text="${p.name}"></td>
                <td th:text="${p.age}"></td>
                <td th:text="${p.city}"></td>
            </tr>
        </table>
    </section>
</body>
</html>
```

**動作確認:**
1. アプリケーションを起動
2. http://localhost:8080/model-practice にアクセス
3. 様々なデータ型が正しく表示されることを確認

**成果物:**
- `ModelPracticeController.java`
- `model-practice.html`
- 動作確認のスクリーンショット

---

### 4. application.propertiesの詳細設定（14:30-15:30）

**学習内容:**

application.propertiesで設定できる主要な項目を理解する

**現在の設定を確認:**
```properties
# Server Configuration
server.port=8080
server.servlet.context-path=/

# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/weather_app
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

**各設定の詳細:**

**1. サーバー設定**
```properties
# ポート番号変更
server.port=8080

# コンテキストパス（アプリケーションのルートパス）
server.servlet.context-path=/

# セッションタイムアウト（秒）
server.servlet.session.timeout=1800

# 最大HTTPヘッダーサイズ
server.max-http-header-size=8KB
```

**2. データベース設定**
```properties
# 接続プール設定
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=20000

# データベース初期化
spring.sql.init.mode=always
spring.sql.init.schema-locations=classpath:schema.sql
spring.sql.init.data-locations=classpath:data.sql
```

**3. JPA/Hibernate設定**
```properties
# DDL自動生成モード
# none: 何もしない
# validate: スキーマを検証のみ
# update: スキーマを更新（本番非推奨）
# create: 起動時にスキーマを作成（既存データ削除）
# create-drop: 終了時にスキーマを削除
spring.jpa.hibernate.ddl-auto=update

# SQL出力
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# ネーミング戦略
spring.jpa.hibernate.naming.physical-strategy=org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
```

**4. ログ設定**
```properties
# ログレベル（TRACE, DEBUG, INFO, WARN, ERROR）
logging.level.root=INFO
logging.level.com.example.weatherapp=DEBUG
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE

# ログファイル出力
logging.file.name=logs/application.log
logging.file.max-size=10MB
logging.file.max-history=30
```

**演習:**

環境別の設定ファイルを作成する：

`application-dev.properties`（開発環境）:
```properties
# Development環境設定
server.port=8080
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
logging.level.com.example.weatherapp=DEBUG
```

`application-prod.properties`（本番環境）:
```properties
# Production環境設定
server.port=80
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
logging.level.com.example.weatherapp=INFO
```

**起動時にプロファイルを指定:**
```bash
# 開発環境で起動
./gradlew bootRun --args='--spring.profiles.active=dev'

# 本番環境で起動
./gradlew bootRun --args='--spring.profiles.active=prod'
```

**成果物:**
- 更新された`application.properties`
- `application-dev.properties`
- `application-prod.properties`
- `application-properties-guide.md`（設定項目の説明ドキュメント）

---

### 5. ロギングの実装（15:30-16:30）

**学習内容:**

ログ出力の実装方法を学ぶ

**SLF4Jを使ったロギング:**
```java
package com.example.weatherapp.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/logging")
@Slf4j  // Lombokのログ機能を有効化
public class LoggingController {
    
    @GetMapping
    public String practice(Model model) {
        // 各レベルのログ出力
        log.trace("TRACE level log");
        log.debug("DEBUG level log");
        log.info("INFO level log");
        log.warn("WARN level log");
        log.error("ERROR level log");
        
        // 変数を含むログ
        String userName = "Taro";
        int age = 25;
        log.info("User: {}, Age: {}", userName, age);
        
        // 例外ログ
        try {
            int result = 10 / 0;
        } catch (Exception e) {
            log.error("An error occurred", e);
        }
        
        model.addAttribute("message", "ログ出力完了");
        return "logging";
    }
}
```

**ログレベルの使い分け:**
- **TRACE**: 最も詳細なデバッグ情報
- **DEBUG**: デバッグに必要な情報
- **INFO**: 通常の動作情報
- **WARN**: 警告（処理は継続）
- **ERROR**: エラー（処理に問題）

**演習:**

既存のControllerにログを追加：

```java
@Controller
@Slf4j
public class HelloController {
    
    @GetMapping("/")
    public String hello(Model model) {
        log.info("Hello endpoint accessed");
        
        String currentTime = LocalDateTime.now()
            .format(DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss"));
        
        log.debug("Current time: {}", currentTime);
        
        model.addAttribute("currentTime", currentTime);
        
        log.info("Returning hello view");
        return "hello";
    }
}
```

**成果物:**
- ログ機能を追加した各Controller
- ログファイル（`logs/application.log`）

---

### 6. Gitコミットとまとめ（16:30-17:00）

**手順:**

1. 変更をステージング
```bash
git add .
git status
```

2. コミット
```bash
git commit -m "feat: Spring Boot基礎の学習とアノテーション練習を追加"
```

3. リモートにプッシュ
```bash
git push origin main
```

**ドキュメント作成:**

`day-05-summary.md`を作成：
```markdown
# Day 5 学習まとめ

## 学んだこと

### Spring Bootの仕組み
- @SpringBootApplicationの3つの役割
- DIコンテナの仕組み
- 自動設定の動作原理

### アノテーション
- @Controller, @Service, @Repository, @Component
- @GetMapping, @PostMapping
- @RequestParam, @PathVariable
- @ResponseBody

### Modelの使い方
- 基本データ型の渡し方
- リスト、Mapの渡し方
- オブジェクトの渡し方

### application.properties
- サーバー設定
- データベース設定
- JPA設定
- ログ設定
- プロファイル別設定

### ロギング
- SLF4Jの使い方
- ログレベルの使い分け
- Lombokの@Slf4j

## 成果物

1. spring-boot-architecture.md
2. PracticeController.java
3. ModelPracticeController.java
4. LoggingController.java
5. 各種テンプレートファイル
6. application-dev.properties
7. application-prod.properties
8. application-properties-guide.md

## 感想・気づき

[自分の言葉で記載]

## 明日への準備

- Open-Meteo APIの公式ドキュメントを読む
- 要件定義の書き方を調べる
```

**成果物:**
- `day-05-summary.md`
- GitHubへのpush完了

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] Spring Bootの自動設定の仕組みが理解できた
- [ ] @SpringBootApplicationの役割が説明できる
- [ ] 主要なアノテーションが使える
- [ ] Modelでデータを渡せる
- [ ] application.propertiesの設定ができる
- [ ] プロファイル別設定が作成できた
- [ ] ログ出力が実装できた
- [ ] すべての成果物が完成した
- [ ] GitHubにコミット・プッシュした
- [ ] day-05-summary.mdを作成した

---

## 📚 参考リンク

- [Spring Boot公式ドキュメント](https://spring.io/projects/spring-boot)
- [Spring Framework公式ドキュメント](https://spring.io/projects/spring-framework)
- [Thymeleaf公式ドキュメント](https://www.thymeleaf.org/)
- [SLF4J公式ドキュメント](http://www.slf4j.org/)
- [Lombok公式ドキュメント](https://projectlombok.org/)

---

## 🆘 トラブルシューティング

### @Slf4jが動作しない
- IntelliJ IDEAのLombokプラグインがインストールされているか確認
- Annotation Processingが有効になっているか確認

### application.propertiesの設定が反映されない
- ファイル名が正しいか確認（application.properties）
- 配置場所が正しいか確認（src/main/resources/）
- アプリケーションを再起動

### ログが出力されない
- logging.level設定を確認
- ログファイルのパスが正しいか確認
- ディレクトリの書き込み権限を確認

---

## 📝 本日のまとめ

`day-05-summary.md`を作成し、以下の質問に答えてください：

1. Spring Bootのどの機能が最も便利だと思いましたか？
2. アノテーションの使い分けで困ったことは？
3. application.propertiesで設定したい項目は他にありますか？
4. 明日からの開発で活用したい知識は？

---

## 🎉 完了後

すべてのチェックリストが完了したら：
1. [Day 6](day-06.md)の準備をする
2. Open-Meteo APIのドキュメントを読む（予習）
3. 要件定義の書き方を調べる

お疲れさまでした！
