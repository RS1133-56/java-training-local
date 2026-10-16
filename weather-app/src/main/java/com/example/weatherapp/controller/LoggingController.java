package com.example.weatherapp.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/logging")
@Slf4j  // Lombokのログ機能を有効化
public class LoggingController {
    
    @GetMapping
    public String practice(Model model) {
        // 各レベルのログ出力
        log.trace("TRACE level log");
        log.debug("DEBUG level log");
        log.info("INFO level log");
        log.warn("WARN level log");
        log.error("ERROR level log");
        
        // 変数を含むログ
        String userName = "Taro";
        int age = 25;
        log.info("User: {}, Age: {}", userName, age);
        
        // 例外ログ
        try {
            int result = 10 / 0;
        } catch (Exception e) {
            log.error("An error occurred", e);
        }
        
        model.addAttribute("message", "ログ出力完了");
        return "logging";
    }
}