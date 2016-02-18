#!/usr/bin/python
#coding:utf-8

import numpy as np
import math
import sys    
import os
import time
import matplotlib.pyplot as plt
from pprint import pprint
import matplotlib.animation as animation  
import cPickle as pickle
from copy import deepcopy

def load_coordiantes(file_path):
    with open(file_path, 'rb') as f:
        coordiantes_l = pickle.load(f)
    for coordiantes in coordiantes_l:
        yield coordiantes

def init2():
    cmd = ""
    cmd = cmd + "/usr/bin/ntpq -c peers & "
    cmd = cmd + "/usr/bin/ntpq -c assoc & "
    os.system(cmd) 


flag = 0

def main():
    try:
        start_time = float(sys.argv[1])
        #default time_unit 997
        time_unit = int(sys.argv[2])
    except:
         help_info = "Usage:%s <start_time> <time_unit(ms)>\n" % sys.argv[0]

    colors = ['b', 'g', 'r', 'c', 'm' , 'y', 'k', 'slategrey', 'orange', 
              'mediumblue', 'brown', 'orchid']
#     print(len(colors))
    file_path = './coordiantes_l'

    init2()
    coordiantes_iter = load_coordiantes(file_path)
    patchs = []
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)

    axes = plt.axes(xlim=(0, 3000), ylim=(0, 1500))
    axes.grid(True)
#     axes.set_xticks([0, 750, 1500, 2250, 3000])
#    axes.set_xticks(range(0, 3750, 375))
#    axes.set_yticks(range(0, 1750, 250))
    axes.set_xticks(range(0, 3750, 750))
    axes.set_yticks(range(0, 1750, 500))
    
    def init():
        global flag 
        if flag == 0:
            flag = 1
        else:
            return tuple(patchs)
        coordiantes = coordiantes_iter.next()
        print "只执行一次"
        print time.time()
        for index, coordiante in enumerate(coordiantes):
            i = index/5
#             if i >0: break
#             coordiante = [int(e) for e in coordiante]
            patch = plt.Circle(coordiante, radius=50, color=colors[i],alpha=0.5)
            patchs.append(patch)
            axes.add_patch(patch)
        axes.axis('equal')
        axes.margins(0)
        return tuple(patchs)
    
    def animate(i):
        try:
            coordiantes = coordiantes_iter.next()
        except:
            sys.exit(0)
        for index,coordiante in enumerate(coordiantes):
            patchs[index].center = coordiante
        return tuple(patchs)

    print "Waiting for starting"
    while time.time() < (start_time - 5):
        time.sleep(0.1)
    print "Start now!!!" 
    print time.time()
    #anim = animation.FuncAnimation(fig, animate, 
    #                           init_func=init, 
    #                            frames=360, 
    #                           interval=time_unit,
    #                           blit=True)
    #plt.title('IPLAB Community Mobility Models', fontsize=10)
    init()
    plt.xlabel('1500m')
    plt.ylabel('3000m')
    plt.show()

if __name__ == '__main__':
    main()
