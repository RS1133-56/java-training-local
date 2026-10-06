# Java研修プログラム - 40日間完全ガイド

## 📋 概要

このリポジトリは、JavaによるWebアプリケーション開発の40日間研修プログラムです。  
Git初心者から始めて、Spring Bootを使った実践的なWebアプリケーション開発まで段階的に学習します。

## 🎯 研修の目標

- **Gitの基本操作**をマスターする
- **Spring Boot**を使ったWebアプリケーション開発ができるようになる
- **REST API**の設計と実装ができる
- **データベース設計**と実装ができる
- 実務で必要な**設計ドキュメント**が作成できる

## 📅 研修スケジュール（40営業日）

### Week 1: 環境構築 & Git基礎（Day 1-5）
- Day 1: [Gitの基本操作とGitHubの準備](daily-tasks/day-01.md)
- Day 2: [開発環境のセットアップ](daily-tasks/day-02.md)
- Day 3: [環境構築完了とHello World](daily-tasks/day-03.md)
- Day 4: [Spring Boot基礎とプロジェクト作成](daily-tasks/day-04.md)
- Day 5: [Spring Boot Hello Worldの理解](daily-tasks/day-05.md)

### Week 2: 設計基礎（Day 6-10）
- Day 6: [要件定義とAPI調査](daily-tasks/day-06.md)
- Day 7: [API調査の詳細と動作確認](daily-tasks/day-07.md)
- Day 8: [画面設計（ワイヤーフレーム）](daily-tasks/day-08.md)
- Day 9: [画面遷移図の作成](daily-tasks/day-09.md)
- Day 10: [データベース設計（ER図）](daily-tasks/day-10.md)

### Week 3: 設計完成（Day 11-15）
- Day 11: [テーブル定義書とDDL作成](daily-tasks/day-11.md)
- Day 12: [初期データ投入](daily-tasks/day-12.md)
- Day 13: [シーケンス図作成（一覧表示）](daily-tasks/day-13.md)
- Day 14: [シーケンス図作成（詳細表示と履歴保存）](daily-tasks/day-14.md)
- Day 15: [設計レビューと修正](daily-tasks/day-15.md)

### Week 4: バックエンド実装（Day 16-20）
- Day 16: [Entityクラス実装](daily-tasks/day-16.md)
- Day 17: [Repository層実装](daily-tasks/day-17.md)
- Day 18: [DTO設計と実装](daily-tasks/day-18.md)
- Day 19: [Service層実装（Prefecture）](daily-tasks/day-19.md)
- Day 20: [外部API連携（OpenMeteoClient）](daily-tasks/day-20.md)

### Week 5: API実装（Day 21-25）
- Day 21: [Service層実装（Weather）](daily-tasks/day-21.md)
- Day 22: [Controller層実装（Home）](daily-tasks/day-22.md)
- Day 23: [Controller層実装（Weather）](daily-tasks/day-23.md)
- Day 24: [例外ハンドリング統一化](daily-tasks/day-24.md)
- Day 25: [バックエンド統合テスト](daily-tasks/day-25.md)

### Week 6: フロントエンド実装（Day 26-30）
- Day 26: [Thymeleafテンプレート基礎](daily-tasks/day-26.md)
- Day 27: [トップページ実装（index.html）](daily-tasks/day-27.md)
- Day 28: [天気詳細ページ実装（weather-detail.html）](daily-tasks/day-28.md)
- Day 29: [CSS基礎とスタイリング](daily-tasks/day-29.md)
- Day 30: [レスポンシブデザイン対応](daily-tasks/day-30.md)

### Week 7: 機能追加（Day 31-35）
- Day 31: [ローディング機能実装](daily-tasks/day-31.md)
- Day 32: [天気アイコン表示](daily-tasks/day-32.md)
- Day 33: [お気に入り機能実装](daily-tasks/day-33.md)
- Day 34: [エラーページの作成](daily-tasks/day-34.md)
- Day 35: [アクセシビリティ対応](daily-tasks/day-35.md)

