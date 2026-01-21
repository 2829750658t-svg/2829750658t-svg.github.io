---
title: "misc"
date: 2026-01-21 19:39:43
categories: 默认分类
tags: [笔记]
---





# ZIP 明文爆破笔记（CTF 实战版）

## 一、核心原理

### 1. 加密逻辑（ZipCrypto 算法）

- 加密：明文 XOR 密码流 = 密文
- 解密：密文 XOR 密码流 = 明文
- 反推密码流：明文 XOR 密文 = 密码流

### 2. XOR（异或）规则

二进制运算：相同为 0，不同为 1

例：`a`（01100001）XOR 5（00000101）= `d`（01100100）；`d` XOR 5 又变回 `a`

### 3. 明文爆破本质

已知明文 + 对应密文→算密码流→反推 ZIP 的 3 个核心密钥（key0/key1/key2）→用密钥解密整个 ZIP

**前提**：仅对 ZIP 传统加密有效，AES256 加密无效！

## 二、bkcrack 使用条件

1. ZIP 内文件**未压缩**（检查：`bkcrack -L 压缩包.zip`）

2. ##### 已知至少**12 字节明文**（8 字节连续）+ 明文在文件中的位置（偏移）



## 三、题目

**bkcrack 无法直接破解 ZIP 密码，必须靠 “已知明文”和“你已有密文” 反推加密密钥，再用密钥解密**



不管是字符明文还是文件头明文，核心是：

**准备明文文件 → 得密钥 → 用密钥解密**

区别只在 “明文来源”—— 字符明文来自题目暗示，文件头明文来自格式固定规则。

### 题目 1：字符明文爆破（已知部分字符内容）

#### 场景

