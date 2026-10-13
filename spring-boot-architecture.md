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
