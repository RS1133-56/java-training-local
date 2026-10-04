# Day 19: Service層実装（Prefecture）

## 📅 実施日
- 予定: Week 4 - Day 19
- 実施日: YYYY/MM/DD
- 予定時間: 8h (午前4h + 午後4h)
- 実績時間: ____h

## 📅 所要時間
8時間

## 🎯 目標
PrefectureServiceを実装し、ビジネスロジック層を構築する

---

## 📋 午前の作業（9:00-13:00）

### 1. Service層の役割理解（9:00-9:30）

**Service層とは:**
- ビジネスロジックを実装する層
- Controller と Repository の橋渡し
- トランザクション管理
- 複数のRepositoryを組み合わせた処理

**レイヤーアーキテクチャ:**

```
Controller（プレゼンテーション層）
    ↓ HTTPリクエスト/レスポンス
Service（ビジネスロジック層）  ← 今日実装
    ↓ ドメインロジック
Repository（データアクセス層）
    ↓ SQL
Database（永続化層）
```

**Serviceの責務:**
1. ビジネスルールの実装
2. トランザクション境界の定義
3. Entity ↔ DTO の変換
4. 例外のハンドリング
5. ログ出力

---

### 2. PrefectureService実装（9:30-12:00）

**インターフェース作成:** `src/main/java/com/example/weatherapp/service/PrefectureService.java`

```java
package com.example.weatherapp.service;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.entity.Prefecture;

import java.util.List;
import java.util.Map;

/**
 * 都道府県サービスのインターフェース
 */
public interface PrefectureService {
    
    /**
     * 全都道府県を取得
     */
    List<PrefectureDto> findAll();
    
    /**
     * IDで都道府県を取得
     */
    PrefectureDto findById(Long id);
    
    /**
     * IDで都道府県Entityを取得（内部用）
     */
    Prefecture findEntityById(Long id);
    
    /**
     * 地域で都道府県を取得
     */
    List<PrefectureDto> findByRegion(String region);
    
    /**
     * 地域別にグループ化して取得
     */
    Map<String, List<PrefectureDto>> findAllGroupedByRegion();
    
    /**
     * 都道府県名で検索
     */
    PrefectureDto findByName(String name);
}
```

**実装クラス作成:** `src/main/java/com/example/weatherapp/service/impl/PrefectureServiceImpl.java`

```java
package com.example.weatherapp.service.impl;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.mapper.PrefectureMapper;
import com.example.weatherapp.repository.PrefectureRepository;
import com.example.weatherapp.service.PrefectureService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 都道府県サービスの実装クラス
 */
@Service
@Transactional(readOnly = true)
@Slf4j
public class PrefectureServiceImpl implements PrefectureService {
    
    private final PrefectureRepository prefectureRepository;
    private final PrefectureMapper prefectureMapper;
    
    /**
     * コンストラクタインジェクション
     */
    public PrefectureServiceImpl(
        PrefectureRepository prefectureRepository,
        PrefectureMapper prefectureMapper
    ) {
        this.prefectureRepository = prefectureRepository;
        this.prefectureMapper = prefectureMapper;
    }
    
    /**
     * 全都道府県を取得
     * 
     * @return 全都道府県のDTOリスト
     */
    @Override
    public List<PrefectureDto> findAll() {
        log.info("全都道府県を取得");
        
        List<Prefecture> prefectures = prefectureRepository.findAll();
        
        log.debug("取得件数: {}", prefectures.size());
        
        return prefectureMapper.toDtoList(prefectures);
    }
    
    /**
     * IDで都道府県を取得
     * 
     * @param id 都道府県ID
     * @return 都道府県DTO
     * @throws ResourceNotFoundException 存在しない場合
     */
    @Override
    public PrefectureDto findById(Long id) {
        log.info("都道府県を取得: id={}", id);
        
        Prefecture prefecture = prefectureRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException(
                "都道府県が見つかりません: id=" + id
            ));
        
        return prefectureMapper.toDto(prefecture);
    }
    
    /**
     * IDで都道府県Entityを取得（内部用）
     * WeatherServiceから呼ばれる
     * 
     * @param id 都道府県ID
     * @return 都道府県Entity
     * @throws ResourceNotFoundException 存在しない場合
     */
    @Override
    public Prefecture findEntityById(Long id) {
        log.debug("都道府県Entityを取得: id={}", id);
        
        return prefectureRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException(
                "都道府県が見つかりません: id=" + id
            ));
    }
    
    /**
     * 地域で都道府県を取得
     * 
     * @param region 地域名
     * @return 該当地域の都道府県DTOリスト
     */
    @Override
    public List<PrefectureDto> findByRegion(String region) {
        log.info("地域で都道府県を取得: region={}", region);
        
        List<Prefecture> prefectures = prefectureRepository
            .findByRegionOrderById(region);
        
        log.debug("取得件数: {}", prefectures.size());
        
        return prefectureMapper.toDtoList(prefectures);
    }
    
    /**
     * 地域別にグループ化して取得
     * トップページで使用
     * 
     * @return 地域をキーとしたMap<地域名, 都道府県リスト>
     */
    @Override
    public Map<String, List<PrefectureDto>> findAllGroupedByRegion() {
        log.info("地域別グループ化で全都道府県を取得");
        
        List<Prefecture> allPrefectures = prefectureRepository.findAll();
        
        // 地域別にグループ化
        Map<String, List<PrefectureDto>> grouped = allPrefectures.stream()
            .collect(Collectors.groupingBy(
                Prefecture::getRegion,
                LinkedHashMap::new,  // 順序を保持
                Collectors.mapping(
                    prefectureMapper::toDto,
                    Collectors.toList()
                )
            ));
        
        log.debug("グループ数: {}", grouped.size());
        
        return grouped;
    }
    
    /**
     * 都道府県名で検索
     * 
     * @param name 都道府県名
     * @return 都道府県DTO
     * @throws ResourceNotFoundException 存在しない場合
     */
    @Override
    public PrefectureDto findByName(String name) {
        log.info("都道府県名で検索: name={}", name);
        
        Prefecture prefecture = prefectureRepository.findByName(name)
            .orElseThrow(() -> new ResourceNotFoundException(
                "都道府県が見つかりません: name=" + name
            ));
        
        return prefectureMapper.toDto(prefecture);
    }
}
```

