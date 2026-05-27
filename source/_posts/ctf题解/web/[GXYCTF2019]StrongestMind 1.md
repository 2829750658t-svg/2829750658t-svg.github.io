---
title: '[GXYCTF2019]StrongestMind 1'
categories:
  - 
tags: []
abbrlink: 8670a4ce
date: 2026-03-05 20:42:31
---
# [GXYCTF2019]StrongestMind

# 1



代码来计算

```
import requests
import re
import time

url = "http://e67cb175-bc55-4f9e-b0a8-14c64e03faee.node5.buuoj.cn:81"
session = requests.session()
req = session.get(url).text
flag = ""

for i in range(1010):
    try:
        result = re.findall("<br\>\<br\>(\d.*?)\<br\>\<br\>", req)  # 获取[数字]
        result = "".join(result)  # 提取字符串
        result = eval(result)  # 运算
        print("time: " + str(i) + "   " + "result: " + str(result))

        data = {"answer": result}
        req = session.post(url, data=data).text
        if "flag{" in req:
            print(re.search("flag{.*}", req).group(0)[:50])
            break
        time.sleep(0.1)  # 防止访问太快断开连接
    except:
        print("[-]")
```

