def extended_gcd(a, b):
    """扩展欧几里得算法：返回 (gcd, x, y)，满足 a*x + b*y = gcd(a, b)"""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a // b) * y)

def mod_inverse(e, t):
    """求 e 关于模 t 的乘法逆元 d，即满足 (e*d) % t == 1 的 d"""
    g, x, y = extended_gcd(e, t)
    if g != 1:
        # 如果 e 和 t 不互质，则不存在逆元（RSA 中 e 和 t 必须互质）
        return None
    else:
        # 确保结果为正整数
        return x % t

# 已知参数
p = 473398607161
q = 4511491
e = 17
n = p * q
t = (p - 1) * (q - 1)

# 计算 d
d = mod_inverse(e, t)
print("d =", d)