---
title: 'NewStar CTF 2025 Week1 - misc EZ_fence'
categories:
  - 
tags: []
abbrlink: 68bc984e
date: 2026-03-07 14:12:24
---
# NewStar CTF 2025 Week1 - misc EZ_fence



题目：

“

RAR 发现一张残缺的照片竟然需 要 4 颗钉子才能钉住，照片里面似乎藏着秘密。

”

1.说照片里面有秘密不如先看看照片里面能找到什么

->找到了flag还有rar压缩包



![image-20260206150445828](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206150445828.png)



于是选择binwalk查看和分离(参数-e)

不知道为什么foremost分离不出来

![image-20260206150507159](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206150507159.png)

这里面需要密码

这时候联想到栅栏fence密码和四个栏数（四个钉子），但是我们去哪里找到这个密码呢？



2.查看属性发现高度被修改了

![image-20260206144119011](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206144119011.png)



打开steglove改一些数据

![image-20260206144036614](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206144036614.png)

找到宽和长修改

理解：

1.FF C0 ->JPEG 的 **Start of Frame** 标记

2.00 11 ->该段内容的长度

3.08    ->精确度

![image-2170920260206144532.png](/images/image-2170920260206144532.png)

就得到了图片里面的内容：

```
8426513709qazwsxedcrfvtgbyhnu jmikop1QWSAERFDTYHGUIKJOPLMNBVCXZ -_


rdh9zfwzSgoVA7GWtLPQJK=vwuZvjhvPyyvjnMWoSotB
```

2.1先用四个栏数看看解密，发现w型居然有点像base64

```
rdh9zfwzSgoVA7GWtLPQJK=vwuZvjhvPyyvjnMWoSotB
```



![image-20260206145446658](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206145446658.png)

2.2而这时候照片里面得到这串码刚好可以做解码的字母表

注意如果直接复制原码会出错，记得删空格还要转义后面两个符号

```
8426513709qazwsxedcrfvtgbyhnujmikoplQWSAERFDTYHGUIKJOPLMNBVCXZ\-\_
```

![image-20260206150118982](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206150118982.png)





密码拿到解压压缩包即可拿到flag





