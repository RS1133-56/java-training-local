package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/practice")
public class PracticeController {
    
    // 1. 基本的なGETマッピング
    @GetMapping
    public String index(Model model) {
        model.addAttribute("message", "練習ページ");
        return "practice/index";
    }
    
    // 2. @RequestParamの使用
    @GetMapping("/param")
    public String withParam(
        @RequestParam String name,
        @RequestParam(defaultValue = "0") int age,
        Model model
    ) {
        model.addAttribute("name", name);
        model.addAttribute("age", age);
        return "practice/param";
    }
    
    // 3. @PathVariableの使用
    @GetMapping("/user/{userId}")
    public String userDetail(
        @PathVariable Long userId,
        Model model
    ) {
        model.addAttribute("userId", userId);
        return "practice/user";
    }
    
    // 4. 複数のパスパラメータ
    @GetMapping("/article/{category}/{id}")
    public String articleDetail(
        @PathVariable String category,
        @PathVariable Long id,
        Model model
    ) {
        model.addAttribute("category", category);
        model.addAttribute("id", id);
        return "practice/article";
    }
    
    // 5. @ResponseBodyでJSON返却
    @GetMapping("/json")
    @ResponseBody
    public String returnJson() {
        return "{\"message\": \"Hello JSON\"}";
    }
}