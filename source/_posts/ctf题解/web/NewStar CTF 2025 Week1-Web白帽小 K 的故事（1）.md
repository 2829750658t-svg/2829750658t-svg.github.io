---
title: 'NewStar CTF 2025 Week1-Web白帽小 K 的故事（1）'
categories:
  - 
tags: []
abbrlink: 14d10c76
date: 2026-03-16 21:53:28
---

# NewStar CTF 2025 Week1-Web白帽小 K 的故事（1）

对话提示看源代码（下面的图时候来上传完截屏的，有我们需要上传的test.mp3）

![image-20260312113359459](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260312113359898.png)

### 源代码

在/v1/onload页面

假设使用post传file=文件名

如果文件已经上传成功data.success为true，那么我们就能得到File content:

->猜测onload是执行接口

思路一：那如果我们直接上传木马catflag呢，我们是不是可以直接得到flag？

思路二：phpinfo(),flag也在里面





#### ${encodeURIComponent(file)}

如果不加这个函数，直接发送 `file=../../muma.php`：

1. **路径截断**：浏览器或服务器可能会把 `../` 识别为改变当前的 URL 路径，导致请求发到错地址。
2. **特殊字符冲突**：如果你的文件名包含 `&` 或 `=`，后端解析 POST 请求时会把它当成“下一个参数”的开始，导致文件名被切断，服务器找不到文件。

**加上它，就是为了把文件名变成符合 URL 规范的纯文本字符串，确保后端能接收到完整的路径字符串。**





```
        // 小岸同学到时候记得把这个函数删掉
        async function fetchload(file) {
            try {
                const res = await fetch('/v1/onload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: `file=${encodeURIComponent(file)}`
                });
                const data = await res.json();
                if (data.success) {
                    console.log('File content:', data.success);
                } else {
                    console.error('Error loading file:', data.error);
                }
            } catch (e) {
                console.error('Request failed', e);
            }
        }
```

上传木马

![image-20260312113325079](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260312113325164.png)



![image-20260312113009795](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260312113009908.png)