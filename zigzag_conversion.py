from collections import defaultdict


def convert(s: str, n: int) -> str:
    i = 0
    increasing = True
    result = defaultdict(str)
    for x in s:
        result[i] += x
        if i < n - 1 and increasing:
            i += 1
        elif i > 0:
            increasing = False
            i -= 1
            if i == 0:
                increasing = True
    r = ""
    for i in range(n):
        r += result[i]
    return r


print(convert("PAYPALISHIRING", 3))
