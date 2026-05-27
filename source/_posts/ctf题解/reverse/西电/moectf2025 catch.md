---
title: 'moectf2025 catch'
categories:
  - 
tags: []
abbrlink: 950d76bc
date: 2026-03-01 13:08:36
---
# moectf2025 catch

## 知识点：

### 1.ROT13

ROT13 的全称是 **Rotate by 13 places**（循环右移13位）。

字母表一共有 26 个字母，13 恰好是它的一半。这个加密方法就是把字母表对折：

- **A** 变成第 14 个字母 **N**
- **B** 变成第 15 个字母 **O**
- ...以此类推

**它的特点是：**

- **对称性**：如果你对一个词做两次 ROT13，它就会变回原样。
- **只换字母**：数字（如 `4`）、符号（如 `{`、`_`）完全不受影响。

## 题目提示：

IDA pro 9.0 推出了针对 [C++ exception](https://hex-rays.com/blog/unveiling-ida-pro-9-0-c-exceptions-support-in-the-decompiler) 的优化

但是这并不意味着所有的 try catch 都能被正确反编译

---

查找字符串发现了疑似flag的字符串还有一个try to catch me

.data:0000000140027120	00000027	C	zbrpgs{F4z3_Ge1px_jvgu_@sybjre_qrfhjn}



既然题目提示了catch，我们去找到try to catch me的位置，一探究竟



### try to catch me

```
 printf("try to catch me\n");
  v1 = strlen(flag);
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= v1 )
      break;
    flag[i] = enc(flag[i]);
  }
  return result;
}
```

enc是什么？

寻找enc，发现是异或

### enc

```
_int64 __fastcall enc(char a1)
{
  return (unsigned int)(a1 ^ 17);
}
```





zbrpgs{F4z3_Ge1px_jvgu_@sybjre_qrfhjn}

moectf{...}

->

`z` 的 ASCII 码是 **122**

`m` 的 ASCII 码是 **109**

122⊕109=23（这说明异或的不是 17，或者是经过了其他变换）



考虑移位

z` 对应 `m
b` 对应 `o

r` 对应 `e 

这其实是著名的 **ROT13** 加密（凯撒密码的一种，字母表位移 13 位）







### 脚本

####  代码逻辑

- `if 'a' <= char <= 'z':`
  - 检查这个字符是不是小写字母。
- `(ord(char) - ord('a') + 13) % 26 + ord('a')`
  - **`ord(char) - ord('a')`**：算出这个字母是第几个（比如 'a' 是 0，'b' 是 1）。
  - **`+ 13`**：向后数 13 个。
  - **`% 26`**：这是关键！如果数过了 26（超过了 'z'），就撞墙回头，从 'a' 重新开始数。
  - **`+ ord('a')`**：把数字变回真正的电脑字母编码。

```
cipher = "zbrpgs{F4z3_Ge1px_jvgu_@sybjre_qrfhjn}"


def rot13(data):
    result = ""
    for char in data:
        if "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + 13) % 26 + ord("a"))
        elif "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + 13) % 26 + ord("A"))
        else:
            result += char
    return result


print("--- ROT13 结果 ---")
print(rot13(cipher))

```





![image-20260225185440020](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260225185440020.png)

**最终结果：** `moectf{S4m3_Tr1ck_with_@flower_desuwa}`