---
title: 'NewStar CTF 2025 Week2-搞点哦润吉吃吃🍊'
categories:
  - 
tags: []
abbrlink: 1e6d13ae
date: 2026-03-16 21:53:03
---

# NewStar CTF 2025 Week2-搞点哦润吉吃吃🍊



登录，账户密码在源代码

登陆后开始挑战，写脚本就行

先要知道几个重要信息，提示抓包，那抓包看看

![image-20260312101452624](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260312101459769.png)

说明start响应页面的setcookie会作为下面verify页面的session

这里不一样应该是因为过了几次我想到还有一个验证页面

![image-20260312101523876](https://cdn.jsdelivr.net/gh/2829750658t-svg/Screenshots@main/img/20260312101523949.png)

我们只需写一个脚本，满足：

从登陆后的响应中拿到session，和计算式子然后拿到计算结果去挑战



```
import requests


def auto_challenge():
    base_url = "http://127.0.0.1:17375"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": "session=eyJsb2dnZWRfaW4iOnRydWUsInVzZXJuYW1lIjoiRG9ybyJ9.abIkjg.T6Y6VWnRZT8jy9kWQljm8KME9qM",
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # 1. 启动挑战
        start_response = session.post(f"{base_url}/start_challenge")
        if start_response.status_code != 200:
            return

        # 2. 获取新的session cookie
        new_session_cookie = None
        if "Set-Cookie" in start_response.headers:
            set_cookie = start_response.headers["Set-Cookie"]
            if "session=" in set_cookie:
                new_session_cookie = set_cookie.split("session=")[1].split(";")[0]
                session.cookies.set("session", new_session_cookie)

        start_data = start_response.json()
        if "error" in start_data:
            return

        # 3. 获取表达式并计算token
        expression = start_data.get("expression", "")
        if not expression or "token =" not in expression:
            return

        calc_expr = expression.split("token =")[1].strip()
        token = eval(calc_expr)

        # 4. 提交验证
        submit_data = {"token": int(token)}
        submit_headers = (
            {"Cookie": f"session={new_session_cookie}"}
            if new_session_cookie
            else headers
        )

        submit_response = session.post(
            f"{base_url}/verify_token", json=submit_data, headers=submit_headers
        )
        print(submit_response.text)

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    auto_challenge()
```



计算逻辑：

```
expression 的内容是：
"token = (17158300 * 1000) ^ 54321"

    .split("token =")：以 token = 为分界点，把字符串切成两半。

        左半部分 [0]：" "

        右半部分 [1]：" (17158300 * 1000) ^ 54321"

    [1]：我们只要右边

    .strip()：把算式两头多余的空格删掉。

        结果 calc_expr 变成了："(17158300 * 1000) ^ 54321"
```


