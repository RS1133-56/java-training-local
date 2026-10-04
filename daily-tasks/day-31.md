# Day 31: ローディング機能実装

## 📅 実施日
- 予定: Week 7 - Day 31
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
APIデータ取得中のローディング表示を実装し、ユーザー体験を向上させる

---

## 📋 午前の作業（9:00-13:00）

### 1. ローディングUIの設計（9:00-9:30）

**ローディング表示が必要な場面:**
1. トップページ読み込み時
2. 天気詳細ページ読み込み時
3. 地域フィルタ変更時
4. リロード時

**ローディングパターン:**

| パターン | 用途 | 実装方法 |
|---------|------|---------|
| スピナー | データ取得中 | CSS Animation |
| スケルトン | 初期表示 | Placeholder |
| プログレスバー | 段階的処理 | JavaScript |
| オーバーレイ | 画面全体 | Fixed Position |

---

### 2. CSSスピナー実装（9:30-11:00）

`src/main/resources/static/css/loading.css`:

```css
/* ===================================
   ローディングコンポーネント
   =================================== */

/* オーバーレイ */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: var(--z-modal);
    opacity: 0;
    visibility: hidden;
    transition: opacity var(--transition-base), 
                visibility var(--transition-base);
}

.loading-overlay.show {
    opacity: 1;
    visibility: visible;
}

/* スピナーコンテナ */
.spinner-container {
    text-align: center;
}

/* スピナー - 基本 */
.spinner {
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto var(--space-md);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* スピナー - カラフル */
.spinner-colorful {
    width: 60px;
    height: 60px;
    border: 4px solid transparent;
    border-top-color: #3498db;
    border-right-color: #e74c3c;
    border-bottom-color: #2ecc71;
    border-left-color: #f39c12;
    border-radius: 50%;
    animation: spin 1.2s linear infinite;
    margin: 0 auto var(--space-md);
}

/* スピナー - パルス */
.spinner-pulse {
    width: 60px;
    height: 60px;
    background: white;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    margin: 0 auto var(--space-md);
}

@keyframes pulse {
    0%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
}

/* スピナー - ドット */
.spinner-dots {
    display: flex;
    gap: var(--space-sm);
    justify-content: center;
    margin: 0 auto var(--space-md);
}

.spinner-dots .dot {
    width: 12px;
    height: 12px;
    background: white;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
}

.spinner-dots .dot:nth-child(1) {
    animation-delay: -0.32s;
}

.spinner-dots .dot:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes bounce {
    0%, 80%, 100% {
        transform: scale(0);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

/* ローディングテキスト */
.loading-text {
    color: white;
    font-size: var(--font-lg);
    font-weight: var(--font-medium);
    margin-top: var(--space-md);
}

/* インラインローディング */
.loading-inline {
    display: inline-flex;
    align-items: center;
    gap: var(--space-sm);
}

.loading-inline .spinner {
    width: 20px;
    height: 20px;
    border-width: 2px;
    margin: 0;
}

/* スケルトンスクリーン */
.skeleton {
    background: linear-gradient(
        90deg,
        #f0f0f0 0%,
        #e0e0e0 50%,
        #f0f0f0 100%
    );
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s ease-in-out infinite;
    border-radius: var(--radius-md);
}

@keyframes skeleton-loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

/* スケルトン - カード */
.skeleton-card {
    padding: var(--space-lg);
    background: white;
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-md);
}

.skeleton-title {
    height: 24px;
    width: 60%;
    margin-bottom: var(--space-md);
}

.skeleton-text {
    height: 16px;
    width: 100%;
    margin-bottom: var(--space-sm);
}

.skeleton-text:last-child {
    width: 80%;
}

/* プログレスバー */
.progress-bar {
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin-top: var(--space-md);
}

.progress-bar-fill {
    height: 100%;
    background: white;
    border-radius: var(--radius-full);
    transition: width var(--transition-slow);
}

/* インデタミネート（不定） */
.progress-bar-indeterminate {
    position: relative;
    overflow: hidden;
}

.progress-bar-indeterminate::after {
    content: '';
    position: absolute;
    top: 0;
    left: -50%;
    width: 50%;
    height: 100%;
    background: white;
    animation: progress-indeterminate 1.5s linear infinite;
}

@keyframes progress-indeterminate {
    0% {
        left: -50%;
    }
    100% {
        left: 100%;
    }
}

/* ボタンローディング */
.btn-loading {
    position: relative;
    color: transparent;
    pointer-events: none;
}

.btn-loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

/* ミニスピナー */
.spinner-sm {
    width: 24px;
    height: 24px;
    border-width: 2px;
}

.spinner-xs {
    width: 16px;
    height: 16px;
    border-width: 2px;
}
```

