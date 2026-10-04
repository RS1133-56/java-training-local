# Day 30: レスポンシブデザイン対応

## 📅 実施日
- 予定: Week 6 - Day 30
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
メディアクエリを使ってモバイル、タブレット、PCに対応したレスポンシブデザインを実装する

---

## 📋 午前の作業（9:00-13:00）

### 1. レスポンシブデザインの基礎（9:00-9:30）

**ブレークポイント設計:**

| デバイス | 幅 | 対応 |
|---------|-----|------|
| スマートフォン | 〜767px | モバイルファースト |
| タブレット | 768px〜1023px | 2カラム |
| PC | 1024px〜 | フルレイアウト |

**モバイルファースト設計:**
```css
/* デフォルト: モバイル向け */
.container {
    padding: 16px;
}

/* タブレット以上 */
@media (min-width: 768px) {
    .container {
        padding: 24px;
    }
}

/* PC以上 */
@media (min-width: 1024px) {
    .container {
        padding: 32px;
    }
}
```

---

### 2. レスポンシブ用CSS作成（9:30-12:00）

`src/main/resources/static/css/responsive.css`:

```css
/* ===================================
   レスポンシブデザイン
   =================================== */

/* ブレークポイント定義 */
:root {
    --bp-mobile: 0px;
    --bp-tablet: 768px;
    --bp-desktop: 1024px;
    --bp-wide: 1280px;
}

/* ===================================
   基本レイアウト
   =================================== */

/* モバイル（デフォルト） */
.container {
    max-width: 100%;
    padding: 0 var(--space-md);
}

/* タブレット */
@media (min-width: 768px) {
    .container {
        padding: 0 var(--space-lg);
    }
}

/* PC */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
}

/* ===================================
   グリッドシステム
   =================================== */

/* モバイル: 1カラム */
.grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-md);
}

/* タブレット: 2カラム */
@media (min-width: 768px) {
    .grid-2,
    .grid-3,
    .grid-4 {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* PC: 指定カラム数 */
@media (min-width: 1024px) {
    .grid-2 {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .grid-3 {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .grid-4 {
        grid-template-columns: repeat(4, 1fr);
    }
}

/* ===================================
   都道府県グリッド
   =================================== */

/* モバイル: 2カラム */
.prefecture-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-sm);
}

/* タブレット: 3カラム */
@media (min-width: 768px) {
    .prefecture-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-md);
    }
}

/* PC: 5カラム */
@media (min-width: 1024px) {
    .prefecture-grid {
        grid-template-columns: repeat(5, 1fr);
    }
}

/* ===================================
   天気予報グリッド
   =================================== */

/* モバイル: 2カラム */
.forecast-container {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-sm);
}

/* タブレット: 4カラム */
@media (min-width: 768px) {
    .forecast-container {
        grid-template-columns: repeat(4, 1fr);
        gap: var(--space-md);
    }
}

/* PC: 7カラム */
@media (min-width: 1024px) {
    .forecast-container {
        grid-template-columns: repeat(7, 1fr);
    }
}

/* ===================================
   現在の天気カード
   =================================== */

/* モバイル: 縦並び */
.current-weather-card {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
}

.weather-icon {
    grid-row: 1;
    grid-column: 1;
}

.weather-main {
    grid-row: 2;
    grid-column: 1;
}

.weather-details {
    grid-row: 3;
    grid-column: 1;
    grid-template-columns: repeat(2, 1fr);
}

/* タブレット以上: 横並び */
@media (min-width: 768px) {
    .current-weather-card {
        grid-template-columns: auto 1fr;
        grid-template-rows: auto auto;
    }
    
    .weather-icon {
        grid-row: 1 / 3;
        grid-column: 1;
    }
    
    .weather-main {
        grid-row: 1;
        grid-column: 2;
    }
    
    .weather-details {
        grid-row: 2;
        grid-column: 1 / 3;
        grid-template-columns: repeat(3, 1fr);
    }
}

/* PC: 3カラム詳細 */
@media (min-width: 1024px) {
    .weather-details {
        grid-template-columns: repeat(6, 1fr);
    }
}

/* ===================================
   ナビゲーション
   =================================== */

/* モバイル: ハンバーガーメニュー */
.navbar .container {
    flex-direction: column;
    align-items: flex-start;
}

.nav-menu {
    flex-direction: column;
    width: 100%;
    gap: var(--space-sm);
}

/* タブレット以上: 横並び */
@media (min-width: 768px) {
    .navbar .container {
        flex-direction: row;
        align-items: center;
    }
    
    .nav-menu {
        flex-direction: row;
        width: auto;
        gap: var(--space-lg);
    }
}

/* ===================================
   検索・フィルタセクション
   =================================== */

/* モバイル: 縦並び */
.search-filter-section {
    flex-direction: column;
    gap: var(--space-md);
}

.search-box {
    width: 100%;
}

/* タブレット以上: 横並び */
@media (min-width: 768px) {
    .search-filter-section {
        flex-direction: row;
        align-items: center;
    }
    
    .search-box {
        flex: 1;
        min-width: 250px;
    }
}

/* ===================================
   フォント調整
   =================================== */

/* モバイル: 小さめ */
.page-header h1 {
    font-size: var(--font-xxl);
}

.prefecture-title {
    font-size: var(--font-xl);
}

.temperature {
    font-size: 48px;
}

/* タブレット */
@media (min-width: 768px) {
    .page-header h1 {
        font-size: var(--font-xxxl);
    }
    
    .prefecture-title {
        font-size: var(--font-xxl);
    }
    
    .temperature {
        font-size: 56px;
    }
}

/* PC */
@media (min-width: 1024px) {
    .temperature {
        font-size: 64px;
    }
}

/* ===================================
   スペーシング調整
   =================================== */

/* モバイル */
.page-header {
    padding: var(--space-lg);
}

.section-title {
    font-size: var(--font-lg);
}

/* タブレット */
@media (min-width: 768px) {
    .page-header {
        padding: var(--space-xl);
    }
    
    .section-title {
        font-size: var(--font-xl);
    }
}

/* PC */
@media (min-width: 1024px) {
    .page-header {
        padding: var(--space-xxl) var(--space-xl);
    }
    
    .section-title {
        font-size: var(--font-xxl);
    }
}

/* ===================================
   ボタン
   =================================== */

/* モバイル: フル幅 */
.action-buttons {
    flex-direction: column;
    gap: var(--space-md);
}

.btn {
    width: 100%;
}

/* タブレット以上: 横並び */
@media (min-width: 768px) {
    .action-buttons {
        flex-direction: row;
        justify-content: center;
    }
    
    .btn {
        width: auto;
    }
}

/* ===================================
   表示/非表示ユーティリティ
   =================================== */

/* モバイルのみ表示 */
.show-mobile {
    display: block;
}

.show-tablet,
.show-desktop {
    display: none;
}

/* タブレット以上 */
@media (min-width: 768px) {
    .show-mobile {
        display: none;
    }
    
    .show-tablet {
        display: block;
    }
}

/* PC以上 */
@media (min-width: 1024px) {
    .show-tablet {
        display: none;
    }
    
    .show-desktop {
        display: block;
    }
}

/* ===================================
   画像
   =================================== */

img {
    max-width: 100%;
    height: auto;
}

/* ===================================
   テーブル（レスポンシブ）
   =================================== */

/* モバイル: スクロール */
.table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

table {
    min-width: 100%;
}

/* PC: 通常表示 */
@media (min-width: 1024px) {
    .table-responsive {
        overflow-x: visible;
    }
}

/* ===================================
   プリントスタイル
   =================================== */

@media print {
    .navbar,
    .footer,
    .action-buttons {
        display: none;
    }
    
    .container {
        max-width: 100%;
        padding: 0;
    }
    
    .page-header {
        background: white;
        color: black;
    }
}
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. viewportメタタグの確認（13:00-13:30）

`fragments/header.html`を更新：

```html
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title th:text="${title}">天気予報アプリ</title>
    
    <!-- CSS読み込み -->
    <link rel="stylesheet" th:href="@{/css/variables.css}">
    <link rel="stylesheet" th:href="@{/css/base.css}">
    <link rel="stylesheet" th:href="@{/css/components.css}">
    <link rel="stylesheet" th:href="@{/css/pages.css}">
    <link rel="stylesheet" th:href="@{/css/responsive.css}">
