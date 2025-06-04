#!/bin/python3
 
#打印等腰三角形

h = 20 #设置三角形高,实际为高的两倍

for _ in range(1,h,2): #
    print((h-_) * " ",_ * "*",end="")
    print((_-1) * "*")

