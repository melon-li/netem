#!/usr/bin/python 
#coding:utf-8
import sys
import time

for i in range(11000):
    i = str(i)
    sys.stdout.write(i)
    sys.stdout.flush()
#    time.sleep(1)
    sys.stdout.write("\b"*len(i))
