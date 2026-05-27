---
title: '[b01lers2020]Welcome to Earth 1'
categories:
  - 
tags: []
abbrlink: 5dd1d6ba
date: 2026-03-01 19:56:46
---
# [b01lers2020]Welcome to Earth

# 1



发现有个快速跳过的/chase/文件

没有思路抓包看看/chase/文件

![image-20260301192606527](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301192606527.png)

很明显

**/leftt/**是多出来的，去看看

![image-20260301192754216](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301192754216.png)

黄线部分翻译过来是：你已经瞄准了障碍球，开杆吧

而下面的**/shoot/**刚好是射击的意思，呼应了

看看shoot

![image-20260301193006184](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193006184.png)

得到**/door/**

看**/door/**

```
    <button onClick="check_door()">Check</button>
```

我们看到了这个函数，但这个函数是啥

![image-20260301193327335](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193327335.png)

我们去js文件/static/js/door.js看看

![image-20260301193418728](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193418728.png)

找到了**/open/**

继续**/open/**

![image-20260301193513194](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193513194.png)

**How** **do** **you** **open** **it?**和**open(0);**

暗示我们去看看open是啥，不如看看js文件**/static/js/open_sesame.js**

![image-20260301193609840](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193609840.png)

当然继续看**/fight/**

![image-20260301193703329](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193703329.png)

查看js文件

![image-20260301193739423](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301193739423.png)

代审

scramble是炒蛋的意思？理解为翻炒，即打乱吧

```
// Run to scramble original flag
//console.log(scramble(flag, action));
function scramble(flag, key) {
  for (var i = 0; i < key.length; i++) {
    let n = key.charCodeAt(i) % flag.length;
    let temp = flag[i];
    flag[i] = flag[n];
    flag[n] = temp;
  }
  return flag;
}

function check_action() {
  var action = document.getElementById("action").value;
  var flag = ["{hey", "_boy", "aaaa", "s_im", "ck!}", "_baa", "aaaa", "pctf"];

  // TODO: unscramble function
}
```

其实不需要理解很多，这里`var flag = ["{hey", "_boy", "aaaa", "s_im", "ck!}", "_baa", "aaaa", "pctf"];`



只要排序一下就行

pctf{hey_boys_im_baaaaaaaaaack!}











当然可以选择脚本，格式肯定是pctf{hey      ck!}

剩下 "_boy", "aaaa", "s_im", "_baa", "aaaa"全排列即可

```
import itertools

word_list = ["_boy", "aaaa", "s_im", "_baa", "aaaa"]

# 使用 permutations 进行全排列
# r=4 表示从 5 个零件里选 4 个出来排列
combinations = list(itertools.permutations(word_list, 4))

print(f"总共有 {len(combinations)} 种组合，正在生成...\n")

for combo in combinations:
    # 将元组组合成字符串
    key = "".join(combo)
    flag = f"pctf{% raw %}{{hey{key}ck!}}{% endraw %}"
    
    # 打印出所有可能的 flag
    print(flag)
```



![image-20260301195643965](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260301195643965.png)