### Week 8: テスト・完成（Day 36-40）
- Day 36: [テスト・品質保証](daily-tasks/day-36.md)
- Day 37: [ドキュメント作成](daily-tasks/day-37.md)
- Day 38: [パフォーマンス最適化](daily-tasks/day-38.md)
- Day 39: [最終レビュー・総合テスト](daily-tasks/day-39.md)
- Day 40: [成果発表準備・プロジェクト完成 🎉](daily-tasks/day-40.md)

## 🛠️ 使用技術

- **言語**: Java 17
- **フレームワーク**: Spring Boot 3.x
- **ビルドツール**: Gradle
- **データベース**: MySQL 8.0
- **テンプレートエンジン**: Thymeleaf
- **外部API**: Open-Meteo API
- **バージョン管理**: Git / GitHub

## 📦 開発環境

- **IDE**: IntelliJ IDEA Community Edition
- **JDK**: OpenJDK 17
- **MySQL**: MySQL 8.0
- **ツール**: Postman, MySQL Workbench

## 📚 成果物

### 設計ドキュメント
- 要件定義書
- API調査レポート
- 画面設計書（ワイヤーフレーム、画面遷移図）
- データベース設計書（ER図、テーブル定義）
- シーケンス図
- README.md

### 実装コード
- Spring Bootアプリケーション
- REST APIエンドポイント
- データベースマイグレーション
- Thymeleafテンプレート
- CSSスタイルシート
- テストコード

## 🎓 学習リソース

- [GitHubインポートガイド](GITHUB_IMPORT_GUIDE.md)（Issue一括登録・運用）
- [進捗管理ガイド](PROGRESS_GUIDE.md)（実績時間の記録と分析）
- 各Dayファイル内の「参考リンク」「トラブルシューティング」

## ✅ 完了基準

- [ ] 47都道府県の天気が表示できる
- [ ] 週間天気予報（7日間）が表示できる
- [ ] データベースに履歴が保存される
- [ ] レスポンシブデザインが機能する
- [ ] エラーハンドリングが適切
- [ ] お気に入り機能が動作する
- [ ] すべてのテストが成功する
- [ ] 全ドキュメントが揃っている

## 📞 サポート

質問や問題が発生した場合：
1. その日のIssue（Dayファイル）の「🆘 トラブルシューティング」欄で解決策を探す（全Dayに用意しています）
2. 解決しなければ、「質問の仕方」を参考に状況をまとめてTeamsで質問

## 🚀 始め方

### 1. 準備（最初の1回だけ）

**先に用意するもの（Issueを作る前に必要です）:**
- **GitHubアカウント**（無料）
- **Git**（Windowsの方は、一緒に入る **Git Bash** でコマンドを実行します）
- **GitHub CLI（`gh`）** とログイン（`gh auth login`）

> インストール手順は、[Day 1](daily-tasks/day-01.md) の「1. Gitのインストールと初期設定」「2. GitHubの準備」に書いてあります。
> このリポジトリの `daily-tasks/day-01.md` を開き、そこに従って先に進めてください。
> （Issueはまだ作られていないので、この時点では、リポジトリ内のファイルを読みます）

**手順:**

1. このリポジトリを**フォーク**する（自分のGitHubアカウントにコピーされます）
2. フォークした**自分のリポジトリ**をローカルにクローンする
   ```bash
   git clone https://github.com/<自分のユーザー名>/<リポジトリ名>.git
   cd <リポジトリ名>
   ```
