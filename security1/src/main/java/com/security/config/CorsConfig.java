package com.security.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {


  @Bean
  public CorsFilter corsFilter() {
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowCredentials(true); // 내 서버가 응답을 할때 json을 자바스크립트에서 처리할 수 있게 할지를 설정하는
    config.addAllowedOrigin("http://localhost:3000");
    //config.addAllowedOrigin("*"); // 모든 ip에 응답 허용
    config.addAllowedHeader("*"); // 모든 header에 응답 허용
    config.addAllowedMethod("*"); // 모든 post,get,put,delete,patch 요청 허용
    source.registerCorsConfiguration("http://localhost:3000/**", config);
    source.registerCorsConfiguration("/api/v1/**", config);
    return new CorsFilter(source);
  }


}

