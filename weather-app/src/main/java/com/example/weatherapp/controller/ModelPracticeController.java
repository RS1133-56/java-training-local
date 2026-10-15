package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/model-practice")
public class ModelPracticeController {
    
    @GetMapping
    public String practice(Model model) {
        // 1. 基本データ型
        model.addAttribute("title", "Modelの練習");
        model.addAttribute("count", 100);
        model.addAttribute("isActive", true);
        model.addAttribute("currentTime", LocalDateTime.now());
        
        // 2. リスト
        List<String> fruits = Arrays.asList("Apple", "Banana", "Orange", "Grape");
        model.addAttribute("fruits", fruits);
        
        // 3. Map
        Map<String, Integer> scores = new HashMap<>();
        scores.put("Math", 85);
        scores.put("English", 92);
        scores.put("Science", 78);
        model.addAttribute("scores", scores);
        
        // 4. オブジェクト
        Person person = new Person("Yamada Taro", 30, "Tokyo");
        model.addAttribute("person", person);
        
        // 5. オブジェクトのリスト
        List<Person> people = Arrays.asList(
            new Person("Sato Hanako", 25, "Osaka"),
            new Person("Tanaka Jiro", 35, "Nagoya"),
            new Person("Suzuki Yuki", 28, "Fukuoka")
        );
        model.addAttribute("people", people);
        
        return "model-practice";
    }
    
    // 内部クラスとしてPersonを定義
    public static class Person {
        private String name;
        private int age;
        private String city;
        
        public Person(String name, int age, String city) {
            this.name = name;
            this.age = age;
            this.city = city;
        }
        
        // Getter
        public String getName() { return name; }
        public int getAge() { return age; }
        public String getCity() { return city; }
    }
}