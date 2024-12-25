#!/bin/python

'''这是一个批量ping域名的脚本'''

import time
import ping3

urls = []

'''通过文本导入需要ping的域名'''
with open("host.txt","r+") as file:
    f = file.readlines()

'''将域名后面的换行符去掉'''
for line in f:
    line = line.strip("\n")
    '''判断是否有注释符'''
    if line[:1] != "#":
        urls.append(line)
    else:
        pass

'''ping主代码'''
def ping():
    for url in urls:
        ping_time = ping3.ping(url)
        time.sleep(0)
        if ping_time != 0:            
            if ping_time != None:
                ping_time = ping_time*1000
                print(url,"%.3fms" %ping_time)
            else:
                print(url,"ping超时")
        else:
            print(url,"域名/IP不正确")

if __name__=="__main__":
    ping()