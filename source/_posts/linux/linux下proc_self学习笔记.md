---
title: 'linux下proc_self学习笔记'
categories:
  - 
tags: []
abbrlink: 713c99f6
date: 2026-01-27 11:17:50
---
# **Linux `/proc` 文件系统**（`/proc/self`）的学习笔记



出处：https://blog.csdn.net/cjdgg/article/details/119860355

前提知识点：**文件句柄**（File Descriptor，简称 fd）是 Linux 内核为每个进程分配的**唯一标识符**（非负整数），用于跟踪该进程打开的**文件、管道、网络套接字、设备**等资源。

- 所有 I/O 操作（读写文件、网络通信等）都通过文件句柄进行。例如：
  - `0` 标准输入（stdin）
  - `1` 标准输出（stdout）
  - `2` 标准错误（stderr）
  - 其他句柄：普通文件（如 `3`）、网络套接字等。





内容精简如下：

### 1. `/proc/self` 是什么？

**`/proc` 目录**：Linux 的伪文件系统，存储内核和进程信息（只存在内存中）。

**`/proc/[pid]`**：存储特定进程（如 PID 1083）信息的目录。

**`/proc/self`**：一个快捷方式。谁访问它，它就指向**访问者自己**的进程目录。

**作用**：攻击者在不知道当前进程 PID 的情况下，可以直接用 `/proc/self` 获取当前进程的信息。

### 2. 常用子目录/文件

攻击者常利用以下文件获取敏感信息：

**`cmdline`**：启动当前进程的完整命令。

**`cwd`**：当前进程的运行目录。

**`environ`**：当前进程的环境变量（可能包含密钥、密码）。

**`fd` (File Descriptors)**：文件描述符目录，包含进程当前打开的所有文件。

**利用点**：如果程序打开了一个文件（如 `flag`）但删除了它，只要进程没关闭该文件句柄，依然可以通过 `/proc/self/fd/[数字]` 读取到文件内容。

### 3. CTF 题目实战 ([pasecactf_2019]flask_ssti)

**题目逻辑：Python Flask 应用读取 `flag`，加密后存入配置，然后**删除了 `flag` 文件**。

**解法**思路：

1. 虽然文件被删，但 Python 进程可能还持有该文件的句柄（File Descriptor）。
2. 利用 SSTI（模板注入）漏洞执行命令。
3. 直接 `cat /proc/self/fd/3` 失败，因为 `popen` 启动的 `cat` 是个新进程，它的 `self` 是 `cat` 自己，不是 Flask 进程。
4. **正确解法**：
   - 找到 Flask 进程的 PID（通常是 1）。
   - 构造 Payload 读取 `/proc/1/fd/3`（或者遍历 fd 目录寻找 flag）。
   - Payload 示例：`{% raw %}{{ ... popen("cat /proc/1/fd/3").read() ... }}{% endraw %}`。

**总结**： `/proc/self` 和 `/proc/[pid]/fd/` 在 Linux 环境下找回被删除但未释放的文件内容，或者在不知道 PID 时获取当前进程环境信息。

