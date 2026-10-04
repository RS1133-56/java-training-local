# Day 29: CSS基礎とスタイリング

## 📅 実施日
- 予定: Week 6 - Day 29
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
CSSファイルを分離し、デザインシステムを構築してアプリ全体のスタイリングを統一する

---

## 📋 午前の作業（9:00-13:00）

### 1. CSSアーキテクチャの設計（9:00-9:30）

**CSS構成:**

```
static/
  └── css/
      ├── base.css           # リセット・基本設定
      ├── variables.css      # CSS変数（カラー・サイズ）
      ├── components.css     # 再利用可能なコンポーネント
      └── pages.css          # ページ固有のスタイル
```

**設計方針:**
- CSS変数でカラーパレット・サイズを統一
- BEM命名規則を採用
- モバイルファースト設計

---

### 2. CSS変数とベーススタイル作成（9:30-12:00）

**CSS変数定義:** `src/main/resources/static/css/variables.css`

```css
:root {
    /* カラーパレット */
    --primary-color: #3498db;
    --primary-dark: #2980b9;
    --primary-light: #5dade2;
    
    --secondary-color: #2ecc71;
    --secondary-dark: #27ae60;
    --secondary-light: #58d68d;
    
    --accent-color: #e74c3c;
    --accent-dark: #c0392b;
    --accent-light: #ec7063;
    
    --warning-color: #f39c12;
    --info-color: #3498db;
    --success-color: #2ecc71;
    --error-color: #e74c3c;
    
    /* グレースケール */
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --text-light: #95a5a6;
    
    --bg-primary: #ffffff;
    --bg-secondary: #ecf0f1;
    --bg-tertiary: #f8f9fa;
    
    --border-color: #e1e8ed;
    --border-dark: #bdc3c7;
    
    /* グラデーション */
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-success: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
    --gradient-warning: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    
    /* スペーシング */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-xxl: 48px;
    
    /* フォントサイズ */
    --font-xs: 12px;
    --font-sm: 14px;
    --font-base: 16px;
    --font-lg: 18px;
    --font-xl: 24px;
    --font-xxl: 32px;
    --font-xxxl: 48px;
    
    /* フォントウェイト */
    --font-normal: 400;
    --font-medium: 500;
    --font-bold: 700;
    
    /* ボーダー半径 */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-full: 9999px;
    
    /* シャドウ */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 5px 15px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
    --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.2);
    
    /* トランジション */
    --transition-fast: 0.15s ease-in-out;
    --transition-base: 0.3s ease-in-out;
    --transition-slow: 0.5s ease-in-out;
    
    /* Z-index */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-tooltip: 1060;
}
```

**ベーススタイル:** `src/main/resources/static/css/base.css`

```css
/* リセット */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ベーススタイル */
html {
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                 "Helvetica Neue", Arial, "Noto Sans", sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--bg-secondary);
}

/* コンテナ */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

.container-fluid {
    width: 100%;
    padding: 0 var(--space-lg);
}

/* タイポグラフィ */
h1, h2, h3, h4, h5, h6 {
    font-weight: var(--font-bold);
    line-height: 1.2;
    margin-bottom: var(--space-md);
}

h1 { font-size: var(--font-xxxl); }
h2 { font-size: var(--font-xxl); }
h3 { font-size: var(--font-xl); }
h4 { font-size: var(--font-lg); }
h5 { font-size: var(--font-base); }
h6 { font-size: var(--font-sm); }

p {
    margin-bottom: var(--space-md);
}

a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color var(--transition-base);
}

a:hover {
    color: var(--primary-dark);
}

/* リスト */
ul, ol {
    margin-bottom: var(--space-md);
    padding-left: var(--space-xl);
}

/* 画像 */
img {
    max-width: 100%;
    height: auto;
    display: block;
}
```

**コンポーネント:** `src/main/resources/static/css/components.css`

