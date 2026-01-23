---
title:  web-ssrf
date: 2026-01-21 19:39:43
tags: [web-ssrf]
categories:
  - ctf题解
  - web
---



## web-ssrf

## 		SSRF = 服务器端请求伪造

## 特点

1. **主体是服务器**：请求是「服务器发起」的，不是你的电脑；
2. **权限是服务器的权限**：服务器能访问的资源（本地文件、内网 IP），你本来访问不到，但通过 SSRF 就能间接访问；
3. **核心是 “伪造请求”**：你伪造一个服务器会执行的请求（比如本地文件地址、内网地址），服务器替你执行。



## [网鼎杯 2018]Fakebook

### 1



1.注册登陆界面，sqlmap扫描



```powershell
python dirsearch.py -u "http://3992b9c4-b99e-44db-96b6-111d3cb92681.node5.buuoj.cn:81/" -e php --threads 1 --delay 3 -w ./ctf_core.txt
```



![image-20251217210112375](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251217210112375.png![image-20251217210507607](/images/image-20251217210507607.png)



![image-20251217204024349](/images/image-20251217204024349.png)

打开备份文件



```
<?php


class UserInfo
{
    public $name = "";
    public $age = 0;
    public $blog = "";

    public function __construct($name, $age, $blog)
    {
        $this->name = $name;
        $this->age = (int)$age;
        $this->blog = $blog;
    }

    function get($url)
    {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $output = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if($httpCode == 404) {
            return 404;
        }
        curl_close($ch);

        return $output;
    }

    public function getBlogContents ()
    {
        return $this->get($this->blog);
    }

    public function isValidBlog ()
    {
        $blog = $this->blog;
        return preg_match("/^(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?$/i", $blog);
    }

}
```



方法一：

```plaintext
用户构造恶意序列化字符串 → 后端用unserialize()解析 → 生成篡改了blog属性的UserInfo对象 → 调用getBlogContents() → 执行curl_exec() → 读取flag.php
```











方法2：sql注入

注册，登录，发现蓝字

![image-20251217215524707](/images/image-20251217215524707.png)



点击得到no参数





![image-20251217215543418](/images/image-20251217215543418.png)



发现过滤

![image-20251217210311771](/images/image-20251217210311771.png)





![image-20251217210702831](/images/image-20251217210702831.png)





2.1

```
view.php?no=-1%20union/**/select%201,2,3,4--+
```

为什么是-1不是1？

1. **no=-1**：靶机里根本没有编号为 - 1 的记录，原 SQL 查询返回空结果；此时`union select`的结果会补位显示在页面上，注入成功。
2. **no=1**：靶机里有编号为 1 的真实记录，原 SQL 查询结果会覆盖`union select`的结果，你看不到注入效果（或因列类型不兼容直接报错），看似 “失败”。

核心就一句话：`-1`让原查询无结果，注入语句的结果能显示；`1`让原查询有结果，把注入结果盖住了。

这就是为什么我前面在输入1的时候注入点一直返回admin用户名，而没有任何回显

![image-20251217212408795](/images/image-20251217212408795.png)



得到回显位为2



2.2

view.php?no=-1%20union/**/select 1,database(),3,4--+



![image-20251217212559085](/images/image-20251217212559085.png)

2. 3

   ?no=-1 union/**/select 1,user(),3,4--+　　　　//数据库信息**,查看权限

```
root@localhos
```

为什么要查看权限？



① **确认权限**：`user()`能看当前数据库用户的权限（比如是不是 root）——root 权限能直接读 / 写文件、查所有库，普通用户只能查当前库；

② **定位目标**：`database()`能知道靶机的核心数据库名（比如`buu_flag`），后续直接查这个库的表 / 字段，就能找到 flag；

③ **验证环境**：比如查`version()`（数据库版本），能判断用什么注入技巧（比如 MySQL5.5 和 8.0 的注入方法有差异）。



是root权限，利用load_file()函数可以用绝对路径去加载一个文件，

load_file(file_name):file_name是一个完整的路径，

于是我们直接用var/www/html/flag.php路径去访问一下这个文件



### 一、核心原理

`load_file()` 是 MySQL 的文件读取函数，root 权限下能直接读取服务器上的文件；`/var/www/html/` 是 Linux 服务器中 PHP 网站的默认根目录，`flag.php` 大概率放在这里，把这个路径传给`load_file()`，就能通过 SQL 注入读取文件内容。

1. 写法：`union select 1,load_file('绝对路径'),3,4`（把路径换成`/var/www/html/flag.php`）；
2. 操作：浏览器直接访问拼接后的 URL，页面会显示`flag.php`的内容；
3. 兜底：读不到就换路径 / 加`hex()`转码，CTF 靶机的`flag.php`几乎都在`/var/www/html/`下，root 权限必能读到

### 二、注入语句写法

 `user()` 替换成 `load_file('/var/www/html/flag.php')` 即可，最终完整 URL：





```
view.php?no=-1union/**/select 1,load_file("/var/www/html/flag.php"),3,4--+
```





```plaintext
# 备用1：网站根目录简写
load_file('/var/www/flag.php')
# 备用2：nginx/apache默认路径
load_file('/usr/share/nginx/html/flag.php')
# 备用3：临时目录
load_file('/tmp/flag.php')
```



为什么是这个路径，报错时候有显示，请看下图：

![image-20251217214135585](/images/image-20251217214135585.png)

![image-20251217213911581](/images/image-20251217213911581.png)





注入之后发现并没有flag，去抓包看看





**view.php?no=-1%20union/**/select 1,group_concat,3,4--+

