#!/bin/bash
# GitHub CLI で Day 1〜40 の Issue を一括作成する
#
# 使い方（自分のリポジトリ＝フォークをcloneしたフォルダで実行）:
#   ./create-github-issues.sh --dry-run   # 作成せず、宛先・件数・タイトルだけ確認
#   ./create-github-issues.sh             # 実際に作成（実行前に宛先の確認あり）
#
# 事前準備:
#   - GitHub CLI(gh) をインストールし、gh auth login 済みであること
#   - Windows の場合は Git Bash で実行すること
#
# 動作:
#   - 宛先は「このフォルダの git remote origin」＝あなたのリポジトリになります
#   - ラベル(training, day-1〜day-40)とマイルストーンが無ければ自動で作成します
#   - 既に同じタイトルのIssueがある場合はスキップします（再実行しても重複しません）
#
# 環境変数で上書き可能:
#   REPO="owner/name"  MILESTONE="40日間研修"

set -euo pipefail

MILESTONE="${MILESTONE:-40日間研修}"
DRY_RUN=false
[ "${1:-}" = "--dry-run" ] && DRY_RUN=true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$SCRIPT_DIR/daily-tasks"

# 宛先リポジトリ: 環境変数 REPO > git remote origin
if [ -z "${REPO:-}" ]; then
  ORIGIN_URL="$(git -C "$SCRIPT_DIR" remote get-url origin 2>/dev/null || true)"
  REPO="$(echo "$ORIGIN_URL" | sed -E 's#^(git@github\.com:|https://github\.com/)##; s#\.git$##')"
fi
if [ -z "$REPO" ]; then
  echo "❌ 宛先リポジトリを特定できません。REPO=\"owner/name\" を指定してください"
  exit 1
fi

echo "📌 宛先リポジトリ : $REPO"
echo "📌 マイルストーン : $MILESTONE"
echo

if ! $DRY_RUN; then
  read -r -p "このリポジトリにIssueを40件作成します。よろしいですか？ (y/N): " ANSWER
  [ "$ANSWER" = "y" ] || [ "$ANSWER" = "Y" ] || { echo "中止しました"; exit 0; }

  echo "🏷  ラベルを準備中..."
  gh label create "training" --repo "$REPO" --color 0E8A16 --description "研修課題" --force >/dev/null
  for day in $(seq 1 40); do
    gh label create "day-$day" --repo "$REPO" --color FBCA04 --force >/dev/null
  done

  echo "🎯 マイルストーンを準備中..."
  if ! gh api "repos/$REPO/milestones?state=all&per_page=100" --jq '.[].title' | grep -Fxq "$MILESTONE"; then
    gh api "repos/$REPO/milestones" -f title="$MILESTONE" >/dev/null
  fi

  EXISTING_TITLES="$(gh issue list --repo "$REPO" --state all --limit 500 --json title --jq '.[].title')"
fi

count=0
skipped=0
for day in $(seq 1 40); do
  FILE="$TASK_DIR/day-$(printf "%02d" "$day").md"

  if [ ! -f "$FILE" ]; then
    echo "⚠ Day $day のファイルが見つかりません: $FILE"
    continue
  fi

  # 1行目は「# Day N: タイトル」なので、先頭の「# 」だけ除いてそのままタイトルにする
  TITLE="$(head -n 1 "$FILE" | tr -d '\r' | sed 's/^# *//')"

  if $DRY_RUN; then
    echo "[dry-run] $TITLE  (labels: training,day-$day)"
    count=$((count + 1))
    continue
  fi

  if echo "$EXISTING_TITLES" | grep -Fxq "$TITLE"; then
    echo "- スキップ（作成済み）: $TITLE"
    skipped=$((skipped + 1))
    continue
  fi

  gh issue create \
    --repo "$REPO" \
    --title "$TITLE" \
    --body-file "$FILE" \
    --label "training,day-$day" \
    --milestone "$MILESTONE" >/dev/null
  echo "✓ $TITLE を作成"
  count=$((count + 1))
  sleep 1  # API制限対策
done

if $DRY_RUN; then
  echo "🔍 dry-run 完了: ${count}件が作成対象です"
else
  echo "🎉 完了: 作成 ${count}件 / スキップ ${skipped}件"
fi
