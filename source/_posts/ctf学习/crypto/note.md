---
title: "note"
date: 2026-01-21 19:39:43
categories:
  - ctf学习
  - crypto
  - rsa
tags: [碰到的一些密码]
---





## 密码笔记

HEX、DEC、OCT 和 BIN含义如下：

- HEX，英文全称 **Hexadecimal**，表示**十六进制**。
- DEC，英文全称 **Decimal**，表示**十进制**。
- OCT，英文全称 **Octal**，表示**八进制**。
- BIN，英文全称 **Binary**，表示**二进制**。



## 1.Quoted-printabl     可打印字符 引用 编码

Quoted-printable编码是一种**二进制数据在Internet上传输时的一种编码方式**。 它将二进制数据转换成可打印的ASCII字符。 这种编码方式将每个非可打印字符 (ASCII值小于32或大于126)，如二进制数据的控制字符或扩展字符 (如汉字)，转换为一个等号"=“加上它的ASCII值的16进制表示，如”x0A"会变成"=0A"。



## 2.栅栏密码

[1](https://blog.csdn.net/Makboli/article/details/126464442)[2](https://baike.baidu.com/item/栅栏密码/228209)[3](https://blog.csdn.net/qq_52828510/article/details/122563626)

栅栏密码是一种简单的替换式密码



加密过程

以明文 "THIS IS ZHISHITOM" 为例，去除空格后得到 "THISISZHISHITOM"。如果设置栏数为3进行加密，加密过程如下：

- 第一组：T H I S I
- 第二组：S Z H I S
- 第三组：H I T O M

按列取出字母得到：TSH HZI IHT SIO ISM，然后将这些字母连在一起，形成加密后的密文 "TSHHZIIHTSIOISM"。

解密过程

解密是加密过程的逆过程。对于上述加密后的密文 "TSHHZIIHTSIOISM"，首先将其分割成与加密时相同数量的组：

- T S H
- H Z I
- I H T
- S I O
- I S M

然后按列顺序取字母，得到解密后的明文 "THISISZHISHITOM"。



## 3.Rabbit加解密算法：

Rabbit 是一种**流密码算法**（像 “无限长的密码本”，逐位生成密钥流和明文混合），用大白话讲就是：

1. **准备 “密码本”**：用一个密钥（比如 16 字节的字符串）初始化算法，生成一个 “动态变化的序列”（密钥流）；
2. **加密**：把明文的每个字节，和密钥流的对应字节做 “异或” 运算（简单的二进制位运算），得到密文；
3. **解密**：用同样的密钥生成一模一样的密钥流，再把密文和密钥流做异或，就能还原出明文。

核心特点：**速度快、密钥短（通常 128 位）**，CTF 里偶尔会遇到，但不如 AES、DES 常见。



