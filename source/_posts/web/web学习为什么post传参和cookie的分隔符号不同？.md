---
title: 'web学习为什么post传参和cookie的分隔符号不同？'
categories:
  - 
tags: []
abbrlink: 9dfa48a8
date: 2026-03-08 14:57:17
---
# web学习为什么post传参和cookie的分隔符号不同？

在学传参的时候将常会遇到多传参的题目，但是cookie用的是`;`,post用的是`&`



它们诞生于不同的年代，服务于不同的标准，为了互不干扰，必须使用不同的“切割符”。

------

### 1. & 分隔符：来自“表单”的传统 (HTML 标准)

`&` 符号主要用于 **URL 查询参数**（GET）和 **POST 请求体**（`application/x-www-form-urlencoded`）。

- **起源**：它是由 HTML 标准定义的。当我们提交一个网页表单时，浏览器需要一种方式把 `key1=value1`、`key2=value2` 串起来。
- **为什么选 `&`**：在早期的 ASCII 码表中，`&` (Ampersand) 是一个常用的连接符，且在普通文本中出现的频率远低于逗号或分号，不容易引起歧义。
- **结构示例**： `user=admin&pass=123456&action=login`

------

### 2. ; 分隔符：来自“饼干”的规范 (HTTP Cookie 标准)

Cookie 的格式是由专门的 **RFC 规范**（如 RFC 6265）定义的，它和 HTML 表单参数完全是两套体系。

- **起源**：Cookie 诞生于 1994 年（由网景公司发明），比标准表单处理要晚一些。设计者希望 Cookie 的字符串能够和 URL 参数**产生明显的视觉和逻辑区分**。
- **为什么选 `;`**：
  - **避免冲突**：如果 Cookie 也用 `&` 分隔，那么当程序在处理一段既包含 URL 参数又包含 Cookie 的复杂字符串时，很容易发生“串味”。
  - **RFC 规范**：HTTP 协议的 Header 字段（如 `Accept`, `Cache-Control`）通常都倾向于使用分号 `;` 或逗号 `,` 来分隔属性。Cookie 既然是 Header 的一部分，自然遵循了 Header 的家族传统。
- **结构示例**： `Cookie: action=scan; sign=6d00fef7; sessionid=abc`



## 记忆方式：

| **位置**                    | **格式名称** | **分隔符** | **举例**               |
| --------------------------- | ------------ | ---------- | ---------------------- |
| **第一层：URL 路径**        | Query String | `&`        | `?id=1&type=web`       |
| **第二层：请求头 (Header)** | Cookie       | `;`        | `Cookie: a=1; b=2`     |
| **第三层：请求体 (Body)**   | Form Data    | `&`        | `user=admin&token=xyz` |