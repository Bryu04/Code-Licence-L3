#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np

def Classeur(x,input_dir,output_dir):
    header = '! time    log(Av)    log(n)    log(T)   \n ! (yr)   (mag)      (cm-3)    (K) '
    max = 4.69897
    cnt = 0
    for i in x:
        fn_in =  "{}/{}".format(input_dir,i) 
        f = open(fn_in,'r')
        f.readline()
        f.readline()
        for ligne in f:
            mots = ligne.split()
            a = float(mots[0])
            b = float(mots[1])
            c = float(mots[2])
            d = float(mots[3])
            if b >= max:
                cnt = cnt +1
                new_array = ref(i, input_dir)
                fn_out =  "{}/{}".format(output_dir,i) 
                print fn_out
                #print new_array
                np.savetxt(fn_out, new_array.T,fmt=('%.2E'))
                break
    print cnt    
def ref(x, input_dir):
    alist = []
    blist = []
    clist = []
    dlist = []
    fn_in =  "{}/{}".format(input_dir,x) 
    f = open(fn_in,'r')
    f.readline()
    f.readline()
    for ligne in f:
        mots = ligne.split()
        a = float(mots[0])
        b = float(mots[1])
        c = float(mots[2])
        d = float(mots[3])
        a = a*10**6
        alist.append(a)
        blist.append(b)
        clist.append(c)
        dlist.append(d)
    return np.array([alist,dlist,blist,clist])
	   
input_dir = 'clump_11'
output_dir = 'clump_11_reordered'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

filelist =  os.listdir(input_dir)
filelist = filelist[0:]
#print filelist

Classeur(filelist,input_dir, output_dir)