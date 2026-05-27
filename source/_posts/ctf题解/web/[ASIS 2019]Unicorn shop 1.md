---
title: '[ASIS 2019]Unicorn shop 1'
abbrlink: a64d52a6
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# [ASIS 2019]Unicorn shop 1

2019年的题目了，7年前，时间太恐怖了

题目如图：一个purchase的提交表单

![image-20260427201052399](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427201052532.png)

## 0x01 思路

### 1.先随便输入购买，进行抓包

![image-20260427201037550](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427201037630.png)

没懂，回复是：错误的商品

### 2.继续试一下html实体编码后的字符： `&#49`，这个表示1，发现有报错信息

![image-20260427200231873](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427200231971.png)

看一下报错是：只能接受一个unicode字符作为参数

```
unicodedata.numeric(price)
TypeError: need a single Unicode character as parameter
```

那这样我们只能买id为1价格为1的独角兽了，但是我们第一此买的就是这个，回复显示了：错误的商品

### 3.试试看unicode，毕竟题目提示“Unicode”，而且你猜unicorn读起来是不是很Unicode很像呢？

已知我们肯定需要更多钱去被一个unicode字符表示

'price=億'数值就是一个亿了

但是又到回复了错误商品`wrong commodity`

想到购买的商品原来是错的，试试ultra的独角兽

![image-20260427200158170](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427200158246.png)

### 4.payload：

```
id=4&price=億
```

![image-20260427200033770](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427200040956.png)



### 能绕过的原因：

让我们传入' a single Unicode character'，但是由于“億”在unicode编码里面也标记的他的数值属性

我们可以用一个unicode字符去表示一个具体数值比较大的数字

详见：https://www.unicodecharacter.org/U+5104

![image-20260427203200694](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427203200783.png)



---

## 0x02 知识点

现在我们来好好认识一下unicode吧

### 1.什么是unicode编码

Unicode 给全世界每一种语言的每一个字符（包括汉字、字母、emoji、甚至古埃及象形文字）都分配了一个唯一的数字，这个数字叫做**码点（Code Point）**。

通常写作 `U+` 后面加十六进制数字

![image-20260427202123640](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427202123699.png)



### 2.在线Unicode字符集网站[https://symbl.cc/cn/unicode-table/]

![image-20260427202441507](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260427202441658.png)