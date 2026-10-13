package com.example.weatherapp.repository;

import com.example.weatherapp.entity.TestMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TestMessageRepository extends JpaRepository<TestMessage, Long> {
    // 基本的なCRUD操作は自動で提供される
    // カスタムクエリが必要な場合はここに追加
}