</head>
```

---

### 4. タッチ最適化（13:30-15:00）

`src/main/resources/static/css/touch.css`:

```css
/* タッチデバイス最適化 */

/* タップ可能な要素のサイズ */
@media (pointer: coarse) {
    /* ボタン */
    .btn {
        min-height: 44px;
        min-width: 44px;
        padding: var(--space-md) var(--space-lg);
    }
    
    /* リンク */
    a {
        min-height: 44px;
        display: inline-flex;
        align-items: center;
    }
    
    /* フォーム要素 */
    .form-control {
        min-height: 44px;
        font-size: 16px; /* iOS拡大防止 */
    }
    
    select {
        min-height: 44px;
        font-size: 16px;
    }
}

/* ホバー無効化（タッチデバイス） */
@media (hover: none) {
    .card:hover,
    .prefecture-card:hover,
    .forecast-card:hover {
        transform: none;
    }
}

/* スクロールスナップ */
@media (max-width: 767px) {
    .forecast-container {
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
    }
    
    .forecast-card {
        scroll-snap-align: start;
    }
}
```

---

### 5. レスポンシブテスト（15:00-17:00）

**テストページ作成:** `src/main/resources/templates/practice/responsive-test.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('レスポンシブテスト')}"></head>
<body>
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <div class="container">
        <h1>レスポンシブテスト</h1>
        
        <!-- ブレークポイント表示 -->
        <div class="mb-lg">
            <div class="alert alert-info show-mobile">
                📱 モバイル表示（〜767px）
            </div>
            <div class="alert alert-info show-tablet">
                📱 タブレット表示（768px〜1023px）
            </div>
            <div class="alert alert-info show-desktop">
                🖥️ デスクトップ表示（1024px〜）
            </div>
        </div>
        
        <!-- グリッドテスト -->
        <section class="mb-xl">
            <h2>グリッドテスト</h2>
            <div class="grid grid-4">
                <div class="card"><div class="card-body">1</div></div>
                <div class="card"><div class="card-body">2</div></div>
                <div class="card"><div class="card-body">3</div></div>
                <div class="card"><div class="card-body">4</div></div>
            </div>
        </section>
        
        <!-- ボタンテスト -->
        <section class="mb-xl">
            <h2>ボタンテスト</h2>
            <div class="action-buttons">
                <button class="btn btn-primary">Primary</button>
                <button class="btn btn-secondary">Secondary</button>
                <button class="btn btn-success">Success</button>
            </div>
        </section>
    </div>
    
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <!-- デバッグ用：画面サイズ表示 -->
    <script>
        function showScreenSize() {
            const width = window.innerWidth;
            let device = 'モバイル';
            
            if (width >= 1024) device = 'デスクトップ';
            else if (width >= 768) device = 'タブレット';
            
            console.log(`画面幅: ${width}px (${device})`);
        }
        
        window.addEventListener('resize', showScreenSize);
        showScreenSize();
    </script>
