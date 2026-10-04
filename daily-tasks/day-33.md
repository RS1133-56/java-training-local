# Day 33: お気に入り機能実装

## 📅 実施日
- 予定: Week 7 - Day 33
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
LocalStorageを使ってお気に入り都道府県を保存し、素早くアクセスできる機能を実装する

---

## 📋 午前の作業（9:00-13:00）

### 1. お気に入り機能の設計（9:00-9:30）

**機能要件:**
1. 都道府県をお気に入りに追加
2. お気に入りから削除
3. お気に入り一覧を表示
4. LocalStorageに永続化

**データ構造:**

```javascript
// LocalStorage保存形式
{
    "favorites": [13, 27, 1],  // 都道府県ID配列
    "lastUpdated": "2024-01-05T15:30:00Z"
}
```

---

### 2. お気に入り管理クラス実装（9:30-12:00）

`src/main/resources/static/js/favorites.js`:

```javascript
/**
 * お気に入り管理クラス
 */
class FavoritesManager {
    constructor() {
        this.storageKey = 'weather_app_favorites';
        this.favorites = this.load();
        this.listeners = [];
    }
    
    /**
     * LocalStorageから読み込み
     */
    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (!data) return [];
            
            const parsed = JSON.parse(data);
            return Array.isArray(parsed.favorites) ? parsed.favorites : [];
        } catch (error) {
            console.error('お気に入りの読み込みエラー:', error);
            return [];
        }
    }
    
    /**
     * LocalStorageに保存
     */
    save() {
        try {
            const data = {
                favorites: this.favorites,
                lastUpdated: new Date().toISOString()
            };
            localStorage.setItem(this.storageKey, JSON.stringify(data));
            this.notifyListeners();
        } catch (error) {
            console.error('お気に入りの保存エラー:', error);
        }
    }
    
    /**
     * お気に入りに追加
     * @param {number} prefectureId - 都道府県ID
     */
    add(prefectureId) {
        const id = parseInt(prefectureId);
        
        if (this.favorites.includes(id)) {
            console.log('既にお気に入りに追加済み:', id);
            return false;
        }
        
        this.favorites.push(id);
        this.save();
        console.log('お気に入りに追加:', id);
        return true;
    }
    
    /**
     * お気に入りから削除
     * @param {number} prefectureId - 都道府県ID
     */
    remove(prefectureId) {
        const id = parseInt(prefectureId);
        const index = this.favorites.indexOf(id);
        
        if (index === -1) {
            console.log('お気に入りに存在しません:', id);
            return false;
        }
        
        this.favorites.splice(index, 1);
        this.save();
        console.log('お気に入りから削除:', id);
        return true;
    }
    
    /**
     * お気に入りトグル
     * @param {number} prefectureId - 都道府県ID
     */
    toggle(prefectureId) {
        if (this.isFavorite(prefectureId)) {
            return this.remove(prefectureId);
        } else {
            return this.add(prefectureId);
        }
    }
    
    /**
     * お気に入りチェック
     * @param {number} prefectureId - 都道府県ID
     * @returns {boolean}
     */
    isFavorite(prefectureId) {
        return this.favorites.includes(parseInt(prefectureId));
    }
    
    /**
     * すべて取得
     * @returns {Array<number>}
     */
    getAll() {
        return [...this.favorites];
    }
    
    /**
     * すべてクリア
     */
    clear() {
        this.favorites = [];
        this.save();
        console.log('お気に入りをすべてクリア');
    }
    
    /**
     * 件数取得
     * @returns {number}
     */
    count() {
        return this.favorites.length;
    }
    
    /**
     * リスナー登録
     * @param {Function} callback - コールバック関数
     */
    addListener(callback) {
        this.listeners.push(callback);
    }
    
    /**
     * リスナー通知
     */
    notifyListeners() {
        this.listeners.forEach(callback => {
            try {
                callback(this.favorites);
            } catch (error) {
                console.error('リスナー実行エラー:', error);
            }
        });
    }
    
    /**
     * エクスポート（JSON）
     * @returns {string}
     */
    export() {
        return JSON.stringify({
            favorites: this.favorites,
            exportedAt: new Date().toISOString()
        }, null, 2);
    }
    
    /**
     * インポート（JSON）
     * @param {string} json - JSONデータ
     */
    import(json) {
        try {
            const data = JSON.parse(json);
            if (Array.isArray(data.favorites)) {
                this.favorites = data.favorites;
                this.save();
                return true;
            }
        } catch (error) {
            console.error('インポートエラー:', error);
        }
        return false;
    }
}

// グローバルインスタンス
const favoritesManager = new FavoritesManager();

/**
 * お気に入りボタンUI更新
 */
function updateFavoriteButton(prefectureId, button) {
    const isFav = favoritesManager.isFavorite(prefectureId);
    
    if (isFav) {
        button.classList.add('active');
        button.innerHTML = '★';
        button.title = 'お気に入りから削除';
    } else {
        button.classList.remove('active');
        button.innerHTML = '☆';
        button.title = 'お気に入りに追加';
    }
}

/**
 * お気に入りボタンクリック処理
 */
function handleFavoriteClick(prefectureId, button) {
    favoritesManager.toggle(prefectureId);
    updateFavoriteButton(prefectureId, button);
    
    // お気に入り件数更新
    updateFavoriteCount();
}

/**
 * お気に入り件数表示更新
 */
function updateFavoriteCount() {
    const count = favoritesManager.count();
    const badge = document.getElementById('favoriteBadge');
    
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
}

/**
 * DOMContentLoaded時の初期化
 */
document.addEventListener('DOMContentLoaded', function() {
    // お気に入りボタン初期化
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(button => {
        const prefectureId = button.getAttribute('data-prefecture-id');
        updateFavoriteButton(prefectureId, button);
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            handleFavoriteClick(prefectureId, button);
        });
    });
    
    // お気に入り件数更新
    updateFavoriteCount();
});
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 3. お気に入りUI実装（13:00-15:00）

**お気に入りボタンCSS:** `src/main/resources/static/css/favorites.css`

```css
/* お気に入りボタン */
.favorite-btn {
    position: absolute;
    top: var(--space-sm);
    right: var(--space-sm);
    width: 40px;
    height: 40px;
    border: none;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 50%;
    font-size: 24px;
    cursor: pointer;
    transition: all var(--transition-base);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-sm);
}

