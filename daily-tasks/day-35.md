# Day 35: アクセシビリティ対応

## 📅 実施日
- 予定: Week 7 - Day 35
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
WCAG 2.1準拠のアクセシビリティ対応を実装し、すべてのユーザーが使いやすいアプリを実現する

---

## 📋 午前の作業（9:00-13:00）

### 1. アクセシビリティの基礎（9:00-9:30）

**WCAG 2.1 の4原則（POUR）:**

| 原則 | 説明 | 実装例 |
|------|------|--------|
| Perceivable（知覚可能） | 情報が知覚できる | alt属性、字幕 |
| Operable（操作可能） | UIが操作できる | キーボード操作 |
| Understandable（理解可能） | 情報が理解できる | 明確なラベル |
| Robust（堅牢） | 様々な技術で解釈可能 | セマンティックHTML |

**主要な対応項目:**
1. セマンティックHTML
2. キーボード操作
3. スクリーンリーダー対応
4. 色のコントラスト
5. フォーカス管理
6. ARIA属性

---

### 2. セマンティックHTML実装（9:30-11:00）

**index.html改善:**

```html
<!DOCTYPE html>
<html lang="ja" xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('全国天気予報')}"></head>
<body>
    <!-- スキップリンク -->
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    <!-- ナビゲーション -->
    <nav aria-label="メインナビゲーション" th:replace="~{fragments/navbar :: navbar}"></nav>
    
    <!-- メインコンテンツ -->
    <main id="main-content" role="main">
        <div class="container">
            <!-- ページヘッダー -->
            <header>
                <h1>全国天気予報</h1>
                <p>47都道府県の天気情報をチェック</p>
            </header>
            
            <!-- 検索セクション -->
            <section aria-label="検索とフィルタ">
                <h2 class="visually-hidden">都道府県の検索</h2>
                
                <form role="search" aria-label="都道府県検索">
                    <label for="searchInput" class="visually-hidden">都道府県名で検索</label>
                    <input type="search" 
                           id="searchInput" 
                           name="search"
                           placeholder="都道府県名で検索..."
                           aria-describedby="searchHelp">
                    <span id="searchHelp" class="visually-hidden">
                        都道府県名を入力してEnterキーを押すと検索できます
                    </span>
                </form>
                
                <div class="region-filter">
                    <label for="regionSelect">地域で絞り込み:</label>
                    <select id="regionSelect" 
                            name="region"
                            aria-label="地域選択">
                        <option value="">すべての地域</option>
                        <option th:each="r : ${regions}" 
                                th:value="${r}" 
                                th:text="${r}">
                        </option>
                    </select>
                </div>
            </section>
            
            <!-- 都道府県リスト -->
            <section aria-label="都道府県一覧">
                <h2>都道府県リスト</h2>
                
                <div th:each="entry : ${groupedPrefectures}">
                    <h3 th:text="${entry.key}">北海道</h3>
                    
                    <ul role="list" class="prefecture-grid">
                        <li th:each="pref : ${entry.value}">
                            <article class="prefecture-card">
                                <button class="favorite-btn" 
                                        th:attr="data-prefecture-id=${pref.id},
                                                aria-label='${pref.name}をお気に入りに追加',
                                                aria-pressed='false'">
                                    <span aria-hidden="true">☆</span>
                                </button>
                                
                                <a th:href="@{/weather/{id}(id=${pref.id})}"
                                   th:attr="aria-label='${pref.name}の天気を見る'">
                                    <h4 th:text="${pref.name}">東京都</h4>
                                    <p class="prefecture-name-en" 
                                       th:text="${pref.nameEn}"
                                       aria-label="英語名">Tokyo</p>
                                </a>
                            </article>
                        </li>
                    </ul>
                </div>
            </section>
        </div>
    </main>
    
    <!-- フッター -->
    <footer th:replace="~{fragments/footer :: footer}"></footer>
</body>
</html>
```

**アクセシビリティ用CSS:** `src/main/resources/static/css/accessibility.css`