```css
/* ボタン */
.btn {
    display: inline-block;
    padding: var(--space-sm) var(--space-lg);
    font-size: var(--font-base);
    font-weight: var(--font-medium);
    text-align: center;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-base);
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn-secondary {
    background-color: var(--text-secondary);
    color: white;
}

.btn-secondary:hover {
    background-color: var(--text-primary);
}

.btn-success {
    background-color: var(--success-color);
    color: white;
}

.btn-warning {
    background-color: var(--warning-color);
    color: white;
}

.btn-error {
    background-color: var(--error-color);
    color: white;
}

.btn-lg {
    padding: var(--space-md) var(--space-xl);
    font-size: var(--font-lg);
}

.btn-sm {
    padding: var(--space-xs) var(--space-md);
    font-size: var(--font-sm);
}

/* カード */
.card {
    background-color: var(--bg-primary);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: all var(--transition-base);
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-4px);
}

.card-header {
    padding: var(--space-lg);
    background-color: var(--bg-tertiary);
    border-bottom: 1px solid var(--border-color);
}

.card-body {
    padding: var(--space-lg);
}

.card-footer {
    padding: var(--space-lg);
    background-color: var(--bg-tertiary);
    border-top: 1px solid var(--border-color);
}

/* バッジ */
.badge {
    display: inline-block;
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--font-xs);
    font-weight: var(--font-bold);
    border-radius: var(--radius-full);
    text-transform: uppercase;
}

.badge-primary {
    background-color: var(--primary-color);
    color: white;
}

.badge-success {
    background-color: var(--success-color);
    color: white;
}

.badge-warning {
    background-color: var(--warning-color);
    color: white;
}

.badge-error {
    background-color: var(--error-color);
    color: white;
}

/* アラート */
.alert {
    padding: var(--space-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
}

.alert-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* フォーム */
.form-group {
    margin-bottom: var(--space-lg);
}

.form-label {
    display: block;
    margin-bottom: var(--space-sm);
    font-weight: var(--font-medium);
    color: var(--text-primary);
}

.form-control {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    font-size: var(--font-base);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-md);
    transition: border-color var(--transition-base);
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-control:disabled {
    background-color: var(--bg-secondary);
    cursor: not-allowed;
}

/* グリッド */
.grid {
    display: grid;
    gap: var(--space-lg);
}

.grid-2 {
    grid-template-columns: repeat(2, 1fr);
}

.grid-3 {
    grid-template-columns: repeat(3, 1fr);
}

.grid-4 {
    grid-template-columns: repeat(4, 1fr);
}

/* ユーティリティ */
.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.text-primary {
    color: var(--primary-color);
}

.text-secondary {
    color: var(--text-secondary);
}

.mt-xs { margin-top: var(--space-xs); }
.mt-sm { margin-top: var(--space-sm); }
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
.mt-xl { margin-top: var(--space-xl); }

.mb-xs { margin-bottom: var(--space-xs); }
.mb-sm { margin-bottom: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.mb-lg { margin-bottom: var(--space-lg); }
.mb-xl { margin-bottom: var(--space-xl); }

.p-xs { padding: var(--space-xs); }
.p-sm { padding: var(--space-sm); }
.p-md { padding: var(--space-md); }
.p-lg { padding: var(--space-lg); }
.p-xl { padding: var(--space-xl); }
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. ページ固有のスタイル（13:00-15:00）

`src/main/resources/static/css/pages.css`:

```css
/* トップページ */
.page-header {
    background: var(--gradient-primary);
    color: white;
    padding: var(--space-xxl) var(--space-lg);
    border-radius: var(--radius-xl);
    margin-bottom: var(--space-xl);
    text-align: center;
}

.prefecture-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: var(--space-md);
}

.prefecture-card {
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-lg);
    transition: all var(--transition-base);
}

.prefecture-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-color);
}

/* 天気詳細ページ */
.weather-header {
    background: var(--gradient-primary);
    color: white;
    padding: var(--space-xl);
    border-radius: var(--radius-xl);
    margin-bottom: var(--space-xl);
}

.current-weather-card {
    background: var(--bg-primary);
    border-radius: var(--radius-xl);
    padding: var(--space-xl);
    box-shadow: var(--shadow-md);
    margin-bottom: var(--space-xl);
}

