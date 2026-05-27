---
title: 'BUUCTF MISC 小明的保险箱 1'
abbrlink: 3a81db43
categories: 
  - ctf题解/misc
date: 2026-05-14 22:25:33
---## BUUCTF MISC 小明的保险箱 1

​							 					

小明有一个保险箱，里面珍藏了小明的日记本，他记录了什么秘密呢？。。。告诉你，其实保险箱的密码四位纯数字密码。（答案格式：flag｛答案｝，只需提交答案） 注意：得到的 flag 请包上 flag{} 提交

图片另存为，010打开发现压缩包rar

![image-20260330204504918](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330204504988.png)

linux里foremost分离得到压缩包

爆破密码

```
2026/3/30 20:50:01 - 开始暴力攻击...
2026/3/30 20:50:22 - 口令已成功恢复!
2026/3/30 20:50:22 - '7869' 是这个文件的一个有效口令
```



解压得到

```
flag{75a3d68bf071ee188c418ea6cf0bb043}
```

![image-20260330205146852](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330205146923.png)