</body>
</html>
```

**テストチェックリスト:** `responsive-test-checklist.md`

```markdown
# レスポンシブデザインテストチェックリスト

## モバイル（〜767px）

- [ ] トップページが2カラムで表示
- [ ] ナビゲーションが縦並び
- [ ] 検索とフィルタが縦並び
- [ ] 天気予報が2カラム
- [ ] ボタンが全幅表示
- [ ] タップサイズが44px以上

## タブレット（768px〜1023px）

- [ ] トップページが3カラムで表示
- [ ] ナビゲーションが横並び
- [ ] 検索とフィルタが横並び
- [ ] 天気予報が4カラム
- [ ] ボタンが適切なサイズ

## デスクトップ（1024px〜）

- [ ] トップページが5カラムで表示
- [ ] レイアウトが最大1200pxでセンタリング
- [ ] 天気予報が7カラム
- [ ] すべてのコンテンツが見やすい

## ブラウザテスト

- [ ] Chrome（モバイル・デスクトップ）
- [ ] Safari（iOS）
- [ ] Firefox
- [ ] Edge

## 実機テスト

- [ ] iPhone
- [ ] Android
- [ ] iPad
```

---

## ✅ チェックリスト

- [ ] レスポンシブCSSを作成した
- [ ] メディアクエリを設定した
- [ ] タッチ最適化を実装した
- [ ] viewportメタタグを設定した
- [ ] モバイル、タブレット、PCで確認した
- [ ] テストページを作成した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): レスポンシブデザイン対応"
git push origin main
```

---

## 📚 参考リンク

### レスポンシブデザイン
- [レスポンシブデザイン基礎（日本語）](https://developer.mozilla.org/ja/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [メディアクエリ（日本語）](https://developer.mozilla.org/ja/docs/Web/CSS/Media_Queries/Using_media_queries)

### モバイルファースト
- [モバイルファースト設計（日本語）](https://qiita.com/mrd-takahashi/items/b82a5c452fa5e41e33f4)

---

## 📝 本日のまとめ

1. **実装した機能:**
   - レスポンシブデザイン
   - メディアクエリ
   - タッチ最適化

2. **学んだこと:**
   - モバイルファースト設計
   - ブレークポイント設計
   - タッチデバイス対応

3. **明日への引き継ぎ:**
   - Day 31以降で機能追加

---

## 🎉 完了後

次は [Day 31](day-31.md) へ

お疲れさまでした！
