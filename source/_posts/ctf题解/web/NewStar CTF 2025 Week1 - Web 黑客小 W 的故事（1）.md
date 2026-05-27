---
title: 'NewStar CTF 2025 Week1 - Web 黑客小 W 的故事（1）'
categories:
  - 
tags: []
abbrlink: f3818761
date: 2026-02-06 12:17:07
---
# NewStar CTF 2025 Week1 - Web 黑客小 W 的故事（1）

抓包看到



![image-20260204130701573](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204130701573.png)

修改请求头



![image-20260204130749690](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204130749690.png)



继续修改拿到第二关地址



![image-20260204130811555](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204130811555.png)





注意得用get方法

![image-20260204130858783](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260204130858783.png)



如果还是进不去去控制台传入cookie，我之前直接改会重定向

```
document.cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoiVHJ1ZSIsImxldmVsIjoyfQ.KMoDTrhIPWahIY_BPx0OI_KcqDbeeEqBvniVkbmyFAA; path=/";
```





![image-20260206111218339](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206111218339.png)



“

这样吧，你用 DELETE 的方法把我身上的虫子(chongzi)都弄掉，我就把骨钉给你

”



![image-20260206111532857](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206111532857.png)



输入guding

![image-20260206111518033](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206111518033.png)

![image-20260206111604823](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206111604823.png)

拿到cookie

每次给你新cookie了记得下一个地址要拿去用



又遇见重定向了

你可以在网络里面找到下一关入口的，一般来说双击就进去了

![image-20260206120117649](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206120117649.png)



/Level3_SheoChallenge

结合前面他说身份信息ua，我们修改一下就行，记得别忘记版本号，表示这个技能的牛逼程度





![image-20260206120444082](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206120444082.png)



如果改的版本号比较低，它会提示你太慢了，再修改就欧克



![image-20260206120808076](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206120808076.png)



dashdlash同理，然后得到flag，这里也有重定向，网络里面双击即可



![image-20260206121013366](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206121013366.png)