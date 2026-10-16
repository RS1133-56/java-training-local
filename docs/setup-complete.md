# 環境構築完了レポート

## インストール済みツール

### JDK
- バージョン: [openjdk 17.0.20]
- インストールパス: [/home/roiko/.sdkman/candidates/java/17.0.20-tem/bin/java]

### VSCode
- バージョン: [1.140.0]
- インストール済みプラグイン: [
ms-ceintl.vscode-language-pack-ja
redhat.java
vscjava.vscode-gradle
vscjava.vscode-java-debug
vscjava.vscode-java-dependency
vscjava.vscode-java-pack
vscjava.vscode-java-test
vscjava.vscode-maven
]

### Git / GitHub（Day 1で設定済み）
- Gitのバージョン: [git version 2.53.0]
- GitHub CLI（gh）のバージョン: [2.102.0]
- GitHubのユーザー名: [RS1133-56]
- リポジトリのURL: [https://github.com/RS1133-56/java-training-local)]

### MySQL
- バージョン: [バージョンを記載]
- ポート: 3306
- データベース: weather_app

### Postman
- バージョン: [12.31.3]
- テスト結果: 成功

### Chrome
- バージョン: [154.0.8037.98（公式ビルド） （64 ビット）]
- 研修で使うサイトへの接続: [すべてOK]

## 動作確認
- [◯] Java実行確認
- [◯] IntelliJ IDEA起動確認
- [◯] Git操作確認（`git --version`、`gh auth status`）
- [◯] MySQL接続確認
- [◯] Postman動作確認
- [◯] Chromeと研修で使うサイトへの接続確認

## 問題と解決策
[　MySQLのポート競合
→java-trainingの方はDockerコンテナでたて、別研修で使用しているものはポート3307にして解決

]

## 完了日時
[10/9 9:55]