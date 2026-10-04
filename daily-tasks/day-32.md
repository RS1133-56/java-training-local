# Day 32: 天気アイコン表示

## 📅 実施日
- 予定: Week 7 - Day 32
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 🎯 目標
天気コードに対応したアイコンを動的に表示し、視覚的にわかりやすいUIを実現する

---

## 📋 午前の作業（9:00-13:00）

### 1. 天気アイコンシステムの設計（9:00-9:30）

**WMO天気コード対応表:**

| コード | 天気 | 絵文字 | アイコン |
|--------|------|--------|----------|
| 0 | 快晴 | ☀️ | sun |
| 1-3 | 晴れ〜曇り | 🌤️⛅☁️ | cloud-sun |
| 45-48 | 霧 | 🌫️ | fog |
| 51-65 | 雨 | 🌦️🌧️ | rain |
| 71-77 | 雪 | 🌨️❄️ | snow |
| 80-82 | にわか雨 | 🌦️ | shower |
| 95-99 | 雷雨 | ⛈️ | storm |

**アイコン実装方法:**
1. CSS（カスタムアイコン）
2. SVG（スケーラブル）
3. 絵文字（シンプル）
4. アイコンフォント（Font Awesome等）

---

### 2. SVGアイコン作成（9:30-12:00）

`src/main/resources/static/images/weather-icons/`にSVGを作成：

**sun.svg（晴れ）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <circle cx="50" cy="50" r="20" fill="#FDB813"/>
    <g stroke="#FDB813" stroke-width="3" stroke-linecap="round">
        <line x1="50" y1="10" x2="50" y2="20"/>
        <line x1="50" y1="80" x2="50" y2="90"/>
        <line x1="10" y1="50" x2="20" y2="50"/>
        <line x1="80" y1="50" x2="90" y2="50"/>
        <line x1="20" y1="20" x2="27" y2="27"/>
        <line x1="73" y1="73" x2="80" y2="80"/>
        <line x1="20" y1="80" x2="27" y2="73"/>
        <line x1="73" y1="27" x2="80" y2="20"/>
    </g>
</svg>
```

**cloud-sun.svg（曇り時々晴れ）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <circle cx="35" cy="35" r="12" fill="#FDB813"/>
    <path d="M55 50 Q55 40, 65 40 Q75 40, 75 50 Q75 60, 65 60 L40 60 Q30 60, 30 50 Q30 40, 40 40 Q45 40, 48 43" fill="#E0E0E0" stroke="#B0B0B0" stroke-width="2"/>
</svg>
```

**cloud.svg（曇り）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <path d="M25 60 Q25 40, 40 40 Q45 30, 60 30 Q75 30, 75 45 Q90 45, 90 60 Q90 75, 75 75 L25 75 Q10 75, 10 60 Q10 45, 25 45 Z" fill="#B0B0B0"/>
</svg>
```

**rain.svg（雨）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <path d="M20 40 Q20 25, 35 25 Q40 15, 55 15 Q70 15, 70 30 Q85 30, 85 45 Q85 60, 70 60 L20 60 Q5 60, 5 45 Q5 30, 20 30 Z" fill="#7090A0"/>
    <g stroke="#4A90E2" stroke-width="2" stroke-linecap="round">
        <line x1="25" y1="65" x2="22" y2="80"/>
        <line x1="40" y1="65" x2="37" y2="80"/>
        <line x1="55" y1="65" x2="52" y2="80"/>
        <line x1="70" y1="65" x2="67" y2="80"/>
    </g>
</svg>
```

**snow.svg（雪）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <path d="M20 40 Q20 25, 35 25 Q40 15, 55 15 Q70 15, 70 30 Q85 30, 85 45 Q85 60, 70 60 L20 60 Q5 60, 5 45 Q5 30, 20 30 Z" fill="#D0D0D0"/>
    <g fill="#FFFFFF" stroke="#B0B0B0" stroke-width="1">
        <circle cx="25" cy="72" r="3"/>
        <circle cx="40" cy="75" r="3"/>
        <circle cx="55" cy="72" r="3"/>
        <circle cx="70" cy="75" r="3"/>
    </g>
</svg>
```

**storm.svg（雷雨）:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
    <path d="M20 35 Q20 20, 35 20 Q40 10, 55 10 Q70 10, 70 25 Q85 25, 85 40 Q85 55, 70 55 L20 55 Q5 55, 5 40 Q5 25, 20 25 Z" fill="#505050"/>
    <path d="M50 60 L45 75 L52 75 L48 90 L60 70 L53 70 Z" fill="#FDB813"/>
</svg>
```

---

