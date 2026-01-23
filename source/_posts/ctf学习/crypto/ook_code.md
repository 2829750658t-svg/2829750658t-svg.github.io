---
title: "ook_code"
date: 2026-01-21 19:39:43
categories:
  - ctf学习
  - crypto
  - ook编码
tags: [碰到的一些编码]
---





## Ook编码详解

## [Ook编码详解](https://ctf.bugku.com/tool/brainfuck)

[1](https://ctf.bugku.com/tool/brainfuck)

[2](https://blog.csdn.net/m0_47311097/article/details/144930147)

[3](https://www.cnblogs.com/harmor/p/17279609.html)

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
