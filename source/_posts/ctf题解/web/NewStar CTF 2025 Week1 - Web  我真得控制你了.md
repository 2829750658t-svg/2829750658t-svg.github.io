---
title: 'NewStar CTF 2025 Week1 - Web  我真得控制你了'
categories:
  - 
tags: []
abbrlink: b8ab710c
date: 2026-02-04 11:37:06
---
# NewStar CTF 2025 Week1 - Web 我真得控制你了



就算禁用我们还是可以打开看码的

火狐： 右上角三个横线->更多工具->web开发者工具

![image-20260204111049114](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204111049114.png)



那么就算我们禁用了js，也同时禁用了按钮，所以不如直接绕过：

因为看到了

```
<form id="nextLevelForm" method="POST" action="next-level.php">
            <input type="hidden" name="access" value="1">
            <input type="hidden" name="csrf_token" value="c79b33582967a0c72527f8d08071e37802377527cd050bebf60bc4d5ccb2426d">
        </form>
```

我们便知道我们要去next-level.php，但是这里需要提交表单form才能执行动作去到next-level.php

控制台输入：

```
javascript:document.getElementById('nextLevelForm').submit();
```

1. `javascript:` —— 切换执行环境

- **它是啥**：这是一个“伪协议”。
- **作用**：通常你在地址栏输入 `http://` 是为了**跳转网页**。当你输入 `javascript:` 时，是告诉浏览器：“**停下！不要跳走，就在这个页面里运行我后面写的代码。**”
- **关键点**：它能让你以“管理员”权限运行脚本，无视页面上那些不让你点右键、不让你按 F12 的限制。

2. `document.getElementById('nextLevelForm')` —— 定位目标对象

- **`document`**：代表你当前看到的整个网页文档。
- **`.getElementById('...')`**：这是浏览器自带的一个搜索功能。
- **`'nextLevelForm'`**：这是你在源码里看到的那个表单的唯一 ID（身份证号）。
- **执行结果**：计算机找到了那个隐藏的、装着 `csrf_token` 的表单容器。

3. `.submit();` —— 激活内置功能

- **它是啥**：这是 HTML 表单（Form）对象自带的一个**原生函数**。
- **作用**：它直接向表单的 `action` 目标（也就是 `next-level.php`）发起 POST 请求。
- **为什么选它**：因为它是**强制性**的。网页源码里那个按钮被设置了 `disabled=true`。而 `.submit()` 是在“逻辑层”直接发号施令，它不需要经过那个变灰的按钮。





然后跳转到了下一关——弱密码爆破

![image-20260204112545609](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204112545609.png)

抓包

![image-20260203211535220](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203211535220.png)

密码:111111

下一关来到了源码

```

源码
<?php
error_reporting(0);

function generate_dynamic_flag($secret) {
    return getenv("ICQ_FLAG") ?: 'default_flag';
}


if (isset($_GET['newstar'])) {
    $input = $_GET['newstar'];
    
    if (is_array($input)) {
        die("恭喜掌握新姿势");
    }
    

    if (preg_match('/[^\d*\/~()\s]/', $input)) {
        die("老套路了，行不行啊");
    }
    

    if (preg_match('/^[\d\s]+$/', $input)) {
        die("请输入有效的表达式");
    }
    
    $test = 0;
    try {
        @eval("\$test = $input;");
    } catch (Error $e) {
        die("表达式错误");
    }
    
    if ($test == 2025) {
        $flag = generate_dynamic_flag($flag_secret);
        echo "<div class='success'>拿下flag！</div>";
        echo "<div class='flag-container'><div class='flag'>FLAG: {$flag}</div></div>";
    } else {
        echo "<div class='error'>大哥哥泥把数字算错了: $test ≠ 2025</div>";
    }
} else {
    ?>
<?php } ?>
```



```
@eval("\$test = $input;");
```

这里提示我们一个思路，既然是eval那么可以给他塞一个计算表达式啊

```
preg_match('/[^\d*\/~()\s]/'
preg_match('/^[\d\s]+$/'
```

这两个正则：

1.^出现了在括号内是排除：如果输入出现了除了`数字 * / ~ （） 空格`之外的东西会失败

2.^出现在括号之外，说明在开头的意思，再加上$表示结尾：

如果输入从头到尾只输入了`数字和空格`，也会失败

那么构造payload

```
$test == 45*45
```

抓包传入

![image-20260203211506988](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203211506988.png)