**ポイント解説:**

1. **@Service**
   - Spring管理のServiceとして登録
   - シングルトン

2. **@Transactional(readOnly = true)**
   - クラスレベル: デフォルトで読み取り専用
   - パフォーマンス最適化
   - 更新メソッドには`@Transactional`を個別指定

3. **@Slf4j**
   - Lombokでロガー自動生成
   - `log.info()`, `log.debug()` が使える

4. **コンストラクタインジェクション**
   - フィールドインジェクションより推奨
   - テストしやすい
   - 不変性を保証

5. **orElseThrow()**
   - Optionalの値がない場合に例外
   - カスタム例外で明確なエラーメッセージ

---

### 3. カスタム例外作成（11:00-12:00）

`src/main/java/com/example/weatherapp/exception/ResourceNotFoundException.java`:

```java
package com.example.weatherapp.exception;

/**
 * リソースが見つからない場合の例外
 */
public class ResourceNotFoundException extends RuntimeException {
    
    public ResourceNotFoundException(String message) {
        super(message);
    }
    
    public ResourceNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

`src/main/java/com/example/weatherapp/exception/BusinessException.java`:

```java
package com.example.weatherapp.exception;

/**
 * ビジネスロジックエラーの基底例外
 */
public class BusinessException extends RuntimeException {
    
