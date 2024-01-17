import math
import random

all = 2048*1088*121*121

sum = 0
# 四隅
for x in range(180):
    for y in range(180):
        a = (60 - math.floor(x/3))*61
        b = (60 - math.floor(y/3))*61
        c = (60 - math.floor(x/3))*(60 - math.floor(y/3))
        sum += a + b + c
sum *= 4

# 短辺端
for x in range(180):
    a = (60 - math.floor(x/3)) * 121 * (1088 - 180*2)
    sum += a * 2

# 長辺端
for y in range(180):
    b = (60 - math.floor(y/3)) * 121 * (2048 - 180*2)
    sum += b * 2

print(all, sum)
print(sum/all)
print(all - sum)

