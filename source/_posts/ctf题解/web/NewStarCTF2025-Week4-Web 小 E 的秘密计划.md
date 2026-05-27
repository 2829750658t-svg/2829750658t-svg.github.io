---
title: 'NewStarCTF2025-Week4-Web 小 E 的秘密计划'
abbrlink: 2ec20435
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week4-Web 小 E 的秘密计划

知识点：

### 1. git相关

- **分支 (Branch)**：在 Git 内部，分支指向当前最新的 Commit 对象。
- **HEAD指针**：它指向你当前正在工作的分支文件。
- **Git Reflog**：记录的是 **HEAD 指针及其分支引用（refs）在本地更新的物理日志**。

---

小 E 最近在秘密研发一个代号为「Project X」的系统。然而，小 E  在开发和部署过程中，习惯性地留下了许多「不经意」的痕迹——无论是临时的备份，还是版本管理上的小疏忽，甚至是 Mac  系统自动生成的文件，都可能成为你解开「Project X」秘密的关键……

---

![image-20260326110952145](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326110952591.png)

御剑扫描找到备份网页url

![image-20260326100828571](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326100828751.png)

下载

![image-20260326100805458](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326100812660.png)

源代码：

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project X - 登录系统</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="floating-shapes">
        <div class="floating-shape shape-circle" style="top: 15%; left: 10%;"></div>
        <div class="floating-shape shape-ring" style="top: 40%; left: 85%;"></div>
        <div class="floating-shape shape-polygon" style="top: 70%; left: 20%;"></div>
    </div>

    
    <div class="login-container">
        <div class="login-box">
            <div class="login-logo">
                <h1>PROJECT X</h1>
                <p>系统访问认证</p>
                <p>tips: 默认密码使用uuid4生成，不可能被爆破</p>
            </div>
            
            <form id="login-form">
                <div class="input-group">
                    <label for="username">用户ID</label>
                    <input type="text" id="username" placeholder="输入您的用户ID">
                </div>
                
                <div class="input-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" placeholder="输入您的密码">
                </div>
                <div class="login-actions">
                    <a href="/" class="btn">返回首页</a>
                    <button type="button" class="btn btn-primary" id="login-btn">验证登录</button>
                </div>
                
                <div class="login-footer">
                    <p>版本 5.1.4</p>
                </div>
            </form>
        </div>
    </div>
    <script>
        document.getElementById('login-btn').addEventListener('click', function() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            fetch('login.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.text();
                }
            })
            .then(text => {
                if (text) {
                    alert(text);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    </script>
</body>
</html>
```

发现user.php，但是根本没有user.php，怎么找到账号密码呢

```
<?php
require_once 'user.php';
$userData = getUserData();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    if ($username === $userData['username'] && $password === $userData['password']) {
        header('Location: /secret-xxxxxxxxxxxxxxxxxxx');
        exit();
    } else {
        echo '登录失败,在git里找找吧';
        exit();
    }
}



```

直接在文件夹public-555edc76-9621-4997-86b9-01483a50293e内打开cmd，利用git log查找日志和记录，然后得到一些信息

了解到branch分支：

想找回**已经删除**的分支，该怎么做？

 ->情况：分支只是被删除了

1.查看日志

```
git reflog
```

**寻找目标**：在输出记录里找带有 `checkout: moving from <分支名> to <另一个分支名>` 或者 `commit: <信息>` 的记录。

**找回它**：找到那个分支最后一次活跃的 **Commit ID**（比如 `abc1234`）

2.直接重建分支：

```
git checkout -b <原分支名> abc1234
```



```
PS C:\Users\21709\Desktop\public-555edc76-9621-4997-86b9-01483a50293e> git log
commit 5fef682d7eceba025c894af4a5f8bf4680666368 (HEAD -> master)	//可以根据时间看出最后删除了什么
Author: admin <admin@admin.com>
Date:   Wed Oct 1 12:14:25 2025 +0800

    删除提示

commit 5f8ecc03aee0de892013bba7ce0522876c419b58
Author: admin <admin@admin.com>
Date:   Wed Oct 1 12:14:08 2025 +0800

    新增提示

commit 1389b4798a8013a1c90fb2d867243d0da18c5175
Author: admin <admin@admin.com>
Date:   Wed Oct 1 12:10:02 2025 +0800

    初始化
PS C:\Users\21709\Desktop\public-555edc76-9621-4997-86b9-01483a50293e> git show 5fef68	//我们找找看删除了啥
commit 5fef682d7eceba025c894af4a5f8bf4680666368 (HEAD -> master)
Author: admin <admin@admin.com>
Date:   Wed Oct 1 12:14:25 2025 +0800

    删除提示

diff --git a/tips.txt b/tips.txt
deleted file mode 100644
index a7fa1d9..0000000
--- a/tips.txt
+++ /dev/null
@@ -1 +0,0 @@
-tips：什么是branch	//这里提示了分支，那就去看看分支的日志，用git reflog查看
\ No newline at end of file
PS C:\Users\21709\Desktop\public-555edc76-9621-4997-86b9-01483a50293e> git reflog
5fef682 (HEAD -> master) HEAD@{0}: commit: 删除提示
5f8ecc0 HEAD@{1}: commit: 新增提示
1389b47 HEAD@{2}: checkout: moving from test to master
353b98f HEAD@{3}: commit: 测试，这个branch会删	//那我们就去看看删了啥
1389b47 HEAD@{4}: checkout: moving from master to test
1389b47 HEAD@{5}: commit (initial): 初始化
PS C:\Users\21709\Desktop\public-555edc76-9621-4997-86b9-01483a50293e> git checkout 353b98f	//查看
Note: switching to '353b98f'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 353b98f 测试，这个branch会删
PS C:\Users\21709\Desktop\public-555edc76-9621-4997-86b9-01483a50293e>
```

这时候你再重新打开文件夹就会发现多了个文件user.php

![image-20260326113707335](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326113707617.png)



![image-20260328200236540](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260328200236616.png)

那就拿着账号密码登陆吧

```
<?php

function getUserData() {
    return [
        'username' => 'admin',
        'password' => 'f75cc3eb-21e0-4713-9c30-998a8edb13de'
    ];
}
```



![image-20260326105222806](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326105223511.png)

登录得到

![image-20260326105201217](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326105201581.png)

提示是mac

### **.DS_Store ：**

1. **是啥**：macOS（苹果系统）自动生成的**隐藏文件**。
2. **存什么**：存文件夹的“显示设置”。比如图标大小、位置、窗口缩放等。
3. **安全隐患**：如果传到网站服务器，黑客可以下载它并**解析出你文件夹里所有的文件名**（包括隐藏的备份文件）。

------

那就是.DS_Store

打开看看

![image-20260326110609834](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326110610202.png)

得到一个文件txt，然后看到flag文件名了

![image-20260326110716250](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326110716464.png)

拿去到根目录下访问

![image-20260326110845878](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260326110846051.png)