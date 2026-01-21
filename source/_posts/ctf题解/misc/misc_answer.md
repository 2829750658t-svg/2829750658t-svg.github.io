---
title: "misc_answer"
date: 2026-01-21 19:39:43
categories: 默认分类
tags: [笔记]
---





bf6题解：

1.压缩包，放kali，有png，用bk

2.准备png开头 明文文件

echo 开头码 | xxd -r ps > 明文文件

3.得到密钥

bkcrack -C -c -p -o

4.解密压缩文件

bkcrack -C -c -k -d

5.发现图片有隐藏的10编码，steg打开得到乱码，图片comment里面有密钥，解码后flag



## 二维码

### 1



一个完整的 JPG 文件由 FF D8 开头，FF D9结尾
 在使用图片浏览器时，图片浏览器会忽略 FF D9 以后的内容，因此可以在 JPG 文件中加入其他文件。其他文件隐藏如png.gif文件隐藏也是这个道理。



```bash
# ========== 前期定位工具 & 切换工作目录 ==========
# 1. （尝试找bkcrack目录失败，改用全局查找工具路径）
which bkcrack  # 确认bkcrack路径：/usr/local/bin/bkcrack

# 2. 切换到桌面（二维码图片所在目录，核心工作目录）
cd ~/Desktop

# ========== 1. 从二维码中分离加密ZIP包 ==========
# 3. 用binwalk提取二维码中隐藏的ZIP数据
binwalk -e QR_code.png  # 分离出加密ZIP包（偏移0x1D7，对应文件1D7.zip）

# 4. 进入分离后的目录，查看并复制ZIP包到桌面
cd _QR_code.png.extracted  # 进入binwalk生成的提取目录
ls                         # 查看分离出的文件：1D7.zip
cp 1D7.zip ~/Desktop/      # 复制ZIP包到桌面（方便后续操作）
cd ~/Desktop               # 切回桌面



# 5.爆破密码，打开就ok





原来思路：
# ========== 2. 准备明文文件（bkcrack明文攻击用） ==========
# 5. 创建与ZIP内同名的空白文件（4number.txt）
touch 4number.txt

# ========== 3. 尝试bkcrack明文攻击（因ZIP包不完整报错，后改用爆破） ==========
# 6. 执行bkcrack明文攻击（报错：ZIP缺少目录尾签名）
bkcrack -C 1D7.zip -c 4number.txt -P ./ -p 4number.txt

# ========== 补充：你后续爆破1D7.zip的核心逻辑（可选命令） ==========
# （若用fcrackzip爆破4位数字密码，示例命令）
fcrackzip -b -l 4-4 -u 1D7.zip  # -b=爆破模式，-l 4-4=4位数字，-u=只显示正确密码
# 爆破成功后解压（假设密码为1234）
unzip -P 1234 1D7.zip  # -P指定密码，解压后查看4number.txt拿到flag
```







## 大白 1

1.发现图片太大，说们看不到全部，其实是图片的高被修改了，不信的话打开属性查看他的高

2、将图片放在010 Editor，修改图片宽高。我们来分析png文件格式，
首先，“89 50 4E 47 0D 0A 1A 0A”为标识png文件的八个字节的文件头标志。
然后是IHDR数据块，
“00 00 00 0D”说明IHDR头块长为13
”49 48 44 52“为IHDR标识（ASCII码为IHDR）

“00 00 02 A7”为图像的宽，24像素
”00 00 01 00“为图像的高，24像素
![image-20251217150833002](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251217150833002.png)

3.高也改成“00 00 02 A7”







## wireshark

### 1

这道题目是要分析流量，需要用到wireshark

1.使用http.request.method==POST命令进行过滤，得到一条流量

问题：为什么不用get？-->用户在登录密码时一般不会用[get](https://so.csdn.net/so/search?q=get&spm=1001.2101.3001.7020)方式提交，因为这样不安全，相比较而言post安全一点。

2.根据图片，点击分析，点击追踪流，选择http看到密码，即flag

![屏幕截图 2025-12-17 153428](C:\Users\21709\Pictures\Screenshots\屏幕截图 2025-12-17 153428.png)













## N种方法解决

### 1

1.exe改成txt，发现先开头什么jpg，base64，把逗号后面的全部base64解密

![image-20251217155500971](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251217155500971.png)







2.解密得到png文件`89 50 4E 47 0D`

https://the-x.cn/encodings/Base64.aspx

![image-20251217154521265](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251217154521265.png)



另外一种方法：010新建文件，edit-->pastefrom-->from base64

另起一行粘贴base原码，点击save，改后缀，得到二维码



![image-20251217155311781](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251217155311781.png)









## 数据包中的线索

### 1

​							 					

公安机关近期截获到某网络犯罪团伙在线交流的数据包，但无法分析出具体的交流内容，聪明的你能帮公安机关找到线索吗？ 注意：得到的 flag 请包上 flag{} 提交



1.WIRESHARK分析，看到有http，查看，发现有base64编码

2.解码得到jpg文件，看到flag

如果没有这中一件解码拿文件我们可以看到utf-8是乱码，试试16进制hex

![image-20251218212909920](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251218212909920.png)





发现ffd8ff的文件头，0110保存为图片就ok















## BUUCTF [BJDCTF2020]藏藏藏 1



1.0110发现有pk压缩包，还有个docx

![image-20251218214521489](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251218214521489.png)





2.kali打开

2.1解析

```
binwalk 图片.jpg  //解析得到存在zip
```

2.2分离

```
foremost 图片.jpg //分离得到图片中的压缩包，默认在output目录里面
```

2.3解压

```
unzip ./output/zip/文件名.zip   //得到 ：福利.docx
```

2.4查看

```
cat 福利.docx  //又发现pk文件头
```

2.5binwalk检测，发现很多压缩包

2.6foremost分离，此时加后缀-t，放在另一个output中

2.7tree ./新output

```
──(kali㉿kali)-[~/Desktop]
└─$ tree ./output_Thu_Dec_18_08_56_09_2025/zip 
./output_Thu_Dec_18_08_56_09_2025/zip
└── 00000000.zip

```

2.8 解压unzip ./output_Thu_Dec_18_08_56_09_2025/zip/00000000.zip

2.9 得到一张图片，打开是二维码，扫一就ok





![image-20251218220400272](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251218220400272.png)









## 文件中的秘密

### 1



![image-20251220163705385](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220163705385.png)









## 被嗅探的流量

### 1





![屏幕截图 2025-12-20 164112](C:\Users\21709\Pictures\Screenshots\屏幕截图 2025-12-20 164112.png)



















## 另外一个世界

### 1



![image-20251220164742430](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220164742430.png)



![image-20251220164954811](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220164954811.png)



![image-20251220164727740](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220164727740.png)















## FLAG

### 1





![image-20251220165504312](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220165504312.png)



1.steglove extract preview发现pk

​	   保存（save bin）为zip

2.解压出现名字为1的文件

3.改后缀txt或者010打开，即可查看





















![image-20251220174136448](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220174136448.png)





![image-20251220174526862](C:\Users\21709\AppData\Roaming\Typora\typora-user-images\image-20251220174526862.png)