### 3. アイコン表示コンポーネント作成（12:00-12:30）

`src/main/resources/static/js/weather-icons.js`:

```javascript
/**
 * 天気コードからアイコン名を取得
 */
function getWeatherIcon(weatherCode) {
    const code = parseInt(weatherCode);
    
    // 快晴
    if (code === 0) return 'sun';
    
    // 晴れ〜曇り
    if (code >= 1 && code <= 3) {
        if (code === 1) return 'cloud-sun';
        if (code === 2) return 'cloud-sun';
        return 'cloud';
    }
    
    // 霧
    if (code >= 45 && code <= 48) return 'fog';
    
    // 雨
    if (code >= 51 && code <= 67) {
        if (code >= 61 && code <= 67) return 'rain';
        return 'drizzle';
    }
    
    // 雪
    if (code >= 71 && code <= 77) return 'snow';
    
    // にわか雨
    if (code >= 80 && code <= 82) return 'shower';
    
    // にわか雪
    if (code >= 85 && code <= 86) return 'snow-shower';
    
    // 雷雨
    if (code >= 95 && code <= 99) return 'storm';
    
    return 'unknown';
}

/**
 * 天気アイコン要素を作成
 */
function createWeatherIcon(weatherCode, size = 'md') {
    const iconName = getWeatherIcon(weatherCode);
    const iconPath = `/images/weather-icons/${iconName}.svg`;
    
    const img = document.createElement('img');
    img.src = iconPath;
    img.alt = getWeatherDescription(weatherCode);
    img.className = `weather-icon weather-icon-${size}`;
    
    // フォールバック：絵文字
    img.onerror = function() {
        const emoji = getWeatherEmoji(weatherCode);
        this.style.display = 'none';
        const span = document.createElement('span');
        span.textContent = emoji;
        span.className = `weather-emoji weather-emoji-${size}`;
        this.parentNode.replaceChild(span, this);
    };
    
    return img;
}

/**
 * 天気コードから絵文字を取得（フォールバック用）
 */
function getWeatherEmoji(weatherCode) {
    const code = parseInt(weatherCode);
    
    if (code === 0) return '☀️';
    if (code === 1) return '🌤️';
    if (code === 2) return '⛅';
    if (code === 3) return '☁️';
    if (code >= 45 && code <= 48) return '🌫️';
    if (code >= 51 && code <= 67) return '🌧️';
    if (code >= 71 && code <= 77) return '❄️';
    if (code >= 80 && code <= 86) return '🌦️';
    if (code >= 95) return '⛈️';
    
    return '❓';
}

/**
 * DOMContentLoaded時に実行
 */
document.addEventListener('DOMContentLoaded', function() {
    // data-weather-code属性を持つ要素を探してアイコン表示
    const iconPlaceholders = document.querySelectorAll('[data-weather-code]');
    
    iconPlaceholders.forEach(placeholder => {
        const code = placeholder.getAttribute('data-weather-code');
        const size = placeholder.getAttribute('data-size') || 'md';
        const icon = createWeatherIcon(code, size);
        placeholder.appendChild(icon);
    });
});
```

---

### 昼休憩（12:30-13:30）

---

## 📋 午後の作業（13:30-17:00）

### 4. HTMLテンプレート更新（13:30-15:00）

**weather-detail.html更新:**

```html
<!-- 現在の天気アイコン -->
<div class="weather-icon">
    <div data-weather-code="${weather.current.weatherCode}" 
         data-size="xl">
    </div>
</div>

<!-- 予報カードアイコン -->
<div th:each="day : ${weather.dailyForecasts}" class="forecast-card">
    <div class="forecast-weather">
        <div data-weather-code="${day.weatherCode}"
             data-size="lg">
        </div>
        <div class="forecast-description" 
             th:text="${day.weatherDescription}">晴れ</div>
    </div>
</div>
```

**アイコンサイズ用CSS:**

```css
/* 天気アイコンサイズ */
.weather-icon-xs {
    width: 24px;
    height: 24px;
}

.weather-icon-sm {
    width: 32px;
    height: 32px;
}

.weather-icon-md {
    width: 48px;
    height: 48px;
}

.weather-icon-lg {
    width: 64px;
    height: 64px;
}

.weather-icon-xl {
    width: 96px;
    height: 96px;
}

/* 絵文字サイズ */
.weather-emoji-xs { font-size: 24px; }
.weather-emoji-sm { font-size: 32px; }
.weather-emoji-md { font-size: 48px; }
.weather-emoji-lg { font-size: 64px; }
.weather-emoji-xl { font-size: 96px; }

/* アニメーション */
.weather-icon {
    display: inline-block;
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* ホバーエフェクト */
.weather-icon:hover {
    transform: scale(1.1);
    transition: transform 0.3s;
}
```

