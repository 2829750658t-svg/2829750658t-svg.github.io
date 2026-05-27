---
title: 'NewStarCTF2025-Week4-Web 武功秘籍'
abbrlink: 9c3cac17
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week4-Web 武功秘籍

## 知识点：

### 1.CVE(Common Vulnerablilities and Exposures)

![image-20260329153442277](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329153442341.png)



2. ### CMS(content management system)

![image-20260329153626263](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329153626333.png)







## exp:

一开始进去是个网站

有很多图片木马上传点，我选择新闻上传，会发现新闻内容里面的图片无法上传，但是可以看到上传页面的有其他图片上传点

### 1.塞个木马图，抓包改后缀，蚁剑连接

![image-20260330110543214](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330110543370.png)

系统管理下数据库管理里面找到木马图片

![image-20260330110709735](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330110709795.png)



但是蚁剑连接返回为空

![image-20260330110904987](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330110905060.png)

使用disable_functions也不行，因为要求题目是Linux系统

![image-20260330111901392](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330111901458.png)

那就重新上传木马直接看phpinfo吧

![image-20260330111950971](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330111951027.png)



查看

![image-20260330111831492](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330111831593.png)



找到flag，在env里面



![image-20260330112026772](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330112026855.png)