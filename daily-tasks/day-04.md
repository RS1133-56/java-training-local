# Day 4: Spring Boot基礎とプロジェクト作成

## 📅 実施日
- 予定: Week 1 - Day 4
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
Spring Bootの基本概念を理解し、天気アプリのプロジェクト構造を準備する

---

## 午前の作業（9:00-13:00）

### 1. Spring Bootアーキテクチャの理解（9:00-11:00）

**学習内容:**
- MVCパターンとは
  - Model: データとビジネスロジック
  - View: 表示層（Thymeleaf）
  - Controller: リクエストとレスポンスの制御

- Spring Bootの主要コンポーネント
  - `@Controller`: HTTPリクエストを処理
  - `@Service`: ビジネスロジックを実装
  - `@Repository`: データベースアクセス
  - `@Entity`: データベーステーブルとマッピング

- DIコンテナと依存性注入
  - `@Autowired`の仕組み
  - コンストラクタインジェクション
  - フィールドインジェクション

**演習:**
簡単なサンプルコードでMVCを体験
```java
// Model
@Data
public class Message {
    private String text;
    private String author;
}

// Controller
@Controller
public class MessageController {
    @GetMapping("/message")
    public String showMessage(Model model) {
        Message message = new Message();
        message.setText("Hello from Spring Boot!");
        message.setAuthor("Claude");
        model.addAttribute("message", message);
        return "message";
    }
}
```

**成果物:**
- `spring-boot-architecture.md`（学習内容のまとめ）

---

### 2. プロジェクト構造の設計（11:00-12:00）

**手順:**
天気アプリのパッケージ構造を作成

```
com.example.weatherapp/
├── WeatherAppApplication.java
├── controller/
│   ├── HomeController.java
│   └── WeatherController.java
├── service/
│   ├── PrefectureService.java
│   └── WeatherService.java
├── repository/
│   ├── PrefectureRepository.java
│   └── WeatherRecordRepository.java
├── entity/
│   ├── Prefecture.java
│   └── WeatherRecord.java
├── dto/
│   ├── WeatherResponse.java
│   └── PrefectureDto.java
├── client/
│   └── OpenMeteoClient.java
├── exception/
│   ├── ResourceNotFoundException.java
│   └── GlobalExceptionHandler.java
└── config/
    └── WebConfig.java
```

**成果物:**
- 作成されたパッケージ構造

---

### 昼休憩（12:00-13:00）

---

## 午後の作業（13:00-17:00）

### 3. Lombok導入と基本的なEntityクラス作成（13:00-14:30）

**手順:**
1. `build.gradle`の確認（Lombokが含まれているか）
```gradle
dependencies {
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
}
```

2. IntelliJ IDEAにLombokプラグインをインストール
   - Settings → Plugins → "Lombok" を検索してインストール
   - Annotation Processing を有効化
   - Settings → Build, Execution, Deployment → Compiler → Annotation Processors
   - "Enable annotation processing" にチェック

3. 簡単なEntityクラスを作成
```java
package com.example.weatherapp.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "test_messages")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String message;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @PrePersist
    public void prePersist() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }
}
```

**Lombokアノテーションの説明:**
- `@Data`: getter/setter/toString/equals/hashCodeを自動生成
- `@NoArgsConstructor`: 引数なしコンストラクタ
- `@AllArgsConstructor`: 全フィールドを引数に持つコンストラクタ
- `@Builder`: ビルダーパターンを自動生成

**成果物:**
- `TestMessage.java`
- Lombok設定完了

---

### 4. JPA Repositoryの作成（14:30-15:30）

**手順:**
```java
package com.example.weatherapp.repository;

import com.example.weatherapp.entity.TestMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TestMessageRepository extends JpaRepository<TestMessage, Long> {
    // 基本的なCRUD操作は自動で提供される
    // カスタムクエリが必要な場合はここに追加
}
```

**JpaRepositoryが提供するメソッド:**
- `save(entity)`: 保存
- `findById(id)`: IDで検索
- `findAll()`: 全件取得
- `deleteById(id)`: 削除
- `count()`: 件数取得

**成果物:**
- `TestMessageRepository.java`

---

### 5. Serviceレイヤーの作成（15:30-16:30）

**手順:**
```java
package com.example.weatherapp.service;

import com.example.weatherapp.entity.TestMessage;
import com.example.weatherapp.repository.TestMessageRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TestMessageService {
    
    private final TestMessageRepository repository;
    
    public List<TestMessage> getAllMessages() {
        return repository.findAll();
    }
    
    @Transactional
    public TestMessage createMessage(String messageText) {
        TestMessage message = TestMessage.builder()
            .message(messageText)
            .build();
        return repository.save(message);
    }
}
```

**ポイント:**
- `@RequiredArgsConstructor`: finalフィールドのコンストラクタを自動生成（DI）
- `@Transactional(readOnly = true)`: 読み取り専用トランザクション
- `@Transactional`: 書き込み可能トランザクション

**成果物:**
- `TestMessageService.java`

---

### 6. Controllerでの動作確認（16:30-17:00）

**手順:**
```java
package com.example.weatherapp.controller;

import com.example.weatherapp.entity.TestMessage;
import com.example.weatherapp.service.TestMessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
@RequestMapping("/test")
public class TestController {
    
    private final TestMessageService testMessageService;
    
    @GetMapping
    public String showMessages(Model model) {
        model.addAttribute("messages", testMessageService.getAllMessages());
        return "test";
    }
    
    @PostMapping
    public String createMessage(@RequestParam String message) {
        testMessageService.createMessage(message);
        return "redirect:/test";
    }
}
```

テンプレート `src/main/resources/templates/test.html`:
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Test Messages</title>
</head>
<body>
    <h1>Test Messages</h1>
    
    <form method="post" action="/test">
        <input type="text" name="message" placeholder="Enter message">
        <button type="submit">Send</button>
    </form>
    
    <ul>
        <li th:each="msg : ${messages}">
            <span th:text="${msg.message}"></span>
            (<span th:text="${msg.createdAt}"></span>)
        </li>
    </ul>
</body>
</html>
```

**動作確認:**
1. アプリケーション起動
2. http://localhost:8080/test にアクセス
3. メッセージを入力して送信
4. データベースに保存されることを確認

**成果物:**
- `TestController.java`
- `test.html`
- 動作確認のスクリーンショット

---

## ✅ チェックリスト

- [ ] Spring BootのMVCパターンが理解できた
- [ ] プロジェクトのパッケージ構造が作成された
- [ ] Lombokが正しく動作する
- [ ] Entityクラスが作成された
- [ ] Repositoryが作成された
- [ ] Serviceクラスが作成された
- [ ] Controllerが作成された
- [ ] データベースにデータが保存できる
- [ ] Thymeleafテンプレートでデータ表示ができる
- [ ] GitHubにコミット・プッシュ済み

---

## 📚 参考リンク

- [Spring Data JPA公式ドキュメント](https://spring.io/projects/spring-data-jpa)
- [Lombok公式ドキュメント](https://projectlombok.org/)
- [Thymeleaf + Spring統合ガイド](https://www.thymeleaf.org/doc/tutorials/3.1/thymeleafspring.html)

---

## 🎉 完了後

[Day 5](day-05.md)の準備をする

お疲れさまでした！
