---
title: 'reverse3 1'
categories:
  - 
tags: []
abbrlink: a2644cd8
date: 2026-03-16 21:55:04
---

# reverse3

# 1





```
  for ( i = 0; i < 100; ++i )
  {
    if ( (unsigned int)i >= 0x64 )
      j____report_rangecheckfailure();
    Destination[i] = 0;
  }
  sub_41132F("please enter the flag:", v7);
  sub_411375("%20s", (char)Str);
  v3 = j_strlen(Str);
  v4 = (const char *)sub_4110BE(Str, v3, v14);
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





e3nifIH9b_C@n@dH



Base64 的核心特性是：**将 3 个字节的原始数据编码为 4 个字符**





```
  if ( !a1 || !a2 )
    return 0;
  v9 = a2 / 3;
  if ( (int)(a2 / 3) % 3 )
    ++v9;
  v10 = 4 * v9;
  *a3 = v10;
  v12 = malloc(v10 + 1);
```



![image-20260310214139302](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260310214139464.png)





```
b'{i_l0ve_you}'
```