题目给了加密 ZIP 包`flag_360.zip`，里面有`flag.txt`，且已知`flag.txt`里包含 “lag {16e374f6...” 这样的字符片段。

#### 步骤 1：准备已知明文



```bash
# 把8个连续明文“lag{16e3”存成文件（bkcrack需要文件形式的明文）
echo -n "lag{16e3" > plain1.txt  
# 把额外明文“74f6”转成十六进制（备用，后续填到命令里）
echo -n "74f6" | xxd  
```

执行后得到 “74f6” 对应的十六进制`37346636`，记下来。

#### 步骤 2：解密钥

偏移量=你的明文第一个字符的位置

```bash
bkcrack -C flag_360.zip  # 指定要破解的ZIP包
        -c flag.txt      # 指定ZIP里要攻击的文件
        -p plain1.txt    # 用刚才存的8个连续（plaintext）明文文件
        -o 1             # 明文“lag{16e3”在flag.txt里的起始位置是   ？偏移1
        -x 29 37346636   # 额外明文：偏移29的位置是“74f6”（对应十六进制）  ？
```

运行后得到 3 个密钥，比如`b21e5df4 ab9a9430 8c336475`。

#### 步骤 3：解密文件



```bash
bkcrack -C flag_360.zip  # 原加密ZIP包
        -c flag.txt      # 要解密的文件
        -k b21e5df4 ab9a9430 8c336475  # 爆破出的密钥
        -d flag.txt      # 解密后保存的文件名
```

打开解密后的`flag.txt`就能拿到 flag。

### 题目 2：文件头固定明文爆破（PNG 文件）

#### 场景

题目给了加密 ZIP 包`png4.zip`，里面有`2.png`，无其他明文信息，但知道 PNG 文件头是固定的。

#### 步骤 1：准备 PNG 固定文件头明文



```bash
# PNG文件头的固定十六进制转成二进制文件（bkcrack需要二进制明文）
echo 89504E470D0A1A0A0000000D49484452 | xxd -r -ps > png_header  //（把字符ASCII二进制转成十六进制对应二进制）
```

（

这个`png_header`文件里存的就是 PNG 文件开头的二进制数据。

#### 步骤 2：爆破密钥



```bash
bkcrack -C png4.zip   # 指定加密ZIP包
        -c 2.png      # 指定ZIP里的PNG文件
        -p png_header # 用PNG固定文件头作为明文
        -o 0          # PNG文件头从偏移0开始（文件最开头）
```

运行后得到密钥，比如`c9ce002a 9749123a 1d9079b9`。

#### 步骤 3：解密 PNG 文件



```bash
bkcrack -C png4.zip  # 原加密ZIP包
        -c 2.png     # 要解密的PNG文件
        -k c9ce002a 9749123a 1d9079b9  # 爆破出的密钥
        -d 2_dec.png # 解密后保存的PNG文件名
```

打开`2_dec.png`，里面可能藏着 flag（比如图片里的文字、隐写内容）。

### 题目 3：JPG 文件头固定明文爆破（举一反三）

#### 场景

题目给了加密 ZIP 包`jpg5.zip`，里面有`3.jpg`，无其他明文信息。

#### 步骤 1：准备 JPG 固定文件头明文

（把字符ASCII二进制转成十六进制对应二进制）

```bash
# JPG文件头固定十六进制：FFD8FFE000104A4649460001
echo FFD8FFE000104A4649460001 | xxd -r -ps > jpg_header
```

#### 步骤 2：爆破密钥



```bash
bkcrack -C jpg5.zip   # 加密ZIP包
        -c 3.jpg      # ZIP里的JPG文件
        -p jpg_header # JPG固定文件头明文
        -o 0          # 文件头从偏移0开始
```

#### 步骤 3：解密文件



```bash
bkcrack -C jpg5.zip -c 3.jpg -k [爆破出的密钥] -d 3_dec.jpg
```

打开解密后的 JPG 文件获取 flag。





## bf6题解：

1.压缩包，放kali，有png，用bk

2.准备png开头 明文文件

echo 开头码 | xxd -r ps > 明文文件

3.得到密钥

bkcrack -C -c -p -o

4.解密压缩文件

bkcrack -C -c -k -d

5.发现图片有隐藏的10编码，steg打开得到乱码，图片comment里面有密钥，解码后flag







## 二维码

### 1



一个完整的 JPG 文件由 FF D8 开头，FF D9结尾
 在使用图片浏览器时，图片浏览器会忽略 FF D9 以后的内容，因此可以在 JPG 文件中加入其他文件。其他文件隐藏如png.gif文件隐藏也是这个道理。



```bash
# ========== 前期定位工具 & 切换工作目录 ==========
# 1. （尝试找bkcrack目录失败，改用全局查找工具路径）
which bkcrack  # 确认bkcrack路径：/usr/local/bin/bkcrack

# 2. 切换到桌面（二维码图片所在目录，核心工作目录）
cd ~/Desktop

# ========== 1. 从二维码中分离加密ZIP包 ==========
# 3. 用binwalk提取二维码中隐藏的ZIP数据
binwalk -e QR_code.png  # 分离出加密ZIP包（偏移0x1D7，对应文件1D7.zip）

# 4. 进入分离后的目录，查看并复制ZIP包到桌面
cd _QR_code.png.extracted  # 进入binwalk生成的提取目录
ls                         # 查看分离出的文件：1D7.zip
cp 1D7.zip ~/Desktop/      # 复制ZIP包到桌面（方便后续操作）
cd ~/Desktop               # 切回桌面



# 5.爆破密码，打开就ok





原来思路：
# ========== 2. 准备明文文件（bkcrack明文攻击用） ==========
# 5. 创建与ZIP内同名的空白文件（4number.txt）
touch 4number.txt

# ========== 3. 尝试bkcrack明文攻击（因ZIP包不完整报错，后改用爆破） ==========
# 6. 执行bkcrack明文攻击（报错：ZIP缺少目录尾签名）
bkcrack -C 1D7.zip -c 4number.txt -P ./ -p 4number.txt

# ========== 补充：你后续爆破1D7.zip的核心逻辑（可选命令） ==========
# （若用fcrackzip爆破4位数字密码，示例命令）
fcrackzip -b -l 4-4 -u 1D7.zip  # -b=爆破模式，-l 4-4=4位数字，-u=只显示正确密码
# 爆破成功后解压（假设密码为1234）
unzip -P 1234 1D7.zip  # -P指定密码，解压后查看4number.txt拿到flag
```

cs