    public BusinessException(String message) {
        super(message);
    }
    
    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## 午後の作業（13:00-17:00）

### 4. Serviceのテスト作成（13:00-15:30）

`src/test/java/com/example/weatherapp/service/PrefectureServiceTest.java`:

```java
package com.example.weatherapp.service;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.entity.Prefecture;
import com.example.weatherapp.exception.ResourceNotFoundException;
import com.example.weatherapp.mapper.PrefectureMapper;
import com.example.weatherapp.repository.PrefectureRepository;
import com.example.weatherapp.service.impl.PrefectureServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * PrefectureServiceのテスト
 * Mockitoを使った単体テスト
 */
@ExtendWith(MockitoExtension.class)
class PrefectureServiceTest {
    
    @Mock
    private PrefectureRepository prefectureRepository;
    
    @Mock
    private PrefectureMapper prefectureMapper;
    
    @InjectMocks
    private PrefectureServiceImpl prefectureService;
    
    private Prefecture tokyoPrefecture;
    private PrefectureDto tokyoDto;
    
    @BeforeEach
    void setUp() {
        // テストデータ準備
        tokyoPrefecture = Prefecture.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .latitude(35.689)
            .longitude(139.692)
            .region("関東")
            .build();
        
        tokyoDto = PrefectureDto.builder()
            .id(13L)
            .name("東京都")
            .nameEn("Tokyo")
            .latitude(35.689)
            .longitude(139.692)
            .region("関東")
            .build();
    }
    
    @Test
    @DisplayName("全都道府県を取得できる")
    void testFindAll() {
        // Given
        List<Prefecture> prefectures = Arrays.asList(tokyoPrefecture);
        List<PrefectureDto> dtos = Arrays.asList(tokyoDto);
        
        when(prefectureRepository.findAll()).thenReturn(prefectures);
        when(prefectureMapper.toDtoList(prefectures)).thenReturn(dtos);
        
        // When
        List<PrefectureDto> result = prefectureService.findAll();
        
        // Then
        assertThat(result).hasSize(1);
        assertThat(result.get(0).getName()).isEqualTo("東京都");
        
        verify(prefectureRepository, times(1)).findAll();
        verify(prefectureMapper, times(1)).toDtoList(prefectures);
    }
    
    @Test
    @DisplayName("IDで都道府県を取得できる")
    void testFindById() {
        // Given
        when(prefectureRepository.findById(13L))
            .thenReturn(Optional.of(tokyoPrefecture));
        when(prefectureMapper.toDto(tokyoPrefecture))
            .thenReturn(tokyoDto);
        
        // When
        PrefectureDto result = prefectureService.findById(13L);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(13L);
        assertThat(result.getName()).isEqualTo("東京都");
        
        verify(prefectureRepository, times(1)).findById(13L);
    }
    
    @Test
    @DisplayName("存在しないIDで例外が発生する")
    void testFindById_NotFound() {
        // Given
        when(prefectureRepository.findById(999L))
            .thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> prefectureService.findById(999L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("都道府県が見つかりません");
        
        verify(prefectureRepository, times(1)).findById(999L);
        verify(prefectureMapper, never()).toDto(any());
    }
    
    @Test
    @DisplayName("地域で都道府県を取得できる")
    void testFindByRegion() {
        // Given
        List<Prefecture> kantoList = Arrays.asList(tokyoPrefecture);
        List<PrefectureDto> kantoDtos = Arrays.asList(tokyoDto);
        
        when(prefectureRepository.findByRegionOrderById("関東"))
            .thenReturn(kantoList);
        when(prefectureMapper.toDtoList(kantoList))
            .thenReturn(kantoDtos);
        
        // When
        List<PrefectureDto> result = prefectureService.findByRegion("関東");
        
        // Then
        assertThat(result).hasSize(1);
        assertThat(result.get(0).getRegion()).isEqualTo("関東");
    }
    
    @Test
    @DisplayName("地域別にグループ化して取得できる")
    void testFindAllGroupedByRegion() {
        // Given
        Prefecture osaka = Prefecture.builder()
            .id(27L)
            .name("大阪府")
            .region("関西")
            .build();
        
        List<Prefecture> allPrefectures = Arrays.asList(
            tokyoPrefecture, 
            osaka
        );
        
        when(prefectureRepository.findAll()).thenReturn(allPrefectures);
        when(prefectureMapper.toDto(tokyoPrefecture)).thenReturn(tokyoDto);
        when(prefectureMapper.toDto(osaka)).thenReturn(
            PrefectureDto.builder().id(27L).name("大阪府").region("関西").build()
        );
        
        // When
        Map<String, List<PrefectureDto>> result = 
            prefectureService.findAllGroupedByRegion();
        
        // Then
        assertThat(result).hasSize(2);
        assertThat(result.get("関東")).hasSize(1);
        assertThat(result.get("関西")).hasSize(1);
    }
}
```

**テストのポイント:**

1. **@ExtendWith(MockitoExtension.class)**
   - JUnit 5でMockitoを使用

2. **@Mock**
   - 依存オブジェクトのモック作成

3. **@InjectMocks**
   - モックを自動注入してインスタンス作成

4. **when().thenReturn()**
   - モックの振る舞いを定義

5. **verify()**
   - メソッド呼び出しの検証

---

### 5. 統合テスト作成（15:30-17:00）

`src/test/java/com/example/weatherapp/service/PrefectureServiceIntegrationTest.java`:

```java
package com.example.weatherapp.service;

import com.example.weatherapp.dto.PrefectureDto;
import com.example.weatherapp.exception.ResourceNotFoundException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.*;

/**
 * PrefectureServiceの統合テスト
 * 実際のデータベースを使用
 */
@SpringBootTest
@Transactional
@Sql("/test-data.sql")
class PrefectureServiceIntegrationTest {
    
    @Autowired
    private PrefectureService prefectureService;
    
    @Test
    @DisplayName("全都道府県を取得できる（統合テスト）")
    void testFindAll_Integration() {
        // When
        List<PrefectureDto> result = prefectureService.findAll();
        
        // Then
        assertThat(result).isNotEmpty();
        assertThat(result).hasSizeGreaterThanOrEqualTo(11);
    }
    
    @Test
    @DisplayName("東京都を取得できる（統合テスト）")
    void testFindById_Tokyo() {
        // When
        PrefectureDto tokyo = prefectureService.findById(13L);
        
        // Then
        assertThat(tokyo).isNotNull();
        assertThat(tokyo.getName()).isEqualTo("東京都");
        assertThat(tokyo.getNameEn()).isEqualTo("Tokyo");
        assertThat(tokyo.getRegion()).isEqualTo("関東");
    }
    
    @Test
    @DisplayName("関東地方の都道府県を取得できる")
    void testFindByRegion_Kanto() {
        // When
        List<PrefectureDto> kanto = prefectureService.findByRegion("関東");
        
        // Then
        assertThat(kanto).hasSize(7);
        assertThat(kanto).extracting(PrefectureDto::getRegion)
            .containsOnly("関東");
    }
    
    @Test
    @DisplayName("地域別グループ化が正しく動作する")
    void testFindAllGroupedByRegion_Integration() {
        // When
        Map<String, List<PrefectureDto>> grouped = 
            prefectureService.findAllGroupedByRegion();
        
        // Then
        assertThat(grouped).isNotEmpty();
        assertThat(grouped.get("関東")).hasSizeGreaterThanOrEqualTo(7);
        assertThat(grouped.get("関西")).hasSizeGreaterThanOrEqualTo(2);
    }
    
    @Test
    @DisplayName("存在しないIDで例外が発生する（統合テスト）")
    void testFindById_NotFound_Integration() {
        // When & Then
        assertThatThrownBy(() -> prefectureService.findById(999L))
            .isInstanceOf(ResourceNotFoundException.class);
    }
}
```

---

## ✅ チェックリスト

- [ ] Service層の役割を理解した
- [ ] PrefectureServiceインターフェース作成
- [ ] PrefectureServiceImpl実装
- [ ] カスタム例外作成
- [ ] 単体テスト作成（Mockito）
- [ ] 統合テスト作成（実DB）
- [ ] すべてのテストがパス
- [ ] GitHubにプッシュ

---

## 📚 参考リンク

- [Spring Serviceの書き方（日本語）](https://qiita.com/disc99/items/21b247e29c77f7e9e8d7)
- [DIとコンストラクタインジェクション（日本語）](https://qiita.com/opengl-8080/items/a528d55f6e673a91903d)
- [Mockitoの使い方（日本語）](https://qiita.com/disc99/items/cfa9ae5fa630e04d0b1f)
- [@Transactionalの使い方（日本語）](https://qiita.com/NagaokaKenichi/items/c3371ce8dea0a1f8fa5b)

---

## 🆘 トラブルシューティング

### テストで `NullPointerException`（`@Mock` の対象がnull）
**原因:** Mockitoの初期化がされていない

**解決策:**
1. テストクラスに `@ExtendWith(MockitoExtension.class)` が付いているか確認
2. テスト対象に `@InjectMocks`、依存先に `@Mock` を付けているか確認

### `UnnecessaryStubbingException` / `Strict stubbing argument mismatch`
**原因:** 使われていないスタブがある、またはスタブの引数と実際の呼び出し引数が違う

**解決策:**
1. そのテストで呼ばれない `when(...)` を削除する
2. `when(repo.findById(13L))` の引数が、実際に渡される値（`13L`、`Long`）と同じか確認

### `NoSuchBeanDefinitionException`（統合テスト）
**原因:** `@SpringBootTest` で必要なBeanが登録されていない

**解決策:**
1. Service・Repositoryに `@Service` / `@Repository` が付いているか確認
2. テストクラスに `@SpringBootTest` が付いているか確認

### `@Transactional` が効かない（ロールバックされない／遅延読み込みでエラー）
**原因:** 同じクラス内のメソッド呼び出しや、`private` メソッドには効かない

**解決策:**
1. `@Transactional` は `public` メソッドに付ける
2. 同じクラス内の別メソッドを呼んでも効かない（外から呼び出すこと）

### カスタム例外が `catch` できない／`throws` が必要と言われる
**原因:** 例外クラスの親が違う

**解決策:**
1. `RuntimeException` を継承しているか確認（検査例外にしない）

---

## 🎉 完了後

次は [Day 20](day-20.md) でOpenMeteoClient（外部API連携）を実装する

お疲れさまでした！
