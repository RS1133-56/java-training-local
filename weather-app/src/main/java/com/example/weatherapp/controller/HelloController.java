package com.example.weatherapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import lombok.extern.slf4j.Slf4j;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Controller
@Slf4j
public class HelloController {
    
    @GetMapping("/")
    public String hello(Model model) {
        log.info("Hello endpoint accessed");
        
        String currentTime = LocalDateTime.now()
            .format(DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss"));
        
        log.debug("Current time: {}", currentTime);
        
        model.addAttribute("currentTime", currentTime);
        
        log.info("Returning hello view");
        return "hello";
    }
}