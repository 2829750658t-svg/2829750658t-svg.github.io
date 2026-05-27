---
title: 'NewStarCTF2025-Week3-Web MyGO!!!'
abbrlink: d3bf6579
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week3-Web MyGO!!!

![image-20260319215932189](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319215932266.png)

题目提示我们把flag下载下来

先看看代码，是文件读取漏洞，运用file伪协议绕过

`file://` —— 读取本地文件

```
<?php
$client_ip = $_SERVER['REMOTE_ADDR'];

// 只允许本地访问
if ($client_ip !== '127.0.0.1' && $client_ip !== '::1') {
    header('HTTP/1.1 403 Forbidden');
    echo "你是外地人，我只要\"本地\"人";
    exit;
}

highlight_file(__FILE__);
if (isset($_GET['soyorin'])) {
    $url = $_GET['soyorin'];

    echo "flag在根目录";
    // 普通请求
    $ch = curl_init($url);
    //curl_init($url) 本身只是一个“去访问某个网址”的工具，但它支持多种协议（不仅仅是 http）
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, false); // 直接输出给浏览器
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_BUFFERSIZE, 8192);
    curl_exec($ch);
    curl_close($ch);
    exit;
}

?>
flag在根目录
```

构造：

![image-20260319215133481](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319215133656.png)