.favorite-btn:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-md);
}

.favorite-btn.active {
    color: #f39c12;
    background: rgba(243, 156, 18, 0.1);
}

/* お気に入りバッジ */
.favorite-badge {
    display: inline-block;
    min-width: 20px;
    padding: 2px 6px;
    background: var(--error-color);
    color: white;
    font-size: var(--font-xs);
    font-weight: var(--font-bold);
    border-radius: var(--radius-full);
    text-align: center;
}

/* お気に入りセクション */
.favorites-section {
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    color: white;
    padding: var(--space-xl);
    border-radius: var(--radius-xl);
    margin-bottom: var(--space-xl);
}

.favorites-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-top: var(--space-lg);
}

.favorite-card {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    text-align: center;
    transition: all var(--transition-base);
    position: relative;
}

.favorite-card:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-5px);
}

.favorite-card .remove-btn {
    position: absolute;
    top: var(--space-xs);
    right: var(--space-xs);
    width: 24px;
    height: 24px;
    background: rgba(231, 76, 60, 0.8);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: var(--font-sm);
    line-height: 1;
}

/* 空の状態 */
.favorites-empty {
    text-align: center;
    padding: var(--space-xxl);
    color: rgba(255, 255, 255, 0.8);
}

.favorites-empty-icon {
    font-size: 64px;
    margin-bottom: var(--space-md);
}
```

**トップページ更新（index.html）:**

```html
<!-- お気に入りセクション -->
<section class="favorites-section" id="favoritesSection" style="display: none;">
    <div class="favorites-header">
        <h2>
            ⭐ お気に入り
            <span class="favorite-badge" id="favoriteBadge">0</span>
        </h2>
        <button class="btn btn-sm" onclick="clearAllFavorites()">
            すべてクリア
        </button>
    </div>
    
    <div class="favorites-grid" id="favoritesGrid">
        <!-- JavaScriptで動的生成 -->
    </div>
    
    <div class="favorites-empty" id="favoritesEmpty">
        <div class="favorites-empty-icon">⭐</div>
        <p>お気に入りの都道府県を追加してください</p>
    </div>
