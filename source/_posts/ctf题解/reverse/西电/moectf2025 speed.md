---
title: 'moectf2025 speed'
categories:
  - 
tags: []
abbrlink: 5f40f32e
date: 2026-03-01 13:15:19
---
# moectf2025 speed

题目提示：

Did you see my little pony? She runs really fast...

---

运行软件后出现窗口，出现后立马闪退

当然你可以录视频截屏看到窗口内容，在后面我们会知道内容就是flag



也可以来好好研究一下底层逻辑：

首先找到窗口函数，winmain

![image-20260225171049172](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225171049172.png)

f5反汇编

得到

![image-20260225182028963](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225182028963.png)

红色部分可能不太清楚，那个就是销毁窗口函数，我们只要调试然后在这里做断点就ok了

然后就可以看到停留的窗口

调试方法：f2断点，断电为红色圆圈的时候，按软件上面的运行键|>



---

以下是我掉过的坑，看到flag就直接去找flag的线索了，没思考题目的意思

得到的flag也是错的



```
  for ( i = 0; i < 100; ++i )
  {
    if ( i >= (unsigned int)'d' )
      j____report_rangecheckfailure();
    Destination[i] = 0;
  }
  
  sub_41132F("please enter the flag:", v7);
  sub_411375("%20s", (char)Str);
  v3 = j_strlen(Str);
  v4 = (const char *)sub_4110BE((int)Str, v3, (int)v14);
  strncpy(Destination, v4, 0x28u);
  v11 = j_strlen(Destination);
  for ( j = 0; j < v11; ++j )
    Destination[j] += j;
  v5 = j_strlen(Destination);
  if ( !strncmp(Destination, Str2, v5) )
    sub_41132F("rigth flag!\n", v8);
  else
    sub_41132F("wrong flag!\n", v8);
  return 0;
}
```







![image-20260225163444356](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225163444356.png)



e3nifIH9b_C@n@dH





![image-20260225165235598](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225165235598.png)