```css
/* ===================================
   アクセシビリティ
   =================================== */

/* スキップリンク */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px 16px;
    text-decoration: none;
    z-index: 9999;
}

.skip-link:focus {
    top: 0;
}

/* 視覚的に非表示（スクリーンリーダーには表示） */
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* フォーカス表示 */
*:focus {
    outline: 3px solid #667eea;
    outline-offset: 2px;
}

/* ボタンのフォーカス */
button:focus,
a:focus {
    outline: 3px solid #667eea;
    outline-offset: 2px;
}

/* ハイコントラストモード対応 */
@media (prefers-contrast: high) {
    :root {
        --primary-color: #0000ee;
        --text-primary: #000000;
        --bg-primary: #ffffff;
        --border-color: #000000;
    }
}

/* 動きを減らす設定 */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* キーボードナビゲーション専用スタイル */
.keyboard-user *:focus {
    outline: 3px solid #667eea;
    outline-offset: 2px;
}

/* タッチデバイスではフォーカスアウトライン非表示 */
.touch-user *:focus {
    outline: none;
}

/* フォーカス可能要素の最小サイズ */
button,
a,
input,
select,
textarea {
    min-width: 44px;
    min-height: 44px;
}

/* コントラスト改善 */
.high-contrast {
    --primary-color: #0000ff;
    --text-primary: #000000;
    --bg-primary: #ffffff;
    --border-color: #000000;
}

.high-contrast a {
    text-decoration: underline;
    font-weight: bold;
}
```

---

### 3. キーボード操作実装（11:00-12:00）

**キーボードナビゲーション:** `src/main/resources/static/js/keyboard-navigation.js`

```javascript
/**
 * キーボードナビゲーション
 */
class KeyboardNavigation {
    constructor() {
        this.init();
    }
    
    init() {
        // キーボードユーザー検出
        document.addEventListener('keydown', this.detectKeyboardUser.bind(this));
        document.addEventListener('mousedown', this.detectMouseUser.bind(this));
        
        // キーボードショートカット
        document.addEventListener('keydown', this.handleShortcuts.bind(this));
        
        // フォーカストラップ（モーダル用）
        this.setupFocusTrap();
    }
    
    /**
     * キーボードユーザー検出
     */
    detectKeyboardUser(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-user');
            document.body.classList.remove('mouse-user');
        }
    }
    
    /**
     * マウスユーザー検出
     */
    detectMouseUser() {
        document.body.classList.add('mouse-user');
        document.body.classList.remove('keyboard-user');
    }
    
    /**
     * キーボードショートカット
     */
    handleShortcuts(e) {
        // Ctrl/Cmd + K: 検索フォーカス
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Esc: モーダルを閉じる
        if (e.key === 'Escape') {
            this.closeModals();
        }
        
        // ?: ヘルプ表示
        if (e.key === '?') {
            this.showKeyboardHelp();
        }
    }
    
    /**
     * フォーカストラップ設定
     */
    setupFocusTrap() {
        const modals = document.querySelectorAll('[role="dialog"]');
        
        modals.forEach(modal => {
            modal.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    this.trapFocus(e, modal);
                }
            });
        });
    }
    
    /**
     * フォーカストラップ
     */
    trapFocus(e, container) {
        const focusable = container.querySelectorAll(
            'a[href], button:not([disabled]), textarea, input, select'
        );
        
        const firstFocusable = focusable[0];
        const lastFocusable = focusable[focusable.length - 1];
        
        if (e.shiftKey) {
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    }
    
    /**
     * モーダルを閉じる
     */
    closeModals() {
        const modals = document.querySelectorAll('[role="dialog"][aria-hidden="false"]');
        modals.forEach(modal => {
            modal.setAttribute('aria-hidden', 'true');
            modal.style.display = 'none';
        });
    }
    
    /**
     * キーボードヘルプ表示
     */
    showKeyboardHelp() {
        alert(`
キーボードショートカット:
Ctrl/Cmd + K: 検索
Tab: 次の要素へ移動
Shift + Tab: 前の要素へ移動
Enter/Space: 選択・実行
Esc: モーダルを閉じる
?: このヘルプを表示
        `);
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', function() {
    new KeyboardNavigation();
});
```

---

### 昼休憩（12:00-13:00）

---

## 📋 午後の作業（13:00-17:00）

### 4. ARIA属性の追加（13:00-15:00）

**お気に入りボタンARIA対応:**

```javascript
/**
 * お気に入りボタンのARIA更新
 */
function updateFavoriteButtonAria(prefectureId, button, prefectureName) {
    const isFav = favoritesManager.isFavorite(prefectureId);
    
    // aria-pressed更新
    button.setAttribute('aria-pressed', isFav);
    
    // aria-label更新
    const label = isFav 
        ? `${prefectureName}をお気に入りから削除`
        : `${prefectureName}をお気に入りに追加`;
    button.setAttribute('aria-label', label);
    
    // 視覚的表示
    button.innerHTML = isFav 
        ? '<span aria-hidden="true">★</span>'
        : '<span aria-hidden="true">☆</span>';
}
```

**ローディングARIA対応:**