</section>

<!-- 都道府県カードにお気に入りボタン追加 -->
<div class="prefecture-card" style="position: relative;">
    <button class="favorite-btn" 
            data-prefecture-id="${pref.id}"
            onclick="event.stopPropagation();">
        ☆
    </button>
    <a th:href="@{/weather/{id}(id=${pref.id})}">
        <h3 th:text="${pref.name}">東京都</h3>
    </a>
</div>
```

---

### 4. お気に入り表示機能実装（15:00-16:30）

**お気に入り表示JavaScript追加:**

```javascript
/**
 * お気に入り一覧を表示
 */
function renderFavorites() {
    const favoritesSection = document.getElementById('favoritesSection');
    const favoritesGrid = document.getElementById('favoritesGrid');
    const favoritesEmpty = document.getElementById('favoritesEmpty');
    
    const favorites = favoritesManager.getAll();
    
    if (favorites.length === 0) {
        favoritesSection.style.display = 'block';
        favoritesGrid.style.display = 'none';
        favoritesEmpty.style.display = 'block';
        return;
    }
    
    favoritesSection.style.display = 'block';
    favoritesGrid.style.display = 'grid';
    favoritesEmpty.style.display = 'none';
    
    // お気に入りカード生成
    favoritesGrid.innerHTML = '';
    
    favorites.forEach(id => {
        // 都道府県情報取得（DOM から）
        const prefCard = document.querySelector(`[data-prefecture-id="${id}"]`)?.closest('.prefecture-card');
        if (!prefCard) return;
        
        const prefName = prefCard.querySelector('.prefecture-name')?.textContent || `ID: ${id}`;
        
        const card = document.createElement('div');
        card.className = 'favorite-card';
        card.innerHTML = `
            <button class="remove-btn" onclick="removeFavorite(${id})" title="削除">×</button>
            <a href="/weather/${id}" style="color: white; text-decoration: none;">
                <div class="favorite-card-content">
                    <h3>${prefName}</h3>
                </div>
            </a>
        `;
        
        favoritesGrid.appendChild(card);
    });
}

/**
 * お気に入りから削除
 */
function removeFavorite(prefectureId) {
    if (confirm('お気に入りから削除しますか？')) {
        favoritesManager.remove(prefectureId);
        renderFavorites();
        updateFavoriteCount();
        
        // ボタン更新
        const button = document.querySelector(`[data-prefecture-id="${prefectureId}"]`);
        if (button) {
            updateFavoriteButton(prefectureId, button);
        }
    }
}

/**
 * すべてクリア
 */
function clearAllFavorites() {
    if (confirm('すべてのお気に入りをクリアしますか？')) {
        favoritesManager.clear();
        renderFavorites();
        updateFavoriteCount();
        
        // すべてのボタン更新
        document.querySelectorAll('.favorite-btn').forEach(button => {
            const id = button.getAttribute('data-prefecture-id');
            updateFavoriteButton(id, button);
        });
    }
}

// リスナー登録
favoritesManager.addListener(renderFavorites);