3. 40日分のIssueを**一括作成**する（Git Bash / ターミナルで、クローンしたフォルダ内で実行）
   ```bash
   gh auth login                      # 初回のみ。ログインしておく
   ./create-github-issues.sh --dry-run   # 宛先とタイトルの確認（まだ作成しない）
   ./create-github-issues.sh             # 本番実行（宛先リポジトリが自分のものか確認して y）
   ```
   - ラベルとマイルストーンは自動で作られます
   - 手順の詳細・うまくいかない場合は [GitHubインポートガイド](GITHUB_IMPORT_GUIDE.md)
4. 自分のリポジトリの「Issues」タブに Day 1〜40 が並んでいることを確認し、**Day 1 のIssueから**研修を始める

### 2. 毎日の作業場所

- 作業は**自分のリポジトリの「Issues」タブ**から、その日の Day の Issue を開いて進めます
  - ⚠️ 他の人のリポジトリや、フォーク元の Issue ではなく、**自分のリポジトリ**の Issue です
  - Issue の内容を手でコピーして新しく作る必要はありません（一括作成で作られています）
- 日次レポートは、その Day の Issue の**コメント**に書き、作業が終わったら Issue を**クローズ**します
  （詳しくは下の「毎日の進め方」）

### 3. 困ったとき

- Issue 内のリンク（`day-XX.md` など）が「ページが見つかりません（404）」になるときは、
  リンクを辿らず、自分のリポジトリの **Issues タブ** から Day の Issue を直接開いてください
- それ以外は上の「サポート」を参照してください

---

## 📖 毎日の進め方

### 🌅 1日の基本フロー

#### 朝イチ
1. **今日のDayファイルを開く**
   - `daily-tasks/day-XX.md` を開く
   - 目標とタスク内容を確認

2. **GitHubでissueを確認**（GitHub管理の場合）
   - 今日のDayのissueを開く
   - `in-progress` ラベルを付ける

3. **前日の振り返り**
   - 前日の学びを簡単に復習
   - 疑問点があれば質問リストに追加

#### 午前 ~ 午後
1. **Issue内のタスクを実施**
   - Dayファイル内のタスクを順番に進める
   - コードを書きながら理解を深める
   - わからないことはメモしておく

2. **こまめにコミット**
   ```bash
   git add .
   git commit -m "feat: XXXを実装"
   git push origin main
   ```

   > 💡 ブランチ運用: Day 1 でブランチ・マージの操作を練習しますが、Day 2 以降の日々の作業は
   > **`main` ブランチに直接コミット・プッシュ**します（個人の研修なので、ブランチは切らなくてOKです）

3. **チェックリストを更新**
   - 完了したタスクにチェック

#### 終業前
1. **チェックリストの最終確認**
   - すべて完了しているか確認
   - 未完了があれば翌日に持ち越し

2. **実績を記録**
   ```markdown
   ## 📅 実施日
   - 実施日: 2024/11/26
   - 実績時間: 10h
   ```

3. **Gitにコミット・プッシュ**
   ```bash
   git add .
   git commit -m "chore: Day XX完了"
   git push origin main
   ```

4. **GitHubでissueをクローズ**（GitHub管理の場合）
   - issueに完了報告をコメント
   - issueをクローズ

5. **振り返り（5分）**
   - 日次レポート(下記日時レポート欄参照)を記載する

---

### 🎯 効果的な学習のコツ

#### ✅ DO（やるべきこと）

1. **手を動かす**
   - コピペだけでなく、自分で書く
   - エラーを恐れない

2. **理解してから進む**
   - わからないまま進まない
   - 疑問点は必ずメモ

3. **コミットを細かく**
   - 機能ごとにコミット
   - わかりやすいコミットメッセージ

4. **質問する**
   - 30分悩んだらAIに質問
   - 質問の仕方も学習の一部

5. **復習する**
   - 週末に1週間分を振り返る
   - 理解度を確認

#### ❌ DON'T（避けるべきこと）

1. **コピペだけで済ませない**
   - 理解せずに進むと後で困る

2. **エラーを放置しない**
   - エラーは学びのチャンス
   - 解決方法を記録

