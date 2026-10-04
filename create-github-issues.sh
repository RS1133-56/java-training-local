#!/bin/bash
# GitHub CLI で Day 1〜40 の Issue を一括作成する
#
# 使い方:
#   ./create-github-issues.sh --dry-run   # 作成せず件数・タイトルだけ確認
#   ./create-github-issues.sh             # 実際に作成
#
# 事前準備:
#   - gh auth login 済みであること
#   - ラベル(training, day-1〜day-40)とマイルストーン(MILESTONE)を作成済みであること
#     詳細は GITHUB_IMPORT_GUIDE.md を参照
#
# 環境変数で上書き可能:
#   REPO="owner/name" MILESTONE="40日間研修" ./create-github-issues.sh

set -euo pipefail

REPO="${REPO:-kn-fd-creator/java-training-template}"
MILESTONE="${MILESTONE:-40日間研修}"
DRY_RUN=false
[ "${1:-}" = "--dry-run" ] && DRY_RUN=true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$SCRIPT_DIR/daily-tasks"

count=0
for day in $(seq 1 40); do
  FILE="$TASK_DIR/day-$(printf "%02d" "$day").md"

  if [ ! -f "$FILE" ]; then
    echo "⚠ Day $day のファイルが見つかりません: $FILE"
    continue
  fi

  # 1行目は「# Day N: タイトル」なので、先頭の「# 」だけ除いてそのままタイトルにする
  TITLE=$(head -n 1 "$FILE" | sed 's/^# *//')

  if $DRY_RUN; then
    echo "[dry-run] $TITLE  (labels: training,day-$day)"
  else
    gh issue create \
      --repo "$REPO" \
      --title "$TITLE" \
      --body-file "$FILE" \
      --label "training,day-$day" \
      --milestone "$MILESTONE"
    echo "✓ $TITLE を作成"
    sleep 1  # API制限対策
  fi
  count=$((count + 1))
done

if $DRY_RUN; then
  echo "🔍 dry-run 完了: ${count}件(宛先: $REPO / マイルストーン: $MILESTONE)"
else
  echo "🎉 ${count}件のIssueを作成しました"
fi
