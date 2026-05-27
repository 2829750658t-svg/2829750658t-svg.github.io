---
title: 'NewStar CTF 2025 Week1 - Misc OSINT：天空 belong'
categories:
  - 
tags: []
abbrlink: 799d6190
date: 2026-03-19 20:53:25
---

# NewStar CTF 2025 Week1 - Misc OSINT：天空 belong

### 知识点：

**Open Source Intelligence**

[开源情报](https://zhida.zhihu.com/search?content_id=261410963&content_type=Article&match_order=1&q=开源情报&zhida_source=entity)（Open Source Intelligence,  OSINT）是现代情报分析、安全研究、尽职调查的利器，通过公开信息挖掘高价值线索。本文系统梳理了OSINT数据源与工具，涵盖关系分析、数据集、地理定位、社交媒体、企业信息、威胁情报、APT研究、事实核查、公共记录等领域，为分析师提供全面参考。

---

### 推荐阅读帖子：

接下来先推荐一个大佬的帖子

-->

”[首发]开源情报分析（OSINT）实战指南：从基础到高级的信息收集技术“https://xz.aliyun.com/news/17607

另外一篇

-->

“开源情报（OSINT）数据源与工具全攻略”https://zhuanlan.zhihu.com/p/1937056741192860299

---

### 爬虫下载（跟解题无关，拓展）

我们需要做的就是挖取情报了，刚刚那两个帖子挺有趣的，说实话我从来没有这么“系统”地学习过这种“视奸”方法。

于是花费了半天时间来kaihe自己和好朋友

题外话：

大家可以尝试下载一下maigret来玩一下，github有

语法：

```
maigret --web 5000	//这个直接打开本地5000端口就可以在线查看搜索了，如下图
```

![b1c6e20634ea23f8f0acffc687fcb3f2](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319204853574.png)

还有其他语法，自行搜索吧

![3bec0dc1ec9543435db441aca822a6ae](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319204904393.png)



---

### 解题思路：

ok进入正题



气死我了，这么简单的题目整了我一个多小时

首先你可以根据010或者stegsolve查看exif图片自带信息

也可以简单打开一个在线识别网站：https://exif.tuchong.com

![image-20260319203905526](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319203905848.png)

已知设备小米，时间，就差航班号和城市

但是根据图片我们可以看到飞机的注册编号：b7185

![image-20260319204043168](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319204043237.png)

那么简单了，只要打开一个能查询到航班的网站就ok

https://www.flightera.net/zh

飞机降落时间15：17

但是图片是15：03拍的，说明有可能是在湖南省也有可能在湖北省

长沙和武汉都试一下

payload：

```
flag{UQ3574_武汉市_Xiaomi}
```

![image-20260319204221284](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260319204221384.png)

这道题目让我感觉我还是有点可以去当侦探的天赋的，感谢出题人

