---
title: 'BUUCTF MISC 九连环'
abbrlink: 8e8560ef
categories: 
  - ctf题解/misc
date: 2026-05-14 22:25:33
---# BUUCTF MISC 九连环

1.binwalk和foremost之后拿到zip，发现要密码，我就试试了123456cry发现不行

![image-20260411212828502](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411212828565.png)

2.打开010发现50 4B 01 02，原来是伪加密，全局方式位标记改成00 00

![image-20260411212927521](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411212927589.png)

保存重新打开发现

![image-20260411212938860](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411212938958.png)

你说给我们一个压缩包，再给我们张图片是什么意思呢？

拿着图片里面的信息解压zip啊

3.图片存在隐写，下载steghide提取图片信息，然后打开复制文本信息，作为密码解压zip压缩包

这里steghide的密码直接回车就好了

>为什么？
>
>如果设置了密码，它会用密码对数据进行加密后再嵌入。
>
>如果没有设置密码（即空密码），它就直接将数据按照算法逻辑塞进图片。

4.解压拿到flag

![image-20260411212719329](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411212719514.png)