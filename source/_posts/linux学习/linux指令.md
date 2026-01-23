---
title: linux指令
date: 2026-01-21 19:38:14
categories:
  - linux学习
tags: [linux命令]
---



## linux指令

**1.通用格式：command [-options] [parameter]**

1.command：命令本身

2.-options：命令选项，可控制命令的行为细节（可选）

3.parameter：命令参数，用于命令的指向目标（可选）

实例：

*ls -l/home/itheima 

 以列表的形式，显示/home/itheima目录内的内容

*cp -r test1 test2

 

 

**2.ls命令的参数和选项**

1.ls命令的参数

作用：指定查看文件夹（目录）的内容

若不给参数，查看的是 当前工作目录 的内容

/ ：根目录

2.ls命令的选项j

-a （all）展示隐藏内容（以.开头文件默认被隐藏，要用-a显示）

-l  以列表形式展示，并展示更多细节

-h 需和-l搭配用，人性化显示文件大小单位

 

命令的选项组合使用

例：ls-lah  =  ls -a -l -h

 

**3.cd pwd 命令**

1.cd：change directory

语法：cd [Linux路径]

cd无选项，只有参数，表示要切换到哪个目录下

cd直接执行，不写参数，表示回到用户的home目录s

![image-20260121191957243](/images/image-20260121191957243.png)



![image-20260121192021098](/images/image-20260121192021098.png)



2.pwd命令（print work directory）

直接用ls验证不恰当，用pwd查看当前的工作目录

语法：pwd （无需选项和参数，直接输入即可）

 

**4.相对路径 绝对路径 特殊路径符**

 

cd /home/itheima/desktop 绝对路径：以根目录为起点  有/

cd desktop              相对路径：以当前目录为起点 无/

 

特殊路径符

.  表示当前目录

.. 表示上一级目录

~ 表示home目录

![$1](/images/$2)

 

 

**5.创建目录命令**

 

**mkdir**命令（make directory）

语法：mkdir [-p] linux路径

1.参数必填，相对/绝对路径均可

2.-p可选填，表示自动创建不存在的父目录，是用于创建连续多层次的目录

例子：

mkdir bigtest

ls

 

mkdir /home/bigtest/test1

ls

 

mkdir ./test2

ls

 

cd Desktop

pwd

mkdir ../test3

cd ..

ls

 

mkdir ~/test4

ls

![image-20260121192125053](/images/image-20260121192125053.png)



3.创建文件夹要保证操作都在home内，超出无权限

 

**6.touch cat more 命令**

**题外话：CTRL+l  清空屏幕**

 

touch命令 创建文件

1.无选项，参数必填（路径），绝对、相对、特殊路径均可使用

 

cat命令 查看文件内容

语法：cat Linux路径

1.无选项，参数必填（被查看文件路径），绝对、相对、特殊路径均可使用

 

more命令 查看文件内容

语法：more Linux路径

1.无选项，参数必填（被查看文件路径），绝对、相对、特殊路径均可使用

2.与cat不同的是：

cat直接将内容全部显示出来

more支持翻页（通过空格翻页，通过q退出），若内容过多，可一页一页展示

 

**7.cp mv rm 命令**

 

**cp复制文件/文件夹 copy**

语法：cp [-r] 参数1 参数2

1.-r选项，可选，用于复制文件夹使用，表示递归

2.参数1：Linux路径，表示被复制文件或文件夹

3.参数2：Linux路径，表示要复制去哪

 

**mv移动文件/文件夹 move**

语法：mv 参数1 参数2

1.参数1：路径，表示被移动的文件/文件夹

2.参数2：表示要移动去的地方。若目标不存在，则将参数1进行改名，以确保目标存在

 

**rm删除文件/文件夹 remove**

语法：rm [-r -f] 参数1 参数2 ......参数N

1.-r用于删除文件夹。-f表示force，强制删除（不会弹出提示确认信息）

 普通用户删除内容不会弹出提示，只有root管理员用户删除才会有

2.参数1、参数2......参数N 表示要删除的文件或文件夹路径，按照空格隔开

 

**rm删除文件/文件夹-通配符**

 

rm命令支持通配符*，用来做模糊匹配

