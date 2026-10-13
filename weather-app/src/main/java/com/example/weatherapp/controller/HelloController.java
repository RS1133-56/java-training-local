package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Controller
public class HelloController {
    
    @GetMapping("/")
    public String hello(Model model) {
        String currentTime = LocalDateTime.now()
            .format(DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss"));
        model.addAttribute("currentTime", currentTime);
        return "hello";
    }
}