```javascript
/**
 * ローディングのARIA通知
 */
function showLoadingWithAria(message = '読み込み中') {
    loading.show(message);
    
    // aria-live領域に通知
    announceToScreenReader(message);
}

function announceToScreenReader(message) {
    const announcer = document.getElementById('aria-announcer');
    if (announcer) {
        announcer.textContent = message;
    }
}
```

**ARIA Live Region追加（HTML）:**

```html
<!-- スクリーンリーダー用通知領域 -->
<div id="aria-announcer" 
     class="visually-hidden" 
     role="status" 
     aria-live="polite" 
     aria-atomic="true">
</div>
```

---

### 5. 色のコントラスト改善（15:00-16:00）

**コントラストチェックと改善:**

```css
/* 最小コントラスト比 4.5:1 を確保 */

/* Before: コントラスト不足 */
.btn-primary {
    background: #667eea; /* 薄すぎる */
    color: white;
}

/* After: コントラスト改善 */
.btn-primary {
    background: #5568d3; /* より濃く */
    color: white;
}

/* リンクのコントラスト */
a {
    color: #0056b3; /* WCAG AA準拠 */
}

/* エラーメッセージ */
.error-text {
    color: #c0392b; /* 十分なコントラスト */
}

/* 成功メッセージ */
.success-text {
    color: #27ae60; /* 十分なコントラスト */
}

/* 無効状態 */
button:disabled {
    background: #95a5a6;
    color: #ecf0f1;
    opacity: 0.6;
}
```

---

### 6. アクセシビリティテスト（16:00-17:00）

**テストチェックリスト:** `accessibility-checklist.md`

```markdown
# アクセシビリティチェックリスト

## ✅ セマンティックHTML
- [ ] 適切な見出し階層（h1-h6）
- [ ] ランドマーク（main, nav, aside, footer）
- [ ] リスト（ul, ol）の使用
- [ ] ボタン要素（button, a）の適切な使用

## ✅ キーボード操作
- [ ] Tabキーですべて操作可能
- [ ] フォーカス表示が明確
- [ ] スキップリンクが機能
- [ ] Escキーでモーダルを閉じられる

## ✅ スクリーンリーダー
- [ ] すべての画像にalt属性
- [ ] フォームにlabel
- [ ] ARIA属性の適切な使用
- [ ] aria-live領域の設定

## ✅ 視覚
- [ ] 色のコントラスト比 4.5:1以上
- [ ] 色だけに依存しない情報伝達
- [ ] フォントサイズ16px以上
- [ ] ズーム200%で表示崩れなし

## ✅ モーション
- [ ] prefers-reduced-motion対応
- [ ] 自動再生の制御
- [ ] アニメーションの一時停止

## ✅ テスト実施
- [ ] スクリーンリーダー（NVDA/VoiceOver）
- [ ] キーボードのみで操作
- [ ] 自動チェック（Lighthouse/axe）
```

**自動テスト:**

```html
<!-- Lighthouse でテスト -->
<!-- Chrome DevTools > Lighthouse > Accessibility -->

<!-- axe DevTools でテスト -->
<!-- ブラウザ拡張機能をインストール -->
```

---

## ✅ チェックリスト

- [ ] セマンティックHTMLに変更した
- [ ] ARIA属性を追加した
- [ ] キーボード操作を実装した
- [ ] スキップリンクを追加した
- [ ] 色のコントラストを改善した
- [ ] フォーカス管理を実装した
- [ ] prefers-reduced-motion対応した
- [ ] スクリーンリーダーテストを実施した
- [ ] Lighthouseで90点以上を確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(a11y): アクセシビリティ対応実装"
git push origin feature/day-35
```

---

## 📚 参考リンク

### WCAG
- [WCAG 2.1（日本語）](https://waic.jp/translations/WCAG21/)
- [アクセシビリティ基礎（MDN）](https://developer.mozilla.org/ja/docs/Web/Accessibility)

### ツール
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/)

---

## 🆘 トラブルシューティング

### スクリーンリーダーが読まない
**原因:** aria-hidden="true"が設定されている

**解決策:** 装飾要素のみにaria-hidden使用

### キーボードで操作できない
**原因:** tabindex="-1"が設定されている

**解決策:** tabindex削除または0に変更

---

## 📝 本日のまとめ

1. **実装した機能:**
   - セマンティックHTML
   - ARIA属性
   - キーボード操作
   - アクセシビリティCSS

2. **学んだこと:**
   - WCAG 2.1準拠
   - スクリーンリーダー対応
   - ユニバーサルデザイン

3. **明日への引き継ぎ:**
   - Day 36でテスト・品質保証

---

## 🎉 完了後

次は [Day 36](day-36.md) へ

お疲れさまでした！
