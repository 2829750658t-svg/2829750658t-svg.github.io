---
title: 'webshell后门 1'
categories:
  - 
tags: []
abbrlink: bd616a3f
date: 2026-03-01 12:58:46
---
## webshell后门

### 1

题目提示别忘记看，是找pass

---

文件毕竟是有后门的，我的火绒把他识别了然后删掉了问题文件

别忘记做这道题目之前把火绒给关了

![image-20260223120927376](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260223120927376.png)



可用d盾软件查杀文件，看看可疑文件里面有没有我们想知道的pass



![image-20260223121422380](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260223121422380.png)

打开zp.php之后发现pass



```
/*===================== 程序配置 =====================*/

//echo encode_pass('angel');exit;
//angel = ba8e6c6f35a53933b871480bb9a9545c
// 如果需要密码验证,请修改登陆密码,留空为不需要验证
$pass  = 'ba8e6c6f35a53933b871480bb9a9545c'; //angel


```

