---
title: '[NPUCTF2020]EzShiro 48'
categories:
  - 
tags: []
abbrlink: d87674c8
date: 2026-02-01 23:28:09
---
## [NPUCTF2020]EzShiro

### 48

![image-20260131211323795](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260131211323795.png)





这道题目我做了三天，虽然不是持续做，但是仍任磨练意志力；

我于2026.2.1 23:25决定只学原理不找flag了

------

## 1. 原始形态：反序列化“炸弹”长啥样？

在你执行 `ysoserial` 生成 `payload.ser` 时，它本质上是一个 **Java 序列化对象流**。如果你用十六进制查看器（Hex Editor）打开它，你会看到：

- **文件头**：总是以 `AC ED 00 05` 开头（这是 Java 序列化对象的魔法数字）。
- **内容**：里面并不是代码，而是**一串嵌套的对象**。
  - 最外层是一个 `HashSet`（在 CC6 链中）。
  - 里面包裹着 `TiedMapEntry`。
  - 最核心的是 `LazyMap` 和 `ChainedTransformer`。
- **逻辑**：它像一串精心排布的**多米诺骨牌**。当这个对象被“反序列化”（即从字节还原成对象）时，Java 会自动调用它的 `readObject()` 方法。第一块骨牌倒下，最终会触发 `Runtime.getRuntime().exec()` 执行你的命令。

------

## 2. Shiro 的“快递拆包”原理

当你把这串字节发送给服务器时，Shiro 并不是直接拿来用的。它有一套严格的过滤和解密流程：

### 流程图解：

1. **Base64 解码**：

   你在 Cookie 里发的是字符（A-Z, 0-9），Shiro 先把它还原成二进制字节流。

2. **AES 解密**（漏洞核心）：

   Shiro 拿到字节流后，会使用硬编码在代码里的 **Key**（也就是 `kPH+bIxk5D2deZiIxcaaaA==`）进行 AES 解密。

   > **核心漏洞点**：Shiro 1.2.4 及以前的版本，这个 Key 是默认的。攻击者只要知道了 Key，就能构造出让服务器认可的密文。

3. **Java 反序列化**：

   解密后的数据如果以 `AC ED 00 05` 开头，Shiro 就会调用 `ObjectInputStream.readObject()`。

   **此时，“多米诺骨牌”被推倒，你的命令在服务器上运行。**

------

## 3. 为什么会有 Jackson 的干扰？

这道题叫 `EzShiro`，但你发现路径里有 `/json` 且返回 `jackson interface`。这是因为这道题组合了两个漏洞：

1. **Shiro 权限绕过 (`/;`)**：

   原本 `/json` 可能是后台接口，普通人进不去。利用 Shiro 的解析漏洞，通过 `/;/json` 骗过拦截器进入后台。

2. **Jackson 触发点**：

   后端代码可能长这样：

   Java

   ```
   @PostMapping("/json")
   public String readJson(@RequestBody Object obj) { 
       // 只要这行代码执行，Jackson 就会解析你发的 JSON
       return "jackson interface"; 
   }
   ```

   当你发送一个含有 `rememberMe` 的请求到这个接口时，虽然你发的是 JSON 数据（`true=1`），但 **Shiro 的拦截器级别更高**。

   - **Shiro 先动**：它先去检查 Header 里的 Cookie。只要它发现了 `rememberMe`，它就先解密、先反序列化。
   - **Jackson 后动**：如果 Shiro 反序列化没把程序搞崩溃，Jackson 才会去解析 Body 里的 JSON。

------

## 4. 总结：我们构造的究竟是什么？

- **ysoserial** 负责制造“炸弹”（CC6 序列化对象）。

### 为什么失败了？

- **如果是 404**：说明“炸弹”炸了（执行了），但你放旗子的位置不对（Web 路径猜错了）。

