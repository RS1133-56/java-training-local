# GitHub Issue 一括登録ガイド

Day 1-40をGitHubのissueに一括登録する3つの方法を紹介します。

---

## 方法1: GitHub CLI（一番簡単！）★おすすめ★

### 必要なもの
- GitHub CLI（gh コマンド）

### 手順

#### 1. GitHub CLIインストール

**Mac:**
```bash
brew install gh
```

**Windows:**
```bash
winget install --id GitHub.cli
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install gh

# RHEL/CentOS
sudo dnf install gh
```

#### 2. ログイン
```bash
gh auth login
```

#### 3. スクリプト実行

**宛先は、スクリプトを置いたフォルダの `git remote origin`（＝フォークした自分のリポジトリ）になります。** スクリプトの編集は不要です。
ラベル（`training`、`day-1`〜`day-40`）とマイルストーン（`40日間研修`）が無ければ自動で作成され、既に同じタイトルのIssueがある場合はスキップされます。
別のリポジトリに作る場合だけ `REPO="owner/name"` を指定します。

まず `--dry-run` で件数とタイトルを確認：
```bash
chmod +x create-github-issues.sh
./create-github-issues.sh --dry-run
# 別リポジトリの場合: REPO="owner/name" ./create-github-issues.sh --dry-run
```

問題なければ実行：
```bash
./create-github-issues.sh
```

※ ラベルとマイルストーンは自動で作成されます（手動で作る場合は下記「ラベルとマイルストーン」参照）。

これだけ！40件のissueが自動作成されます 🎉

---

## 方法2: Python + GitHub API

### 必要なもの
- Python 3.x
- requests ライブラリ
- GitHub Personal Access Token

### 手順

#### 1. GitHub Tokenを作成

1. https://github.com/settings/tokens にアクセス
2. "Generate new token (classic)" をクリック
3. `repo` 権限にチェック
4. トークンをコピー

#### 2. スクリプト編集

トークンはスクリプトに書かず、環境変数で渡します（誤ってコミットしないため）：
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
# 宛先はgit remote originから自動判定。別リポジトリの場合のみ: export REPO_OWNER=xxx REPO_NAME=yyy
```

#### 3. 実行

```bash
pip install requests
python3 create_issues.py --dry-run   # まず確認
python3 create_issues.py             # 実行
```

---

## 方法3: CSV + 手動インポート

### 手順

#### 1. CSVファイルを使用
`github-issues.csv` が既に生成されています。

#### 2. GitHub Projectsでインポート

1. GitHubリポジトリの "Projects" タブ
2. "New project" → "Table" を選択
3. "Import" → CSVファイルをアップロード
4. 各行を右クリック → "Convert to issue"

**メリット:** トークン不要  
**デメリット:** 手動操作が必要

---

## 方法4: GitHub Actions（自動化）

CI/CDパイプラインで自動的にissueを作成する方法もあります。

`.github/workflows/create-issues.yml` を作成：

```yaml
name: Create Training Issues

on:
  workflow_dispatch:  # 手動実行

jobs:
  create-issues:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Issues
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          for day in {1..40}; do
            FILE="daily-tasks/day-$(printf '%02d' $day).md"
            TITLE=$(head -n 1 "$FILE" | sed 's/# //')
            BODY=$(cat "$FILE")
            
            gh issue create \
              --title "Day $day: $TITLE" \
              --body "$BODY" \
              --label "training,day-$day"
              
            sleep 1
          done
```

---

## 比較表

| 方法 | 難易度 | 所要時間 | トークン必要 |
|------|--------|---------|-------------|
| GitHub CLI | ⭐ 簡単 | 5分 | 不要 |
| Python API | ⭐⭐ 中 | 10分 | 必要 |
| CSV手動 | ⭐⭐⭐ 面倒 | 30分 | 不要 |
| GitHub Actions | ⭐⭐ 中 | 15分 | 不要 |

---

## トラブルシューティング

### 認証エラー
```
gh auth login
```
で再ログインしてください。

### API Rate Limit
1時間に5000リクエストまでです。
スクリプト内のsleepで間隔を調整してください。

### トークンの権限不足
`repo` スコープが必要です。
トークンを再作成してください。

---

## おすすめ設定

### Labels（ラベル）を事前作成

```bash
gh label create "training" --color "0E8A16" --description "研修課題"
gh label create "day-1" --color "FBCA04"
gh label create "day-2" --color "FBCA04"
# ... (必要に応じて)
```

### Milestone（マイルストーン）作成

```bash
gh api repos/{owner}/{repo}/milestones \
  -f title="40日間研修" \
  -f description="新入社員向け天気アプリ開発研修"
