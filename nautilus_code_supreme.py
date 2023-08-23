#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from multiprocessing import Pool




def common_function(j):
    os.chdir(j)
    os.system('/home/melisse/nautilus/nautilus >{}.log &'.format(j)) 
    

def start_pool(project_list):
    if __name__ == '__main__':
        p = Pool(processes=1)  # run no more than 10 at a time
        p.map(common_function,project_list)
        p.close()
        p.join()
        print 'workers=',p._processes


    
        
def nautilus_code_supreme(x):
    q = []
    m = [r for r in os.walk(x)]
    
    for i in m[1:]:
        if i[1]:
            #print i
            for j in i[1]:
                if j != 'ab' and j !='struct':
                    q.append(os.path.abspath(os.path.join(i[0],j)))
    #print q
    start_pool(q)
    
x = 'p'
nautilus_code_supreme(x)

    
            
        