// 初期表示
document.addEventListener('DOMContentLoaded', function() {
    renderFavorites();
});
```

---

### 5. テストとデバッグ（16:30-17:00）

**テストページ:** `src/main/resources/templates/practice/favorites-test.html`

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('お気に入り機能テスト')}"></head>
<body>
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <div class="container">
        <h1>お気に入り機能テスト</h1>
        
        <section class="mb-xl">
            <h2>コントロールパネル</h2>
            <div class="grid grid-3">
                <button class="btn btn-primary" onclick="testAdd()">追加テスト</button>
                <button class="btn btn-secondary" onclick="testRemove()">削除テスト</button>
                <button class="btn btn-error" onclick="testClear()">クリアテスト</button>
            </div>
        </section>
        
        <section class="mb-xl">
            <h2>現在のお気に入り</h2>
            <pre id="favoritesDisplay" class="card card-body"></pre>
        </section>
        
        <section class="mb-xl">
            <h2>エクスポート/インポート</h2>
            <button class="btn btn-primary" onclick="exportFavorites()">エクスポート</button>
            <button class="btn btn-secondary" onclick="importFavorites()">インポート</button>
            <textarea id="importExport" class="form-control" rows="5"></textarea>
        </section>
    </div>
    
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <script th:src="@{/js/favorites.js}"></script>
    <script>
        function testAdd() {
            favoritesManager.add(13);
            favoritesManager.add(27);
            favoritesManager.add(1);
            updateDisplay();
        }
        
        function testRemove() {
            favoritesManager.remove(13);
            updateDisplay();
        }
        
        function testClear() {
            favoritesManager.clear();
            updateDisplay();
        }
        
        function exportFavorites() {
            document.getElementById('importExport').value = favoritesManager.export();
        }
        
        function importFavorites() {
            const json = document.getElementById('importExport').value;
            if (favoritesManager.import(json)) {
                alert('インポート成功');
                updateDisplay();
            } else {
                alert('インポート失敗');
            }
        }
        
        function updateDisplay() {
            const display = document.getElementById('favoritesDisplay');
            display.textContent = JSON.stringify({
                favorites: favoritesManager.getAll(),
                count: favoritesManager.count()
            }, null, 2);
        }
        
        // 初期表示
        updateDisplay();
        
        // リスナー登録
        favoritesManager.addListener(updateDisplay);
    </script>
</body>
</html>
```

---

## ✅ チェックリスト

- [ ] FavoritesManagerクラスを実装した
- [ ] LocalStorage連携を実装した
- [ ] お気に入りボタンを実装した
- [ ] お気に入り一覧表示を実装した
- [ ] 追加/削除機能を実装した
- [ ] エクスポート/インポート機能を実装した
- [ ] CSSスタイルを適用した
- [ ] テストページを作成した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): お気に入り機能実装"
git push origin feature/day-33
```

---

## 📚 参考リンク

### LocalStorage
- [LocalStorage（日本語）](https://developer.mozilla.org/ja/docs/Web/API/Window/localStorage)
- [Web Storage API（日本語）](https://developer.mozilla.org/ja/docs/Web/API/Web_Storage_API)

### JavaScript
- [クラス構文（日本語）](https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Classes)
- [イベントリスナー（日本語）](https://developer.mozilla.org/ja/docs/Web/API/EventTarget/addEventListener)

---

## 🆘 トラブルシューティング

### LocalStorageが保存されない
**症状:** リロードすると消える

**原因:** プライベートブラウジングモード

**解決策:** 通常モードで確認

### お気に入りが表示されない
**症状:** UI更新されない

**原因:** リスナーが登録されていない

**解決策:**
```javascript
favoritesManager.addListener(renderFavorites);
```

---

## 📝 本日のまとめ

1. **実装した機能:**
   - お気に入り管理
   - LocalStorage連携
   - お気に入りUI

2. **学んだこと:**
   - LocalStorageの使い方
   - クラス設計
   - イベント駆動設計

3. **明日への引き継ぎ:**
   - Day 34以降で完成に向けた作業

---

## 🎉 完了後

次は [Day 34](day-34.md) へ

お疲れさまでした！
