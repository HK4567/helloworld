#!/bin/python3
 
#打印等腰三角形

n = 20 #设置三角形高,实际为高的两倍

for _ in range(1,n,2): #
    print((n-_) * " ",_ * "*",end="")
    print((_-1) * "*")

