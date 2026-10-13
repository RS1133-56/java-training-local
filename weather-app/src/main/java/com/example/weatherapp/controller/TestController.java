package com.example.weatherapp.controller;

import com.example.weatherapp.entity.TestMessage;
import com.example.weatherapp.service.TestMessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
@RequestMapping("/test")
public class TestController {
    
    private final TestMessageService testMessageService;
    
    @GetMapping
    public String showMessages(Model model) {
        model.addAttribute("messages", testMessageService.getAllMessages());
        return "test";
    }
    
    @PostMapping
    public String createMessage(@RequestParam String message) {
        testMessageService.createMessage(message);
        return "redirect:/test";
    }
}