3. **ドキュメントを読まない**
   - 公式ドキュメントは最良の教材
   - 参考リンクを活用

4. **孤独に悩まない**
   - 困ったら相談
   - チームで学ぶ

---

### 📝 記録の取り方

#### 日次レポート

毎日の終わりに簡単にメモし、各日のIssue終端に記載：

```markdown
# Day XX 振り返り

## 完了したこと
- タスク1
- タスク2

## 学んだこと
1. XXXの仕組み
2. YYYの使い方
3. ZZZのパターン

## 困ったこと・解決方法
- 問題: XXXでエラー
- 解決: YYYを確認したら解決

## 明日への課題
- ZZZについて理解を深める
```

---

### 🔧 トラブル時の対処法

#### 1. エラーが出た
```
1. エラーメッセージを読む
2. Google検索（日本語＋英語）
3. 公式ドキュメント確認
4. Stack Overflow検索
5. 30分悩んだら質問
```

#### 2. 時間内に終わらない
```
1. 焦らない
2. 優先順位を確認
3. 翌日に持ち越しOK(時間は目安)
```

#### 3. 理解できない
```
1. 参考リンクを読む
2. 動画チュートリアル探す
3. 手を動かして実験
4. メンターに質問
```

#### 4. モチベーション低下
```
1. 小さな達成を祝う
2. 仲間と進捗共有
3. 目標を再確認
4. 休憩を取る
```

---

### 📊 進捗管理

#### GitHub Issues活用

詳細は [GitHubインポートガイド](GITHUB_IMPORT_GUIDE.md) を参照

**推奨フロー:**
```
1. 朝: 今日のissueをOpen
2. 作業中: in-progressラベル
3. 完了: 完了報告 → Close
```

#### 週次振り返り

毎週末（金曜日）に：

```markdown
# Week X 振り返り

## 進捗
- 完了: 5/5日
- 予定時間: 40h
- 実績時間: 45h

## 今週の学び
1. XXX
2. YYY
3. ZZZ

## 来週の目標
- XXXを重点的に
```

#### 進捗分析

各Dayファイルの「実施日」「実績時間」を記入したら、週次で分析スクリプトを実行：

```bash
python3 analyze_progress.py
```

詳細は [進捗管理ガイド](PROGRESS_GUIDE.md) を参照

### 🎓 学習リソースの活用

#### 公式ドキュメント
- Spring Boot: https://spring.io/projects/spring-boot
- Thymeleaf: https://www.thymeleaf.org/
- MySQL: https://dev.mysql.com/doc/

#### 推奨書籍
- Spring徹底入門
- Javaの絵本
- SQLアンチパターン

#### オンライン学習
- Udemy
- Coursera
- YouTube

---

### 💬 質問の仕方

**良い質問:**
```markdown
## Day 16で発生した問題

### 環境
- OS: Windows 11
- Java: 17
- IDE: IntelliJ IDEA

### やりたいこと
Entityクラスを作成したい

### 発生している問題
@Entityアノテーションがエラーになる

### エラーメッセージ
```
Cannot resolve symbol 'Entity'
```

### 試したこと
1. build.gradleを確認 → spring-boot-starter-data-jpaはある
2. Gradleをリフレッシュ → 変わらず
3. IntelliJを再起動 → 変わらず

### 質問
依存関係は正しいのに認識されない理由は？
```

**避けるべき質問:**
```
エラーが出ます。助けてください。
```

---

## 🎉 40日後のゴール

この研修を完走すると：

✅ Spring Bootアプリを1から作れる  
✅ データベース設計ができる  
✅ REST APIが設計・実装できる  
✅ Gitが使いこなせる  
✅ 実務レベルのコードが書ける  
✅ 問題解決能力が身につく  
✅ チーム開発の基礎ができる  
✅ 自走できるエンジニアになれる  

**がんばってください！40日後には立派なJava Webエンジニアです！🎉**
