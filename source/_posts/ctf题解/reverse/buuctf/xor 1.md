---
title: 'xor 1'
categories:
  - 
tags: []
abbrlink: ffea23e0
date: 2026-01-29 15:04:57
---
# xor

# 1





找到

```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+2Ch] [rbp-124h]
  char __b[264]; // [rsp+40h] [rbp-110h] BYREF

  memset(__b, 0, 0x100u);
  printf("Input your flag:\n");
  get_line(__b, 256);
  if ( strlen(__b) != 33 )
    goto LABEL_7;
  for ( i = 1; i < 33; ++i )
    __b[i] ^= __b[i - 1];
    
    //异或：b[i]=b[i]^b[i-1]
    
  if ( !strncmp(__b, global, '!') )
  	//你的输出要和global一摸一样
    printf("Success");
  else
LABEL_7:
    printf("Failed");
  return 0;
}
```

寻找global

看到

```
__cstring:0000000100000F6E aFKWOXZUPFVMDGH db 'f',0Ah              ; DATA XREF: __data:_global↓o
__cstring:0000000100000F70                 db 'k',0Ch,'w&O.@',11h,'x',0Dh,'Z;U',11h,'p',19h,'F',1Fh,'v"M#D',0Eh,'g'
__cstring:0000000100000F89                 db 6,'h',0Fh,'G2O',0
```

db是**Define Byte**



b为flag



**加密过程：** 

因为b[i] = b[i] ^ b[i-1]` ：` 

global[i] = flag原始[i] ^ global[i-1]

` (注：这里用 `global[i-1]` 是因为循环到 i 时，`b[i-1]` 已经变成了加密后的密文)



**反向推导解密：** 目标是求 `flag原始[i]`。

1. **等式建立：** `global[i] = flag原始[i] ^ global[i-1]`

2. **两边同时异或 `global[i-1]`：** 

   `global[i] ^ global[i-1] = flag原始[i] ^ global[i-1] ^ global[i-1]`

3. **根据异或特性（同数抵消）：** `global[i] ^ global[i-1] = flag原始[i]`

**结论：** 所以 **`flag[i] = global[i] ^ global[i-1]`**





脚本

```
target = [
    ord('f'), 0x0A, ord('k'), 0x0C, ord('w'), ord('&'), ord('O'), ord('.'), 
    ord('@'), 0x11, ord('x'), 0x0D, ord('Z'), ord(';'), ord('U'), 0x11, 
    ord('p'), 0x19, ord('F'), 0x1F, ord('v'), ord('"'), ord('M'), ord('#'), 
    ord('D'), 0x0E, ord('g'), 0x06, ord('h'), 0x0F, ord('G'), ord('2'), ord('O')
]
flag = ""
if len(target) > 0:
	flag += char(target[0])
	
	for i range(1,len(target)):
		flag += chr(target[i] ^ target[i-1])
		
print(flag)		

```

### tips:

1.`ord()` 是 Python 的一个内置函数，它的全称是 **ordinal**（序数）。

- **作用**：把**一个字符**转换成对应的**数字（ASCII 码 / Unicode）**。
- **为什么用它？**：因为我们要进行 `^`（异或）数学运算，**字符是没法直接计算的，必须先变成数字**。

### 最终：

得到flag{QianQiuWanDai_YiTongJiangHu}