---

### 3. JavaScript実装（11:00-12:00）

`src/main/resources/static/js/loading.js`:

```javascript
/**
 * ローディング管理クラス
 */
class LoadingManager {
    constructor() {
        this.overlay = null;
        this.init();
    }
    
    /**
     * 初期化
     */
    init() {
        // オーバーレイ作成
        this.overlay = document.createElement('div');
        this.overlay.className = 'loading-overlay';
        this.overlay.id = 'loadingOverlay';
        
        // スピナーとテキスト
        this.overlay.innerHTML = `
            <div class="spinner-container">
                <div class="spinner"></div>
                <div class="loading-text">読み込み中...</div>
                <div class="progress-bar progress-bar-indeterminate">
                    <div class="progress-bar-fill"></div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.overlay);
    }
    
    /**
     * ローディング表示
     * @param {string} message - 表示メッセージ
     */
    show(message = '読み込み中...') {
        const textEl = this.overlay.querySelector('.loading-text');
        if (textEl) {
            textEl.textContent = message;
        }
        
        // 少し遅延して表示（すぐ終わる処理で点滅させない）
        setTimeout(() => {
            this.overlay.classList.add('show');
        }, 100);
    }
    
    /**
     * ローディング非表示
     */
    hide() {
        this.overlay.classList.remove('show');
    }
    
    /**
     * メッセージ更新
     * @param {string} message - 新しいメッセージ
     */
    updateMessage(message) {
        const textEl = this.overlay.querySelector('.loading-text');
        if (textEl) {
            textEl.textContent = message;
        }
    }
}

// グローバルインスタンス
const loading = new LoadingManager();

/**
 * ページ読み込み時のローディング
 */
document.addEventListener('DOMContentLoaded', function() {
    
    // すべてのリンクにローディング追加
    const weatherLinks = document.querySelectorAll('a[href^="/weather/"]');
    weatherLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            loading.show('天気情報を取得中...');
        });
    });
    
    // フォーム送信時
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            loading.show('処理中...');
        });
    });
    
    // 地域フィルタ変更時
    const regionSelect = document.getElementById('regionSelect');
    if (regionSelect) {
        regionSelect.addEventListener('change', function() {
            loading.show('地域情報を読み込み中...');
        });
    }
});

/**
 * ページ読み込み完了時にローディング非表示
 */
window.addEventListener('load', function() {
    loading.hide();
});

/**
 * 戻るボタン時もローディング非表示
 */
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        loading.hide();
    }
});
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. スケルトンスクリーン実装（13:00-15:00）

**スケルトンローディング用テンプレート:**

`src/main/resources/templates/fragments/skeleton.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<body>
    <!-- 都道府県カードスケルトン -->
    <div th:fragment="prefecture-skeleton" class="skeleton-card">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
    </div>
    
    <!-- 天気カードスケルトン -->
    <div th:fragment="weather-skeleton" class="skeleton-card">
        <div style="display: flex; gap: 20px;">
            <div class="skeleton" style="width: 80px; height: 80px; border-radius: 50%;"></div>
            <div style="flex: 1;">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
            </div>
        </div>
        <div class="skeleton skeleton-text" style="margin-top: 20px;"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text"></div>
    </div>
    
    <!-- 予報カードスケルトン -->
    <div th:fragment="forecast-skeleton" class="skeleton-card">
        <div class="skeleton" style="width: 60px; height: 20px; margin: 0 auto 10px;"></div>
        <div class="skeleton" style="width: 80px; height: 80px; margin: 0 auto 10px; border-radius: 50%;"></div>
        <div class="skeleton skeleton-text"></div>
    </div>
</body>
</html>
```

**スケルトン表示用JavaScript:**

```javascript
/**
 * スケルトンローディング表示
 */
function showSkeletonLoading(containerId, count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-card';
        skeleton.innerHTML = `
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-text"></div>
            <div class="skeleton skeleton-text"></div>
        `;
        container.appendChild(skeleton);
    }
}

/**
 * スケルトンローディング非表示
 */
function hideSkeletonLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.classList.remove('loading');
}
```

---

### 5. 遅延ローディングの実装（15:00-16:30）

**画像遅延ロード:**

```html
<!-- 通常の画像 -->
<img src="/images/weather-icon.png" alt="天気アイコン">

<!-- 遅延ロード -->
<img data-src="/images/weather-icon.png" 
     alt="天気アイコン"
     class="lazy-load"
     src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect fill='%23f0f0f0'/%3E%3C/svg%3E">
```

**遅延ロードJavaScript:**

