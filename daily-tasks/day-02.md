# Day 2: Gitの基本操作をマスターする

## 📅 実施日
- 予定: Week 1 - Day 2
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Gitの基本操作（clone, branch, commit, push, pull, fetch, rebase, merge）を習得し、GitHubでの開発フローを理解する

---

## 📋 午前の作業（9:00-13:00）

### 1. Gitの基礎概念の学習（9:00-10:00）

**学習内容:**
- バージョン管理とは？
- Gitの仕組み（ローカルリポジトリ / リモートリポジトリ）
- GitとGitHubの違い
- ワーキングディレクトリ、ステージングエリア、コミット履歴

**演習:**
1. 以下の概念を自分の言葉で説明できるようにする
   - リポジトリ
   - コミット
   - ブランチ
   - リモート

2. `git-concepts.md`ファイルを作成し、学んだことをまとめる

**成果物:**
- `git-concepts.md`

---

### 2. GitHubアカウント作成とリポジトリのクローン（10:00-11:00）

**手順:**
1. GitHubアカウントの作成
   - https://github.com/signup
   - ユーザー名、メールアドレス、パスワードを設定

2. 研修用リポジトリのフォーク
   - 研修用テンプレートリポジトリをフォーク
   - 自分のGitHubアカウントにコピーされる

3. ローカルへのクローン
   ```bash
   cd ~/workspace
   git clone https://github.com/YOUR_USERNAME/java-training.git
   cd java-training
   ```

4. リポジトリの確認
   ```bash
   git status
   git log
   git remote -v
   ```

**成果物:**
- GitHubアカウント
- クローンされたローカルリポジトリ

---

### 3. 基本コマンドの練習（11:00-12:00）

**手順:**
1. 練習用ファイルの作成
   ```bash
   touch practice.txt
   echo "Hello Git" > practice.txt
   ```

2. `git status`で状態確認
   ```bash
   git status
   # Untracked filesとして表示される
   ```

3. `git add`でステージングエリアに追加
   ```bash
   git add practice.txt
   git status
   # Changes to be committedとして表示される
   ```

4. `git commit`でコミット
   ```bash
   git commit -m "feat: 練習用ファイルを追加"
   ```

5. コミット履歴の確認
   ```bash
   git log
   git log --oneline
   ```

**演習:**
- 10回以上コミットを作成する
- コミットメッセージは意味のあるものにする

**成果物:**
- 10個以上のコミット履歴

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. ブランチ操作の練習（13:00-14:30）

**手順:**
1. ブランチの作成
   ```bash
   git branch feature/profile
   git branch
   # * main
   #   feature/profile
   ```

2. ブランチの切り替え
   ```bash
   git checkout feature/profile
   # または
   git switch feature/profile
   ```

3. ブランチ作成と切り替えを同時に行う
   ```bash
   git checkout -b feature/readme
   # または
   git switch -c feature/readme
   ```

4. ブランチでの作業
   ```bash
   # feature/profileブランチに移動
   git switch feature/profile
   
   # profile.mdを作成
   touch profile.md
   echo "# 自己紹介" > profile.md
   
   # コミット
   git add profile.md
   git commit -m "feat: 自己紹介ファイルを追加"
   ```

**演習:**
- 3つ以上のブランチを作成
- 各ブランチで異なるファイルを編集

**成果物:**
- 複数のブランチ
- 各ブランチでのコミット

---

### 5. merge操作の練習（14:30-15:30）

**手順:**
1. mainブランチに戻る
   ```bash
   git switch main
   ```

2. feature/profileブランチをマージ
   ```bash
   git merge feature/profile
   ```

3. マージ後の確認
   ```bash
   git log --oneline --graph --all
   ```

