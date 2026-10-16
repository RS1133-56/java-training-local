

# Java研修：Spring Boot開発環境構築・運用メモ

&#x20;2026年10月13日 動作確認完了

対象プロジェクト：`weather-app`

作業環境：Windows + WSL2 Ubuntu + VSCode

## 1. 現在の開発環境

| 項目             | バージョン・設定                |
| -------------- | ----------------------- |
| OS             | Ubuntu（WSL2）            |
| IDE            | VSCode                  |
| Java           | Temurin OpenJDK 17.0.20 |
| Spring Boot    | 3.5.16                  |
| Gradle Wrapper | 8.14.3                  |
| グローバルGradle    | 9.8.0                   |
| ビルド設定          | Gradle Groovy DSL       |
| Docker Engine  | 29.8.2                  |
| Docker Desktop | 4.94.0                  |
| MySQL          | 8.0.46                  |
| データベース         | `weather_app`           |
| Gitリポジトリ       | `java-training-local`   |

プロジェクトの場所：

```
~/workspace/java-training-local/
├── .git/
├── docker-compose.yml
└── weather-app/
    ├── .env
    ├── build.gradle
    ├── settings.gradle
    ├── gradlew
    ├── gradle/
    └── src/
        └── main/
            ├── java/
            └── resources/
                └── application.properties
```

`.env` は作成済みであることを前提とした構成だよ。

## 2. 今回発生した問題と対処方法

| 問題                             | 原因と対処                                                              |
| ------------------------------ | ------------------------------------------------------------------ |
| Spring Initializrに3.5.xが表示されない | Initializrが4.x以降のみ受け付けていた。4.1.1のひな形を生成し、`build.gradle` を3.5.16用に変更 |
| Gradle 9.8.0をインストールしてしまった      | アンインストール不要。Gradle Wrapperで8.14.3を使用                                |
| `./gradlew build` でテスト失敗       | DB接続設定が不足。MySQLを起動し、`application.properties` に接続情報を設定              |
| Dockerコマンドが見つからない              | Docker DesktopのWSL Integrationが利用できない状態。連携設定と再起動で復旧                |
| WSLがタイムアウトする                   | `Wsl/Service/0x8007274c`。`wsl --shutdown` 後、Ubuntuの起動を確認           |
| Dockerのコンテナが消えていた              | 既存ボリュームは残存。`docker compose up -d db` で再作成                          |
| DBパスワードの管理                     | `.env` に保存して環境変数として読み込み、Git管理から除外                                  |
| Spring Bootが起動するか不安            | `./gradlew clean build` が成功し、`bootRun` でHello World表示を確認           |

### Spring Bootのバージョン修正

`build.gradle` のプラグイン設定：

```
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.5.16'
    id 'io.spring.dependency-management' version '1.1.7'
}
```

Gradle Wrapperの設定ファイル：

`gradle/wrapper/gradle-wrapper.properties`

```
distributionUrl=https\://services.gradle.org/distributions/gradle-8.14.3-bin.zip
```

普段の作業では、Gradle 9.8.0ではなく `./gradlew` を使うこと。

## 3. 毎日の作業開始手順

# 作業開始チェックリスト

- [ ] WindowsでDocker Desktopを起動
- [ ] Ubuntu（WSL2）を起動
- [ ] MySQLコンテナを起動
- [ ] weather-appディレクトリに移動
- [ ] DB_PASSWORDを読み込む
- [ ] Spring Bootを起動



### ① Docker Desktopを起動

Windows側でDocker Desktopを起動する。

Ubuntuのターミナルで動作確認：

```
docker info
```

エラーなくサーバー情報が表示されればOK。

### ② MySQLコンテナの起動確認

```
cd ~/workspace/java-training-local
docker compose ps
```

`java-training-local-db-1` が `Up` なら起動済み。

停止している、または存在しない場合は、

```
docker compose up -d db
```

で起動する。

### ③ Spring Bootプロジェクトへ移動

```
cd ~/workspace/java-training-local/weather-app
```

### ④ DBパスワードを読み込む

`.env` に `DB_PASSWORD` を保存している場合：

```
set -a
source .env
set +a
```

環境変数を確認：

```
[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD is set"
```

`DB_PASSWORD is set` と表示されればOK。

