---
title: '[Zer0pts2020]Can you guess it 1'
categories:
  - 
tags: []
abbrlink: 101c8db6
date: 2026-02-02 16:48:54
---
# [Zer0pts2020]Can you guess it?

# 1



```
<?php
include 'config.php'; // FLAG is defined in config.php

if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

if (isset($_GET['source'])) {
  highlight_file(basename($_SERVER['PHP_SELF']));
  exit();
}

$secret = bin2hex(random_bytes(64));
if (isset($_POST['guess'])) {
  $guess = (string) $_POST['guess'];
  if (hash_equals($secret, $guess)) {
    $message = 'Congratulations! The flag is: ' . FLAG;
  } else {
    $message = 'Wrong.';
  }
}
?>
```

## 思考：

从猜数方面来说，我们要考虑绕过

```
  if (hash_equals($secret, $guess)) {
    $message = 'Congratulations! The flag is: ' . FLAG;
    
    ...
    
$secret = bin2hex(random_bytes(64));    //随机生成
```

没有弱比较强比较了，无法绕过

再加上每次刷新页面都随机生成

（

PHP 是一种**无状态（Stateless）**的脚本语言。

- **每一次请求都是新开始：** 当你刷新页面、点击提交按钮或者访问 URL 时，服务器都会启动一个新的 PHP 进程（或线程）

- **内存不共享：** 执行结束都会被**从内存中彻底释放**

- **重新执行：** 当你下一次访问时，PHP 引擎会再次从第一行代码开始跑。

  ）

其实这里我们为什么不可以换一条思路？

```
highlight_file(basename($_SERVER['PHP_SELF']));
```

这个basename我们从来没有见到过之前，我们来了解一下

---

1. **`$_SERVER['PHP_SELF']` 是什么？**

这是一个超全局变量，它保存 **当前正在执行脚本的文件名**，且路径是相对于网站根目录的。

- **它的用途：** 通常用于表单的 `action` 属性，让表单提交给页面自己。
- **它的危险点：** 它是**用户可控**的。

**举例：** 

如果你访问：`http://example.com/index.php` 

>`$_SERVER['PHP_SELF']` 的值就是 `/index.php`。

如果你访问：`http://example.com/index.php/extra/path` 

> `$_SERVER['PHP_SELF']` 会变成 `/index.php/extra/path`。 

2. **`basename()` 是什么？**

一个处理路径字符串的函数。作用：**给它一个路径，它只返回最后的文件名部分。**

- **它的逻辑：** 它会找到路径中最后一个斜杠 `/`（在 Windows 上也会识别 `\`），然后把后面的字符串切出来。

```
echo basename("/var/www/html/config.php"); 
// 输出结果: config.php

echo basename("/index.php/config.php");
// 输出结果: config.php
```

------

如果我们传入index.php/config.php,basename就会把前面部分删掉只留下config.php，而config.php就有我们要的flag

```
highlight_file(basename($_SERVER['PHP_SELF']));
->
highlight_file(basename(/index.php/config.php));
->
highlight_file(config.php);
```

但是这里我们忽略了正则

```
if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

意思是：检查路径是否以 `config.php` 结尾。
```

这里的正则详解->

| **符号**      | **名称**       | **作用**                                                     |
| ------------- | -------------- | ------------------------------------------------------------ |
| `/`           | **定界符**     | 正则开始                                                     |
| `config\.php` | **匹配文本**   | 匹配字符串 `config.php`。因为在正则中 `.` 代表任意字符，所以要转义，注意这里的 `\.` |
| `\/*`         | **斜杠重复**   | `\/` 匹配斜杠 `/`；`*` 代表**重复 0 次或多次**。表示`/`可以重复0-n次 |
| `$`           | **锚点**       | 表示**匹配字符串的末尾**。它要求 `config.php`（或带斜杠的它）必须出现在路径的最后面。 |
| `/i`          | **模式修饰符** | `i` 代表 **Ignore case**（忽略大小写）                       |





怎么办呢？怎么才能输入/index.php/config.php

但是不让正则过滤掉呢？



#### 正则过滤器——%ff

什么是%ff？:其实就是个非法字符

常用非法字符：

| **字符**       | **URL 编码**  | **作用**                                                     |
| -------------- | ------------- | ------------------------------------------------------------ |
| **空字节**     | `%00`         | 经典的“截断”符。很多旧版本的 PHP 看到它就认为字符串结束了。  |
| **点**         | `/.`          | 路径表示“当前目录”。`basename("a.php/.")` 依然返回 `a.php`。 |
| **空格**       | `%20`         | 有时正则会因为末尾有空格而不匹配，但文件系统会自动修剪掉末尾空格。 |
| **非法 UTF-8** | `%80` - `%ff` | 这一段范围内的字节在 UTF-8 中通常都是非法的，都可以用来测试。 |



```
preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])
```

正则检查路径是否以 `config.php` 结尾。

- 如果你访问 `index.php/config.php` → **被拦截**。
- 如果你访问 `index.php/config.php/%ff` → **安全通过**。因为结尾是 `%ff` 这个怪字符，不是 `config.php`。

#### 那是否会影响basename()呢

在某些操作系统（比如 Windows）或者特定的 PHP 版本/配置下，`basename()` 在处理路径时，

如果遇到它**无法识别的非法字符**（比如不可打印的 `%ff`），它有时会采取“忽略”或“截断”的策略。

执行流程如下：

所以他最终拿到的还是config.php



![image-20260202162241328](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202162241328.png)