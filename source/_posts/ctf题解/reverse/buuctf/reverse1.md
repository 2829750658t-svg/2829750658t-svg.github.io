---
title: 'reverse1'
categories:
  - 
tags: []
abbrlink: a51de1
date: 2026-01-28 16:48:59
---


# reverse 1

# 

## 快捷键：

shift+f12 字符串搜索窗口

x交叉搜索

f5反汇编c

r数字转ascii



## 解法:

进去是一个exe程序，可以用脱壳软件脱壳，

但是这个没有壳

直接ida反汇编就ok





### 1.查看

shift+f12 字符串搜索窗口，搜flag，找到相关内容

双击打开，再交叉引用找到文件位置并打开（找到这个字符串在什么时候被引用了），反汇编c看代码

![image-20260128153736998](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260128153736998.png)

### 1.1 strncmp函数

strncmp(Str1, Str2, v5)

比较前两个字符串，前v5个位置；

相等值为0；

大于值为正数；

小于值为负数；



str1是什么？

->

 sub_1400111D1("input the flag:");猜测d1是printf；

 sub_14001128F("%20s", Str1);

可以看到str1是我们输入的内容；

str2是什么？

->

寻找这个字符串

![image-20260128164335686](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260128164335686.png)



### 1.2 for循环遍历，把所有ascii为111的字符都换为48

这里光标指向后按r，可以把ascii转字符

得到：

![image-20260128153957521](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260128153957521.png)



### 1.3 综合

```
  if ( !strncmp(Str1, Str2, v5) )
    sub_1400111D1("this is the right flag!\n");
```

那么我们输入的str1必须要和str2被转换后的值一摸一样才能得到"this is the right flag!\n"

那不就表明这时候的str1不就是flag吗？



具体原文：

```
int __fastcall main_0(int argc, const char **argv, const char **envp)
{
  char *v3; // rdi
  __int64 i; // rcx
  size_t v5; // rax
  char v7; // [rsp+0h] [rbp-20h] BYREF
  int j; // [rsp+24h] [rbp+4h]
  char Str1[224]; // [rsp+48h] [rbp+28h] BYREF
  __int64 v10; // [rsp+128h] [rbp+108h]

  v3 = &v7;
  for ( i = 82; i; --i )
  {
    *(_DWORD *)v3 = -858993460;
    v3 += 4;
  }
  for ( j = 0; ; ++j )
  {
    v10 = j;
    if ( j > j_strlen(Str2) )
      break;
    if ( Str2[j] == 111 )
      Str2[j] = 48;
  }
  sub_1400111D1("input the flag:");
  sub_14001128F("%20s", Str1);
  v5 = j_strlen(Str2);
  if ( !strncmp(Str1, Str2, v5) )
    sub_1400111D1("this is the right flag!\n");
  else
    sub_1400111D1("wrong flag\n");
  return 0;
}
```