※ 新しいターミナルでは再度読み込みが必要。VSCodeの実行機能から起動する場合も、そのプロセスに環境変数が渡るようにする。

### ⑤ VSCodeで開く

```
code .
```

VSCode左下が `WSL: Ubuntu` になっていることを確認する。

### ⑥ Spring Bootを起動

```
./gradlew bootRun
```

ブラウザで、

[http://localhost:8080](http://localhost:8080)

にアクセスする。

今回作成したHello Worldが表示されればOK。

※ Gradle Wrapperや依存関係のダウンロードは初回のみ。普段は再ダウンロードされない。

## 4. 作業終了時の手順

作業終了チェックリスト

Spring Bootを Ctrl+C で停止

必要に応じて変更内容をGitに保存

MySQLコンテナを停止

VSCodeとUbuntuの作業を終了

0 / 4 完了リセット

### ① Spring Bootを停止

`./gradlew bootRun` を実行しているターミナルで、

`Ctrl + C`

これでSpring Bootを終了できる。

### ② Gitの変更状態を確認

```
cd ~/workspace/java-training-local
git status
```

変更内容を確認して、必要ならコミット。

```
git add weather-app
git commit -m "Update weather app"
```

コミット前には `.env` がGitの管理対象に含まれていないことを確認してね。リモートに反映するなら、そのあと `git push` を実行する。

### ③ MySQLコンテナを停止

```
cd ~/workspace/java-training-local
docker compose stop db
```

`stop` はコンテナを停止するだけで、データベースのデータは削除しないよ。

毎回必ず停止する必要はないけれど、作業が終わって使わないなら停止しておいていい。

### ④ Docker Desktopを終了

Docker Desktop自体も使わないなら、Windows側で終了してOK。

WSLを完全に停止したいときはWindowsのPowerShellで、

```
wsl --shutdown
```

を実行する。ただし、毎日の作業終了時に必須の操作ではないよ。ほかのWSL環境もまとめて停止するので、必要なときだけ使おう。

## 5. よく使うコマンド早見表

| 操作            | コマンド                                     |
| ------------- | ---------------------------------------- |
| Spring Boot起動 | `./gradlew bootRun`                      |
| Spring Boot停止 | `Ctrl + C`                               |
| ビルド＋テスト       | `./gradlew build`                        |
| クリーンビルド       | `./gradlew clean build`                  |
| テストのみ         | `./gradlew test`                         |
| テストを除くビルド     | `./gradlew build -x test`                |
| Gradle確認      | `./gradlew --version`                    |
| Docker状態確認    | `docker compose ps`                      |
| MySQL起動       | `docker compose up -d db`                |
| MySQL停止       | `docker compose stop db`                 |
| MySQL接続       | `docker compose exec db mysql -uroot -p` |
| VSCode起動      | `code .`                                 |

Docker Composeのコマンドは `java-training-local` ディレクトリで、Gradleコマンドは `weather-app` ディレクトリで実行すること。

## 6. 特に注意したいこと

データベースを消さないこと

今回MySQLのデータはDockerの `java-training-local_mysql_data` ボリュームに保存されていたよ。

`docker compose stop` は安全に停止するためのコマンドだけど、

```
docker compose down -v
```

はボリュームも削除する可能性があるので、普段は使わないこと。

パスワードをGitに登録しないこと

`.env` がGit管理から除外されているかは、

```
git check-ignore weather-app/.env
```

で確認できる。これはリポジトリのルートで実行してね。対象パスが表示されれば除外設定が効いているよ。

また、今のDB接続はrootユーザーを使っているので、研修の進行に合わせてアプリ専用ユーザーに切り替えるとより安全だね。

DockerがまたWSLから使えなくなった場合

再インストールする前に、Docker DesktopのWSL Integrationを確認すること。

WSL自体が応答しない場合は、今回成功した `wsl --shutdown` と `wsl -d Ubuntu -e whoami` による切り分けが役立つよ。

これで、今回のトラブルと復旧方法、毎日の起動・終了手順をひと通りまとめられたよ。

特に今後の普段の作業は、Docker起動 → MySQL起動 → `.env` 読み込み → `./gradlew bootRun` という流れを覚えておけば大丈夫。

最初の環境構築は大変だったけど、ここから先は毎回GradleやDockerを設定し直す必要はないからね。