# Day 1: Gitの基本操作とGitHubの準備

## 📅 実施日
- 予定: Week 1 - Day 1
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
Gitと GitHub CLI（`gh`）を使えるようにして、フォーク・クローン・Issue一括作成までの準備を完了する。
そのうえで、Gitの基本操作（clone, branch, commit, push, pull, fetch, rebase, merge）を習得し、GitHubでの開発フローを理解する

---

## 📋 午前の作業（9:00-13:00）

### 1. Gitのインストールと初期設定（9:00-9:30）

**手順:**
1. Gitのインストール
   - Windows: https://git-scm.com/download/win
     - インストール時の設定は、基本的にすべて「Next」のままでOKです
     - **Git Bash** も一緒にインストールされます（下の注意を参照）
   - Mac: `brew install git`
   - Linux: `sudo apt install git`

> 💻 **Windowsの方へ: コマンドは「Git Bash」で実行します**
> この研修のコマンド（`git`、`gh`、`./create-github-issues.sh` など）は、Windowsでは
> **Git Bash**（スタートメニューから「Git Bash」を検索して起動）で実行してください。
> PowerShellやコマンドプロンプトでは、Issue一括作成のスクリプト（bash用）が動きません。
> Macは「ターミナル」で実行します。

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

---

### 2. GitHubの準備（9:30-10:30）

> 📌 **このIssueが見えている方へ**
> 研修の開始時に、README の「始め方」の手順（フォーク → クローン → Issue一括作成）を済ませていれば、
> **この手順はすでに完了しています**。その場合は、各手順で「何をしたのか」を確認しながら、
> 動作確認のコマンド（`gh auth status`、`git remote -v`）だけ実行してください。

**手順:**

1. **GitHubアカウントの作成**
   - https://github.com/signup
   - ユーザー名、メールアドレス、パスワードを設定
   - 作成済みの場合はスキップ

2. **GitHub CLI（`gh`）のインストール**
   - `gh` は、ターミナルからGitHubを操作するツールです。この研修では、**40日分のIssueを一括作成**するために使います
   - Windows（Git Bashで）: https://cli.github.com/ からインストーラーをダウンロード、または `winget install --id GitHub.cli`
   - Mac: `brew install gh`
   - Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   - 動作確認（**インストール後はGit Bash／ターミナルを開き直す**）
     ```bash
     gh --version
     ```

3. **GitHubにログイン（`gh auth login`）**
   ```bash
   gh auth login
   ```
   - 質問には次のように答えます
     - `What account do you want to log into?` → **GitHub.com**
     - `What is your preferred protocol for Git operations?` → **HTTPS**
     - `Authenticate Git with your GitHub credentials?` → **Y**
     - `How would you like to authenticate GitHub CLI?` → **Login with a web browser**
   - 表示された**ワンタイムコード**をコピーし、ブラウザの画面に入力して許可する
   - ログイン状態の確認
     ```bash
     gh auth status
     # ✓ Logged in to github.com account ユーザー名 と表示されればOK
     ```

4. **研修用リポジトリのフォーク**
   - 研修用テンプレートリポジトリをブラウザで開き、右上の「**Fork**」をクリック
   - 自分のGitHubアカウントに、リポジトリのコピー（フォーク）が作られる
   - ⚠️ 以降の作業は、**フォーク元ではなく、自分のフォーク**で行います

5. **ローカルへのクローン**
   ```bash
   cd ~/workspace    # 作業用フォルダ（なければ mkdir ~/workspace）
   git clone https://github.com/<自分のユーザー名>/<リポジトリ名>.git
   cd <リポジトリ名>
   ```

6. **リポジトリの確認**
   ```bash
   git status
   git log
   git remote -v
   # origin が「自分のユーザー名」のURLになっていることを確認（フォーク元のURLではない）
   ```

