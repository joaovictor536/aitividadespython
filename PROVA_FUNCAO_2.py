def maior_numero(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

resultado = maior_numero(10, 5, 8)

print(resultado)
