# サーバー設定

## ポート番号 8080
```java
server.port=8080
```
## コンテキストパス（アプリケーションのルートパス） 
💡アプリケーションにアクセスするURLの始まり
```java
server.servlet.context-path=/
```
## セッションタイムアウト　1800秒
```java
server.servlet.session.timeout=1800
```
## 最大HTTPヘッダーサイズ 8KB 
```java
server.max-http-header-size=8KB
```
💡HTTPヘッダー…アプリのブラウザ表示Body部分に含まれる以外の情報 通信方式やCookieなど

# データベース設定

## 接続プール設定 
 - 💡DBへの接続を確立して管理しておく設定
### 最大同時接続数　10
```java
spring.datasource.hikari.maximum-pool-size=10
```
### 最小アイドル接続数（確立しているが誰にも使われていない待機状態の接続）5
```java
spring.datasource.hikari.minimum-idle=5
```
### 接続を利用できるまでの最大待ち時間　20秒
```java
spring.datasource.hikari.connection-timeout=20000
```

## データベース初期化 
~~~java
spring.sql.init.mode=always
spring.sql.init.schema-locations=classpath:schema.sql
spring.sql.init.data-locations=classpath:data.sql
~~~
- 💡アプリ起動時に必要なテーブルやデータを用意する
# JPA/Hibernate設定

## DDL自動生成モード
 - none: 何もしない
 - validate: スキーマを検証のみ
 - **update: スキーマを更新（本番非推奨）**
 - create: 起動時にスキーマを作成（既存データ削除）
 - create-drop: 終了時にスキーマを削除
```java
spring.jpa.hibernate.ddl-auto=update
```
 💡DDL…データ定義言語　SQLなどのなかでDB内にあるテーブルなどの構造を操作する言語。  
 💡スキーマ…DBの構造や設計。何列あるかや主キーはどれかなどの設定　MySQLではデータベースそのものを指す

## SQL出力
```java
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```
💡実行したSQL文をコンソ－ルに表示し読みやすくする設定

## ネーミング戦略
```java
spring.jpa.hibernate.naming.physical-strategy=org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
```
 💡DBへテーブルの自動生成するときや、Entityと紐づけする際のテーブル名の規則を設定　この場合名前を変換せずそのままクラス名などをテーブル名にする

# ログ設定
💡アプリの起動・実行時のログをどこまで表示するかの設定

## ログレベル（TRACE, DEBUG, INFO, WARN, ERROR）
```java
logging.level.root=INFO
logging.level.com.example.weatherapp=DEBUG
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate.SQL=DEBUG
# SQL文のプレースホルダーに実際渡された値を確認する
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```
| ログレベル | 意味 | 例 |
|---|---|---|
| ERROR | エラー |動作・起動そのものができないエラー。DBへの接続に失敗したなど |
| WARN | 警告 |動作はするが、非推奨の設定が使われている |
| INFO| 一般的な情報 | アプリが起動した |
| DEBUG | 開発・調査用の詳細情報 |どの処理が実行されたか |
| TRACE | さらに細かい情報 | 内部処理の詳細な追跡 |

## ログファイル出力
```java
#ログファイルの名前と保存先設定
logging.file.name=logs/application.log
#一つのログファイルが10MBに達したら次の新しいファイルを作る
logging.file.max-size=10MB
#過去のログを30世代分まで保存する
logging.file.max-history=30
```
 - メモ：現在はログローテーション設定には別の設定名が使われているかも
 ```java
logging.logback.rollingpolicy.max-file-size=10MB
logging.logback.rollingpolicy.max-history=30
```


 # 環境別の設定ファイル

 ## 開発用
 ```java
 　　application-dev.properties
    # Development環境設定
    server.port=8080
    spring.jpa.hibernate.ddl-auto=update
    spring.jpa.show-sql=true
```
 ### 開発環境で起動
 ```
./gradlew bootRun --args='--spring.profiles.active=dev'
```

## 本番用
```java
    application-prod.properties
    # Production環境設定
    server.port=80
    spring.jpa.hibernate.ddl-auto=validate
    spring.jpa.show-sql=false
    logging.level.com.example.weatherapp=INFO
```
### 本番環境で起動
```
./gradlew bootRun --args='--spring.profiles.active=prod'
```