```javascript
/**
 * Intersection Observerで画像遅延ロード
 */
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img.lazy-load');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-load');
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // フォールバック：すぐにロード
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
});
```

---

### 6. 実装テスト（16:30-17:00）

**テストページ:** `src/main/resources/templates/practice/loading-demo.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('ローディングデモ')}"></head>
<body>
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <div class="container">
        <h1>ローディング機能デモ</h1>
        
        <!-- スピナー一覧 -->
        <section class="mb-xl">
            <h2>スピナー</h2>
            
            <div class="grid grid-4">
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-center">基本</h3>
                        <div class="spinner" style="border-top-color: #3498db;"></div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-center">カラフル</h3>
                        <div class="spinner-colorful"></div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-center">パルス</h3>
                        <div class="spinner-pulse" style="background: #3498db;"></div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-center">ドット</h3>
                        <div class="spinner-dots">
                            <div class="dot" style="background: #3498db;"></div>
                            <div class="dot" style="background: #e74c3c;"></div>
                            <div class="dot" style="background: #2ecc71;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- ボタンローディング -->
        <section class="mb-xl">
            <h2>ボタンローディング</h2>
            <button class="btn btn-primary" onclick="simulateLoading(this)">
                クリックしてローディング
            </button>
        </section>
        
        <!-- オーバーレイ -->
        <section class="mb-xl">
            <h2>オーバーレイローディング</h2>
            <button class="btn btn-primary" onclick="showOverlay()">
                オーバーレイ表示
            </button>
        </section>
        
        <!-- スケルトン -->
        <section class="mb-xl">
            <h2>スケルトンスクリーン</h2>
            <div id="skeletonDemo"></div>
            <button class="btn btn-primary" onclick="showSkeleton()">
                スケルトン表示
            </button>
        </section>
    </div>
    
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <script th:src="@{/js/loading.js}"></script>
    <script>
        function simulateLoading(btn) {
            btn.classList.add('btn-loading');
            btn.disabled = true;
            
            setTimeout(() => {
                btn.classList.remove('btn-loading');
                btn.disabled = false;
            }, 2000);
        }
        
        function showOverlay() {
            loading.show('処理中...');
            
            setTimeout(() => {
                loading.updateMessage('もうすぐ完了...');
            }, 1500);
            
            setTimeout(() => {
                loading.hide();
            }, 3000);
        }
        
        function showSkeleton() {
            const container = document.getElementById('skeletonDemo');
            container.innerHTML = `
                <div class="skeleton-card">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text"></div>
                </div>
            `;
            
            setTimeout(() => {
                container.innerHTML = '<p>データ読み込み完了！</p>';
            }, 2000);
        }
    </script>
</body>
</html>
```

---

## ✅ チェックリスト

- [ ] loading.cssを作成した
- [ ] loading.jsを作成した
- [ ] スピナー（4種類）を実装した
- [ ] オーバーレイローディングを実装した
- [ ] スケルトンスクリーンを実装した
- [ ] ボタンローディングを実装した
- [ ] 遅延ロードを実装した
- [ ] デモページを作成した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): ローディング機能実装"
git push origin feature/day-31
```

---

## 📚 参考リンク

### CSS Animation
- [CSS Animations（日本語）](https://developer.mozilla.org/ja/docs/Web/CSS/CSS_Animations/Using_CSS_animations)
- [Loading Spinner Examples](https://loading.io/css/)

### Intersection Observer
- [Intersection Observer API（日本語）](https://developer.mozilla.org/ja/docs/Web/API/Intersection_Observer_API)
- [遅延ロード実装（日本語）](https://qiita.com/tanaka-takuto/items/c5d0bd39e6a3e1d9292b)

### UX
- [ローディングのUX（日本語）](https://qiita.com/baby-degu/items/c6d0cf2e4b2e0b1c0d4d)

---

## 🆘 トラブルシューティング

### スピナーが表示されない
**症状:** ローディングが表示されない

**原因:** CSSが読み込まれていない

**解決策:**
```html
<link rel="stylesheet" th:href="@{/css/loading.css}">
```

### オーバーレイが表示されたまま
**症状:** ローディングが消えない

**原因:** hide()が呼ばれていない

**解決策:**
```javascript
window.addEventListener('load', function() {
    loading.hide();
});
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - 各種スピナー
   - オーバーレイローディング
   - スケルトンスクリーン
   - 遅延ロード

2. **学んだこと:**
   - CSSアニメーション
   - Intersection Observer API
   - UX向上テクニック

3. **明日への引き継ぎ:**
   - Day 32で天気アイコン実装

---

## 🎉 完了後

次は [Day 32](day-32.md) へ

お疲れさまでした！