1.符号*表示通配符，即匹配容易内容（包括空）

例子：

test*，表示匹配任何以test开头的内容

*test，表示匹配任何以test结尾的内容

*test*，表示匹配任何包含test的内容

![image-20260121192233605](/images/image-20260121192233605.png)

**7.which find命令**

which命令

语法：which 要查找的命令

 

find命令-按文件名查找文件

语法：find 起始路径 -name ''被查找文件名''

 

find命令-通配符

同上

 

find命令-按文件大小查找文件

语法：find 起始路径 -size +/-n[kMG]

1.+、-表示 大于、小于

2.n表示大小数字

3.kMG表示大小单位，k（小写）表示kb，M表示MB，G表示GB

例子：find / -size =100k

 

题外话：CTRL+c 表示停止

 

 

**8.echo，tail，重定向符**

 

echo

语法：echo 输出内容

1.相当于print

2.复杂内容用“”

 

反引号  

无需选项，只有一个参数（表示要输出的内容，复杂内容可以用双引号包括）

作用：包围的内容作为命令去执行，而不是普通内容

例子：echo pwd  //输出pwd

echo `pwd`

行使命令

 

重定向符>和>>

\>   将左侧命令的结果，覆盖写入到符号右侧指定文件中

\>> 将左侧命令结果，追加写入到符号右侧指定文件中

 

 

 

**9.tail命令**

作用：查看文件尾部内容，跟踪文件的最新更改

语法：tail [-f -num] Linux路径

参数：表示Linux路径，表示被跟踪的文件

选项：-f，表示持续跟踪

选项：num，表示查看尾部多少行，不填默认10行

 

**10.grep命令**

语法： grep [-n] 关键字 文件路径

1.选项-n 可选 ，表示在结果中显示匹配的行的行号

2.参数，关键字，必填，表示过滤的关键字，若带有空格等其他特殊符号，建议使用“”

3.参数， 文件路径，必填，表示要过滤内容的文件路径，可作为内容输入端口

 

**10.wc命令 做数量统计**

1.语法： wc [-c -m -l -w] 文件路径

2.选项：

-c 统计bytes数量

-m 统计字符数量

-l 统计行数

-w 统计单词数量

3.参数：文件路径，被统计的文件，可作为内容输入端口

 

**12.管道符|**

1.含义：将管道符左边的命令结果，作为右边命令的输入

例子：

cat tes.text | grep f

cat tes.text | grep f | grep u



ls | grep test

 

**13.vi vim 编辑器**

1.使用命令：

vim 文件路径

若存在，打开；不存在，创建

2.命令：

i 在当前光标位置进入输入模式

a 在当前光标位置后，进入输入模式

I 在当前开进入输入模式

A 在当前行结尾，进入输入模式

o 当前光标下一行进入命令模式

O 当前光标上一行进入输入模式

esc 返回命令模式

![image-20260121192314419](/images/image-20260121192314419.png)



快捷键

![image-20260121192333909](/images/image-20260121192333909.png)

![image-20260121192349191](/images/image-20260121192349191.png)



底线命令模式：

:wq保存并退出

:q退出

:q!强制退出

:w保存

:set nu显示行号

:set paste设置粘贴模式

 

 

 

**13.用户和权限**

1.超级管理员：root

进入格式：

su - root 

 普通：在自己home内有权限

 

su命令

语法：su - 用户名

1.符号可选，建议带上

2.用户名省略表示切换到root

3.切换后，可以通过exit 或者 CTRL+d退回上一个用户

 

sudo命令

1.长时间使用root会有破坏，所以我们用sudo作为临时普通授权

2.语法：

sudo 其他命令

 

**14.用户和用户组管理**

用户组管理：

1.以下命令需要root用户执行

2.创建用户组：

groupadd 用户组名

3.删除

groupdel

 

15.用户管理：

1.创建用户：

useradd [-g -d] 用户名

-g：指定用户的组，不用会自动创建同名组

如果已经有同名组，必须使用-g

-d：指定用户home路径，不指定home'目录默认在：/home/用户名

2.删除

usedel [-r] 用户名

-r 删除用户的home目录，不使用不删除

3.查看用户所属组

id [用户名]

