---
title: 'NewStar CTF 2025 Week1 - 宇宙的中心是 PHP'
categories:
  - 
tags: []
abbrlink: f9aefca5
date: 2026-02-06 13:47:58
---
# NewStar CTF 2025 Week1 - 宇宙的中心是 PHP







![image-20260206122517783](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206122517783.png)





s3kret.php



```
 <?php
highlight_file(__FILE__);
include "flag.php";
if(isset($_POST['newstar2025'])){
    $answer = $_POST['newstar2025'];
    if(intval($answer)!=47&&intval($answer,0)==47){
        echo $flag;
    }else{
        echo "你还未参透奥秘";
    }
} 
```

重点：

```
intval($answer)!=47&&intval($answer,0)==47
```

->了解intval

PHP 中，`intval($value, $base)` 

- 如果 `$base` 是 `0`，PHP 会根据 `$value` 的**前缀**来决定使用哪种进制解析：

  - base无参数：默认按 **十进制** 解析。

  - 以 `0x` 或 `0X` 开头：按 **十六进制** 解析。

  - 以 `0` 开头：按 **八进制** 解析。

    

所以我们只要满足一个数他的十进制不是47，但是其他进制其中一个满足就ok

```
057
```

payload:newstar2025=057

![image-20260206123124960](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260206123124960.png)