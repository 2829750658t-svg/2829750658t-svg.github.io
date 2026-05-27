---
title: 'reverse2'
categories:
  - 
tags: []
abbrlink: 99ac4c5b
date: 2026-01-29 11:12:45
---


# reverse 2

按下shift+f12

<img src="https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105246045.png" alt="image-20260129105246045" style="zoom: 67%;" />

进入字符串窗口看到 

.rodata:0000000000400925	00000018	C	this is the right flag!

.data:0000000000601080	00000012	C	{hacking_for_fun}

![image-20260129105358819](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105358819.png)

双击字符串进入这界面，点击aThisIsTheRight，按x键

![image-20260129105543028](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105543028.png)

弹出，按ok

![image-20260129105622612](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105622612.png)

来到新界面，按f5可以反编译c

![image-20260129105721401](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105721401.png)

来到

![image-20260129105815454](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129105815454.png)



```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int stat_loc; // [rsp+4h] [rbp-3Ch] BYREF
  int i; // [rsp+8h] [rbp-38h]
  __pid_t pid; // [rsp+Ch] [rbp-34h]
  char s2[24]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v8; // [rsp+28h] [rbp-18h]

  v8 = __readfsqword(0x28u);
  pid = fork();
  if ( pid )
  {
    waitpid(pid, &stat_loc, 0);
  }
  else
  {
    for ( i = 0; i <= strlen(flag); ++i )
    {
      if ( flag[i] == 'i' || flag[i] == 114 )
        flag[i] = 49;
    }
  }
  printf("input the flag:");
  __isoc99_scanf("%20s", s2);
  if ( !strcmp(flag, s2) )
    return puts("this is the right flag!");
  else
    return puts("wrong flag!");
}
```

这里可以点击ascii按r转换成字符，

遍历flag，把i和r转换成1（这里我已经转换过i了，但其他我还没转换）

```
if ( flag[i] == 'i' || flag[i] == 114 )
        flag[i] = 49;
```

那么我们只要让我们输入的s2和flag一摸一样就可以得到真正的flag了

```
!strcmp(flag, s2)
```

那么接下来的任务就是找flag

![image-20260129110658734](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129110658734.png)

那么接下来你就知道该干啥了