4修改用户所属组

usermod -aG 用户组 用户名

 

3.getent命令

1.可以查看当前系统中有哪些用户

语法：getent passwd

用户名：密码（x）：用户id：组id：描述信息（无用）

：home目录：执行终端（默认bash）

2.可以查看当前系统中有哪些组

语法：getent group

组名称：组认证（显示为x）：组id

 

认知权限信息

通过ls-l 可以以列表形式查看内容，并显示权限细节

1.权限细节

权限细节共10个槽位

举例：drwxr-xr-x

-/d/l r/- w/- x/- r/- w/- x/- r/- w/- x/-

​     用户权限    用户组权限  其他用户权限

第一槽位中：

d表示文件夹

l表示软链接

-表示文件

后续槽位中：

-表示无权限

 

r：read读权限（查看）

w：write写权限（文件：修改）（文件夹：创建 删除 改名）

x：执行权限（文件：可以将文件作为执行程序 ）（文件夹：可以更改工作目录到此文件夹，即 cd进入）

 

chmod修改权限信息（只有文件文件夹的所属用户或root可以修改）

1.语法：chmod [-R] 权限 文件或文件夹

举例：

chmod u=rmx,g=rx,o=x hello.txt

（其中：u表示user所属用户权限，g表示group组权限，o表示other其他用户权限）

chmod -R u=rwx,g=rx,o=x test 改后：rwxr-x--x

-R表示不仅修改它本身，把里面的文件都一起修改

chmod 751 hello.txt

![image-20260121192412310](/images/image-20260121192412310.png)

chown修改文件、文件夹的所属用户、用户组

 

普通用户无法修改，只能root

1.语法：chown [-R] [用户] [:] [用户组] 文件或文件夹

选项：

-R 同chmod，对文件夹内全部内容应用相同规则

用户：修改所属用户

用户组：修改所属用户组

：用于分隔用户和用户组

2.实例：

chown root：itheima hello.text

将hello.text所属用户改为root，所属用户组改为itheima

chown -R root test

将未见加test所属的用户修改为root，并对文件夹内全部内用应用同样规则

3.切换root

su -

 

 

快捷键：

1.CTRL+c 强制停止

2.CTRL+d 退出用户登录或退出程序

3.history：查看历史输入的命令

grep 筛选的东西

4.！

！p搜索离现在最近的跑开头的命令

5.ctrl a：跳到命令开头

6.ctrl e：跳到命令结尾

7.ctrl 左键：左跳一单词

8.ctrl 右键：右跳一单词

9.ctrl l：清屏

clear

 

 

软件管理器rpm的安装

yum/apt：联网自动化安装Linux软件，自动解决依赖问题

yum：centos

apt：debiansu （ubuntu）

1.语法：yum [-y] [install | remove | search] 程序名称

apt [-y] [install | remove | search] 程序名称

-y：不在询问

2.要求：

需要root权限：su/sudo提权

sudo su - root

需要联网

 

systemctl命令

0.目的：控制软件的启动和关闭

 服务：能够被这个命令管理的软件

例如：

NetworkManager主网络服务

network副网络服务

firewalld防火墙服务

sshd，ssh远程登陆

1.语法：

systemctl start | stop | status | enable | disable 服务名

1.1 status 查看状态

enable 开启开机自启

disable关闭开机自启

 

软连接（快捷方式）

ln命令创建软连接

1. 语法：

ln -s 参数1 ~参数2

-s 选项： 创建软连接

参数1 ： 被链接的文件或文件夹

参数2 ： 链接到哪里去

 

2. 例子

ln -s /etc/yum.conf ~/yum.conf

ln -s /etc/yum/ ~/yum 

 

 

日期和时区

 

 

1. date

通过date命令在命令行中查看系统时间

语法：date [-d] [+格式化字符串]

​        -d 按照给定字符串显示日期，一般用于日期计算

​        格式化字符：通过特定字符串标记，来控制显示的日期格式

1. %Y 年
2. %y 年份后2位（2006）：06 01-99
3. %m 月份   01-12
4. %d 日  01-31
5. %H  时00-23
6. %M min 00-59
7. %S s秒 00-60

%s 自1970-01-01 00：00：00 UT
