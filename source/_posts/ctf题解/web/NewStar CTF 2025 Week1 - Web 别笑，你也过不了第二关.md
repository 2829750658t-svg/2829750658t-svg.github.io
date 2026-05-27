---
title: 'NewStar CTF 2025 Week1 - Web 别笑，你也过不了第二关'
categories:
  - 
tags: []
abbrlink: 190e486e
date: 2026-02-04 11:02:58
---
# NewStar CTF 2025 Week1 - Web 别笑，你也过不了第二关

直接看源代码

    let targetScores = [30, 1000000]; // 每关目标分数
    let currentLevel = 0; // 0 表示第一关

主要解题函数

```
if (score >= targetScores[currentLevel]) {
    alert(`恭喜通过第 ${currentLevel + 1} 关！得分: ${score}`);
    currentLevel++;
    if (currentLevel < targetScores.length) {
      // 下一关
      resetLevel(currentLevel);
      startGame();
    } else {
      // 全部通关
      gameEnded = true;
      const formData = new URLSearchParams();
formData.append("score", score);

      fetch("/flag.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: formData.toString()
})
.then(res => res.text())
.then(data => {
  alert("服务器返回:\n" + data);
})
.catch(err => {
  alert("请求失败: " + err);
});
    }
  } else {
    alert(`第 ${currentLevel + 1} 关未达成目标分数 (目标: ${targetScores[currentLevel]})，将重新开始本关！`);
    resetLevel(currentLevel);
    startGame();
  }
}

```

如果直接访问flag.php呢？

![image-20260203205852981](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203205852981.png)

如果直接传参

![image-20260203205940145](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260203205940145.png)