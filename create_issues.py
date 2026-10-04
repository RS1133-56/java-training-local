#!/usr/bin/env python3
"""
GitHubのissueを一括作成するスクリプト

使い方:
  python3 create_issues.py --dry-run   # 作成せずタイトルだけ確認
  python3 create_issues.py             # 実際に作成（要 GITHUB_TOKEN）
"""

import re
import requests
import time
import os
import sys
from pathlib import Path

# 設定（環境変数で上書き可能）
# GITHUB_TOKEN は直書きせず環境変数で渡す: export GITHUB_TOKEN=xxxx
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = os.environ.get("REPO_OWNER", "kn-fd-creator")
REPO_NAME = os.environ.get("REPO_NAME", "java-training-template")
MILESTONE_TITLE = os.environ.get("MILESTONE", "40日間研修")
DRY_RUN = "--dry-run" in sys.argv

# GitHubのissue作成用ベースURL
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

# ヘッダー
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_milestone_number():
    """マイルストーン名から番号を取得（未作成ならNone）"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/milestones?state=all&per_page=100"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    for m in response.json():
        if m["title"] == MILESTONE_TITLE:
            return m["number"]
    return None


def create_issue(day_number, title, body, labels=None, milestone=None):
    """issueを作成（titleは「Day N: ...」形式のものをそのまま使う）"""
    
    data = {
        "title": title,
        "body": body,
        "labels": labels or ["training", f"day-{day_number}"],
    }
    if milestone:
        data["milestone"] = milestone
    
    if DRY_RUN:
        print(f"[dry-run] {title}  (labels: {data['labels']})")
        return True
    
    try:
        response = requests.post(BASE_URL, json=data, headers=HEADERS)
        
        if response.status_code == 201:
            print(f"✓ Day {day_number} のissue作成成功")
            return True
        else:
            print(f"✗ Day {day_number} のissue作成失敗: {response.status_code}")
            print(f"  エラー: {response.json()}")
            return False
            
    except Exception as e:
        print(f"✗ エラー発生: {e}")
        return False

def main():
    """メイン処理"""
    
    # Day 1-40のmarkdownファイルを処理
    daily_tasks_dir = Path(__file__).resolve().parent / "daily-tasks"
    
    milestone = None
    if not DRY_RUN:
        milestone = get_milestone_number()
        if milestone is None:
            print(f"⚠ マイルストーン「{MILESTONE_TITLE}」が見つかりません。先に作成してください")
            sys.exit(1)
    
    success_count = 0
    fail_count = 0
    
    for day in range(1, 41):
        file_path = daily_tasks_dir / f"day-{day:02d}.md"
        
        if not file_path.exists():
            print(f"⚠ Day {day} のファイルが見つかりません")
            continue
        
        # ファイル読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # タイトル抽出（1行目「# Day N: タイトル」から先頭の # だけ除去）
        lines = content.split('\n')
        title = re.sub(r'^#\s*', '', lines[0]).strip()
        
        # issue作成
        if create_issue(day, title, content, milestone=milestone):
            success_count += 1
        else:
            fail_count += 1
        
        # API制限対策（1秒待機）
        time.sleep(1)
    
    print("\n" + "="*50)
    print(f"🎉 処理完了！")
    print(f"  成功: {success_count}件")
    print(f"  失敗: {fail_count}件")
    print("="*50)

if __name__ == "__main__":
    print("GitHub Issue一括作成スクリプト")
    print("="*50)
    
    # トークン確認（dry-runでは不要）
    if not GITHUB_TOKEN and not DRY_RUN:
        print("⚠ エラー: 環境変数 GITHUB_TOKEN を設定してください")
        print("1. https://github.com/settings/tokens でトークン作成")
        print("2. export GITHUB_TOKEN=xxxx を実行")
        print("   （確認だけなら --dry-run を付けて実行）")
        exit(1)
    
    main()
