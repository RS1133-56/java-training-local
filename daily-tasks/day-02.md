# Day 2: 開発環境のセットアップ

## 📅 実施日
- 予定: Week 1 - Day 2
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
開発に必要なツール（JDK、IntelliJ IDEA、MySQL、Postman、ブラウザ）をインストールし、動作確認を完了する

> ℹ️ GitとGitHub（GitHub CLIを含む）のセットアップは、[Day 1](day-01.md)で完了しています。

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

### 3. ブラウザと通信環境の確認（11:00-12:00）

**手順:**
1. **Google Chrome のインストール**（未インストールの場合）
   - https://www.google.com/chrome/
   - この研修では、Chrome の**開発者ツール**（`F12`キー）を、画面の確認やデバッグで使います
   - 開発者ツールの「Elements」「Console」「Network」タブを、一度ずつ開いて確認する

2. **研修で使うサイトに接続できるか確認**（ブラウザで開く）
   | サイト | 用途 | 確認方法 |
   |---|---|---|
   | https://start.spring.io/ | Spring Initializr（Day 3） | ページが表示される |
   | https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current=temperature_2m | 天気API（Day 6以降） | JSONが表示される |
   | https://app.diagrams.net/ | draw.io（Day 8以降） | 画面が表示される |
   | https://repo.maven.apache.org/maven2/ | ライブラリのダウンロード（Day 3以降） | ページが表示される |

3. **連絡手段の確認**
   - Teamsの研修課題用チャネルを開けること
   - テスト投稿をして、メンターに届くこと

> ⚠️ 開けないサイトがある場合は、社内ネットワークの制限（プロキシなど）の可能性があります。
> そのまま進めず、**今日のうちに**Teamsで質問してください（後のDayで詰まる原因になります）。

**成果物:**
- スクリーンショット: Chrome の開発者ツール
- 上の表の確認結果（開けた／開けなかった）

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
   
   ### Git / GitHub（Day 1で設定済み）
   - Gitのバージョン: [バージョンを記載]
   - GitHub CLI（gh）のバージョン: [バージョンを記載]
   - GitHubのユーザー名: [名前]
   - リポジトリのURL: [フォークしたリポジトリのURL]
   
   ### MySQL
   - バージョン: [バージョンを記載]
   - ポート: 3306
   - データベース: weather_app
   
   ### Postman
   - バージョン: [バージョンを記載]
   - テスト結果: 成功
   
   ### Chrome
   - バージョン: [バージョンを記載]
   - 研修で使うサイトへの接続: [すべてOK／NGがあれば記載]
   
   ## 動作確認
   - [ ] Java実行確認
   - [ ] IntelliJ IDEA起動確認
   - [ ] Git操作確認（`git --version`、`gh auth status`）
   - [ ] MySQL接続確認
   - [ ] Postman動作確認
   - [ ] Chromeと研修で使うサイトへの接続確認
   
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
- [ ] ChromeがインストールされF12の開発者ツールが開ける
- [ ] 研修で使うサイト（Spring Initializr、Open-Meteo API、draw.io）に接続できる
- [ ] Teamsの研修課題用チャネルにテスト投稿できた
- [ ] MySQLがインストールされ、データベースが作成されている
- [ ] MySQL Workbenchで接続できる
- [ ] Postmanがインストールされ、APIリクエストが成功する
- [ ] `setup-complete.md`が作成されている
- [ ] スクリーンショットが保存されている

---

## 📚 参考リンク

- [OpenJDK公式サイト](https://adoptium.net/)
- [IntelliJ IDEA公式ドキュメント](https://www.jetbrains.com/help/idea/)
- [MySQL公式ドキュメント](https://dev.mysql.com/doc/)
- [Postman学習センター](https://learning.postman.com/)

---

## 🆘 トラブルシューティング

### JDKのインストールで問題が発生した場合
- 環境変数が正しく設定されているか確認
- 複数のJavaバージョンがインストールされていないか確認

### ネットワークの制限でサイトに接続できない場合
- 開けないサイトのURLと、表示されるエラー（「接続できません」「証明書エラー」など）をメモする
- 社内ネットワークのプロキシ設定が必要な場合があるため、メンターに確認する

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
2. [Day 3](day-03.md)の準備をする（明日は、GradleとSpring Bootプロジェクトを作成します）

お疲れさまでした！
