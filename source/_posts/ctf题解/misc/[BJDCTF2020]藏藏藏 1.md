---
title: '[BJDCTF2020]藏藏藏 1'
categories:
  - 
tags: []
abbrlink: f0e972f6
date: 2026-02-06 15:27:53
---
# [BJDCTF2020]藏藏藏 1



1.0110发现有pk压缩包，还有个docx

![image-20251218214521489](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251218214521489.png)





2.kali打开

2.1解析

```
binwalk 图片.jpg  //解析得到存在zip
```

2.2分离

```
foremost 图片.jpg //分离得到图片中的压缩包，默认在output目录里面
```

2.3解压

```
unzip ./output/zip/文件名.zip   //得到 ：福利.docx
```

2.4查看

```
cat 福利.docx  //又发现pk文件头
```

2.5binwalk检测，发现很多压缩包

2.6foremost分离，此时加后缀-t，放在另一个output中

2.7tree ./新output

```
──(kali㉿kali)-[~/Desktop]
└─$ tree ./output_Thu_Dec_18_08_56_09_2025/zip 
./output_Thu_Dec_18_08_56_09_2025/zip
└── 00000000.zip

```

2.8 解压unzip ./output_Thu_Dec_18_08_56_09_2025/zip/00000000.zip

2.9 得到一张图片，打开是二维码，扫一就ok





![image-20251218220400272](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20251218220400272.png)