```

---

## さらに便利に

### issue templateの活用

`.github/ISSUE_TEMPLATE/daily-task.md`:
```markdown
---
name: 日次タスク
about: 研修の日次タスク
labels: training
---

## 本日の目標

## タスク
- [ ] 

## 学んだこと

## 質問・相談
```

### Project boards連携

GitHubのProject（カンバンボード）と連携すると、
進捗管理が視覚的にできて便利です！

---

## まとめ

**初めての方:** 方法1（GitHub CLI）がおすすめ！  
**自動化したい方:** 方法4（GitHub Actions）  
**Pythonが好きな方:** 方法2（Python API）

どの方法でも、40日分のissueを簡単に作成できます 🚀

---

## 📋 issueの運用方法

### Day完了時のフロー

1. **Dayのタスクを完了**
   - チェックリストをすべて完了
   - コードをコミット・プッシュ
   - 実施日・実績時間を記録

2. **GitHubでissueを更新**
   - issueにコメントで完了報告
   - issueをクローズ

3. **次のDayへ**
   - 次のissueを開く

### issueコメント例

```markdown
## ✅ Day 1 完了報告

### 実施記録
- 実施日: 2024/11/26
- 予定時間: 8h
- 実績時間: 10h

### 完了チェックリスト
- [x] JDK 17インストール
- [x] IntelliJ IDEA設定
- [x] MySQLインストール
- [x] Gradleプロジェクト作成
- [x] 動作確認

### 学んだこと
- Gradleの基本的な使い方
- Spring Bootプロジェクトの構造

### 困ったこと・質問
- MySQLの初期設定でエラー
  → 文字コードの設定で解決

### 次のDay予定
Day 2: Gitの基本とGitHub連携
```

### ラベル活用例

**推奨ラベル:**
- `training` - 研修課題
- `in-progress` - 作業中
- `completed` - 完了
- `blocked` - 問題発生
- `question` - 質問あり
- `week-1` 〜 `week-8` - Week別

**使い方:**
1. Day開始時: `in-progress` ラベル追加
2. 完了時: `completed` ラベル追加 → Close
3. 問題発生: `blocked` ラベル追加
4. 解決後: `blocked` ラベル削除

### マイルストーン活用

```bash
# Week別マイルストーン作成
gh api repos/{owner}/{repo}/milestones \
  -f title="Week 1: 設計フェーズ" \
  -f description="Day 1-5" \
  -f due_on="2024-12-06T23:59:59Z"
```

各issueにマイルストーンを設定すると、Week別の進捗が見やすくなります。

### Project Board活用

GitHubのProjectsでカンバンボード作成：

**列の構成:**
- 📋 Backlog (未着手)
- 🚧 In Progress (作業中)
- ✅ Done (完了)

**自動化:**
- issueがOpenになったら "Backlog" へ
- `in-progress` ラベルで "In Progress" へ
- issueがCloseされたら "Done" へ

---

## 🎯 進捗の可視化

### GitHub Insightsの活用

**リポジトリの Insights タブで確認:**
- Pulse: 週次の活動サマリー
- Contributors: コントリビューション状況
- Commits: コミット履歴
- Issues: issue統計

### 進捗レポート自動生成

`.github/workflows/progress-report.yml`:

```yaml
name: Weekly Progress Report

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日0時

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate Report
        run: |
          echo "# 週次進捗レポート" > report.md
          echo "## 完了したDay" >> report.md
          
          # 完了issue数を取得
          CLOSED=$(gh issue list --state closed --label training --json number | jq length)
          TOTAL=40
          
          echo "進捗: $CLOSED/$TOTAL ($(($CLOSED * 100 / $TOTAL))%)" >> report.md
          
      - name: Post to Slack (optional)
        # Slackに通知する場合
        run: |
          # Slack Webhook実装
```

---

## 💡 Tips

### 一括操作

**完了したissueを一括でラベル付け:**
```bash
gh issue list --state closed --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "completed"
```

**Week別に進捗確認:**
```bash
# Week 1の進捗
gh issue list --label "week-1" --state all
```

### テンプレート活用

`.github/ISSUE_TEMPLATE/daily-task.md`:

```markdown
---
name: 日次タスク
about: 研修の日次タスク
labels: training
---

## Day X: タスク名

### 目標
[目標を記載]

### チェックリスト
- [ ] タスク1
- [ ] タスク2

### 完了報告（完了後に記入）
- 実施日: YYYY/MM/DD
- 実績時間: ___h

### メモ
[自由記述]
```

---

これで、GitHubで完璧に進捗管理できます！🎉
