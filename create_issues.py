#!/usr/bin/env python3
"""
GitHubのissueを一括作成するスクリプト

使い方:
  python3 create_issues.py --dry-run   # 作成せずタイトルだけ確認
  python3 create_issues.py             # 実際に作成（要 GITHUB_TOKEN）
  python3 create_issues.py --yes       # 確認なしで作成

本文中の相対リンク（day-NN.md）は、Issue上でも開けるよう
GitHub上のファイルへの絶対URL（mainブランチ）に書き換えて登録します。
"""

import re
import subprocess
import requests
import time
import os
import sys
from pathlib import Path

# 設定（環境変数で上書き可能）
# GITHUB_TOKEN は直書きせず環境変数で渡す: export GITHUB_TOKEN=xxxx
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def detect_repo():
    """宛先リポジトリを決める: 環境変数 REPO_OWNER/REPO_NAME > このフォルダの git remote origin"""
    owner, name = os.environ.get("REPO_OWNER"), os.environ.get("REPO_NAME")
    if owner and name:
        return owner, name
    try:
        url = subprocess.check_output(
            ["git", "-C", str(Path(__file__).resolve().parent), "remote", "get-url", "origin"],
            text=True,
        ).strip()
        m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if m:
            return m.group(1), m.group(2)
    except Exception:
        pass
    return None, None


REPO_OWNER, REPO_NAME = detect_repo()
MILESTONE_TITLE = os.environ.get("MILESTONE", "40日間研修")
DRY_RUN = "--dry-run" in sys.argv
ASSUME_YES = "--yes" in sys.argv or "-y" in sys.argv

# GitHubのissue作成用ベースURL
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

# ヘッダー
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_or_create_milestone():
    """マイルストーン番号を取得（無ければ作成）"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/milestones"
    response = requests.get(url, params={"state": "all", "per_page": 100}, headers=HEADERS)
    response.raise_for_status()
    for m in response.json():
        if m["title"] == MILESTONE_TITLE:
            return m["number"]
    response = requests.post(url, json={"title": MILESTONE_TITLE}, headers=HEADERS)
    response.raise_for_status()
    return response.json()["number"]


def ensure_labels():
    """ラベル(training, day-1〜day-40)を作成（既にあれば無視）"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/labels"
    labels = [("training", "0E8A16")] + [(f"day-{d}", "FBCA04") for d in range(1, 41)]
    for name, color in labels:
        requests.post(url, json={"name": name, "color": color}, headers=HEADERS)  # 422は既存なので無視


def get_existing_titles():
    """作成済みIssueのタイトル一覧（重複作成を防ぐ）"""
    titles = set()
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        response = requests.get(url, params={"state": "all", "per_page": 100, "page": page}, headers=HEADERS)
        response.raise_for_status()
        items = response.json()
        if not items:
            return titles
        titles.update(i["title"] for i in items if "pull_request" not in i)
        page += 1


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
    
    print(f"📌 宛先リポジトリ: {REPO_OWNER}/{REPO_NAME}")
    print(f"📌 マイルストーン: {MILESTONE_TITLE}\n")

    milestone = None
    existing_titles = set()
    if not DRY_RUN:
        if not ASSUME_YES and input("このリポジトリにIssueを40件作成します。よろしいですか？ (y/N): ").strip().lower() != "y":
            print("中止しました")
            return
        ensure_labels()
        milestone = get_or_create_milestone()
        existing_titles = get_existing_titles()
    
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
        
        # 作成済みならスキップ
        if title in existing_titles:
            print(f"- スキップ（作成済み）: {title}")
            continue
        
        # 相対リンク(day-NN.md)を絶対URLに書き換える
        body = re.sub(
            r"\]\((day-\d+\.md)\)",
            rf"](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/daily-tasks/\1)",
            content,
        )
        body = re.sub(
            r"\]\(\.\./([A-Za-z_]+\.md)\)",
            rf"](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/\1)",
            body,
        )
        
        # issue作成
        if create_issue(day, title, body, milestone=milestone):
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
    if not REPO_OWNER or not REPO_NAME:
        print("⚠ エラー: 宛先リポジトリを特定できません。REPO_OWNER / REPO_NAME を環境変数で指定してください")
        sys.exit(1)
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
