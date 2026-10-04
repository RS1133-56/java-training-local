# Day 1: 開発環境のセットアップ

## 📅 実施日
- 予定: Week 1 - Day 1
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
開発に必要なすべてのツールをインストールし、動作確認を完了する

---

## 📋 午前の作業（9:00-13:00）

### 1. JDK 17のインストール（9:00-10:00）

**手順:**
1. OpenJDK 17をダウンロード
   - Windows: https://adoptium.net/
   - Mac: `brew install openjdk@17`
   - Linux: `sudo apt install openjdk-17-jdk`

2. 環境変数の設定
   - `JAVA_HOME`を設定
   - `PATH`に追加

3. 動作確認
   ```bash
   java -version
   javac -version
   ```

**成果物:**
- スクリーンショット: `java -version`の実行結果

---

### 2. IntelliJ IDEA Community Editionのインストール（10:00-11:00）

**手順:**
1. IntelliJ IDEA Community Editionをダウンロード
   - https://www.jetbrains.com/idea/download/

2. インストールと初期設定
   - テーマの選択（Darcula推奨）
   - フォントサイズの調整
   - キーマップの確認

3. プラグインのインストール（任意）
   - Japanese Language Pack（日本語化）
   - Rainbow Brackets

**成果物:**
- スクリーンショット: IntelliJ IDEAの起動画面

---

### 3. Gitのインストールと初期設定（11:00-12:00）

**手順:**
1. Gitのインストール
   - Windows: https://git-scm.com/download/win
   - Mac: `brew install git`
   - Linux: `sudo apt install git`

2. 初期設定
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   git config --global init.defaultBranch main
   ```

3. 動作確認
   ```bash
   git --version
   git config --list
   ```

**成果物:**
- `git config --list`のスクリーンショット

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. MySQLのインストールと設定（13:00-14:30）

**手順:**
1. MySQL 8.0のダウンロードとインストール
   - https://dev.mysql.com/downloads/mysql/

2. MySQL Serverの設定
   - rootパスワードの設定
   - ポート: 3306（デフォルト）

3. MySQL Workbenchのインストール
   - https://dev.mysql.com/downloads/workbench/

4. 接続確認
   ```bash
   mysql -u root -p
   ```

5. 研修用データベースの作成
   ```sql
   CREATE DATABASE weather_app;
   USE weather_app;
   ```

**成果物:**
- MySQL Workbenchの接続スクリーンショット
- データベース作成のスクリーンショット

---

### 5. Postmanのインストール（14:30-15:30）

**手順:**
1. Postmanのダウンロードとインストール
   - https://www.postman.com/downloads/

2. アカウント作成（無料プラン）

3. 簡単なGETリクエストのテスト
   - URL: `https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m`
   - Sendボタンをクリック
   - レスポンスを確認

**成果物:**
- Postmanでのリクエスト成功のスクリーンショット

---

### 6. 環境確認とドキュメント作成（15:30-17:00）

**手順:**
1. すべてのツールの動作確認チェックリスト作成

2. `setup-complete.md`ファイルの作成
   ```markdown
   # 環境構築完了レポート
   
   ## インストール済みツール
   
   ### JDK
   - バージョン: [ここにバージョンを記載]
   - インストールパス: [パスを記載]
   
   ### IntelliJ IDEA
   - バージョン: [バージョンを記載]
   - インストール済みプラグイン: [リストを記載]
   
   ### Git
   - バージョン: [バージョンを記載]
   - ユーザー名: [名前]
   - メールアドレス: [メール]
   
   ### MySQL
   - バージョン: [バージョンを記載]
   - ポート: 3306
   - データベース: weather_app
   
   ### Postman
   - バージョン: [バージョンを記載]
   - テスト結果: 成功
   
   ## 動作確認
   - [ ] Java実行確認
   - [ ] IntelliJ IDEA起動確認
   - [ ] Git操作確認
   - [ ] MySQL接続確認
   - [ ] Postman動作確認
   
   ## 問題と解決策
   [問題があれば記載]
   
   ## 完了日時
   [日時を記載]
   ```

3. スクリーンショットの整理
   - `screenshots/`フォルダを作成
   - 各ツールのスクリーンショットを保存

**成果物:**
- `setup-complete.md`
- スクリーンショット集（`screenshots/`フォルダ）

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] JDK 17がインストールされ、`java -version`が動作する
- [ ] IntelliJ IDEA Community Editionが起動する
- [ ] Gitがインストールされ、初期設定が完了している
- [ ] MySQLがインストールされ、データベースが作成されている
- [ ] MySQL Workbenchで接続できる
- [ ] Postmanがインストールされ、APIリクエストが成功する
- [ ] `setup-complete.md`が作成されている
- [ ] スクリーンショットが保存されている

---

## 📚 参考リンク

- [OpenJDK公式サイト](https://adoptium.net/)
- [IntelliJ IDEA公式ドキュメント](https://www.jetbrains.com/help/idea/)
- [Git公式ドキュメント](https://git-scm.com/doc)
- [MySQL公式ドキュメント](https://dev.mysql.com/doc/)
- [Postman学習センター](https://learning.postman.com/)

---

## 🆘 トラブルシューティング

### JDKのインストールで問題が発生した場合
- 環境変数が正しく設定されているか確認
- 複数のJavaバージョンがインストールされていないか確認

### MySQLの接続ができない場合
- MySQLサービスが起動しているか確認
- ファイアウォールの設定を確認
- ポート3306が使用可能か確認

### その他の問題
- 解決しない場合は、README の「質問の仕方」を参考に状況をまとめて、Teamsで質問する
- メンターに相談

---

## 🎉 完了後

すべてのチェックリストが完了したら：
1. `setup-complete.md`をメンターに提出
2. [Day 2](day-02.md)の準備をする
3. 明日の予習（Gitの基本概念を調べておく）

お疲れさまでした！
