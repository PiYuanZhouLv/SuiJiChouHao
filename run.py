import os

while True:
    r = os.system('main')
    if r == 0:
        break
    print(f'意外退出: {r}({hex(r)})')
