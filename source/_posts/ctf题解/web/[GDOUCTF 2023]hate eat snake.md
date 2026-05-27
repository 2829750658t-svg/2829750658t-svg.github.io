---
title: '[GDOUCTF 2023]hate eat snake'
categories:
  - 
tags: []
abbrlink: 9f0b177
date: 2026-01-31 15:23:32
---
# [GDOUCTF 2023]hate eat snake

方法一：那么根据游戏提示，我们需要在地图上存活60s

那为什么不把地图改大一点呢？

![image-20260131151840121](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260131151840121.png)

控制台直接输入这个，然后开始游戏就行

```
new Snake('eatSnake',10,false,1000,1000)
```

方法二：寻找alert弹框，

在以下位置

这里什么girlfriend想都不用想，就是他们给的flag里的内容，我们只要让alert执行就行

看到getscore要符合一定的分数，寻找getscore

![image-20260131151258559](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260131151258559.png)



看到

```
getScore: function () {
    ///////////////////////
    var score = Math.round((this.timeCounter + new Date().getTime() - this.startTime) / 1000);
    /////////////////////////
    return score;
  },
```

改score的值就行：

这里需要设置断点，在return score的地方，然后在控制台输入score=100000000000

之后继续运行就行，然后就能看到弹窗了

![image-20260131151724370](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260131151724370.png)