---

### 5. アイコンギャラリー作成（15:00-16:30）

`src/main/resources/templates/practice/icon-gallery.html`:

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head th:replace="~{fragments/header :: head('天気アイコンギャラリー')}"></head>
<body>
    <div th:replace="~{fragments/navbar :: navbar}"></div>
    
    <div class="container">
        <h1>天気アイコンギャラリー</h1>
        
        <section class="mb-xl">
            <h2>全アイコン</h2>
            <div class="icon-grid">
                <div class="icon-card">
                    <div data-weather-code="0" data-size="xl"></div>
                    <p class="icon-label">快晴 (0)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="1" data-size="xl"></div>
                    <p class="icon-label">晴れ (1)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="2" data-size="xl"></div>
                    <p class="icon-label">一部曇り (2)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="3" data-size="xl"></div>
                    <p class="icon-label">曇り (3)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="45" data-size="xl"></div>
                    <p class="icon-label">霧 (45)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="61" data-size="xl"></div>
                    <p class="icon-label">雨 (61)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="71" data-size="xl"></div>
                    <p class="icon-label">雪 (71)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="80" data-size="xl"></div>
                    <p class="icon-label">にわか雨 (80)</p>
                </div>
                
                <div class="icon-card">
                    <div data-weather-code="95" data-size="xl"></div>
                    <p class="icon-label">雷雨 (95)</p>
                </div>
            </div>
        </section>
        
        <section class="mb-xl">
            <h2>サイズバリエーション</h2>
            <div class="size-demo">
                <div data-weather-code="1" data-size="xs"></div>
                <div data-weather-code="1" data-size="sm"></div>
                <div data-weather-code="1" data-size="md"></div>
                <div data-weather-code="1" data-size="lg"></div>
                <div data-weather-code="1" data-size="xl"></div>
            </div>
        </section>
    </div>
    
    <div th:replace="~{fragments/footer :: footer}"></div>
    
    <script th:src="@{/js/weather-icons.js}"></script>
    
    <style>
        .icon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: var(--space-lg);
            margin: var(--space-xl) 0;
        }
        
        .icon-card {
            background: white;
            padding: var(--space-lg);
            border-radius: var(--radius-lg);
            text-align: center;
            box-shadow: var(--shadow-sm);
        }
        
        .icon-label {
            margin-top: var(--space-md);
            font-size: var(--font-sm);
            color: var(--text-secondary);
        }
        
        .size-demo {
            display: flex;
            align-items: center;
            gap: var(--space-lg);
            background: white;
            padding: var(--space-xl);
            border-radius: var(--radius-lg);
        }
    </style>
</body>
</html>
```

---

### 6. 動作確認（16:30-17:00）

**確認項目:**
- [ ] すべての天気コードでアイコンが表示される
- [ ] SVGアイコンが正しく読み込まれる
- [ ] フォールバック（絵文字）が動作する
- [ ] サイズバリエーションが正しい
- [ ] アニメーションが動作する
- [ ] レスポンシブ対応されている

---

## ✅ チェックリスト

- [ ] SVGアイコンを作成した（9種類）
- [ ] weather-icons.jsを実装した
- [ ] アイコン表示機能を実装した
- [ ] フォールバック機能を実装した
- [ ] CSSアニメーションを追加した
- [ ] アイコンギャラリーを作成した
- [ ] HTMLテンプレートを更新した
- [ ] ブラウザで動作確認した
- [ ] GitHubにコミット・プッシュした

**Gitコミット:**
```bash
git add .
git commit -m "feat(frontend): 天気アイコン表示機能実装"
git push origin feature/day-32
```

---

## 📚 参考リンク

### SVG
- [SVG入門（日本語）](https://developer.mozilla.org/ja/docs/Web/SVG/Tutorial)
- [SVGアイコン作成（日本語）](https://qiita.com/takeshisakuma/items/777e3cb0a54ea7b1dbe7)

### アイコンデザイン
- [Weather Icons](https://erikflowers.github.io/weather-icons/)
- [天気アイコンデザイン](https://www.flaticon.com/packs/weather-99)

---

## 📝 本日のまとめ

1. **実装した機能:**
   - SVG天気アイコン
   - 動的アイコン表示
   - フォールバック機能

2. **学んだこと:**
   - SVG作成
   - 動的DOM操作
   - フォールバック実装

3. **明日への引き継ぎ:**
   - Day 33でお気に入り機能実装

---

## 🎉 完了後

次は [Day 33](day-33.md) へ

お疲れさまでした！