7. **40日分のIssueを一括作成**（作成済みの場合は確認だけ）
   ```bash
   ./create-github-issues.sh --dry-run   # まず確認（宛先が自分のリポジトリか見る）
   ./create-github-issues.sh             # 実行。宛先が合っていれば y
   ```
   - ラベルとマイルストーンは自動で作られます
   - すでに作成済みのIssueは「スキップ」と表示されます（再実行しても重複しません）
   - 自分のリポジトリの「**Issues**」タブに、Day 1〜40 が並んでいることを確認する
   - 詳しくは [GitHubインポートガイド](../GITHUB_IMPORT_GUIDE.md)

**成果物:**
- GitHubアカウント
- スクリーンショット: `gh auth status` の実行結果
- クローンされたローカルリポジトリ（`git remote -v` の結果）
- スクリーンショット: 自分のリポジトリの Issues タブ（Day 1〜40）

---

### 3. Gitの基礎概念の学習（10:30-11:15）

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

2. `practice/git-concepts.md`ファイルを作成し、学んだことをまとめる

**成果物:**
- `practice/git-concepts.md`

---

---

### 4. 基本コマンドの練習（11:15-12:00）

> 📁 **練習用のファイルは、`practice/` フォルダにまとめて作ります。**
> 研修用の `README.md` などを書き換えてしまわないためです。

**手順:**
1. 練習用ファイルの作成
   ```bash
   mkdir -p practice
   echo "Hello Git" > practice/practice.txt
   ```

2. `git status`で状態確認
   ```bash
   git status
   # Untracked filesとして表示される
   ```

3. `git add`でステージングエリアに追加
   ```bash
   git add practice/practice.txt
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

### 5. ブランチ操作の練習（13:00-14:30）

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
   echo "# 自己紹介" > practice/profile.md
   
   # コミット
   git add practice/profile.md
   git commit -m "feat: 自己紹介ファイルを追加"
   ```

**演習:**
- 3つ以上のブランチを作成
- 各ブランチで異なるファイルを編集

**成果物:**
- 複数のブランチ
- 各ブランチでのコミット

---

### 6. merge操作の練習（14:30-15:30）

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
   # mainブランチで practice/conflict.md を作成
   echo "Main branch" > practice/conflict.md
   git add practice/conflict.md
   git commit -m "docs: conflict.md作成(main)"
   
   # feature/readmeブランチに移動
   git switch feature/readme
   
   # 同じファイル名で、違う内容を作成
   echo "Feature branch" > practice/conflict.md
   git add practice/conflict.md
   git commit -m "docs: conflict.md作成(feature)"
   
   # mainにマージしてコンフリクト発生
   git switch main
   git merge feature/readme
   # CONFLICT (add/add): Merge conflict in practice/conflict.md
   
   # コンフリクトを解決
   # エディタで practice/conflict.md を開き、<<<<<<< ======= >>>>>>> の行を削除して、残したい内容にする
   git add practice/conflict.md
   git commit -m "merge: feature/readmeをマージ"
   ```

**成果物:**
- マージ済みのブランチ
- コンフリクト解決の経験

---

### 7. push/pull/fetch操作の練習（15:30-16:30）

**手順:**
1. リモートへのpush
   ```bash
   git push origin main
   ```

2. 新しいブランチをリモートにpush
   ```bash
   git switch -c feature/test
   echo "test" > practice/test.txt
   git add practice/test.txt
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

### 8. rebase操作の練習（16:30-17:00）

**手順:**
1. 新しいブランチを作成
   ```bash
   git switch -c feature/rebase-test
   echo "Rebase test" > practice/rebase.txt
   git add practice/rebase.txt
   git commit -m "feat: rebaseテスト"
   ```

