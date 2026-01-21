---
title: "codetijie"
date: 2026-01-21 19:56:05
categories: 默认分类
tags: [笔记]
---

## 大帝的密码武器

### 1

题解

FRPHEVGL偏移13位security

密文：ComeChina，通过偏移13

得到flag，注意大小写



## 看我回旋踢

### 1

1. 遇到synt{xx-xx-xx} 判定他为rot13；
2. 题目一般都是提示信息，“回旋踢”就暗示了rot13的特点，会重新绕回；

flag{5cd1004d-86a5-46d8-b720-beb5ba0417e1}





## moectf misc Cor1e的支票

解码网站：https://www.dcode.fr/ook-language

## [Ook编码详解](https://ctf.bugku.com/tool/brainfuck)

[1](https://ctf.bugku.com/tool/brainfuck)[2](https://blog.csdn.net/m0_47311097/article/details/144930147)[3](https://www.cnblogs.com/harmor/p/17279609.html)

**Ook!** 是一种基于极简主义设计的编程语言，属于 esolang（怪异语言）的一种。它是从 **Brainfuck** 演变而来的，主要用于编码和解码任务。Ook! 的指令由简单的短语组成，例如 *Ook. Ook?* 或 *Ook! Ook!*，这些短语对应 Brainfuck 的操作符。

编码规则

Ook! 使用一组固定的短语来表示操作符，每个短语由两个单词组成。以下是 Ook! 和 Brainfuck 的对应关系：

- *Ook. Ook.* 对应 *>*（指针右移）
- *Ook! Ook!* 对应 *<*（指针左移）
- *Ook. Ook!* 对应 *+*（当前单元格值加一）
- *Ook! Ook.* 对应 *-*（当前单元格值减一）
- *Ook! Ook?* 对应 *[*（循环开始）
- *Ook? Ook!* 对应 *]*（循环结束）
- *Ook. Ook?* 对应 *.*（输出当前单元格值）
- *Ook? Ook.* 对应 *,*（输入值到当前单元格）



```
。。。。。。。。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。。。。。。。。。？。？！。？。。。。。。。。。。。。。。。。。。！。。。。。！。？。。。。。。。！？！！。？！！！！！！？。？！。？！！！。！！！！！。？。。。。。。。。。！？！！。？。。。。。。。。？。？！。？。。！。？。。。。。。。！？！！。？！！！！！！？。？！。？！！！！！！！！！！！。？。。。。。。。。。！？！！。？。。。。。。。。？。？！。？。。。。。。。。。。！。？。。。。。。。。。！？！！。？！！！！！！！！？。？！。？！！！！！！！！！！！！！！！！！。？。。。。。。。！？！！。？。。。。。。？。？！。？。。。。。。！。。。。。。。！。？。。。。。。。。。。。。。。。。。！？！！。？！！！！！！！！！！！！！！！！？。？！。？！！！。？。。。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。。。？。？！。？。。。。。。！。！！！！！！！！！！！！！。？。。。。。。。。。。。！？！！。？！！！！！！！！！！？。？！。？！！！！！！！！！！！。？。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。？。？！。？。。。。。。。。。。。。。。。。。。！。？。。。。。。。。。。。。。！？！！。？！！！！！！！！！！！！？。？！。？！！！！！！！！！！！！！。？。。。。。。。。。。。！？！！。？。。。。。。。。。。？。？！。？。。。。！。。。。。。。。。。。。。！。？。。。。。。。。。。。。。。。！？！！。？！！！！！！！！！！！！！！？。？！。？！！！。？。。。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。。。？。？！。？。。。。。。。。。。。。。。。。。。。。。。。。。。！。！！！！！！！！！！！！！！！！！。！！！！！！！！！。！！！！！！！！！！！！！。？。。。。。。。。。。。。。！？！！。？！！！！！！！！！！！！？。？！。？！！！！！！！！！！！！！！！！！！！！！。？。。。。。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。。。。。？。？！。？。。。。！。？。。。。。。。。。！？！！。？！！！！！！！！？。？！。？！！！！！！！！！。？。。。。。。。。。。。！？！！。？！！！！！！！！！！？。？！。？！！！！！！！。？。。。。。。。！？！！。？。。。。。。？。？！。？。。。。。。。。！。？。。。。。。。。。。。。。！？！！。？。。。。。。。。。。。。？。？！。？。。。。。。。。。。。。。。。。。。！。？。
```

替换为ook

```
。->Ook.
！->Ook!
？->Ook?
```







## moectf misc Macross

世界名画，笑死我了，看了个题解，他人好有趣



```
崉 崉            €   8  €   8    €?N  d   L           2         '  ?                             $ E N D         2   '  ?   !  ?                             $ E N D            !  ?     ?                             $ E N D              ?     ?                             $ E N D              ?     ?                             $ E N D              ?     ?                             $ E N D              ?   
  ?                             $ E N D            
  ?     ?                             $ E N D              ?     ?                             $ E N D              ?     ?                             $ E N D         	     ?     ?                             $ E N D               ?                                   $ E N D                                                 $ E N D                  ?   
                            $ E N D            ?   
  ?                               $ E N D            ?     ?                               $ E N D            ?     ?                               $ E N D            ?     ?   %                            $ E N D            ?   %  ?   +                   
```



![image-20251225194916353](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251225194916353.png)





**分析这段文本的可能含义：**

- **设备控制码/状态信息：** 这些字符很可能是某种显示屏（如LCD驱动芯片 RA8806 的指令）或通信协议的原始数据。
- **乱码（Glyph Corruption）：** 字符 `宕 `, `鈧 `, `铮 `等显示异常，说明原始字节流被错误地解释或传输了。
- **数据序列：** `2`, `8`, `D`, `J`, `M`, `G`, `A`, `;`, `5`, `/`, `)` 可能是某种命令参数或数据值，遵循特定格式。
- **结构化标记：** `$END` 明确表示一个数据块的结束，这在网络通信、文件传输或设备驱动中很常见。 





说是鼠标移动的信息，下载个记录鼠标移动的软件，用画图打开运行文件就能看到名画









## moectf misc White Album



在线条形码

https://online-barcode-reader.inliteresearch.com/



![image-20251225200017128](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251225200017128.png)









## moectf misc Augustine's Way#2

奥古斯丁？？？打错了吧？？？奥古斯都







这要从罗马的第一位“皇帝”[奥古斯都](https://zhida.zhihu.com/search?content_id=1924561&content_type=Answer&match_order=1&q=奥古斯都&zhida_source=entity)

说起。奥古斯都本名叫屋大维（Gaius Octavius）。前44年，凯撒被刺，留下遗嘱把屋大维定为自己的继承人，因此屋大维的名字被改为Gaius Julius **Caesar** Octavianus，虽然在中文里仍译作屋大维，但实际上同时代的人已经只使用“凯撒”来称呼他了。

至于为什么“凯撒”这个名字被后来的皇帝延续使用下去，并不是因为它在罗马改制之前就变成了一个荣誉性质的称号。原因其实很简单：后来的几位皇帝，直到[尼禄](https://zhida.zhihu.com/search?content_id=1924561&content_type=Answer&match_order=1&q=尼禄&zhida_source=entity)

为止，全是屋大维的亲戚。不管是血亲也好，养子也好，因为和屋大维的亲属关系，他们的姓氏有的本来就是凯撒。有的本来姓氏不是凯撒的，作为合法继承人他们通常被前任皇帝所领养，因此依据古罗马的领养惯例，其姓氏也变成了凯撒。







## moectf misc Ex Viginere?





## Ex Viginere?

### 350

这难道是**维吉尼亚**吗？

```
text is a plain English text which only consists of lowercase letters (without any symbol)
```



维吉尼亚对照表

![img](https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Vigen%C3%A8re_square.svg/330px-Vigen%C3%A8re_square.svg.png)



例如，假设[明文](https://zh.wikipedia.org/wiki/明文)为：

```
ATTACKATDAWN
```

选择某一关键词并重复而得到密钥，如关键词为`LEMON`时，密钥为：

```
LEMONLEMONLE
```

对于明文的第一个字母`A`，对应密钥的第一个字母`L`，于是使用表格中`L`行字母表进行加密，得到[密文](https://zh.wikipedia.org/wiki/密文)第一个字母`L`。类似地，明文第二个字母为`T`，在表格中使用对应的`E`行进行加密，得到密文第二个字母`X`。以此类推，可以得到：

```
明文：ATTACKATDAWN
密钥：LEMONLEMONLE
密文：LXFOPVEFRNHR
```













## moectf misc Ez Vigenere

### 150

这题貌似是真的简单！ 但是你可能需要去知道什么是Vigenere~

同时，**key**我并没有告诉你哦

`dlcawx{kec_ihq_fc_tgjwebpc_lk_iuwwgk}` 







一个一个字母做密钥去试试，

moectf{the_key_of_vigenere_is_rxyyds}





![image-20251225205747380](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251225205747380.png)


