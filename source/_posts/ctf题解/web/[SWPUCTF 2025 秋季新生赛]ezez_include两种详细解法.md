---
abbrlink: b5b8cee2
title: '[SWPUCTF 2025 秋季新生赛]ezez_include两种详细解法'
categories:
  - 
date: 2026-03-18 18:50:20
---
# [SWPUCTF 2025 秋季新生赛]ezez_include



## 方法一：日志文件包含

一开始考虑的是文件上传，dirsearch扫描出来有upload页面

结果根据响应页面这个版本的文件上传漏洞完全做不出来，服务器解析不了

换个思路，文件包含

![image-20260318165829606](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260318165829766.png)



### 利用日志包含漏洞

---

#### 什么是日志包含漏洞：就是把恶意代码塞在日志中，然后利用包含漏洞读取日志时就可以查看了

#### 过程：（针对于访问日志）

1.发送访问请求：

修改 `User-Agent` 或访问带代码的 URL

服务器会自动把你的请求写进磁盘上的日志文件

```
User-Agent：<?php phpinfo(); ?>
或者
GET /<?php phpinfo(); ?> HTTP/1.1
```

2.访问日志：

利用漏洞`include` 这个日志文件

/var/log/nginx/access.log

![image-20260318165610795](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260318165610884.png)



payload:

改ua和nss

![image-20260318165549009](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260318165556190.png)

---

## 方法二：文件上传漏洞

写完看了一下大佬们的题解，发现其实我尝试过蚁剑连接中就差一个步骤就成功了：因为我没有真正激活木马

很容易发现文件（这里指jpg文件，估计是白名单过滤）上传成功之后，我们点击back回到index页面，继续输入成功的upload/shell.jpg上传路径，页面回显居然就是如图所示简单的一行字

->说明是正常存入木马了而且php解析成功（不然就是400报错了）

但是我们蚁剑连接的页面在哪儿呢？

要注意：这里的蚁剑链接路径在木马执行页面也就是index.php，但是我们不能忘记一些参数：

比如说你刚开始在抓包的时候，发现了只要输入你想读取的文件，然后点击read，body中就会有

```
nss=你输入的文件
```

木马虽然在 `upload/shell.jpg` 里，但它只是一个**死文件**

我们找到的真正木马执行的地方->也就要加入参数nss=upload/shell.jpg，这时候相当于手动点击了read按钮

这样index.php就能运行木马了



![image-20260318183501128](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260318183501222.png)

之后就找flag吧：在根目录下

![image-20260318184859767](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260318184859888.png)



---



知识点补充：

日志漏洞利用的另外一种方法

### Error Log（错误日志）

当服务器处理请求出错（如 404 Not Found, 403 Forbidden, 或 PHP 运行报错）时，相关信息写入 `error.log`。

- 如果你请求一个不存在的文件：`GET /non_existent_<?php phpinfo(); ?>` 

  `error.log` 会记录： `[error] [client 192.168.1.1] File does not exist: /var/www/html/non_existent_<?php phpinfo(); ?>`

- **差异性**：有些 Apache 配置会对 URL 路径进行转义（Encoding），导致 `access.log` 里的 `<` 变成 `\x3c`。

  但在 `error.log` 的错误路径描述中，有时能保持原始字符。

然后在文件包含漏洞中查看/var/log/apache（这里不同服务器名字不一样）/error.log即可

---