2. mainブランチで新しいコミット
   ```bash
   git switch main
   echo "Main update" > practice/main-update.txt
   git add practice/main-update.txt
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
- `practice/merge-vs-rebase.md`（違いをまとめたドキュメント）

---

## ✅ チェックリスト

完了したらチェックを入れてください：

- [✅] Gitがインストールされ、初期設定（名前・メール）が完了している
- [✅] （Windowsの方）Git Bashでコマンドを実行できる
- [✅] GitHubアカウントが作成されている
- [✅] GitHub CLI（`gh`）がインストールされ、`gh auth status` でログイン済みと表示される
- [✅] 研修用リポジトリを**自分のアカウントにフォーク**した
- [✅] フォークをクローンし、`git remote -v` の `origin` が自分のリポジトリになっている
- [✅] 自分のリポジトリの Issues タブに Day 1〜40 のIssueが作成されている
- [✅] `git status`, `git add`, `git commit`が使える
- [✅] ブランチの作成・切り替えができる
- [✅] `git merge`でブランチを統合できる
- [✅] コンフリクトを解決できる
- [✅] `git push`でリモートに送信できる
- [✅] `git pull`でリモートから取得できる
- [✅] `git fetch`と`git pull`の違いが分かる
- [✅] `git rebase`の基本が分かる
- [✅] `merge`と`rebase`の違いが理解できている

---

## 📚 参考リンク

- [Pro Git Book（日本語版）](https://git-scm.com/book/ja/v2)
- [GitHub公式ドキュメント](https://docs.github.com/ja)
- [GitHub CLI マニュアル](https://cli.github.com/manual/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching（インタラクティブ学習）](https://learngitbranching.js.org/?locale=ja)

---

## 🆘 トラブルシューティング

### `gh: command not found`（`gh` が見つからない）
**原因:** インストール直後で、ターミナルが `gh` を認識していない

**解決策:**
1. Git Bash（またはターミナル）を**いったん閉じて開き直す**
2. それでも直らない場合は、PCを再起動する
3. Windowsでは、インストーラー（https://cli.github.com/）で入れ直す

### `gh auth login` でブラウザの認証が進まない
**原因:** 社内ネットワークの制限、またはブラウザの設定の問題

**解決策:**
1. 表示されたワンタイムコードを、正しいアカウントでログインしたブラウザに入力しているか確認
2. ブラウザが自動で開かない場合は、画面に表示されたURLを手でブラウザに貼る
3. 解決しない場合は、ネットワークの制限の可能性があるため、Teamsで質問する

### Windowsで `./create-github-issues.sh` が動かない（`command not found` や `\r` というエラー）
**原因:** Git Bash以外（PowerShell、コマンドプロンプト）で実行している、または改行コードの問題

**解決策:**
1. **Git Bash** で実行しているか確認する
2. `bad interpreter` や `$'\r': command not found` と出る場合は、改行コードが原因です。次を実行してから、もう一度クローンし直す
   ```bash
   git config --global core.autocrlf input
   ```

### `git push` でユーザー名・パスワードを聞かれる／拒否される
**原因:** GitHubへの認証が済んでいない

**解決策:**
1. `gh auth status` でログイン済みか確認する
2. `gh auth setup-git` を実行して、`git` に認証情報を連携する
3. パスワードにはGitHubのログインパスワードではなく、`gh auth login` で認証済みの状態を使う

### Issueが40件作られていない／別のリポジトリに作られた
**原因:** スクリプトを実行した場所が違う（フォーク元をクローンしている、など）

**解決策:**
1. `git remote -v` で、`origin` が**自分のフォーク**になっているか確認する
2. 別のリポジトリに作ってしまった場合は、そのIssueをGitHub上で削除（Close/Delete）してから、正しい場所で再実行する

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

## 📝 本日のまとめ

`practice/git-summary.md`を作成し、以下の質問に答えてください：

1. Gitのどの機能が最も便利だと思いましたか？
2. コンフリクトを解決するときに困ったことは？
3. `merge`と`rebase`の違いを自分の言葉で説明してください
4. 明日から実際の開発で使いたいGitコマンドは？

---

## 🎉 完了後

すべてのチェックリストが完了したら：
1. すべての成果物をGitHubにpush
2. [Day 2](day-02.md)の準備をする（明日は、JDK・IntelliJ IDEA・MySQLなどの開発環境をセットアップします）
3. Git操作のチートシートを作成しておく

お疲れさまでした！