4. コンフリクトの発生と解決
   ```bash
   # mainブランチでREADME.mdを編集
   echo "Main branch" >> README.md
   git add README.md
   git commit -m "docs: README更新(main)"
   
   # feature/readmeブランチに移動
   git switch feature/readme
   
   # 同じ場所を編集
   echo "Feature branch" >> README.md
   git add README.md
   git commit -m "docs: README更新(feature)"
   
   # mainにマージしてコンフリクト発生
   git switch main
   git merge feature/readme
   # CONFLICT (content): Merge conflict in README.md
   
   # コンフリクトを解決
   # エディタでREADME.mdを開き、<<<<<<< ======= >>>>>>>を削除
   git add README.md
   git commit -m "merge: feature/readmeをマージ"
   ```

**成果物:**
- マージ済みのブランチ
- コンフリクト解決の経験

---

### 6. push/pull/fetch操作の練習（15:30-16:30）

**手順:**
1. リモートへのpush
   ```bash
   git push origin main
   ```

2. 新しいブランチをリモートにpush
   ```bash
   git switch -c feature/test
   touch test.txt
   git add test.txt
   git commit -m "feat: テストファイル追加"
   git push origin feature/test
   ```

3. リモートの変更をfetch
   ```bash
   git fetch origin
   git branch -r  # リモートブランチ一覧
   ```

4. リモートの変更をpull
   ```bash
   git switch main
   git pull origin main
   ```

**成果物:**
- GitHubにpushされたコミット
- リモートとローカルの同期

---

### 7. rebase操作の練習（16:30-17:00）

**手順:**
1. 新しいブランチを作成
   ```bash
   git switch -c feature/rebase-test
   echo "Rebase test" > rebase.txt
   git add rebase.txt
   git commit -m "feat: rebaseテスト"
   ```

2. mainブランチで新しいコミット
   ```bash
   git switch main
   echo "Main update" > main-update.txt
   git add main-update.txt
   git commit -m "feat: main更新"
   ```

3. feature/rebase-testでrebase
   ```bash
   git switch feature/rebase-test
   git rebase main
   ```

4. mergeとrebaseの違いを確認
   ```bash
   git log --oneline --graph --all
   ```

**学習ポイント:**
- `merge`: 履歴が分岐する
- `rebase`: 履歴が一直線になる

**成果物:**
- rebase完了後の履歴
- `merge-vs-rebase.md`（違いをまとめたドキュメント）

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [ ] GitHubアカウントが作成されている
- [ ] リポジトリがクローンされている
- [ ] `git status`, `git add`, `git commit`が使える
- [ ] ブランチの作成・切り替えができる
- [ ] `git merge`でブランチを統合できる
- [ ] コンフリクトを解決できる
- [ ] `git push`でリモートに送信できる
- [ ] `git pull`でリモートから取得できる
- [ ] `git fetch`と`git pull`の違いが分かる
- [ ] `git rebase`の基本が分かる
- [ ] `merge`と`rebase`の違いが理解できている

---

## 📚 参考リンク

- [Pro Git Book（日本語版）](https://git-scm.com/book/ja/v2)
- [GitHub公式ドキュメント](https://docs.github.com/ja)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching（インタラクティブ学習）](https://learngitbranching.js.org/?locale=ja)

---

## 🆘 トラブルシューティング

### pushが拒否される場合
```bash
git pull origin main --rebase
git push origin main
```

### コンフリクトが怖い場合
```bash
# 作業を一時退避
git stash

# mainを更新
git pull origin main

# 作業を戻す
git stash pop
```

### 間違ってコミットした場合
```bash
# 直前のコミットを取り消し（変更は残る）
git reset --soft HEAD^

# コミットも変更も全て取り消し
git reset --hard HEAD^
```

---

## 📝 本日のまとめ

`git-summary.md`を作成し、以下の質問に答えてください：

1. Gitのどの機能が最も便利だと思いましたか？
2. コンフリクトを解決するときに困ったことは？
3. `merge`と`rebase`の違いを自分の言葉で説明してください
4. 明日から実際の開発で使いたいGitコマンドは？

---

## 🎉 完了後

すべてのチェックリストが完了したら：
1. すべての成果物をGitHubにpush
2. [Day 3](day-03.md)の準備をする
3. Git操作のチートシートを作成しておく

お疲れさまでした！
