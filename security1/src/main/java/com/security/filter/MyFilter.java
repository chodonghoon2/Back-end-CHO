package com.security.filter;

import java.io.IOException;
import java.io.PrintWriter;
import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class MyFilter implements Filter {

  @Override
  public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
      throws IOException, ServletException {

    HttpServletRequest req = (HttpServletRequest) request;
    HttpServletResponse res = (HttpServletResponse) response;
    // 토큰 : cos 이걸 만들어줘야함. id pw 정상적으로 들어와서 로그인이 완료되면 토큰을 만들어주고 그걸 응답해준다
    // 요청할 때마다 header에 Authorization에 value값으로 토큰을 가지고 와서
    // 그때 토큰이 넘어오면 이 토큰이 내가 만든 토큰이 맞는지만 검증하면 됨.( RSA , HS256)
    if (req.getMethod().equals("POST")) {
      System.out.println("POST요청됨");
      String headerAuth = req.getHeader("Authorization");
      System.out.println(headerAuth);
      System.out.println("필터작동");

      if (headerAuth.equals("cos")) {
        chain.doFilter(req, res);
      } else {
        PrintWriter out = res.getWriter();
        out.println("인증안됨");
      }
    }
  }

}
