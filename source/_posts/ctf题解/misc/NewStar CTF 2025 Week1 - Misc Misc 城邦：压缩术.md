---
title: 'NewStar CTF 2025 Week1 - Misc Misc 城邦：压缩术'
categories:
  - 
tags: []
abbrlink: b2ca8b76
date: 2026-03-16 21:55:16
---

# 明文攻击详解NewStar CTF 2025 Week1 - Misc 城邦：压缩术



### 前期准备：

010打开发现里面有很多压缩包和文件，用foremost分离

```
zsh: corrupt history file /home/kali/.zsh_history
┌──(kali㉿kali)-[~/Desktop]
└─$ binwalk compression-magic.zip

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, encrypted at least v2.0 to extract, compressed size: 417, uncompressed size: 516, name: bkcrack.zip
458           0x1CA           Zip archive data, encrypted at least v2.0 to extract, compressed size: 154, uncompressed size: 162, name: tips.txt
833           0x341           End of Zip archive, footer length: 22

                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ foremost compression-magic.zip
Processing: compression-magic.zip
|foundat=bkcrack.zip5
�9ج*▒�&�Z�      �    ߤA��$�'e���[�����X���̴��Z�M2t`���G��        G��*���
�!�!�y�^���▒x��
;       �,���W�h�Mɸ�
                    {u�▒�;�9�뭊"▒���ȗ�\Ap��׳ؐq���ٍ,S�O�PA�G�$�▒�t$Kx�����j�
                                                                         �/W▒��&^�Q�2*oe�u�y?`�_!▒�#�9;Q)
                                                                                                         �ukYk����U▒���tDsl����Y��i�c���g��
foundat=tips.txt��^��▒�`
                        ��~=�[/{�����
                                     �����G��i"8�>;��s�����E2��'���* ���;4"Q�%�ʍ'�X�����V�Y<��Y��3ԫ�H9▒�2�o%b��J(=S�؍T&TWK�PKZt��Pw2�+>��s}
*|
                                                                                                                 
┌──(kali㉿kali)-[~/Desktop]
└─$ 

```



分离之后暴力破解zip

提示六位密码，还有咒语abcd...xyz0123...789，说明是小写字母加数字



![image-20260313215713105](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260313215720256.png)



得到

“恭喜你，通过了第一道考验，请用其他压缩魔法打开下一扇门吧！（下一扇门明明没有密码，为什么还是要输入密码呢？）”

->

说明是伪加密

可以看一下另一篇伪加密的题解https://2829750658t-svg.github.io/posts/1cf77fba.html

改一下全局方式位标记

![image-20260313220412915](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260313220413029.png)



另存为一个文件，打开发现里面还有zip压缩包

![image-20260314124655212](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260314124655292.png)

这里是需要明文爆破：

说明：因为这里zip外的key.txt和zip内的key.txt明显根据信息可以猜测是同一个文件

---



## 知识点：

##### 1. 加密算法本质：流加密（Stream Cipher）

ZIP 的传统加密（ZipCrypto）本质是一个**伪随机数生成器**。

它有三个key，每个是32位：$Key_0, Key_1, Key_2$。

**加密公式：** $C_i = P_i \oplus K_i$

- $P_i$：明文的第 $i$ 个字节。
- $K_i$：由 $Key_2$ 经过特定位运算生成的密钥（8位）。
- $C_i$：你看到的密文。

##### 2. key的运算

每处理一个字节，三个 Key 会按照以下逻辑迭代：

1. $Key_0 = \text{crc32}(Key_0, P_i)$
2. $Key_1 = (Key_1 + (Key_0 \text{ \& } 0xFF)) \times 134775813 + 1$
3. $Key_2 = \text{crc32}(Key_2, Key_1 >> 24)$

总之就是计算啦，不用深究

##### 3. 为什么已知明文可以推导出原始加密文件里面的内容？

明文攻击目的：**还原这三个key**，而不是还原密码字符串。

因为 $C_i = P_i \oplus K_i$，

### **已知：** 密文 **C**part（zip中的flag.txt） + 明文 **P**part(flag.zip)→ **求出** 三个核心 Key。

(前提：当有12字节以上的明文->因为3×32 位=96 位。字节：96÷8=12 字节。)

### **推导：** 三个核心 Key→ **演变出** 所有的密钥字节 **K**all。

### **解密：** 密文 **C**all⊕**K**all→ **还原出** 所有的明文 **P**all。



---



那么我们只需要把外面的明文key.txt无密码加密（加密方式要和原文件一样），然后用工具爆破就行



![image-20260314124834322](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260314124834463.png)

怎么确保加密方式要和原文件一样呢？

可以010打开文件头部，观察是哪种加密



<img src="https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260314122949083.png" alt="image-20260314122941940" style="zoom: 50%;" />

## 方法一：archpr工具



加密文件打开，软件中点击明文选项，找到明文，直接点击开始选项开始攻击

![image-20260314123736895](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260314123737018.png)



ARCHPR 的真实逻辑顺序是： **明文/密文对比** → **算出 3 个 32 位内部 Key** → **得到全部文件**。 

##### 为什么它给出了最后的“密码”

在得到那 3 个 32 位内部 Key 后，ARCHPR 会尝试进行**最后一次计算**：

初始的 3 个 Key 是由你的原始密码经过公式算出来的。

如果你的密码**短**，ARCHPR 反向去“猜”是哪个字符串生成了这组 Key。

如果它成功猜到了就会把这个密码给你。







## 方法二：题目的提示的bkcrack

当遇上大文件时建议用此方法，方法一耗时太久

------

### 解题思路：

##### 1. 准备明文

把外面那个 `key.txt` 压成 `zip`。

> 压缩方式必须一样。如果原包是“标准”压缩，你也得用“标准”；如果原包是“存储”（不压缩），你也得选“存储”。

##### 2. 破解

输入：

```
bkcrack -C secret.zip -c key.txt -P manual.zip -p key.txt
```

- `-C` (Big C): 那个**加密**的包。
- `-c` (small c): 加密包里那个**已知文件**的名字。
- `-P` (Big P): 你刚才**手动压**的那个明文包。
- `-p` (small p): 明文包里那个**文件**的名字。

##### 3. 获取三key

```
Data: 1a2b3c4d 5e6f7g8h 9i0j1k2l
```

##### 4. 直接提取

```
bkcrack -C secret.zip -k 1a2b3c4d 5e6f7g8h 9i0j1k2l -U result.zip
```

`result.zip` 就是一个完全没有密码、可以直接打开的包了。

