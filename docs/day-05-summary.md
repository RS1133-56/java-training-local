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

はじめは知らない用語が多かったが、切り分けて学習することで少しずつ理解できた。
環境ごとのapplication.properties設定ファイルは、今のところすべてかいているがもしかすると要らないのかもしれない。

## 明日への準備

- Open-Meteo APIの公式ドキュメントを読む
- 要件定義の書き方を調べる