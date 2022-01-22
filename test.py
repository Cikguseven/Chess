def x(n):
    if n == 0:
        return 0
    else:
        return x(n // 2) + (n % 2)


for i in range(1, 17):
    print(x(i))