.forecast-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: var(--space-md);
}

.forecast-card {
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
    transition: all var(--transition-base);
}

.forecast-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-md);
    border-color: var(--primary-color);
}

.forecast-card.today {
    background: var(--gradient-primary);
    color: white;
    border-color: transparent;
}
```

---

### 4. HTMLへのCSS適用（15:00-16:30）

**header.html更新:**

```html
<head th:fragment="head(title)">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title th:text="${title}">天気予報アプリ</title>
    
    <!-- CSS読み込み -->
    <link rel="stylesheet" th:href="@{/css/variables.css}">
    <link rel="stylesheet" th:href="@{/css/base.css}">
    <link rel="stylesheet" th:href="@{/css/components.css}">
    <link rel="stylesheet" th:href="@{/css/pages.css}">
</head>
```

---

### 5. スタイルガイド作成（16:30-17:00）

`src/main/resources/templates/practice/style-guide.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('スタイルガイド')}"></head>
<body>
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <div class="container">
        <h1>スタイルガイド</h1>
        
        <!-- カラーパレット -->
        <section class="mb-xl">
            <h2>カラーパレット</h2>
            <div class="grid grid-4">
                <div class="card">
                    <div class="card-body" style="background: var(--primary-color); color: white;">
                        Primary
                    </div>
                </div>
                <div class="card">
                    <div class="card-body" style="background: var(--secondary-color); color: white;">
                        Secondary
                    </div>
                </div>
                <div class="card">
                    <div class="card-body" style="background: var(--accent-color); color: white;">
                        Accent
                    </div>
                </div>
                <div class="card">
                    <div class="card-body" style="background: var(--warning-color); color: white;">
                        Warning
                    </div>
                </div>
            </div>
        </section>
        
        <!-- ボタン -->
        <section class="mb-xl">
            <h2>ボタン</h2>
            <button class="btn btn-primary">Primary</button>
            <button class="btn btn-secondary">Secondary</button>
            <button class="btn btn-success">Success</button>
            <button class="btn btn-warning">Warning</button>
            <button class="btn btn-error">Error</button>
        </section>
        
        <!-- カード -->
        <section class="mb-xl">
            <h2>カード</h2>
            <div class="grid grid-3">
                <div class="card">
                    <div class="card-header">
                        <h3>カードタイトル</h3>
                    </div>
                    <div class="card-body">
                        <p>カードの本文です。</p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-primary">詳細</button>
                    </div>
                </div>
            </div>
        </section>
    </div>
    
    <div th:replace="~{fragments/footer :: footer}"></div>
</body>
</html>
```

---

## ✅ チェックリスト

- [ ] CSS変数を定義した
- [ ] ベーススタイルを作成した
- [ ] コンポーネントスタイルを作成した
- [ ] ページ固有スタイルを作成した
- [ ] HTMLにCSSを適用した
- [ ] スタイルガイドを作成した
- [ ] ブラウザで確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): CSSアーキテクチャとデザインシステム構築"
git push origin main
```

---

## 📚 参考リンク

### CSS設計
- [CSS設計ガイド（日本語）](https://qiita.com/manabuyasuda/items/dbb76ed36970bec95470)
- [BEM命名規則（日本語）](https://qiita.com/Takuan_Oishii/items/0f0d2c5dc33a9b2d9e7b)

### CSS変数
- [CSS Custom Properties（日本語）](https://developer.mozilla.org/ja/docs/Web/CSS/Using_CSS_custom_properties)

---

## 📝 本日のまとめ

1. **実装した機能:**
   - CSSアーキテクチャ構築
   - デザインシステム
   - 再利用可能コンポーネント

2. **学んだこと:**
   - CSS変数の活用
   - BEM命名規則
   - コンポーネント設計

3. **明日への引き継ぎ:**
   - Day 30でレスポンシブデザイン対応

---

## 🎉 完了後

次は [Day 30](day-30.md) へ

お疲れさまでした！
